import streamlit as st
import numpy as np
import plotly.graph_objs as go
import time

# Title
st.set_page_config(page_title="🌊 3D Wave Visualizer", layout="wide")
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
real_min = st.sidebar.slider("Real Min", -20.0, 0.0, -10.0)
real_max = st.sidebar.slider("Real Max", 0.0, 20.0, 10.0)
imag_min = st.sidebar.slider("Imaginary Min", -20.0, 0.0, -10.0)
imag_max = st.sidebar.slider("Imaginary Max", 0.0, 20.0, 10.0)
animate = st.sidebar.checkbox("🎞 Animate over time", value=False)
speed = st.sidebar.slider("Speed (frames/sec)", 1, 30, 10)

# Grid setup
x = np.linspace(real_min, real_max, 100)
y = np.linspace(imag_min, imag_max, 100)
X, Y = np.meshgrid(x, y)

# Placeholder for animation
plot_placeholder = st.empty()

# Animation loop
frames = np.linspace(0, 10, 100)
if animate:
    for t in frames:
        func = functions[selected_function]
        Z_real, Z_imag = func(X, Y, t)

        fig = go.Figure()
        fig.add_trace(go.Surface(x=X, y=Y, z=Z_real, colorscale='Viridis', showscale=False, name='Real'))
        fig.add_trace(go.Scatter3d(
            x=X.flatten(), y=Y.flatten(), z=Z_real.flatten(),
            mode='markers',
            marker=dict(size=2, color=Z_imag.flatten(), colorscale='RdBu', opacity=0.6),
            name="Imaginary"
        ))

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

        plot_placeholder.plotly_chart(fig, use_container_width=True)
        time.sleep(1 / speed)
else:
    t = st.sidebar.slider("Time (t)", 0.0, 10.0, 1.0, step=0.1)
    func = functions[selected_function]
    Z_real, Z_imag = func(X, Y, t)

    fig = go.Figure()
    fig.add_trace(go.Surface(x=X, y=Y, z=Z_real, colorscale='Viridis', showscale=False, name='Real'))
    fig.add_trace(go.Scatter3d(
        x=X.flatten(), y=Y.flatten(), z=Z_real.flatten(),
        mode='markers',
        marker=dict(size=2, color=Z_imag.flatten(), colorscale='RdBu', opacity=0.6),
        name="Imaginary"
    ))

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

    plot_placeholder.plotly_chart(fig, use_container_width=True)
