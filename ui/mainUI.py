import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
import sympy as smp
import numpy as np
import pyperclip
import matplotlib.pyplot as plt
from formula import derivative, integral
from matplotlib.widgets import Slider
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


class DerivativeIntegralSolverApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.win_width = 1200
        self.win_height = 700
        self.title("Derivative/Integral Solver")
        self.geometry(f"{self.win_width}x{self.win_height}")
        self.minsize(self.win_width, self.win_height)

        self.create_widgets()
        self.plot_graph()
        # pack_toolbar=False will make it easier to use a layout manager later on.
        self.protocol("WM_DELETE_WINDOW", self.on_closing)


    def create_widgets(self):
        # main frame
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(pady=20, padx=20, fill=ctk.BOTH, expand=True)

        # Calculator frame
        self.calculator_frame = ctk.CTkFrame(self.main_frame, width=500, height=500)
        self.calculator_frame.pack(side=ctk.LEFT, padx=20, pady=20, expand=True, anchor="center")

        # Graph frame
        self.graph_frame = ctk.CTkFrame(self.main_frame, width=500, height=500)
        self.graph_frame.pack(side=ctk.LEFT, padx=10, pady=10, fill=ctk.BOTH, expand=True)

        # UI Elements
        self.header_label = ctk.CTkLabel(self.calculator_frame, text="Derivative/Integral Calculator", font=("Arial", 20))
        self.header_label.pack(pady=20)

        self.entry = ctk.CTkEntry(self.calculator_frame, placeholder_text="Enter function in terms of x", width=300)
        self.entry.pack(pady=10)

        self.order_entry = ctk.CTkEntry(self.calculator_frame, placeholder_text="Order of derivative (for derivatives; optional)", width=300)
        self.order_entry.pack(pady=10, anchor="center")

        # Result label
        self.result_label = ctk.CTkLabel(self.calculator_frame, text="")
        self.result_label.pack(pady=10)

        # Buttons Frame
        self.buttons_frame = ctk.CTkFrame(self.calculator_frame, fg_color="transparent")
        self.buttons_frame.pack(pady=5, anchor="center")

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
                self.btn = ctk.CTkButton(self.row_frame, text=char, width=100, command=lambda c=char: self.insert_text(c))
                self.btn.pack(side=ctk.LEFT, padx=5)

        # Special function buttons
        self.special_buttons = [
            ["sin(x)", "cos(x)", "tan(x)", "π"],
            ["sqrt(", "cbrt(", "^", "|x|",],
            ["(", ")", ",", "log(x)"],
        ]

        for row in self.special_buttons:
            self.row_frame = ctk.CTkFrame(self.buttons_frame, fg_color="transparent")
            self.row_frame.pack(pady=5)
            for func in row:
                self.btn = ctk.CTkButton(self.row_frame, text=func, width=100, command=lambda f=func: self.insert_text(f))
                self.btn.pack(side=ctk.LEFT, padx=5)

        # Control buttons
        self.control_frame = ctk.CTkFrame(self.calculator_frame, fg_color="transparent")
        self.control_frame.pack(pady=5, anchor="center")

        self.clear_button = ctk.CTkButton(self.control_frame, text="Clear", width=100, command=self.clear_text)
        self.clear_button.pack(side=ctk.LEFT, padx=5)

        self.enter_button = ctk.CTkButton(self.control_frame, text="Enter", width=100, command=self.compute_derivative_and_integral)
        self.enter_button.pack(side=ctk.LEFT, padx=5)

        self.copy_button = ctk.CTkButton(self.control_frame, text="Copy", command=self.copy_to_clipboard)
        self.copy_button.pack(side=ctk.LEFT, padx=5)

        self.save_button = ctk.CTkButton(self.control_frame, text="Save", command=self.save_to_file)
        self.save_button.pack(side=ctk.LEFT, padx=5)

    # Function to compute derivatives
    def compute_derivative_and_integral(self):
        expr_text = self.entry.get()
        self.order = int(self.order_entry.get()) if self.order_entry.get().isdigit() else 1
        try:
            x = smp.symbols('x')
            result_derivative = str(derivative.derivative(expr_text, x, self.order))
            result_integral = str(integral.ub_integral(expr_text, x))
            self.result_label.configure(
                text=f"Derivative: {result_derivative}\nIntegral: {result_integral}")
            self.plot_graph()

        except Exception as e:
            print(e)
            self.result_label.configure(text=f"Error")

    def clear_text(self):
        self.entry.delete(0, ctk.END)  
        self.order_entry.delete(0, ctk.END) 

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
            "^": "**",
            "π": "pi",
        }
        text = replacements.get(text, text)  # Replace if in dictionary
        self.entry.insert(self.entry.index(ctk.INSERT), text)

    def plot_graph(self):
        if hasattr(self, "fig"):
            plt.close(self.fig)  # Close the matplotlib figure
        if hasattr(self, "graph_canvas"):
            self.graph_canvas.get_tk_widget().destroy() 
        if hasattr(self, "toolbar"):
            self.toolbar.destroy()

        self.symbol = smp.symbols('x', real=True)
        a, b = 1, 10

        if len(res := self.entry.get().strip()) != 0:
            self.expr = res
        else:
            self.expr = "x**2"

        og_fn = smp.parse_expr(self.expr, {"x": self.symbol})
        self.order = int(self.order_entry.get()) if self.order_entry.get().isdigit() else 1
        self.x = np.linspace(a, b, 100)
        self.lambdas = {
            "original": smp.lambdify(self.symbol, og_fn, modules=['numpy']),
            "derivative": derivative.scipy_derivative_func(self.expr, self.symbol, a, b, self.order),
            "integral": integral.scipy_integral_func(self.expr, self.symbol, a, b)
        }

        # Create figure and axes directly
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.line1, = self.ax.plot(self.x, self.lambdas['derivative'](self.x), label='Derivative', color='blue')
        self.line2, = self.ax.plot(self.x, self.lambdas['integral'](self.x), label='Integral', color='green')
        self.line3, = self.ax.plot(self.x, self.lambdas['original'](self.x), label='Original', color='black')
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
            valmin=1,
            valmax=30,
            valinit=15,
            valstep=1,
        )
        self.slider.on_changed(self.slider_update)

        self.graph_canvas.get_tk_widget().pack(fill="both", expand=True, pady=10)


    def slider_update(self, val):
            new_range = self.slider.val
            x_new = np.linspace(1, new_range, 100)
            self.line1.set_xdata(x_new)
            self.line1.set_ydata(self.lambdas['derivative'](x_new))
            self.line2.set_xdata(x_new)
            self.line2.set_ydata(self.lambdas['integral'](x_new))
            self.line3.set_xdata(x_new)
            self.line3.set_ydata(self.lambdas['original'](x_new))
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
    y = int(((screen_height/2) - (height/1.5)) * scale_factor)
    return f"{width}x{height}+{x}+{y}"


if __name__ == "__main__":
    app = DerivativeIntegralSolverApp()
    # app.geometry(center_window(app, app.win_width, app.win_height, app._get_window_scaling()))
    app.mainloop()
