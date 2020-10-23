from json import load


"""
The Dactinote server module.
Should be configured with a port for websocket communication.
Other data sources should be registered to the server.
"""
class Server:
    def __init__(self, config_path):
        with open(config_path, "r") as fp:
            self.conf = load(fp)
            self.data_sources = []
        pass

    def register_data_source(self):

        pass

    def register_controller(self, controller):

        pass

    def start(self):
        """
        Launches the server with the given configurations.
        """
    pass

"""
The Dactinote Client system.
Loads a configuration file containing:
    server websocket address
    a list of servos (just servos for now)
"""
class Client:
    
    pass