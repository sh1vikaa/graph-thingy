import streamlit as st
import numpy as np
import plotly.graph_objs as go

st.set_page_config(layout="wide")
st.title("🌊 Interactive 3D Wave Visualizer (Streamlit + Plotly)")

# --- Function Definitions ---
def func1(x, y, t):
    return np.sin(x + t) + np.cos(y + t), np.cos(x + t) - np.sin(y + t)

def func2(x, y, t):
    return np.sin(x + t) * np.cos(y + t), np.cos(x + t) * np.sin(y + t)

functions = {
    "Sin + Cos": func1,
    "Sin * Cos": func2
}

# --- Sidebar Controls ---
st.sidebar.header("🎛 Controls")
selected_func = st.sidebar.radio("Function", list(functions.keys()))
t = st.sidebar.slider("Time (t)", 0.0, 10.0, 5.0, step=0.05)
real_min = st.sidebar.slider("Real Min", -20.0, 0.0, -10.0)
real_max = st.sidebar.slider("Real Max", 0.0, 20.0, 10.0)
imag_min = st.sidebar.slider("Imag Min", -20.0, 0.0, -10.0)
imag_max = st.sidebar.slider("Imag Max", 0.0, 20.0, 10.0)

# --- Mesh Grid ---
x = np.linspace(real_min, real_max, 100)
y = np.linspace(imag_min, imag_max, 100)
X, Y = np.meshgrid(x, y)

# --- Calculate Function ---
Z_real, Z_imag = functions[selected_func](X, Y, t)

# --- Plotly 3D Plot ---
fig = go.Figure()

# Surface = Real part
fig.add_trace(go.Surface(
    x=X,
    y=Y,
    z=Z_real,
    colorscale='Viridis',
    showscale=False,
    name='Real Surface'
))

# Colored points = Imaginary part
fig.add_trace(go.Scatter3d(
    x=X.flatten(),
    y=Y.flatten(),
    z=Z_real.flatten(),
    mode='markers',
    marker=dict(
        size=2,
        color=Z_imag.flatten(),
        colorscale='RdBu',
        opacity=0.5,
        colorbar=dict(title="Imaginary")
    ),
    name='Imaginary Points'
))

# --- Layout ---
fig.update_layout(
    title=f"{selected_func} | t = {t:.2f}",
    scene=dict(
        xaxis_title="Real Axis",
        yaxis_title="Imaginary Axis",
        zaxis_title="Z (Output)"
    ),
    height=700,
    margin=dict(l=0, r=0, b=0, t=40)
)

# --- Display ---
st.plotly_chart(fig, use_container_width=True)
