import streamlit as st
st.set_page_config(
    page_title="4cast",
    layout="wide"
)
page = st.sidebar.radio("Go to", ["about","dataset", "insights", "prediction"])
from 4cast.pages import about, dataset, insights, prediction
# Load the appropriate page
if page == "about":
    about.show()
elif page == "dataset":
    dataset.main()
elif page == "insights":
    insights.main()
elif page == "prediction":
    prediction.main()
