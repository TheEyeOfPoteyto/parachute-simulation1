l, g, duration, dt)
    max_y = max(position) + 5

    # Create frames
    frames = []
    for y, v in zip(position[::2], velocity[::2]):
        frame = create_parachute_frame(background_img, parachuter_img, y, v, max_y, 300, 800)
        frames.append(frame)

    gif_data = generate_gif(frames, v_terminal)

    gif_placeholder = st.empty()
    gif_placeholder.markdown(f'<img src="data:image/gif;base64,{gif_data}" width="300">', unsafe_allow_html=True)
import streamlit as st 
import numpy as np
from PIL import Image, ImageDraw
import io
import base64

# Simulation parameters
def calculate_terminal_velocity(mass, g, D, d, A):
    k = D * d / 2
    v_terminal = np.sqrt(mass * g / (k * A))
    return v_terminal, k

def simulate_fall(v_terminal, k, duration, dt):
    t = np.arange(0, duration, dt)
    position = v_terminal * (t - (1 - np.exp(-t)))  # Approximated position model
    velocity = v_terminal * (1 - np.exp(-t))        # Velocity capped by terminal velocity
    return t, position, velocity

def create_parachute_frame(bg_img, parachute_img, y, v, max_y, fig_width, fig_height):
    frame = bg_img.copy()
    draw = ImageDraw.Draw(frame)

    # Position parachute
    y_ratio = y / max_y
    y_pos = int(y_ratio * (fig_height - parachute_img.height))
    x_pos = int(fig_width / 2 - parachute_img.width /_
