import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("850x640")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar_frame = ctk.CTkScrollableFrame(self, width=240, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        for i in range(12):
            btn = ctk.CTkButton(self.sidebar_frame, text=f"Button {i}", height=40)
            btn.grid(row=i, column=0, padx=15, pady=8, sticky="ew")

        self.bind("<Configure>", self.on_resize)
    
    def on_resize(self, event):
        if event.widget == self:
            if self.winfo_height() < 600:
                self.sidebar_frame._scrollbar.grid(row=0, column=1, sticky="ns")
            else:
                self.sidebar_frame._scrollbar.grid_forget()
                if hasattr(self.sidebar_frame, '_parent_canvas'):
                    self.sidebar_frame._parent_canvas.yview_moveto(0)

if __name__ == "__main__":
    app = App()
    # just run for 2 seconds and exit for test
    app.after(500, lambda: app.geometry("850x500"))
    app.after(1000, lambda: app.geometry("850x700"))
    app.after(2000, app.destroy)
    app.mainloop()
