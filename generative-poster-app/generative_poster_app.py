import random
import math
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import io

# -------------------------------
# 页面配置
# -------------------------------
st.set_page_config(page_title="🎨 Generative Abstract Poster", layout="wide")
st.title("🎨 Generative Abstract Poster - Interactive Preview")
st.markdown("**Create organic generative posters inspired by data & randomness.**")

# -------------------------------
# Utility: 随机调色板生成
# -------------------------------
def random_palette(k=5):
    """生成随机调色板"""
    return [(random.random(), random.random(), random.random()) for _ in range(k)]

# -------------------------------
# Shape generators
# -------------------------------
def blob(center=(0.5, 0.5), r=0.3, points=200, wobble=0.15):
    angles = np.linspace(0, 2 * math.pi, points)
    radii = r * (1 + wobble * (np.random.rand(points) - 0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

def polygon(center=(0.5, 0.5), sides=6, r=0.3, wobble=0.1):
    angles = np.linspace(0, 2 * math.pi, sides, endpoint=False)
    radii = r * (1 + wobble * (np.random.rand(sides) - 0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return np.append(x, x[0]), np.append(y, y[0])

def waves(center=(0.5, 0.5), r=0.3, points=400, frequency=6, wobble=0.05):
    angles = np.linspace(0, 2 * math.pi, points)
    radii = r * (1 + wobble * np.sin(frequency * angles))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

def rings(center=(0.5, 0.5), base_r=0.3, count=4, wobble=0.1):
    coords = []
    for i in range(count):
        r = base_r * (0.5 + i * 0.4)
        x, y = blob(center, r, 200, wobble)
        coords.append((x, y))
    return coords

# -------------------------------
# Draw Poster
# -------------------------------
def draw_poster(shape_type="Blob", n_layers=8, wobble=0.15, seed=None):
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
        color = random.choice(palette)
        alpha = random.uniform(0.25, 0.6)

        if shape_type == "Blob":
            x, y = blob((cx, cy), rr, wobble=wobble)
            ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0, 0, 0, 0))

        elif shape_type == "Polygon":
            x, y = polygon((cx, cy), sides=random.randint(3, 8), r=rr, wobble=wobble)
            ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0, 0, 0, 0))

        elif shape_type == "Waves":
            x, y = waves((cx, cy), rr, frequency=random.randint(4, 8), wobble=wobble)
            ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0, 0, 0, 0))

        elif shape_type == "Rings":
            rings_list = rings((cx, cy), rr, count=random.randint(2, 4), wobble=wobble)
            for x, y in rings_list:
                ax.plot(x, y, color=color, alpha=alpha, lw=2)

    ax.text(0.05, 0.95, "Generative Poster", fontsize=18, weight="bold", transform=ax.transAxes)
    ax.text(0.05, 0.91, "Interactive • Arts & Advanced Big Data", fontsize=11, transform=ax.transAxes)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return fig

# -------------------------------
# Sidebar 控件
# -------------------------------
with st.sidebar:
    st.header("⚙️ Controls")
    shape = st.selectbox("Shape Type", ["Blob", "Polygon", "Waves", "Rings"])
    layers = st.slider("Number of Layers", 1, 20, 8, 1)
    wobble = st.slider("Wobble Intensity", 0.01, 0.5, 0.15, 0.01)
    seed = st.text_input("Random Seed (optional)", value="0")

    regenerate = st.button("🎲 Generate New Poster")

# -------------------------------
# Layout 显示
# -------------------------------
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 🔍 Basic Functions")
    st.markdown("""
    - Adjust **Layers** for complexity  
    - Change **Wobble** for shape variation  
    - Switch **Shape Type** (Blob / Polygon / Waves / Rings)  
    - Use **Seed** for repeatable randomness  
    - Click **Generate** for a new composition  
    - Download your art as PNG  
    """)

with col2:
    if regenerate:
        fig = draw_poster(shape, layers, wobble, seed)
    else:
        fig = draw_poster(shape, layers, wobble, seed)
    st.pyplot(fig, use_container_width=True)

# -------------------------------
# 下载按钮
# -------------------------------
png_bytes = io.BytesIO()
fig.savefig(png_bytes, format="png", dpi=300, bbox_inches="tight")

st.download_button(
    "💾 Download Poster as PNG",
    data=png_bytes.getvalue(),
    file_name="poster.png",
    mime="image/png",
    help="Save your poster as a high-resolution PNG file"
)

st.markdown("---")
st.caption("Developed for **Arts & Advanced Big Data** • Enhanced Interactive Edition")

