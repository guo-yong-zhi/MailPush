#!/bin/sh

touch runningflag
#show status
while [ -f runningflag ]; do
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
    TEST_DOMAIN="www.bing.com"
    TIMEOUT=30      # number of seconds to attempt a connection
    TIMER=$TIMEOUT  
    CONNECTED=0     # whether we are currently connected
    while [ 0 -eq $CONNECTED ]; do
    	# test whether we can ping outside
    	/bin/ping -c 1 -w 2 $TEST_DOMAIN > /dev/null 2>&1 && CONNECTED=1
    	# if we can't, checkout timeout or sleep for 1s
    	if [ 0 -eq $CONNECTED ]; then
    		TIMER=$(($TIMER-1))
    		if [ 0 -eq $TIMER ]; then
    			logger "No internet connection after ${TIMEOUT} seconds, aborting."
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

if :; then
    #run the main task from arguments
    "$@"
    code=$?

    rm -f runningflag
    #show result
    if [ 0 -eq $code ]; then
        msg="Operation success    "
    else
        msg="Operation failed     "
    fi
    sleep 5
    eips 30 1 "$msg" > /dev/null
fi &

TIMEOUT=600   # number of seconds before forced termination
TIMER=$TIMEOUT  
while [ -f runningflag ]; do
    TIMER=$(($TIMER-1))
	if [ 0 -eq $TIMER ]; then
		logger "Not completed after ${TIMEOUT} seconds, aborting."
		break
	fi
	sleep 1
done
sleep 6
kill $(jobs -p) > /dev/null 2>&1
if [ -f runningflag  ]; then
    eips 30 1 "Time out, aborting   " > /dev/null
fi

# Restore WiFi status
if [ 1 -eq $WIFI_IS_OFF ]; then
	lipc-set-prop com.lab126.cmd wirelessEnable 0
	eips 30 3 "Turning off WiFi              " > /dev/null
    sleep 1
    eips 30 3 "                              " > /dev/null
fi
ps aux | grep [m]ailpush | awk '{print $2}' | xargs -i kill {} > /dev/null