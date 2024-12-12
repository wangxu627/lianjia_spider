#!/bin/bash
set -euo pipefail

script_dir=$(dirname "$0")
echo $script_dir
pushd "$script_dir" || exit 1

rm -f nohup.out
current_date=$(date +"%Y-%m-%d_%H")
output_filename="data_${current_date}.jsonl"

cd "$(dirname "$0")"
source venv/bin/activate
nohup scrapy crawl lianjia -o "${output_filename}" &

popd

deactivate
