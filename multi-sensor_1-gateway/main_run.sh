#! /bin/bash
source ~/venv/bin/activate
python logger_single.py &
python logger_single2.py &
python send_to_api.py
