import streamlit as st
import CORE_FUNCTIONS.constants_n_conf as CONSTANTS
import CORE_FUNCTIONS.toasts as TOAST

# $$$$$$$$$$#

MODULE_NAME = "AWS"
RESOURCE_NAME = "aws_iam_role"

# $$$$$$$$$$#


class MODULE:
    def __init__(self) -> None:
        self.MAP_VERSIONS_METHODS_DELETION_OBLIGATIONS = {
            "5.81.0": self.deletion_obligations_5_81_0
        }
        self.MAP_VERSIONS_METHODS_DELETION = {"5.81.0": self.delete_resource_5_81_0}

    def delete_resource(self, resource_name: str) -> None:
        self.MAP_VERSIONS_METHODS_DELETION[
            st.session_state[CONSTANTS.EXISTING_PROJECTS][
                st.session_state[CONSTANTS.SELECTED_PROJECT]
            ][CONSTANTS.CONF_EXISTING_PROJECTS][CONSTANTS.PROVIDERS][
                MODULE_NAME.lower()
            ]
        ](resource_name)
        st.rerun()

    def delete_resource_5_81_0(self, resource_name: str) -> None:
        obligations = self.deletion_obligations()
        if obligations == None:
            del st.session_state[CONSTANTS.RESOURCE_CONF][CONSTANTS.RESOURCES][
                MODULE_NAME.lower()
            ][RESOURCE_NAME][resource_name]
            TOAST.create_toast(
                f"The {RESOURCE_NAME} {resource_name} has been deleted", "✅"
            )
        else:
            TOAST.create_toast(
                f"The {RESOURCE_NAME} {resource_name} is being used by some other resource",
                "⚠️",
            )

    def deletion_obligations(self) -> dict[str, str | list[str]] | None:
        self.MAP_VERSIONS_METHODS_DELETION_OBLIGATIONS[
            st.session_state[CONSTANTS.EXISTING_PROJECTS][
                st.session_state[CONSTANTS.SELECTED_PROJECT]
            ][CONSTANTS.CONF_EXISTING_PROJECTS][CONSTANTS.PROVIDERS][
                MODULE_NAME.lower()
            ]
        ]()

    def deletion_obligations_5_81_0(self) -> None:
        pass


# $$$$$$$$$$#

OBJ = MODULE()
