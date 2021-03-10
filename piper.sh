#!/bin/bash

counter=0

while [ $counter -le $1 ]
do
    mkfifo foo
    ./main.py < foo | ./solver.py > foo /dev/null 2>&1 
    rm foo
    ((counter++))
done
