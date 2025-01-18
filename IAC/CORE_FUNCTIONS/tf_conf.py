import streamlit as st
import CORE_FUNCTIONS.constants_n_conf as CONSTANTS

#$$$$$$$$$$#

def conf_in_tf_syntax(modules: dict) -> str :
    templated_resource_confs = []
    for _ in st.session_state[CONSTANTS.RESOURCE_CONF][CONSTANTS.RESOURCES]:
        for __ in st.session_state[CONSTANTS.RESOURCE_CONF][
            CONSTANTS.RESOURCES
        ][_]:
            templated_resource_confs.append(
                modules[_][__][CONSTANTS.TEMPLATING_MODULE].OBJ.template()
            )
    complete_tf_conf = "\n".join(templated_resource_confs)

    return complete_tf_conf
