import streamlit as st
from pathlib import Path


# ============================================================
# DASHBOARD DIRECTORY
# ============================================================

DASHBOARD_DIR = Path(__file__).resolve().parent

PAGES_DIR = DASHBOARD_DIR / "pages"

BI_DIR = PAGES_DIR / "Business_Intelligence"
Op_DIR = PAGES_DIR / "Operations"
An_DIR = PAGES_DIR / "analytics"


# ============================================================
# NAVIGATION
# ============================================================

def create_navigation():

    pages = {

        "🏠 HOME": [

            st.Page(
                PAGES_DIR / "Home.py",
                title="Home",
                icon="🏠"
            ),

        ],

        "📊 BUSINESS INTELLIGENCE": [

            st.Page(
                BI_DIR / "Executive_Overview.py",
                title="Executive Overview",
                icon="📊"
            ),

            st.Page(
                BI_DIR / "Airline_performance.py",
                title="Airline Performance",
                icon="✈️"
            ),

            st.Page(
                BI_DIR / "Airport_Intelligence.py",
                title="Airport Intelligence",
                icon="🛫"
            ),

            st.Page(
                BI_DIR / "Route_Intelligence.py",
                title="Route Intelligence",
                icon="🛣️"
            ),

        ],
          "🌦️Operations": [
        
                    st.Page(
                        Op_DIR / "flight_operation.py",
                        title="Flight Operation",
                        icon="✈️"
                    ),
                    st.Page(
                        Op_DIR/"weather_vs_flight.py",
                        title="Flight vs weather",
                        icon="🌦️"
                    ),
                    st.Page(
                         Op_DIR/"Airplane_analysis.py",
                         title="Fleet /Airplane analysis",
                         icon="🛩️"
                                        ),


                    ],





                     "📊 Analytics": [
                            
                                        st.Page(
                                            An_DIR / "delay_analysis.py",
                                            title="Delay Analysis",
                                            icon="📊"
                                        ),
                                         st.Page(
                                                                                    An_DIR / "cancellation.py",
                                                                                    title="cancellation Analysis",
                                                                                    icon="📊"
                                                                                ),
                                        
                    
                                        ],





    }

    return st.navigation(pages)