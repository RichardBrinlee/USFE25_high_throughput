#!/bin/bash

i=1
cd 1
while [ $i -le 99 ]
do
    sbatch lmp.batch
    ((i++))
    cd ../$i
done
