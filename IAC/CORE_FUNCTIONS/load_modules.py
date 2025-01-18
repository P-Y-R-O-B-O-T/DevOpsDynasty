import streamlit as st
import os

import CORE_FUNCTIONS.constants_n_conf as CONSTANTS
import importlib

# $$$$$$$$$$#


@st.cache_resource
def load_modules(modules_needed: list[str]) -> dict:
    modules = {}
    for _ in os.listdir(CONSTANTS.MODULES_DIR):
        modules[_.lower()] = {}
        for __ in os.listdir(os.path.join(CONSTANTS.MODULES_DIR, _)):
            if (
                os.path.isfile(
                    os.path.join(
                        CONSTANTS.MODULES_DIR,
                        _,
                        __,
                        CONSTANTS.UI_MODULE_DIRECTORY,
                        CONSTANTS.CREATE_MODIFY_MODULE_FILE,
                    )
                )
                and os.path.isfile(
                    os.path.join(
                        CONSTANTS.MODULES_DIR,
                        _,
                        __,
                        CONSTANTS.UTILITIES_MODULE_DIRECTORY,
                        CONSTANTS.DELETION_MODULE_FILE,
                    )
                )
                and os.path.isfile(
                    os.path.join(
                        CONSTANTS.MODULES_DIR,
                        _,
                        __,
                        CONSTANTS.UTILITIES_MODULE_DIRECTORY,
                        CONSTANTS.TEMPLATING_MODULE_FILE,
                    )
                )
            ):
                modules[_.lower()][__.lower()] = {}
                if CONSTANTS.UI_MODULE in modules_needed:
                    modules[_.lower()][__.lower()][CONSTANTS.UI_MODULE] = (
                        importlib.import_module(
                            f"{CONSTANTS.MODULES_DIR}.{_}.{__}.{CONSTANTS.UI_MODULE_DIRECTORY}.{CONSTANTS.CREATE_MODIFY_MODULE_FILE[:-3]}"
                        )
                    )
                if CONSTANTS.TEMPLATING_MODULE in modules_needed:
                    modules[_.lower()][__.lower()][CONSTANTS.TEMPLATING_MODULE] = (
                        importlib.import_module(
                            f"{CONSTANTS.MODULES_DIR}.{_}.{__}.{CONSTANTS.UTILITIES_MODULE_DIRECTORY}.{CONSTANTS.TEMPLATING_MODULE_FILE[:-3]}"
                        )
                    )
                if CONSTANTS.DELETION_MODULE in modules_needed:
                    modules[_.lower()][__.lower()][CONSTANTS.DELETION_MODULE] = (
                        importlib.import_module(
                            f"{CONSTANTS.MODULES_DIR}.{_}.{__}.{CONSTANTS.UTILITIES_MODULE_DIRECTORY}.{CONSTANTS.DELETION_MODULE_FILE[:-3]}"
                        )
                    )

    return modules
