import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Constants
AIR_DENSITY = 1.2  # kg/m³
dt = 0.05  # time step

# Streamlit interface
st.title("Parachute Terminal Velocity Simulator")

mass = st.slider("Mass (kg)", 30.0, 120.0, 70.0, step=1.0)
area = st.slider("Cross-sectional Area (m²)", 0.5, 5.0, 1.2, step=0.1)
drag_coefficient = st.slider("Drag Coefficient", 0.5, 2.5, 1.5, step=0.1)
gravity = st.slider("Gravitational Acceleration (m/s²)", 1.0, 20.0, 9.81, step=0.1)

# Terminal velocity calculation
k = (drag_coefficient * AIR_DENSITY) / 2
terminal_velocity = np.sqrt((mass * gravity) / (k * area))
st.markdown(f"### Terminal Velocity: **{terminal_velocity:.2f} m/s**")

# Time and velocity arrays for animation
time = np.arange(0, 5, dt)
velocity = [0]
position = [0]

for t in time[1:]:
    v_prev = velocity[-1]
    drag = 0.5 * AIR_DENSITY * drag_coefficient * area * v_prev**2
    acceleration = gravity - (drag / mass)
    v_new = v_prev + acceleration * dt
    y_new = position[-1] + v_new * dt

    velocity.append(v_new)
    position.append(y_new)

# Animation
fig, ax = plt.subplots(figsize=(3, 6))
ax.set_xlim(0, 1)
ax.set_ylim(0, max(position) + 5)
ball, = ax.plot([], [], 'ro', markersize=20)

def init():
    ball.set_data([], [])
    return ball,

def update(i):
    ball.set_data(0.5, position[i])
    return ball,

ani = animation.FuncAnimation(fig, update, frames=len(position),
                              init_func=init, blit=True, interval=50, repeat=False)

st.pyplot(fig)
