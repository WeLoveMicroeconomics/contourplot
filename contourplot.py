import streamlit as st
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

st.title("Equation Contour Plot")

# --- Input equation ---
equation_input = st.text_input("Enter equation (e.g. p**2 + q**2 = 4):", value="p**2 + q**2 = 4")

# --- Variables ---
var1 = st.text_input("First variable (X-axis):", value="p")
var2 = st.text_input("Second variable (Y-axis):", value="q")

sym1, sym2 = sp.symbols(f"{var1} {var2}")

# --- Parse equation with '=' ---
if "=" in equation_input:
    left, right = equation_input.split("=")
    expr = sp.sympify(left) - sp.sympify(right)
else:
    expr = sp.sympify(equation_input)

st.latex(sp.latex(expr) + " = 0")

# --- Plot ranges ---
x_min = st.number_input(f"{var1}-min:", value=-10.0)
x_max = st.number_input(f"{var1}-max:", value=10.0)
y_min = st.number_input(f"{var2}-min:", value=-10.0)
y_max = st.number_input(f"{var2}-max:", value=10.0)

# --- Build function ---
f = sp.lambdify((sym1, sym2), expr, "numpy")

# --- Grid ---
X = np.linspace(x_min, x_max, 400)
Y = np.linspace(y_min, y_max, 400)
X_grid, Y_grid = np.meshgrid(X, Y)
Z = f(X_grid, Y_grid)

# --- Contour plot (ONLY the equation curve) ---
fig, ax = plt.subplots()
cp = ax.contour(X_grid, Y_grid, Z, levels=[0], colors="red", linewidths=2)  # <<< KEY CHANGE
ax.set_xlabel(var1)
ax.set_ylabel(var2)
ax.set_title("Equation Contour")

st.pyplot(fig)
