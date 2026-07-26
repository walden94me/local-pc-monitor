#!/bin/bash
FILE="/home/liang/local-monitor/custom_metrics/my_script.prom"

val=$(grep -oP 'my_script_success_total \K\d+' "$FILE")
new=$((val + 1))
sed -i "s/my_script_success_total $val/my_script_success_total $new/" "$FILE"
