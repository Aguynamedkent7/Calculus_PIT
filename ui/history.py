import customtkinter as ctk


class CalculationHistoryWindow(ctk.CTkToplevel):
    def __init__(self, master, history):
        super().__init__(master)
        self.title("Calculation History")
        self.geometry("400x300")
        self.resizable(False, False)
        
        self.attributes("-topmost", True)

        self.history = history

        # Create a read-only text box to display the history
        self.text_box = ctk.CTkTextbox(self, width=380, height=280, state="disabled")
        self.text_box.pack(pady=10, padx=10, fill=ctk.BOTH, expand=True)

        # Populate the history initially
        self.update_history()

    def update_history(self):
        """Update the history text box with the latest calculations."""
        self.text_box.configure(state="normal")  # Enable editing temporarily
        self.text_box.delete("1.0", ctk.END)  # Clear the text box
        self.text_box.insert("1.0", "\n".join(self.history))  # Add the history
        self.text_box.configure(state="disabled")  # Make it read-only again