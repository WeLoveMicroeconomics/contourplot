import streamlit as st
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

st.title("Contour Plot of a Custom Equation")

# --- Input equation ---
equation_input = st.text_input("Enter your equation (e.g., p**2 + q**2 = 4):", value="p**2 + q**2 = 4")

# --- Variable names ---
var1 = st.text_input("First variable (X-axis):", value="p")
var2 = st.text_input("Second variable (Y-axis):", value="q")

# Define sympy symbols
sym1, sym2 = sp.symbols(f"{var1} {var2}")

# --- Parse equation with '=' ---
try:
    if "=" in equation_input:
        left, right = equation_input.split("=")
        expr = sp.sympify(left) - sp.sympify(right)
    else:
        expr = sp.sympify(equation_input)

    st.latex(sp.latex(expr) + " = 0")
except Exception as e:
    st.error(f"Invalid equation: {e}")
    st.stop()

# --- Plot ranges ---
x_min = st.number_input(f"{var1}-axis minimum:", value=-10.0)
x_max = st.number_input(f"{var1}-axis maximum:", value=10.0)
y_min = st.number_input(f"{var2}-axis minimum:", value=-10.0)
y_max = st.number_input(f"{var2}-axis maximum:", value=10.0)

# --- Contour levels ---
levels_input = st.text_input("Contour levels (comma-separated, default 0):", value="0")
try:
    levels = [float(l.strip()) for l in levels_input.split(",")]
except Exception:
    st.error("Invalid levels format. Please enter numbers separated by commas.")
    st.stop()

# --- Create numerical function ---
f = sp.lambdify((sym1, sym2), expr, "numpy")

# --- Grid for plotting ---
X = np.linspace(x_min, x_max, 400)
Y = np.linspace(y_min, y_max, 400)
X_grid, Y_grid = np.meshgrid(X, Y)

# Evaluate expression
Z = f(X_grid, Y_grid)

# --- Plot contour ---
fig, ax = plt.subplots()
contours = ax.contour(X_grid, Y_grid, Z, levels=levels, colors="black")
ax.clabel(contours, inline=True, fontsize=8)
ax.set_xlabel(var1)
ax.set_ylabel(var2)
ax.set_title("Contour Plot")

st.pyplot(fig)
