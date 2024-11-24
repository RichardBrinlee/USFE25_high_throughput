#!/bin/bash

i=1
cd 1
while [ $i -le 99 ]
do
    # Run the min.sh script in each directory
    sh min.sh

    # find the name of the directory
    dir=$(basename `pwd`)

    # Extract the second column from min_aE and append it to lattice.txt
    awk '{print $2}' min_aE >> ../$dir.txt

    # add the i
    ((i++))
    cd ../$i
done
