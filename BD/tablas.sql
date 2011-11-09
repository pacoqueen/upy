--#############################################################################
-- Copyright (C) 2009-2010 Francisco José Rodríguez Bogado                    #
--                         (frbogado@novaweb.es)                              #
--                                                                            #
-- This file is part of $NAME.                                                #
--                                                                            #
-- $NAME is free software; you can redistribute it and/or modify              #
-- it under the terms of the GNU General Public License as published by       #
-- the Free Software Foundation; either version 2 of the License, or          #
-- (at your option) any later version.                                        #
--                                                                            #
-- $NAME is distributed in the hope that it will be useful,                   #
-- but WITHOUT ANY WARRANTY; without even the implied warranty of             #
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              #
-- GNU General Public License for more details.                               #
--                                                                            #
-- You should have received a copy of the GNU General Public License          #
-- along with $NAME; if not, write to the Free Software                       #
-- Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA #
--#############################################################################

-------------------------------------------------------------
-- Script de creación de tablas para la aplicación Geotex-INN
-------------------------------------------------------------

---- OPERADORES ----

--CREATE FUNCTION xor(BOOL, BOOL) RETURNS BOOL AS
    --'SELECT ($1 AND NOT $2) OR (NOT $1 AND $2);'
    --LANGUAGE 'sql';

-- En realidad creo que <> se comporta igual que XOR. En algunas versiones de
-- PostgreSQL incluso hay un operador != que equivale al XOR lógico también.
-- De cualquier forma, me curo en salud y me construyo el mío propio.
--CREATE OPERATOR +^ (PROCEDURE='xor', LEFTARG = BOOL, RIGHTARG = BOOL);



---- TABLAS ------

-------------
-- Tarifas --
-------------
CREATE TABLE tarifa(
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    observaciones TEXT DEFAULT '',
    periodo_validez_ini DATE DEFAULT NULL,
        -- Fechas de validez de la tarifa. NULL significa que
    periodo_validez_fin DATE DEFAULT NULL       -- no tiene caducidad.
);

---------------------
-- Tabla proveedor --
---------------------
CREATE TABLE proveedor(
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    cif TEXT DEFAULT '',
    direccion TEXT DEFAULT '',
    pais TEXT DEFAULT '',
    ciudad TEXT DEFAULT '',
    provincia TEXT DEFAULT '',
    cp TEXT DEFAULT '',
    telefono TEXT DEFAULT '',
    fax TEXT DEFAULT '',
    contacto TEXT DEFAULT '',
    observaciones TEXT DEFAULT '',
    -- Segunda dirección
    direccionfacturacion TEXT DEFAULT '',
    paisfacturacion TEXT DEFAULT '',
    ciudadfacturacion TEXT DEFAULT '',
    provinciafacturacion TEXT DEFAULT '',
    cpfacturacion TEXT DEFAULT '',
    email TEXT DEFAULT '',
    formadepago TEXT DEFAULT '',    -- Obsoleto. Se usa el campo "vencimiento".
    documentodepago TEXT DEFAULT '',
    vencimiento TEXT DEFAULT '',    -- En principio va igual que los
                                    -- vencimientos de clientes.
    diadepago TEXT DEFAULT '',  -- El día en que se harán los pagos realmente
                                -- (independientemente de lo que marque
                                -- el vencimiento, el pago se puede hacer días
                                -- antes o días después, en un día del
                                -- mes fijo) P.ej: El vencimiento cumple el 15
                                -- de enero pero siempre se le paga al
                                -- proveedor los días 5 de cada mes.
                                -- De momento es texto (aunque en teoría sería
                                -- un INT) para contemplar la posibilidad
                                -- de meter días concatenados con comas -por
                                -- ejemplo- y así expresar que se le
                                -- pagan -por ejemplo one more time- los días
                                -- 5 y 20 de cada mes.
    correoe TEXT DEFAULT '',    -- NEW! 26/09/2006
    web TEXT DEFAULT '',        -- NEW! 26/09/2006
    banco TEXT DEFAULT '',      -- NEW! 04/12/2006
    swif TEXT DEFAULT '',       -- NEW! 04/12/2006. En realidad es SWIFT, pero
                                -- ya sabes cómo es quien tú sabes en esto de
                                -- inventarse nombres...
    iban TEXT DEFAULT '',       -- NEW! 04/12/2006
    cuenta TEXT DEFAULT '',     -- NEW! 04/12/2006
    inhabilitado BOOLEAN DEFAULT FALSE, -- NEW! 05/12/06
    motivo TEXT DEFAULT '',     -- NEW! 05/12/06. Si está inhabilitado no se
                                -- permitirá hacerle más pedidos de
                                -- compra.(CWT)
    iva FLOAT DEFAULT 0.18,     -- NEW! 30/01/07. Iva por defecto del
                                -- proveedor (18% a no ser que sea extranjero).
    nombre_banco TEXT DEFAULT ''    -- NEW! 07/02/2007. CWT: Nombre del
                                    -- banco. No es lo mismo que "banco"
                                    -- ¿Porcuá? pues no lo sé.
);

--------------------
-- Transportistas --
--------------------
CREATE TABLE transportista(
    id SERIAL PRIMARY KEY,
    agencia TEXT DEFAULT '',
    nombre TEXT DEFAULT '',
    DNI TEXT,
    telefono TEXT DEFAULT '',
    matricula TEXT DEFAULT ''
);

--------------
-- Destinos --
-------------------
-- NEW! 23/11/06 --
-------------------
CREATE TABLE destino(
    id SERIAL PRIMARY KEY,
    nombre TEXT DEFAULT '',
    direccion TEXT DEFAULT '',
    cp TEXT DEFAULT '',
    ciudad TEXT DEFAULT '',
    telefono TEXT DEFAULT '',
    pais TEXT DEFAULT ''
--    observaciones TEXT DEFAULT ''
);

-----------------------
-- Pedidos de compra --
-----------------------
CREATE TABLE pedido_compra(
    id SERIAL PRIMARY KEY,
    proveedor_id INT REFERENCES proveedor,   -- Id del proveedor del pedido.
    fecha DATE DEFAULT CURRENT_DATE,
    numpedido TEXT,
    iva FLOAT DEFAULT 0.18,
    descuento FLOAT DEFAULT 0.0, -- Descuento en fracción de 1: 23,44% = 0.2344
    entregas TEXT DEFAULT '',    -- Texto libre para indicar entregas.
    forma_de_pago TEXT DEFAULT '',   -- NEW! 26/09/06
    observaciones TEXT DEFAULT '',   -- NEW! 26/09/06
    bloqueado BOOLEAN DEFAULT FALSE, -- NEW! 08/10/06
    cerrado BOOLEAN DEFAULT FALSE,   -- NEW! 27/11/06. Si el pedido está
                                     -- cerrado no admitirá más albaranes de
                                     -- entrada relacionados ni aparecerá en
                                     -- el listado de pendientes de recibir.
    direccion_entrega0 TEXT DEFAULT '',  -- NEW! 27/02/2009
    direccion_entrega1 TEXT DEFAULT '',  -- NEW! 27/02/2009
    direccion_entrega2 TEXT DEFAULT '',  -- NEW! 27/02/2009
    responsable0 TEXT DEFAULT '',        -- NEW! 27/02/2009
    responsable1 TEXT DEFAULT '',        -- NEW! 27/02/2009
    portes0 TEXT DEFAULT '',             -- NEW! 27/02/2009
    portes1 TEXT DEFAULT '',             -- NEW! 27/02/2009
    observaciones0 TEXT DEFAULT '',     -- NEW! 26/05/2009 3 líneas que van a 
    observaciones1 TEXT DEFAULT '',     -- NEW! 26/05/2009 llevar un texto 
    observaciones2 TEXT DEFAULT ''      -- NEW! 26/05/2009 "casi" fijo. 
);

----------------------
-- Tipo de material --
----------------------
CREATE TABLE tipo_de_material(
    id SERIAL PRIMARY KEY,
    descripcion TEXT
);

-------------------------
-- Productos de compra --
-------------------------
CREATE TABLE producto_compra(
    id SERIAL PRIMARY KEY,
    tipo_de_material_id INT REFERENCES tipo_de_material,
    descripcion TEXT,
    codigo TEXT,
    unidad TEXT DEFAULT 'ud.',
    minimo FLOAT DEFAULT 0.0,
    existencias FLOAT DEFAULT 0.0,
    precio_defecto FLOAT DEFAULT 0.0,
    control_existencias BOOLEAN DEFAULT TRUE,
        -- Si False el programa no controlará las existencias de este producto:
        -- * No mostrará existencias en ventana.
        -- * No mostrará el producto en el listado.
        -- * No permitirá que se añada a la formulación ni se relacione
        --   con consumos.
        -- * No aumentará existencias cuando se le agregue a un albarán de
        --   entrada.
    fvaloracion TEXT DEFAULT '',
        -- Función de evaluación para valorar las existencias en almacén.
        -- Si '' se usa el precio medio (por defecto).
    observaciones TEXT DEFAULT '', 
    obsoleto BOOLEAN DEFAULT FALSE
);

