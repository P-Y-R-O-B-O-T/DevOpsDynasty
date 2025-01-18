import streamlit as st
import CORE_FUNCTIONS.constants_n_conf as CONSTANTS
import CORE_FUNCTIONS.load_modules as LM

# $$$$$$$$$$#

MODULES = LM.load_modules([CONSTANTS.TEMPLATING_MODULE])

# $$$$$$$$$$#


def conf_in_tf_syntax() -> str:
    templated_resource_confs = []
    for _ in st.session_state[CONSTANTS.RESOURCE_CONF][CONSTANTS.RESOURCES]:
        for __ in st.session_state[CONSTANTS.RESOURCE_CONF][CONSTANTS.RESOURCES][_]:
            templated_resource_confs.append(
                MODULES[_][__][CONSTANTS.TEMPLATING_MODULE].OBJ.template()
            )
    complete_tf_conf = "\n".join(templated_resource_confs)

    return complete_tf_conf
