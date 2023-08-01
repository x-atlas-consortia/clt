from atlas_consortia_clt.common import config, main


def entry():
    appcfg = config.read_cfg_file()
    cfg = config.Config(
        name="sennet-clt",
        consortium="SenNet",
        ingest_url=appcfg["SENNET_INGEST_URL"],
        entity_id="SNT123.ABCD.456",
        entity_id_name="sennet_id",
        docs_url="https://docs.sennetconsortium.org/libraries/clt",
    )
    main.launch_command(cfg)
