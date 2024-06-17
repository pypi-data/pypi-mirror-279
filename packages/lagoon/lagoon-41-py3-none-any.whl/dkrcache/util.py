from contextlib import contextmanager
from lagoon.util import mapcm
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import tarfile

class ContextStream:

    @classmethod
    @contextmanager
    def open(cls, dockerstdin):
        with tarfile.open(mode = 'w:gz', fileobj = dockerstdin) as tar:
            yield cls(tar)

    def __init__(self, tar):
        self.tar = tar

    def put(self, name, path):
        self.tar.add(path, name)

    def putstream(self, name, stream):
        self.tar.addfile(self.tar.gettarinfo(arcname = name, fileobj = stream), stream)

    def mkdir(self, name):
        with TemporaryDirectory() as empty:
            self.put(name, empty)

@contextmanager
def iidfile():
    with mapcm(Path, TemporaryDirectory()) as tempdir:
        path = tempdir / 'iid'
        yield SimpleNamespace(args = ('--iidfile', path), read = path.read_text)
