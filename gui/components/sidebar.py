import customtkinter as ctk

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, accent_color="#615251", on_home_click=None, on_settings_click=None, **kwargs):
        super().__init__(
            master, 
            width=180, 
            corner_radius=0, 
            fg_color="#0b0b0f",
            border_width=1,
            border_color="#181822",
            **kwargs
        )
        self.grid_propagate(False)

        self.accent_color = accent_color
        self.on_home_click = on_home_click
        self.on_settings_click = on_settings_click
        self.active_tab = "home"

        self._build_header()
        self._build_navigation()
        self._build_footer()

    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(30, 20), padx=20)

        self.logo = ctk.CTkLabel(
            header, text="SOUL", 
            font=ctk.CTkFont(family="Minecraft", size=20, weight="bold"),
            text_color=self.accent_color
        )
        self.logo.pack(anchor="w")

        self.sub = ctk.CTkLabel(
            header, text="Nothing ever last forever.", 
            font=ctk.CTkFont(family="Minecraft", size=9, weight="bold"),
            text_color="#6e6e82"
        )
        self.sub.pack(anchor="w", pady=(1, 0))

    def _build_navigation(self):
        self.nav_container = ctk.CTkFrame(self, fg_color="transparent")
        self.nav_container.pack(fill="x", padx=12)

        self.btn_home = self._create_nav_button("Play", self._handle_home_click)
        self.btn_settings = self._create_nav_button("Settings", self._handle_settings_click)

    def _create_nav_button(self, text, command):
        btn = ctk.CTkButton(
            self.nav_container,
            text=text,
            anchor="w",
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(family="Minecraft", size=12, weight="bold"),
            fg_color="transparent",
            hover_color="#161622",
            text_color="#6e6e82",
            command=command
        )
        btn.pack(fill="x", pady=4)
        return btn

    def _build_footer(self):
        status = ctk.CTkLabel(
            self, text="● 1.8.9 Ready", 
            font=ctk.CTkFont(family="Minecraft", size=10, weight="bold"),
            text_color="#4ade80"
        )
        status.pack(side="bottom", pady=20, anchor="w", padx=20)

    def _handle_home_click(self):
        self.set_active_button("home")
        if self.on_home_click: self.on_home_click()

    def _handle_settings_click(self):
        self.set_active_button("settings")
        if self.on_settings_click: self.on_settings_click()

    def set_active_button(self, tab_name: str):
        self.active_tab = tab_name
        
        if tab_name == "home":
            self.btn_home.configure(fg_color=self.accent_color, text_color="#ffffff", hover_color=self._darken(self.accent_color))
            self.btn_settings.configure(fg_color="transparent", text_color="#6e6e82", hover_color="#161622")
        else:
            self.btn_settings.configure(fg_color=self.accent_color, text_color="#ffffff", hover_color="#161622")
            self.btn_home.configure(fg_color="transparent", text_color="#6e6e82", hover_color="#161622")

    def apply_accent(self, new_hex: str):
        self.accent_color = new_hex
        self.logo.configure(text_color=self.accent_color)
        self.set_active_button(self.active_tab)

    def _darken(self, hex_color):
        try:
            h = hex_color.lstrip('#')
            r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
            return f"#{int(r*0.8):02x}{int(g*0.8):02x}{int(b*0.8):02x}"
        except: return "#555"