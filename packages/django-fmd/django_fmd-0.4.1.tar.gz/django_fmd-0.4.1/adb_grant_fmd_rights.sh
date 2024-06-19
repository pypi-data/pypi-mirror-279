#!/bin/bash

# Script to grant extra permissions to FMD app via adb.
#
# Install "adb", e.g.:
#   ~$ sudo apt install adb
#
# * Connect Andorid device to PC.
# * run this script
# * grant permissions for this USB connection
#

# https://gitlab.com/Nulide/findmydevice/-/wikis/PERMISSION%20WRITE_SECURE_SETTINGS


set -ex

# Just list connected device:
adb devices

# Grant permissions:
adb shell pm grant de.nulide.findmydevice android.permission.WRITE_SECURE_SETTINGS
