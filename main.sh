#!/bin/sh

#show status
while :; do
    eips 30 1 "Fetching.            "
    sleep 1
    eips 30 1 "Fetching..           "
    sleep 1
    eips 30 1 "Fetching...          "
    sleep 1
done > /dev/null &

# enable wireless if it is currently off
WIFI_IS_OFF=0
if [ 0 -eq `lipc-get-prop com.lab126.cmd wirelessEnable` ]; then
	eips 30 3 "WiFi is off, turning it on now" > /dev/null
	lipc-set-prop com.lab126.cmd wirelessEnable 1
	WIFI_IS_OFF=1
	
	# wait for network to be up
    TEST_DOMAIN="www.baidu.com"
    TIMER=30     # number of seconds to attempt a connection
    CONNECTED=0                  # whether we are currently connected
    while [ 0 -eq $CONNECTED ]; do
    	# test whether we can ping outside
    	/bin/ping -c 1 -w 2 $TEST_DOMAIN > /dev/null && CONNECTED=1
    	# if we can't, checkout timeout or sleep for 1s
    	if [ 0 -eq $CONNECTED ]; then
    		TIMER=$(($TIMER-1))
    		if [ 0 -eq $TIMER ]; then
    			logger "No internet connection after ${NETWORK_TIMEOUT} seconds, aborting."
    			break
    		else
    			sleep 1
    		fi
    	fi
    done
    if [ 1 -eq $CONNECTED ]; then
        eips 30 3 "WiFi is on now                " > /dev/null
    else
        eips 30 3 "No internet connection        " > /dev/null
    fi
fi

#run the main task from arguments
"$@"
code=$?

#show result
if [ 0 -eq $code ]; then
    msg="Operation success    "
else
    msg="Operation failed     "
fi
kill $(jobs -p)
eips 30 1 "$msg" > /dev/null

# Restore WiFi status
if [ 1 -eq $WIFI_IS_OFF ]; then
	lipc-set-prop com.lab126.cmd wirelessEnable 0
	eips 30 3 "Turning off WiFi              " > /dev/null
    sleep 1
    eips 30 3 "                              " > /dev/null
fi
