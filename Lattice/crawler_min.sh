#!/bin/bash

i=1
cd 1
while [ $i -le 99 ]
do
    sh min.sh
    tail min_aE >> ../sat.dat
    ((i++))
    cd ../$i
done
