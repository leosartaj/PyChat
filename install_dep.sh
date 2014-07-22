#!/usr/bin/env sh

##
# PyGp
# https://github.com/leosartaj/PyGp.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

# Installs dependencies
unzip dep/pyfiglet-master.zip # unzip
cd pyfiglet-master
python2 setup.py install # install
cd ..
rm -r pyfiglet-master # clean the directory
