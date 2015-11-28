#!/usr/bin/env bash

echo "Manually syncing this folder with raspberry pi"
scp -r ./* pi@192.168.0.15:/home/pi/xfactor_project/human_tracking_PIR_FYP/grid_eye_server/
