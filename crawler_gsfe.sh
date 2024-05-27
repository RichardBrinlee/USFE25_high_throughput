#!/bin/bash

i=1
inner=20
outer=1
# MoNb\1
while [ $i -le $outer ]
do
    # MoNb\1\1
    cd $i
    p=1
    avg_ufse=0
    while [ $p -le $inner ]
    do
        cd $p
        sh gsfe_curve.sh
        # This finds the max number in the GSFE file
        array=()
        file="gsfe"
        while IFS= read -r line; do
            array+="$line"
            array+=" "
        done < "$file"
        test=${array[@]}
        max=$(echo $test | tr ' ' '\n' | sort -n | tail -1)
        avg_ufse=$(awk 'BEGIN {print '"$avg_ufse"' + '"$max"'}')
        cd ../
        if [ $p -eq $inner ]
        then   
            # This finds the USFE and writes it to a file.
            result=$(awk 'BEGIN {print '"$avg_ufse"' / '"$p"'}')
            echo $i $result >> ../usfe.txt
            echo 'The usfe for' $i 'is:' $result
            cd ../
            break   
        fi
        ((p++))
    done 
    ((i++))
done
