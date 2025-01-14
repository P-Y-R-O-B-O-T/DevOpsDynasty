import streamlit as st
import os
import importlib

import CORE_FUNCTIONS.constants_n_conf as CONSTANTS
import CORE_FUNCTIONS.toasts as TOAST

#$$$$$$$$$$#

#@st.cache_resource
def load_modules() -> dict :
    modules = {}
    for _ in os.listdir(CONSTANTS.MODULES_DIR) :
        modules[_.lower()] = {CONSTANTS.UI_MODULES: {},
                              CONSTANTS.TEMPLATING_MODULES: {},
                              CONSTANTS.DELETION_MODULES: {}}
        for __ in os.listdir(os.path.join(CONSTANTS.MODULES_DIR, _, CONSTANTS.MODULES_PAGES_DIR)) :
            if os.path.isfile(os.path.join(CONSTANTS.MODULES_DIR, _, CONSTANTS.MODULES_PAGES_DIR, __)) :
                modules[_.lower()][CONSTANTS.UI_MODULES][__.lower()[:-3]] = importlib.import_module(f"{CONSTANTS.MODULES_DIR}.{_}.{CONSTANTS.MODULES_PAGES_DIR}.{__[:-3]}")
                modules[_.lower()][CONSTANTS.TEMPLATING_MODULES][__.lower()[:-3]] = importlib.import_module(f"{CONSTANTS.MODULES_DIR}.{_}.{CONSTANTS.MODULES_CORE_DIR}.{CONSTANTS.MODULES_CORE_TEMPLATING_DIR}.{__[:-3]}")
                modules[_.lower()][CONSTANTS.DELETION_MODULES][__.lower()[:-3]] = importlib.import_module(f"{CONSTANTS.MODULES_DIR}.{_}.{CONSTANTS.MODULES_CORE_DIR}.{CONSTANTS.MODULES_CORE_DELETION_DIR}.{__[:-3]}")
    return modules

MODULES = load_modules()

st.write(MODULES)

#$$$$$$$$$$#

