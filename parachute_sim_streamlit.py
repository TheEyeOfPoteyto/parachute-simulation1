import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import base64

# Constants
AIR_DENSITY = 1.2  # kg/m³
dt = 0.05
duration = 5  # seconds

# Sidebar controls
st.title("🎈 Parachute Terminal Velocity Simulation")

with st.sidebar:
    st.header("Simulation Parameters")
    mass = st.slider("Mass (kg)", 30.0, 120.0, 70.0, step=1.0)
    area = st.slider("Cross-sectional Area (m²)", 0.5, 5.0, 1.2, step=0.1)
    drag_coefficient = st.slider("Drag Coefficient", 0.5, 2.5, 1.5, step=0.1)
    gravity = st.slider("Gravity (m/s²)", 1.0, 20.0, 9.81, step=0.1)
    restart = st.button("🔄 Restart Animation")

# Terminal velocity
k = (drag_coefficient * AIR_DENSITY) / 2
v_terminal = np.sqrt((mass * gravity) / (k * area))
st.markdown(f"### Terminal Velocity: **{v_terminal:.2f} m/s**")

# Physics simulation
time = np.arange(0, duration, dt)
velocity = [0]
position = [0]

for t in time[1:]:
    v_prev = velocity[-1]
    drag = 0.5 * AIR_DENSITY * drag_coefficient * area * v_prev**2
    a = gravity - (drag / mass)
    v_new = v_prev + a * dt
    y_new = position[-1] + v_new * dt
    velocity.append(v_new)
    position.append(y_new)

# Generate each frame as an image
frames = []
for y in position[::3]:  # Skip every few frames for speed
    fig, ax = plt.subplots(figsize=(3, 6))
    ax.set_xlim(0, 1)
    ax.set_ylim(max(position) + 5, 0)
    ax.axis("off")
    ax.plot(0.5, y, 'o', color='blue', markersize=20)
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    frame = Image.open(buf)
    frames.append(frame)

# Save GIF to BytesIO
gif_buf = BytesIO()
frames[0].save(gif_buf, format="GIF", save_all=True, append_images=frames[1:], duration=50, loop=0)
gif_data = base64.b64encode(gif_buf.getvalue()).decode("utf-8")

# Display GIF in Streamlit
st.markdown(f'<img src="data:image/gif;base64,{gif_data}" width="300">', unsafe_allow_html=True)
