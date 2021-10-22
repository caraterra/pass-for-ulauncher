from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from pathlib import Path
from os import getenv

prefix = None

class PassExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        items = []
        # for i in range(5):
        #     items.append(ExtensionResultItem(icon='images/file-earmark-lock.svg',
        #                                      name='Password %s' % i,
        #                                      description='This is password #%s' % i,
        #                                      on_enter=HideWindowAction()))
        return RenderResultListAction(items)

if __name__ == '__main__':
    prefix = Path(getenv('PASSWORD_STORE_DIR', '~/.password-store'))

    PassExtension().run()
