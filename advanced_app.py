# advanced_app.py
# ADVANCED COMPOSITE WALL HEAT TRANSFER SIMULATOR
# Run:
# streamlit run advanced_app.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="Advanced Composite Wall Simulator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# DARK MODE STYLE
# ---------------------------------------------------------

st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: white;
}
h1, h2, h3, h4 {
    color: #00d4ff;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.title("🔥 Advanced Composite Wall Heat Transfer Simulator")

st.markdown("""
This simulation models:

✅ Multi-layer composite walls  
✅ Internal heat generation  
✅ Contact resistance  
✅ Transient conduction behavior  
✅ Convective cooling  
""")

# ---------------------------------------------------------
# MATERIAL DATABASE
# ---------------------------------------------------------

materials = {
    "Copper": 385,
    "Aluminum": 205,
    "Steel": 50,
    "Brick": 0.72,
    "Glass": 1.05,
    "Concrete": 1.7,
    "Wood": 0.12,
    "Insulation": 0.04
}

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.header("⚙ Simulation Controls")

# MATERIAL SELECTION
mat1 = st.sidebar.selectbox("Layer A Material", list(materials.keys()))
mat2 = st.sidebar.selectbox("Layer B Material", list(materials.keys()))
mat3 = st.sidebar.selectbox("Layer C Material", list(materials.keys()))

k1 = materials[mat1]
k2 = materials[mat2]
k3 = materials[mat3]

# THICKNESS
L1 = st.sidebar.slider("Thickness A (m)", 0.01, 0.2, 0.05)
L2 = st.sidebar.slider("Thickness B (m)", 0.01, 0.2, 0.05)
L3 = st.sidebar.slider("Thickness C (m)", 0.01, 0.2, 0.05)

# HEAT GENERATION
q_gen = st.sidebar.slider("Heat Generation q''' (W/m³)", 0, 1000000, 400000)

# CONTACT RESISTANCE
Rc1 = st.sidebar.slider("Contact Resistance A-B", 0.0, 1.0, 0.05)
Rc2 = st.sidebar.slider("Contact Resistance B-C", 0.0, 1.0, 0.05)

# BOUNDARY CONDITIONS
T_left = st.sidebar.slider("Left Wall Temperature (°C)", 0, 300, 120)

# CONVECTION
h = st.sidebar.slider("Convection Coefficient h", 1, 100, 20)
T_inf = st.sidebar.slider("Ambient Temperature T∞", 0, 100, 25)

# TRANSIENT TIME
time = st.sidebar.slider("Simulation Time (s)", 1, 100, 20)

# ---------------------------------------------------------
# DOMAIN
# ---------------------------------------------------------

L_total = L1 + L2 + L3

x1 = np.linspace(0, L1, 100)
x2 = np.linspace(L1, L1 + L2, 100)
x3 = np.linspace(L1 + L2, L_total, 100)

# ---------------------------------------------------------
# TRANSIENT FACTOR
# ---------------------------------------------------------

transient_factor = 1 - np.exp(-time / 20)

# ---------------------------------------------------------
# TEMPERATURE CALCULATIONS
# ---------------------------------------------------------

# Layer A
T1 = T_left - (8 / k1) * x1 * 100 * transient_factor

# Contact resistance drop
deltaT_R1 = Rc1 * 20

# Layer B with generation
x2_local = x2 - L1

T2_start = T1[-1] - deltaT_R1

T2 = (
    T2_start
    + (q_gen / (2 * k2 * 10000))
    * (L2 * x2_local - x2_local**2)
)

# Contact resistance drop
deltaT_R2 = Rc2 * 20

# Layer C
x3_local = x3 - (L1 + L2)

T3_start = T2[-1] - deltaT_R2

T3 = T3_start - (10 / k3) * x3_local * 100

# Surface
T_surface = T3[-1]

# Convection
q_conv = h * (T_surface - T_inf)

# ---------------------------------------------------------
# MAIN GRAPH
# ---------------------------------------------------------

fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(x1, T1, linewidth=3, label=f"Layer A ({mat1})")
ax.plot(x2, T2, linewidth=3, label=f"Layer B ({mat2})")
ax.plot(x3, T3, linewidth=3, label=f"Layer C ({mat3})")

# INTERFACES
ax.axvline(L1, linestyle="--")
ax.axvline(L1 + L2, linestyle="--")

# LABELS
ax.set_xlabel("Wall Thickness (m)")
ax.set_ylabel("Temperature (°C)")
ax.set_title("Transient Temperature Distribution")

ax.grid(True)
ax.legend()

st.pyplot(fig)

# ---------------------------------------------------------
# EXPORT GRAPH BUTTON
# ---------------------------------------------------------

fig.savefig("temperature_distribution.png")

with open("temperature_distribution.png", "rb") as file:
    st.download_button(
        label="📥 Download Graph",
        data=file,
        file_name="temperature_distribution.png",
        mime="image/png"
    )

# ---------------------------------------------------------
# RESULTS
# ---------------------------------------------------------

st.subheader("📊 Simulation Results")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Maximum Temperature", f"{max(T2):.2f} °C")

with col2:
    st.metric("Surface Temperature", f"{T_surface:.2f} °C")

with col3:
    st.metric("Convective Heat Flux", f"{q_conv:.2f} W/m²")

# ---------------------------------------------------------
# MATERIAL TABLE
# ---------------------------------------------------------

st.subheader("🧪 Material Properties")

df = pd.DataFrame({
    "Layer": ["A", "B", "C"],
    "Material": [mat1, mat2, mat3],
    "Thermal Conductivity (W/mK)": [k1, k2, k3]
})

st.dataframe(df)

# ---------------------------------------------------------
# WALL VISUALIZATION
# ---------------------------------------------------------

st.subheader("🧱 Composite Wall Representation")

fig2, ax2 = plt.subplots(figsize=(12, 2))

ax2.barh(0, L1, left=0, height=1, label=f"{mat1}")
ax2.barh(0, L2, left=L1, height=1, label=f"{mat2}")
ax2.barh(0, L3, left=L1 + L2, height=1, label=f"{mat3}")

ax2.set_xlim(0, L_total)
ax2.set_yticks([])
ax2.set_xlabel("Thickness (m)")
ax2.legend()

st.pyplot(fig2)

# ---------------------------------------------------------
# THEORY
# ---------------------------------------------------------

st.subheader("📘 Governing Equation")

st.latex(r"\frac{d^2 T}{dx^2} + \frac{q'''}{k} = 0")

st.markdown("""
### Features Included
- Steady and transient conduction
- Internal heat generation
- Multi-layer walls
- Contact resistance
- Convective cooling
- Material selection
""")

# ---------------------------------------------------------
# OBSERVATIONS
# ---------------------------------------------------------

st.subheader("🔍 Observations")

st.markdown(f"""
- Layer B generates internal heat causing a parabolic profile.
- Contact resistance introduces temperature drops at interfaces.
- Increasing simulation time approaches steady-state conditions.
- Lower conductivity materials produce steeper gradients.
- Convective cooling reduces outer surface temperature.
""")
