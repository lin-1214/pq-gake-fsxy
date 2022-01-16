#!/usr/bin/env bash

./bin/test_speed_kem > ../kem.txt
./bin/test_speed_ake > ../ake.txt
./bin/test_speed_commitment > ../commitment.txt

Ns=(2 4 8)
for N in "${Ns[@]}"
do
  ./bin/test_speed_gake ${N} > ../gake_${N}.txt
done
