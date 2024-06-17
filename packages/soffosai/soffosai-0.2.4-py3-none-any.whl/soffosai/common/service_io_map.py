'''
Copyright (c)2022 - Soffos.ai - All rights reserved
Created at: 2023-04-21
Purpose: get all service IO definitions
-----------------------------------------------------
'''
import sys
import inspect
from .serviceio_fields import *

attrs = dir()
classes = [getattr(sys.modules[__name__], name) for name in attrs if inspect.isclass(getattr(sys.modules[__name__], name))]

SERVICE_IO_MAP = {obj.service: obj for obj in classes}
