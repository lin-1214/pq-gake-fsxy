#!/usr/bin/env bash

PARTIES_CONF="graphics/PARTIES.conf"
JSON2CSV_FOLDER="graphics"
FOLDER="build"
OUTPUT="results"

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

TYPES=(
  "ake"
  "kem"
  "commitment"
  "gake"
)

mkdir -p ${FOLDER}/${OUTPUT}

for type in "${TYPES[@]}"
do
  if [[ ${type} == "gake" ]]; then
    for N in "${Ns2[@]}"
    do
      type_gake="${type}_${N}"
      echo $type_gake
      cat ${FOLDER}/${type_gake}.txt | sed '1,14d;$d' | ./node_modules/parse-markdown-table-cli/bin | node ${JSON2CSV_FOLDER}/json2csv.js ${type} ${N} > ${FOLDER}/${OUTPUT}/${type_gake}.csv
      cp ${FOLDER}/${type_gake}.txt ${FOLDER}/${OUTPUT}
    done
  else
    echo $type
    cat ${FOLDER}/${type}.txt | sed '1,14d;$d' | ./node_modules/parse-markdown-table-cli/bin | node ${JSON2CSV_FOLDER}/json2csv.js ${type} ${N} > ${FOLDER}/${OUTPUT}/${type}.csv
    cp ${FOLDER}/${type}.txt ${FOLDER}/${OUTPUT}
  fi
done

awk '(NR == 1) || (FNR > 1)' ${FOLDER}/${OUTPUT}/gake_*.csv > ${FOLDER}/${OUTPUT}/gake.csv
