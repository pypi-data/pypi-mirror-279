'''
Author: Devin
Date: 2024-06-19 11:16:09
LastEditors: Devin
LastEditTime: 2024-06-19 12:10:41
Description: 

Copyright (c) 2024 by Devin, All Rights Reserved. 
'''
from .cmaps import Cmaps
from .show_map_helper import show_cmaps
import sys
sys.modules[__name__] = Cmaps()
