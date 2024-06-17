from collections import defaultdict
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import local
import os, re, sys

mangled = re.compile('_.*(__.*[^_]_?)')
PYTHONPATH = os.pathsep.join(sys.path[1:]) # XXX: Include first entry?

def unmangle(name):
    m = mangled.fullmatch(name)
    return name if m is None else m.group(1)

@contextmanager
def atomic(path):
    path.parent.mkdir(parents = True, exist_ok = True)
    with TemporaryDirectory(dir = path.parent) as d:
        q = Path(d, f"{path.name}.part")
        yield q
        q.rename(path) # XXX: Or replace?

class threadlocalproperty:

    def __init__(self, defaultfactory):
        self.local = local()
        self.defaultfactory = defaultfactory

    def _lookup(self):
        try:
            return self.local.lookup
        except AttributeError:
            self.local.lookup = lookup = defaultdict(self.defaultfactory)
            return lookup

    def __get__(self, obj, objtype):
        return self._lookup()[obj]

    def __set__(self, obj, value):
        self._lookup()[obj] = value

@contextmanager
def onerror(f):
    try:
        yield
    except:
        f()
        raise

@contextmanager
def mapcm(f, obj):
    with obj as cm:
        yield f(cm)

def stripansi(text):
    return re.sub('\x1b\\[[\x30-\x3f]*[\x20-\x2f]*[\x40-\x7e]', '', text) # XXX: Duplicated code?
