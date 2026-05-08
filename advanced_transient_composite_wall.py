# ==========================================================
# FINAL STABLE VERSION
# TRANSIENT HEAT CONDUCTION THROUGH COMPOSITE WALL
# USING FINITE DIFFERENCE METHOD (FDM)
#
# FEATURES:
# ----------------------------------------------------------
# ✅ Multi-layer composite wall
# ✅ Different materials
# ✅ Transient conduction
# ✅ Convective cooling
# ✅ Stable explicit FDM
# ✅ Animation with time
# ✅ Streamlit GUI
# ✅ Dark mode UI
# ✅ Export graph
#
# RUN:
# streamlit run advanced_transient_composite_wall.py
# ==========================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Transient Composite Wall Simulator",
    layout="wide"
)

# ==========================================================
# DARK MODE
# ==========================================================

st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: white;
}

h1, h2, h3 {
    color: #00d4ff;
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# TITLE
# ==========================================================

st.title("🔥 Transient Heat Conduction Through Composite Walls")

st.markdown("""
Interactive simulation of transient heat conduction through a
three-layer composite wall using the Finite Difference Method (FDM).
""")

# ==========================================================
# MATERIAL DATABASE
# ==========================================================

materials = {

    "Copper": {
        "k": 385,
        "rho": 8960,
        "cp": 385
    },

    "Aluminum": {
        "k": 205,
        "rho": 2700,
        "cp": 900
    },

    "Steel": {
        "k": 50,
        "rho": 7850,
        "cp": 470
    },

    "Brick": {
        "k": 0.72,
        "rho": 1800,
        "cp": 840
    },

    "Glass": {
        "k": 1.05,
        "rho": 2500,
        "cp": 840
    },

    "Wood": {
        "k": 0.12,
        "rho": 600,
        "cp": 2400
    },

    "Insulation": {
        "k": 0.04,
        "rho": 30,
        "cp": 1400
    }
}

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.header("⚙ Simulation Controls")

# MATERIALS
mat1 = st.sidebar.selectbox("Layer A Material", list(materials.keys()))
mat2 = st.sidebar.selectbox("Layer B Material", list(materials.keys()))
mat3 = st.sidebar.selectbox("Layer C Material", list(materials.keys()))

# PROPERTIES
k1 = materials[mat1]["k"]
rho1 = materials[mat1]["rho"]
cp1 = materials[mat1]["cp"]

k2 = materials[mat2]["k"]
rho2 = materials[mat2]["rho"]
cp2 = materials[mat2]["cp"]

k3 = materials[mat3]["k"]
rho3 = materials[mat3]["rho"]
cp3 = materials[mat3]["cp"]

# THICKNESS
L1 = st.sidebar.slider("Thickness A (m)", 0.01, 0.20, 0.05)
L2 = st.sidebar.slider("Thickness B (m)", 0.01, 0.20, 0.05)
L3 = st.sidebar.slider("Thickness C (m)", 0.01, 0.20, 0.05)

# INITIAL CONDITION
T_initial = st.sidebar.slider("Initial Temperature (°C)", 0, 100, 25)

# LEFT WALL TEMP
T_left = st.sidebar.slider("Left Boundary Temperature (°C)", 50, 300, 120)

# CONVECTION
h = st.sidebar.slider("Convection Coefficient h", 1, 100, 20)

T_inf = st.sidebar.slider("Ambient Temperature (°C)", 0, 100, 25)

# SIMULATION TIME
total_time = st.sidebar.slider("Simulation Time (s)", 1, 500, 100)

# ==========================================================
# DOMAIN
# ==========================================================

nx = 80

L_total = L1 + L2 + L3

dx = L_total / nx

x = np.linspace(0, L_total, nx)

# ==========================================================
# MATERIAL PROPERTY DISTRIBUTION
# ==========================================================

k = np.zeros(nx)
rho = np.zeros(nx)
cp = np.zeros(nx)

for i in range(nx):

    if x[i] <= L1:

        k[i] = k1
        rho[i] = rho1
        cp[i] = cp1

    elif x[i] <= (L1 + L2):

        k[i] = k2
        rho[i] = rho2
        cp[i] = cp2

    else:

        k[i] = k3
        rho[i] = rho3
        cp[i] = cp3

# ==========================================================
# THERMAL DIFFUSIVITY
# ==========================================================

alpha = k / (rho * cp)

# ==========================================================
# STABILITY CONDITION
# ==========================================================

alpha_max = np.max(alpha)

dt = 0.4 * dx**2 / alpha_max

nt = int(total_time / dt)

# ==========================================================
# INITIAL TEMPERATURE
# ==========================================================

T = np.ones(nx) * T_initial

# ==========================================================
# GOVERNING EQUATION
# ==========================================================

st.subheader("📘 Governing Equation")

st.latex(r"\frac{\partial T}{\partial t} = \alpha \frac{\partial^2 T}{\partial x^2}")

# ==========================================================
# MATERIAL TABLE
# ==========================================================

st.subheader("🧪 Material Properties")

df = pd.DataFrame({

    "Layer": ["A", "B", "C"],

    "Material": [mat1, mat2, mat3],

    "Thermal Conductivity (W/mK)": [k1, k2, k3],

    "Density (kg/m³)": [rho1, rho2, rho3],

    "Specific Heat (J/kgK)": [cp1, cp2, cp3]
})

st.dataframe(df)

# ==========================================================
# WALL VISUALIZATION
# ==========================================================

st.subheader("🧱 Composite Wall Structure")

fig_wall, ax_wall = plt.subplots(figsize=(10, 2))

ax_wall.barh(0, L1, left=0, height=1, label=mat1)

ax_wall.barh(0, L2, left=L1, height=1, label=mat2)

ax_wall.barh(0, L3, left=L1 + L2, height=1, label=mat3)

ax_wall.set_xlim(0, L_total)

ax_wall.set_yticks([])

ax_wall.set_xlabel("Wall Thickness (m)")

ax_wall.legend()

st.pyplot(fig_wall)

# ==========================================================
# RUN BUTTON
# ==========================================================

run_simulation = st.button("▶ Run Simulation")

# ==========================================================
# PLACEHOLDERS
# ==========================================================

plot_placeholder = st.empty()

progress_bar = st.progress(0)

# ==========================================================
# MAIN SIMULATION
# ==========================================================

if run_simulation:

    for n in range(nt):

        T_new = T.copy()

        # --------------------------------------------------
        # INTERNAL NODES
        # --------------------------------------------------

        for i in range(1, nx - 1):

            Fo = alpha[i] * dt / (dx ** 2)

            T_new[i] = (
                T[i]
                + Fo * (
                    T[i+1]
                    - 2*T[i]
                    + T[i-1]
                )
            )

        # --------------------------------------------------
        # LEFT BOUNDARY
        # --------------------------------------------------

        T_new[0] = T_left

        # --------------------------------------------------
        # RIGHT CONVECTIVE BOUNDARY
        # --------------------------------------------------

        T_new[-1] = (
            T[-2] + (h * dx / k[-1]) * T_inf
        ) / (
            1 + (h * dx / k[-1])
        )

        # --------------------------------------------------
        # UPDATE
        # --------------------------------------------------

        T = T_new.copy()

        # --------------------------------------------------
        # STABILITY CHECK
        # --------------------------------------------------

        if np.any(np.isnan(T)) or np.any(np.isinf(T)):

            st.error("Numerical instability detected.")

            st.stop()

        # --------------------------------------------------
        # PLOT
        # --------------------------------------------------

        fig, ax = plt.subplots(figsize=(12, 5))

        ax.plot(x, T, linewidth=3)

        # INTERFACE LINES
        ax.axvline(L1, linestyle="--")

        ax.axvline(L1 + L2, linestyle="--")

        ax.set_title(
            f"Transient Temperature Distribution (t = {n * dt:.2f} s)"
        )

        ax.set_xlabel("Wall Thickness (m)")

        ax.set_ylabel("Temperature (°C)")

        ax.grid(True)

        # DARK MODE PLOT
        fig.patch.set_facecolor("#0e1117")

        ax.set_facecolor("#0e1117")

        ax.tick_params(colors='white')

        ax.xaxis.label.set_color('white')

        ax.yaxis.label.set_color('white')

        ax.title.set_color('white')

        for spine in ax.spines.values():

            spine.set_color('white')

        # DISPLAY
        plot_placeholder.pyplot(fig)

        progress_bar.progress((n + 1) / nt)

        plt.close()

    # ======================================================
    # EXPORT GRAPH
    # ======================================================

    fig.savefig("final_temperature_distribution.png")

    with open("final_temperature_distribution.png", "rb") as file:

        st.download_button(
            label="📥 Download Final Graph",
            data=file,
            file_name="final_temperature_distribution.png",
            mime="image/png"
        )

# ==========================================================
# OBSERVATIONS
# ==========================================================

st.subheader("🔍 Observations")

st.markdown("""
- Heat propagates gradually through the composite wall with time.
- Different materials show different temperature gradients due to varying thermal diffusivity.
- The system gradually approaches steady-state conditions.
- Convective cooling reduces the temperature near the outer boundary.
- Higher conductivity materials transfer heat more rapidly.
""")
