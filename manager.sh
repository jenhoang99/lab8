#!/bin/bash

if [ -z $1 ]; then
        echo "Expecting IP address and port"
        exit
fi

if [ -z $2 ]; then
        echo "Expecting port"
        exit
fi

echo
echo "=========="
echo "disk..."
echo disk | nc $1 $2

echo
echo "=========="
echo "memory..."
echo memory | nc $1 $2

echo
echo "=========="
echo "users..."
echo users | nc $1 $2

echo
echo "=========="
echo "unimplemented command..."
echo NOT_A_VALID_COMMAND | nc $1 $2

echo
echo "DONE"
