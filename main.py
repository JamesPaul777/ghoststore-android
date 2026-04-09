from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from ui.home_screen import HomeScreen
from ui.hide_screen import HideScreen
from ui.reveal_screen import RevealScreen
from ui.vault_screen import VaultScreen


class GhostStoreApp(App):
    def build(self):
        self.title = "GhostStore"
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(HideScreen(name="hide"))
        sm.add_widget(RevealScreen(name="reveal"))
        sm.add_widget(VaultScreen(name="vault"))
        return sm


if __name__ == "__main__":
    GhostStoreApp().run()