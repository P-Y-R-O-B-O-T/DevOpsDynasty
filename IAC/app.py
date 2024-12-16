import streamlit as st

#$$$$$$$$$$#

class MAIN_APP :
    def __init__(self) -> None:
        self.page_config()
        self.create_sidebar()

    def create_sidebar(self) :
        navigations = {
            "project": st.Page("CORE_PAGES/project.py", title="🚀 Manage Projects"),
            "config": st.Page("CORE_PAGES/configure.py", title="🛠️ Configure Resources")
        }
        page_navigations = st.navigation([navigations[_] for _ in navigations])
        page_navigations.run()

    def page_config(self) :
        st.set_page_config(page_title="DevOpsDynasty", page_icon="☁️", layout="wide")

MAIN_APP()
