import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
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

# Matplotlib animation setup
fig, ax = plt.subplots(figsize=(3, 6))
ax.set_xlim(0, 1)
ax.set_ylim(0, max(position) + 5)
ball, = ax.plot([], [], 'o', color='blue', markersize=20)

def init():
    ball.set_data([], [])
    return ball,

def update(i):
    ball.set_data(0.5, position[i])
    return ball,

ani = animation.FuncAnimation(fig, update, frames=len(position),
                              init_func=init, blit=True, interval=50)

# Convert animation to GIF for Streamlit
def convert_to_gif(anim):
    buf = BytesIO()
    anim.save(buf, format='gif', writer='pillow')
    gif_data = base64.b64encode(buf.getvalue()).decode()
    return gif_data

if restart or True:  # Always generate gif on load
    gif = convert_to_gif(ani)
    st.markdown(f'<img src="data:image/gif;base64,{gif}" width="300">', unsafe_allow_html=True)


