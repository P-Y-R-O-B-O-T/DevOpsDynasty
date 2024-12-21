import streamlit as st
import CORE_FUNCTIONS.constants_n_conf as CONSTANTS

#$$$$$$$$$$#

class CONFIG :
    def __init__(self) -> None:
        st.write("# Config page")
        if CONSTANTS.RESOURCE_CONF in st.session_state :
            st.write(st.session_state[CONSTANTS.RESOURCE_CONF])

#$$$$$$$$$$#

CONFIG()
