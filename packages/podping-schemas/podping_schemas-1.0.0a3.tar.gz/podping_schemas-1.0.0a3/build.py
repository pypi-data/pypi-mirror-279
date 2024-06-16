import glob

from capnpy.compiler.distutils import capnpy_schemas

from generate_python_json_class import json_schemas


class SetupKwargsProxy:
    def __init__(self, d):
        self._d = d

    @property
    def capnpy_options(self):
        return {
            # do NOT convert camelCase to camel_case
            "convert_case": False,
            "include_reflection_data": True,
            'pyx': 'auto',
            # prevents us from having to call .decode("UTF-8") on strings
            # https://capnpy.readthedocs.io/en/latest/usage.html#text
            "text_type": "unicode",
            "version_check": False
        }

    @property
    def ext_modules(self):
        try:
            return self._d["ext_modules"]
        except KeyError:
            return None

    @ext_modules.setter
    def ext_modules(self, v):
        self._d["ext_modules"] = v


capnpy_schema_files = [
    p for p in
    glob.glob("podping_schemas/**/*.capnp", recursive=True)
    if not p.endswith("rust.capnp")
]
json_schema_files = glob.glob("podping_schemas/**/*.json", recursive=True)


def build(setup_kwargs):
    capnpy_schemas(SetupKwargsProxy(setup_kwargs), "capnpy_schemas", capnpy_schema_files)
    json_schemas(json_schema_files)
