import io
import os
import sys
import importlib
from importlib.machinery import ModuleSpec
from nbformat import read
from IPython.core.interactiveshell import InteractiveShell

__version__ = "0.2"


def find_notebook(fullname, path=None):
    """find a notebook, given its fully qualified name and an optional path

    This turns "foo.bar" into "foo/bar.ipynb"
    and tries turning "Foo_Bar" into "Foo Bar" if Foo_Bar
    does not exist.
    """
    name = fullname.rsplit(".", 1)[-1]
    if not path:
        path = [""]
    for d in path:
        nb_path = os.path.join(d, name + ".ipynb")
        if os.path.isfile(nb_path):
            return nb_path
        # let import Notebook_Name find "Notebook Name.ipynb"
        nb_path = nb_path.replace("_", " ")
        if os.path.isfile(nb_path):
            return nb_path


class NotebookLoader(object):
    """Module Loader for Jupyter Notebooks"""

    def __init__(self, path=None):
        self.shell = InteractiveShell.instance()
        self.path = path

    def create_module(self, spec):
        """import a notebook as a module"""
        path = find_notebook(spec.name, self.path)
        #        print("importing Jupyter notebook from %s" % path)
        mod = ModuleSpec(name=spec.name, loader=self, origin=path)
        return mod

    def exec_module(self, mod):
        # load the notebook object
        with io.open(mod.origin, "r", encoding="utf-8") as f:
            nb = read(f, 4)

        # extra work to ensure that magics that would affect the user_ns
        # actually affect the notebook module's ns
        save_user_ns = self.shell.user_ns
        self.shell.user_ns = mod.__dict__

        try:
            for cell in nb.cells:
                if cell.cell_type == "code":
                    # transform the input to executable Python
                    code = self.shell.input_transformer_manager.transform_cell(
                        cell.source
                    )
                    # run the code in themodule
                    exec(code, mod.__dict__)
        finally:
            self.shell.user_ns = save_user_ns


class NotebookFinder(object):
    """Module finder that locates Jupyter Notebooks"""

    def __init__(self):
        self.loaders = {}

    def find_spec(self, fullname, path=None, target=None):
        nb_path = find_notebook(fullname, path)
        if not nb_path:
            return
        return importlib.util.spec_from_loader(
            fullname, NotebookLoader(path), is_package=False
        )


sys.meta_path.append(NotebookFinder())
