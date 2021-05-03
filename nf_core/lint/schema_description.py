#!/usr/bin/env python

from logging import warn
import nf_core.schema


def schema_description(self):
    """Check that every parameter in the schema has a description

    The ``nextflow_schema.json`` pipeline schema should describe every flat parameter
    Furthermore warns about parameters outside of groups

    * Warning: Parameters in ``nextflow_schema.json`` without a description
    * Warning: Parameters in ``nextflow_schema.json`` that are defined outside of a group
    """
    passed = []
    warned = []
    failed = []

    # First, get the top-level config options for the pipeline
    # Schema object already created in the `schema_lint` test
    self.schema_obj = nf_core.schema.PipelineSchema()
    self.schema_obj.get_schema_path(self.wf_path)
    self.schema_obj.get_wf_params()
    self.schema_obj.no_prompts = True
    self.schema_obj.load_lint_schema()

    # Get ungrouped params
    if "properties" in self.schema_obj.schema.keys():
        ungrouped_params = self.schema_obj.schema["properties"].keys()
        for up in ungrouped_params:
            warned.append(f"Ungrouped param in schema {up}")

    # Iterate over groups and add warning for parameters without a description
    for group_key in self.schema_obj.schema["definitions"].keys():
        group = self.schema_obj.schema["definitions"][group_key]
        for param_key in group["properties"].keys():
            param = group["properties"][param_key]
            if not "description" in param.keys():
                warned.append(f"No description provided in schema for parameter '{param_key}'")

    return {"passed": passed, "warned": warned, "failed": failed}
