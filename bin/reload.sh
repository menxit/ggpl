#!/usr/bin/env bash

kill -9 $(ps -ax | grep "python $1" | awk '{print $1}')
python $1 & disown
