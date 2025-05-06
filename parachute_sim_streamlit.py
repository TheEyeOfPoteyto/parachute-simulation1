import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
import numpy as np
import io

# Title
st.title("Parachute Terminal Velocity Simulation")

# Sidebar sliders
mass = st.sidebar.slider("Mass (kg)", 40.0, 120.0, 80.0, 5.0)
air_resistance = st.sidebar.slider("Air Resistance Coefficient", 0.5, 2.5, 1.0, 0.1)
g = st.sidebar.slider("Gravitational Acceleration (m/s²)", 5.0, 15.0, 9.8, 0.1)

# Constants and initial values
y0 = 800  # initial height in pixels
x0 = 150  # x position (centered)
dt = 0.1  # time step

# Calculated parameters
k_over_m = air_resistance / mass
terminal_velocity = mass * g / air_resistance

# Load parachute image
parachute_img = Image.open("parachute.png").resize((50, 50))
parachute_arr = np.asarray(parachute_img)

# Load background image
background_img = Image.open("sky_background.jpg").resize((300, 800)).convert("RGBA")

# Create figure and axis
fig, ax = plt.subplots(figsize=(3, 8))
ax.set_xlim(0, 300)
ax.set_ylim(0, 800)
ax.imshow(background_img, extent=[0, 300, 0, 800])
ax.axis('off')

# Create the parachute object
imagebox = OffsetImage(parachute_arr, zoom=1)
parachute = AnnotationBbox(imagebox, (x0, y0), frameon=False)
ax.add_artist(parachute)

# Velocity text display
velocity_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=12, color='white',
                        bbox=dict(facecolor='black', alpha=0.5, edgecolor='none'))

def animate(frame):
    t = frame * dt
    v = terminal_velocity * (1 - np.exp(-k_over_m * t))
    y = y0 - (terminal_velocity / k_over_m) * (t + (1 / k_over_m) * np.exp(-k_over_m * t) - (1 / k_over_m))

    if y < 50:
        y = 50  # Stop at ground level

    parachute.xybox = (x0, y)
    velocity_text.set_text(f"Velocity: {v:.2f} m/s")
    return parachute, velocity_text

def convert_to_gif(ani):
    buf = io.BytesIO()
    ani.save(buf, format='gif', writer='pillow', fps=30, savefig_kwargs={'facecolor': 'white'})
    buf.seek(0)
    return buf

# Animation button
if st.button("Start / Restart Simulation"):
    ani = animation.FuncAnimation(fig, animate, frames=200, interval=50, blit=True, repeat=False)
    gif = convert_to_gif(ani)
    st.image(gif, caption="Parachute Falling Simulation")

# Display terminal velocity
st.markdown(f"### Calculated Terminal Velocity: {terminal_velocity:.2f} m/s")
