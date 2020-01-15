#!/usr/bin/env bash
LINE = "$(tail -1 ./.github/workflows/unittest_output.txt)"
echo "The last line is: $LINE"
[[ $LINE == *"OK"* ]] && exit 0 || exit -1