-------------------------------------
-- Clases que componen un producto --
-- y que guarda los datos          --
-- específicos de "agenda".        --
-------------------------------------
CREATE TABLE clase(
    id SERIAL PRIMARY KEY,
    producto_compra_id INT REFERENCES producto_compra,
    num_clases_mes INT DEFAULT 1,       -- Número de clases al mes
    num_clases_semana INT DEFAULT 1,    -- Número de clases por semana.
    pax INT DEFAULT 1,                  -- 1 si es privada. Más si es de grupo.
    dia_semana CHAR(7) DEFAULT NULL,    -- L = lunes. 
                                        -- M = martes.
                                        -- X = miércoles.
                                        -- J = jueves.
                                        -- V = viernes.
                                        -- S = sábado.
                                        -- D = domingo.
                                        -- None si es irrelevante.
    master_trainer BOOLEAN DEFAULT FALSE,   -- Si es con un Máster Trainer 
                                            -- obligatoriamente (más caras).
    caducidad INT DEFAULT 120,  -- Días para agotar las clases compradas.
    num_clases_totales INT DEFAULT 1    -- Si no tiene restricciones de tiempo.
);

----------------------------------------------------------------
-- Precios (relación con atributos entre tarifas y productos) --
----------------------------------------------------------------
CREATE TABLE precio(
    id SERIAL PRIMARY KEY,
    tarifa_id INT REFERENCES tarifa NOT NULL,
    precio FLOAT DEFAULT 0,
    producto_compra_id INT REFERENCES producto_compra 
);

-----------------------
-- Categoría laboral --
-----------------------
CREATE TABLE categoria_laboral(
    id SERIAL PRIMARY KEY,
    codigo TEXT,    -- Lo usaré para "estandarizar" las búsquedas y tal (para
                    -- evitar casos como Jefe turno != Jefe de turno)...
    puesto TEXT,    -- Jefe de turno, Oficial producción, ...
    da_clases BOOLEAN DEFAULT TRUE      -- Si True, da clases de Pilates.
);

---------------
-- Almacenes --
---------------
-- NEW! 11/12/2008
CREATE TABLE almacen(
    id SERIAL PRIMARY KEY, 
    nombre TEXT, 
    observaciones TEXT DEFAULT '', 
    direccion TEXT DEFAULT '', 
    ciudad TEXT DEFAULT '', 
    provincia TEXT DEFAULT '', 
    cp TEXT DEFAULT '', 
    telefono TEXT DEFAULT '', 
    fax TEXT DEFAULT '',
    email TEXT DEFAULT '',
    pais TEXT DEFAULT 'España', 
    principal BOOLEAN DEFAULT TRUE --OJO: solo se usará el primero de los 
                    -- almacenes principales definidos (en caso de que por 
                    -- error se crearan varios). Si el almacén es principal 
                    -- la producción y los consumos de las líneas se harán 
                    -- directamente en él.
    -- ¿Llegaremos a necesitar datos GIS?
);

--------------------------
-- Albaranes de entrada --
--------------------------
CREATE TABLE albaran_entrada(
    id SERIAL PRIMARY KEY,
    proveedor_id INT REFERENCES proveedor DEFAULT NULL,
    fecha DATE DEFAULT CURRENT_DATE,
    numalbaran TEXT,
    bloqueado BOOLEAN DEFAULT FALSE,  -- NEW! 08/10/06
    repuestos BOOLEAN DEFAULT FALSE,    -- NEW! 12/02/08
        -- Si TRUE es un albarán de repuestos, tratamiento un poco especial.
        -- No provienen directamente de pedidos. En ventana permiten crear
        -- artículos.
    almacen_id INT REFERENCES almacen,  -- NEW! 09/01/2009 
    transportista_id INT REFERENCES transportista DEFAULT NULL -- BUGFIX 
                                                               -- 15/01/2009
);

------------------------------------------------------
-- Historial de existencias de productos de compra. --
------------------------------------------------------
-- NEW! 24/11/06                                    --
----------------------------------------------------------
-- Existencias de los productos de compra en una fecha  --
-- determinada.                                         --
----------------------------------------------------------
CREATE TABLE historial_existencias_compra(
    id SERIAL PRIMARY KEY,
    producto_compra_id INT REFERENCES producto_compra NOT NULL,
    fecha DATE DEFAULT CURRENT_DATE,
    cantidad FLOAT DEFAULT 0.0,
    observaciones TEXT DEFAULT '', 
    almacen_id INT REFERENCES almacen 
);

-------------------------------------------------------------------
-- Relación muchos a muchos entre producto de compra y almacenes --
-------------------------------------------------------------------
-- Aquí se guardan las existencias de los productos de compra.
-- La suma de las existencias de todos los almacenes debe coincidir con 
-- el total almacenado en el producto de compra.
CREATE TABLE stock_almacen(
    id SERIAL PRIMARY KEY, 
    almacen_id INT REFERENCES almacen, 
    producto_compra_id INT REFERENCES producto_compra, 
    existencias FLOAT DEFAULT 0.0
);

-----------------------
-- Centro de trabajo --
-----------------------
CREATE TABLE centro_trabajo(
    id SERIAL PRIMARY KEY,
    nombre TEXT, 
    almacen_id INT REFERENCES almacen DEFAULT NULL 
);

-----------------------
-- TABLAS AUXILIARES --
-----------------------
CREATE TABLE usuario(
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(16) UNIQUE NOT NULL CHECK (usuario <> ''), -- Usuario de
                                                               -- la aplicación
    passwd CHAR(32) NOT NULL, -- MD5 de la contraseña
    nombre TEXT DEFAULT '',   -- Nombre completo del usuario
    cuenta TEXT DEFAULT '',   -- Cuenta de correo de soporte
    cpass TEXT DEFAULT '',    -- Contraseña del correo de soporte. TEXTO PLANO.
    nivel INT DEFAULT 5,      -- 0 es el mayor. 5 es el menor.
        -- Además de los permisos sobre ventanas, para un par de casos
        -- especiales se mirará el nivel de privilegios para permitir volver a
        -- desbloquear partes, editar albaranes antiguos y cosas así...
    email TEXT DEFAULT '',          -- NEW! 25/10/2006. Dirección de correo
        -- electrónico del usuario (propia, no soporte).
    smtpserver TEXT DEFAULT '',     -- NEW! 25/10/2006. Servidor SMTP
        -- correspondiente a la dirección anterior por donde
        -- enviar, por ejemplo, albaranes.
    smtpuser TEXT DEFAULT '',       -- NEW! 25/10/2006. Usuario para
        -- autenticación en el servidor SMTP (si fuera necesario)
    smtppassword TEXT DEFAULT '',   -- NEW! 25/10/2006. Contraseña para
        -- autenticación en el servidor SMTP (si fuera necesario).
    firma_total BOOLEAN DEFAULT FALSE,      -- NEW! 26/02/2007. Puede firmar
        -- por cualquiera de los 4 roles en facturas de compra.
    firma_comercial BOOLEAN DEFAULT FALSE,  -- NEW! 26/02/2007. Puede firmar
        -- como director comercial.
    firma_director BOOLEAN DEFAULT FALSE,   -- NEW! 26/02/2007. Puede firmar
        -- como director general.
    firma_tecnico BOOLEAN DEFAULT FALSE,    -- NEW! 26/02/2007. Puede firmar
        -- como director técnico.
    firma_usuario BOOLEAN DEFAULT FALSE,    -- NEW! 26/02/2007. Puede firmar
        -- como usuario (confirmar total de factura).
    observaciones TEXT DEFAULT ''           -- NEW! 26/02/2007. Observaciones.
);

---------------
-- Empleados --
---------------
CREATE TABLE empleado(
    id SERIAL PRIMARY KEY,
    categoria_laboral_id INT REFERENCES categoria_laboral DEFAULT NULL,
    centro_trabajo_id INT REFERENCES centro_trabajo DEFAULT NULL,
    nombre TEXT CHECK (nombre<>''),
    apellidos TEXT,
    dni TEXT,
    activo BOOLEAN DEFAULT TRUE,    -- Si False, el empleado está dado de
                                    -- baja pero se conserva en la BD.
    usuario_id INT REFERENCES usuario DEFAULT NULL, -- NEW! 30/12/2008
        -- Usuario con el que el empleado hace login. Será util para 
        -- identificar a los comerciales automáticamente.
    color_r INT DEFAULT 255, 
    color_g INT DEFAULT 255, 
    color_b INT DEFAULT 255     -- NEW! 22/03/2010
);

------------------------
-- Festivos genéricos --
-------------------------------------------------------------------------------
-- Provisional. No sé si habrá algún cambio en el futuro con las dos tablas  --
-- de festivos.                                                              --
-- Tabla con los festivos comunes a todos los años. Son los festivos por     --
-- defecto que se crean en cada mes y año particular (calendarios_laborales).--
-------------------------------------------------------------------------------
CREATE TABLE festivo_generico(
    id SERIAL PRIMARY KEY,
    fecha DATE      -- El año puede ser ignorado.
);

------------------------------------------------
-- Contador de números de factura por cliente --
------------------------------------------------
CREATE TABLE contador(
    id SERIAL PRIMARY KEY,
    prefijo TEXT DEFAULT '',
    sufijo TEXT DEFAULT '',
    contador INT8
);

-------------------------------------------------
-- Tabla de cuentas origen para transferencias --
-------------------------------------------------
-- No necesita relacionarse con ningún         --
-- registro como ocurre con las cuentas        --
-- destino porque pertenecen a la propia       --
-- empresa, que siempre es la misma (el primer --
-- -y único- registro de la tabla              --
-- datos_de_la_empresa).                       --
-------------------------------------------------
-- NEW! 21/02/07 --
-------------------
CREATE TABLE cuenta_origen(
    id SERIAL PRIMARY KEY,
    nombre TEXT DEFAULT '',
    banco TEXT DEFAULT '',
    ccc TEXT DEFAULT '',
    observaciones TEXT DEFAULT '',
    contacto TEXT DEFAULT '',     -- NEW! 27/02/2007. Persona de contacto en
                                  -- el banco para los faxes de transferencia.
    fax TEXT DEFAULT '',          -- NEW! 27/02/2007.
    telefono TEXT DEFAULT ''      -- NEW! 27/02/2007.
);

