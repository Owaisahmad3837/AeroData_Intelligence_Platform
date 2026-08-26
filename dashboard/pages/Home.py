import streamlit as st
from pathlib import Path
import sys


# ============================================================
# PROJECT ROOT
# ============================================================

ROOT_DIR = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT_DIR))


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SkyHub Airport Data Platform",
    page_icon="✈️",
    layout="wide"
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main page */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    /* Hero */
    .hero-box {
        padding: 35px;
        border-radius: 20px;
        background: linear-gradient(
            135deg,
            #0f172a,
            #1e3a5f
        );
        margin-bottom: 30px;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        color: white;
    }

    .hero-subtitle {
        font-size: 22px;
        color: #dbeafe;
        margin-top: 8px;
    }

    .hero-description {
        font-size: 16px;
        color: #cbd5e1;
        line-height: 1.7;
        margin-top: 15px;
        max-width: 850px;
    }

    .hero-tag {
        margin-top: 18px;
        font-size: 15px;
        color: #bfdbfe;
        font-weight: 600;
    }

    /* Card */
    .card {
        border: 1px solid rgba(128,128,128,0.25);
        border-radius: 16px;
        padding: 22px;
        min-height: 135px;
        margin-bottom: 15px;
        background-color: rgba(128,128,128,0.04);
    }

    .card-icon {
        font-size: 30px;
    }

    .card-title {
        font-size: 18px;
        font-weight: 700;
        margin-top: 8px;
    }

    .card-description {
        font-size: 14px;
        opacity: 0.7;
        margin-top: 7px;
        line-height: 1.5;
    }

    .status {
        font-size: 14px;
        font-weight: 600;
        margin-top: 8px;
    }

    /* Section */
    .section-title {
        font-size: 26px;
        font-weight: 750;
        margin-top: 15px;
        margin-bottom: 10px;
    }

    .section-description {
        opacity: 0.7;
        margin-bottom: 20px;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 25px;
        opacity: 0.6;
        font-size: 13px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HERO
# ====================================================

with st.container(border=True):

    st.title("✈️ SkyHub Airport Data Platform")

    st.subheader(
        "Airport Operations & Flight Intelligence"
    )

    st.write(
        "Monitor airport activity, analyze flight performance, "
        "identify operational risks, and transform aviation data "
        "into meaningful business intelligence."
    )

    st.info(
        "Monitor • Analyze • Understand • Improve"
    )

# ============================================================
# PLATFORM STATUS
# ============================================================

st.markdown(
    '<div class="section-title">🟢 Platform Status</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)


with col1:
    with st.container(border=True):
        st.markdown("### 🗄️ Database")
        st.success("Connected")


with col2:
    with st.container(border=True):
        st.markdown("### ⚙️ ETL Pipeline")
        st.success("Healthy")


with col3:
    with st.container(border=True):
        st.markdown("### 📡 Data Platform")
        st.success("Operational")


# ============================================================
# DATA COVERAGE
# ============================================================

st.markdown(
    '<div class="section-title">📦 Data Coverage</div>',
    unsafe_allow_html=True
)

coverage = [
    ("🛫", "Airlines"),
    ("🗺️", "Routes"),
    ("🛬", "Flights"),
    ("🛄", "Airports"),
    ("✈️", "Aircraft"),
    ("🌤️", "Weather"),
]

cols = st.columns(3)

for i, (icon, name) in enumerate(coverage):

    with cols[i % 3]:

        with st.container(border=True):

            st.markdown(f"## {icon}")

            st.markdown(f"**{name}**")

            st.caption("Available")


# ============================================================
# BUSINESS INTELLIGENCE
# ============================================================

st.markdown(
    '<div class="section-title">📊 Business Intelligence</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="section-description">
        Explore aviation performance, operational efficiency,
        airport activity and route intelligence.
    </div>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# EXECUTIVE OVERVIEW
# ------------------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    with st.container(border=True):

        st.markdown("## 📊")

        st.markdown("### Executive Overview")

        st.write(
            "High-level KPIs, flight trends, operational risks, "
            "airline performance and executive insights."
        )

        st.page_link(
            "pages/Business_Intelligence/Executive_Overview.py",
            label="📊 Open Executive Overview",
            use_container_width=True
        )


# ------------------------------------------------------------
# AIRLINE PERFORMANCE
# ------------------------------------------------------------

with col2:

    with st.container(border=True):

        st.markdown("## ✈️")

        st.markdown("### Airline Performance")

        st.write(
            "Compare airlines using flight volume, delays, "
            "on-time performance and cancellations."
        )

        st.page_link(
            "pages/Business_Intelligence/Airline_performance.py",
            label="✈️ Open Airline Performance",
            use_container_width=True
        )


# ------------------------------------------------------------
# AIRPORT INTELLIGENCE
# ------------------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    with st.container(border=True):

        st.markdown("## 🛫")

        st.markdown("### Airport Intelligence")

        st.write(
            "Analyze airport traffic, delays, reliability, "
            "cancellations and airport rankings."
        )

        st.page_link(
            "pages/Business_Intelligence/Airport_Intelligence.py",
            label="🛫 Open Airport Intelligence",
            use_container_width=True
        )


# ------------------------------------------------------------
# ROUTE INTELLIGENCE
# ------------------------------------------------------------

with col2:

    with st.container(border=True):

        st.markdown("## 🛣️")

        st.markdown("### Route Intelligence")

        st.write(
            "Discover busiest routes, route delays, "
            "reliability and operational risk."
        )

        st.page_link(
            "pages/Business_Intelligence/Route_Intelligence.py",
            label="🛣️ Open Route Intelligence",
            use_container_width=True
        )


# ============================================================
# PLATFORM CAPABILITIES
# ============================================================

st.markdown(
    '<div class="section-title">🚀 Platform Capabilities</div>',
    unsafe_allow_html=True
)

capabilities = [
    (
        "📈",
        "Flight Analytics",
        "Analyze flight volume and trends."
    ),
    (
        "⏱️",
        "Delay Analysis",
        "Monitor operational delays."
    ),
    (
        "🛫",
        "Airport Analytics",
        "Evaluate airport performance."
    ),
    (
        "🛣️",
        "Route Analytics",
        "Identify route risks."
    ),
]

cols = st.columns(4)

for i, (icon, title, description) in enumerate(capabilities):

    with cols[i]:

        with st.container(border=True):

            st.markdown(f"## {icon}")

            st.markdown(f"### {title}")

            st.caption(description)


# ============================================================
# TECHNOLOGY STACK
# ============================================================

st.markdown(
    '<div class="section-title">🧰 Technology Stack</div>',
    unsafe_allow_html=True
)

with st.container(border=True):

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("🐍 **Python**")
        st.markdown("🐼 **Pandas**")
        st.markdown("🔢 **NumPy**")
        st.markdown("🧮 **SQL**")

    with col2:
        st.markdown("🗄️ **PostgreSQL**")
        st.markdown("☁️ **Neon**")
        st.markdown("📦 **CSV / Parquet**")
        st.markdown("🧪 **Pytest**")

    with col3:
        st.markdown("🖥️ **Streamlit**")
        st.markdown("📊 **Power BI**")
        st.markdown("📓 **Jupyter**")
        st.markdown("📝 **Logging**")

    with col4:
        st.markdown("🔧 **Git**")
        st.markdown("🐙 **GitHub**")
        st.markdown("📊 **Data Analytics**")
        st.markdown("✈️ **Aviation Intelligence**")


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div class="footer">

        ✈️ <b>SkyHub Airport Data Platform</b>
        <br>
        Airport Operations & Flight Intelligence
        <br><br>
        Monitor • Analyze • Understand • Improve

    </div>
    """,
    unsafe_allow_html=True
)