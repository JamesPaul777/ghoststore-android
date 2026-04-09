from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
import threading
import os

from core.pipeline import run_hide_pipeline


class HideScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.secret_file = None
        self.carrier_file = None

        layout = BoxLayout(orientation="vertical", padding=30, spacing=15)

        title = Label(
            text="Hide a File",
            font_size="26sp",
            bold=True,
            size_hint=(1, 0.1)
        )

        self.lbl_secret = Label(
            text="No secret file selected",
            font_size="14sp",
            color=(0.7, 0.7, 0.7, 1),
            size_hint=(1, 0.08)
        )

        btn_pick_secret = Button(
            text="Select Secret File",
            font_size="16sp",
            size_hint=(1, 0.1),
            background_color=(0.2, 0.6, 1, 1)
        )
        btn_pick_secret.bind(on_press=self.pick_secret_file)

        self.lbl_carrier = Label(
            text="No carrier selected",
            font_size="14sp",
            color=(0.7, 0.7, 0.7, 1),
            size_hint=(1, 0.08)
        )

        btn_pick_carrier = Button(
            text="Select Carrier (PNG or WAV)",
            font_size="16sp",
            size_hint=(1, 0.1),
            background_color=(0.2, 0.6, 1, 1)
        )
        btn_pick_carrier.bind(on_press=self.pick_carrier_file)

        password_label = Label(
            text="Password:",
            font_size="14sp",
            size_hint=(1, 0.07),
            halign="left"
        )

        self.password_input = TextInput(
            hint_text="Enter encryption password",
            password=True,
            multiline=False,
            font_size="16sp",
            size_hint=(1, 0.1)
        )

        btn_hide = Button(
            text="Hide File",
            font_size="18sp",
            size_hint=(1, 0.12),
            background_color=(0.1, 0.7, 0.3, 1)
        )
        btn_hide.bind(on_press=self.run_hide)

        self.status_label = Label(
            text="",
            font_size="13sp",
            color=(0.5, 1, 0.5, 1),
            size_hint=(1, 0.15),
            text_size=(None, None),
            halign="center"
        )

        btn_back = Button(
            text="Back",
            font_size="15sp",
            size_hint=(1, 0.08),
            background_color=(0.4, 0.4, 0.4, 1)
        )
        btn_back.bind(on_press=lambda x: setattr(self.manager, "current", "home"))

        layout.add_widget(title)
        layout.add_widget(self.lbl_secret)
        layout.add_widget(btn_pick_secret)
        layout.add_widget(self.lbl_carrier)
        layout.add_widget(btn_pick_carrier)
        layout.add_widget(password_label)
        layout.add_widget(self.password_input)
        layout.add_widget(btn_hide)
        layout.add_widget(self.status_label)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    def pick_secret_file(self, instance):
        from android.storage import primary_external_storage_path
        from plyer import filechooser
        filechooser.open_file(on_selection=self.on_secret_selected)

    def on_secret_selected(self, selection):
        if selection:
            self.secret_file = selection[0]
            self.lbl_secret.text = f"Secret: {os.path.basename(self.secret_file)}"

    def pick_carrier_file(self, instance):
        from plyer import filechooser
        filechooser.open_file(
            on_selection=self.on_carrier_selected,
            filters=["*.png", "*.wav"]
        )

    def on_carrier_selected(self, selection):
        if selection:
            self.carrier_file = selection[0]
            self.lbl_carrier.text = f"Carrier: {os.path.basename(self.carrier_file)}"

    def run_hide(self, instance):
        if not self.secret_file:
            self.status_label.text = "Please select a secret file."
            return
        if not self.carrier_file:
            self.status_label.text = "Please select a carrier file."
            return
        if not self.password_input.text.strip():
            self.status_label.text = "Please enter a password."
            return

        self.status_label.text = "Processing..."
        threading.Thread(target=self._hide_thread).start()

    def _hide_thread(self):
        try:
            from android.storage import primary_external_storage_path
            output_dir = os.path.join(primary_external_storage_path(), "GhostStore", "output")
            os.makedirs(output_dir, exist_ok=True)

            result = run_hide_pipeline(
                secret_path=self.secret_file,
                carrier_path=self.carrier_file,
                password=self.password_input.text.strip(),
                output_dir=output_dir
            )
            Clock.schedule_once(lambda dt: self._on_success(result))
        except Exception as e:
            Clock.schedule_once(lambda dt: self._on_error(str(e)))

    def _on_success(self, result):
        self.status_label.text = f"✓ Done! Saved to GhostStore/output"
        self.status_label.color = (0.2, 1, 0.4, 1)

    def _on_error(self, error):
        self.status_label.text = f"Error: {error}"
        self.status_label.color = (1, 0.3, 0.3, 1)