--------------
-- Clientes --
--------------
CREATE TABLE cliente(
    id SERIAL PRIMARY KEY,
    tarifa_id INT REFERENCES tarifa DEFAULT NULL,
    contador_id INT REFERENCES contador DEFAULT NULL,
    telefono TEXT DEFAULT '',
    nombre TEXT DEFAULT '',
    cif TEXT DEFAULT '',
    direccion TEXT DEFAULT '',
    pais TEXT DEFAULT '',
    ciudad TEXT DEFAULT '',
    provincia TEXT DEFAULT '',
    cp TEXT DEFAULT '',
    iva FLOAT DEFAULT 0.18,
    direccionfacturacion TEXT DEFAULT '',
    paisfacturacion TEXT DEFAULT '',
    ciudadfacturacion TEXT DEFAULT '',
    provinciafacturacion TEXT DEFAULT '',
    cpfacturacion TEXT DEFAULT '',
    nombref TEXT DEFAULT '',        -- Nombre de facturación (por si difiere
                                    -- del del cliente en la factura).
    email TEXT DEFAULT '',          -- Dirección (o direcciones separadas por
                                    -- coma) de correo electrónico.
    contacto TEXT DEFAULT '',
    observaciones TEXT DEFAULT '',
    vencimientos TEXT DEFAULT '',
    formadepago TEXT DEFAULT '',
    documentodepago TEXT DEFAULT '',
    diadepago TEXT DEFAULT '',  -- El día en que se harán los pagos realmente
                                -- (independientemente de lo que marque
                                -- el vencimiento, el pago se puede hacer días
                                -- antes o días después, en un día del
                                -- mes fijo) P.ej: El vencimiento cumple el 15
                                -- de enero pero siempre se le paga al
                                -- proveedor los días 5 de cada mes.
                                -- De momento es texto (aunque en teoría sería
                                -- un INT) para contemplar la posibilidad
                                -- de meter días concatenados con comas -por
                                -- ejemplo- y así expresar que se le
                                -- pagan -por ejemplo one more time- los días
                                -- 5 y 20 de cada mes.
    inhabilitado BOOLEAN DEFAULT FALSE, -- NEW! 08/10/06
    motivo TEXT DEFAULT '',     -- NEW! 08/10/06. Si está inhabilitado no se
        -- permitirá hacerle más pedidos de venta. (CWT)
    porcentaje FLOAT DEFAULT 0.0,                   -- NEW! 25/10/2006.
        -- Porcentaje de comisión de la facturación que se lleva.
    enviar_correo_albaran BOOLEAN DEFAULT FALSE,    -- NEW! 25/10/2006. Si
        -- TRUE, se envía por correo-e el PDF del albarán Geotexan.
    enviar_correo_factura BOOLEAN DEFAULT FALSE,    -- NEW! 25/10/2006. Si
        -- TRUE, se envía por correo-e el PDF de la factura.
    enviar_correo_packing BOOLEAN DEFAULT FALSE,    -- NEW! 25/10/2006. Si
        -- TRUE, se envía por correo-e el PDF del packing list.
    fax TEXT DEFAULT '',                            -- NEW! 25/10/2006.
        -- Incomprensiblemente, lleva el fax en la ventana
        -- ¡meses! y todavía no estaba en la tabla.
    cuenta_origen_id INT REFERENCES cuenta_origen DEFAULT NULL,-- NEW! 26/02/07
        -- Cuenta bancaria _destino_ por defecto para transferencias.
    riesgo_asegurado FLOAT DEFAULT -1.0, -- NEW! 06/11/2008. -1 = Indefinido
    riesgo_concedido FLOAT DEFAULT -1.0, -- NEW! 06/11/2008. -1 = Indefinido
    packing_list_con_codigo BOOLEAN DEFAULT FALSE,  -- NEW! 27/02/2009
    facturar_con_albaran BOOLEAN DEFAULT TRUE,      -- NEW! 02/03/2009
    copias_factura INT DEFAULT 0,   -- Sin incluir la original. NEW! 09/07/2009
    fecha_alta DATE DEFAULT CURRENT_DATE,   -- NEW! 23/04/2010 
    fecha_nacimiento DATE DEFAULT NULL,     -- NEW! 23/04/2010
    sexo_masculino BOOLEAN DEFAULT NULL,    -- NEW! 23/04/2010  
    lunes BOOLEAN DEFAULT TRUE,     -- NEW! 5/10/2010 
    martes BOOLEAN DEFAULT TRUE,     -- NEW! 5/10/2010 
    miercoles BOOLEAN DEFAULT TRUE,     -- NEW! 5/10/2010 
    jueves BOOLEAN DEFAULT TRUE,     -- NEW! 5/10/2010 
    viernes BOOLEAN DEFAULT TRUE,     -- NEW! 5/10/2010 
    sabado BOOLEAN DEFAULT TRUE,     -- NEW! 5/10/2010 
    domingo BOOLEAN DEFAULT TRUE,    -- NEW! 5/10/2010 
    -- ALTER TABLE cliente ADD COLUMN lunes BOOLEAN DEFAULT TRUE; 
    -- ALTER TABLE cliente ADD COLUMN martes BOOLEAN DEFAULT TRUE; 
    -- ALTER TABLE cliente ADD COLUMN miercoles BOOLEAN DEFAULT TRUE; 
    -- ALTER TABLE cliente ADD COLUMN jueves BOOLEAN DEFAULT TRUE; 
    -- ALTER TABLE cliente ADD COLUMN viernes BOOLEAN DEFAULT TRUE; 
    -- ALTER TABLE cliente ADD COLUMN sabado BOOLEAN DEFAULT TRUE; 
    -- ALTER TABLE cliente ADD COLUMN domingo BOOLEAN DEFAULT TRUE; 
    -- UPDATE CLIENTE SET lunes = TRUE; 
    -- UPDATE CLIENTE SET martes = TRUE; 
    -- UPDATE CLIENTE SET miercoles = TRUE; 
    -- UPDATE CLIENTE SET jueves = TRUE; 
    -- UPDATE CLIENTE SET viernes = TRUE; 
    -- UPDATE CLIENTE SET sabado = TRUE; 
    -- UPDATE CLIENTE SET domingo = TRUE; 
    profesion TEXT DEFAULT '',   -- NEW! 07/10/2010
    codigo INT DEFAULT NULL UNIQUE
);

------------
-- aFotes --
---------------------
-- NEW! 26/04/2010 --
---------------------
CREATE TABLE foto(
    id SERIAL PRIMARY KEY, 
    empleado_id INT REFERENCES empleado DEFAULT NULL, 
    cliente_id INT REFERENCES cliente DEFAULT NULL, 
    data TEXT DEFAULT ''  
    -- ancho INT DEFAULT NULL, 
    -- alto INT DEFAULT NULL, 
    -- tipo TEXT DEFAULT NULL  
    --extension TEXT DEFAULT NULL	-- ¡Mojón de Windows, que sin extensión no 
    							-- sabe identificar el tipo de imagen!
);

-----------------------------------------------------
-- Relación entre clientes y productos contratados --
-----------------------------------------------------
-- NEW! 23/03/2.010 --
----------------------
CREATE TABLE producto_contratado(
    id SERIAL PRIMARY KEY, 
    cliente_id INT REFERENCES cliente NOT NULL,
    producto_compra_id INT REFERENCES producto_compra NOT NULL, 
    fecha_contratacion DATE DEFAULT CURRENT_DATE
);

------------------------------------
-- Cuentas bancarias de clientes. --
------------------------------------
-- NEW! 01/07/07 --
-------------------
CREATE TABLE cuenta_bancaria_cliente(
    id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES cliente NOT NULL,
    observaciones TEXT DEFAULT '',
    banco TEXT DEFAULT '',
    swif TEXT DEFAULT '',
    iban TEXT DEFAULT '',
    cuenta TEXT DEFAULT ''
);

----------------------
-- Pedidos de venta --
----------------------
CREATE TABLE pedido_venta(
    id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES cliente,
    tarifa_id INT REFERENCES tarifa DEFAULT NULL,
    transporte_a_cargo BOOLEAN DEFAULT False,   -- CWT one more time. Al
        -- principio bastaba con la tarifa del cliente, ya no.
    fecha DATE DEFAULT CURRENT_DATE,
    numpedido TEXT,
    iva FLOAT DEFAULT 0.18,
    descuento FLOAT DEFAULT 0.0,     -- Descuento como fracción de 1.
                                     -- 1,44% = 0.0144
    bloqueado BOOLEAN DEFAULT FALSE, -- NEW! 08/10/06
    cerrado BOOLEAN DEFAULT FALSE,   -- NEW! 08/10/06. Si el pedido está
                                     -- cerrado no admitirá más albaranes de
                                     -- salida relacionados ni aparecerá en el
                                     -- listado de pendientes de servir.
    envio_direccion TEXT DEFAULT '', -- NEW! 25/10/2006. Dirección de envío
                                     -- heredable por el albarán de salida.
    envio_ciudad TEXT DEFAULT '',    -- NEW! 25/10/2006. Ciudad de envío.
    envio_provincia TEXT DEFAULT '', -- NEW! 25/10/2006. Dirección de envío:
                                     -- provincia.
    envio_cp TEXT DEFAULT '',        -- NEW! 25/10/2006. Dirección de envío:
                                     -- Código postal.
    envio_pais TEXT DEFAULT '',      -- NEW! 25/10/2006. Dirección de envío:
                                     -- país.
    nombre_correspondencia TEXT DEFAULT '',     -- NEW! 27/02/2009
    direccion_correspondencia TEXT DEFAULT '',  -- NEW! 27/02/2009
    cp_correspondencia TEXT DEFAULT '',         -- NEW! 27/02/2009
    ciudad_correspondencia TEXT DEFAULT '',     -- NEW! 27/02/2009
    provincia_correspondencia TEXT DEFAULT '',  -- NEW! 27/02/2009
    pais_correspondencia TEXT DEFAULT ''       -- NEW! 27/02/2009
);

