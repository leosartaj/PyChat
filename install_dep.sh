#!/usr/bin/env bash

##
# PyGp
# https://github.com/leosartaj/PyGp.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

# Installs dependencies
tar -zxpf dep/pyfiglet.tar.gz # untar
cd pyfiglet-master
./setup.py install # install
cd ..
rm -r pyfiglet-master # clean the directory
