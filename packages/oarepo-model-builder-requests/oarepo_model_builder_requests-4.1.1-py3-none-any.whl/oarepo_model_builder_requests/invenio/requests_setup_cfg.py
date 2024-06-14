from oarepo_model_builder.builders import OutputBuilder
from oarepo_model_builder.outputs.cfg import CFGOutput
from oarepo_model_builder.utils.python_name import split_package_base_name


class RequestsSetupCfgBuilder(OutputBuilder):
    TYPE = "requests_setup_cfg"

    def finish(self):
        super().finish()

        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")

        output.add_dependency("oarepo-requests", ">=1.0.2")
