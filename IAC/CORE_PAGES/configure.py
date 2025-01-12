from re import L
from pandas.core.dtypes.dtypes import re
import streamlit as st
import os
import importlib

import CORE_FUNCTIONS.constants_n_conf as CONSTANTS

#$$$$$$$$$$#

@st.cache_resource
def load_modules() -> dict :
    modules = {}
    for _ in os.listdir(CONSTANTS.MODULES_DIR) :
        modules[_.lower()] = {CONSTANTS.UI_MODULES: {},
                      CONSTANTS.TEMPLATING_MODULES: {}}
        for __ in os.listdir(os.path.join(CONSTANTS.MODULES_DIR, _, CONSTANTS.MODULES_PAGES_DIR)) :
            if os.path.isfile(os.path.join(CONSTANTS.MODULES_DIR, _, CONSTANTS.MODULES_PAGES_DIR, __)) :
                st.write(_, __)
                modules[_.lower()][CONSTANTS.UI_MODULES][__.lower()[:-3]] = importlib.import_module(f"{CONSTANTS.MODULES_DIR}.{_}.{CONSTANTS.MODULES_PAGES_DIR}.{__[:-3]}")
                modules[_.lower()][CONSTANTS.TEMPLATING_MODULES][__.lower()[:-3]] = importlib.import_module(f"{CONSTANTS.MODULES_DIR}.{_}.{CONSTANTS.MODULES_CORE_DIR}.{CONSTANTS.MODULES_CORE_TEMPLATING_DIR}.{__[:-3]}")
    return modules

MODULES = load_modules()

#$$$$$$$$$$#

class CONFIG :
    def __init__(self) -> None:
        if CONSTANTS.RESOURCE_CONF in st.session_state :
            self.sidebar()
            self.main_ui()

    def main_ui(self) -> None :
        st.write("# Config page")
        if st.session_state[CONSTANTS.SELECTED_RESOURCE] == None :
            st.write("Select a resource to configure")
            return
        st.write(st.session_state[CONSTANTS.SELECTED_RESOURCE])
        st.write(st.session_state[CONSTANTS.RESOURCE_CONF])
        st.write(st.session_state[CONSTANTS.EXISTING_PROJECTS])
        st.write(st.session_state[CONSTANTS.EXISTING_PROJECTS][st.session_state[CONSTANTS.SELECTED_PROJECT]][CONSTANTS.CONF_EXISTING_PROJECTS][CONSTANTS.PROVIDERS])
        used_resource_col, resource_list_col = st.columns([1, 3])

        with used_resource_col :
            self.used_resources()
        with resource_list_col :
            create_resource_button = st.button("Create New Resource",
                                               key=f"create_resource_{st.session_state[CONSTANTS.SELECTED_RESOURCE]}",
                                               type="primary",
                                               use_container_width=True)
            if create_resource_button :
                st.write(MODULES)
                provider = st.session_state[CONSTANTS.SELECTED_RESOURCE][:st.session_state[CONSTANTS.SELECTED_RESOURCE].find("_")]
                resource_type = st.session_state[CONSTANTS.SELECTED_RESOURCE][st.session_state[CONSTANTS.SELECTED_RESOURCE].find("_")+1:]
                MODULES[provider][CONSTANTS.UI_MODULES][resource_type].OBJ.create_resource()


            self.resource_list()

    def used_resources(self) -> None :
        for _ in st.session_state[CONSTANTS.RESOURCE_CONF] :
            for __ in st.session_state[CONSTANTS.RESOURCE_CONF][_] :
                used_resource_select_button = st.button(f"{_.lower()}_{__.lower()}",
                                                        key=f"used_resource_selection{_.lower()}_{__.lower()}",
                                                        use_container_width=True)
                if used_resource_select_button :
                    st.session_state[CONSTANTS.SELECTED_RESOURCE] = f"{_.lower()}_{__.lower()}"
                    st.rerun()

    def resource_list(self) -> None :
        st.write("this clumn will be used to list all the resources of the selected type that are being used in the current project")
        st.session_state[CONSTANTS.RESOURCE_CONF]
        st.write(st.session_state[CONSTANTS.SELECTED_RESOURCE].find("_"))
        provider = st.session_state[CONSTANTS.SELECTED_RESOURCE][:st.session_state[CONSTANTS.SELECTED_RESOURCE].find("_")]
        resource_type = st.session_state[CONSTANTS.SELECTED_RESOURCE][st.session_state[CONSTANTS.SELECTED_RESOURCE].find("_")+1:]
        if provider in st.session_state[CONSTANTS.RESOURCE_CONF] and resource_type in st.session_state[CONSTANTS.RESOURCE_CONF][provider] :
            for _ in st.session_state[CONSTANTS.RESOURCE_CONF][provider][resource_type] :
                with st.container(border=True) :
                    st.subheader(_)
                    st.write(st.session_state[CONSTANTS.RESOURCE_CONF][provider][resource_type][_])

    def sidebar(self) -> None :
        with st.sidebar :
            for _ in MODULES :
                if _.lower() in st.session_state[CONSTANTS.EXISTING_PROJECTS][st.session_state[CONSTANTS.SELECTED_PROJECT]][CONSTANTS.CONF_EXISTING_PROJECTS][CONSTANTS.PROVIDERS] :
                    st.write(_)
                    for __ in MODULES[_][CONSTANTS.UI_MODULES] :
                        resource_select_button = st.button(f"{_.lower()}_{__.lower()}",
                                                           key=f"resource_selection{_}_{__}",
                                                           use_container_width=True)
                        if resource_select_button :
                            st.session_state[CONSTANTS.SELECTED_RESOURCE] = f"{_.lower()}_{__.lower()}"

#$$$$$$$$$$#

CONFIG()
