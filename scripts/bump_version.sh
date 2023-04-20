#!/usr/bin/env bash

VERSION=1.0.1

NEXTVERSION=$(echo ${VERSION} | awk -F. -v OFS=. '{$NF += 1 ; print}')

echo NEXTVERSION