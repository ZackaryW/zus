
import os

from zuu.string import dump_meta

def resolve_template_type(string: str):
    if os.sep in string:
        extension = string.split(os.sep)[-1].split(".")[-1]
    else:
        extension = string.split(".")[-1]

    match extension:
        case "html":
            return "html"
        case "md":
            return "markdown"
        case "tex":
            return "latex"
        case "pdf":
            return "latex"
        case "docx":
            return "docx"
        case "odt":
            return "odt"
        case "rtf":
            return "rtf"
        case "txt":
            return "plain"
        case "html":
            return "html"
        case "epub":
            return "epub"
        case "epub3":
            return "epub3"
        case "odt":
            return "odt"
        case "docx":
            return "docx"
        case "pptx":
            return "pptx"
        case "ppt":
            return "ppt"
        case "odp":
            return "odp"
        case "ods":
            return "ods"


PANDOC_CMD = (
    'pandoc {input_md} -o {outname} -f markdown -t {outtype} --template="{template}"'
)

def gen_file(
    workdir: str, outtype: str, template: str, data: dict, outname: str = "pandoc.out"
):
    os.makedirs(workdir, exist_ok=True)

    dump_meta(os.path.join(workdir, "input.md"), data)

    os.system(
        PANDOC_CMD.format(
            input_md=os.path.join(workdir, "input.md"),
            outname=os.path.join(workdir, outname),
            outtype=outtype,
            template=template,
        )
    )
