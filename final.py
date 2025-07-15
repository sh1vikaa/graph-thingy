import streamlit as st
import numpy as np
import plotly.graph_objs as go
import time

# Config
st.set_page_config(layout="wide")

# Functions
def func1(x, y, t):
    return np.sin(x + t) + np.cos(y + t), np.cos(x + t) - np.sin(y + t)

def func2(x, y, t):
    return np.sin(x + t) * np.cos(y + t), np.cos(x + t) * np.sin(y + t)

functions = {
    "Sin + Cos": func1,
    "Sin * Cos": func2
}

# Sidebar Controls
st.sidebar.title("🎛 Controls")
selected_function = st.sidebar.radio("Function", list(functions.keys()))
real_min = st.sidebar.slider("Real Min", -20.0, 0.0, -10.0)
real_max = st.sidebar.slider("Real Max", 0.0, 20.0, 10.0)
imag_min = st.sidebar.slider("Imag Min", -20.0, 0.0, -10.0)
imag_max = st.sidebar.slider("Imag Max", 0.0, 20.0, 10.0)
animate = st.sidebar.checkbox("🎞 Animate over time", value=False)
fps = st.sidebar.slider("Speed (FPS)", 1, 30, 10)

# Mesh Grid
x = np.linspace(real_min, real_max, 100)
y = np.linspace(imag_min, imag_max, 100)
X, Y = np.meshgrid(x, y)
func = functions[selected_function]

# Plot placeholder
plot_area = st.empty()

if animate:
    frames = np.linspace(0, 10, 100)
    for t in frames:
        Z_real, Z_imag = func(X, Y, t)

        fig = go.Figure()

        fig.add_trace(go.Surface(x=X, y=Y, z=Z_real, colorscale='Viridis', showscale=False))
        fig.add_trace(go.Scatter3d(
            x=X.flatten(), y=Y.flatten(), z=Z_real.flatten(),
            mode='markers',
            marker=dict(size=2, color=Z_imag.flatten(), colorscale='RdBu', opacity=0.6)
        ))

        fig.update_layout(
            title=f"{selected_function} | t = {t:.2f}",
            scene=dict(
                xaxis_title="Real",
                yaxis_title="Imaginary",
                zaxis_title="Z"
            ),
            height=750,
            margin=dict(l=0, r=0, b=0, t=50)
        )

        plot_area.plotly_chart(fig, use_container_width=True)
        time.sleep(1 / fps)

else:
    t = st.sidebar.slider("Time", 0.0, 10.0, 1.0, 0.1)
    Z_real, Z_imag = func(X, Y, t)

    fig = go.Figure()

    fig.add_trace(go.Surface(x=X, y=Y, z=Z_real, colorscale='Viridis', showscale=False))
    fig.add_trace(go.Scatter3d(
        x=X.flatten(), y=Y.flatten(), z=Z_real.flatten(),
        mode='markers',
        marker=dict(size=2, color=Z_imag.flatten(), colorscale='RdBu', opacity=0.6)
    ))

    fig.update_layout(
        title=f"{selected_function} | t = {t:.2f}",
        scene=dict(
            xaxis_title="Real",
            yaxis_title="Imaginary",
            zaxis_title="Z"
        ),
        height=750,
        margin=dict(l=0, r=0, b=0, t=50)
    )

    plot_area.plotly_chart(fig, use_container_width=True)
