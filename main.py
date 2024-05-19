from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
import json
from ollama import Client
EXTENSION_ICON = 'images/icon.png'

class DemoExtension(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        url = extension.preferences['url']
        prompt = event.get_argument()
        
        if not prompt:
            return RenderResultListAction([
                ExtensionResultItem(icon=EXTENSION_ICON,
                                    name='Type in a prompt...',
                                    on_enter=DoNothingAction())
            ])
        
        client = Client(host=url)
        response = client.generate(model=extension.preferences["dmodel"], prompt=prompt, stream=False)
        
        
        return RenderResultListAction([
            ExtensionResultItem(icon=EXTENSION_ICON,
                                name=response["response"],
                                on_enter=CopyToClipboardAction(response["response"]))
        ])

if __name__ == '__main__':
    DemoExtension().run()