import os
import cv2
import PIL.Image, PIL.ImageTk
import customtkinter as ctk

class CanvasBackground(ctk.CTkCanvas):
    def __init__(self, master, accent_color="#615251", **kwargs):
        super().__init__(master, highlightthickness=0, bg="#0b0b0f", **kwargs)
        self.accent_color = accent_color
        
        video_path = os.path.join(os.getcwd(), "background.mp4")
        self.vid = cv2.VideoCapture(video_path) if os.path.exists(video_path) else None
        
        self.image_id = None
        
        if self.vid and self.vid.isOpened():
            self._update_frame()
        else:
            self.create_text(375, 220, text="background.mp4 not found in root folder", fill="#ef4444", font=("Segoe UI", 12))

    def _update_frame(self):
        if not self.vid or not self.vid.isOpened():
            return

        ret, frame = self.vid.read()
        if not ret:
            self.vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.vid.read()

        if ret:
            width = self.winfo_width() or 750
            height = self.winfo_height() or 440
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = PIL.Image.fromarray(frame)
            image = image.resize((width, height), PIL.Image.Resampling.LANCZOS)
            
            self.photo = PIL.ImageTk.PhotoImage(image=image)
            
            if self.image_id:
                self.itemconfig(self.image_id, image=self.photo)
            else:
                self.image_id = self.create_image(0, 0, image=self.photo, anchor="nw")

        self.after(33, self._update_frame)

    def apply_accent(self, new_hex: str):
        self.accent_color = new_hex

    def destroy(self):
        if self.vid:
            self.vid.release()
        super().destroy()