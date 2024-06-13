from atlas_consortia_clt.common import config, main


def entry():
    appcfg = config.read_cfg_file()
    cfg = config.Config(
        name="hubmap-clt",
        consortium="HuBMAP",
        ingest_url=appcfg["HUBMAP_INGEST_URL"],
        entity_id="HBM744.FNLN.846",
        entity_id_name="hubmap_id",
        docs_url="https://docs.hubmapconsortium.org/clt",
    )
    main.launch_command(cfg)
