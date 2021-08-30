#!/bin/bash

# enable wireless if it is currently off
if [ 0 -eq `lipc-get-prop com.lab126.cmd wirelessEnable` ]; then
	eips 30 3 "WiFi is off, turning it on now"
	lipc-set-prop com.lab126.cmd wirelessEnable 1
	WIFI_IS_OFF=1
fi

. "$@"

# Restore WiFi status
if [ 1 -eq $WIFI_IS_OFF ]; then
	lipc-set-prop com.lab126.cmd wirelessEnable 0
	eips 30 3 "Disabling WiFi.               "
fi
/usr/bin/WebReaderViewer result.txt 
# Clear screen
sleep 1
eips 30 3 "                              "