----------------------------
-- Presupuestos (ofertas) --
----------------------------
-- NEW! 15/03/07 --
------------------------------------------------------------------
-- Relación de productos y servicios ofrecidos a un cliente     --
-- concreto y a un precio determinado. Si se aceptan, pasa      --
-- a ser pedido y de ahí en adelantes sigue si cauce natural.   --
------------------------------------------------------------------
CREATE TABLE presupuesto(
    id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES cliente,
    fecha DATE DEFAULT CURRENT_DATE,
    persona_contacto TEXT DEFAULT '',   -- Por defecto el del cliente.
    nombrecliente TEXT DEFAULT '',      -- Nombre del cliente. Por defecto el
                                        -- del cliente, pero puede ser otro
                                        -- (una obra/constructora o algo).
    direccion TEXT DEFAULT '',          -- Por defecto la del cliente.
    ciudad TEXT DEFAULT '',             -- Por defecto será la del cliente.
    provincia TEXT DEFAULT '',          -- Por defecto será la del cliente.
    cp TEXT DEFAULT '',                 -- Código postal. Por defecto el del
                                        -- cliente.
    pais TEXT DEFAULT '',               -- Por defecto el del cliente.
    telefono TEXT DEFAULT '',           -- Por defecto el del cliente.
    fax TEXT DEFAULT '',                -- Por defecto el del cliente.
    texto TEXT DEFAULT '',              -- Texto de la carta de oferta. Es un
                                        -- texto libre.
    despedida TEXT DEFAULT '',          -- Texto de despedida de la carta de
                                        -- oferta. Es texto libre también.
    validez INT DEFAULT 6,              -- Validez del presupuesto en meses.
                                        -- Si != 0, se tiene en cuenta.
    numpresupuesto INT DEFAULT NULL,    -- NEW! 31/07/2008
    descuento FLOAT DEFAULT 0.0         -- NEW! 31/07/2008 Dto. global en %
);

--------------------
-- Albarán salida --
--------------------
CREATE TABLE albaran_salida(
    id SERIAL PRIMARY KEY,
    numalbaran TEXT UNIQUE,
    transportista_id INT REFERENCES transportista DEFAULT NULL,
    cliente_id INT REFERENCES cliente DEFAULT NULL,
    fecha DATE DEFAULT CURRENT_DATE,
    -- Datos de la dirección de envío:
    nombre TEXT DEFAULT '',
    direccion TEXT DEFAULT '',
    cp TEXT DEFAULT '',
    ciudad TEXT DEFAULT '',
    telefono TEXT DEFAULT '',
    pais TEXT DEFAULT '',
    observaciones TEXT DEFAULT '',
    -- Nuevos campos
    facturable BOOLEAN DEFAULT TRUE,
        -- Si False, el albarán no se puede facturar.
    motivo TEXT DEFAULT '',
        -- Motivo por el que el albarán no puede ser facturado.
    bloqueado BOOLEAN DEFAULT FALSE,
        -- Si True, el albarán solo lo puede modificar un usuario
        -- con nivel de privilegios <= 1.
    destino_id INT REFERENCES destino DEFAULT NULL, 
    almacen_origen_id INT REFERENCES almacen DEFAULT NULL, 
        -- Aunque en realidad por defecto será el almacén principal, pero a la 
        -- hora de crear el registro no se puede definir.
    almacen_destino_id INT REFERENCES almacen DEFAULT NULL
);

--------------------------------
-- Tabla de facturas de venta --
--------------------------------
CREATE TABLE factura_venta(
    id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES cliente,
    fecha DATE DEFAULT CURRENT_DATE,
    numfactura TEXT,
    descuento FLOAT DEFAULT 0.0,
    cargo NUMERIC(9, 2) DEFAULT 0.0,
    observaciones TEXT DEFAULT '',
    iva FLOAT DEFAULT 0.18,    -- Si el cliente no tiene un IVA válido
                               -- definido, se usará el 18%.
    -- OJO: No se tiene en cuenta Recargo de Equivalencia por petición expresa
    -- en documento de requisitos.
    bloqueada BOOLEAN DEFAULT False,
        -- Campo de factura bloqueada para impedir cambios una vez se imprima
        -- y entregue al cliente.
        -- No estoy seguro de que se llegue a usar, pero por si acaso la
        -- incluyo.
    irpf FLOAT DEFAULT 0.0 -- NEW! 10/04/07. Si en datos_de_la_empresa
                            -- irpf != 0.0, aparecerá en la ventana y se
                            -- aplicará a la B.I.
);

--------------------------------
-- Tabla de facturas proforma --
-- o prefacturas.             --
--------------------------------
CREATE TABLE prefactura(
    id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES cliente,
    fecha DATE DEFAULT CURRENT_DATE,
    numfactura TEXT,
    descuento FLOAT DEFAULT 0.0,
    cargo NUMERIC(9, 2) DEFAULT 0.0,
    observaciones TEXT DEFAULT '',
    iva FLOAT DEFAULT 0.18,     -- Si el cliente no tiene un IVA válido
                                -- definido, se usará el 18%.
    -- OJO: No se tiene en cuenta Recargo de Equivalencia por petición expresa
    -- en documento de requisitos.
    bloqueada BOOLEAN DEFAULT False,
        -- Campo de factura bloqueada para impedir cambios una vez se imprima
        -- y entregue al cliente.
        -- No estoy seguro de que se llegue a usar, pero por si acaso la
        -- incluyo.
    irpf FLOAT DEFAULT 0.0  -- NEW! 10/04/07. Si en datos_de_la_empresa
        -- irpf != 0.0, aparecerá en la ventana y se aplicará a la B.I.
);

------------------------------
-- Tickets de venta por TPV --
------------------------------
-- NEW! 19/04/07            --
------------------------------
CREATE TABLE ticket(
    id SERIAL PRIMARY KEY,
    fechahora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    numticket INT8 -- UNIQUE       -- No es UNIQUE. Cada año se vuelve a 1.
);

---------------------
-- Líneas de venta --
---------------------
CREATE TABLE linea_de_venta(
    id SERIAL PRIMARY KEY,
    -- producto_venta_id INT REFERENCES producto_venta,
    pedido_venta_id INT REFERENCES pedido_venta,
    albaran_salida_id INT REFERENCES albaran_salida DEFAULT NULL,
    factura_venta_id INT REFERENCES factura_venta DEFAULT NULL,
    prefactura_id INT REFERENCES prefactura DEFAULT NULL,
    fechahora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cantidad FLOAT,
    precio FLOAT DEFAULT 0.0,
    descuento FLOAT DEFAULT 0.0,
    --    NEW! 23/22/06
    producto_compra_id INT REFERENCES producto_compra DEFAULT NULL,
    ticket_id INT REFERENCES ticket DEFAULT NULL, -- NEW! 19/04/07
    notas TEXT DEFAULT '',  -- NEW! 28/11/07 Campo para guardar anotaciones
                            -- sobre una LDV.
                            -- No son estrictamente observaciones (que según
                            -- el to-do se imprimirían en la factura). Son
                            -- notas para uso interno del usuario, visibles
                            -- solo en pantalla.
    descripcion_complementaria TEXT DEFAULT ''     -- NEW! 30/11/07
        -- Descripción complementaria. Editable por usuario.
);

----------------------
-- Líneas de pedido --
-- NEW! 08/10/06 CWT--
----------------------
CREATE TABLE linea_de_pedido(
    id SERIAL PRIMARY KEY,
    pedido_venta_id INT REFERENCES pedido_venta,
    fechahora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cantidad FLOAT,
    precio FLOAT DEFAULT 0.0,
    descuento FLOAT DEFAULT 0.0,
    fecha_entrega DATE DEFAULT CURRENT_DATE,    -- NEW! 08/10/06
    texto_entrega TEXT DEFAULT '',    -- NEW! 08/10/06
    --    NEW! 26/12/06
    producto_compra_id INT REFERENCES producto_compra DEFAULT NULL,
    presupuesto_id INT REFERENCES presupuesto DEFAULT NULL, -- NEW! 15/03/07
    notas TEXT DEFAULT ''       -- NEW! 29/11/07
);

-------------------------------
-- Eventos especiales        --
-- (Bajas, vacaciones, etc.) --
-------------------------------
CREATE TABLE evento(
    id SERIAL PRIMARY KEY, 
    nombre TEXT DEFAULT '', 
    color_r INT DEFAULT 255, 
    color_g INT DEFAULT 255, 
    color_b INT DEFAULT 255
);

