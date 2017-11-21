#!/bin/bash

FILES=/home/pi/PDF/*.pdf

shopt -s nullglob

for f in $FILES
do	
	filename=$(basename "$f")
	filename="${filename%.*}"
	echo "Processing $filename..." > /home/pi/LOG/test_daemon.log
	convert -density 350 $f -depth 8 /home/pi/IMG/$filename.jpg
done
