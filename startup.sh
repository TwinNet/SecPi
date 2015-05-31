#!/bin/bash

# startup script for SecPi

if [ $# -gt 0 ]
then

	# set python path so all classes are found
	export PYTHONPATH=`pwd`

	if [ $1 = "manager" ]
	then
		cd management
		python manager.py
	elif [ $1 = "worker" ]
	then
		cd worker
		python worker.py
	elif [ $1 = "webui" ]
	then
		cd webinterface
		python main.py
	fi

else
	echo "Usage: startup.sh <manager|worker|webui>"

fi