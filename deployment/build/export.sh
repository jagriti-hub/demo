#!/bin/bash
Test="$(cat $PWD/input.json | jq -r '.ImageName')"
echo $Test