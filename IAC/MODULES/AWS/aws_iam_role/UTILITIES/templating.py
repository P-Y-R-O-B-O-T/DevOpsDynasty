import jinja2
import streamlit as st
import CORE_FUNCTIONS.constants_n_conf as CONSTANTS

# $$$$$$$$$$#

MODULE_NAME = "AWS"
RESOURCE_NAME = "aws_iam_role"

AWS_IAM_ROLE_POLICY_ATTACHMENT = "aws_iam_role_policy_attachment"
AWS_IAM_POLICY = "aws_iam_policy"

class MODULE:
    def __init__(self) -> None:
        self.MAP_VERSIONS_METHODS_TEMPLATE = {"5.81.0": self.template_5_81_0}

    def template(self) -> str:
        return self.MAP_VERSIONS_METHODS_TEMPLATE[
            st.session_state[CONSTANTS.EXISTING_PROJECTS][
                st.session_state[CONSTANTS.SELECTED_PROJECT]
            ][CONSTANTS.CONF_EXISTING_PROJECTS][CONSTANTS.PROVIDERS][
                MODULE_NAME.lower()
            ]
        ]()

    def template_5_81_0(self) -> str:
        env = jinja2.Environment()
        template = env.from_string(
            """
#  █████╗ ██╗    ██╗███████╗        ██╗ █████╗ ███╗   ███╗        ██████╗  ██████╗ ██╗     ███████╗
# ██╔══██╗██║    ██║██╔════╝        ██║██╔══██╗████╗ ████║        ██╔══██╗██╔═══██╗██║     ██╔════╝
# ███████║██║ █╗ ██║███████╗        ██║███████║██╔████╔██║        ██████╔╝██║   ██║██║     █████╗
# ██╔══██║██║███╗██║╚════██║        ██║██╔══██║██║╚██╔╝██║        ██╔══██╗██║   ██║██║     ██╔══╝
# ██║  ██║╚███╔███╔╝███████║███████╗██║██║  ██║██║ ╚═╝ ██║███████╗██║  ██║╚██████╔╝███████╗███████╗
# ╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝
# {{ resource_name }}
{% for _ in resources %}
resource "{{ resource_name }}" "{{ _ }}" {
  name = "{{ _ }}"
  assume_role_policy = jsonencode(
  {{ resources[_]["policy"] }}
  )
}
{% for __ in resources[_]["aws_iam_policy"] %}
resource "aws_iam_role_policy_attachment" "{{ _ }}_{{ __ }}" {
  role = {{ resource_name }}.{{ _ }}.name
  policy_arn = aws_iam_policy.{{ __ }}.arn
}
{% endfor %}
{% endfor %}
"""
        )
        return template.render(
            resources=st.session_state[CONSTANTS.RESOURCE_CONF][CONSTANTS.RESOURCES][
                MODULE_NAME.lower()
            ][RESOURCE_NAME],
            resource_name=RESOURCE_NAME,
        )


# $$$$$$$$$$#

OBJ = MODULE()
