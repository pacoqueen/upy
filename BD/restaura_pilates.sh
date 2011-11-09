#!/bin/sh

pg_restore -c -d pilates -Fc $1

