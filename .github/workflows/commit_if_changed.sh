#!/usr/bin/env bash

#TODO chmod a+x this file
COUNT = $(git diff --cached --numstat | wc -l)
if ["$COUNT" != "0"]
then
  git commit -am "Rescaled images (Github Action)"
  git push
else
  echo "Nothing changed"
fi
