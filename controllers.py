from data_sources import DataSource
from abc import ABC, abstractmethod


"""
A controller is an object that uses sensor data, a targeter and uses these to instruct actuators.
"""

class RemoteController:
    """
    A controller that works with a remote robot.
    This means that sensor data is 'data sources' rather than locally stored data.
    """

    
