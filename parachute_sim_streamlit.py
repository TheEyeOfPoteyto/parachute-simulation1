import streamlit as st
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import matplotlib.pyplot as plt

# Terminal velocity calculation
def calculate_terminal_velocity(mass, g, D, d, A):
    v_terminal = np.sqrt((2 * mass * g) / (D * d * A))
    return v_terminal

# Motion simulation
def simulate_fall(v_terminal, g, duration, dt):
    t = np.arange(0, duration, dt)
    v = v_terminal * (1 - np.exp(-g * t / v_terminal))  # Correct exponential decay
    y = np.cumsum(v * dt)  # Numerical integration for position
    return t, y, v

# Create frame with parachuter and velocity text
def create_frame(bg_img, parachuter_img, y, v, max_y, width, height, y_99):
    frame = bg_img.copy()
    draw = ImageDraw.Draw(frame)

    # Draw 99% terminal velocity line
    y_99_pos = int((y_99 / max_y) * (height - parachuter_img.height))
    draw.line([(0, y_99_pos), (width, y_99_pos)], fill="green", width=2)
    draw.text((10, y_99_pos - 15), "99% Terminal Velocity", fill="green")

    # Position the parachuter
    y_ratio = y / max_y
    y_pos = int(y_ratio * (height - parachuter_img.height))
    x_pos = int(width / 2 - parachuter_img.width / 2)

    frame.paste(parachuter_img, (x_pos, y_pos), parachuter_img)

    # Add velocity text to top right
    velocity_text = f"v = {v:.2f} m/s"
    draw.text((width - 120, 10), velocity_text, fill="black")

    return frame

# Generate GIF from frames
def generate_gif(frames, duration_ms):
    buf = io.BytesIO()
    frames[0].save(
        buf,
        format='GIF',
        save_all=True,
        append_images=frames[1:],
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
t_99 = -(v_terminal / g) * np.log(0.01)
y_99 = v_terminal * (t_99 - (1 - np.exp(-g * t_99 / v_terminal)) / (g / v_terminal))
st.write(f"**Terminal Velocity:** {v_terminal:.2f} m/s")
st.write(f"**Time to Reach 99% of Terminal Velocity:** {t_99:.2f} s")

# Load images
bg_img = Image.open("sky_background.jpg").resize((300, 1000)).convert("RGBA")
parachuter_img = Image.open("parachuter.png").resize((50, 50)).convert("RGBA")

# Start button logic
if st.button("Start / Restart Animation"):
    duration = 8.0
    dt = 0.05

    t_vals, y_vals, v_vals = simulate_fall(v_terminal, g, duration, dt)
    max_y = max(y_vals) + 5
    width, height = bg_img.size

    frames = []
    for y, v in zip(y_vals[::2], v_vals[::2]):
        frame = create_frame(bg_img, parachuter_img, y, v, max_y, width, height, y_99)
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