-----------------------
-- Grupos de alumnos --
-----------------------
CREATE TABLE grupo_alumnos(
    id SERIAL PRIMARY KEY, 
    empleado_id INT REFERENCES empleado DEFAULT NULL,    -- Profesor asignado.
    nombre TEXT DEFAULT '', 
    color_r INT DEFAULT 255, 
    color_g INT DEFAULT 255, 
    color_b INT DEFAULT 255, 
    cupo INT DEFAULT 0  -- Cantidad de alumnos que caben.
);

-------------------------------------------
-- Tabla de servicios facturables       --
-- (Servicios prestados por la empresa) --
------------------------------------------
CREATE TABLE servicio(
    id SERIAL PRIMARY KEY,
    factura_venta_id INT REFERENCES factura_venta,
    prefactura_id INT REFERENCES prefactura DEFAULT NULL,
    albaran_salida_id INT REFERENCES albaran_salida DEFAULT NULL,
    concepto TEXT,
    cantidad FLOAT DEFAULT 1.0,
    precio FLOAT,
    descuento FLOAT DEFAULT 0.0,
    pedido_venta_id INT REFERENCES pedido_venta DEFAULT NULL,
    presupuesto_id INT REFERENCES presupuesto DEFAULT NULL, -- NEW! 15/03/07
    notas TEXT DEFAULT ''  -- NEW! 28/11/07
    -- actividad_id INT REFERENCES actividad DEFAULT NULL
);

-----------------------------
-- Actividades en cada día --
-----------------------------
CREATE TABLE actividad(
    id SERIAL PRIMARY KEY, 
    evento_id INT REFERENCES evento, 
    -- grupo_alumnos_id INT REFERENCES grupo_alumnos, 
    fechahora_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    fechahora_fin TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    descripcion TEXT DEFAULT '', 
    empleado_id INT REFERENCES empleado DEFAULT NULL, 
    servicio_id INT REFERENCES servicio DEFAULT NULL,
    producto_compra_id INT REFERENCES producto_compra DEFAULT NULL
    -- ALTER TABLE actividad ADD COLUMN producto_compra_id INT REFERENCES producto_compra DEFAULT NULL; UPDATE actividad SET producto_compra = NULL;
);

-----------------------------------
-- Tabla de relación n a n entre --
-- actividades y alumnos         --
-----------------------------------
CREATE TABLE actividad_cliente(
    cliente_id INT REFERENCES cliente, 
    actividad_id INT REFERENCES actividad
);

---------------------------
-- Máquinas del gimnasio -- 
---------------------------
CREATE TABLE maquina(
    id SERIAL PRIMARY KEY, 
    nombre TEXT DEFAULT '', 
    fecha_compra DATE DEFAULT NULL, 
    numserie TEXT DEFAULT ''
);

-----------------------------------
-- Tabla de relación n a n entre --
-- actividades y máquinas        --
-----------------------------------
CREATE TABLE actividad_maquina(
    actividad_id INT REFERENCES actividad, 
    maquina_id INT REFERENCES maquina
);

---------------------------------
-- Tabla de facturas de compra --
---------------------------------
CREATE TABLE factura_compra(
    id SERIAL PRIMARY KEY,
    proveedor_id INT REFERENCES proveedor,
    fecha DATE DEFAULT CURRENT_DATE,
    numfactura TEXT,
    descuento FLOAT DEFAULT 0.0,
    cargo NUMERIC(9,2) DEFAULT 0.0,
    iva FLOAT DEFAULT 0.18,
    bloqueada BOOLEAN DEFAULT FALSE,
        -- Estado se usará a modo de "flag" para indicar si la factura está
        -- marcada como bloqueada (bloqueada = aceptada, recibida y pagada, no
        -- admite cambios por parte del proveedor). Al igual que con las
        -- facturas de venta, aún no se usa este campo.
    visto_bueno_director BOOLEAN DEFAULT FALSE,
        -- NEW! 25/10/2006. Vto. bueno del director general. Si False, no se
        -- aprueba el pago de la factura.
    visto_bueno_comercial BOOLEAN DEFAULT FALSE,
        -- NEW! 25/10/2006. Vto. bueno del director comercial. Si False, no se
        -- aprueba el pago de la factura.
    visto_bueno_tecnico BOOLEAN DEFAULT FALSE,
        -- NEW! 25/10/2006. Vto. bueno del director técnico. Si False, no se
        -- aprueba el pago de la factura.
    fecha_entrada DATE DEFAULT CURRENT_DATE,
        -- NEW! 25/10/2006. Fecha de entrada de la factura (puede diferir de
        -- la fecha de la factura, que suele ser de emisión).
    fecha_visto_bueno_director DATE DEFAULT CURRENT_DATE,   -- Fecha en que se
        -- da el visto bueno.
    fecha_visto_bueno_comercial DATE DEFAULT CURRENT_DATE,  -- Todas estas
        -- columnas de vistos buenos son automáticas si la
    fecha_visto_bueno_tecnico DATE DEFAULT CURRENT_DATE,    -- factura tiene
        -- pedido y albarán y las cantidades y precios no son superiores a
        -- las de éstos.
    visto_bueno_usuario BOOLEAN DEFAULT FALSE,  -- Necesita una comprobación
        -- de totales del usuario para el vº. bueno auto.
    fecha_visto_bueno_usuario DATE DEFAULT NULL,
    observaciones TEXT DEFAULT '',   -- NEW! 15/02/07. Pues eso. Observaciones.
    vencimientos_confirmados BOOLEAN DEFAULT FALSE -- NEW! 29/08/2008. Para
        -- que no pregunte CADA vez si los vencimientos son correctos cuando 
        -- no coincidan con los del proveedor.
);

-------------------------
-- Líneas de de compra --
-------------------------
CREATE TABLE linea_de_compra(
    id SERIAL PRIMARY KEY,
    pedido_compra_id INT REFERENCES pedido_compra DEFAULT NULL,
    albaran_entrada_id INT REFERENCES albaran_entrada DEFAULT NULL,
    factura_compra_id INT REFERENCES factura_compra DEFAULT NULL,
    producto_compra_id INT REFERENCES producto_compra,
    cantidad FLOAT,
    precio FLOAT DEFAULT 0.0,   -- Sin IVA
    descuento FLOAT DEFAULT 0.0,
    --    factura_compra_id INT REFERENCES factura_compra DEFAULT NULL,
    entrega TEXT DEFAULT '',     -- Entrega estimada del contenido de la LDV
        -- (opcional, se escribe en pedidos de compra) NEW! 26/09/2006
    iva FLOAT DEFAULT 0.18      -- NEW! 15/02/07. IVA de la LDC. Por
        -- compatibilidad con los servicios de las facturas de compra con IVA
        -- mixto.
);

--------------------------------
-- Líneas de pedido de compra --
--------------------------------
-- NEW! 23/11/06              --
-----------------------------------------------------------------
-- Líneas de pedidos de compra. Funcionan igual que las líneas --
-- de pedido de pedidos de venta. Son las líneas que contienen --
-- el pedido original y a partir de las cuales se crean las    --
-- líneas de compra albaraneadas y/o facturadas.               --
-----------------------------------------------------------------
CREATE TABLE linea_de_pedido_de_compra(
    id SERIAL PRIMARY KEY,
    producto_compra_id INT REFERENCES producto_compra,
    pedido_compra_id INT REFERENCES pedido_compra,
    fechahora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cantidad FLOAT,
    precio FLOAT DEFAULT 0.0,
    descuento FLOAT DEFAULT 0.0,
    fecha_entrega DATE DEFAULT CURRENT_DATE,
    texto_entrega TEXT DEFAULT '',
    notas TEXT DEFAULT ''   -- NEW! 12/12/07. Meto aquí también la
                            -- columna notas.
);

----------------------------------------------------------------------------
-- Relación múltiple entre líneas de pedido de compra y líneas de compra. --
----------------------------------------------------------------------------
CREATE TABLE linea_de_pedido_de_compra__linea_de_compra(
    linea_de_pedido_de_compra_id INT NOT NULL
        REFERENCES linea_de_pedido_de_compra,
    linea_de_compra_id INT NOT NULL REFERENCES linea_de_compra
);

----------------------------------------
-- Transportes a cuenta de la empresa --
----------------------------------------------
-- NEW! 21/11/2006                          --
----------------------------------------------
-- Transportes pagados por la empresa de    --
-- los que se recibirá factura.             --
----------------------------------------------
CREATE TABLE transporte_a_cuenta(
    id SERIAL PRIMARY KEY,
    concepto TEXT DEFAULT '',
    precio FLOAT DEFAULT 0.0,
    observaciones TEXT DEFAULT '',
    fecha DATE DEFAULT CURRENT_DATE,
    albaran_salida_id INT REFERENCES albaran_salida DEFAULT NULL,
    proveedor_id INT REFERENCES proveedor DEFAULT NULL
);

