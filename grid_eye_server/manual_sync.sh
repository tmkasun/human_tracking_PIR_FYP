#!/usr/bin/env bash

echo "Manually syncing this folder with raspberry pi"
scp ./* pi@192.168.1.1:/home/pi/xfactor_project/human_tracking_PIR_FYP/grid_eye_server/
