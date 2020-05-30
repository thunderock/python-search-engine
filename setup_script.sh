#! /bin/bash
apt-get install python3-venv -y
python3 -m venv .

source ./bin/activate
./bin/pip install -r requirements.txt
./bin/python main.py