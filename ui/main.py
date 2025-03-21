import customtkinter as ctk
import sympy as sp
import pyperclip

# Initialize main window
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title("Derivative Solver")
root.geometry("500x500")

# Function to compute derivatives
def compute_derivative():
    expr_text = entry.get().replace(" ", "").replace("x", "*x").replace("(*x", "(x").replace("^", "**")
    order = int(order_entry.get()) if order_entry.get().isdigit() else 1
    try:
        x = sp.symbols('x')
        expr = sp.sympify(expr_text)
        derivative = sp.diff(expr, x, order)
        result = re.sub(r'(\d+)\*(x)', r'\1\2', str(derivative))  # 4*x → 4x
        result_label.configure(text=f"Result: {result}")

    except Exception as e:
        result_label.configure(text=f"Error: {e}")


# Function to copy result to clipboard
def copy_to_clipboard():
    pyperclip.copy(result_label.cget("text")[8:])

# Function to save result to a file
def save_to_file():
    with open("derivative_result.txt", "w") as file:
        file.write(result_label.cget("text")[8:])

# Function to insert text into entry field
def insert_text(text):
    replacements = {
        "sin(x)": "sp.sin(x)",
        "cos(x)": "sp.cos(x)",
        "tan(x)": "sp.tan(x)",
        "π": "sp.pi",
        "log(x)": "sp.log(x)"
    }
    text = replacements.get(text, text)  # Replace if in dictionary
    entry.insert(entry.index(ctk.INSERT), text)



# UI Elements
entry = ctk.CTkEntry(root, placeholder_text="Enter function in terms of x", width=300)
entry.pack(pady=10)

order_entry = ctk.CTkEntry(root, placeholder_text="Order of derivative (1, 2, 3, etc.)", width=300)
order_entry.pack(pady=10)

# Result label
result_label = ctk.CTkLabel(root, text="Result: ")
result_label.pack(pady=10)

# Buttons Frame
buttons_frame = ctk.CTkFrame(root, fg_color="transparent")
buttons_frame.pack(pady=5)

# Keypad layout
keypad = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "x", "+"]
]

for row in keypad:
    row_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent")
    row_frame.pack(pady=5)
    for char in row:
        btn = ctk.CTkButton(row_frame, text=char, width=100, command=lambda c=char: insert_text(c))
        btn.pack(side=ctk.LEFT, padx=5)

# Special function buttons
special_buttons = [
    ["sin(x)", "cos(x)", "tan(x)", "π"],
    ["√(", "^", "|x|", "log(x)"],
    ["(", ")", ",", "ans"]
]

for row in special_buttons:
    row_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent")
    row_frame.pack(pady=5)
    for func in row:
        btn = ctk.CTkButton(row_frame, text=func, width=100, command=lambda f=func: insert_text(f))
        btn.pack(side=ctk.LEFT, padx=5)

# Control buttons
control_frame = ctk.CTkFrame(root, fg_color="transparent")
control_frame.pack(pady=5)

enter_button = ctk.CTkButton(control_frame, text="Enter", width=100, command=compute_derivative)
enter_button.pack(side=ctk.LEFT, padx=5)

copy_button = ctk.CTkButton(control_frame, text="Copy", command=copy_to_clipboard)
copy_button.pack(side=ctk.LEFT, padx=5)

save_button = ctk.CTkButton(control_frame, text="Save", command=save_to_file)
save_button.pack(side=ctk.LEFT, padx=5)



root.mainloop()
