import requests


class ProgramContext:
    def __init__(self, *, cp_names, references):
        # TODO: should represent cp ownership of experiments
        self._cp_names = cp_names
        self._references = references

    @staticmethod
    def from_schema(*, cp_url, ref_url):
        # TODO: remove this once representing cp ownership of experiments
        r = requests.get(url=cp_url)
        cp_schema = r.json()
        r = requests.get(url=ref_url)
        ref_schema = r.json()
        return ProgramContext(
            cp_names=[name for name in cp_schema['enum']
                      if name != 'UNDEFINED'],
            references=[ref for ref in ref_schema['enum'] if ref != 'Unknown']
        )

    @property
    def cp_names(self):
        return self._cp_names

    @property
    def exp_references(self):
        # TODO: should be relative to cp
        return self._references
