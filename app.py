# app.py
# Simulation of Heat Generation and Conduction Through a Composite Wall
# Run using:
# streamlit run app.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Composite Wall Heat Conduction", layout="wide")

st.title("🔥 Heat Generation and Conduction Through Composite Walls")

st.markdown("""
This simulation analyzes steady-state heat conduction through a three-layer composite wall
with internal heat generation.
""")

# ---------------------------------------------------
# SIDEBAR INPUTS
# ---------------------------------------------------

st.sidebar.header("Input Parameters")

# Layer thickness
L1 = st.sidebar.slider("Thickness of Layer A (m)", 0.01, 0.20, 0.05)
L2 = st.sidebar.slider("Thickness of Layer B (m)", 0.01, 0.20, 0.05)
L3 = st.sidebar.slider("Thickness of Layer C (m)", 0.01, 0.20, 0.05)

# Thermal conductivity
k1 = st.sidebar.slider("Thermal Conductivity k₁ (W/mK)", 1.0, 100.0, 15.0)
k2 = st.sidebar.slider("Thermal Conductivity k₂ (W/mK)", 1.0, 100.0, 8.0)
k3 = st.sidebar.slider("Thermal Conductivity k₃ (W/mK)", 1.0, 100.0, 20.0)

# Heat generation
q_gen = st.sidebar.slider("Heat Generation q''' (W/m³)", 0, 1000000, 300000)

# Boundary conditions
T_left = st.sidebar.slider("Left Surface Temperature (°C)", 0, 200, 100)

# Convection
h = st.sidebar.slider("Convective Heat Transfer Coefficient h (W/m²K)", 1, 100, 20)
T_inf = st.sidebar.slider("Ambient Temperature T∞ (°C)", 0, 100, 25)

# ---------------------------------------------------
# WALL DOMAIN
# ---------------------------------------------------

L_total = L1 + L2 + L3

x1 = np.linspace(0, L1, 100)
x2 = np.linspace(L1, L1 + L2, 100)
x3 = np.linspace(L1 + L2, L_total, 100)

# ---------------------------------------------------
# TEMPERATURE DISTRIBUTION
# ---------------------------------------------------

# Layer A (linear)
T1 = T_left - (10 / k1) * x1 * 50

# Layer B (with heat generation → parabolic)
x2_local = x2 - L1
T2_start = T1[-1]

T2 = (
    -(q_gen / (2 * k2)) * (x2_local ** 2)
    + 20 * x2_local
    + T2_start
)

# Layer C (linear cooling)
T3_start = T2[-1]

x3_local = x3 - (L1 + L2)

T3 = T3_start - (15 / k3) * x3_local * 50

# Convective effect
T_surface = T3[-1]
q_conv = h * (T_surface - T_inf)

# ---------------------------------------------------
# PLOT
# ---------------------------------------------------

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(x1, T1, linewidth=3, label="Layer A")
ax.plot(x2, T2, linewidth=3, label="Layer B (Heat Generation)")
ax.plot(x3, T3, linewidth=3, label="Layer C")

# Interface lines
ax.axvline(L1, linestyle="--")
ax.axvline(L1 + L2, linestyle="--")

ax.set_xlabel("Wall Thickness (m)")
ax.set_ylabel("Temperature (°C)")
ax.set_title("Temperature Distribution Across Composite Wall")

ax.legend()
ax.grid(True)

st.pyplot(fig)

# ---------------------------------------------------
# RESULTS
# ---------------------------------------------------

st.subheader("📊 Results")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Maximum Temperature", f"{max(T2):.2f} °C")

with col2:
    st.metric("Surface Temperature", f"{T_surface:.2f} °C")

with col3:
    st.metric("Convective Heat Flux", f"{q_conv:.2f} W/m²")

# ---------------------------------------------------
# THEORY SECTION
# ---------------------------------------------------

st.subheader("📘 Governing Equation")

st.latex(r"\frac{d^2 T}{dx^2} + \frac{q'''}{k} = 0")

st.markdown("""
### Assumptions
- One-dimensional steady-state conduction
- Constant thermal conductivity
- Uniform heat generation in Layer B
- Perfect thermal contact
- No radiation losses
""")

# ---------------------------------------------------
# WALL VISUALIZATION
# ---------------------------------------------------

st.subheader("🧱 Composite Wall Representation")

fig2, ax2 = plt.subplots(figsize=(10, 2))

ax2.barh(0, L1, left=0, height=1, label="Layer A")
ax2.barh(0, L2, left=L1, height=1, label="Layer B")
ax2.barh(0, L3, left=L1 + L2, height=1, label="Layer C")

ax2.set_xlim(0, L_total)
ax2.set_yticks([])
ax2.set_xlabel("Wall Thickness (m)")
ax2.set_title("Composite Wall Layers")

ax2.legend()

st.pyplot(fig2)

# ---------------------------------------------------
# OBSERVATIONS
# ---------------------------------------------------

st.subheader("🔍 Observations")

st.markdown(f"""
- Internal heat generation causes a **parabolic temperature profile** in Layer B.
- Lower thermal conductivity increases the **temperature gradient**.
- Increasing heat generation raises the **maximum temperature**.
- Convective cooling removes heat from the outer surface.
""")
