import streamlit as st
import numpy as np
import plotly.graph_objs as go

st.set_page_config(layout="wide")
st.title("⚡ Real 4D-Like Animated Surface (Plotly in Streamlit)")

# Define functions
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

# Mesh grid
x = np.linspace(real_min, real_max, 50)
y = np.linspace(imag_min, imag_max, 50)
X, Y = np.meshgrid(x, y)
X_flat = X.flatten()
Y_flat = Y.flatten()

func = functions[selected_function]

# Create frames for animation
frames = []
frame_count = 40
t_values = np.linspace(0, 10, frame_count)

for t in t_values:
    Z_real, Z_imag = func(X, Y, t)
    frame = go.Frame(
        data=[
            go.Surface(z=Z_real, x=X, y=Y, colorscale='Viridis', showscale=False),
            go.Scatter3d(
                x=X_flat,
                y=Y_flat,
                z=Z_real.flatten(),
                mode='markers',
                marker=dict(size=2, color=Z_imag.flatten(), colorscale='RdBu', opacity=0.6)
            )
        ],
        name=str(t)
    )
    frames.append(frame)

# Initial Z values
Z_real, Z_imag = func(X, Y, t_values[0])

# Create figure
fig = go.Figure(
    data=[
        go.Surface(z=Z_real, x=X, y=Y, colorscale='Viridis', showscale=False),
        go.Scatter3d(
            x=X_flat,
            y=Y_flat,
            z=Z_real.flatten(),
            mode='markers',
            marker=dict(size=2, color=Z_imag.flatten(), colorscale='RdBu', opacity=0.6)
        )
    ],
    layout=go.Layout(
        title="Animated 3D Wave 🌊",
        scene=dict(
            xaxis_title="Real",
            yaxis_title="Imaginary",
            zaxis_title="Z"
        ),
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            buttons=[dict(label="Play", method="animate", args=[None, {"frame": {"duration": 50}, "fromcurrent": True}])]
        )]
    ),
    frames=frames
)

# Display
st.plotly_chart(fig, use_container_width=True)
