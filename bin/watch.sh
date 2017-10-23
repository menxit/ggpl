#!/usr/bin/env bash

fswatch -o $1 | xargs -n1 ./bin/reload.sh $1
