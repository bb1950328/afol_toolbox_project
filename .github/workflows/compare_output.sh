#!/usr/bin/env bash
LINE=$(tac ./unittest_output.txt |egrep -m 1 .)  # last line
[[ $LINE == *"OK"* ]] && exit 0 || exit -1
