#!/bin/bash
cd /root/Desktop/Deluge/youtor/deluge/scripts/search
mkdir temp
export PYTHONPATH=./temp
/usr/bin/python setup.py build develop --install-dir ./temp
cp ./temp/Search.egg-link /root/.config/deluge/plugins
rm -fr ./temp
