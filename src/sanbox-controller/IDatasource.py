import abc, six

@six.add_metaclass(abc.ABCMeta)
class IDatasource():
    """
    Interface Classe for available Datasources
    """

    @abc.abstractmethod
    def getStore(self, storeId):
        """
        Returns a List of spawnable Objects
        :param storeId: Id of the store to spawn
        :return: List
        """
        raise NotImplemented

    @abc.abstractmethod
    def getAllShelves(self, storeId):
        """
        Returns a List of spawnable Shelf Objects
        :param storeId: Id of the store from which the shelves data should come
        :return: List
        """
        raise NotImplemented

    @abc.abstractmethod
    def getAllItems(self, storeId):
        """
        Returns a List of spawnable Items Objects
        :param storeId: Id of the store from which the Items data should come
        :return: List
        """
        raise NotImplemented
