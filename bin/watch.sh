#!/usr/bin/env bash

fswatch -o 0-villa-emo/view.py | xargs -n1 ./bin/reload.sh $1
