import streamlit as st
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

st.title("Contour Plot of a Custom Equation")

# --- Input equation ---
st.markdown("### Enter your equation in terms of two variables (e.g., `x**2 + y**2`).")
equation_input = st.text_input("Equation:", value="x**2 + y**2")

# --- Define symbols dynamically ---
var1 = st.text_input("First variable name:", value="x")
var2 = st.text_input("Second variable name:", value="y")

# Sympy symbols
x, y = sp.symbols(f"{var1} {var2}")

# --- Select axis mapping ---
axis_choice_x = st.selectbox("Select variable for X-axis:", [var1, var2])
axis_choice_y = st.selectbox("Select variable for Y-axis:", [var1, var2])

x_label = st.text_input("Label for X-axis:", value=axis_choice_x)
y_label = st.text_input("Label for Y-axis:", value=axis_choice_y)

# --- Convert equation ---
try:
    expr = sp.sympify(equation_input)
    st.latex(sp.latex(expr))  # Display in LaTeX
except Exception as e:
    st.error(f"Invalid equation: {e}")
    st.stop()

# --- Create function for numerical evaluation ---
f = sp.lambdify((x, y), expr, "numpy")

# --- Grid for plotting ---
X = np.linspace(-10, 10, 400)
Y = np.linspace(-10, 10, 400)
X_grid, Y_grid = np.meshgrid(X, Y)

# Evaluate function safely
try:
    Z = f(X_grid, Y_grid)
except Exception as e:
    st.error(f"Could not evaluate function: {e}")
    st.stop()

# --- Plot contour ---
fig, ax = plt.subplots()
cp = ax.contourf(X_grid, Y_grid, Z, levels=30, cmap="viridis")
fig.colorbar(cp)
ax.set_xlabel(x_label)
ax.set_ylabel(y_label)
ax.set_title("Contour Plot")

st.pyplot(fig)
