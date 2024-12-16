import streamlit as st

#$$$$$$$$$$#

def create_toast(text, icon) -> None :
    if "toast_messages" in st.session_state :
        st.session_state["toast_messages"].append([text, icon])
    else :
        st.session_state["toast_messages"] = [[text, icon]]

def display_toasts() -> None :
    if "toast_messages" in st.session_state :
        for _ in st.session_state["toast_messages"] :
            st.toast(_[0], icon=_[1])
        st.session_state["toast_messages"] = []
