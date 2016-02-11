#!/bin/bash

python ./setup.py clean -a
python ./setup.py build
python ./setup.py install
python ./setup.py install_data
python ./setup.py clean -a
