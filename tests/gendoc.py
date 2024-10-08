from zus.core.caching import GitCacher
from zus.core.gendoc import GenDoc
GitCacher().add("https://github.com/ZackaryW/zugen-resources.git")

GenDoc(
    workdir="tests/gendoc/txt",
    template="@txt_2024/template.md",
    data="@example-data/data.toml",
    start=True,
    moveFile=False
)

script = [
    "import os",
    "load()",
    'file("@awesome-cv/awesome-cv.cls")',
    "gen()",
    'os.rename("pandoc.out", f"output.{ext}")',
    'os.system("xelatex -interaction=nonstopmode output.tex")',
    "capture('output.pdf')",
]

GenDoc(
    workdir="tests/gendoc/tex",
    template="@awe2024tex/template.tex",
    data="@example-data/data.toml",
    start=True,
    moveFile=False,
    script=script
)
