#!/usr/bin/env bash

if [ ! -z $(grep "OK" "./unittest_output.txt") ];
then
  exit 0;
else
  exit 1;
fi