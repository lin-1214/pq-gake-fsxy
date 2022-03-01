#!/usr/bin/env bash

FILES=(
  "cycles_level_kem"
  "cycles_level_ake"
  "cycles_level_commitment"
  "cycles_level_gake"
)
INPUT="build/results"
OUTPUT="build/results/cuts"

mkdir -p ${OUTPUT}

for file in "${FILES[@]}"
do
  echo $file
  convert ${INPUT}/${file}.png -crop 3060x1100+0+300 ${OUTPUT}/${file}_level1.png
  convert ${INPUT}/${file}.png -crop 3060x1100+0+1375 ${OUTPUT}/${file}_level3.png
  convert ${INPUT}/${file}.png -crop 3060x1100+0+2475 ${OUTPUT}/${file}_level5.png
done

file="scalability_level_time"
convert ${INPUT}/${file}.png -crop 3060x825+0+300 ${OUTPUT}/${file}_level1.png
convert ${INPUT}/${file}.png -crop 3060x825+0+1375 ${OUTPUT}/${file}_level3.png
convert ${INPUT}/${file}.png -crop 3060x825+0+2475 ${OUTPUT}/${file}_level5.png
