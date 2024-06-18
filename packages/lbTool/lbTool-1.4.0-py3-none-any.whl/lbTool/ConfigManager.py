import os.path

import yaml


class ConfigManager:
    """
    配置管理类
    """
    yaml_file = os.path.normpath(os.path.join(os.getcwd(), "config/config.yml"))

    @staticmethod
    def get_value(config_name, default_value=""):
        """
        获取配置值
        :param config_name: 配置名称
        :param default_value: 默认值
        :return:
        """
        try:
            with open(ConfigManager.yaml_file, 'r', encoding='utf-8') as file:
                config_data = yaml.load(file.read(), Loader=yaml.FullLoader)

                # 将配置名称按点拆分成多个部分
                keys = config_name.split('.')

                # 逐级访问嵌套的键
                value = config_data
                for key in keys:
                    value = value.get(key, None)
                    if value is None:
                        break

                return value if value is not None else default_value
        except (FileNotFoundError, KeyError):
            return default_value
