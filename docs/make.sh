#!/usr/bin/env bash
clean.sh
for f in Makefile; do
  make -f "$f" html || exit
done
