from abc import ABC
import pickle


class AbstractDAO(ABC):
    def __init__(self, datasource=''):
        self.__datasource = datasource
        self.__cache = {}
        try:
            self.__load()
        except FileNotFoundError:
            self.__dump()

    #atualiza o arquivo
    def __dump(self):
        pickle.dump(self.__cache, open(self.__datasource, 'wb'))
    
    #carrega o arquivo no cache
    def __load(self):
        self.__cache = pickle.load(open(self.__datasource, 'rb'))

    #adiciona objeto no dicionário, atualiza o arquivo
    def add(self, objeto, key):
        self.__cache[key] = objeto
        self.__dump()

    # retorna o objeto associado à chave
    def get(self, key):
        try:
            return self.__cache[key]
        except KeyError:
            pass

    # remove o objeto do dicionario e atualiza o arquivo
    def remove(self, key):
        try:
            self.__cache.pop(key)
            self.__dump()
        except KeyError:
            return False

    def update(self, key, item):
        try:
            self.__cache[key] = item
            self.__dump()
        except KeyError:
            return False


    def get_all(self):
        return self.__cache.values()
    
