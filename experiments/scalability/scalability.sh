#!/bin/bash

export LC_ALL=C

for size in {0..10}; do
    n=$((2**size))
    echo -n "live $n " & for run in {1..5}; do sudo docker run --privileged -i sovrin-schema-matching:cli --ledger live < "b$n.txt" --print-time-only & done | awk '{sum=sum+$1; sumX2+=(($1)^2)} END {printf "Average: %f. Standard Deviation: %f\n", sum/NR, sqrt(sumX2/(NR) - ((sum/NR)^2))}'
    echo -n "builder $n " & for run in {1..5}; do sudo docker run --privileged -i sovrin-schema-matching:cli --ledger builder < "b$n.txt" --print-time-only & done | awk '{sum=sum+$1; sumX2+=(($1)^2)} END {printf "Average: %f. Standard Deviation: %f\n", sum/NR, sqrt(sumX2/(NR) - ((sum/NR)^2))}'
    echo -n "sandbox $n " & for run in {1..5}; do sudo docker run --privileged -i sovrin-schema-matching:cli --ledger sandbox < "b$n.txt" --print-time-only & done | awk '{sum=sum+$1; sumX2+=(($1)^2)} END {printf "Average: %f. Standard Deviation: %f\n", sum/NR, sqrt(sumX2/(NR) - ((sum/NR)^2))}'
done
