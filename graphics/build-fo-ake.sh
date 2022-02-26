git clone https://github.com/jiep/kyber-gake
cd kyber-gake
git checkout cpu-cycles

mkdir -p build-fo-ake
cd build-fo-ake

cmake ..
make
cd ../..

reverse() {
    # first argument is the array to reverse
    # second is the output array
    declare -n arr="$1" rev="$2"
    for i in "${arr[@]}"
    do
        rev=("$i" "${rev[@]}")
    done
}

PARTIES_CONF="graphics/PARTIES.conf"
BINARIES_PATH="kyber-gake/build-fo-ake"
OUTPUT_FOLDER="build/results"

TYPES=(
  "kex"
  "gake"
)

SEC_LEVELS=(512 768 1024)

IFS=$'\n' read -d '' -r -a Ns < ${PARTIES_CONF}
reverse Ns Ns2

echo

for type in "${TYPES[@]}"
do
  for level in "${SEC_LEVELS[@]}"
  do
    if [[ "$type" == "gake" ]];
    then
      for N in "${Ns2[@]}"
      do
        echo fo-ake-${type}_${level}_${N}.txt
        ./${BINARIES_PATH}/avx2/test_${type}_qrom${level}_avx2 ${N} > fo-ake-${type}_${level}_${N}.txt
        cat fo-ake-${type}_${level}_${N}.txt | sed '1,1d;' | ./node_modules/parse-markdown-table-cli/bin | node graphics/json2csv-fo-ake.js fo-gake ${N} Kyber${level} > fo-ake-${type}_${level}_${N}.csv
      done
    else
      echo fo-ake-${type}_${level}.txt
      ./${BINARIES_PATH}/avx2/test_${type}_qrom${level}_avx2 > fo-ake-${type}_${level}.txt
      cat fo-ake-${type}_${level}.txt | sed '1,1d;$d' | ./node_modules/parse-markdown-table-cli/bin | node graphics/json2csv-fo-ake.js fo-ake 0 Kyber${level} > fo-ake-${type}_${level}.csv
    fi
  done
done

awk '(NR == 1) || (FNR > 1)' fo-ake-kex_*.csv > ${OUTPUT_FOLDER}/fo-ake-ake.csv
awk '(NR == 1) || (FNR > 1)' fo-ake-gake*.csv > ${OUTPUT_FOLDER}/fo-ake-gake.csv

mv *.txt *.csv ${OUTPUT_FOLDER}
