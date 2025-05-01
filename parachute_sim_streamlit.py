import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import base64
import os

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

# Load images
parachuter_path = os.path.join("assets", "parachuter.png")
background_path = os.path.join("assets", "sky_background.jpg")

if not os.path.exists(parachuter_path) or not os.path.exists(background_path):
    st.error("Parachuter or background image not found. Please ensure 'parachuter.png' and 'sky_background.jpg' are placed in the 'assets' directory.")
else:
    parachuter_img = Image.open(parachuter_path).convert("RGBA")
    background_img = Image.open(background_path).convert("RGBA")

    # Resize background to match figure size
    fig_width, fig_height = 300, 600  # pixels
    background_img = background_img.resize((fig_width, fig_height))

    # Generate each frame as an image
    frames = []
    max_y = max(position) + 5
    for y in position[::3]:  # Skip frames for speed
        # Create a new image with the background
        frame = background_img.copy()

        # Calculate parachuter position
        y_pos = int((y / max_y) * fig_height)
        x_pos = int(fig_width / 2 - parachuter_img.width / 2)
        y_pos = int(fig_height - y_pos - parachuter_img.height / 2)

        # Paste parachuter onto the background
        frame.paste(parachuter_img, (x_pos, y_pos), parachuter_img)

        frames.append(frame)

    # Save GIF to BytesIO
    gif_buf = BytesIO()
    frames[0].save(gif_buf, format="GIF", save_all=True, append_images=frames[1:], duration=50, loop=0)
    gif_data = base64.b64encode(gif_buf.getvalue()).decode("utf-8")

    # Display GIF in Streamlit
    st.markdown(f'<img src="data:image/gif;base64,{gif_data}" width="{fig_width}">', unsafe_allow_html=True)
