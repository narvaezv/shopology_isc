#!/bin/bash

FILES=/home/pi/IMG/*.jpg

shopt -s nullglob

for f in $FILES
do
	filename=$(basename "$f")
	filename="${filename%.*}"
	DIR=$(dirname "$f")
	echo "Processing $filename..." > /home/pi/LOG/txt_daemon.log
	tesseract $DIR/$filename.jpg /home/pi/TXT/$filename
done
