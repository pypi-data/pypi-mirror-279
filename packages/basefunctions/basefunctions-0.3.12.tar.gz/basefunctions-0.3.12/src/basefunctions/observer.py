"""
# =============================================================================
#
#  Licensed Materials, Property of Ralph Vogl, Munich
#
#  Project : basefunctions
#
#  Copyright (c) by Ralph Vogl
#
#  All rights reserved.
#
#  Description:
#
#  a simple observer pattern
#
# =============================================================================
"""

# -------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------

# -------------------------------------------------------------
#  FUNCTION DEFINITIONS
# -------------------------------------------------------------

# -------------------------------------------------------------
# DEFINITIONS REGISTRY
# -------------------------------------------------------------

# -------------------------------------------------------------
# DEFINITIONS
# -------------------------------------------------------------


# -------------------------------------------------------------
# VARIABLE DEFINTIONS
# -------------------------------------------------------------
class Observer:
    """
    The Observer interface declares the update method, used by subjects.
    """

    def update(self, message: any) -> None:
        """
        Receive update from subject.

        Parameters:
        -----------
        message : any
            The message sent by the subject to the Observers.
        """
        pass


class Subject:
    """
    The Subject interface declares a set of methods for managing subscribers.
    """

    def __init__(self) -> None:
        """
        Initialize the list of subscribers.
        """
        self._observers = []

    def attach(self, observer: Observer) -> None:
        """
        Attach an observer to the subject.

        Parameters:
        -----------
        observer : Observer
            The observer to attach to the subject.
        """
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """
        Detach an observer from the subject.

        Parameters:
        -----------
        observer : Observer
            The observer to detach from the subject.
        """
        self._observers.remove(observer)

    def notify(self, message: any) -> None:
        """
        Notify all observers about an event.

        Parameters:
        -----------
        message : any
            The message to send to the observers.
        """
        for observer in self._observers:
            observer.update(message)
