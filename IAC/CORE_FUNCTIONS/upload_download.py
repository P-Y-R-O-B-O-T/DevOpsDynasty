import CORE_FUNCTIONS.constants_n_conf as CONSTANTS
import streamlit as st
import os


def extensive_project_structure_check(file_upload) -> bool :
    if not (os.path.exists(os.path.join(CONSTANTS.UPLOAD_DIR, file_upload.name[:-7], CONSTANTS.PROJ_CONF_DIR)) and
            os.path.isfile(os.path.join(CONSTANTS.UPLOAD_DIR, file_upload.name[:-7], CONSTANTS.PROJ_CONF_DIR, CONSTANTS.CONF_FILE)) and
            os.path.isfile(os.path.join(CONSTANTS.UPLOAD_DIR, file_upload.name[:-7], CONSTANTS.PROJ_CONF_DIR, CONSTANTS.RESOURCE_CONF_FILE))) :
        return False
    return True

def gen_zip_file() -> None :
    if not os.path.exists(CONSTANTS.DOWNLOAD_DIR) : os.mkdir(CONSTANTS.DOWNLOAD_DIR)
    if os.path.exists(os.path.join(CONSTANTS.DOWNLOAD_DIR, f"{st.session_state[CONSTANTS.SELECTED_PROJECT]}.tar.xz")) :
        os.system(f"rm {os.path.join(CONSTANTS.DOWNLOAD_DIR, st.session_state[CONSTANTS.SELECTED_PROJECT])}.tar.xz")
    os.system(f"tar --create --xz --file {os.path.join(CONSTANTS.DOWNLOAD_DIR, st.session_state[CONSTANTS.SELECTED_PROJECT])}.tar.xz -C {CONSTANTS.PROJECTS_DIR} {st.session_state[CONSTANTS.SELECTED_PROJECT]}")
