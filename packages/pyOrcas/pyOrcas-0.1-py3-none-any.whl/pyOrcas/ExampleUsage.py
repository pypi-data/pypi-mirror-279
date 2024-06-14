# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 17:48:02 2024

@author: DAlexander
"""

from actuator import Actuator


orca = Actuator(port='COM36', baudrate=1250000)
print(orca)

try:
    while True:
        orca.force=20000

except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    orca.close()
    print("Serial port closed")
