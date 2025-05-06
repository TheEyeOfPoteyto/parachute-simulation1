import streamlit as st
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import matplotlib.pyplot as plt

# Terminal velocity calculation
def calculate_terminal_velocity(mass, g, D, d, A):
    k = D * d / 2
    v_terminal = np.sqrt(mass * g / (k * A))
    return v_terminal

# Motion simulation
def simulate_fall(v_terminal, g, duration, dt):
    t = np.arange(0, duration, dt)
    v = g * t
    v = np.clip(v, 0, v_terminal)  # Cap at terminal velocity
    y = v_terminal * (t - (1 - np.exp(-t)))  # Smoothed position
    return t, y, v

# Create frame with parachuter and velocity text
def create_frame(bg_img, parachuter_img, y, v, max_y, width, height):
    frame = bg_img.copy()
    draw = ImageDraw.Draw(frame)
    font = ImageFont.load_default()

    y_ratio = y / max_y
    y_pos = int(y_ratio * (height - parachuter_img.height))
    x_pos = int(width / 2 - parachuter_img.width / 2)

    frame.paste(parachuter_img, (x_pos, y_pos), parachuter_img)

    # Add velocity text to top right
    velocity_text = f"v = {v:.2f} m/s"
    draw.text((width - 120, 10), velocity_text, fill="black", font=font)

    return frame

# Generate GIF from frames
def generate_gif(frames, duration_ms):
    converted_frames = [frame.convert("P", dither=Image.NONE) for frame in frames]
    buf = io.BytesIO()
    converted_frames[0].save(
        buf,
        format='GIF',
        save_all=True,
        append_images=converted_frames[1:],
        duration=duration_ms,
        disposal=2  # prevent trailing effects
    )
    gif_data = base64.b64encode(buf.getvalue()).decode("utf-8")
    return gif_data

# Streamlit UI
st.title("Parachute Terminal Velocity Simulation")

# Sidebar sliders
mass = st.sidebar.slider("Mass (kg)", 1.0, 100.0, 70.0, 1.0)
g = st.sidebar.slider("Gravitational Acceleration (m/s²)", 5.0, 20.0, 9.81, 0.1)
D = st.sidebar.slider("Drag Coefficient", 0.1, 2.0, 1.0, 0.1)
d = st.sidebar.slider("Air Density (kg/m³)", 0.5, 2.0, 1.2, 0.1)
A = st.sidebar.slider("Cross-sectional Area (m²)", 0.1, 5.0, 1.0, 0.1)

# Calculate terminal velocity
v_terminal = calculate_terminal_velocity(mass, g, D, d, A)
st.write(f"**Terminal Velocity:** {v_terminal:.2f} m/s")

# Load images
bg_img = Image.open("sky_background.jpg").resize((300, 1000)).convert("RGBA")
parachuter_img = Image.open("parachuter.png").resize((50, 50)).convert("RGBA")

# Check input changes to prevent auto-run
inputs = (mass, g, D, d, A)
if "prev_inputs" not in st.session_state:
    st.session_state.prev_inputs = inputs

if st.session_state.prev_inputs != inputs:
    st.session_state.run_sim = False
    st.session_state.prev_inputs = inputs

# Start button logic
if "run_sim" not in st.session_state:
    st.session_state.run_sim = False

if st.button("Start / Restart Animation"):
    st.session_state.run_sim = True

# Run simulation and generate output
if st.session_state.run_sim:
    duration = 8.0  # seconds
    dt = 0.05

    t_vals, y_vals, v_vals = simulate_fall(v_terminal, g, duration, dt)
    max_y = max(y_vals) + 5
    width, height = bg_img.size

    # Create animation frames
    frames = []
    for y, v in zip(y_vals[::2], v_vals[::2]):
        frame = create_frame(bg_img, parachuter_img, y, v, max_y, width, height)
        frames.append(frame)

    gif_data = generate_gif(frames, duration_ms=50)
    st.markdown(f'<img src="data:image/gif;base64,{gif_data}" width="{width}">', unsafe_allow_html=True)

    # Plotting velocity vs. time
    fig, ax = plt.subplots()
    ax.plot(t_vals, v_vals, label="Instantaneous Velocity", color='blue')
    ax.axhline(y=v_terminal, color='red', linestyle='--', label="Terminal Velocity")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Velocity (m/s)")
    ax.set_title("Velocity vs. Time")
    ax.legend()
    st.pyplot(fig)
    plt.plot()
