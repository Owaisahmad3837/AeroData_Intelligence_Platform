import streamlit as st


st.set_page_config(
  page_title="SkyHub Airport Data Platform",
  page_icon="✈️",
  layout="wide"
)


st.title("✈️ SkyHub Airport Data Platform")
st.write("This is full SkyHub Airport Data Platform")


st.markdown("""
### Airport Operations & Flight Intelligence

Welcome to the SkyHub Airport Data Platform.

Use the navigation menu to explore:

- Flight operations
- Airline performance
- Airport analysis
- Data explorer
- Data quality
- Pipeline monitoring
""")
st.divider()

st.subheader("Platform Overview")

col1,col2,col3=st.columns(3)

with col1:
  st.metric("Data Platform", "Online")

with col2:
  st.metric("Database", "PostgreSQL")


with col3:
    st.metric("Pipeline", "Ready")