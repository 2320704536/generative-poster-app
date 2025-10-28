import random
import math
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import io

# -------------------------------
# Streamlit page config
# -------------------------------
st.set_page_config(page_title="🎨 Generative Abstract Poster", layout="centered")
st.title("🎨 Generative Abstract Poster")
st.markdown("**Interactive • Arts & Advanced Big Data Project**")
st.caption("Use the controls on the left to design your own generative poster in real-time.")

# -------------------------------
# Palette generator
# -------------------------------
def random_palette(k=6):
    return [(random.random(), random.random(), random.random()) for _ in range(k)]

# -------------------------------
# Organic shape (blob)
# -------------------------------
def blob(center=(0.5, 0.5), r=0.3, points=200, wobble=0.15):
    angles = np.linspace(0, 2 * math.pi, points)
    radii = r * (1 + wobble * (np.random.rand(points) - 0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

# -------------------------------
# Draw poster
# -------------------------------
def draw_poster(n_layers=8, wobble=0.15, seed=None):
    if seed not in (None, 0, ""):
        try:
            seed = int(seed)
            random.seed(seed)
            np.random.seed(seed)
        except:
            pass

    fig, ax = plt.subplots(figsize=(7, 10))
    ax.axis("off")
    ax.set_facecolor((0.98, 0.98, 0.97))
    palette = random_palette(6)

    for _ in range(n_layers):
        cx, cy = random.random(), random.random()
        rr = random.uniform(0.15, 0.45)
        x, y = blob(center=(cx, cy), r=rr, wobble=wobble)
        color = random.choice(palette)
        alpha = random.uniform(0.25, 0.6)
        ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0, 0, 0, 0))

    ax.text(0.05, 0.95, "Generative Poster", fontsize=18, weight="bold", transform=ax.transAxes)
    ax.text(0.05, 0.91, "Interactive • Arts & Advanced Big Data", fontsize=11, transform=ax.transAxes)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return fig

# -------------------------------
# Sidebar controls
# -------------------------------
st.sidebar.header("⚙️ Controls")
layers = st.sidebar.slider("Number of Layers", 1, 20, 8, 1)
wobble = st.sidebar.slider("Wobble Intensity", 0.01, 0.5, 0.15, 0.01)
seed = st.sidebar.text_input("Random Seed (optional)", value="0")

# Draw figure
fig = draw_poster(layers, wobble, seed)
st.pyplot(fig, use_container_width=True)

# -------------------------------
# Download current figure as PNG
# -------------------------------
png_bytes = io.BytesIO()
fig.savefig(png_bytes, format="png", dpi=300, bbox_inches="tight")
st.download_button(
    "💾 Download PNG",
    data=png_bytes.getvalue(),
    file_name="poster.png",
    mime="image/png",
    help="Download the current poster as a high-res PNG",
)

st.markdown("""---
**Tips**
- Change the seed for reproducible results.
- Increase layers for richer overlaps; increase wobble for more organic edges.
""")

st.caption("Developed by Arts & Advanced Big Data • Streamlit Edition")
