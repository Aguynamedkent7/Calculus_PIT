import sympy as smp
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from formula import derivative, integral
from matplotlib.widgets import Slider, TextBox

def main():
    symbol = smp.symbols('x', real=True)
    a, b = 1, 10
    expr = "x**2/x**3"
    x = np.linspace(a, b, 100)
    lambdas = {
        "derivative": derivative.derivative_of_range(expr, symbol, a, b),
        "integral": integral.ub_integral_of_range(expr, symbol, a, b)
    }


    # create the plot
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)
    line1, = ax.plot(x, lambdas['derivative'](x), label='Derivative', color='blue')
    line2, = ax.plot(x, lambdas['integral'](x), label='Integral', color='green')
    ax.set_title(f'Derivative and Integral of the function {expr}')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.legend()
    ax.grid()

    ax_slider = plt.axes([0.25, 0.1, 0.65, 0.03])
    slider = Slider(ax_slider, 'Range', 1, 20, valinit=10, valstep=1)
    ax_textbox = plt.axes([0.2, 0.05, 0.65, 0.05])
    textbox = TextBox(ax_textbox, 'Function', initial=expr)

    def on_submit(text):
        expr = text
        lambdas['derivative'] = derivative.derivative_of_range(expr, symbol, a, b)
        lambdas['integral'] = integral.ub_integral_of_range(expr, symbol, a, b)
        line1.set_xdata(x)
        line2.set_xdata(x)
        line1.set_ydata(lambdas['derivative'](x))
        line2.set_ydata(lambdas['integral'](x))
        ax.set_title(f'Derivative and Integral of the function {text}')
        ax.relim()
        ax.autoscale_view()
        plt.draw()

    
    def update(val):
        new_range = slider.val
        x_new = np.linspace(1, new_range, 100)
        line1.set_xdata(x_new)
        line1.set_ydata(lambdas['derivative'](x_new))
        line2.set_xdata(x_new)
        line2.set_ydata(lambdas['integral'](x_new))
        ax.relim()
        ax.autoscale_view()
        plt.draw()

    slider.on_changed(update)
    textbox.on_submit(on_submit)
    plt.show() 

if __name__ == '__main__':
    main()