------------------------
-- Servicios tomados. --
----------------------------------------------
-- NEW! 21/11/2006                          --
----------------------------------------------
-- Servicios prestados a la empresa que nos --
-- son facturados. No tienen albarán ni     --
-- pedido de compra.                        --
----------------------------------------------
CREATE TABLE servicio_tomado(
    id SERIAL PRIMARY KEY,
    factura_compra_id INT REFERENCES factura_compra,
    concepto TEXT DEFAULT '',
    cantidad FLOAT DEFAULT 0.0,
    precio FLOAT DEFAULT 0.0,
    descuento FLOAT DEFAULT 0.0,
    transporte_a_cuenta_id INT REFERENCES transporte_a_cuenta DEFAULT NULL,
    iva FLOAT DEFAULT 0.18      -- NEW! 15/02/07. IVA del servicio para
        -- facturas de compra "especiales" con IVA mixto. Si una
        -- factura de compra tiene servicios a diferentes IVAs, el IVA de la
        -- factura debe ser 0% e ignorarse.
);

--------------------------
-- Vencimientos de pago --
--------------------------
CREATE TABLE vencimiento_pago(
    id SERIAL PRIMARY KEY,
    factura_compra_id INT REFERENCES factura_compra,
    fecha DATE DEFAULT CURRENT_DATE,
    importe FLOAT DEFAULT 0.0,
    observaciones TEXT DEFAULT ''
);

-----------------------------------------------
-- Tabla de pagarés para pagos a proveedores --
-- NEW! 25 de mayo de 2006                   --
-----------------------------------------------
CREATE TABLE pagare_pago(
    id SERIAL PRIMARY KEY,
    codigo TEXT DEFAULT '',                     -- Algún tipo de código
        -- identificativo o algo. No sé si lo llegaré a usar.
    fecha_emision DATE DEFAULT CURRENT_DATE,    -- Fecha en que se emite el
        -- pagaré.
    fecha_pago DATE DEFAULT NULL,  -- Fecha en que el pago del pagaré se
                                   -- realiza al completo.
    cantidad FLOAT,                -- Cantidad que cubre el pagaré.
    pagado FLOAT DEFAULT 0,        -- Pagado del pagaré hasta el momento.
    observaciones TEXT DEFAULT '', 
    procesado BOOLEAN DEFAULT FALSE,-- Si True, el programa no 
        -- cambiará el estado del pagaré de "pendiente" a "pagado" de forma 
        -- automática.
    fecha_cobrado DATE DEFAULT NULL   -- Fecha en que se paga el pagaré     
        -- definitivamente. Tanto por cumplirse el vencimiento como por 
        -- haberse negociado. Si cobrado >= cantidad, este campo guarda la 
        -- fecha en que se ha realizado el cobro y el confirming ha dejado de 
        -- estar pendiente.
);

--------------------------------------------------
-- Tabla de cuentas destino para transferencias --
--------------------------------------------------
-- NEW! 21/02/07 --
-------------------
CREATE TABLE cuenta_destino(
    id SERIAL PRIMARY KEY,
    nombre TEXT DEFAULT '',
    observaciones TEXT DEFAULT '',
    banco TEXT DEFAULT '',     -- Copiado tal cual de la tabla de proveedores.
    swif TEXT DEFAULT '',      -- Copiado tal cual de la tabla de proveedores.
    iban TEXT DEFAULT '',      -- Copiado tal cual de la tabla de proveedores.
    cuenta TEXT DEFAULT '',    -- Copiado tal cual de la tabla de proveedores.
    nombre_banco TEXT DEFAULT '',   -- Copiado tal cual de la tabla de
                                    -- proveedores.
    proveedor_id INT REFERENCES proveedor DEFAULT NULL  -- Proveedor al que
                                                        -- pertenece la cuenta
);

--------------------
-- Tabla de pagos --
--------------------
CREATE TABLE pago(
    id SERIAL PRIMARY KEY,
    factura_compra_id INT REFERENCES factura_compra,
    fecha DATE DEFAULT CURRENT_DATE,
    importe FLOAT DEFAULT 0.0,
    observaciones TEXT DEFAULT '',
    pagare_pago_id INT REFERENCES pagare_pago DEFAULT NULL,
    proveedor_id INT REFERENCES proveedor DEFAULT NULL,
    cuenta_origen_id INT REFERENCES cuenta_origen DEFAULT NULL,
        -- NEW! 21/02/07. Cuenta bancaria origen para las transferencias.
    cuenta_destino_id INT REFERENCES cuenta_destino DEFAULT NULL, 
        -- NEW! 21/02/07. Cuenta bancaria destino para las transferencias.
    concepto_libre TEXT DEFAULT ''    -- Concepto editable para transferencias.
);

-----------------------
-- Recibos bancarios --
-----------------------
-- NEW! 22/05/07 --
-------------------
CREATE TABLE recibo(
    id SERIAL PRIMARY KEY,
    numrecibo INT,
    anno INT,   -- Imagino que por defecto será el año de la
                -- fecha_libramiento, pero por si acaso pondré por defecto el
                -- año actual en el "constructor".
    -- numrecibo será "calculado" = numrecibo/anno
    lugar_libramiento TEXT DEFAULT '',
    fecha_libramiento DATE DEFAULT CURRENT_DATE,
    -- importe será un campo calculado con la suma de los vencimientos
    -- relacionados. factura será un texto con los números de factura de cada
    -- vencimiento separados por coma. fecha factura se tratará igual que el
    -- campo factura cliente será el cliente del primero de los vencimientos.
    fecha_vencimiento DATE DEFAULT CURRENT_DATE,    -- Por defecto deberá ser
        -- la fecha del primero de los vencimientos,
        -- pero permito editarla por si hay varios o algo.
    persona_pago TEXT DEFAULT '', -- Supongo que lo sacaré de DDE por defecto.
    domicilio_pago TEXT DEFAULT '', -- Ídem
    cuenta_origen_id INT REFERENCES cuenta_origen DEFAULT NULL,  -- Cuenta
        -- bancaria de la empresa para el cobro. OBSOLETO. UNUSED.
    nombre_librado TEXT DEFAULT '', -- Por defecto lo sacaré del cliente, pero
        -- por si acaso dejo editable como campo.
    direccion_librado TEXT DEFAULT '',  -- Ídem
    observaciones TEXT DEFAULT '',      -- No se usará en un futuro inmediato,
        -- pero nunca se sabe.
    cuenta_bancaria_cliente_id INT
        REFERENCES cuenta_bancaria_cliente DEFAULT NULL  -- Cuenta del cliente
        -- donde cargar el recibo.
);

---------------------------
-- Vencimientos de cobro --
---------------------------
CREATE TABLE vencimiento_cobro(
    id SERIAL PRIMARY KEY,
    factura_venta_id INT REFERENCES factura_venta,
    prefactura_id INT REFERENCES prefactura DEFAULT NULL,
    fecha DATE DEFAULT CURRENT_DATE,
    importe FLOAT DEFAULT 0.0,
    observaciones TEXT DEFAULT '',
    cuenta_origen_id INT
        REFERENCES cuenta_origen DEFAULT NULL, -- NEW! 26/02/07. Cuenta
        -- bancaria _destino_ para la transferencia.
        -- Se llama cuenta_origen por motivos de compatibilidad, pero en
        -- realidad es la cuenta de la "propia_empresa" donde el cliente
        -- debe hacer la transferencia.
    recibo_id INT REFERENCES recibo DEFAULT NULL    -- NEW! 22/05/07
);

-----------------------
-- Tablas de Pagarés --
-- NEW! 25/05/2006   --
-----------------------
CREATE TABLE pagare_cobro(
    id SERIAL PRIMARY KEY,
    codigo TEXT DEFAULT '',                     -- Algún tipo de código
        -- identificativo o algo. No sé si lo llegaré a usar.
    fecha_recepcion DATE DEFAULT CURRENT_DATE,  -- Fecha en que se recibe el
        -- pagaré.
    fecha_cobro DATE DEFAULT NULL,  -- Fecha en que el cobro del
        -- pagaré se realiza al completo. Se usa como vencimiento del pagaré.
    cantidad FLOAT,     -- Cantidad que cubre el pagaré.
    cobrado FLOAT DEFAULT 0,    -- Cobrado del pagaré hasta el momento.
    observaciones TEXT DEFAULT '', 
    fecha_cobrado DATE DEFAULT NULL,   -- Fecha en que se cobra el pagaré 
        -- definitivamente. Tanto por cumplirse el vencimiento como por 
        -- haberse negociado. Si cobrado >= cantidad, este campo guarda la 
        -- fecha en que se ha realizado el cobro y el pagaré ha dejado de 
        -- estar pendiente.
    procesado BOOLEAN DEFAULT FALSE -- Si True ya se ha procesado 
        -- automáticamente y no hace falta actualizar el estado al cumplir la 
        -- fecha de vencimiento.
);

--------------------------
-- Tabla de confirmings --
----------------------------------------------------------------------
-- Como pagarés pero con los impagos cubiertos por el propio banco. --
-- Solo uso confirmings para cobrar. Ni se paga ni se emiten.       --
----------------------------------------------------------------------
CREATE TABLE confirming(
    id SERIAL PRIMARY KEY, 
    codigo TEXT DEFAULT '',     -- Número -o código- del confirming 
    fecha_recepcion DATE DEFAULT CURRENT_DATE, 
    fecha_cobro DATE DEFAULT NULL,  -- AKA vencimiento
    cantidad FLOAT,                 -- Cantidad cubierta
    cobrado FLOAT DEFAULT 0,        -- Cobrado hasta el momento. Generalmente 
        -- será 0 o la cantidad completa cuando llegue la fecha de vto.
    observaciones TEXT DEFAULT '', 
    fecha_cobrado DATE DEFAULT NULL,   -- Fecha en que se cobra el confirming
        -- definitivamente. Tanto por cumplirse el vencimiento como por 
        -- haberse negociado. Si cobrado >= cantidad, este campo guarda la 
        -- fecha en que se ha realizado el cobro y el confirming ha dejado de 
        -- estar pendiente.
    procesado BOOLEAN DEFAULT FALSE -- Si True ya se ha procesado 
        -- automáticamente y no hace falta actualizar el estado al cumplir la 
        -- fecha de vencimiento.
);      -- NEW! 20/11/2008

