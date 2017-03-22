import yaml
import pathlib


def detect_config(file_path, trafaret, config_name='config.yaml'):

    dir_to_explore = pathlib.Path(file_path).parent
    conf_path = dir_to_explore / config_name

    with open(conf_path, 'rt') as file:
        config = yaml.load(file)
    trafaret.check(config)

    return config
