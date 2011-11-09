#!/bin/sh

#TWOFACE=192.168.1.100
TWOFACE=twoface

echo -n "Copiando base de datos..."
ssh pilates@$TWOFACE "/home/pilates/codificación/BD/backup_full.sh"
scp pilates@$TWOFACE:/tmp/full_pilates.pgdump /tmp
echo "DONE"
echo -n "Restaurando base de datos en local... "
pg_restore -c -d pilates /tmp/full_pilates.pgdump 
echo "DONE"
echo -n "Copiando log"
scp pilates@$TWOFACE:/home/compartido/upy/formularios/ginn.log ../formularios
echo "DONE"