---------------------
-- Tabla de cobros --
---------------------
CREATE TABLE cobro(
    id SERIAL PRIMARY KEY,
    factura_venta_id INT REFERENCES factura_venta,
    prefactura_id INT REFERENCES prefactura DEFAULT NULL,
    fecha DATE DEFAULT CURRENT_DATE,
    importe FLOAT DEFAULT 0.0,
    observaciones TEXT DEFAULT '',
    pagare_cobro_id INT REFERENCES pagare_cobro DEFAULT NULL,
    cliente_id INT REFERENCES cliente DEFAULT NULL,
    -- factura_de_abono_id INT REFERENCES factura_de_abono DEFAULT NULL, 
    confirming_id INT REFERENCES confirming DEFAULT NULL -- NEW! 20/11/2008
);

-------------------------------
-- TABLAS AUXILIARES (cont.) --
-------------------------------
CREATE TABLE modulo(
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    icono TEXT,
    descripcion TEXT
);

CREATE TABLE ventana(
    id SERIAL PRIMARY KEY,
    modulo_id INT REFERENCES modulo,
    descripcion TEXT,
    fichero TEXT,         -- Nombre del fichero .py
    clase TEXT,           -- Nombre de la clase principal de la ventana.
    icono TEXT DEFAULT '' -- Fichero del icono o '' para el icono por defecto
);

CREATE TABLE permiso(
    -- Relación muchos a muchos con atributo entre usuarios y ventanas.
    id SERIAL PRIMARY KEY,
    usuario_id INT REFERENCES usuario,
    ventana_id INT REFERENCES ventana,
    permiso BOOLEAN DEFAULT False,   -- Indica si tiene permiso o no para
                                     -- abrir la ventana.
    --    PRIMARY KEY(usuario_id, ventana_id)   SQLObject requiere que cada
    -- tabla tenga un único ID.
    lectura BOOLEAN DEFAULT False,
    escritura BOOLEAN DEFAULT False,
    nuevo BOOLEAN DEFAULT False     -- Nuevos permisos. Entrarán en la
                                    -- siguiente versión.
);

CREATE TABLE alerta(
    id SERIAL PRIMARY KEY,
    usuario_id INT REFERENCES usuario,
    mensaje TEXT DEFAULT '',
    fechahora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    entregado BOOLEAN DEFAULT False
);

CREATE TABLE datos_de_la_empresa(
    -- Datos de la empresa. Aparecen en los informes, facturas, albaranes,
    -- etc... Además, también sirven para determinar si un cliente es
    -- extranjero, generar albaranes internos...
    id SERIAL PRIMARY KEY,      -- Lo requiere SQLObject, pero no debería
                                -- haber más de un registro aquí.
    nombre TEXT DEFAULT 'Empresa',
    cif TEXT DEFAULT 'T-00.000.000',
    dirfacturacion TEXT DEFAULT 'C/ Dirección de facturación',
    cpfacturacion TEXT DEFAULT '00000',
    ciudadfacturacion TEXT DEFAULT 'Ciudad',
    provinciafacturacion TEXT DEFAULT 'Provincia',
    direccion TEXT DEFAULT 'C/ Dirección postal',
    cp TEXT DEFAULT '00000',
    ciudad TEXT DEFAULT 'Ciudad',
    provincia TEXT DEFAULT 'Provincia',
    telefono TEXT DEFAULT '034 000 00 00 00',
    fax TEXT DEFAULT '034 000 00 00 00',
    email TEXT DEFAULT 'correo@electronico.com',
    paisfacturacion TEXT DEFAULT 'España',
    pais TEXT DEFAULT 'España',
    telefonofacturacion TEXT DEFAULT '000 000 000 000',
    faxfacturacion TEXT DEFAULT '000 000 000 000',
    nombre_responsable_compras TEXT DEFAULT 'Responsable De Compras',
    telefono_responsable_compras TEXT DEFAULT '000 00 00 00',
    nombre_contacto TEXT DEFAULT 'Nombre Contacto',
    registro_mercantil TEXT DEFAULT 'Inscrita en el Registro Mercantil ...',
    email_responsable_compras TEXT DEFAULT 'resposable@compras.com',
    logo TEXT DEFAULT 'logo-inn.png',  -- Nombre de fichero (solo nombre,
        -- no ruta completa) de la imagen del logo de la empresa.
    logo2 TEXT DEFAULT '',  -- Nombre del logo alternativo
    bvqi BOOLEAN DEFAULT TRUE,          -- True si hay que imprimir el logo
                                        -- de calidad certificada BVQI
    -- Dirección para albaran alternativo (albaran composan)
    nomalbaran2 TEXT DEFAULT 'NOMBRE ALTERNATIVO ALBARÁN',
    diralbaran2 TEXT DEFAULT 'Dirección albarán',
    cpalbaran2 TEXT DEFAULT '00000',
    ciualbaran2 TEXT DEFAULT 'Ciudad',
    proalbaran2 TEXT DEFAULT 'Provincia',
    telalbaran2 TEXT DEFAULT '00 000 00 00',
    faxalbaran2 TEXT DEFAULT '00 000 00 00',
    regalbaran2 TEXT DEFAULT 'CIF T-00000000 Reg.Mec. de ...',
    irpf FLOAT DEFAULT 0.0, -- NEW! 10/04/07. Si -0.15 aparecerá el campo
        -- IRPF en las facturas de venta para descontarse de la base imponible
    es_sociedad BOOLEAN DEFAULT TRUE,   -- NEW! 02/05/07. Si es True la
        -- empresa es una sociedad. Si False, la empresa es
        -- persona física o persona jurídica. En los impresos se usará
        -- "nombre" como nombre comercial y nombre_contacto como nombre
        -- fiscal de facturación.
        -- También servirá para discernir si mostrar servicios y transportes
        -- en albaranes y si valorar o no albaranes en el PDF generado al
        -- imprimir.
        -- OJO: También se usa para escribir "FÁBRICA" o "TIENDA" en los
        -- pedidos de compra, etc.
    logoiso1 TEXT DEFAULT 'bvqi.gif',  -- NEW! 27/06/07. Si bvqi es True en
                                       -- algunos impresos aparecerá este logo.
    logoiso2 TEXT DEFAULT 'bvqi2.png', -- NEW! 27/06/07. Si bvqi es True en
                                       -- algunos impresos aparecerá este logo.
    recargo_equivalencia BOOLEAN DEFAULT FALSE, -- 4% adicional de IVA y eso.
    iva FLOAT DEFAULT 0.18, -- IVA soportado por defecto, sin contar R.E.
    ped_compra_texto_fijo TEXT DEFAULT 'ROGAMOS NOS REMITAN COPIA DE ESTE PEDIDO SELLADO Y FIRMADO POR UDS.',   -- Sólo lo puede editar el usuario de nivel 0 (admin).
    ped_compra_texto_editable TEXT DEFAULT 'ESTA MERCANCIA SE DEBE ENTREGAR...', -- Se puede editar por cualquiera con permiso de escritura en pedidos de compra.
    ped_compra_texto_editable_con_nivel1 TEXT DEFAULT 'PAGO A 120 DÍAS F.F. PAGO LOS 25.' -- Solo lo puede editar en perdidos de compra los usuarios con nivel 0 ó 1.
);

------------------------------------------------
-- Documentos adjuntos a pedidos, albaranes,  --
-- facturas y pagarés tanto de venta como de  --
-- compra, etc...                             --
------------------------------------------------
-- NEW! 22/10/2007 --
---------------------
CREATE TABLE documento(
    id SERIAL PRIMARY KEY,
    nombre TEXT DEFAULT '', -- Nombre descriptivo
    -- ruta TEXT,   Prefiero que sea calculado uniendo ruta base de documentos
    -- y nombre de fichero.
    nombre_fichero TEXT DEFAULT '', -- Nombre del fichero. SIN RUTAS.
    observaciones TEXT DEFAULT '',
    pedido_venta_id INT REFERENCES pedido_venta DEFAULT NULL,
    albaran_salida_id INT REFERENCES albaran_salida DEFAULT NULL,
    factura_venta_id INT REFERENCES factura_venta DEFAULT NULL,
    prefactura_id INT REFERENCES prefactura DEFAULT NULL,
    pagare_cobro_id INT REFERENCES pagare_cobro DEFAULT NULL,
    pedido_compra_id INT REFERENCES pedido_compra DEFAULT NULL,
    albaran_entrada_id INT REFERENCES albaran_entrada DEFAULT NULL,
    factura_compra_id INT REFERENCES factura_compra DEFAULT NULL,
    pagare_pago_id INT REFERENCES pagare_pago DEFAULT NULL,
    empleado_id INT REFERENCES empleado DEFAULT NULL,
    cliente_id INT REFERENCES cliente DEFAULT NULL,
    proveedor_id INT REFERENCES proveedor DEFAULT NULL, 
    confirming_id INT REFERENCES confirming DEFAULT NULL -- NEW! 20/11/2008
);

