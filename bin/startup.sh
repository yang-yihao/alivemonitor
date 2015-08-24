#!/bin/sh

cd ..
nohup python main.py alivemonitor > /dev/null &
echo start success.