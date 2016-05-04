# coding:utf-8
import configparser


class ConfigClass(object):
    """config class"""
    __CONFIGS = None

    @classmethod
    def init_conf(cls):
        cls.__CONFIGS = configparser.ConfigParser()
        cls.__CONFIGS.sections()
        cls.__CONFIGS.read('config.ini')

    @classmethod
    def get_conf(cls, key1, key2):
        # if not cls.__CONFIGS.get(key1):
        #    cls.init_conf()

        return cls.__CONFIGS[key1][key2]

    @classmethod
    def get_parent_conf(cls, key):
        return cls.__CONFIGS[key]
