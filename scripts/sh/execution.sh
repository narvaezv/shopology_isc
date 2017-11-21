#!/bin/bash

sudo bash /home/pi/bin/pdftojpg.sh
sudo bash /home/pi/bin/jpgtotxt.sh 
sudo python /home/pi/bin/extract_info.py
