import streamlit as st
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

st.title("Contour Plot of a Custom Equation")

# --- Input equation ---
st.markdown("### Enter your equation with '=' (e.g., `p**2 + q**2 = 4`).")
equation_input = st.text_input("Equation:", value="p**2 + q**2 = 4")

# --- Variable names ---
var1 = st.text_input("First variable name:", value="p")
var2 = st.text_input("Second variable name:", value="q")

# Dynamically define sympy symbols
try:
    sym1, sym2 = sp.symbols(f"{var1} {var2}")
except Exception as e:
    st.error(f"Invalid variable names: {e}")
    st.stop()

# --- Axis mapping ---
axis_choice_x = st.selectbox("Select variable for X-axis:", [var1, var2])
axis_choice_y = st.selectbox("Select variable for Y-axis:", [var1, var2])

x_label = st.text_input("Label for X-axis:", value=axis_choice_x)
y_label = st.text_input("Label for Y-axis:", value=axis_choice_y)

# --- Plot ranges ---
st.markdown("### Set plot ranges")
x_min = st.number_input("X-axis minimum:", value=-10.0)
x_max = st.number_input("X-axis maximum:", value=10.0)
y_min = st.number_input("Y-axis minimum:", value=-10.0)
y_max = st.number_input("Y-axis maximum:", value=10.0)

# --- Parse equation with '=' ---
try:
    if "=" in equation_input:
        left, right = equation_input.split("=")
        expr = sp.sympify(left) - sp.sympify(right)
    else:
        expr = sp.sympify(equation_input)

    st.latex(sp.latex(expr) + " = 0")  # Display in LaTeX
except Exception as e:
    st.error(f"Invalid equation: {e}")
    st.stop()

# --- Contour levels ---
levels_input = st.text_input("Contour levels (comma-separated, e.g. 0 or -1,0,1):", value="0")
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

# Apply axis mapping
if axis_choice_x == var1 and axis_choice_y == var2:
    Z = f(X_grid, Y_grid)
elif axis_choice_x == var2 and axis_choice_y == var1:
    Z = f(Y_grid, X_grid)
else:
    st.error("Axis mapping error.")
    st.stop()

# --- Plot contour ---
fig, ax = plt.subplots()
cp = ax.contour(X_grid, Y_grid, Z, levels=levels, colors="black")  # just contours
ax.clabel(cp, inline=True, fontsize=8)  # labels on contours
ax.set_xlabel(x_label)
ax.set_ylabel(y_label)
ax.set_title("Contour Plot")

st.pyplot(fig)
