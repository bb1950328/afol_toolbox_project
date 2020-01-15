#!/usr/bin/env bash
#LINE=$(tail -1 ./.github/workflows/unittest_output.txt)
cat ./.github/workflows/unittest_output.txt
LINE=$(tac ./.github/workflows/unittest_output.txt |egrep -m 1 .)
echo "The last line is: $LINE"
[[ $LINE == *"OK"* ]] && exit 0 || exit -1
