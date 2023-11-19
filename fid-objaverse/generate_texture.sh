#!/bin/bash
input="/root/CS479-TEXTure/fid-objaverse/guide_list.txt"
while IFS= read -r line
do
  echo "$line"
  python -m scripts.run_texture --config_path="$line"
done < "$input"