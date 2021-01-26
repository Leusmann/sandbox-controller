import abc, six

@six.add_metaclass(abc.ABCMeta)
class ICommunication():
    """
    Interface for a Connection to an arbeitary Sandbox Instance

    Gets the data from outside sources so they can be reused. It should also convert the data to a usesable format
    """

    @abc.abstractmethod
    def send(self,list):
        """
        Sends an spawn Message to the Sandbox
        :param list: List of Objects to spawn
        :return: bsuccess
        """
        raise NotImplemented
