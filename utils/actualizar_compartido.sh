#!/bin/sh

mkdir --mode=0777 /home/compartido/upy
cd /home/pilates/codificación
cp -a * /home/compartido/upy
chmod -R a+rwx /home/compartido/upy
cp -f /home/compartido/upy/framework/ginn.conf.pilates /home/compartido/upy/framework/ginn.conf
