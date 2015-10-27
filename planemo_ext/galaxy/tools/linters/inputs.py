from ..lint_util import is_datasource


def lint_inputs(tool_xml, lint_ctx):
    datasource = is_datasource(tool_xml)
    inputs = tool_xml.findall("./inputs//param")
    num_inputs = 0
    for param in inputs:
        num_inputs += 1
        param_attrib = param.attrib
        has_errors = False
        if "type" not in param_attrib:
            lint_ctx.error("Found param input with no type specified.")
            has_errors = True
        if "name" not in param_attrib and "argument" not in param_attrib:
            lint_ctx.error("Found param input with no name specified.")
            has_errors = True

        if has_errors:
            continue

        param_type = param_attrib["type"]
        param_name = param_attrib.get("name", param_attrib.get("argument"))
        if param_type == "data":
            if "format" not in param_attrib:
                lint_ctx.warn("Param input [%s] with no format specified - 'data' format will be assumed.", param_name)
        # TODO: Validate type, much more...

    if datasource:
        for datasource_tag in ('display', 'uihints'):
            if not any([param.tag == datasource_tag for param in inputs]):
                lint_ctx.info("%s tag usually present in data sources" % datasource_tag)

    if num_inputs:
        lint_ctx.info("Found %d input parameters.", num_inputs)
    else:
        if datasource:
            lint_ctx.info("No input parameters, OK for data sources")
        else:
            lint_ctx.warn("Found no input parameters.")


def lint_repeats(tool_xml, lint_ctx):
    repeats = tool_xml.findall("./inputs//repeat")
    for repeat in repeats:
        if "name" not in repeat.attrib:
            lint_ctx.error("Repeat does not specify name attribute.")
        if "title" not in repeat.attrib:
            lint_ctx.error("Repeat does not specify title attribute.")
