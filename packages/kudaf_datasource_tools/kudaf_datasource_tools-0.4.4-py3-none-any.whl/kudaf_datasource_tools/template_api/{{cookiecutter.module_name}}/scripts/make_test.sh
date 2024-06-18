#!/bin/bash
set -e
set -x

apt-get update && apt-get upgrade -y
apt-get install python3-dev libpq-dev gcc -y
pip3 install --upgrade pip setuptools wheel
pip3 install --no-cache-dir --upgrade -r requirements.txt