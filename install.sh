#!/usr/bin/env sh

##
# PyGp
# https://github.com/leosartaj/PyGp.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

# The directory where the install.sh script is kept
SCRIPT_DIR=$(readlink -f ${0%/*})

# Whether root access is provided
ROOT_ACCESS=1

# UID of the user
USER_UID=$($SCRIPT_DIR/conf/uid.sh)

# If user = root, the root_access = true
if [ "$USER_UID" = "0" ]
then
    ROOT_ACCESS=0
fi

# If no root access, exit
if [ "$ROOT_ACCESS" != "0" ]
then
    echo 'Cannot install without root access'
    exit 1
fi

# Path to install
path=/usr/local/PyGp

if [ ! -d "$path" ]
then
    mkdir "$path" # Make directory if directory does not exist
fi

# Copying important directories
cp "system" "$path" -R
cp "PyGp_recv" "$path" -R
cp "PyGp_server" "$path" -R

# setting required permissions
chmod 646 "$path/PyGp_server/PyGp_log.txt" 
chmod 777 "$path/PyGp_recv" 

# Install files
install -m 0755 "$SCRIPT_DIR/PyGp.py" "/usr/bin/pygp" # Copy the PyGp
