import streamlit as st
import CORE_FUNCTIONS.constants_n_conf as CONSTANTS

#$$$$$$$$$$#

MODULE_NAME = "AWS"
RESOURCE_NAME = "aws_iam_role"

class MODULE:
    def __init__(self) -> None:
        self.MAP_VERSIONS_METHODS_TEMPLATE = {
            "5.81.0": self.template_5_81_0
        }

    def template(self,
                 resources_data: dict) -> str :
        # return self.MAP_VERSIONS_METHODS_TEMPLATE[st.session_state[CONSTANTS.EXISTING_PROJECTS][st.session_state[CONSTANTS.SELECTED_PROJECT]][CONSTANTS.CONF_EXISTING_PROJECTS][CONSTANTS.PROVIDERS][MODULE_NAME]](resources_data)
        return "TEMPLATE_DATA"

    def template_5_81_0(self,
                        resources_data: dict) -> str :
        pass

#$$$$$$$$$$#

OBJ = MODULE()
