import os
from .MoreTypes.HelperFiles.MorePyOverloading import overload

@overload
def execute(command: str):
    os.system(command)

@overload
def execute(*commands: str):
    for command in commands:
        os.system(command)