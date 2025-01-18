import streamlit as st

import CORE_FUNCTIONS.constants_n_conf as CONSTANTS
import CORE_FUNCTIONS.tf_conf as TF

# $$$$$$$$$$#


class CONF_DISPLAY:
    def __init__(self) -> None:
        if self.project_selected():
            self.conf()

    def project_selected(self) -> bool:
        if (
            CONSTANTS.SELECTED_PROJECT in st.session_state
            and st.session_state[CONSTANTS.SELECTED_PROJECT] != None
        ):
            return True
        return False

    def conf(self) -> None:
        st.header(f"Configuration: {st.session_state[CONSTANTS.SELECTED_PROJECT]}")
        st.code(
            TF.conf_in_tf_syntax(), language="tcl", line_numbers=True, wrap_lines=True
        )


# $$$$$$$$$$#

CONF_DISPLAY()
