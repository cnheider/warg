#!/usr/bin/env bash

PARENT="$( dirname -- "$0"; )";
cd "${PARENT}" || exit
#./"${PARENT}"/clean.sh
./clean.sh
# shellcheck disable=SC2043
for f in Makefile; do
  make -f "$f" html || exit
done
