#!/usr/bin/env bash

PARTIES_CONF="graphics/PARTIES.conf"
INPUT_FOLDER="build/bin"
OUTPUT_FOLDER="build"

reverse() {
    # first argument is the array to reverse
    # second is the output array
    declare -n arr="$1" rev="$2"
    for i in "${arr[@]}"
    do
        rev=("$i" "${rev[@]}")
    done
}

IFS=$'\n' read -d '' -r -a Ns < ${PARTIES_CONF}
reverse Ns Ns2

echo -e "Running KEM..."
${INPUT_FOLDER}/test_speed_kem > ${OUTPUT_FOLDER}/kem.txt

echo -e "Running AKE..."
${INPUT_FOLDER}/test_speed_ake > ${OUTPUT_FOLDER}/ake.txt

echo -e "Running Commitment..."
${INPUT_FOLDER}/test_speed_commitment > ${OUTPUT_FOLDER}/commitment.txt

for N in "${Ns2[@]}"
do
  echo -e "Running GAKE-${N}..."
  ${INPUT_FOLDER}/test_speed_gake ${N} > ${OUTPUT_FOLDER}/gake_${N}.txt
done
