#!/bin/bash

for f in /home/pi/PDF/*.pdf
do
	sudo rm $f
done

for f in /home/pi/IMG/*.jpg
do
	sudo rm $f
done

for f in /home/pi/TXT/*.txt
do
	sudo rm $f
done
