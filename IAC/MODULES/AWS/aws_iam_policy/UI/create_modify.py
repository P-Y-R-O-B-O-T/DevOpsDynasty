import streamlit as st
import CORE_FUNCTIONS.constants_n_conf as CONSTANTS
import CORE_FUNCTIONS.input_validation as IV
import CORE_FUNCTIONS.toasts as TOAST

# $$$$$$$$$$#

MODULE_NAME = "AWS"
RESOURCE_NAME = "aws_iam_policy"


class MODULE:
    def __init__(self) -> None:
        self.MAP_VERSIONS_METHODS_CREATE = {"5.81.0": self.create_resource_5_81_0}
        self.MAP_VERSIONS_METHODS_MODIFY = {"5.81.0": self.modify_resource_5_81_0}

        self.VERSIONS = list(self.MAP_VERSIONS_METHODS_CREATE.keys())

    def create_resource(self) -> None:

        self.MAP_VERSIONS_METHODS_CREATE[
            st.session_state[CONSTANTS.EXISTING_PROJECTS][
                st.session_state[CONSTANTS.SELECTED_PROJECT]
            ][CONSTANTS.CONF_EXISTING_PROJECTS][CONSTANTS.PROVIDERS][
                MODULE_NAME.lower()
            ]
        ]()

    def add_resource(self, name: str, data: dict, force: bool = False) -> None:
        if (
            MODULE_NAME.lower()
            not in st.session_state[CONSTANTS.RESOURCE_CONF][CONSTANTS.RESOURCES]
        ):
            st.session_state[CONSTANTS.RESOURCE_CONF][CONSTANTS.RESOURCES][
                MODULE_NAME.lower()
            ] = {}
        if (
            RESOURCE_NAME.lower()
            not in st.session_state[CONSTANTS.RESOURCE_CONF][CONSTANTS.RESOURCES][
                MODULE_NAME.lower()
            ]
        ):
            st.session_state[CONSTANTS.RESOURCE_CONF][CONSTANTS.RESOURCES][
                MODULE_NAME.lower()
            ][RESOURCE_NAME] = {}

        if force == True:
            st.session_state[CONSTANTS.RESOURCE_CONF][CONSTANTS.RESOURCES][
                MODULE_NAME.lower()
            ][RESOURCE_NAME][name] = data
            TOAST.create_toast(f"Resource {name} created successfully", "✅")
            st.rerun()
        if force == False:
            if (
                name
                not in st.session_state[CONSTANTS.RESOURCE_CONF][CONSTANTS.RESOURCES][
                    MODULE_NAME.lower()
                ][RESOURCE_NAME]
            ):
                st.session_state[CONSTANTS.RESOURCE_CONF][CONSTANTS.RESOURCES][
                    MODULE_NAME.lower()
                ][RESOURCE_NAME][name] = data
                TOAST.create_toast(f"Resource {name} created successfully", "✅")
                st.rerun()
            else:
                TOAST.create_toast(f"Resource with name {name} already exists", "⚠️")
                st.rerun()

    @st.dialog(f"Create {RESOURCE_NAME}")
    def create_resource_5_81_0(self) -> None:
        name = st.text_input("Name", key=f"{RESOURCE_NAME}_creation_name_input")

        # resource input steps
        path = st.text_input("Path", key=f"{RESOURCE_NAME}_creation_path_input", value="/")
        description = st.text_input("Description", key=f"{RESOURCE_NAME}_creation_description_input")
        policy = st.text_area(
            "Policy", key=f"{RESOURCE_NAME}_creation_policy_input"
        )

        submit_button = st.button(
            "Submit", key=f"{RESOURCE_NAME}_creation_submit_button"
        )

        if submit_button:
            if not name :
                TOAST.create_toast("Name is necessary", "⚠️")
                st.rerun()

            if not IV.a_zA_z0_9(name):
                TOAST.create_toast(
                    "Name can only have [A-Za-z0-9] and length less then 53",
                    "⚠️",
                )
                st.rerun()
            if not path :
                TOAST.create_toast("Path is necessary", "⚠️")
                st.rerun()

            if not policy :
                TOAST.create_toast("Policy is necessary", "⚠️")
                st.rerun()

            self.add_resource(name=name, data={"name": name, "path": path, "description": description, "policy": policy})
            st.rerun()

    def modify_resource(self, name: str, data: dict) -> None:
        self.MAP_VERSIONS_METHODS_MODIFY[
            st.session_state[CONSTANTS.EXISTING_PROJECTS][
                st.session_state[CONSTANTS.SELECTED_PROJECT]
            ][CONSTANTS.CONF_EXISTING_PROJECTS][CONSTANTS.PROVIDERS][
                MODULE_NAME.lower()
            ]
        ](name, data)

    @st.dialog(f"Edit {RESOURCE_NAME}")
    def modify_resource_5_81_0(self, name: str, data: dict) -> None:
        name = st.text_input(
            label="Name",
            value=name,
            disabled=True,
            key=f"{RESOURCE_NAME}_modification_name_input",
        )

        path = st.text_input("Path", key=f"{RESOURCE_NAME}_creation_path_input", value=data["path"])
        description = st.text_input("Description", key=f"{RESOURCE_NAME}_creation_description_input", value=data["description"])
        policy = st.text_area(
            "Policy", key=f"{RESOURCE_NAME}_creation_policy_input", value=data["policy"]
        )
        # resource input steps

        submit_button = st.button(
            "Submit", key=f"{RESOURCE_NAME}_modification_submit_button"
        )

        if submit_button:
            # resource addition steps
            if not path :
                TOAST.create_toast("Path is necessary", "⚠️")
                st.rerun()
            if not policy :
                TOAST.create_toast("Policy is necessary", "⚠️")
                st.rerun()
            self.add_resource(name=name, data={"name": name, "path": path, "description": description, "policy": policy}, force=True)
            st.rerun()


# $$$$$$$$$$#

OBJ = MODULE()
