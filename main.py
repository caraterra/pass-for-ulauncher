from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from pathlib import *
from os import getenv

prefix = None

class PassExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

# Runs when the text in the prompt is changed
class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        password_files = list(prefix.rglob('*{}*.gpg'.format(event.get_argument())))
        items = []
        print(event.get_argument())
        for i in password_files:
            items.append(ExtensionResultItem(icon='images/file-earmark-lock.svg',
                                             name='{}'.format(i.stem),
                                             description='', # Put filepath here eventually
                                             on_enter=HideWindowAction()))
        return RenderResultListAction(items)

# Runs when the user submits an item
class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        pass # I'll need this later

if __name__ == '__main__':
    prefix = Path(getenv('PASSWORD_STORE_DIR', '~/.password-store')).expanduser()
    PassExtension().run()
