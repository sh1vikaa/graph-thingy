import streamlit as st
import numpy as np
import plotly.graph_objs as go

# Title
st.title("🌊 3D Wave Visualizer")
st.markdown("Visualize complex functions in 3D with time-based dynamics.")

# Define functions
def func1(x, y, t):
    return np.sin(x + t) + np.cos(y + t), np.cos(x + t) - np.sin(y + t)

def func2(x, y, t):
    return np.sin(x + t) * np.cos(y + t), np.cos(x + t) * np.sin(y + t)

# Function switch
functions = {
    "Sin + Cos": func1,
    "Sin * Cos": func2
}

# Sidebar controls
st.sidebar.header("🎛 Controls")
selected_function = st.sidebar.radio("Choose Function:", list(functions.keys()))
t = st.sidebar.slider("Time (t)", 0.0, 10.0, 1.0, step=0.1)
real_min = st.sidebar.slider("Real Min", -20.0, 0.0, -10.0)
real_max = st.sidebar.slider("Real Max", 0.0, 20.0, 10.0)
imag_min = st.sidebar.slider("Imaginary Min", -20.0, 0.0, -10.0)
imag_max = st.sidebar.slider("Imaginary Max", 0.0, 20.0, 10.0)

# Grid setup
x = np.linspace(real_min, real_max, 100)
y = np.linspace(imag_min, imag_max, 100)
X, Y = np.meshgrid(x, y)

# Get selected function
func = functions[selected_function]
Z_real, Z_imag = func(X, Y, t)

# 3D plot using Plotly
fig = go.Figure()

# Surface for real part
fig.add_trace(go.Surface(
    x=X, y=Y, z=Z_real,
    colorscale='Viridis',
    name='Real Part',
    showscale=False
))

# Scatter for imaginary part (colored dots)
fig.add_trace(go.Scatter3d(
    x=X.flatten(),
    y=Y.flatten(),
    z=Z_real.flatten(),
    mode='markers',
    marker=dict(
        size=2,
        color=Z_imag.flatten(),
        colorscale='RdBu',
        opacity=0.6,
        colorbar=dict(title="Imaginary")
    ),
    name="Imaginary"
))

# Layout
fig.update_layout(
    title=f"Function: {selected_function} | Time = {t:.2f}",
    scene=dict(
        xaxis_title="Real Axis",
        yaxis_title="Imaginary Axis",
        zaxis_title="Z (Output)"
    ),
    height=750,
    margin=dict(l=0, r=0, b=0, t=50)
)

# Show plot
st.plotly_chart(fig, use_container_width=True)
