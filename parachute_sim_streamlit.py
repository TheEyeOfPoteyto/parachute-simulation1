import streamlit as st
import numpy as np
from PIL import Image, ImageDraw
import io
import base64
import matplotlib.pyplot as plt

# Simulation parameters
def calculate_terminal_velocity(mass, g, D, d, A):
    k = D * d / 2
    v_terminal = np.sqrt(mass * g / (k * A))
    return v_terminal, k

def simulate_fall(v_terminal, k, duration, dt):
    t = np.arange(0, duration, dt)
    v = v_terminal * (1 - np.exp(-k * t))
    position = np.cumsum(v * dt)
    return t, position, v

def create_parachute_frame(bg_img, parachute_img, y, velocity, max_y, fig_width, fig_height):
    frame = bg_img.copy()
    draw = ImageDraw.Draw(frame)

    # Map position
    y_ratio = y / max_y
    y_pos = int(y_ratio * (fig_height - parachute_img.height))
    x_pos = int(fig_width / 2 - parachute_img.width / 2)

    frame.paste(parachute_img, (x_pos, y_pos), parachute_img)

    # Display velocity in top-right corner
    velocity_text = f"v = {velocity:.2f} m/s"
    draw.text((180, 10), velocity_text, fill="black")

    return frame

def generate_gif(frames):
    buf = io.BytesIO()
    frames[0].save(
        buf, format='GIF', save_all=True,
        append_images=frames[1:], duration=100)
    gif_data = base64.b64encode(buf.getvalue()).decode("utf-8")
    return gif_data


# UI Elements
st.title("Parachute Terminal Velocity Simulation")

# Sidebar controls
mass = st.sidebar.slider("Mass (kg)", 1.0, 100.0, 70.0, 1.0)
g = st.sidebar.slider("Gravitational Acceleration (m/s²)", 5.0, 20.0, 9.81, 0.1)
D = st.sidebar.slider("Drag Coefficient (D)", 0.1, 2.0, 1.0, 0.1)
d = st.sidebar.slider("Air Density (kg/m³)", 0.5, 2.0, 1.2, 0.1)
A = st.sidebar.slider("Cross-sectional Area (m²)", 0.1, 5.0, 1.0, 0.1)

# Terminal velocity
v_terminal, k = calculate_terminal_velocity(mass, g, D, d, A)
st.write(f"**Terminal Velocity:** {v_terminal:.2f} m/s")

# Load images
background_img = Image.open("sky_background.jpg").resize((300, 1200)).convert("RGBA")
parachuter_img = Image.open("parachuter.png").resize((50, 50)).convert("RGBA")

# Animation trigger
if "run_sim" not in st.session_state:
    st.session_state.run_sim = False

if st.button("Start / Restart Animation"):
    st.session_state.run_sim = True

if st.session_state.run_sim:
    duration = 10.0  # longer duration
    dt = 0.05

    t, position, velocity = simulate_fall(v_terminal, k, duration, dt)
    max_y = max(position) + 5

    # Create frames
    frames = []
    for y, v in zip(position[::2], velocity[::2]):
        frame = create_parachute_frame(background_img, parachuter_img, y, v, max_y, 300, 1200)
        frames.append(frame)

    gif_data = generate_gif(frames, v_terminal)
    gif_placeholder = st.empty()
    gif_placeholder.markdown(f'<img src="data:image/gif;base64,{gif_data}" width="300">', unsafe_allow_html=True)

    # Plotting velocity graph
    st.subheader("Instantaneous Velocity Over Time")
    fig, ax = plt.subplots()
    ax.plot(t, velocity)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Velocity (m/s)")
    ax.set_title("Velocity vs Time")
    ax.grid(True)
    st.pyplot(fig)
