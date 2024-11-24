#!/bin/bash

i=1
cd 1
while [ $i -le 99 ]
do
    # Run the min.sh script in each directory
    sh min.sh

    # the file directory is Lattice/{directory name}/{i}
    dir=$(basename $(dirname $(pwd)))

    # Extract the second column from min_aE and append it to {directory name}.txt
    awk '{print $2}' min_aE | tail -n +1 >> ../$dir.txt

    ((i++))
    if [ $i -le 99 ]; then
        cd ../$i
    fi
done
