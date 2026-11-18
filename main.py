if __name__ == '__main__':
    from config import config
    from ok import OK

    from src.patches import import_warning  # noqa: F401  drop the 15s countdown on the import warning dialog

    config = config
    ok = OK(config)
    ok.start()
