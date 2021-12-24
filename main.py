"""Used for getting the user's PASSWORD_STORE_DIR env var"""
import subprocess
from os import getenv
from pathlib import Path
from gi.repository import Notify
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction

# from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction

prefix = ""


def sort_by_basename(fname):
    """Takes Path objects, and returns their name so they may be sorted by list()"""
    return fname.name


class PassExtension(Extension):
    """Initializes the extension"""

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):
    """Runs when the text in the prompt is changed"""

    def on_event(self, event, extension):
        search_str = event.get_argument()
        if search_str:
            password_files = sorted(
                list(prefix.rglob(f"*{search_str}*.gpg")), key=sort_by_basename
            )
        else:
            password_files = sorted(list(prefix.rglob("*.gpg")), key=sort_by_basename)

        items = []
        for pfile in password_files:
            items.append(
                ExtensionResultItem(
                    icon="images/application-pgp-encrypted.svg",
                    name=f"{pfile.stem}",
                    description=f"{pfile}".replace(str(Path.home()), "~"),
                    on_enter=ExtensionCustomAction(pfile),
                )
            )
            if len(items) >= int(extension.preferences["max_display_lines"]):
                break

        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):
    """Runs when the user submits an item"""

    def on_event(self, event, extension):
        pass_arg = str(event.get_data().relative_to(prefix)).replace(".gpg", "")
        subprocess.call(["pass", "show", "-c", pass_arg])
        if extension.preferences["show_notification"] == "yes":
            Notify.Notification.new(
                f"Copied {pass_arg} to clipboard.",
                "Will clear in 45 seconds.",
                "object-unlocked",
            ).show()


if __name__ == "__main__":
    prefix = Path(getenv("PASSWORD_STORE_DIR", "~/.password-store")).expanduser()
    Notify.init("Pass for Ulauncher")
    PassExtension().run()
    Notify.uninit()
