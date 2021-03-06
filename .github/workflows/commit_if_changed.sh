#!/usr/bin/env bash

file_count="$(git diff --cached --numstat | wc -l)"
if [ "$file_count" != "0" ]
then
  git commit -am "Rescaled images (Github Action)"
  git push
else
  echo "Nothing changed"
fi
