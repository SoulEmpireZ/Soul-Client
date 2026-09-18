import os
import ctypes
import customtkinter as ctk

from core.config_manager import ConfigManager
from core.launcher import MinecraftLauncher
from gui.components.sidebar import Sidebar
from gui.views.home_view import HomeView
from gui.views.settings_view import SettingsView

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            app_id = 'soulclient.minecraft.launcher.1.0'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        except Exception:
            pass

        try:
            icon_path = os.path.join("Assets", "icons", "logo.ico")
            if os.path.exists(icon_path):
                self.wm_iconbitmap(icon_path)
        except Exception as e:
            print(f"Skipped icon loading: {e}")

        font_path = os.path.join("Assets", "fonts", "Minecraft.ttf")
        if os.path.exists(font_path):
            ctk.FontManager.load_font(font_path)

        ctk.set_appearance_mode("dark")
        self.title("Soul Client")
        self.geometry("750x440")
        self.resizable(False, False)
        self.configure(fg_color="#0b0b0f")

        self.config_mgr = ConfigManager()
        self.config = self.config_mgr.load_config()
        self.launcher = MinecraftLauncher()

        self.accent_color = self.config.get("accent_color", "#615251")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.content_container = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content_container.grid(row=0, column=1, sticky="nsew")
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)

        self.views = {}
        self._init_views()

        self.sidebar = Sidebar(
            master=self,
            accent_color=self.accent_color,
            on_home_click=lambda: self.show_view("home"),
            on_settings_click=lambda: self.show_view("settings"),
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.show_view("home")

    def _init_views(self):
        self.views["home"] = HomeView(self.content_container, self, self.accent_color)
        self.views["home"].grid(row=0, column=0, sticky="nsew")

        self.views["settings"] = SettingsView(self.content_container, self, self.accent_color)
        self.views["settings"].grid(row=0, column=0, sticky="nsew")

    def show_view(self, view_name: str):
        if view_name in self.views:
            self.views[view_name].tkraise()
            self.sidebar.set_active_button(view_name)