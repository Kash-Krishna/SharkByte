#!/bin/bash
cd /root/Desktop/Deluge/youtor/deluge/scripts/autoforward
mkdir temp
export PYTHONPATH=./temp
/usr/bin/python setup.py build develop --install-dir ./temp
cp ./temp/autoforward.egg-link /root/.config/deluge/plugins
rm -fr ./temp
