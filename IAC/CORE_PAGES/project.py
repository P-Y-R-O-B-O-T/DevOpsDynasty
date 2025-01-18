import streamlit as st
import os
import json
import datetime
import importlib

import streamlit as st
import os
import json
import datetime
import importlib

import CORE_FUNCTIONS.toasts as TOAST
import CORE_FUNCTIONS.constants_n_conf as CONSTANTS
import CORE_FUNCTIONS.input_validation as IV
import CORE_FUNCTIONS.upload_download as UD

#$$$$$$$$$$#

class PROJECT :
    def __init__(self) -> None :
        self.heading_details()
        self.load_modules_versions()
        self.create_upload_download_opts()
        self.list_projects()
        self.show_toasts()

    def heading_details(self) -> None :
        markdown = f"""
        # **Choose a Project**
        **Currently Using : {st.session_state[CONSTANTS.SELECTED_PROJECT] if CONSTANTS.SELECTED_PROJECT in st.session_state else None}**
        """
        st.markdown(markdown)

    def create_upload_download_opts(self) -> None :
        col1, col2, col3 = st.columns([1]*3)
        with col1 :
            project_creation = st.button(label="📝 **Create Project**",
                                         type="primary",
                                         use_container_width=True,
                                         key=f"project_creation_button")
            if project_creation :
                self.create_project()
        with col2 :
            project_upload = st.button(label="📤 **Upload Project**",
                                       type="primary",
                                       use_container_width=True,
                                       key=f"project_upload_button")
            if project_upload :
                self.upload_project()

        with col3 :
            project_download = st.button(label="📥 **Download Project**",
                                         type="primary",
                                         use_container_width=True,
                                         key=f"project_download_button")
            if project_download :
                self.download_project()

    def show_toasts(self) -> None :
        TOAST.display_toasts()

    def load_modules_versions(self) -> None :
        if CONSTANTS.MODULES_VERSIONS in st.session_state :
            return
        module_versions = {}
        for _ in os.listdir(os.path.join(CONSTANTS.MODULES_DIR)) :
            m = importlib.import_module(f"{CONSTANTS.MODULES_DIR}.{_}.{CONSTANTS.VERSIONS_MODULE_FILE[:-3]}")
            module_versions[_.lower()] = m.VERSIONS
        st.session_state[CONSTANTS.MODULES_VERSIONS] = module_versions


    def list_projects(self) :
        if not os.path.exists(CONSTANTS.PROJECTS_DIR) :
            os.mkdir(CONSTANTS.PROJECTS_DIR)
        dirs = os.listdir(CONSTANTS.PROJECTS_DIR)
        st.session_state[CONSTANTS.EXISTING_PROJECTS] = {}
        for _ in dirs :
            if not (CONSTANTS.PROJ_CONF_DIR in os.listdir(os.path.join(CONSTANTS.PROJECTS_DIR, _)) and
                    CONSTANTS.CONF_FILE in os.listdir(os.path.join(CONSTANTS.PROJECTS_DIR, _, CONSTANTS.PROJ_CONF_DIR)) and
                    CONSTANTS.RESOURCE_CONF_FILE in os.listdir(os.path.join(CONSTANTS.PROJECTS_DIR, _, CONSTANTS.PROJ_CONF_DIR))) :
                continue
            if _ in st.session_state[CONSTANTS.EXISTING_PROJECTS] :
                continue
            with open(os.path.join(CONSTANTS.PROJECTS_DIR,
                                   _,
                                   CONSTANTS.PROJ_CONF_DIR,
                                   CONSTANTS.CONF_FILE), "r") as conf_file :
                st.session_state[CONSTANTS.EXISTING_PROJECTS][_] = {CONSTANTS.CONF_EXISTING_PROJECTS: json.load(conf_file)}

        cols = st.columns([1]*3)
        count = 0
        for _ in sorted(list(st.session_state[CONSTANTS.EXISTING_PROJECTS].keys())) :
            with cols[count%len(cols)] :
                with st.container(border=True) :
                    st.markdown(f"### {_}")
                    st.write(st.session_state[CONSTANTS.EXISTING_PROJECTS][_][CONSTANTS.CONF_EXISTING_PROJECTS])
                    col1, col2 = st.columns([1]*2)
                    with col1 :
                        select_button = st.button(label="✅ **Select**",
                                                  type="secondary",
                                                  use_container_width=True,
                                                  key=f"project_select_{_}")
                        if select_button :
                            st.session_state[CONSTANTS.SELECTED_PROJECT] = _
                            with open(os.path.join(CONSTANTS.PROJECTS_DIR, _, CONSTANTS.PROJ_CONF_DIR, CONSTANTS.RESOURCE_CONF_FILE), "r") as resource_conf_file :
                                st.session_state[CONSTANTS.RESOURCE_CONF] = json.load(resource_conf_file)
                            st.session_state[CONSTANTS.SELECTED_RESOURCE] = None
                            st.rerun()
                    with col2 :
                        delete_button = st.button(label="❌ **Delete**",
                                                  type="secondary",
                                                  use_container_width=True,
                                                  key=f"project_delete_{_}")
                        if delete_button :
                            self.delete_prompt(_)
            count += 1

    @st.dialog("Confirm Project Deletion")
    def delete_prompt(self,
                      project: str) -> None :
        st.markdown(f"""
        ### Enter project name below to delete the project 
        ( {project} )
        """)

        prompt = st.text_input("", "",
                               key=f"project_delete_prompt_{project}")
        
        delete_button = st.button(label="Delete",
                                  type="primary",
                                  use_container_width=True,
                                  key=f"project_delete_prompt_button_{project}")
        
        if prompt == project and delete_button :
            try :
                os.system(f"rm {os.path.join(CONSTANTS.PROJECTS_DIR,
                                             project)} -r")

                if CONSTANTS.SELECTED_PROJECT in st.session_state :
                    del st.session_state[CONSTANTS.SELECTED_PROJECT]
                
                del st.session_state[CONSTANTS.EXISTING_PROJECTS][project]

                TOAST.create_toast(f"Project {project} deleted", "🌟")

            except :
                TOAST.create_toast(f"Project {project} can't be deleted", "🌟")
            st.rerun()

    @st.dialog("Create Project")
    def create_project(self) -> None :
        project_name = st.text_input("Project Name", max_chars=20, key=f"create_project_projectname")
        if not IV.a_zA_z0_9(project_name) :
            st.write("⚠️ :red[Project name can only have [A-Za-z0-9]]")

        st.write("### Select providers and versions")

        select_boxes_providers = {}

        for _ in st.session_state[CONSTANTS.MODULES_VERSIONS] :
            select_boxes_providers[_] = st.selectbox(_.upper(),
                                                     tuple(st.session_state[CONSTANTS.MODULES_VERSIONS][_]),
                                                     index=None,
                                                     key=f"selectbox_project_creation_{_}")


        submit_button = st.button("Submit")

        if submit_button and project_name :
            providers = {_:select_boxes_providers[_] for _ in select_boxes_providers if select_boxes_providers[_] is not None}

            if project_name in st.session_state[CONSTANTS.EXISTING_PROJECTS] :
                TOAST.create_toast(f"Project {project_name} Already Exists", "⛔")
                st.rerun()

            if not IV.a_zA_z0_9(project_name) :
                TOAST.create_toast("Project name can only have [A-Za-z0-9]", "⚠️")
                st.rerun()

            os.mkdir(os.path.join(CONSTANTS.PROJECTS_DIR,
                                  project_name))
            os.mkdir(os.path.join(CONSTANTS.PROJECTS_DIR,
                                  project_name,
                                  CONSTANTS.PROJ_CONF_DIR))

            project_conf_base_format = {
                                        CONSTANTS.CREATION_DATE: str(datetime.datetime.now()),
                                        CONSTANTS.PROVIDERS: providers
                                        }

            with open(os.path.join(CONSTANTS.PROJECTS_DIR,
                                   project_name,
                                   CONSTANTS.PROJ_CONF_DIR,
                                   CONSTANTS.CONF_FILE), "w") as provider_conf_file :
                json.dump(project_conf_base_format,
                          provider_conf_file,
                          indent=4)
            with open(os.path.join(CONSTANTS.PROJECTS_DIR,
                                   project_name,
                                   CONSTANTS.PROJ_CONF_DIR,
                                   CONSTANTS.RESOURCE_CONF_FILE), "w") as resource_conf_file :
                json.dump({CONSTANTS.RESOURCES: {}}, resource_conf_file, indent=4)

            st.session_state[CONSTANTS.EXISTING_PROJECTS][project_name] = {CONSTANTS.CONF_EXISTING_PROJECTS: project_conf_base_format}

            TOAST.create_toast(f"Created Project {project_name}", "🌟")
            st.rerun()

    @st.dialog("Download Project")
    def download_project(self) -> None :
        if CONSTANTS.SELECTED_PROJECT not in st.session_state :
            st.write("Select a project first")
        else :
            if os.path.exists(os.path.join(CONSTANTS.DOWNLOAD_DIR, f"{st.session_state[CONSTANTS.SELECTED_PROJECT]}.{CONSTANTS.COMPRESSION_FORMAT}")) :
                os.system(f"rm {os.path.join(CONSTANTS.DOWNLOAD_DIR, st.session_state[CONSTANTS.SELECTED_PROJECT])}.{CONSTANTS.COMPRESSION_FORMAT}")
            generete_file = st.button("Generete File", use_container_width=True, key=f"generate_download_file_{st.session_state[CONSTANTS.SELECTED_PROJECT]}")
            if generete_file :
                UD.gen_zip_file()
            if os.path.exists(os.path.join(CONSTANTS.DOWNLOAD_DIR, f"{st.session_state[CONSTANTS.SELECTED_PROJECT]}.{CONSTANTS.COMPRESSION_FORMAT}")) :
                with open(os.path.join(CONSTANTS.DOWNLOAD_DIR, f"{st.session_state[CONSTANTS.SELECTED_PROJECT]}.{CONSTANTS.COMPRESSION_FORMAT}"), "rb") as download_file :
                    download_button = st.download_button(label="Download",
                                                         data=download_file,
                                                         file_name=f"{st.session_state[CONSTANTS.SELECTED_PROJECT]}.{CONSTANTS.COMPRESSION_FORMAT}",
                                                         mime="application/octet-stream",
                                                         type="primary",
                                                         use_container_width=True,
                                                         key=f"download_link_{st.session_state[CONSTANTS.SELECTED_PROJECT]}")

    @st.dialog("Upload Project")
    def upload_project(self) -> None :
        if not os.path.exists(CONSTANTS.UPLOAD_DIR) :
            os.mkdir(CONSTANTS.UPLOAD_DIR)

        file_upload = st.file_uploader(f"Upload a project file (.{CONSTANTS.COMPRESSION_FORMAT})",
                                       accept_multiple_files=False,
                                       key=f"project_file_upload")
        if file_upload is not None :
            st.write(file_upload.size)

            if file_upload.name[-7:] != f".{CONSTANTS.COMPRESSION_FORMAT}" :
                TOAST.create_toast(f"Upload a tar file with xz compression only (.{CONSTANTS.COMPRESSION_FORMAT})", "⚠️")
                st.rerun()

            if not IV.a_zA_z0_9(file_upload.name[:-7]) :
                TOAST.create_toast("Project name can have only A-Za-z0-9", "⚠️")
                st.rerun()

            if file_upload.name[:-7] in st.session_state[CONSTANTS.EXISTING_PROJECTS] :
                TOAST.create_toast("A project with same name already exists", "📍")
                st.rerun()

            try :
                with open(os.path.join(CONSTANTS.UPLOAD_DIR,
                                       file_upload.name), "wb") as upload_file :
                    upload_file.write(file_upload.read())
                TOAST.create_toast("File uploaded successfully", "🌟")
            except :
                TOAST.create_toast("Error while uploading file", "❗")
                st.rerun()

            try :
                os.system(f"tar --extract --file {os.path.join(CONSTANTS.UPLOAD_DIR,
                                                               file_upload.name)} -C {CONSTANTS.UPLOAD_DIR}")
                os.system(f"rm {os.path.join(CONSTANTS.UPLOAD_DIR,
                                             file_upload.name)}")
            except :
                TOAST.create_toast("Error while saving files", "💾")
                os.system(f"rm {os.path.join(CONSTANTS.UPLOAD_DIR,
                                             file_upload.name[:-7])} -r")
                os.system(f"rm {os.path.join(CONSTANTS.UPLOAD_DIR,
                                             file_upload.name)}")
                st.rerun()

            if not UD.extensive_project_structure_check(file_upload) :
                TOAST.create_toast("Project structure not compatible", "🚫")
                os.system(f"rm {os.path.join(CONSTANTS.UPLOAD_DIR,
                                             file_upload.name[:-7])} -r")
                st.rerun()

            os.system(f"mv {os.path.join(CONSTANTS.UPLOAD_DIR,
                                         file_upload.name[:-7])} {os.path.join(CONSTANTS.PROJECTS_DIR,
                                                                               file_upload.name[:-7])}")
            TOAST.create_toast("Project uploaded successfully", "✅")
            st.rerun()

#$$$$$$$$$$#

PROJECT()
