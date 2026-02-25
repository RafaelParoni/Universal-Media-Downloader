import customtkinter as ctk
import json

app = ctk.CTk()
app.geometry("400x400")
sf = ctk.CTkScrollableFrame(app)
sf.grid(row=0, column=0, sticky="nsew")

info = sf._parent_canvas.grid_info()
clean_info = {k: v for k, v in info.items() if isinstance(v, (int, str, float))}
with open("scroll_info2.json", "w") as f:
    json.dump(clean_info, f, indent=4)

app.destroy()
