#!/bin/bash

set -euo pipefail

if [ ! -f _raw.json ]; then
       curl https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_sr_legacy_food_json_2018-04.zip > _raw.zip
       unzip _raw.zip
       mv FoodData_Central_sr_legacy_food_json_2018-04.json _raw.json
fi


jq -r '.SRLegacyFoods | sort_by(.description) | .[] | 
       .description as $food | 
       ((.foodNutrients[] | select(.nutrient.number == "205") | .amount) // "N/A") as $carbs |
       .foodPortions[]? | 
       [$food, $carbs, .amount, .modifier, .gramWeight] | @csv' _raw.json > data.csv

rm -f data.csv.gz

gzip data.csv
