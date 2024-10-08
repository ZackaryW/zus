import re
import shutil
from zuu.io import read_toml
from ..app.pandoc import gen_file, resolve_template_type
from .caching import resolve_path
import os

class GenDoc:
    @classmethod
    def folder(cls, path : str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Folder {path} does not exist")
        
        if not os.path.isdir(path):
            raise NotADirectoryError(f"Path {path} is not a directory")

    DEFAULT_SCRIPT = [
        "import os",
        "load()", 
        "gen()",
        "if os.path.exists('pandoc.out'):",
        '    os.rename("pandoc.out", f"output.{ext}")',
        "capture(f'output.{ext}')",
    ]
    def __init__(
        self,
        workdir : str = None,
        script : str | list = None,
        data : str | dict = None,
        template : str = None,
        envdict : dict = None,
        start : bool = False,
        moveFile : bool = True
    ):
        self.workdir = workdir
        self.script = script
        self.data = data
        self.template = template
        self.envdict = envdict
        self.captureAll = False
        self.moveFile = moveFile

        if not self.workdir:
            self.workdir = os.path.join(os.getcwd(), "gendoc")
        
        self.workdir = os.path.abspath(self.workdir)

        if os.path.exists(self.workdir):
            shutil.rmtree(self.workdir)

        os.makedirs(self.workdir)

        if not self.script:
            self.script = self.DEFAULT_SCRIPT
        elif isinstance(self.script, str):
            resolved = resolve_path(self.script)
            with open(resolved, "r") as f:
                self.script = f.readlines()

        assert isinstance(self.script, list), "script must be a list of strings"

        if self.template:
            self.template = resolve_path(self.template)
        
        if self.data and isinstance(self.data, str):
            self.data = resolve_path(self.data)

        if start:
            self()

    def __call__(self):
        currcwd = os.getcwd()
        error = False
        os.chdir(self.workdir)
        try:
            self.__prep_script__()
            exec("\n".join(self.script), self.envdict)
        except Exception as e:
            error = True
            raise e
        finally:
            if self.moveFile:
                self.__move_files__(self.workdir, error)
            os.chdir(currcwd)
            

    def __move_files__(self, target, error: bool = False ):
        # loop through capture and exclusions
        if error:
            if os.path.exists(os.path.join(target, "debug")):
                shutil.rmtree(os.path.join(target, "debug"))
            shutil.copytree(self.workdir, os.path.join(target, "debug"))
            return
        
        hasCapture = len(self.envdict["captures"]) > 0
        hasExclusion = len(self.envdict["exclusions"]) > 0

        if not hasCapture and not hasExclusion:
            raise RuntimeError("No captures or exclusions found")

        for path in os.listdir():
            if hasCapture and re.search(self.envdict["captures"], path):
                shutil.copy(path, os.path.join(target, path))
            elif hasExclusion and not re.search(self.envdict["exclusions"], path):
                shutil.copy(path, os.path.join(target, path))

    def __prep_script__(self):

        if self.envdict is None:
            self.envdict = {}

        self.envdict["captures"] = []
        self.envdict["exclusions"] = []
        self.envdict["ctx"] = self

        def load():
            if not self.data:
                raise ValueError("data must be set")
            if isinstance(self.data, str):
                path = resolve_path(self.data)
                self.data = read_toml(path)

            self.template = resolve_path(self.template)
            assert os.path.exists(self.template), "template must exist"

            self.envdict["ext"] = os.path.splitext(self.template)[1][1:]
        
        def capture(string : str, exclude : bool = False):
            match string:
                case "*":
                    self.captureAll = True
                case str() if string.startswith("*"):
                    for fi in os.listdir():
                        if fi.endswith(string[1:]):
                            self.envdict["captures"].append(fi)
                case str() if string.endswith("*"):
                    for fi in os.listdir():
                        if fi.startswith(string[:-1]):
                            self.envdict["captures"].append(fi)
                case str() if os.path.exists(string):
                    self.envdict["captures"].append(string)
                case _:
                    raise RuntimeError()            

        def gen():
            gen_file(
                self.workdir,
                resolve_template_type(self.template),
                self.template,
                self.data
            )
        
        def file(path : str):
            path = resolve_path(path)
            shutil.copy(path, self.workdir)

        self.envdict["load"] = load
        self.envdict["gen"] = gen
        self.envdict["capture"] = capture
        self.envdict["file"] = file

    