class CONFIG :
    def __init__(self) -> None:
        if CONSTANTS.RESOURCE_CONF in st.session_state :
            self.show_toasts()
            self.sidebar()
            self.main_ui()

    def show_toasts(self) -> None :
        TOAST.display_toasts()

    def main_ui(self) -> None :
        if st.session_state[CONSTANTS.SELECTED_RESOURCE] == None :
            st.write("# Config Page")
            st.write("Select a resource to configure")
            return
        col1, col2 = st.columns([8, 1])
        with col1 :
            st.write(f"# Config Page {st.session_state[CONSTANTS.SELECTED_RESOURCE]}")
        with col2 :
            create_resource_button = st.button("## Create",
                                               key=f"create_resource_{st.session_state[CONSTANTS.SELECTED_RESOURCE]}",
                                               type="primary",
                                               use_container_width=True)
            if create_resource_button :
                provider = st.session_state[CONSTANTS.SELECTED_RESOURCE][:st.session_state[CONSTANTS.SELECTED_RESOURCE].find("_")]
                resource_type = st.session_state[CONSTANTS.SELECTED_RESOURCE]
                MODULES[provider][CONSTANTS.UI_MODULES][resource_type].OBJ.create_resource()
        used_resource_col, resource_list_col = st.columns([1, 3])

        with used_resource_col :
            self.used_resources()
        with resource_list_col :
            self.resource_list()

    def used_resources(self) -> None :
        st.subheader("Used Resources")
        for _ in st.session_state[CONSTANTS.RESOURCE_CONF][CONSTANTS.RESOURCES] :
            for __ in st.session_state[CONSTANTS.RESOURCE_CONF][CONSTANTS.RESOURCES][_] :
                used_resource_select_button = st.button(f"{__.lower()}",
                                                        #key=f"used_resource_selection{_.lower()}_{__.lower()}",
                                                        use_container_width=True)
                if used_resource_select_button :
                    st.session_state[CONSTANTS.SELECTED_RESOURCE] = f"{__.lower()}"
                    st.rerun()

    def resource_list(self) -> None :
        provider = st.session_state[CONSTANTS.SELECTED_RESOURCE][:st.session_state[CONSTANTS.SELECTED_RESOURCE].find("_")]
        resource_type = st.session_state[CONSTANTS.SELECTED_RESOURCE]
        if provider in st.session_state[CONSTANTS.RESOURCE_CONF][CONSTANTS.RESOURCES] and resource_type in st.session_state[CONSTANTS.RESOURCE_CONF][CONSTANTS.RESOURCES][provider] :
            for _ in st.session_state[CONSTANTS.RESOURCE_CONF][CONSTANTS.RESOURCES][provider][resource_type] :
                with st.container(border=True) :
                    st.subheader(_)
                    st.write(st.session_state[CONSTANTS.RESOURCE_CONF][CONSTANTS.RESOURCES][provider.lower()][resource_type.lower()][_])
                    col1, col2 = st.columns([1, 1])
                    with col1 :
                        edit_button = st.button("Edit",
                                                use_container_width=True,
                                                key=f"edit_{st.session_state[CONSTANTS.SELECTED_RESOURCE]}_{_}")
                        if edit_button :
                            MODULES[provider][CONSTANTS.UI_MODULES][resource_type].OBJ.modify_resource(name=_,
                                                                                                       data=st.session_state[CONSTANTS.RESOURCE_CONF][CONSTANTS.RESOURCES][provider.lower()][resource_type.lower()][_])
                    with col2 :
                        deletion_button = st.button("Delete",
                                                    use_container_width=True,
                                                    key=f"delete_{st.session_state[CONSTANTS.SELECTED_RESOURCE]}_{_}")
                        if deletion_button :
                            self.resource_deletion_prompt(_)


    @st.dialog("Delete Resource")
    def resource_deletion_prompt(self,
                                 resource_name: str) -> None :
        st.markdown(f"""
        ### Enter resource name below to delete the resource
        ( {resource_name} )
        """)
        prompt = st.text_input("", "",
                               key=f"deletion_prompt_{st.session_state[CONSTANTS.SELECTED_RESOURCE]}_{resource_name}")
        delete_button = st.button(label="Delete",
                                  type="primary",
                                  use_container_width=True,
                                  key=f"deletion_submition_button_{st.session_state[CONSTANTS.SELECTED_RESOURCE]}_{resource_name}")

        if prompt == resource_name and delete_button :
            #try :
                # os.system(f"rm {os.path.join(CONSTANTS.PROJECTS_DIR,
                #                              project)} -r")
                #
                # if CONSTANTS.SELECTED_PROJECT in st.session_state :
                #     del st.session_state[CONSTANTS.SELECTED_PROJECT]
                #
                # del st.session_state[CONSTANTS.EXISTING_PROJECTS][project]
            provider = st.session_state[CONSTANTS.SELECTED_RESOURCE][:st.session_state[CONSTANTS.SELECTED_RESOURCE].find("_")]
            resource_type = st.session_state[CONSTANTS.SELECTED_RESOURCE]


            MODULES[provider][CONSTANTS.DELETION_MODULES][resource_type].OBJ.delete_resource(resource_name)
            #
            # if obligations == None :
            #
            #     TOAST.create_toast(f"Resource {resource_name} deleted", "🌟")
            # else :
            #     TOAST.create_toast(f"Resource {resource_name} can't be deleted", "🌟")
            # st.rerun()



    def sidebar(self) -> None :
        with st.sidebar :
            for _ in MODULES :
                if _.lower() in st.session_state[CONSTANTS.EXISTING_PROJECTS][st.session_state[CONSTANTS.SELECTED_PROJECT]][CONSTANTS.CONF_EXISTING_PROJECTS][CONSTANTS.PROVIDERS] :
                    st.write(_)
                    for __ in MODULES[_][CONSTANTS.UI_MODULES] :
                        resource_select_button = st.button(f"{__.lower()}",
                                                           key=f"resource_selection{_}_{__}",
                                                           use_container_width=True)
                        if resource_select_button :
                            st.session_state[CONSTANTS.SELECTED_RESOURCE] = f"{__.lower()}"

#$$$$$$$$$$#

CONFIG()
