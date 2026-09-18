import customtkinter as ctk

class SettingsView(ctk.CTkFrame):
    def __init__(self, master, app, accent_color, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="transparent", **kwargs)
        self.app = app
        self.accent_color = accent_color

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.card = ctk.CTkFrame(
            self, width=420, height=360, 
            corner_radius=24, fg_color="#0d0d14", 
            border_width=1, border_color="#1c1c28"
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)

        self._build_card()

    def _build_card(self):
        self.title = ctk.CTkLabel(
            self.card, text="SETTINGS", 
            font=ctk.CTkFont(family="Minecraft", size=18, weight="bold"),
            text_color="#f4f4f6"
        )
        self.title.pack(pady=(28, 20))

        # --- RAM SLIDER SECTION ---
        ram_val = self.app.config.get("ram_gb", 2)
        
        self.ram_label = ctk.CTkLabel(
            self.card, text=f"Allocated RAM: {ram_val} GB",
            font=ctk.CTkFont(family="Minecraft", size=12, weight="bold"),
            text_color="#8888a0"
        )
        self.ram_label.pack(pady=(0, 6))

        self.ram_slider = ctk.CTkSlider(
            self.card, from_=1, to=16, number_of_steps=15,
            width=300, progress_color=self.accent_color,
            command=self._on_ram_change
        )
        self.ram_slider.set(ram_val)
        self.ram_slider.pack(pady=(0, 24))

        # --- CLOSE ON LAUNCH TOGGLE ---
        close_on_launch_val = self.app.config.get("close_on_launch", False)

        self.close_switch = ctk.CTkSwitch(
            self.card, text="Close Launcher when Game Spawns",
            font=ctk.CTkFont(family="Minecraft", size=12, weight="bold"),
            text_color="#f4f4f6", progress_color=self.accent_color,
            command=self._on_close_toggle
        )
        if close_on_launch_val:
            self.close_switch.select()
        else:
            self.close_switch.deselect()
            
        self.close_switch.pack(pady=(0, 20))

    def _on_ram_change(self, value):
        ram_gb = int(value)
        self.ram_label.configure(text=f"Allocated RAM: {ram_gb} GB")
        self.app.config["ram_gb"] = ram_gb
        self.app.config_mgr.save_config(self.app.config)

    def _on_close_toggle(self):
        is_enabled = bool(self.close_switch.get())
        self.app.config["close_on_launch"] = is_enabled
        self.app.config_mgr.save_config(self.app.config)