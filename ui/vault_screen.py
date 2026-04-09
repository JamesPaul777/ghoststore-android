from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import threading
import os

from core.vault import Vault


class VaultScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        title = Label(
            text="Vault",
            font_size="26sp",
            bold=True,
            size_hint=(1, 0.08)
        )

        btn_refresh = Button(
            text="Refresh",
            font_size="15sp",
            size_hint=(1, 0.08),
            background_color=(0.2, 0.6, 1, 1)
        )
        btn_refresh.bind(on_press=lambda x: self.load_entries())

        self.scroll = ScrollView(size_hint=(1, 0.75))
        self.entries_layout = GridLayout(
            cols=1,
            spacing=8,
            size_hint_y=None
        )
        self.entries_layout.bind(
            minimum_height=self.entries_layout.setter("height")
        )
        self.scroll.add_widget(self.entries_layout)

        self.status_label = Label(
            text="",
            font_size="13sp",
            color=(0.6, 0.6, 0.6, 1),
            size_hint=(1, 0.05)
        )

        btn_back = Button(
            text="Back",
            font_size="15sp",
            size_hint=(1, 0.08),
            background_color=(0.4, 0.4, 0.4, 1)
        )
        btn_back.bind(on_press=lambda x: setattr(self.manager, "current", "home"))

        self.layout.add_widget(title)
        self.layout.add_widget(btn_refresh)
        self.layout.add_widget(self.scroll)
        self.layout.add_widget(self.status_label)
        self.layout.add_widget(btn_back)

        self.add_widget(self.layout)

    def on_enter(self):
        self.load_entries()

    def load_entries(self):
        self.status_label.text = "Loading..."
        threading.Thread(target=self._load_thread).start()

    def _load_thread(self):
        try:
            from android.storage import primary_external_storage_path
            db_path = os.path.join(
                primary_external_storage_path(), "GhostStore", "vault.db"
            )
            vault = Vault(db_path=db_path)
            entries = vault.list_entries()
            Clock.schedule_once(lambda dt: self._render_entries(entries))
        except Exception as e:
            Clock.schedule_once(
                lambda dt: setattr(self.status_label, "text", f"Error: {e}")
            )

    def _render_entries(self, entries):
        self.entries_layout.clear_widgets()

        if not entries:
            self.status_label.text = "No entries in vault."
            return

        for entry in entries:
            row = BoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=60,
                spacing=10
            )

            lbl = Label(
                text=f"{entry.get('filename', 'Unknown')}  |  {entry.get('created_at', '')}",
                font_size="13sp",
                size_hint=(0.85, 1),
                halign="left",
                valign="middle"
            )
            lbl.bind(size=lbl.setter("text_size"))

            row.add_widget(lbl)
            self.entries_layout.add_widget(row)

        self.status_label.text = f"{len(entries)} entry(s) found."