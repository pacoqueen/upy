#!/bin/sh

echo ALTER TABLE cliente DROP COLUMN cliente_id | psql pilates
echo ALTER TABLE cliente DROP COLUMN proveedor_id | psql pilates
echo DROP TABLE nomina | psql pilates
echo DROP TABLE ausencia | psql pilates
echo DROP TABLE motivo | psql pilates
echo DROP TABLE baja | psql pilates
echo DROP TABLE calendario_laboral | psql pilates
echo DROP TABLE festivo | psql pilates
echo DROP TABLE vacaciones | psql pilates
echo DROP TABLE turno | psql pilates
echo DROP TABLE grupo | psql pilates
echo DROP TABLE laborable | psql pilates
echo DROP TABLE abono | psql pilates
echo DROP TABLE linea_de_abono | psql pilates
echo DROP TABLE albaran_de_entrada_de_abono | psql pilates
echo DROP TABLE linea_de_devolucion | psql pilates
echo DROP TABLE pago_de_abono | psql pilates
echo DROP TABLE observaciones_nominas | psql pilates
echo DROP TABLE orden_empleados | psql pilates
echo DROP TABLE cobro_factura_de_abono | psql pilates
echo ALTER TABLE cobro DROP COLUMN factura_de_abono_id | psql pilates
echo DROP TABLE factura_de_abono | psql pilates
echo ALTER TABLE presupuesto DROP COLUMN obra | psql pilates
echo ALTER TABLE actividad DROP COLUMN grupo_alumnos_id | psql pilates
echo ALTER TABLE empleado DROP COLUMN planta | psql pilates
echo ALTER TABLE empleado DROP COLUMN preciohora | psql pilates
echo ALTER TABLE empleado DROP COLUMN nomina | psql pilates
echo ALTER TABLE categoria_laboral DROP COLUMN planta | psql pilates
echo ALTER TABLE categoria_laboral DROP COLUMN precio_hora_extra | psql pilates
echo ALTER TABLE categoria_laboral DROP COLUMN precio_hora_nocturnidad | psql pilates
echo ALTER TABLE categoria_laboral DROP COLUMN precio_plus_nocturnidad | psql pilates
echo ALTER TABLE categoria_laboral DROP COLUMN precio_plus_turnicidad| psql pilates
echo ALTER TABLE categoria_laboral DROP COLUMN precio_plus_jefe_turno | psql pilates
echo ALTER TABLE categoria_laboral DROP COLUMN precio_plus_festivo | psql pilates
echo ALTER TABLE categoria_laboral DROP COLUMN precio_plus_mantenimiento_sabados | psql pilates
echo ALTER TABLE categoria_laboral DROP COLUMN dias_vacaciones | psql pilates
echo ALTER TABLE categoria_laboral DROP COLUMN dias_convenio | psql pilates
echo ALTER TABLE categoria_laboral DROP COLUMN dias_asuntos_propios | psql pilates
echo ALTER TABLE categoria_laboral DROP COLUMN salario_base | psql pilates
echo ALTER TABLE categoria_laboral DROP COLUMN precio_hora_regular | psql pilates
pg_dump --data-only -f dump_datos_pilates_solo_datos.sql pilates
./init_db.sh pilates pilates pilates dump_datos_pilates_solo_datos.sql


