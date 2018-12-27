import sys
import json

class ConfigImport:
    '''Class to load config and provide methods above it'''

    def __init__(self, filename = "config.json"):
        '''Constuctor'''
        with open(filename, "r") as ifp:
            self.Data = json.load(ifp)

    def Get(self, key):
        '''Get value in certain patterns'''
        return self.__get(self.Data, key.split('/'))

    def __get(self, obj, keys, index = 0):
        '''Helper method to get value from the key'''

        if index >= len(keys):
            raise "IndexOutOfRangeException"

        if keys[index] in obj:
            if (index == len(keys) - 1):
                return obj[keys[index]]

            return self.__get(obj[keys[index]], keys, index + 1)

        raise "KeyNotFoundException - %s" % "/".join(keys)