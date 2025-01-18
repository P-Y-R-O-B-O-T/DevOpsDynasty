import streamlit as st
import os
import json

import CORE_FUNCTIONS.constants_n_conf as CONSTANTS
import CORE_FUNCTIONS.toasts as TOAST
import CORE_FUNCTIONS.tf_conf as TF
import CORE_FUNCTIONS.load_modules as LM

# $$$$$$$$$$#

MODULES = LM.load_modules(
    modules_needed=[CONSTANTS.UI_MODULE, CONSTANTS.DELETION_MODULE]
)

# $$$$$$$$$$#


class CONFIG:
    def __init__(self) -> None:
        if CONSTANTS.RESOURCE_CONF in st.session_state:
            self.show_toasts()
            self.sidebar()
            self.main_ui()

    def show_toasts(self) -> None:
        TOAST.display_toasts()

    def main_ui(self) -> None:
        if st.session_state[CONSTANTS.SELECTED_RESOURCE] == None:
            st.write("# Config Page")
            st.write("Select a resource to configure")
            return
        st.write(f"# Config Page {st.session_state[CONSTANTS.SELECTED_RESOURCE]}")
        col1, col2 = st.columns([1, 1])
        with col1:
            save_resource_conf_button = st.button(
                "## Save",
                type="primary",
                use_container_width=True,
                key=f"save_config_button",
            )
            if save_resource_conf_button:
                self.save_resource_conf()
                self.save_tf_main_file()
        with col2:
            create_resource_button = st.button(
                "## Create",
                key=f"create_resource_{st.session_state[CONSTANTS.SELECTED_RESOURCE]}",
                type="primary",
                use_container_width=True,
            )
            if create_resource_button:
                provider = st.session_state[CONSTANTS.SELECTED_RESOURCE][
                    : st.session_state[CONSTANTS.SELECTED_RESOURCE].find("_")
                ]
                resource_type = st.session_state[CONSTANTS.SELECTED_RESOURCE]
                MODULES[provider][resource_type][
                    CONSTANTS.UI_MODULE
                ].OBJ.create_resource()
        used_resource_col, resource_list_col = st.columns([1, 3])

        with used_resource_col:
            self.used_resources()
        with resource_list_col:
            self.resource_list()

    def used_resources(self) -> None:
        st.subheader("Used Resources")
        for _ in st.session_state[CONSTANTS.RESOURCE_CONF][CONSTANTS.RESOURCES]:
            for __ in st.session_state[CONSTANTS.RESOURCE_CONF][CONSTANTS.RESOURCES][_]:
                used_resource_select_button = st.button(
                    f"{__.lower()}",
                    use_container_width=True,
                    key=f"used_resource_selection_{__}",
                )
                if used_resource_select_button:
                    st.session_state[CONSTANTS.SELECTED_RESOURCE] = f"{__.lower()}"
                    st.rerun()

    def resource_list(self) -> None:
        provider = st.session_state[CONSTANTS.SELECTED_RESOURCE][
            : st.session_state[CONSTANTS.SELECTED_RESOURCE].find("_")
        ]
        resource_type = st.session_state[CONSTANTS.SELECTED_RESOURCE]
        if (
            provider in st.session_state[CONSTANTS.RESOURCE_CONF][CONSTANTS.RESOURCES]
            and resource_type
            in st.session_state[CONSTANTS.RESOURCE_CONF][CONSTANTS.RESOURCES][provider]
        ):
            for _ in st.session_state[CONSTANTS.RESOURCE_CONF][CONSTANTS.RESOURCES][
                provider
            ][resource_type]:
                with st.container(border=True):
                    st.subheader(_)
                    st.write(
                        st.session_state[CONSTANTS.RESOURCE_CONF][CONSTANTS.RESOURCES][
                            provider.lower()
                        ][resource_type.lower()][_]
                    )
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        edit_button = st.button(
                            "Edit",
                            use_container_width=True,
                            key=f"edit_{st.session_state[CONSTANTS.SELECTED_RESOURCE]}_{_}",
                        )
                        if edit_button:
                            MODULES[provider][resource_type][
                                CONSTANTS.UI_MODULE
                            ].OBJ.modify_resource(
                                name=_,
                                data=st.session_state[CONSTANTS.RESOURCE_CONF][
                                    CONSTANTS.RESOURCES
                                ][provider.lower()][resource_type.lower()][_],
                            )
                    with col2:
                        deletion_button = st.button(
                            "Delete",
                            use_container_width=True,
                            key=f"delete_{st.session_state[CONSTANTS.SELECTED_RESOURCE]}_{_}",
                        )
                        if deletion_button:
                            self.resource_deletion_prompt(_)

    @st.dialog("Delete Resource")
    def resource_deletion_prompt(self, resource_name: str) -> None:
        st.markdown(
            f"""
        ### Enter resource name below to delete the resource
        ( {resource_name} )
        """
        )
        prompt = st.text_input(
            "",
            "",
            key=f"deletion_prompt_{st.session_state[CONSTANTS.SELECTED_RESOURCE]}_{resource_name}",
        )
        delete_button = st.button(
            label="Delete",
            type="primary",
            use_container_width=True,
            key=f"deletion_submition_button_{st.session_state[CONSTANTS.SELECTED_RESOURCE]}_{resource_name}",
        )

        if prompt == resource_name and delete_button:
            provider = st.session_state[CONSTANTS.SELECTED_RESOURCE][
                : st.session_state[CONSTANTS.SELECTED_RESOURCE].find("_")
            ]
            resource_type = st.session_state[CONSTANTS.SELECTED_RESOURCE]

            MODULES[provider][resource_type][
                CONSTANTS.DELETION_MODULE
            ].OBJ.delete_resource(resource_name)

    def save_resource_conf(self) -> None:
        os.system(
            f"cp {os.path.join(CONSTANTS.PROJECTS_DIR, CONSTANTS.SELECTED_PROJECT, CONSTANTS.PROJ_CONF_DIR, CONSTANTS.RESOURCE_CONF_FILE)} {os.path.join(CONSTANTS.PROJECTS_DIR, CONSTANTS.SELECTED_PROJECT, CONSTANTS.PROJ_CONF_DIR, CONSTANTS.RESOURCE_CONF_FILE+CONSTANTS.BACKUP_FILE_EXTENSION)}"
        )
        with open(
            os.path.join(
                CONSTANTS.PROJECTS_DIR,
                st.session_state[CONSTANTS.SELECTED_PROJECT],
                CONSTANTS.PROJ_CONF_DIR,
                CONSTANTS.RESOURCE_CONF_FILE,
            ),
            "w",
        ) as resource_conf_file:

            json.dump(
                st.session_state[CONSTANTS.RESOURCE_CONF], resource_conf_file, indent=4
            )

    def save_tf_main_file(self) -> None:
        with open(
            os.path.join(
                CONSTANTS.PROJECTS_DIR,
                st.session_state[CONSTANTS.SELECTED_PROJECT],
                CONSTANTS.TF_MAIN_FILE,
            ),
            "w",
        ) as tf_main_file:
            complete_tf_conf = TF.conf_in_tf_syntax()
            tf_main_file.write(complete_tf_conf)

    def sidebar(self) -> None:
        with st.sidebar:
            for _ in MODULES:
                if (
                    _.lower()
                    in st.session_state[CONSTANTS.EXISTING_PROJECTS][
                        st.session_state[CONSTANTS.SELECTED_PROJECT]
                    ][CONSTANTS.CONF_EXISTING_PROJECTS][CONSTANTS.PROVIDERS]
                ):
                    st.write(_)
                    for __ in MODULES[_]:
                        resource_select_button = st.button(
                            f"{__.lower()}",
                            key=f"resource_selection{_}_{__}",
                            use_container_width=True,
                        )
                        if resource_select_button:
                            st.session_state[CONSTANTS.SELECTED_RESOURCE] = (
                                f"{__.lower()}"
                            )


# $$$$$$$$$$#

CONFIG()
