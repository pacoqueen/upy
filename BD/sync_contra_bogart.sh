#!/bin/sh

BOGART=chaparobo.no-ip.com
SSH=`which ssh`
SCP="`which scp` -C"

echo "Se sincronizará la BD local con la última copia guardada en bogart..."
read -p "Pulsa ENTER para continuar..."
#echo -n "Transfiriendo última copia de seguridad..."
FILEBAK=$($SSH pilates@chaparobo.no-ip.com "ls *.pgdump -tr")
$SCP pilates@$BOGART:$FILEBAK /tmp
echo -n "Restaurando base de datos en local... "
pg_restore -c -d pilates /tmp/$FILEBAK
echo "DONE"
echo "Copiando log..."
$SCP pilates@$BOGART:ginn.log ../formularios
echo "DONE"
