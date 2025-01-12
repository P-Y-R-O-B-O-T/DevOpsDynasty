import streamlit as st
import CORE_FUNCTIONS.constants_n_conf as CONSTANTS

#$$$$$$$$$$#

MODULE_NAME = "AWS"

class MODULE:
    def __init__(self) -> None:
        self.MAP_VERSIONS_METHODS_CREATE = {
            "5.81.0": self.create_resource_5_81_0
        }
        self.MAP_VERSIONS_METHODS_MODIFY = {
            "5.81.0": self.modify_resource_5_81_0
        }

    def create_resource(self) -> None :

        st.write(st.session_state[CONSTANTS.EXISTING_PROJECTS])
        st.write(st.session_state[CONSTANTS.EXISTING_PROJECTS][st.session_state[CONSTANTS.SELECTED_PROJECT]])
        st.write(st.session_state[CONSTANTS.EXISTING_PROJECTS][st.session_state[CONSTANTS.SELECTED_PROJECT]][CONSTANTS.CONF_EXISTING_PROJECTS])
        self.MAP_VERSIONS_METHODS_CREATE[st.session_state[CONSTANTS.EXISTING_PROJECTS][st.session_state[CONSTANTS.SELECTED_PROJECT]][CONSTANTS.CONF_EXISTING_PROJECTS][CONSTANTS.PROVIDERS][MODULE_NAME.lower()]]()

    @st.dialog("IAM Role")
    def create_resource_5_81_0(self) -> None :
        pass

    def modify_resource(self) -> None :
        self.MAP_VERSIONS_METHODS_MODIFY[st.session_state[CONSTANTS.EXISTING_PROJECTS][st.session_state[CONSTANTS.SELECTED_PROJECT]][CONSTANTS.CONF_EXISTING_PROJECTS][CONSTANTS.PROVIDERS][MODULE_NAME]]()

    @st.dialog("IAM Role")
    def modify_resource_5_81_0(self) -> None :
        pass

#$$$$$$$$$$#

OBJ = MODULE()
