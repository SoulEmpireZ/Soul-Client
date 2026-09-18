import threading
import customtkinter as ctk
from gui.components.canvas_bg import CanvasBackground

class HomeView(ctk.CTkFrame):
    def __init__(self, master, app, accent_color, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="transparent", **kwargs)
        self.app = app
        self.accent_color = accent_color
        
        # --- LAUNCH LOCK STATE ---
        self.is_launching = False

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.bg = CanvasBackground(self, accent_color=self.accent_color)
        self.bg.grid(row=0, column=0, sticky="nsew")

        self.card = ctk.CTkFrame(
            self, width=340, height=320, 
            corner_radius=24, fg_color="#0d0d14", 
            border_width=1, border_color="#1c1c28"
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)

        self._build_card()

    def _validate_username(self, text):
        # Allows empty string (so backspace works) and enforces max 16 chars, letters/numbers/underscores only
        if len(text) <= 16 and all(c.isalnum() or c == '_' for c in text):
            return True
        return False

    def _build_card(self):
        self.title = ctk.CTkLabel(
            self.card, text="MINECRAFT 1.8.9", 
            font=ctk.CTkFont(family="Minecraft", size=18, weight="bold"),
            text_color="#f4f4f6"
        )
        self.title.pack(pady=(30, 18))

        # Register validation command with the top-level window
        vcmd = self.winfo_toplevel().register(self._validate_username)

        saved_user = self.app.config.get("username", "")
        self.username_entry = ctk.CTkEntry(
            self.card, placeholder_text="Enter Username",
            width=260, height=42, corner_radius=12,
            fg_color="#08080c", border_color="#1c1c28", border_width=1,
            text_color="#f4f4f6", placeholder_text_color="#525266", justify="center",
            font=ctk.CTkFont(family="Minecraft", size=13, weight="bold"),
            validate="key",
            validatecommand=(vcmd, "%P")
        )
        if saved_user: 
            self.username_entry.insert(0, saved_user)
        self.username_entry.pack(pady=(0, 14))

        self.play_btn = ctk.CTkButton(
            self.card, text="PLAY",
            width=260, height=44, corner_radius=12,
            font=ctk.CTkFont(family="Minecraft", size=14, weight="bold"),
            fg_color=self.accent_color,
            hover_color=self._darken(self.accent_color),
            text_color="#ffffff",
            command=self._on_play
        )
        self.play_btn.pack(pady=(0, 14))

        self.status_lbl = ctk.CTkLabel(
            self.card, text="Ready", 
            font=ctk.CTkFont(family="Minecraft", size=11), text_color="#8888a0"
        )
        self.status_lbl.pack()
    
    def _on_play(self):
        if self.is_launching:
            return

        username = self.username_entry.get().strip()
        if not username:
            self.update_status("Username required", "#ef4444")
            return
            
        # Enforce Minecraft's 3-16 character length requirement
        if not (3 <= len(username) <= 16):
            self.update_status("Username must be 3-16 chars", "#ef4444")
            return

        self.app.config["username"] = username
        self.app.config_mgr.save_config(self.app.config)

        self.is_launching = True
        self.play_btn.configure(state="disabled", text="LAUNCHING...")
        
        threading.Thread(target=self._launch, args=(username,), daemon=True).start()
        
    def _launch(self, username):
        try:
            ram = self.app.config.get("ram_gb", 2)
            
            process = self.app.launcher.launch(
                username=username, 
                ram_gb=ram, 
                status_callback=lambda m: self.after(0, self.update_status, m)
            )

            # Update UI to locked "LAUNCHED" state while game opens
            self.after(0, self._on_game_launched)

            # Stream logs and wait for process exit in background thread
            self._stream_and_wait(process)

            # When game closes, reset UI back to ready
            self.after(0, self._on_game_closed)

        except Exception as e:
            self._reset_ui()
            self.after(0, lambda err=e: self.update_status("Launch Error!", "#ef4444"))
            print(f"[Launch Exception]: {e}", flush=True)

    def _stream_and_wait(self, process):
        try:
            for line in iter(process.stdout.readline, ''):
                if not line:
                    break
                print(f"[Minecraft] {line.strip()}", flush=True)
            process.wait()
        except Exception as e:
            print(f"[Process Stream Error]: {e}", flush=True)

    def _on_game_launched(self):
        self.update_status("Game Running", "#4ade80")
        self.play_btn.configure(state="disabled", text="LAUNCHED")

    def _on_game_closed(self):
        self._reset_ui()
        self.update_status("Ready", "#8888a0")

    def _reset_ui(self):
        self.is_launching = False
        self.play_btn.configure(state="normal", text="PLAY")

    def update_status(self, text, color="#8888a0"):
        self.status_lbl.configure(text=text, text_color=color)

    def _darken(self, hex_color):
        try:
            h = hex_color.lstrip('#')
            r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
            return f"#{int(r*0.8):02x}{int(g*0.8):02x}{int(b*0.8):02x}"
        except Exception: 
            return "#555"