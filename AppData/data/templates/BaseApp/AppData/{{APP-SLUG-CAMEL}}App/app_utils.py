#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Summary

Attributes
----------
root_folder : str
    The main folder containing the Knowledge Base. All commands must be executed
    from this location without exceptions.
"""

import os


root_folder = os.path.realpath(os.path.abspath(os.path.join(
    os.path.normpath(os.getcwd()))))


if __name__ == "__main__":
    pass
