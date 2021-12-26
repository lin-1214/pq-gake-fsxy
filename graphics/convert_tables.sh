#!/usr/bin/env bash

FOLDER="../build"
OUTPUT="results"

TYPES=(
  "ake"
  "kem"
  "commitment"
  "gake"
)
Ns=(2 4 8 16 32 64 128 256)

mkdir -p ${FOLDER}/${OUTPUT}

for type in "${TYPES[@]}"
do
  if [[ ${type} == "gake" ]]; then
    for N in "${Ns[@]}"
    do
      type_gake="${type}_${N}"
      echo $type_gake
      cat ${FOLDER}/${type_gake}.txt | sed '1,14d;$d' | ${FOLDER}/node_modules/parse-markdown-table-cli/bin | node json2csv.js ${type} ${N} > ${FOLDER}/${OUTPUT}/${type_gake}.csv
      cp ${FOLDER}/${type_gake}.txt ${FOLDER}/${OUTPUT}
    done
  else
    echo $type
    cat ${FOLDER}/${type}.txt | sed '1,14d;$d' | ${FOLDER}/node_modules/parse-markdown-table-cli/bin | node json2csv.js ${type} ${N} > ${FOLDER}/${OUTPUT}/${type}.csv
    cp ${FOLDER}/${type}.txt ${FOLDER}/${OUTPUT}
  fi
done

awk '(NR == 1) || (FNR > 1)' ${FOLDER}/${OUTPUT}/gake_*.csv > ${FOLDER}/${OUTPUT}/gake.csv
