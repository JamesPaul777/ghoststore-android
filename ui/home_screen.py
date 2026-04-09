from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", padding=40, spacing=20)

        title = Label(
            text="GhostStore",
            font_size="32sp",
            bold=True,
            size_hint=(1, 0.3)
        )

        subtitle = Label(
            text="Steganographic File Storage",
            font_size="16sp",
            color=(0.6, 0.6, 0.6, 1),
            size_hint=(1, 0.15)
        )

        btn_hide = Button(
            text="Hide a File",
            font_size="18sp",
            size_hint=(1, 0.15),
            background_color=(0.2, 0.6, 1, 1)
        )
        btn_hide.bind(on_press=lambda x: self.go_to("hide"))

        btn_reveal = Button(
            text="Reveal a File",
            font_size="18sp",
            size_hint=(1, 0.15),
            background_color=(0.2, 0.8, 0.4, 1)
        )
        btn_reveal.bind(on_press=lambda x: self.go_to("reveal"))

        btn_vault = Button(
            text="Vault",
            font_size="18sp",
            size_hint=(1, 0.15),
            background_color=(0.6, 0.2, 0.8, 1)
        )
        btn_vault.bind(on_press=lambda x: self.go_to("vault"))

        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(btn_hide)
        layout.add_widget(btn_reveal)
        layout.add_widget(btn_vault)

        self.add_widget(layout)

    def go_to(self, screen_name):
        self.manager.current = screen_name