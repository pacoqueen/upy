#!/bin/sh

if [ $1 = "p" ]; then
	cp -f ginn.conf.psql ginn.conf
elif [ $1 = "s" ]; then
	cp -f ginn.conf.sqlite ginn.conf
fi	