----------------------------------------------------
-- Estadísticas de ventanas abiertas por usuario. --
----------------------------------------------------
-- NEW! 16/12/2007 --
---------------------
CREATE TABLE estadistica(
    id SERIAL PRIMARY KEY,
    usuario_id INT REFERENCES usuario,
    ventana_id INT REFERENCES ventana,
    veces INT DEFAULT 0,
    ultima_vez TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

---------------------------------------------------------------
-- Tabla auxiliar de objetos recientes por usuario y ventana --
---------------------------------------------------------------
-- NEW! 25/08/2008 
CREATE TABLE lista_objetos_recientes(
    id SERIAL PRIMARY KEY, 
    usuario_id INT REFERENCES usuario,
    ventana_id INT REFERENCES ventana
);

----------------------------------------------------
-- IDs de objetos recientes por ventana y usuario --
----------------------------------------------------
-- NEW! 25/08/2008
CREATE TABLE id_reciente(
    id SERIAL PRIMARY KEY, 
    lista_objetos_recientes_id INT REFERENCES lista_objetos_recientes, 
    objeto_id INT NOT NULL
);

---------------------------------------
-- Anotaciones en facturas de venta. --
-- NEW! 26/05/2009                   --
---------------------------------------
CREATE TABLE nota(
    id SERIAL PRIMARY KEY, 
    factura_venta_id INT REFERENCES factura_venta, 
    fechahora TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    texto TEXT DEFAULT '', 
    observaciones TEXT DEFAULT ''
);


-----------------------------------------
-----------------------------------------
--                                     --
-- TABLAS propias de Universal Pilates --
--                                     --
-----------------------------------------
-----------------------------------------

-------------------------------
-- Categorías de actividades --
-------------------------------
CREATE TABLE categoria(
    id SERIAL PRIMARY KEY, 
    nombre TEXT DEFAULT '', 
    color_r INT DEFAULT 255, 
    color_g INT DEFAULT 255, 
    color_b INT DEFAULT 255
);

-----------------------------------------------------------------
-- Relación muchos a muchos entre clientes y grupos de alumnos --
-----------------------------------------------------------------
CREATE TABLE cliente_grupo_alumnos(
    cliente_id INT REFERENCES cliente, 
    grupo_alumnos_id INT REFERENCES grupo_alumnos
);

-----------------------------------------
-- Asistencias a actividades de alumnos --
------------------------------------------
CREATE TABLE asistencia(
    id SERIAL PRIMARY KEY, 
    cliente_id INT REFERENCES cliente, 
    actividad_id INT REFERENCES actividad, 
    fechahora TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    observaciones TEXT DEFAULT ''
);

---------------------
-- Tareas (to-dos) --
---------------------
CREATE TABLE tarea(
    id SERIAL PRIMARY KEY, 
    categoria_id INT REFERENCES categoria, 
    resumen TEXT DEFAULT '', 
    texto TEXT DEFAULT '', 
    fecha_limite DATE DEFAULT NULL, 
    fecha_done DATE DEFAULT NULL, -- Si != None, tarea está completada.
    fechahora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-------------------
-- Notas (memos) --
-------------------
CREATE TABLE memo(
    id SERIAL PRIMARY KEY, 
    categoria_id INT REFERENCES categoria, 
    resumen TEXT DEFAULT '', 
    texto TEXT DEFAULT '', 
    fechahora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-------------------
-- Padecimientos --
-------------------
CREATE TABLE padecimiento(
    id SERIAL PRIMARY KEY, 
    cliente_id INT REFERENCES cliente, 
    fecha DATE DEFAULT CURRENT_DATE,
    texto TEXT DEFAULT ''
);

------------------------ FUNCIONES ------------------------
CREATE FUNCTION ultimo_ticket_mas_uno()
    RETURNS INT8
    LANGUAGE SQL
    AS 'SELECT COALESCE(MAX(numticket), 0)+1
        FROM ticket WHERE date_part(''year'', fechahora)
             = date_part(''year'', CURRENT_DATE);';
        -- NEW! 19/04/07

-------------------------------------------------------------------------------
CREATE FUNCTION cliente_albaran_es_propia_empresa(INT)
    RETURNS BOOLEAN
    LANGUAGE SQL STABLE
    AS 'SELECT COUNT(*) = 1 AS res
        FROM albaran_salida, cliente
        WHERE albaran_salida.id = $1
          AND albaran_salida.cliente_id = cliente.id
          AND cliente.nombre = (SELECT nombre
                                FROM datos_de_la_empresa
                                LIMIT 1)
       ;';      -- NEW! 03/07/2007

---- ALTERS TABLES ---- 
ALTER TABLE ticket ALTER COLUMN numticket SET DEFAULT ultimo_ticket_mas_uno();

---- REGLAS -----

---- ÍNDICES ----
CREATE INDEX cliid ON albaran_salida (cliente_id);
CREATE INDEX prcid ON stock_almacen (producto_compra_id);
CREATE INDEX aid ON stock_almacen (almacen_id);
CREATE UNIQUE INDEX prcid_aid ON stock_almacen (producto_compra_id, almacen_id);
CREATE UNIQUE INDEX hec ON historial_existencias_compra (producto_compra_id, almacen_id, fecha);

---- TRIGGERS ----
CREATE LANGUAGE plpgsql;

-- Para PostgreSQL 7.4 usar:
-- CREATE FUNCTION plpgsql_call_handler() RETURNS language_handler AS '$libdir/plpgsql' LANGUAGE C;
-- CREATE TRUSTED PROCEDURAL LANGUAGE plpgsql HANDLER plpgsql_call_handler;

CREATE FUNCTION contiene_producto_compra(INT)
    RETURNS BOOLEAN
    LANGUAGE SQL STABLE
    AS 'SELECT COUNT(*) > 0 AS res
        FROM albaran_salida, linea_de_venta
        WHERE albaran_salida.id = $1
          AND linea_de_venta.albaran_salida_id = albaran_salida.id
          AND linea_de_venta.producto_compra_id IS NOT NULL
       ;'; 

CREATE FUNCTION es_interno(INT)
    -- Devuelve TRUE si el albarán es un albarán interno de consumo de
    -- materiales o de fibra.
    RETURNS BOOLEAN
    LANGUAGE SQL STABLE
    AS 'SELECT cliente_albaran_es_propia_empresa($1)
           AND contiene_producto_compra($1)
    ;';

CREATE FUNCTION un_solo_almacen_ppal() RETURNS TRIGGER AS '
    BEGIN
--        -- Casos a cubrir:
--        IF OLD IS NULL THEN
--            IF (SELECT COUNT(id) FROM almacen WHERE principal = TRUE) = 0 THEN
--                -- 1.- Que sea el primer almacén que se crea. Debe ser 
--                --     el principal.
--                NEW.principal = TRUE;
--            ELSE
--                -- 2.- Que sea cualquier otro. principal = FALSE.
--                NEW.principal = FALSE;
--            END IF;
--        ELSE    -- OLD IS NOT NULL, está en UPDATE.
--            -- 3.- Que esté actualizando un almacén. 
--            -- IF OLD.principal = TRUE
--                -- Si es el principal, se deja como estaba. 
--                -- NEW.principal = TRUE
--            -- ELSE
--                -- Si no lo es, se pone principal al FALSE.
--                -- NEW.principal = FALSE
--            -- END IF;
--            NEW.principal = OLD.principal;
--        END IF;
        -- Mucho más fácil. Si ya hay un almacén principal el nuevo registro 
        -- debe estar a FALSE en el campo principal. Si no hay ninguno, tanto 
        -- si estoy creando como actualizando registros, devuelvo TRUE y será 
        -- el primero. Las siguientes veces ya siempre devolverá FALSE en ese 
        -- campo.
        IF (SELECT COUNT(id) FROM almacen WHERE principal = TRUE) = 0 THEN
            NEW.principal = TRUE; 
        ELSE
            NEW.principal = FALSE;
        END IF;
        RETURN NEW;
        -- OJO: Si se hace un UPDATE con varios registros, el primero de 
        -- ellos se quedará con el principal a TRUE dependiendo de cómo 
        -- se lo monte el planificador de consultas. De todos modos no me 
        -- preocupa porque el ORM siempre ataca los registros individualmente.
        -- El único problema latente es que hasta que se haga el sync() o 
        -- syncUpdate() el objeto tendrá ese atributo a True.
    END;
' LANGUAGE plpgsql;

CREATE FUNCTION un_solo_almacen_ppal_pero_el_ultimo() RETURNS TRIGGER AS '
    BEGIN
        -- Vale. La idea es justo la contraria que en el caso anterior. Ahora 
        -- voy a intentar respetar el valor del registro nuevo. Si no hay 
        -- definido almacén principal, el nuevo es el principal. Si ya lo 
        -- había y el nuevo quiere serlo, le dejo.
        IF NEW.principal = TRUE THEN
            UPDATE almacen SET principal = FALSE;
        ELSE
            IF (SELECT COUNT(id) FROM almacen WHERE principal = TRUE) = 0 THEN
                NEW.principal = TRUE; 
            END IF;
        END IF;
        RETURN NEW;
    END;
' LANGUAGE plpgsql;

CREATE TRIGGER tr_un_solo_almacen_ppal_pero_el_ultimo 
    BEFORE INSERT OR UPDATE ON almacen 
    --FOR EACH ROW EXECUTE PROCEDURE un_solo_almacen_ppal();
    FOR EACH ROW EXECUTE PROCEDURE un_solo_almacen_ppal_pero_el_ultimo();

