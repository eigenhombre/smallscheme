from smallscheme.repl import repl
from smallscheme.main import main, run_file
from smallscheme.interop import register_fn
import smallscheme.dtypes

from . import _version
__version__ = _version.get_versions()['version']
