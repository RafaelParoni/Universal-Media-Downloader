import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x400")
        
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.pack(fill="both", expand=True)
        self.scroll_frame.grid_columnconfigure(0, weight=1)
        
        self.card = ctk.CTkFrame(self.scroll_frame, fg_color="gray20", corner_radius=25)
        self.card.grid(row=0, column=0, padx=40, pady=40, sticky="nsew")
        
        self.title_label = ctk.CTkLabel(self.card, text="Todos os Serviços", font=ctk.CTkFont(size=24))
        self.title_label.grid(row=0, column=0, pady=(40, 30))
        
        self.service_cards = []
        for i in range(14):
            c = ctk.CTkFrame(self.card, width=140, height=160, fg_color="blue", corner_radius=15)
            c.grid_propagate(False)
            self.service_cards.append(c)
            
        self.current_cols = 0
        self.scroll_frame.bind("<Configure>", self.reorganize_cards)
        
    def reorganize_cards(self, event):
        if event.widget == self.scroll_frame:
            available_width = event.width
            cols = max(1, available_width // 180) 
            
            if getattr(self, 'current_cols', 0) != cols:
                self.current_cols = cols
                self.title_label.grid(row=0, column=0, columnspan=cols, pady=(40, 30))
                for i in range(20):
                    self.card.grid_columnconfigure(i, weight=0)
                for i in range(cols):
                    self.card.grid_columnconfigure(i, weight=1)
                for idx, card in enumerate(self.service_cards):
                    row = 1 + (idx // cols)
                    col = idx % cols
                    card.grid(row=row, column=col, padx=15, pady=15)

if __name__ == "__main__":
    app = App()
    app.mainloop()
