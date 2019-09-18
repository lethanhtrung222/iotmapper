#!/bin/bash

#echo Script Name: "$0"
#echo lat. $1
#echo lon. $2

python kamerka.py --lat $1 --lon $2 --printer --camera
