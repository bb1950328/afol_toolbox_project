#!/usr/bin/env bash

[[ "$(tail -1 unittest_output.txt)" == "OK" ]] && exit 0 || exit -1
