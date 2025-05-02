import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image, ImageDraw
import io
import base64

# Streamlit app setup
st.title("Parachute Simulation with Terminal Velocity")
st.markdown("Adjust the parameters below to see how they affect the motion:")

# Sliders for user input
mass = st.slider("Mass (kg)", 1.0, 100.0, 70.0, 1.0)
area = st.slider("Cross-sectional Area (m²)", 0.1, 5.0, 1.0, 0.1)
resistance_coefficient = st.slider("Drag Coefficient (D)", 0.1, 2.0, 1.0, 0.1)
air_density = st.slider("Air Density (kg/m³)", 0.5, 1.5, 1.2, 0.1)
gravity = st.slider("Gravitational Acceleration (m/s²)", 5.0, 20.0, 9.81, 0.1)

# Constants and terminal velocity calculation
k = (resistance_coefficient * air_density) / 2
v_terminal = np.sqrt(mass * gravity / (k * area))
st.markdown(f"### Terminal Velocity: {v_terminal:.2f} m/s")

# Placeholder for instantaneous velocity display
velocity_placeholder = st.empty()

# Load images
background_img = Image.open("sky_background.jpg").resize((300, 800)).convert("RGBA")
parachute_img = Image.open("parachute.png").resize((60, 60)).convert("RGBA")

# Create animation frames
def generate_gif():
    fig, ax = plt.subplots(figsize=(3, 8), dpi=100)
    plt.close(fig)

    duration = 10  # seconds
    fps = 20
    total_frames = duration * fps

    y_positions = []
    velocities = []

    for i in range(total_frames):
        t = i / fps
        velocity = v_terminal * (1 - np.exp(-k * area * t / mass))
        y = velocity * t  # simplified, you could use numerical integration for more precision
        y_positions.append(min(y, 750))
        velocities.append(velocity)

    frames = []
    for i in range(total_frames):
        base = background_img.copy()
        parachute_y = int(y_positions[i])
        base.alpha_composite(parachute_img, (120, parachute_y))

        # Display instantaneous velocity in the app
        velocity_placeholder.markdown(f"**Instantaneous Velocity:** {velocities[i]:.2f} m/s")

        frames.append(base)

    buf = io.BytesIO()
    frames[0].save(buf, format='GIF', save_all=True, append_images=frames[1:], duration=50)
    buf.seek(0)
    return buf

# Restart button
if st.button("Restart Simulation"):
    gif_data = generate_gif()
    st.image(gif_data, format="gif")
