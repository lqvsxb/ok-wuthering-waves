if __name__ == '__main__':
    from config import config
    from ok import OK

    from src.patches import import_warning  # noqa: F401  drop the 15s countdown on the import warning dialog

    config = config
    config['debug'] = True
    # config['click_screenshots_folder'] = "click_screenshots"  # debug用 点击后截图文件夹]
    ok = OK(config)
    ok.start()
