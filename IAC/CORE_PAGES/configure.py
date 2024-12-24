import streamlit as st
import os
import importlib

import CORE_FUNCTIONS.constants_n_conf as CONSTANTS

#$$$$$$$$$$#

@st.cache_resource
def load_modules() -> dict :
    modules = {}
    for _ in os.listdir(CONSTANTS.MODULES_DIR) :
        modules[_] = {CONSTANTS.UI_MODULES: {},
                      CONSTANTS.TEMPLATING_MODULES: {}}
        for __ in os.listdir(os.path.join(CONSTANTS.MODULES_DIR, _, CONSTANTS.MODULES_PAGES_DIR)) :
            if os.path.isfile(os.path.join(CONSTANTS.MODULES_DIR, _, CONSTANTS.MODULES_PAGES_DIR, __)) :
                modules[_][CONSTANTS.UI_MODULES][__.upper()] = importlib.import_module(f"{CONSTANTS.MODULES_DIR}.{_}.{CONSTANTS.MODULES_PAGES_DIR}.{__[:-3]}")
                modules[_][CONSTANTS.TEMPLATING_MODULES][__.upper()] = importlib.import_module(f"{CONSTANTS.MODULES_DIR}.{_}.{CONSTANTS.MODULES_CORE_DIR}.{CONSTANTS.MODULES_CORE_TEMPLATING_DIR}.{__[:-3]}")
    return modules

MODULES = load_modules()

#$$$$$$$$$$#

class CONFIG :
    def __init__(self) -> None:
        st.write("# Config page")
        if CONSTANTS.RESOURCE_CONF in st.session_state :
            st.write(st.session_state[CONSTANTS.RESOURCE_CONF])

#$$$$$$$$$$#

CONFIG()
