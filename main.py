from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from pathlib import Path
import os

prefix = None
# TODO: Make Maximum visible options a user option
MAX_VIS_OPTIONS=8

def sort_by_basename(fname):
    return fname.name

class PassExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

# Runs when the text in the prompt is changed
class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        search_str = event.get_argument()
        if search_str:
            password_files = sorted(list(prefix.rglob(f'*{search_str}*.gpg')), key=sort_by_basename)
        else:
            password_files = sorted(list(prefix.rglob('*.gpg')), key=sort_by_basename)

        items = []
        for pfile in password_files:
            items.append(ExtensionResultItem(icon='images/file-earmark-lock.svg',
                                             name=f'{pfile.stem}',
                                             description=f'{pfile}'.replace(str(Path.home()), "~"),
                                             on_enter=ExtensionCustomAction(pfile)))
            if (len(items) >= MAX_VIS_OPTIONS):
                break

        return RenderResultListAction(items)

# Runs when the user submits an item
class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        # TODO: notify the user that the password has been copied
        pass_arg = str(event.get_data().relative_to(prefix)).replace('.gpg', '')
        pass_cmd = f'pass show -c {pass_arg} > /dev/null'.format(pass_arg)
        os.system(pass_cmd)

if __name__ == '__main__':
    prefix = Path(os.getenv('PASSWORD_STORE_DIR', '~/.password-store')).expanduser()
    PassExtension().run()
