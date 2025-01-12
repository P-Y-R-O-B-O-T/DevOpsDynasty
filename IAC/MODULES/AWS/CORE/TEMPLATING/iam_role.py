import streamlit as st
import CORE_FUNCTIONS.constants_n_conf as CONSTANTS

#$$$$$$$$$$#
MODULE_NAME = "AWS"

class MODULE:
    def __init__(self) -> None:
        self.MAP_VERSIONS_METHODS_TEMPLATE = {
            "5.81.0": self.templete_5_81_0
        }

    def template(self,
                 resources_data: dict) -> str :
        st.write(st.session_state[CONSTANTS.EXISTING_PROJECTS])
        st.write(st.session_state[CONSTANTS.EXISTING_PROJECTS][st.session_state[CONSTANTS.SELECTED_PROJECT]])
        st.write(st.session_state[CONSTANTS.EXISTING_PROJECTS][st.session_state[CONSTANTS.SELECTED_PROJECT]][CONSTANTS.CONF_EXISTING_PROJECTS])
        return self.MAP_VERSIONS_METHODS_TEMPLATE[st.session_state[CONSTANTS.EXISTING_PROJECTS][st.session_state[CONSTANTS.SELECTED_PROJECT]][CONSTANTS.CONF_EXISTING_PROJECTS][CONSTANTS.PROVIDERS][MODULE_NAME]](resources_data)

    def templete_5_81_0(self,
                        resources_data: dict) -> str :
        pass

#$$$$$$$$$$#

OBJ = MODULE()
