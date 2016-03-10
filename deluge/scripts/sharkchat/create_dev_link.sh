#!/bin/bash
cd /home/rlaw/Documents/cs179_kash/youtor/deluge/scripts/sharkchat
mkdir temp
export PYTHONPATH=./temp
/usr/bin/python setup.py build develop --install-dir ./temp
cp ./temp/SharkChat.egg-link /home/rlaw/.config/deluge/plugins
rm -fr ./temp
