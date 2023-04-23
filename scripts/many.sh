#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
SCRIPTTORUN="glasto2023.py"
NUMBER=5
for ((i=1;i<=NUMBER;i++)); do
    python3 $SCRIPTPATH/$SCRIPTTORUN &
    sleep 10s
done