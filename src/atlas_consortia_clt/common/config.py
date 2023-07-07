import os
import sys

from atlas_consortia_clt.common import help


class Config:
    def __init__(
        self,
        name: str,
        consortium: str,
        ingest_url: str,
        entity_id: str,
        entity_id_name: str,
        docs_url: str,
    ):
        self.name = name
        self.consortium = consortium
        self.ingest_url = ingest_url
        self.entity_id = entity_id
        self.entity_id_name = entity_id_name
        self.docs_url = docs_url

    @property
    def help_txt(self) -> str:
        return help.get_help(self)


def read_cfg_file() -> dict:
    config = {}
    try:
        filename = os.path.join(os.path.dirname(__file__), "app.cfg")
        with open(filename, mode="rb") as config_file:
            exec(compile(config_file.read(), filename, "exec"), config)
        return {k: v for k, v in config.items() if k in ["HUBMAP_INGEST_URL", "SENNET_INGEST_URL"]}
    except OSError as e:
        print("Error reading configuration file:", e)
        sys.exit(1)
