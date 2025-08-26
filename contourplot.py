import streamlit as st
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

st.title("Multiple Equations Contour Plot (expr = 0)")

# --- Input multiple equations ---
equations_input = st.text_area(
    "Enter equations separated by semicolons (e.g. p**2 + q**2 = 4; q - p = 0):",
    value="p**2 + q**2 = 4; q - p = 0"
)

# --- Variables ---
var1 = st.text_input("First variable (X-axis):", value="p")
var2 = st.text_input("Second variable (Y-axis):", value="q")
sym1, sym2 = sp.symbols(f"{var1} {var2}")

# --- Plot ranges ---
x_min = st.number_input(f"{var1}-min:", value=-10.0)
x_max = st.number_input(f"{var1}-max:", value=10.0)
y_min = st.number_input(f"{var2}-min:", value=-10.0)
y_max = st.number_input(f"{var2}-max:", value=10.0)

# --- Resolution ---
resolution = st.number_input(
    "Grid resolution (points per axis, higher = smoother curves):",
    min_value=50,
    max_value=1000,
    value=400,
    step=50
)

# --- Grid ---
X = np.linspace(x_min, x_max, int(resolution))
Y = np.linspace(y_min, y_max, int(resolution))
X_grid, Y_grid = np.meshgrid(X, Y)

# --- Colors and line styles ---
colors = st.text_input("Colors (comma-separated, e.g. red,blue,green):", value="red,blue,green")
linestyles = st.text_input("Line styles (comma-separated, e.g. -,--,:)", value="-,--,:")
color_list = [c.strip() for c in colors.split(",")]
style_list = [s.strip() for s in linestyles.split(",")]

# --- Prepare figure ---
fig, ax = plt.subplots()

# --- Process each equation ---
equations = [eq.strip() for eq in equations_input.split(";") if eq.strip()]
for i, eq_str in enumerate(equations):
    # Parse equation into expr=0
    if "=" in eq_str:
        left, right = eq_str.split("=")
        expr = sp.sympify(left) - sp.sympify(right)
    else:
        expr = sp.sympify(eq_str)
    
    # Show equation in Streamlit LaTeX
    st.latex(sp.latex(expr) + " = 0")
    
    # Build numerical function
    f = sp.lambdify((sym1, sym2), expr, "numpy")
    Z = f(X_grid, Y_grid)
    
    # Choose color and line style (cycle if not enough)
    color = color_list[i % len(color_list)]
    linestyle = style_list[i % len(style_list)]
    
    # Plot contour (only the curve)
    cs = ax.contour(X_grid, Y_grid, Z, levels=[0], colors=color, linestyles=linestyle, linewidths=2)
    
    # Add LaTeX label for legend only if contour exists
    if cs.collections:
        latex_label = f"${sp.latex(expr)}=0$"
        for line in cs.collections:
            line.set_label(latex_label)

# --- Labels and legend ---
ax.set_xlabel(var1)
ax.set_ylabel(var2)
ax.set_title("Equations Contours")
ax.legend(loc="best", fontsize=10, fancybox=True)

st.pyplot(fig)
