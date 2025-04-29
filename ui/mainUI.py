import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
import sympy as smp
import numpy as np
import pyperclip
import matplotlib.pyplot as plt
from formula import derivative, integral, original_function
from matplotlib.widgets import Slider
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class DerivativeIntegralSolverApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.win_width = 1280
        self.win_height = 700
        self.title("Derivative/Integral Calculator")
        self.geometry(f"{self.win_width}x{self.win_height}")
        self.minsize(self.win_width, self.win_height)

        self.history = []
        self.history_window = None

        self.create_widgets()
        self.plot_graph()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)


    def create_widgets(self):
        # main frame
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(pady=20, padx=10, fill=ctk.BOTH, expand=True)

        # History frame
        self.history_frame = ctk.CTkFrame(self.main_frame, width=180, height=500)
        self.history_frame.pack(side=ctk.LEFT, padx=10, pady=10, fill=ctk.BOTH, expand=False, anchor="center")

        self.history_label = ctk.CTkLabel(self.history_frame, text="History", font=("Arial", 20))
        self.history_label.pack(pady=10)

        self.history_textbox = ctk.CTkTextbox(self.history_frame, width=180, height=450, state="disabled")
        self.history_textbox.pack(pady=10, padx=10, fill=ctk.BOTH, expand=True)
        
        # Graph frame
        self.graph_frame = ctk.CTkFrame(self.main_frame, width=600, height=500)
        self.graph_frame.pack(side=ctk.RIGHT, padx=10, pady=10, fill=ctk.BOTH, expand=True, anchor="center")

        # Calculator frame
        self.calculator_frame = ctk.CTkFrame(self.main_frame, width=50, height=500)
        self.calculator_frame.pack(side=ctk.LEFT, padx=10, pady=10, fill=ctk.Y, expand=False, anchor="center")

        

        # UI Elements
        self.header_label = ctk.CTkLabel(self.calculator_frame, text="Derivative/Integral Calculator", font=("Arial", 20))
        self.header_label.pack(pady=20)

        self.entry = ctk.CTkEntry(self.calculator_frame, placeholder_text="Enter function in terms of x", width=300)
        self.entry.pack(pady=10, anchor="center")

        self.order_entry = ctk.CTkEntry(self.calculator_frame, placeholder_text="Order of derivative (for derivatives; optional)", width=300)
        self.order_entry.pack(pady=10, anchor="center")
        
        self.active_entry = self.entry  # Default

        self.entry.bind("<FocusIn>", lambda e: self.set_active_entry(self.entry))
        self.order_entry.bind("<FocusIn>", lambda e: self.set_active_entry(self.order_entry))

        # Result label
        self.result_label = ctk.CTkLabel(self.calculator_frame, text="", font=("Arial", 14),compound="left", text_color="lightgreen", width=500, height=30, corner_radius=10, padx=10, pady=5) 
        self.result_label.pack(pady=10, anchor="w")


        # Buttons Frame
        self.buttons_frame = ctk.CTkFrame(self.calculator_frame, fg_color="transparent")
        self.buttons_frame.pack(pady=5, anchor="center", fill=ctk.BOTH, expand=False)

        # Keypad layout
        self.keypad = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "x", "+"]
        ]

        for row in self.keypad:
            self.row_frame = ctk.CTkFrame(self.buttons_frame, fg_color="transparent")
            self.row_frame.pack(pady=5)
            for char in row:
                self.btn = ctk.CTkButton(self.row_frame, text=char, width=80, command=lambda c=char: self.insert_text(c), corner_radius=20)
                self.btn.pack(side=ctk.LEFT, padx=5)

        # Special function buttons
        self.special_buttons = [
            ["sin(x)", "cos(x)", "tan(x)", "π"],
            ["sqrt(", "cbrt(", "x^2", "x^y",],
            ["(", ")", "e^x", "log(x)"],
        ]

        for row in self.special_buttons:
            self.row_frame = ctk.CTkFrame(self.buttons_frame, fg_color="transparent")
            self.row_frame.pack(pady=5)
            for func in row:
                self.btn = ctk.CTkButton(self.row_frame, text=func, width=80, command=lambda f=func: self.insert_text(f), corner_radius=20)
                self.btn.pack(side=ctk.LEFT, padx=5)

        # Control buttons
        self.control_frame = ctk.CTkFrame(self.buttons_frame, fg_color="transparent")
        self.control_frame.pack(pady=5, anchor="center")
        
        self.clear_button = ctk.CTkButton(self.control_frame,fg_color="#6e110a",hover_color="#FF6666", text="Clear", width=80, command=self.clear_text, corner_radius=20)
        self.clear_button.pack(side=ctk.LEFT, padx=5)
        
        self.copy_button = ctk.CTkButton(self.control_frame,fg_color="#6e110a",hover_color="#FF6666", text="Copy", command=self.copy_to_clipboard, width=80, corner_radius=20)
        self.copy_button.pack(side=ctk.LEFT, padx=5)

        self.save_button = ctk.CTkButton(self.control_frame,fg_color="green",hover_color="#66FF66", text="Save", command=self.save_to_file, width=80, corner_radius=20)
        self.save_button.pack(side=ctk.LEFT, padx=5)
        
        self.enter_button = ctk.CTkButton(self.control_frame,fg_color="green",hover_color="#66FF66", text="Enter", width=80, command=self.compute_derivative_and_integral, corner_radius=20)
        self.enter_button.pack(side=ctk.LEFT, padx=5)

    # Function to compute derivatives
    def compute_derivative_and_integral(self):
        expr_text = self.entry.get()
        self.order = int(self.order_entry.get()) if self.order_entry.get().isdigit() else 1
        text = ""
        try:
            x = smp.symbols('x')
            result_derivative = str(derivative.symbolic_derivative(expr_text, x, self.order))
            result_integral = str(integral.ub_integral(expr_text, x))
            text += f"Derivative: {result_derivative}\nIntegral: {result_integral}\n"
            self.result_label.configure(text=text)

            # Add the result to the history
            self.history.insert(0, f"Function: {expr_text}\n{text}")
            self.update_history_window()

        except Exception as e:
            print(e)
            self.result_label.configure(text=f"Error")

        try:
            self.plot_graph()
        except Exception as e:
            text += "Failed to plot graph"
            self.result_label.configure(text=text)
            print("Failed to plot graph. Might be due to taking the derivative of a constant or invalid syntax.")
            print(e)

            
    def update_history_window(self):
        """Update the embedded history text box."""
        self.history_textbox.configure(state="normal")  # Enable editing temporarily
        self.history_textbox.delete("1.0", ctk.END)  # Clear the text box
        self.history_textbox.insert("1.0", "\n".join(self.history))  # Add the history
        self.history_textbox.configure(state="disabled")  # Make it read-only again

            
    def set_active_entry(self, widget):
        self.active_entry = widget


    def clear_text(self):
        self.entry.delete(0, ctk.END)  
        self.order_entry.delete(0, ctk.END) 

    def center_window(Screen: ctk.CTk, width: int, height: int, scale_factor: float = 1.0):
        screen_width = Screen.winfo_screenwidth()
        screen_height = Screen.winfo_screenheight()
        x = int(((screen_width/2) - (width/2)) * scale_factor)
        y = int(((screen_height/2) - (height/2)) * scale_factor)
        return f"{width}x{height}+{x}+{y}"


    # Function to copy result to clipboard
    def copy_to_clipboard(self):
        pyperclip.copy(self.result_label.cget("text")[8:])

    # Function to save result to a file
    def save_to_file(self):
        with open("derivative_result.txt", "w") as file:
            file.write(self.result_label.cget("text")[8:])

    # Function to insert text into entry field
    def insert_text(self, text):
        replacements = {
            "x^2": "x**2",
            "x^y": "x**",
            "π": "pi",
            "e^x": "exp(x)",
        }
        text = replacements.get(text, text)  # Replace if in dictionary
       
        self.active_entry.insert(self.active_entry.index(ctk.INSERT), text)
        
    def plot_graph(self):
        if hasattr(self, "fig"):
            plt.close(self.fig)  # Close the matplotlib figure
        if hasattr(self, "graph_canvas"):
            self.graph_canvas.get_tk_widget().destroy() 
        if hasattr(self, "toolbar"):
            self.toolbar.destroy()

        # if there is input
        if len(res := self.entry.get().strip()) != 0:
            self.symbol = smp.symbols('x', real=True)
            self.a, self.b = 1, 100
            self.expr = res

            og_fn = smp.parse_expr(self.expr, {"x": self.symbol})
            self.order = int(self.order_entry.get()) if self.order_entry.get().isdigit() else 1
            self.x = np.linspace(self.a, self.b, 100)
            self.lambdas = {
                "original": original_function.plot_og_func,
                "derivative": derivative.numeric_derivative,
                "integral": integral.ub_integral_of_range
            } 

            # Create figure and axes directly
            self.fig = Figure(figsize=(5, 4), dpi=100)
            self.ax = self.fig.add_subplot(111)
            self.line1, = self.ax.plot(self.x, self.lambdas['derivative'](self.expr, self.symbol, self.a, self.b, self.order), label='Derivative', color='blue')
            self.line2, = self.ax.plot(self.x, self.lambdas['integral'](self.expr, self.symbol, self.x), label='Integral', color='green')
            self.line3, = self.ax.plot(self.x, self.lambdas['original'](self.expr, self.symbol, self.x), label='Original', color='black')
            self.ax.set_title(f'Derivative and Integral of the function {self.expr}')
            self.ax.set_xlabel('x')
            self.ax.set_ylabel('f(x)')
            self.ax.legend()
            self.ax.grid()

            self.graph_canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
            self.graph_canvas.draw()
    
            self.toolbar = NavigationToolbar2Tk(self.graph_canvas, self, pack_toolbar=False)
            self.toolbar.update() 
            self.toolbar.pack(side=ctk.BOTTOM, fill=ctk.BOTH)   

            axfreq = self.fig.add_axes([0.25, 0.01, 0.65, 0.03])
            self.slider = Slider(
                ax=axfreq,
                label='Range of x',
                valmin=self.a,
                valmax=self.b,
                valinit=5,
                valstep=1,
            )
            self.slider.on_changed(self.slider_update)
        else:
            # if no input, create a blank graph
            self.fig = Figure(figsize=(5, 4), dpi=100)
            self.ax = self.fig.add_subplot(111)
            self.ax.set_title(f'Derivative and Integral of the function')
            self.ax.set_xlabel('x')
            self.ax.set_ylabel('f(x)')
            self.ax.grid()

            self.graph_canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
            self.graph_canvas.draw()
    
            self.toolbar = NavigationToolbar2Tk(self.graph_canvas, self,)
            self.toolbar.update() 
            self.toolbar.pack(side=ctk.BOTTOM, fill=ctk.BOTH)   

        self.graph_canvas.get_tk_widget().pack(fill="both", expand=True, pady=10)


    def slider_update(self, val):
            self.b = self.slider.val
            self.x = np.linspace(1, self.b, 100)
            self.line1.set_xdata(self.x)
            self.line1.set_ydata(self.lambdas['derivative'](self.expr, self.symbol, self.a, self.b, self.order))
            self.line2.set_xdata(self.x)
            self.line2.set_ydata(self.lambdas['integral'](self.expr, self.symbol, self.x))
            self.line3.set_xdata(self.x)
            self.line3.set_ydata(self.lambdas['original'](self.expr, self.symbol, self.x))
            self.ax.relim()
            self.ax.autoscale_view()
            self.graph_canvas.draw()
            


    def on_closing(self):
        """Clean up resources and exit the application."""
        if hasattr(self, "slider"):
            self.slider.disconnect(self.slider_update)  # Disconnect the slider callback
        if hasattr(self, "fig"):
            plt.close(self.fig)  # Close the matplotlib figure
        if hasattr(self, "graph_canvas"):
            self.graph_canvas.get_tk_widget().destroy() 
        self.destroy()  # Destroy the Tkinter root window


def center_window(Screen: ctk.CTk, width: int, height: int, scale_factor: float = 1.0):
    """
        Centers the window to the main display/monitor
        Credits to HyperNylium for this function (https://github.com/HyperNylium)
    """
    screen_width = Screen.winfo_screenwidth()
    screen_height = Screen.winfo_screenheight()
    x = int(((screen_width/2) - (width/2)) * scale_factor)
    y = int(((screen_height/2) - (height/2)) * scale_factor)
    return f"{width}x{height}+{x}+{y}"


if __name__ == "__main__":
    app = DerivativeIntegralSolverApp()
    app._state_before_windows_set_titlebar_color = 'zoomed'
    app.geometry(center_window(app, app.win_width, app.win_height, app._get_window_scaling()))
    app.mainloop()
