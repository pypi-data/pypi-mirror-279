from tinydb import TinyDB, Storage, Query

# from . import util
import os
import warnings
from moyanlib import jsons
import io
from tqdm import tqdm
import zstandard
from typing import Dict, Any, Optional


class FastJSONStorage(Storage):
    def __init__(
        self,
        path: str,
        create_dirs=False,
        encoding=None,
        access_mode="rb+",
        write_threshold=1,
        **kwargs
    ):
        super().__init__()
        self.cctx = zstandard.ZstdCompressor()
        self.dctx = zstandard.ZstdDecompressor()
        self._mode = access_mode
        self.kwargs = kwargs
        self.write_threshold = write_threshold  # 指定写入阈值
        self.write_counter = 0
        if any(
            [character in self._mode for character in ("+", "w", "a")]
        ):  # any of the writing modes
            self.touch(path, create_dirs=create_dirs)
        self._handle = open(path, mode=self._mode, encoding=encoding)

    def close(self) -> None:
        self._handle.close()

    def touch(self, path: str, create_dirs: bool):
        if create_dirs:
            base_dir = os.path.dirname(path)

            if not os.path.exists(base_dir):
                os.makedirs(base_dir)

        with open(path, "a"):
            pass

    def read(self) -> Optional[Dict[str, Dict[str, Any]]]:
        self._handle.seek(0, os.SEEK_END)
        size = self._handle.tell()

        if not size:
            return None
        else:
            self._handle.seek(0)
            data = self.dctx.decompress(self._handle.read())
            return jsons.loads(data.decode())

    def write(self, data: Dict[str, Dict[str, Any]]):
        self.write_counter += 1
        if self.write_counter == self.write_threshold:
            self._handle.seek(0)

            serialized = jsons.dumps(data, **self.kwargs)
            serialized = self.cctx.compress(serialized.encode())

            try:
                self._handle.write(serialized)
            except io.UnsupportedOperation:
                raise IOError(
                    'Cannot write to the database. Access mode is "{0}"'.format(
                        self._mode
                    )
                )

            self._handle.flush()
            os.fsync(self._handle.fileno())

            self._handle.truncate()
            self.write_counter = 0


class Base:
    def __init__(self, name):
        self.rootdb = TinyDB(
            os.path.join(".", "DB.pcdb"), storage=FastJSONStorage, write_threshold=2
        )
        self.db = self.rootdb.table(name)

    def insert(self, data):
        self.db.insert(data)

    def remove(self, query):
        self.db.remove(query)


class PackageData(Base):
    def __init__(self):
        super(PackageData, self).__init__("PackageData")
        self.query = Query()

    def add(self, name, version, info=None):
        self.db.insert({"Name": name, "Version": version, "info": info})

    def get(self, name):
        return self.db.search(self.query.Name == name)[0]


db = PackageData()
for i in tqdm(range(1145)):
    db.add("json" + str(i), "v1" + str(i))

print(db.db.all())
