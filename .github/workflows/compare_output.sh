#!/usr/bin/env bash
#LINE=$(tail -1 ./.github/workflows/unittest_output.txt)
ls -l
cat ./unittest_output.txt
LINE=$(tac ./unittest_output.txt |egrep -m 1 .)
echo "The last line is: $LINE"
[[ $LINE == *"OK"* ]] && exit 0 || exit -1
