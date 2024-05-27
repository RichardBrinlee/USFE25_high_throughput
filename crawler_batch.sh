#!/bin/bash
# i=1 -le 50, i=51 -le 99
i=1
inner=20
outer=1
while [ $i -le $outer ]
do
    # MoNb\1\1
    cd $i
    p=1
    while [ $p -le $inner ]
    do
        cd $p
        sbatch lmp.batch
        cd ../
        if [ $p -eq $inner ]
        then
            cd ../
            break   
        fi
        ((p++))
    done 
    ((i++))
    echo $i
done
