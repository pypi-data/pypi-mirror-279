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
#  a simple singleton decorator
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
class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass in this example.
    """

    # Dictionary stores single instance of the class for
    # each subclass of the SingletonMeta metaclass
    _instances = {}

    def __call__(cls, *args, **kwargs):
        # Single instance of the class already been created?
        if cls not in cls._instances:
            # Create the instance by calling the call
            # method of the parent's (super () .. call ())
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
