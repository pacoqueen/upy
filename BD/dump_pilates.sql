--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

--
-- Name: plpgsql; Type: PROCEDURAL LANGUAGE; Schema: -; Owner: pilates
--

CREATE PROCEDURAL LANGUAGE plpgsql;


ALTER PROCEDURAL LANGUAGE plpgsql OWNER TO pilates;

SET search_path = public, pg_catalog;

--
-- Name: cliente_albaran_es_propia_empresa(integer); Type: FUNCTION; Schema: public; Owner: pilates
--

CREATE FUNCTION cliente_albaran_es_propia_empresa(integer) RETURNS boolean
    LANGUAGE sql STABLE
    AS $_$SELECT COUNT(*) = 1 AS res
        FROM albaran_salida, cliente
        WHERE albaran_salida.id = $1
          AND albaran_salida.cliente_id = cliente.id
          AND cliente.nombre = (SELECT nombre
                                FROM datos_de_la_empresa
                                LIMIT 1)
       ;$_$;


ALTER FUNCTION public.cliente_albaran_es_propia_empresa(integer) OWNER TO pilates;

--
-- Name: contiene_producto_compra(integer); Type: FUNCTION; Schema: public; Owner: bogado
--

CREATE FUNCTION contiene_producto_compra(integer) RETURNS boolean
    LANGUAGE sql STABLE
    AS $_$SELECT COUNT(*) > 0 AS res
        FROM albaran_salida, linea_de_venta
        WHERE albaran_salida.id = $1
          AND linea_de_venta.albaran_salida_id = albaran_salida.id
          AND linea_de_venta.producto_compra_id IS NOT NULL
       ;$_$;


ALTER FUNCTION public.contiene_producto_compra(integer) OWNER TO bogado;

--
-- Name: es_interno(integer); Type: FUNCTION; Schema: public; Owner: bogado
--

CREATE FUNCTION es_interno(integer) RETURNS boolean
    LANGUAGE sql STABLE
    AS $_$SELECT cliente_albaran_es_propia_empresa($1)
           AND contiene_producto_compra($1)
    ;$_$;


ALTER FUNCTION public.es_interno(integer) OWNER TO bogado;

--
-- Name: ultimo_ticket_mas_uno(); Type: FUNCTION; Schema: public; Owner: pilates
--

CREATE FUNCTION ultimo_ticket_mas_uno() RETURNS bigint
    LANGUAGE sql
    AS $$SELECT COALESCE(MAX(numticket), 0)+1
        FROM ticket WHERE date_part('year', fechahora)
             = date_part('year', CURRENT_DATE);$$;


ALTER FUNCTION public.ultimo_ticket_mas_uno() OWNER TO pilates;

--
-- Name: un_solo_almacen_ppal(); Type: FUNCTION; Schema: public; Owner: pilates
--

CREATE FUNCTION un_solo_almacen_ppal() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
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
$$;


ALTER FUNCTION public.un_solo_almacen_ppal() OWNER TO pilates;

--
-- Name: un_solo_almacen_ppal_pero_el_ultimo(); Type: FUNCTION; Schema: public; Owner: pilates
--

CREATE FUNCTION un_solo_almacen_ppal_pero_el_ultimo() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
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
$$;


ALTER FUNCTION public.un_solo_almacen_ppal_pero_el_ultimo() OWNER TO pilates;

--
-- Name: xor(boolean, boolean); Type: FUNCTION; Schema: public; Owner: pilates
--

CREATE FUNCTION xor(boolean, boolean) RETURNS boolean
    LANGUAGE sql
    AS $_$SELECT ($1 AND NOT $2) OR (NOT $1 AND $2);$_$;


ALTER FUNCTION public.xor(boolean, boolean) OWNER TO pilates;

--
-- Name: +^; Type: OPERATOR; Schema: public; Owner: pilates
--

CREATE OPERATOR +^ (
    PROCEDURE = xor,
    LEFTARG = boolean,
    RIGHTARG = boolean
);


ALTER OPERATOR public.+^ (boolean, boolean) OWNER TO pilates;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: abono; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE abono (
    id integer NOT NULL,
    cliente_id integer,
    factura_de_abono_id integer,
    numabono text DEFAULT ''::text,
    fecha date DEFAULT ('now'::text)::date,
    observaciones text DEFAULT ''::text,
    almacen_id integer
);


ALTER TABLE public.abono OWNER TO pilates;

--
-- Name: abono_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE abono_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.abono_id_seq OWNER TO pilates;

--
-- Name: abono_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE abono_id_seq OWNED BY abono.id;


--
-- Name: abono_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('abono_id_seq', 1, true);


--
-- Name: actividad; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE actividad (
    id integer NOT NULL,
    evento_id integer,
    grupo_alumnos_id integer,
    fechahora_inicio timestamp without time zone DEFAULT now(),
    fechahora_fin timestamp without time zone DEFAULT now(),
    descripcion text DEFAULT ''::text
);


ALTER TABLE public.actividad OWNER TO pilates;

--
-- Name: actividad_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE actividad_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.actividad_id_seq OWNER TO pilates;

--
-- Name: actividad_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE actividad_id_seq OWNED BY actividad.id;


--
-- Name: actividad_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('actividad_id_seq', 29, true);


--
-- Name: albaran_de_entrada_de_abono; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE albaran_de_entrada_de_abono (
    id integer NOT NULL,
    numalbaran text DEFAULT ''::text,
    fecha date DEFAULT ('now'::text)::date,
    observaciones text DEFAULT ''::text
);


ALTER TABLE public.albaran_de_entrada_de_abono OWNER TO pilates;

--
-- Name: albaran_de_entrada_de_abono_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE albaran_de_entrada_de_abono_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.albaran_de_entrada_de_abono_id_seq OWNER TO pilates;

--
-- Name: albaran_de_entrada_de_abono_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE albaran_de_entrada_de_abono_id_seq OWNED BY albaran_de_entrada_de_abono.id;


--
-- Name: albaran_de_entrada_de_abono_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('albaran_de_entrada_de_abono_id_seq', 1, false);


--
-- Name: albaran_entrada; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE albaran_entrada (
    id integer NOT NULL,
    proveedor_id integer,
    fecha date DEFAULT ('now'::text)::date,
    numalbaran text,
    bloqueado boolean DEFAULT false,
    repuestos boolean DEFAULT false,
    almacen_id integer,
    transportista_id integer
);


ALTER TABLE public.albaran_entrada OWNER TO pilates;

--
-- Name: albaran_entrada_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE albaran_entrada_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.albaran_entrada_id_seq OWNER TO pilates;

--
-- Name: albaran_entrada_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE albaran_entrada_id_seq OWNED BY albaran_entrada.id;


--
-- Name: albaran_entrada_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('albaran_entrada_id_seq', 2, true);


--
-- Name: albaran_salida; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE albaran_salida (
    id integer NOT NULL,
    numalbaran text,
    transportista_id integer,
    cliente_id integer,
    fecha date DEFAULT ('now'::text)::date,
    nombre text DEFAULT ''::text,
    direccion text DEFAULT ''::text,
    cp text DEFAULT ''::text,
    ciudad text DEFAULT ''::text,
    telefono text DEFAULT ''::text,
    pais text DEFAULT ''::text,
    observaciones text DEFAULT ''::text,
    facturable boolean DEFAULT true,
    motivo text DEFAULT ''::text,
    bloqueado boolean DEFAULT false,
    destino_id integer,
    almacen_origen_id integer,
    almacen_destino_id integer
);


ALTER TABLE public.albaran_salida OWNER TO pilates;

--
-- Name: albaran_salida_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE albaran_salida_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.albaran_salida_id_seq OWNER TO pilates;

--
-- Name: albaran_salida_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE albaran_salida_id_seq OWNED BY albaran_salida.id;


--
-- Name: albaran_salida_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('albaran_salida_id_seq', 3, true);


--
-- Name: alerta; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE alerta (
    id integer NOT NULL,
    usuario_id integer,
    mensaje text DEFAULT ''::text,
    fechahora timestamp without time zone DEFAULT ('now'::text)::timestamp(0) without time zone,
    entregado boolean DEFAULT false
);


ALTER TABLE public.alerta OWNER TO pilates;

--
-- Name: alerta_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE alerta_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.alerta_id_seq OWNER TO pilates;

--
-- Name: alerta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE alerta_id_seq OWNED BY alerta.id;


--
-- Name: alerta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('alerta_id_seq', 1, false);


--
-- Name: almacen; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE almacen (
    id integer NOT NULL,
    nombre text,
    observaciones text DEFAULT ''::text,
    direccion text DEFAULT ''::text,
    ciudad text DEFAULT ''::text,
    provincia text DEFAULT ''::text,
    cp text DEFAULT ''::text,
    telefono text DEFAULT ''::text,
    fax text DEFAULT ''::text,
    email text DEFAULT ''::text,
    pais text DEFAULT 'España'::text,
    principal boolean DEFAULT true
);


ALTER TABLE public.almacen OWNER TO pilates;

--
-- Name: almacen_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE almacen_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.almacen_id_seq OWNER TO pilates;

--
-- Name: almacen_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE almacen_id_seq OWNED BY almacen.id;


--
-- Name: almacen_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('almacen_id_seq', 2, true);


--
-- Name: asistencia; Type: TABLE; Schema: public; Owner: bogado; Tablespace: 
--

CREATE TABLE asistencia (
    id integer NOT NULL,
    cliente_id integer,
    actividad_id integer,
    fechahora timestamp without time zone DEFAULT now(),
    observaciones text DEFAULT ''::text
);


ALTER TABLE public.asistencia OWNER TO bogado;

--
-- Name: asistencia_id_seq; Type: SEQUENCE; Schema: public; Owner: bogado
--

CREATE SEQUENCE asistencia_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.asistencia_id_seq OWNER TO bogado;

--
-- Name: asistencia_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bogado
--

ALTER SEQUENCE asistencia_id_seq OWNED BY asistencia.id;


--
-- Name: asistencia_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bogado
--

SELECT pg_catalog.setval('asistencia_id_seq', 46, true);


--
-- Name: ausencia; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE ausencia (
    id integer NOT NULL,
    empleado_id integer,
    motivo_id integer,
    fecha date DEFAULT ('now'::text)::date,
    observaciones text DEFAULT ''::text
);


ALTER TABLE public.ausencia OWNER TO pilates;

--
-- Name: ausencia_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE ausencia_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.ausencia_id_seq OWNER TO pilates;

--
-- Name: ausencia_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE ausencia_id_seq OWNED BY ausencia.id;


--
-- Name: ausencia_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('ausencia_id_seq', 1, false);


--
-- Name: baja; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE baja (
    id integer NOT NULL,
    empleado_id integer,
    motivo text DEFAULT ''::text,
    fecha_inicio date DEFAULT ('now'::text)::date,
    fecha_fin date,
    observaciones text DEFAULT ''::text
);


ALTER TABLE public.baja OWNER TO pilates;

--
-- Name: baja_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE baja_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.baja_id_seq OWNER TO pilates;

--
-- Name: baja_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE baja_id_seq OWNED BY baja.id;


--
-- Name: baja_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('baja_id_seq', 1, false);


--
-- Name: calendario_laboral; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE calendario_laboral (
    id integer NOT NULL,
    mes_anno date DEFAULT ('now'::text)::date,
    observaciones text DEFAULT ''::text
);


ALTER TABLE public.calendario_laboral OWNER TO pilates;

--
-- Name: calendario_laboral_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE calendario_laboral_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.calendario_laboral_id_seq OWNER TO pilates;

--
-- Name: calendario_laboral_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE calendario_laboral_id_seq OWNED BY calendario_laboral.id;


--
-- Name: calendario_laboral_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('calendario_laboral_id_seq', 1, false);


--
-- Name: categoria; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE categoria (
    id integer NOT NULL,
    nombre text DEFAULT ''::text,
    color_r integer DEFAULT 255,
    color_g integer DEFAULT 255,
    color_b integer DEFAULT 255
);


ALTER TABLE public.categoria OWNER TO pilates;

--
-- Name: categoria_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE categoria_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.categoria_id_seq OWNER TO pilates;

--
-- Name: categoria_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE categoria_id_seq OWNED BY categoria.id;


--
-- Name: categoria_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('categoria_id_seq', 2, true);


--
-- Name: categoria_laboral; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE categoria_laboral (
    id integer NOT NULL,
    codigo text,
    puesto text,
    planta boolean DEFAULT true,
    precio_hora_extra double precision DEFAULT 8.26,
    precio_hora_nocturnidad double precision DEFAULT 9.58,
    precio_plus_nocturnidad double precision DEFAULT 10.57,
    precio_plus_turnicidad double precision DEFAULT 100.0,
    precio_plus_jefe_turno double precision DEFAULT 104.0,
    precio_plus_festivo double precision DEFAULT 11.0,
    precio_plus_mantenimiento_sabados double precision DEFAULT 11.0,
    dias_vacaciones integer DEFAULT 36,
    dias_convenio integer DEFAULT 2,
    dias_asuntos_propios integer DEFAULT 2,
    salario_base double precision DEFAULT 0.0,
    precio_hora_regular double precision DEFAULT 0.0,
    da_clases boolean DEFAULT true
);


ALTER TABLE public.categoria_laboral OWNER TO pilates;

--
-- Name: categoria_laboral_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE categoria_laboral_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.categoria_laboral_id_seq OWNER TO pilates;

--
-- Name: categoria_laboral_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE categoria_laboral_id_seq OWNED BY categoria_laboral.id;


--
-- Name: categoria_laboral_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('categoria_laboral_id_seq', 4, true);


--
-- Name: centro_trabajo; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE centro_trabajo (
    id integer NOT NULL,
    nombre text,
    almacen_id integer
);


ALTER TABLE public.centro_trabajo OWNER TO pilates;

--
-- Name: centro_trabajo_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE centro_trabajo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.centro_trabajo_id_seq OWNER TO pilates;

--
-- Name: centro_trabajo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE centro_trabajo_id_seq OWNED BY centro_trabajo.id;


--
-- Name: centro_trabajo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('centro_trabajo_id_seq', 1, false);


--
-- Name: cliente; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE cliente (
    id integer NOT NULL,
    tarifa_id integer,
    contador_id integer,
    telefono text DEFAULT ''::text,
    nombre text DEFAULT ''::text,
    cif text DEFAULT ''::text,
    direccion text DEFAULT ''::text,
    pais text DEFAULT ''::text,
    ciudad text DEFAULT ''::text,
    provincia text DEFAULT ''::text,
    cp text DEFAULT ''::text,
    iva double precision DEFAULT 0.18,
    direccionfacturacion text DEFAULT ''::text,
    paisfacturacion text DEFAULT ''::text,
    ciudadfacturacion text DEFAULT ''::text,
    provinciafacturacion text DEFAULT ''::text,
    cpfacturacion text DEFAULT ''::text,
    nombref text DEFAULT ''::text,
    email text DEFAULT ''::text,
    contacto text DEFAULT ''::text,
    observaciones text DEFAULT ''::text,
    vencimientos text DEFAULT ''::text,
    formadepago text DEFAULT ''::text,
    documentodepago text DEFAULT ''::text,
    diadepago text DEFAULT ''::text,
    inhabilitado boolean DEFAULT false,
    motivo text DEFAULT ''::text,
    cliente_id integer,
    porcentaje double precision DEFAULT 0.0,
    enviar_correo_albaran boolean DEFAULT false,
    enviar_correo_factura boolean DEFAULT false,
    enviar_correo_packing boolean DEFAULT false,
    fax text DEFAULT ''::text,
    proveedor_id integer,
    cuenta_origen_id integer,
    riesgo_asegurado double precision DEFAULT (-1.0),
    riesgo_concedido double precision DEFAULT (-1.0),
    packing_list_con_codigo boolean DEFAULT false,
    facturar_con_albaran boolean DEFAULT true,
    copias_factura integer DEFAULT 0
);


ALTER TABLE public.cliente OWNER TO pilates;

--
-- Name: cliente_grupo_alumnos; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE cliente_grupo_alumnos (
    cliente_id integer,
    grupo_alumnos_id integer
);


ALTER TABLE public.cliente_grupo_alumnos OWNER TO pilates;

--
-- Name: cliente_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE cliente_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.cliente_id_seq OWNER TO pilates;

--
-- Name: cliente_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE cliente_id_seq OWNED BY cliente.id;


--
-- Name: cliente_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('cliente_id_seq', 11, true);


--
-- Name: cobro; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE cobro (
    id integer NOT NULL,
    factura_venta_id integer,
    prefactura_id integer,
    fecha date DEFAULT ('now'::text)::date,
    importe double precision DEFAULT 0.0,
    observaciones text DEFAULT ''::text,
    pagare_cobro_id integer,
    cliente_id integer,
    factura_de_abono_id integer,
    confirming_id integer
);


ALTER TABLE public.cobro OWNER TO pilates;

--
-- Name: cobro_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE cobro_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.cobro_id_seq OWNER TO pilates;

--
-- Name: cobro_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE cobro_id_seq OWNED BY cobro.id;


--
-- Name: cobro_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('cobro_id_seq', 6, true);


--
-- Name: confirming; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE confirming (
    id integer NOT NULL,
    codigo text DEFAULT ''::text,
    fecha_recepcion date DEFAULT ('now'::text)::date,
    fecha_cobro date,
    cantidad double precision,
    cobrado double precision DEFAULT 0,
    observaciones text DEFAULT ''::text,
    fecha_cobrado date,
    procesado boolean DEFAULT false
);


ALTER TABLE public.confirming OWNER TO pilates;

--
-- Name: confirming_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE confirming_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.confirming_id_seq OWNER TO pilates;

--
-- Name: confirming_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE confirming_id_seq OWNED BY confirming.id;


--
-- Name: confirming_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('confirming_id_seq', 1, false);


--
-- Name: contador; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE contador (
    id integer NOT NULL,
    prefijo text DEFAULT ''::text,
    sufijo text DEFAULT ''::text,
    contador bigint
);


ALTER TABLE public.contador OWNER TO pilates;

--
-- Name: contador_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE contador_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.contador_id_seq OWNER TO pilates;

--
-- Name: contador_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE contador_id_seq OWNED BY contador.id;


--
-- Name: contador_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('contador_id_seq', 1, true);


--
-- Name: cuenta_bancaria_cliente; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE cuenta_bancaria_cliente (
    id integer NOT NULL,
    cliente_id integer NOT NULL,
    observaciones text DEFAULT ''::text,
    banco text DEFAULT ''::text,
    swif text DEFAULT ''::text,
    iban text DEFAULT ''::text,
    cuenta text DEFAULT ''::text
);


ALTER TABLE public.cuenta_bancaria_cliente OWNER TO pilates;

--
-- Name: cuenta_bancaria_cliente_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE cuenta_bancaria_cliente_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.cuenta_bancaria_cliente_id_seq OWNER TO pilates;

--
-- Name: cuenta_bancaria_cliente_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE cuenta_bancaria_cliente_id_seq OWNED BY cuenta_bancaria_cliente.id;


--
-- Name: cuenta_bancaria_cliente_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('cuenta_bancaria_cliente_id_seq', 2, true);


--
-- Name: cuenta_destino; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE cuenta_destino (
    id integer NOT NULL,
    nombre text DEFAULT ''::text,
    observaciones text DEFAULT ''::text,
    banco text DEFAULT ''::text,
    swif text DEFAULT ''::text,
    iban text DEFAULT ''::text,
    cuenta text DEFAULT ''::text,
    nombre_banco text DEFAULT ''::text,
    proveedor_id integer
);


ALTER TABLE public.cuenta_destino OWNER TO pilates;

--
-- Name: cuenta_destino_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE cuenta_destino_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.cuenta_destino_id_seq OWNER TO pilates;

--
-- Name: cuenta_destino_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE cuenta_destino_id_seq OWNED BY cuenta_destino.id;


--
-- Name: cuenta_destino_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('cuenta_destino_id_seq', 2, true);


--
-- Name: cuenta_origen; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE cuenta_origen (
    id integer NOT NULL,
    nombre text DEFAULT ''::text,
    banco text DEFAULT ''::text,
    ccc text DEFAULT ''::text,
    observaciones text DEFAULT ''::text,
    contacto text DEFAULT ''::text,
    fax text DEFAULT ''::text,
    telefono text DEFAULT ''::text
);


ALTER TABLE public.cuenta_origen OWNER TO pilates;

--
-- Name: cuenta_origen_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE cuenta_origen_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.cuenta_origen_id_seq OWNER TO pilates;

--
-- Name: cuenta_origen_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE cuenta_origen_id_seq OWNED BY cuenta_origen.id;


--
-- Name: cuenta_origen_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('cuenta_origen_id_seq', 2, true);


--
-- Name: datos_de_la_empresa; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE datos_de_la_empresa (
    id integer NOT NULL,
    nombre text DEFAULT 'Empresa'::text,
    cif text DEFAULT 'T-00.000.000'::text,
    dirfacturacion text DEFAULT 'C/ Dirección de facturación'::text,
    cpfacturacion text DEFAULT '00000'::text,
    ciudadfacturacion text DEFAULT 'Ciudad'::text,
    provinciafacturacion text DEFAULT 'Provincia'::text,
    direccion text DEFAULT 'C/ Dirección postal'::text,
    cp text DEFAULT '00000'::text,
    ciudad text DEFAULT 'Ciudad'::text,
    provincia text DEFAULT 'Provincia'::text,
    telefono text DEFAULT '034 000 00 00 00'::text,
    fax text DEFAULT '034 000 00 00 00'::text,
    email text DEFAULT 'correo@electronico.com'::text,
    paisfacturacion text DEFAULT 'España'::text,
    pais text DEFAULT 'España'::text,
    telefonofacturacion text DEFAULT '000 000 000 000'::text,
    faxfacturacion text DEFAULT '000 000 000 000'::text,
    nombre_responsable_compras text DEFAULT 'Responsable De Compras'::text,
    telefono_responsable_compras text DEFAULT '000 00 00 00'::text,
    nombre_contacto text DEFAULT 'Nombre Contacto'::text,
    registro_mercantil text DEFAULT 'Inscrita en el Registro Mercantil ...'::text,
    email_responsable_compras text DEFAULT 'resposable@compras.com'::text,
    logo text DEFAULT 'logo-inn.png'::text,
    logo2 text DEFAULT ''::text,
    bvqi boolean DEFAULT true,
    nomalbaran2 text DEFAULT 'NOMBRE ALTERNATIVO ALBARÁN'::text,
    diralbaran2 text DEFAULT 'Dirección albarán'::text,
    cpalbaran2 text DEFAULT '00000'::text,
    ciualbaran2 text DEFAULT 'Ciudad'::text,
    proalbaran2 text DEFAULT 'Provincia'::text,
    telalbaran2 text DEFAULT '00 000 00 00'::text,
    faxalbaran2 text DEFAULT '00 000 00 00'::text,
    regalbaran2 text DEFAULT 'CIF T-00000000 Reg.Mec. de ...'::text,
    irpf double precision DEFAULT 0.0,
    es_sociedad boolean DEFAULT true,
    logoiso1 text DEFAULT 'bvqi.gif'::text,
    logoiso2 text DEFAULT 'bvqi2.png'::text,
    recargo_equivalencia boolean DEFAULT false,
    iva double precision DEFAULT 0.18,
    ped_compra_texto_fijo text DEFAULT 'ROGAMOS NOS REMITAN COPIA DE ESTE PEDIDO SELLADO Y FIRMADO POR UDS.'::text,
    ped_compra_texto_editable text DEFAULT 'ESTA MERCANCIA SE DEBE ENTREGAR...'::text,
    ped_compra_texto_editable_con_nivel1 text DEFAULT 'PAGO A 120 DÍAS F.F. PAGO LOS 25.'::text
);


ALTER TABLE public.datos_de_la_empresa OWNER TO pilates;

--
-- Name: datos_de_la_empresa_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE datos_de_la_empresa_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.datos_de_la_empresa_id_seq OWNER TO pilates;

--
-- Name: datos_de_la_empresa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE datos_de_la_empresa_id_seq OWNED BY datos_de_la_empresa.id;


--
-- Name: datos_de_la_empresa_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('datos_de_la_empresa_id_seq', 5, true);


--
-- Name: destino; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE destino (
    id integer NOT NULL,
    nombre text DEFAULT ''::text,
    direccion text DEFAULT ''::text,
    cp text DEFAULT ''::text,
    ciudad text DEFAULT ''::text,
    telefono text DEFAULT ''::text,
    pais text DEFAULT ''::text
);


ALTER TABLE public.destino OWNER TO pilates;

--
-- Name: destino_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE destino_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.destino_id_seq OWNER TO pilates;

--
-- Name: destino_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE destino_id_seq OWNED BY destino.id;


--
-- Name: destino_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('destino_id_seq', 1, true);


--
-- Name: documento; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE documento (
    id integer NOT NULL,
    nombre text DEFAULT ''::text,
    nombre_fichero text DEFAULT ''::text,
    observaciones text DEFAULT ''::text,
    pedido_venta_id integer,
    albaran_salida_id integer,
    factura_venta_id integer,
    prefactura_id integer,
    pagare_cobro_id integer,
    pedido_compra_id integer,
    albaran_entrada_id integer,
    factura_compra_id integer,
    pagare_pago_id integer,
    empleado_id integer,
    cliente_id integer,
    proveedor_id integer,
    confirming_id integer
);


ALTER TABLE public.documento OWNER TO pilates;

--
-- Name: documento_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE documento_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.documento_id_seq OWNER TO pilates;

--
-- Name: documento_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE documento_id_seq OWNED BY documento.id;


--
-- Name: documento_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('documento_id_seq', 1, true);


--
-- Name: empleado; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE empleado (
    id integer NOT NULL,
    categoria_laboral_id integer,
    centro_trabajo_id integer,
    nombre text,
    apellidos text,
    dni text,
    planta boolean DEFAULT true,
    nomina numeric(9,2) DEFAULT 0.0,
    preciohora numeric(9,2) DEFAULT 0.0,
    activo boolean DEFAULT true,
    usuario_id integer,
    CONSTRAINT empleado_nombre_check CHECK ((nombre <> ''::text))
);


ALTER TABLE public.empleado OWNER TO pilates;

--
-- Name: empleado_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE empleado_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.empleado_id_seq OWNER TO pilates;

--
-- Name: empleado_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE empleado_id_seq OWNED BY empleado.id;


--
-- Name: empleado_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('empleado_id_seq', 4, true);


--
-- Name: estadistica; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE estadistica (
    id integer NOT NULL,
    usuario_id integer,
    ventana_id integer,
    veces integer DEFAULT 0,
    ultima_vez timestamp without time zone DEFAULT ('now'::text)::timestamp(0) without time zone
);


ALTER TABLE public.estadistica OWNER TO pilates;

--
-- Name: estadistica_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE estadistica_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.estadistica_id_seq OWNER TO pilates;

--
-- Name: estadistica_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE estadistica_id_seq OWNED BY estadistica.id;


--
-- Name: estadistica_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('estadistica_id_seq', 56, true);


--
-- Name: evento; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE evento (
    id integer NOT NULL,
    nombre text DEFAULT ''::text,
    color_r integer DEFAULT 255,
    color_g integer DEFAULT 255,
    color_b integer DEFAULT 255
);


ALTER TABLE public.evento OWNER TO pilates;

--
-- Name: evento_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE evento_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.evento_id_seq OWNER TO pilates;

--
-- Name: evento_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE evento_id_seq OWNED BY evento.id;


--
-- Name: evento_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('evento_id_seq', 2, true);


--
-- Name: factura_compra; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE factura_compra (
    id integer NOT NULL,
    proveedor_id integer,
    fecha date DEFAULT ('now'::text)::date,
    numfactura text,
    descuento double precision DEFAULT 0.0,
    cargo numeric(9,2) DEFAULT 0.0,
    iva double precision DEFAULT 0.18,
    bloqueada boolean DEFAULT false,
    visto_bueno_director boolean DEFAULT false,
    visto_bueno_comercial boolean DEFAULT false,
    visto_bueno_tecnico boolean DEFAULT false,
    fecha_entrada date DEFAULT ('now'::text)::date,
    fecha_visto_bueno_director date DEFAULT ('now'::text)::date,
    fecha_visto_bueno_comercial date DEFAULT ('now'::text)::date,
    fecha_visto_bueno_tecnico date DEFAULT ('now'::text)::date,
    visto_bueno_usuario boolean DEFAULT false,
    fecha_visto_bueno_usuario date,
    observaciones text DEFAULT ''::text,
    vencimientos_confirmados boolean DEFAULT false
);


ALTER TABLE public.factura_compra OWNER TO pilates;

--
-- Name: factura_compra_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE factura_compra_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.factura_compra_id_seq OWNER TO pilates;

--
-- Name: factura_compra_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE factura_compra_id_seq OWNED BY factura_compra.id;


--
-- Name: factura_compra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('factura_compra_id_seq', 2, true);


--
-- Name: factura_de_abono; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE factura_de_abono (
    id integer NOT NULL,
    fecha date DEFAULT ('now'::text)::date
);


ALTER TABLE public.factura_de_abono OWNER TO pilates;

--
-- Name: factura_de_abono_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE factura_de_abono_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.factura_de_abono_id_seq OWNER TO pilates;

--
-- Name: factura_de_abono_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE factura_de_abono_id_seq OWNED BY factura_de_abono.id;


--
-- Name: factura_de_abono_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('factura_de_abono_id_seq', 1, false);


--
-- Name: factura_venta; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE factura_venta (
    id integer NOT NULL,
    cliente_id integer,
    fecha date DEFAULT ('now'::text)::date,
    numfactura text,
    descuento double precision DEFAULT 0.0,
    cargo numeric(9,2) DEFAULT 0.0,
    observaciones text DEFAULT ''::text,
    iva double precision DEFAULT 0.18,
    bloqueada boolean DEFAULT false,
    irpf double precision DEFAULT 0.0
);


ALTER TABLE public.factura_venta OWNER TO pilates;

--
-- Name: factura_venta_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE factura_venta_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.factura_venta_id_seq OWNER TO pilates;

--
-- Name: factura_venta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE factura_venta_id_seq OWNED BY factura_venta.id;


--
-- Name: factura_venta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('factura_venta_id_seq', 29, true);


--
-- Name: festivo; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE festivo (
    id integer NOT NULL,
    calendario_laboral_id integer,
    fecha date DEFAULT ('now'::text)::date
);


ALTER TABLE public.festivo OWNER TO pilates;

--
-- Name: festivo_generico; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE festivo_generico (
    id integer NOT NULL,
    fecha date
);


ALTER TABLE public.festivo_generico OWNER TO pilates;

--
-- Name: festivo_generico_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE festivo_generico_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.festivo_generico_id_seq OWNER TO pilates;

--
-- Name: festivo_generico_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE festivo_generico_id_seq OWNED BY festivo_generico.id;


--
-- Name: festivo_generico_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('festivo_generico_id_seq', 1, false);


--
-- Name: festivo_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE festivo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.festivo_id_seq OWNER TO pilates;

--
-- Name: festivo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE festivo_id_seq OWNED BY festivo.id;


--
-- Name: festivo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('festivo_id_seq', 1, false);


--
-- Name: grupo; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE grupo (
    id integer NOT NULL,
    nombre text,
    jefeturno_id integer,
    operario1_id integer,
    operario2_id integer,
    observaciones text DEFAULT ''::text
);


ALTER TABLE public.grupo OWNER TO pilates;

--
-- Name: grupo_alumnos; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE grupo_alumnos (
    id integer NOT NULL,
    nombre text DEFAULT ''::text,
    color_r integer DEFAULT 255,
    color_g integer DEFAULT 255,
    color_b integer DEFAULT 255,
    cupo integer DEFAULT 0,
    empleado_id integer
);


ALTER TABLE public.grupo_alumnos OWNER TO pilates;

--
-- Name: grupo_alumnos_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE grupo_alumnos_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.grupo_alumnos_id_seq OWNER TO pilates;

--
-- Name: grupo_alumnos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE grupo_alumnos_id_seq OWNED BY grupo_alumnos.id;


--
-- Name: grupo_alumnos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('grupo_alumnos_id_seq', 6, true);


--
-- Name: grupo_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE grupo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.grupo_id_seq OWNER TO pilates;

--
-- Name: grupo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE grupo_id_seq OWNED BY grupo.id;


--
-- Name: grupo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('grupo_id_seq', 1, false);


--
-- Name: historial_existencias_compra; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE historial_existencias_compra (
    id integer NOT NULL,
    producto_compra_id integer NOT NULL,
    fecha date DEFAULT ('now'::text)::date,
    cantidad double precision DEFAULT 0.0,
    observaciones text DEFAULT ''::text,
    almacen_id integer
);


ALTER TABLE public.historial_existencias_compra OWNER TO pilates;

--
-- Name: historial_existencias_compra_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE historial_existencias_compra_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.historial_existencias_compra_id_seq OWNER TO pilates;

--
-- Name: historial_existencias_compra_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE historial_existencias_compra_id_seq OWNED BY historial_existencias_compra.id;


--
-- Name: historial_existencias_compra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('historial_existencias_compra_id_seq', 86, true);


--
-- Name: id_reciente; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE id_reciente (
    id integer NOT NULL,
    lista_objetos_recientes_id integer,
    objeto_id integer NOT NULL
);


ALTER TABLE public.id_reciente OWNER TO pilates;

--
-- Name: id_reciente_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE id_reciente_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.id_reciente_id_seq OWNER TO pilates;

--
-- Name: id_reciente_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE id_reciente_id_seq OWNED BY id_reciente.id;


--
-- Name: id_reciente_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('id_reciente_id_seq', 2, true);


--
-- Name: laborable; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE laborable (
    id integer NOT NULL,
    fecha date DEFAULT ('now'::text)::date,
    turno_id integer,
    calendario_laboral_id integer,
    grupo_id integer,
    observaciones text DEFAULT ''::text
);


ALTER TABLE public.laborable OWNER TO pilates;

--
-- Name: laborable_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE laborable_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.laborable_id_seq OWNER TO pilates;

--
-- Name: laborable_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE laborable_id_seq OWNED BY laborable.id;


--
-- Name: laborable_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('laborable_id_seq', 1, false);


--
-- Name: linea_de_abono; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE linea_de_abono (
    id integer NOT NULL,
    linea_de_venta_id integer,
    abono_id integer,
    diferencia double precision DEFAULT 0.0,
    cantidad double precision DEFAULT 0.0,
    observaciones text DEFAULT ''::text,
    servicio_id integer
);


ALTER TABLE public.linea_de_abono OWNER TO pilates;

--
-- Name: linea_de_abono_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE linea_de_abono_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.linea_de_abono_id_seq OWNER TO pilates;

--
-- Name: linea_de_abono_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE linea_de_abono_id_seq OWNED BY linea_de_abono.id;


--
-- Name: linea_de_abono_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('linea_de_abono_id_seq', 1, false);


--
-- Name: linea_de_compra; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE linea_de_compra (
    id integer NOT NULL,
    pedido_compra_id integer,
    albaran_entrada_id integer,
    factura_compra_id integer,
    producto_compra_id integer,
    cantidad double precision,
    precio double precision DEFAULT 0.0,
    descuento double precision DEFAULT 0.0,
    entrega text DEFAULT ''::text,
    iva double precision DEFAULT 0.18
);


ALTER TABLE public.linea_de_compra OWNER TO pilates;

--
-- Name: linea_de_compra_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE linea_de_compra_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.linea_de_compra_id_seq OWNER TO pilates;

--
-- Name: linea_de_compra_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE linea_de_compra_id_seq OWNED BY linea_de_compra.id;


--
-- Name: linea_de_compra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('linea_de_compra_id_seq', 4, true);


--
-- Name: linea_de_devolucion; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE linea_de_devolucion (
    id integer NOT NULL,
    abono_id integer,
    albaran_de_entrada_de_abono_id integer,
    albaran_salida_id integer,
    precio double precision DEFAULT 0.0,
    observaciones text DEFAULT ''::text
);


ALTER TABLE public.linea_de_devolucion OWNER TO pilates;

--
-- Name: linea_de_devolucion_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE linea_de_devolucion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.linea_de_devolucion_id_seq OWNER TO pilates;

--
-- Name: linea_de_devolucion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE linea_de_devolucion_id_seq OWNED BY linea_de_devolucion.id;


--
-- Name: linea_de_devolucion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('linea_de_devolucion_id_seq', 1, false);


--
-- Name: linea_de_pedido; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE linea_de_pedido (
    id integer NOT NULL,
    pedido_venta_id integer,
    fechahora timestamp without time zone DEFAULT now(),
    cantidad double precision,
    precio double precision DEFAULT 0.0,
    descuento double precision DEFAULT 0.0,
    fecha_entrega date DEFAULT ('now'::text)::date,
    texto_entrega text DEFAULT ''::text,
    producto_compra_id integer,
    presupuesto_id integer,
    notas text DEFAULT ''::text
);


ALTER TABLE public.linea_de_pedido OWNER TO pilates;

--
-- Name: linea_de_pedido_de_compra; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE linea_de_pedido_de_compra (
    id integer NOT NULL,
    producto_compra_id integer,
    pedido_compra_id integer,
    fechahora timestamp without time zone DEFAULT now(),
    cantidad double precision,
    precio double precision DEFAULT 0.0,
    descuento double precision DEFAULT 0.0,
    fecha_entrega date DEFAULT ('now'::text)::date,
    texto_entrega text DEFAULT ''::text,
    notas text DEFAULT ''::text
);


ALTER TABLE public.linea_de_pedido_de_compra OWNER TO pilates;

--
-- Name: linea_de_pedido_de_compra__linea_de_compra; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE linea_de_pedido_de_compra__linea_de_compra (
    linea_de_pedido_de_compra_id integer NOT NULL,
    linea_de_compra_id integer NOT NULL
);


ALTER TABLE public.linea_de_pedido_de_compra__linea_de_compra OWNER TO pilates;

--
-- Name: linea_de_pedido_de_compra_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE linea_de_pedido_de_compra_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.linea_de_pedido_de_compra_id_seq OWNER TO pilates;

--
-- Name: linea_de_pedido_de_compra_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE linea_de_pedido_de_compra_id_seq OWNED BY linea_de_pedido_de_compra.id;


--
-- Name: linea_de_pedido_de_compra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('linea_de_pedido_de_compra_id_seq', 3, true);


--
-- Name: linea_de_pedido_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE linea_de_pedido_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.linea_de_pedido_id_seq OWNER TO pilates;

--
-- Name: linea_de_pedido_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE linea_de_pedido_id_seq OWNED BY linea_de_pedido.id;


--
-- Name: linea_de_pedido_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('linea_de_pedido_id_seq', 3, true);


--
-- Name: linea_de_venta; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE linea_de_venta (
    id integer NOT NULL,
    pedido_venta_id integer,
    albaran_salida_id integer,
    factura_venta_id integer,
    prefactura_id integer,
    fechahora timestamp without time zone DEFAULT now(),
    cantidad double precision,
    precio double precision DEFAULT 0.0,
    descuento double precision DEFAULT 0.0,
    producto_compra_id integer,
    ticket_id integer,
    notas text DEFAULT ''::text,
    descripcion_complementaria text DEFAULT ''::text
);


ALTER TABLE public.linea_de_venta OWNER TO pilates;

--
-- Name: linea_de_venta_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE linea_de_venta_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.linea_de_venta_id_seq OWNER TO pilates;

--
-- Name: linea_de_venta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE linea_de_venta_id_seq OWNED BY linea_de_venta.id;


--
-- Name: linea_de_venta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('linea_de_venta_id_seq', 14, true);


--
-- Name: lista_objetos_recientes; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE lista_objetos_recientes (
    id integer NOT NULL,
    usuario_id integer,
    ventana_id integer
);


ALTER TABLE public.lista_objetos_recientes OWNER TO pilates;

--
-- Name: lista_objetos_recientes_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE lista_objetos_recientes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.lista_objetos_recientes_id_seq OWNER TO pilates;

--
-- Name: lista_objetos_recientes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE lista_objetos_recientes_id_seq OWNED BY lista_objetos_recientes.id;


--
-- Name: lista_objetos_recientes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('lista_objetos_recientes_id_seq', 2, true);


--
-- Name: memo; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE memo (
    id integer NOT NULL,
    categoria_id integer,
    resumen text DEFAULT ''::text,
    texto text DEFAULT ''::text,
    fechahora timestamp without time zone DEFAULT now()
);


ALTER TABLE public.memo OWNER TO pilates;

--
-- Name: memo_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE memo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.memo_id_seq OWNER TO pilates;

--
-- Name: memo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE memo_id_seq OWNED BY memo.id;


--
-- Name: memo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('memo_id_seq', 5, true);


--
-- Name: modulo; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE modulo (
    id integer NOT NULL,
    nombre text,
    icono text,
    descripcion text
);


ALTER TABLE public.modulo OWNER TO pilates;

--
-- Name: modulo_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE modulo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.modulo_id_seq OWNER TO pilates;

--
-- Name: modulo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE modulo_id_seq OWNED BY modulo.id;


--
-- Name: modulo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('modulo_id_seq', 1, false);


--
-- Name: motivo; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE motivo (
    id integer NOT NULL,
    descripcion text,
    descripcion_dias text DEFAULT ''::text,
    retribuido integer DEFAULT 0,
    sin_retribuir integer DEFAULT 0,
    excedencia_maxima integer DEFAULT 0,
    convenio boolean DEFAULT true,
    penaliza boolean DEFAULT true
);


ALTER TABLE public.motivo OWNER TO pilates;

--
-- Name: motivo_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE motivo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.motivo_id_seq OWNER TO pilates;

--
-- Name: motivo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE motivo_id_seq OWNED BY motivo.id;


--
-- Name: motivo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('motivo_id_seq', 1, false);


--
-- Name: nomina; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE nomina (
    id integer NOT NULL,
    empleado_id integer NOT NULL,
    fecha date,
    cantidad numeric(9,2) DEFAULT 0.0,
    horas_extra double precision DEFAULT 0.0,
    horas_nocturnidad double precision DEFAULT 0.0,
    gratificacion double precision DEFAULT 0.0,
    plus_jefe_turno double precision DEFAULT 0.0,
    plus_no_absentismo double precision DEFAULT 0.0,
    plus_festivo double precision DEFAULT 0.0,
    plus_turnicidad double precision DEFAULT 0.0,
    plus_mantenimiento_sabados double precision DEFAULT 0.0,
    total_horas_extra double precision DEFAULT 0.0,
    total_horas_nocturnidad double precision DEFAULT 0.0,
    base double precision DEFAULT 0.0,
    otros double precision DEFAULT 0.0,
    fechaini date DEFAULT ('now'::text)::date,
    fechafin date DEFAULT ('now'::text)::date
);


ALTER TABLE public.nomina OWNER TO pilates;

--
-- Name: nomina_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE nomina_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.nomina_id_seq OWNER TO pilates;

--
-- Name: nomina_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE nomina_id_seq OWNED BY nomina.id;


--
-- Name: nomina_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('nomina_id_seq', 1, false);


--
-- Name: nota; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE nota (
    id integer NOT NULL,
    factura_venta_id integer,
    fechahora timestamp without time zone DEFAULT now(),
    texto text DEFAULT ''::text,
    observaciones text DEFAULT ''::text
);


ALTER TABLE public.nota OWNER TO pilates;

--
-- Name: nota_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE nota_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.nota_id_seq OWNER TO pilates;

--
-- Name: nota_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE nota_id_seq OWNED BY nota.id;


--
-- Name: nota_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('nota_id_seq', 1, false);


--
-- Name: observaciones_nominas; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE observaciones_nominas (
    id integer NOT NULL,
    fecha date DEFAULT ('now'::text)::date,
    observaciones text DEFAULT ''::text
);


ALTER TABLE public.observaciones_nominas OWNER TO pilates;

--
-- Name: observaciones_nominas_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE observaciones_nominas_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.observaciones_nominas_id_seq OWNER TO pilates;

--
-- Name: observaciones_nominas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE observaciones_nominas_id_seq OWNED BY observaciones_nominas.id;


--
-- Name: observaciones_nominas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('observaciones_nominas_id_seq', 1, false);


--
-- Name: orden_empleados; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE orden_empleados (
    id integer NOT NULL,
    orden integer NOT NULL,
    empleado_id integer NOT NULL,
    fecha date DEFAULT ('now'::text)::date
);


ALTER TABLE public.orden_empleados OWNER TO pilates;

--
-- Name: orden_empleados_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE orden_empleados_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.orden_empleados_id_seq OWNER TO pilates;

--
-- Name: orden_empleados_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE orden_empleados_id_seq OWNED BY orden_empleados.id;


--
-- Name: orden_empleados_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('orden_empleados_id_seq', 1, false);


--
-- Name: padecimiento; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE padecimiento (
    id integer NOT NULL,
    cliente_id integer,
    fecha date DEFAULT ('now'::text)::date,
    texto text DEFAULT ''::text
);


ALTER TABLE public.padecimiento OWNER TO pilates;

--
-- Name: padecimiento_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE padecimiento_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.padecimiento_id_seq OWNER TO pilates;

--
-- Name: padecimiento_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE padecimiento_id_seq OWNED BY padecimiento.id;


--
-- Name: padecimiento_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('padecimiento_id_seq', 3, true);


--
-- Name: pagare_cobro; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE pagare_cobro (
    id integer NOT NULL,
    codigo text DEFAULT ''::text,
    fecha_recepcion date DEFAULT ('now'::text)::date,
    fecha_cobro date,
    cantidad double precision,
    cobrado double precision DEFAULT 0,
    observaciones text DEFAULT ''::text,
    fecha_cobrado date,
    procesado boolean DEFAULT false
);


ALTER TABLE public.pagare_cobro OWNER TO pilates;

--
-- Name: pagare_cobro_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE pagare_cobro_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.pagare_cobro_id_seq OWNER TO pilates;

--
-- Name: pagare_cobro_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE pagare_cobro_id_seq OWNED BY pagare_cobro.id;


--
-- Name: pagare_cobro_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('pagare_cobro_id_seq', 2, true);


--
-- Name: pagare_pago; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE pagare_pago (
    id integer NOT NULL,
    codigo text DEFAULT ''::text,
    fecha_emision date DEFAULT ('now'::text)::date,
    fecha_pago date,
    cantidad double precision,
    pagado double precision DEFAULT 0,
    observaciones text DEFAULT ''::text,
    procesado boolean DEFAULT false,
    fecha_cobrado date
);


ALTER TABLE public.pagare_pago OWNER TO pilates;

--
-- Name: pagare_pago_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE pagare_pago_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.pagare_pago_id_seq OWNER TO pilates;

--
-- Name: pagare_pago_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE pagare_pago_id_seq OWNED BY pagare_pago.id;


--
-- Name: pagare_pago_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('pagare_pago_id_seq', 2, true);


--
-- Name: pago; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE pago (
    id integer NOT NULL,
    factura_compra_id integer,
    fecha date DEFAULT ('now'::text)::date,
    importe double precision DEFAULT 0.0,
    observaciones text DEFAULT ''::text,
    pagare_pago_id integer,
    proveedor_id integer,
    cuenta_origen_id integer,
    cuenta_destino_id integer,
    concepto_libre text DEFAULT ''::text
);


ALTER TABLE public.pago OWNER TO pilates;

--
-- Name: pago_de_abono; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE pago_de_abono (
    id integer NOT NULL,
    factura_de_abono_id integer,
    factura_venta_id integer,
    prefactura_id integer,
    importe double precision DEFAULT 0.0,
    pendiente boolean DEFAULT true
);


ALTER TABLE public.pago_de_abono OWNER TO pilates;

--
-- Name: pago_de_abono_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE pago_de_abono_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.pago_de_abono_id_seq OWNER TO pilates;

--
-- Name: pago_de_abono_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE pago_de_abono_id_seq OWNED BY pago_de_abono.id;


--
-- Name: pago_de_abono_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('pago_de_abono_id_seq', 1, false);


--
-- Name: pago_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE pago_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.pago_id_seq OWNER TO pilates;

--
-- Name: pago_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE pago_id_seq OWNED BY pago.id;


--
-- Name: pago_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('pago_id_seq', 2, true);


--
-- Name: pedido_compra; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE pedido_compra (
    id integer NOT NULL,
    proveedor_id integer,
    fecha date DEFAULT ('now'::text)::date,
    numpedido text,
    iva double precision DEFAULT 0.18,
    descuento double precision DEFAULT 0.0,
    entregas text DEFAULT ''::text,
    forma_de_pago text DEFAULT ''::text,
    observaciones text DEFAULT ''::text,
    bloqueado boolean DEFAULT false,
    cerrado boolean DEFAULT false,
    direccion_entrega0 text DEFAULT ''::text,
    direccion_entrega1 text DEFAULT ''::text,
    direccion_entrega2 text DEFAULT ''::text,
    responsable0 text DEFAULT ''::text,
    responsable1 text DEFAULT ''::text,
    portes0 text DEFAULT ''::text,
    portes1 text DEFAULT ''::text,
    observaciones0 text DEFAULT ''::text,
    observaciones1 text DEFAULT ''::text,
    observaciones2 text DEFAULT ''::text
);


ALTER TABLE public.pedido_compra OWNER TO pilates;

--
-- Name: pedido_compra_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE pedido_compra_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.pedido_compra_id_seq OWNER TO pilates;

--
-- Name: pedido_compra_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE pedido_compra_id_seq OWNED BY pedido_compra.id;


--
-- Name: pedido_compra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('pedido_compra_id_seq', 3, true);


--
-- Name: pedido_venta; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE pedido_venta (
    id integer NOT NULL,
    cliente_id integer,
    tarifa_id integer,
    transporte_a_cargo boolean DEFAULT false,
    fecha date DEFAULT ('now'::text)::date,
    numpedido text,
    iva double precision DEFAULT 0.18,
    descuento double precision DEFAULT 0.0,
    bloqueado boolean DEFAULT false,
    cerrado boolean DEFAULT false,
    envio_direccion text DEFAULT ''::text,
    envio_ciudad text DEFAULT ''::text,
    envio_provincia text DEFAULT ''::text,
    envio_cp text DEFAULT ''::text,
    envio_pais text DEFAULT ''::text,
    nombre_correspondencia text DEFAULT ''::text,
    direccion_correspondencia text DEFAULT ''::text,
    cp_correspondencia text DEFAULT ''::text,
    ciudad_correspondencia text DEFAULT ''::text,
    provincia_correspondencia text DEFAULT ''::text,
    pais_correspondencia text DEFAULT ''::text
);


ALTER TABLE public.pedido_venta OWNER TO pilates;

--
-- Name: pedido_venta_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE pedido_venta_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.pedido_venta_id_seq OWNER TO pilates;

--
-- Name: pedido_venta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE pedido_venta_id_seq OWNED BY pedido_venta.id;


--
-- Name: pedido_venta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('pedido_venta_id_seq', 3, true);


--
-- Name: permiso; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE permiso (
    id integer NOT NULL,
    usuario_id integer,
    ventana_id integer,
    permiso boolean DEFAULT false,
    lectura boolean DEFAULT false,
    escritura boolean DEFAULT false,
    nuevo boolean DEFAULT false
);


ALTER TABLE public.permiso OWNER TO pilates;

--
-- Name: permiso_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE permiso_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.permiso_id_seq OWNER TO pilates;

--
-- Name: permiso_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE permiso_id_seq OWNED BY permiso.id;


--
-- Name: permiso_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('permiso_id_seq', 106, true);


--
-- Name: precio; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE precio (
    id integer NOT NULL,
    tarifa_id integer NOT NULL,
    precio double precision DEFAULT 0,
    producto_compra_id integer
);


ALTER TABLE public.precio OWNER TO pilates;

--
-- Name: precio_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE precio_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.precio_id_seq OWNER TO pilates;

--
-- Name: precio_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE precio_id_seq OWNED BY precio.id;


--
-- Name: precio_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('precio_id_seq', 2, true);


--
-- Name: prefactura; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE prefactura (
    id integer NOT NULL,
    cliente_id integer,
    fecha date DEFAULT ('now'::text)::date,
    numfactura text,
    descuento double precision DEFAULT 0.0,
    cargo numeric(9,2) DEFAULT 0.0,
    observaciones text DEFAULT ''::text,
    iva double precision DEFAULT 0.18,
    bloqueada boolean DEFAULT false,
    irpf double precision DEFAULT 0.0
);


ALTER TABLE public.prefactura OWNER TO pilates;

--
-- Name: prefactura_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE prefactura_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.prefactura_id_seq OWNER TO pilates;

--
-- Name: prefactura_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE prefactura_id_seq OWNED BY prefactura.id;


--
-- Name: prefactura_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('prefactura_id_seq', 1, false);


--
-- Name: presupuesto; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE presupuesto (
    id integer NOT NULL,
    cliente_id integer,
    fecha date DEFAULT ('now'::text)::date,
    persona_contacto text DEFAULT ''::text,
    nombrecliente text DEFAULT ''::text,
    direccion text DEFAULT ''::text,
    ciudad text DEFAULT ''::text,
    provincia text DEFAULT ''::text,
    cp text DEFAULT ''::text,
    pais text DEFAULT ''::text,
    telefono text DEFAULT ''::text,
    fax text DEFAULT ''::text,
    texto text DEFAULT ''::text,
    despedida text DEFAULT ''::text,
    validez integer DEFAULT 6,
    numpresupuesto integer,
    descuento double precision DEFAULT 0.0,
    obra text DEFAULT ''::text
);


ALTER TABLE public.presupuesto OWNER TO pilates;

--
-- Name: presupuesto_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE presupuesto_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.presupuesto_id_seq OWNER TO pilates;

--
-- Name: presupuesto_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE presupuesto_id_seq OWNED BY presupuesto.id;


--
-- Name: presupuesto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('presupuesto_id_seq', 1, true);


--
-- Name: producto_compra; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE producto_compra (
    id integer NOT NULL,
    tipo_de_material_id integer,
    descripcion text,
    codigo text,
    unidad text DEFAULT 'ud.'::text,
    minimo double precision DEFAULT 0.0,
    existencias double precision DEFAULT 0.0,
    precio_defecto double precision DEFAULT 0.0,
    control_existencias boolean DEFAULT true,
    fvaloracion text DEFAULT ''::text,
    observaciones text DEFAULT ''::text,
    obsoleto boolean DEFAULT false
);


ALTER TABLE public.producto_compra OWNER TO pilates;

--
-- Name: producto_compra_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE producto_compra_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.producto_compra_id_seq OWNER TO pilates;

--
-- Name: producto_compra_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE producto_compra_id_seq OWNED BY producto_compra.id;


--
-- Name: producto_compra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('producto_compra_id_seq', 5, true);


--
-- Name: proveedor; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE proveedor (
    id integer NOT NULL,
    nombre text,
    cif text DEFAULT ''::text,
    direccion text DEFAULT ''::text,
    pais text DEFAULT ''::text,
    ciudad text DEFAULT ''::text,
    provincia text DEFAULT ''::text,
    cp text DEFAULT ''::text,
    telefono text DEFAULT ''::text,
    fax text DEFAULT ''::text,
    contacto text DEFAULT ''::text,
    observaciones text DEFAULT ''::text,
    direccionfacturacion text DEFAULT ''::text,
    paisfacturacion text DEFAULT ''::text,
    ciudadfacturacion text DEFAULT ''::text,
    provinciafacturacion text DEFAULT ''::text,
    cpfacturacion text DEFAULT ''::text,
    email text DEFAULT ''::text,
    formadepago text DEFAULT ''::text,
    documentodepago text DEFAULT ''::text,
    vencimiento text DEFAULT ''::text,
    diadepago text DEFAULT ''::text,
    correoe text DEFAULT ''::text,
    web text DEFAULT ''::text,
    banco text DEFAULT ''::text,
    swif text DEFAULT ''::text,
    iban text DEFAULT ''::text,
    cuenta text DEFAULT ''::text,
    inhabilitado boolean DEFAULT false,
    motivo text DEFAULT ''::text,
    iva double precision DEFAULT 0.18,
    nombre_banco text DEFAULT ''::text
);


ALTER TABLE public.proveedor OWNER TO pilates;

--
-- Name: proveedor_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE proveedor_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.proveedor_id_seq OWNER TO pilates;

--
-- Name: proveedor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE proveedor_id_seq OWNED BY proveedor.id;


--
-- Name: proveedor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('proveedor_id_seq', 2, true);


--
-- Name: recibo; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE recibo (
    id integer NOT NULL,
    numrecibo integer,
    anno integer,
    lugar_libramiento text DEFAULT ''::text,
    fecha_libramiento date DEFAULT ('now'::text)::date,
    fecha_vencimiento date DEFAULT ('now'::text)::date,
    persona_pago text DEFAULT ''::text,
    domicilio_pago text DEFAULT ''::text,
    cuenta_origen_id integer,
    nombre_librado text DEFAULT ''::text,
    direccion_librado text DEFAULT ''::text,
    observaciones text DEFAULT ''::text,
    cuenta_bancaria_cliente_id integer
);


ALTER TABLE public.recibo OWNER TO pilates;

--
-- Name: recibo_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE recibo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.recibo_id_seq OWNER TO pilates;

--
-- Name: recibo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE recibo_id_seq OWNED BY recibo.id;


--
-- Name: recibo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('recibo_id_seq', 3, true);


--
-- Name: servicio; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE servicio (
    id integer NOT NULL,
    factura_venta_id integer,
    prefactura_id integer,
    albaran_salida_id integer,
    concepto text,
    cantidad double precision DEFAULT 1.0,
    precio double precision,
    descuento double precision DEFAULT 0.0,
    pedido_venta_id integer,
    presupuesto_id integer,
    notas text DEFAULT ''::text,
    actividad_id integer
);


ALTER TABLE public.servicio OWNER TO pilates;

--
-- Name: servicio_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE servicio_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.servicio_id_seq OWNER TO pilates;

--
-- Name: servicio_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE servicio_id_seq OWNED BY servicio.id;


--
-- Name: servicio_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('servicio_id_seq', 219, true);


--
-- Name: servicio_tomado; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE servicio_tomado (
    id integer NOT NULL,
    factura_compra_id integer,
    concepto text DEFAULT ''::text,
    cantidad double precision DEFAULT 0.0,
    precio double precision DEFAULT 0.0,
    descuento double precision DEFAULT 0.0,
    transporte_a_cuenta_id integer,
    iva double precision DEFAULT 0.18
);


ALTER TABLE public.servicio_tomado OWNER TO pilates;

--
-- Name: servicio_tomado_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE servicio_tomado_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.servicio_tomado_id_seq OWNER TO pilates;

--
-- Name: servicio_tomado_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE servicio_tomado_id_seq OWNED BY servicio_tomado.id;


--
-- Name: servicio_tomado_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('servicio_tomado_id_seq', 1, false);


--
-- Name: stock_almacen; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE stock_almacen (
    id integer NOT NULL,
    almacen_id integer,
    producto_compra_id integer,
    existencias double precision DEFAULT 0.0
);


ALTER TABLE public.stock_almacen OWNER TO pilates;

--
-- Name: stock_almacen_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE stock_almacen_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.stock_almacen_id_seq OWNER TO pilates;

--
-- Name: stock_almacen_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE stock_almacen_id_seq OWNED BY stock_almacen.id;


--
-- Name: stock_almacen_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('stock_almacen_id_seq', 7, true);


--
-- Name: tarea; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE tarea (
    id integer NOT NULL,
    categoria_id integer,
    resumen text DEFAULT ''::text,
    texto text DEFAULT ''::text,
    fecha_limite date,
    fecha_done date,
    fechahora timestamp without time zone DEFAULT now()
);


ALTER TABLE public.tarea OWNER TO pilates;

--
-- Name: tarea_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE tarea_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.tarea_id_seq OWNER TO pilates;

--
-- Name: tarea_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE tarea_id_seq OWNED BY tarea.id;


--
-- Name: tarea_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('tarea_id_seq', 5, true);


--
-- Name: tarifa; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE tarifa (
    id integer NOT NULL,
    nombre text,
    observaciones text DEFAULT ''::text,
    periodo_validez_ini date,
    periodo_validez_fin date
);


ALTER TABLE public.tarifa OWNER TO pilates;

--
-- Name: tarifa_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE tarifa_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.tarifa_id_seq OWNER TO pilates;

--
-- Name: tarifa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE tarifa_id_seq OWNED BY tarifa.id;


--
-- Name: tarifa_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('tarifa_id_seq', 1, true);


--
-- Name: ticket; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE ticket (
    id integer NOT NULL,
    fechahora timestamp without time zone DEFAULT now(),
    numticket bigint DEFAULT ultimo_ticket_mas_uno()
);


ALTER TABLE public.ticket OWNER TO pilates;

--
-- Name: ticket_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE ticket_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.ticket_id_seq OWNER TO pilates;

--
-- Name: ticket_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE ticket_id_seq OWNED BY ticket.id;


--
-- Name: ticket_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('ticket_id_seq', 9, true);


--
-- Name: tipo_de_material; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE tipo_de_material (
    id integer NOT NULL,
    descripcion text
);


ALTER TABLE public.tipo_de_material OWNER TO pilates;

--
-- Name: tipo_de_material_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE tipo_de_material_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.tipo_de_material_id_seq OWNER TO pilates;

--
-- Name: tipo_de_material_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE tipo_de_material_id_seq OWNED BY tipo_de_material.id;


--
-- Name: tipo_de_material_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('tipo_de_material_id_seq', 5, true);


--
-- Name: transporte_a_cuenta; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE transporte_a_cuenta (
    id integer NOT NULL,
    concepto text DEFAULT ''::text,
    precio double precision DEFAULT 0.0,
    observaciones text DEFAULT ''::text,
    fecha date DEFAULT ('now'::text)::date,
    albaran_salida_id integer,
    proveedor_id integer
);


ALTER TABLE public.transporte_a_cuenta OWNER TO pilates;

--
-- Name: transporte_a_cuenta_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE transporte_a_cuenta_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.transporte_a_cuenta_id_seq OWNER TO pilates;

--
-- Name: transporte_a_cuenta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE transporte_a_cuenta_id_seq OWNED BY transporte_a_cuenta.id;


--
-- Name: transporte_a_cuenta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('transporte_a_cuenta_id_seq', 1, false);


--
-- Name: transportista; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE transportista (
    id integer NOT NULL,
    agencia text DEFAULT ''::text,
    nombre text DEFAULT ''::text,
    dni text,
    telefono text DEFAULT ''::text,
    matricula text DEFAULT ''::text
);


ALTER TABLE public.transportista OWNER TO pilates;

--
-- Name: transportista_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE transportista_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.transportista_id_seq OWNER TO pilates;

--
-- Name: transportista_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE transportista_id_seq OWNED BY transportista.id;


--
-- Name: transportista_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('transportista_id_seq', 1, true);


--
-- Name: turno; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE turno (
    id integer NOT NULL,
    nombre text,
    horainicio timestamp without time zone,
    horafin timestamp without time zone,
    noche boolean DEFAULT false,
    observaciones text DEFAULT ''::text,
    recuperacion boolean DEFAULT false
);


ALTER TABLE public.turno OWNER TO pilates;

--
-- Name: turno_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE turno_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.turno_id_seq OWNER TO pilates;

--
-- Name: turno_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE turno_id_seq OWNED BY turno.id;


--
-- Name: turno_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('turno_id_seq', 1, false);


--
-- Name: usuario; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE usuario (
    id integer NOT NULL,
    usuario character varying(16) NOT NULL,
    passwd character(32) NOT NULL,
    nombre text DEFAULT ''::text,
    cuenta text DEFAULT ''::text,
    cpass text DEFAULT ''::text,
    nivel integer DEFAULT 5,
    email text DEFAULT ''::text,
    smtpserver text DEFAULT ''::text,
    smtpuser text DEFAULT ''::text,
    smtppassword text DEFAULT ''::text,
    firma_total boolean DEFAULT false,
    firma_comercial boolean DEFAULT false,
    firma_director boolean DEFAULT false,
    firma_tecnico boolean DEFAULT false,
    firma_usuario boolean DEFAULT false,
    observaciones text DEFAULT ''::text,
    CONSTRAINT usuario_usuario_check CHECK (((usuario)::text <> ''::text))
);


ALTER TABLE public.usuario OWNER TO pilates;

--
-- Name: usuario_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE usuario_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.usuario_id_seq OWNER TO pilates;

--
-- Name: usuario_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE usuario_id_seq OWNED BY usuario.id;


--
-- Name: usuario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('usuario_id_seq', 1, true);


--
-- Name: vacaciones; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE vacaciones (
    id integer NOT NULL,
    calendario_laboral_id integer,
    fecha date DEFAULT ('now'::text)::date
);


ALTER TABLE public.vacaciones OWNER TO pilates;

--
-- Name: vacaciones_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE vacaciones_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.vacaciones_id_seq OWNER TO pilates;

--
-- Name: vacaciones_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE vacaciones_id_seq OWNED BY vacaciones.id;


--
-- Name: vacaciones_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('vacaciones_id_seq', 1, false);


--
-- Name: vencimiento_cobro; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE vencimiento_cobro (
    id integer NOT NULL,
    factura_venta_id integer,
    prefactura_id integer,
    fecha date DEFAULT ('now'::text)::date,
    importe double precision DEFAULT 0.0,
    observaciones text DEFAULT ''::text,
    cuenta_origen_id integer,
    recibo_id integer
);


ALTER TABLE public.vencimiento_cobro OWNER TO pilates;

--
-- Name: vencimiento_cobro_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE vencimiento_cobro_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.vencimiento_cobro_id_seq OWNER TO pilates;

--
-- Name: vencimiento_cobro_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE vencimiento_cobro_id_seq OWNED BY vencimiento_cobro.id;


--
-- Name: vencimiento_cobro_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('vencimiento_cobro_id_seq', 13, true);


--
-- Name: vencimiento_pago; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE vencimiento_pago (
    id integer NOT NULL,
    factura_compra_id integer,
    fecha date DEFAULT ('now'::text)::date,
    importe double precision DEFAULT 0.0,
    observaciones text DEFAULT ''::text
);


ALTER TABLE public.vencimiento_pago OWNER TO pilates;

--
-- Name: vencimiento_pago_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE vencimiento_pago_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.vencimiento_pago_id_seq OWNER TO pilates;

--
-- Name: vencimiento_pago_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE vencimiento_pago_id_seq OWNED BY vencimiento_pago.id;


--
-- Name: vencimiento_pago_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('vencimiento_pago_id_seq', 1, true);


--
-- Name: ventana; Type: TABLE; Schema: public; Owner: pilates; Tablespace: 
--

CREATE TABLE ventana (
    id integer NOT NULL,
    modulo_id integer,
    descripcion text,
    fichero text,
    clase text,
    icono text DEFAULT ''::text
);


ALTER TABLE public.ventana OWNER TO pilates;

--
-- Name: ventana_id_seq; Type: SEQUENCE; Schema: public; Owner: pilates
--

CREATE SEQUENCE ventana_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.ventana_id_seq OWNER TO pilates;

--
-- Name: ventana_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pilates
--

ALTER SEQUENCE ventana_id_seq OWNED BY ventana.id;


--
-- Name: ventana_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('ventana_id_seq', 227, true);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE abono ALTER COLUMN id SET DEFAULT nextval('abono_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE actividad ALTER COLUMN id SET DEFAULT nextval('actividad_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE albaran_de_entrada_de_abono ALTER COLUMN id SET DEFAULT nextval('albaran_de_entrada_de_abono_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE albaran_entrada ALTER COLUMN id SET DEFAULT nextval('albaran_entrada_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE albaran_salida ALTER COLUMN id SET DEFAULT nextval('albaran_salida_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE alerta ALTER COLUMN id SET DEFAULT nextval('alerta_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE almacen ALTER COLUMN id SET DEFAULT nextval('almacen_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: bogado
--

ALTER TABLE asistencia ALTER COLUMN id SET DEFAULT nextval('asistencia_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE ausencia ALTER COLUMN id SET DEFAULT nextval('ausencia_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE baja ALTER COLUMN id SET DEFAULT nextval('baja_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE calendario_laboral ALTER COLUMN id SET DEFAULT nextval('calendario_laboral_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE categoria ALTER COLUMN id SET DEFAULT nextval('categoria_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE categoria_laboral ALTER COLUMN id SET DEFAULT nextval('categoria_laboral_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE centro_trabajo ALTER COLUMN id SET DEFAULT nextval('centro_trabajo_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE cliente ALTER COLUMN id SET DEFAULT nextval('cliente_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE cobro ALTER COLUMN id SET DEFAULT nextval('cobro_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE confirming ALTER COLUMN id SET DEFAULT nextval('confirming_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE contador ALTER COLUMN id SET DEFAULT nextval('contador_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE cuenta_bancaria_cliente ALTER COLUMN id SET DEFAULT nextval('cuenta_bancaria_cliente_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE cuenta_destino ALTER COLUMN id SET DEFAULT nextval('cuenta_destino_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE cuenta_origen ALTER COLUMN id SET DEFAULT nextval('cuenta_origen_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE datos_de_la_empresa ALTER COLUMN id SET DEFAULT nextval('datos_de_la_empresa_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE destino ALTER COLUMN id SET DEFAULT nextval('destino_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE documento ALTER COLUMN id SET DEFAULT nextval('documento_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE empleado ALTER COLUMN id SET DEFAULT nextval('empleado_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE estadistica ALTER COLUMN id SET DEFAULT nextval('estadistica_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE evento ALTER COLUMN id SET DEFAULT nextval('evento_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE factura_compra ALTER COLUMN id SET DEFAULT nextval('factura_compra_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE factura_de_abono ALTER COLUMN id SET DEFAULT nextval('factura_de_abono_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE factura_venta ALTER COLUMN id SET DEFAULT nextval('factura_venta_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE festivo ALTER COLUMN id SET DEFAULT nextval('festivo_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE festivo_generico ALTER COLUMN id SET DEFAULT nextval('festivo_generico_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE grupo ALTER COLUMN id SET DEFAULT nextval('grupo_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE grupo_alumnos ALTER COLUMN id SET DEFAULT nextval('grupo_alumnos_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE historial_existencias_compra ALTER COLUMN id SET DEFAULT nextval('historial_existencias_compra_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE id_reciente ALTER COLUMN id SET DEFAULT nextval('id_reciente_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE laborable ALTER COLUMN id SET DEFAULT nextval('laborable_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE linea_de_abono ALTER COLUMN id SET DEFAULT nextval('linea_de_abono_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE linea_de_compra ALTER COLUMN id SET DEFAULT nextval('linea_de_compra_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE linea_de_devolucion ALTER COLUMN id SET DEFAULT nextval('linea_de_devolucion_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE linea_de_pedido ALTER COLUMN id SET DEFAULT nextval('linea_de_pedido_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE linea_de_pedido_de_compra ALTER COLUMN id SET DEFAULT nextval('linea_de_pedido_de_compra_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE linea_de_venta ALTER COLUMN id SET DEFAULT nextval('linea_de_venta_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE lista_objetos_recientes ALTER COLUMN id SET DEFAULT nextval('lista_objetos_recientes_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE memo ALTER COLUMN id SET DEFAULT nextval('memo_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE modulo ALTER COLUMN id SET DEFAULT nextval('modulo_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE motivo ALTER COLUMN id SET DEFAULT nextval('motivo_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE nomina ALTER COLUMN id SET DEFAULT nextval('nomina_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE nota ALTER COLUMN id SET DEFAULT nextval('nota_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE observaciones_nominas ALTER COLUMN id SET DEFAULT nextval('observaciones_nominas_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE orden_empleados ALTER COLUMN id SET DEFAULT nextval('orden_empleados_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE padecimiento ALTER COLUMN id SET DEFAULT nextval('padecimiento_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE pagare_cobro ALTER COLUMN id SET DEFAULT nextval('pagare_cobro_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE pagare_pago ALTER COLUMN id SET DEFAULT nextval('pagare_pago_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE pago ALTER COLUMN id SET DEFAULT nextval('pago_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE pago_de_abono ALTER COLUMN id SET DEFAULT nextval('pago_de_abono_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE pedido_compra ALTER COLUMN id SET DEFAULT nextval('pedido_compra_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE pedido_venta ALTER COLUMN id SET DEFAULT nextval('pedido_venta_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE permiso ALTER COLUMN id SET DEFAULT nextval('permiso_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE precio ALTER COLUMN id SET DEFAULT nextval('precio_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE prefactura ALTER COLUMN id SET DEFAULT nextval('prefactura_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE presupuesto ALTER COLUMN id SET DEFAULT nextval('presupuesto_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE producto_compra ALTER COLUMN id SET DEFAULT nextval('producto_compra_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE proveedor ALTER COLUMN id SET DEFAULT nextval('proveedor_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE recibo ALTER COLUMN id SET DEFAULT nextval('recibo_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE servicio ALTER COLUMN id SET DEFAULT nextval('servicio_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE servicio_tomado ALTER COLUMN id SET DEFAULT nextval('servicio_tomado_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE stock_almacen ALTER COLUMN id SET DEFAULT nextval('stock_almacen_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE tarea ALTER COLUMN id SET DEFAULT nextval('tarea_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE tarifa ALTER COLUMN id SET DEFAULT nextval('tarifa_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE ticket ALTER COLUMN id SET DEFAULT nextval('ticket_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE tipo_de_material ALTER COLUMN id SET DEFAULT nextval('tipo_de_material_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE transporte_a_cuenta ALTER COLUMN id SET DEFAULT nextval('transporte_a_cuenta_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE transportista ALTER COLUMN id SET DEFAULT nextval('transportista_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE turno ALTER COLUMN id SET DEFAULT nextval('turno_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE usuario ALTER COLUMN id SET DEFAULT nextval('usuario_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE vacaciones ALTER COLUMN id SET DEFAULT nextval('vacaciones_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE vencimiento_cobro ALTER COLUMN id SET DEFAULT nextval('vencimiento_cobro_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE vencimiento_pago ALTER COLUMN id SET DEFAULT nextval('vencimiento_pago_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pilates
--

ALTER TABLE ventana ALTER COLUMN id SET DEFAULT nextval('ventana_id_seq'::regclass);


--
-- Data for Name: abono; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY abono (id, cliente_id, factura_de_abono_id, numabono, fecha, observaciones, almacen_id) FROM stdin;
1	2	\N	A00001	2010-02-21		1
\.


--
-- Data for Name: actividad; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY actividad (id, evento_id, grupo_alumnos_id, fechahora_inicio, fechahora_fin, descripcion) FROM stdin;
21	\N	6	2010-02-19 12:30:00	2010-02-19 13:30:00	Power Plate
22	\N	6	2010-02-21 12:30:00	2010-02-21 13:30:00	Power Plate
24	\N	6	2010-02-25 12:30:00	2010-02-25 13:30:00	Power Plate
19	\N	6	2010-02-15 12:30:00	2010-02-15 13:30:00	Power Plate (iniciación)
20	\N	6	2010-02-17 12:30:00	2010-02-17 13:00:00	Power Plate
2	\N	5	2010-02-10 12:25:00	2010-02-10 12:25:00	Calentamiento
27	\N	6	2010-02-19 16:30:00	2010-02-19 17:30:00	Power Plate 2
28	\N	6	2010-02-22 16:30:00	2010-02-22 17:30:00	Power Plate 2
26	\N	6	2010-02-16 16:30:00	2010-02-16 17:30:00	Power Plate 2 (primera clase)
3	\N	3	2010-02-11 13:31:00	2010-02-11 14:31:00	Rehabilitación clase 1
6	\N	3	2010-02-14 13:31:00	2010-02-14 14:31:00	Rehabilitación (refuerzo)
5	\N	3	2010-02-13 13:31:00	2010-02-13 14:50:00	Rehabilitación clase 3
7	\N	3	2010-02-15 13:31:00	2010-02-15 14:31:00	Rehabilitación (clase 4)
8	\N	3	2010-02-16 13:31:00	2010-02-16 14:31:00	Rehabilitación (clase 5)
9	\N	3	2010-02-17 13:31:00	2010-02-17 14:31:00	Rehabilitación (clase 1)
11	\N	3	2010-02-19 13:31:00	2010-02-19 14:31:00	Rehabilitación (relajación)
12	\N	3	2010-02-20 13:31:00	2010-02-20 14:31:00	Rehabilitación (clase 3)
14	\N	3	2010-02-22 13:31:00	2010-02-22 14:31:00	Rehabilitación (clase 1)
15	\N	3	2010-02-23 13:31:00	2010-02-23 14:31:00	Rehabilitación (clase 2)
16	\N	3	2010-02-24 13:31:00	2010-02-24 14:31:00	Rehabilitación (clase 3)
10	\N	3	2010-02-18 13:31:00	2010-02-18 14:31:00	Rehabilitación (clase 2)
25	1	6	2010-02-28 10:00:00	2010-02-28 14:00:00	Puertas abiertas Día de Andalucía
\.


--
-- Data for Name: albaran_de_entrada_de_abono; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY albaran_de_entrada_de_abono (id, numalbaran, fecha, observaciones) FROM stdin;
\.


--
-- Data for Name: albaran_entrada; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY albaran_entrada (id, proveedor_id, fecha, numalbaran, bloqueado, repuestos, almacen_id, transportista_id) FROM stdin;
1	\N	2010-02-12	ALB_EXT_1	f	f	1	\N
2	2	2010-02-15	ALB_EXT_2	f	f	1	\N
\.


--
-- Data for Name: albaran_salida; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY albaran_salida (id, numalbaran, transportista_id, cliente_id, fecha, nombre, direccion, cp, ciudad, telefono, pais, observaciones, facturable, motivo, bloqueado, destino_id, almacen_origen_id, almacen_destino_id) FROM stdin;
1	0	\N	1	2010-02-20								t		f	\N	\N	\N
2	1	\N	2	2010-02-21								t		t	\N	1	\N
3	2	1	4	2010-02-21								t		f	1	1	2
\.


--
-- Data for Name: alerta; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY alerta (id, usuario_id, mensaje, fechahora, entregado) FROM stdin;
\.


--
-- Data for Name: almacen; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY almacen (id, nombre, observaciones, direccion, ciudad, provincia, cp, telefono, fax, email, pais, principal) FROM stdin;
1	Almacén principal de Vitality Studio			Marbella						España	t
2	Almacén de distribución				Sevilla					España	f
\.


--
-- Data for Name: asistencia; Type: TABLE DATA; Schema: public; Owner: bogado
--

COPY asistencia (id, cliente_id, actividad_id, fechahora, observaciones) FROM stdin;
33	1	10	2010-02-18 18:04:58	
34	10	10	2010-02-18 18:04:58	
35	5	10	2010-02-18 18:04:58	
36	7	10	2010-02-18 18:04:58	
37	1	11	2010-02-19 11:00:28	
38	9	11	2010-02-19 11:00:29	
39	10	11	2010-02-19 11:00:29	
40	5	11	2010-02-19 11:00:35	
41	7	11	2010-02-19 11:00:35	
42	1	16	2010-02-25 19:17:03	
43	9	16	2010-02-25 19:17:03	
44	10	16	2010-02-25 19:17:03	
45	5	16	2010-02-25 19:17:03	
46	7	16	2010-02-25 19:17:03	
\.


--
-- Data for Name: ausencia; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY ausencia (id, empleado_id, motivo_id, fecha, observaciones) FROM stdin;
\.


--
-- Data for Name: baja; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY baja (id, empleado_id, motivo, fecha_inicio, fecha_fin, observaciones) FROM stdin;
\.


--
-- Data for Name: calendario_laboral; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY calendario_laboral (id, mes_anno, observaciones) FROM stdin;
\.


--
-- Data for Name: categoria; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY categoria (id, nombre, color_r, color_g, color_b) FROM stdin;
1		255	255	255
2	Categoría 1	255	255	255
\.


--
-- Data for Name: categoria_laboral; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY categoria_laboral (id, codigo, puesto, planta, precio_hora_extra, precio_hora_nocturnidad, precio_plus_nocturnidad, precio_plus_turnicidad, precio_plus_jefe_turno, precio_plus_festivo, precio_plus_mantenimiento_sabados, dias_vacaciones, dias_convenio, dias_asuntos_propios, salario_base, precio_hora_regular, da_clases) FROM stdin;
1	PPN1	Profesor Pilates nivel 1	t	8.2599999999999998	9.5800000000000001	10.57	100	104	11	11	36	2	2	0	0	t
4	PPN2	Profesor Pilates nivel 2	t	8.2599999999999998	9.5800000000000001	10.57	100	104	11	11	36	2	2	0	0	t
3	SLS	Tienda	t	8.2599999999999998	9.5800000000000001	10.57	100	104	11	11	36	2	2	0	0	f
2	ADM	Administrativo	t	8.2599999999999998	9.5800000000000001	10.57	100	104	11	11	36	2	2	0	0	f
\.


--
-- Data for Name: centro_trabajo; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY centro_trabajo (id, nombre, almacen_id) FROM stdin;
\.


--
-- Data for Name: cliente; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY cliente (id, tarifa_id, contador_id, telefono, nombre, cif, direccion, pais, ciudad, provincia, cp, iva, direccionfacturacion, paisfacturacion, ciudadfacturacion, provinciafacturacion, cpfacturacion, nombref, email, contacto, observaciones, vencimientos, formadepago, documentodepago, diadepago, inhabilitado, motivo, cliente_id, porcentaje, enviar_correo_albaran, enviar_correo_factura, enviar_correo_packing, fax, proveedor_id, cuenta_origen_id, riesgo_asegurado, riesgo_concedido, packing_list_con_codigo, facturar_con_albaran, copias_factura) FROM stdin;
1	\N	1		Cliente 1	PENDIENTE						0.18										180 D.F.F.	180 D.F.F.	PAGARÉ	25	f		\N	0	f	f	f		\N	\N	-1	-1	f	t	0
9	\N	1		José López Pérez	PENDIENTE		España	Sevilla	Sevilla	C/ calle...	0.18		España	Sevilla	Sevilla	C/ calle...	José López Pérez			Cliente de prueba.	30-60 D.F.F.	30-60 D.F.F.	Recibo domiciliado	25	f		\N	0	f	t	f		\N	\N	-1	1000	f	t	0
5	\N	1		Cliente 5	48908359X						0.18						Cliente 5				180 D.F.F.	180 D.F.F.	PAGARÉ	25	f		\N	0	f	f	f		\N	\N	-1	-1	f	t	0
7	\N	1		Nuevo cliente de prueba	00000000T						0.18		España				Nuevo cliente de prueba				30 D.F.F.	30 D.F.F.	Recibo domiciliado	25	f		\N	0	f	t	f		\N	\N	-1	-1	f	t	0
8	\N	1		Juan Pérez Pérez	00000001V	C/ calle...	España	Sevilla	Sevilla	41010	0.18		España				Juan Pérez Pérez				180 D.F.F.	180 D.F.F.	PAGARÉ	25	f		\N	0	f	f	f		\N	\N	-1	-1	f	t	0
2	\N	1		Cliente 2	00000000T						0.18						Cliente 2	echo@rediris.es			30	30	RECIBO DOMICILIADO	25	f		\N	0	f	t	f		\N	\N	-1	100	f	t	0
3	\N	1		Fulanito de tal	00000000-T		España	Huelva	Huelva		0.18		España	Huelva	Huelva		Fulanito de tal			Creado desde el TPV.	0	0			f		\N	0	f	f	f		\N	\N	-1	-1	f	t	0
4	\N	1		Menganito	12345678-X		España	Sevilla	Sevilla		0.18		España	Sevilla	Sevilla		Menganito			Creado desde el TPV.	0	0			f		\N	0	f	f	f		\N	\N	-1	-1	f	t	0
6	\N	1		Cliente de prueba	00000000T		España	Sevilla	Sevilla	40010	0.18						Cliente de prueba				0 DFF	0 DFF	RECIBO DOMICILIADO		f		\N	0	f	t	f		\N	\N	-1	-1	f	t	0
10	\N	1		Felipe Márquez	48484848Z		España	Huelva	Huelva		0.18		España	Huelva	Huelva		Felipe Márquez			Creado desde el TPV.	0	0			f		\N	0	f	f	f		\N	\N	-1	-1	f	t	0
11	\N	\N		Universal Pilates Vitality Studio	PENDIENTE						0.18										180 D.F.F.	180 D.F.F.	PAGARÉ	25	f		\N	0	f	f	f		\N	\N	-1	-1	f	t	0
\.


--
-- Data for Name: cliente_grupo_alumnos; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY cliente_grupo_alumnos (cliente_id, grupo_alumnos_id) FROM stdin;
2	1
1	5
2	5
1	6
5	6
9	6
1	3
9	3
10	3
5	3
7	3
8	3
\.


--
-- Data for Name: cobro; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY cobro (id, factura_venta_id, prefactura_id, fecha, importe, observaciones, pagare_cobro_id, cliente_id, factura_de_abono_id, confirming_id) FROM stdin;
1	5	\N	2010-03-25	12.199999999999999	Cobrado al facturar desde TPV.	\N	\N	\N	\N
2	6	\N	2010-02-12	-58	Cobrado al facturar desde TPV.	\N	\N	\N	\N
3	7	\N	2010-02-15	185.59999999999999	Cobrado al facturar desde TPV.	\N	\N	\N	\N
5	29	\N	2010-02-21	71.920000000000002		\N	\N	\N	\N
4	8	\N	2010-02-22	145	Pagaré 1234 con fecha 21/02/2010 y vencimiento 21/02/2010	1	\N	\N	\N
\.


--
-- Data for Name: confirming; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY confirming (id, codigo, fecha_recepcion, fecha_cobro, cantidad, cobrado, observaciones, fecha_cobrado, procesado) FROM stdin;
\.


--
-- Data for Name: contador; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY contador (id, prefijo, sufijo, contador) FROM stdin;
1	F	/2010	22
\.


--
-- Data for Name: cuenta_bancaria_cliente; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY cuenta_bancaria_cliente (id, cliente_id, observaciones, banco, swif, iban, cuenta) FROM stdin;
1	2		Caja Rural del Sur			12345678901234567890
2	7		Caja Rural			
\.


--
-- Data for Name: cuenta_destino; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY cuenta_destino (id, nombre, observaciones, banco, swif, iban, cuenta, nombre_banco, proveedor_id) FROM stdin;
1	Tal	tal	Cual	ss	ss	sss	ss	1
2	Nueva cuenta de PilatesProv		YYYY	1234	5678	2345	8901	2
\.


--
-- Data for Name: cuenta_origen; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY cuenta_origen (id, nombre, banco, ccc, observaciones, contacto, fax, telefono) FROM stdin;
1	Tal	Cual	xx	sñkjdaj	x	x	xxxx
2	Cuenta principal	Caja Granada	20310188910115928707				
\.


--
-- Data for Name: datos_de_la_empresa; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY datos_de_la_empresa (id, nombre, cif, dirfacturacion, cpfacturacion, ciudadfacturacion, provinciafacturacion, direccion, cp, ciudad, provincia, telefono, fax, email, paisfacturacion, pais, telefonofacturacion, faxfacturacion, nombre_responsable_compras, telefono_responsable_compras, nombre_contacto, registro_mercantil, email_responsable_compras, logo, logo2, bvqi, nomalbaran2, diralbaran2, cpalbaran2, ciualbaran2, proalbaran2, telalbaran2, faxalbaran2, regalbaran2, irpf, es_sociedad, logoiso1, logoiso2, recargo_equivalencia, iva, ped_compra_texto_fijo, ped_compra_texto_editable, ped_compra_texto_editable_con_nivel1) FROM stdin;
3	Universal Pilates Vitality Studio	T-00.000.000	C/ Dirección de facturación	00000	Málaga	Málaga	C/ Dirección postal	00000	Marbella	Marbella	034 000 00 00 00	034 000 00 00 00	javier@universalpilates.es	España	España	000 000 000 000	000 000 000 000	Responsable De Compras	000 00 00 00	Javier Bseiso	Inscrita en el Registro Mercantil ...	resposable@compras.com	logo_up.jpg		f	NOMBRE ALTERNATIVO ALBARÁN	Dirección albarán	00000	Málaga	Marbella	00 000 00 00	00 000 00 00	CIF T-00000000 Reg.Mec. de ...	0	t			f	0.18	ROGAMOS NOS REMITAN COPIA DE ESTE PEDIDO SELLADO Y FIRMADO POR UDS.	ESTA MERCANCIA SE DEBE ENTREGAR...	PAGO A 120 DÍAS F.F. PAGO LOS 25.
1	Univesal Pilates Vitality Studio	T-00.000.000	C/ Dirección de facturación	00000	Málaga	Málaga	C/ Dirección postal	00000	Marbella	Málaga	034 000 00 00 00	034 000 00 00 00	javier@universalpilates.es	España	España	000 000 000 000	000 000 000 000	Javier Bseiso	000 00 00 00	Javier Bseiso	Inscrita en el Registro Mercantil ...	compras@universalpilates.es	logo_up.jpg		f	Universal Pilates Vitality Studio	Dirección albarán	00000	Marbella	Málaga	00 000 00 00	00 000 00 00	CIF T-00000000 Reg.Mec. de ...	0	t			f	0.18	ROGAMOS NOS REMITAN COPIA DE ESTE PEDIDO SELLADO Y FIRMADO POR UDS.	ESTA MERCANCIA SE DEBE ENTREGAR...	PAGO A 120 DÍAS F.F. PAGO LOS 25.
2	Empresa	T-00.000.000	C/ Dirección de facturación	00000	Ciudad	Provincia	C/ Dirección postal	00000	Ciudad	Provincia	034 000 00 00 00	034 000 00 00 00	correo@electronico.com	España	España	000 000 000 000	000 000 000 000	Responsable De Compras	000 00 00 00	Nombre Contacto	Inscrita en el Registro Mercantil ...	resposable@compras.com	logo_up.jpg	logo_up.gif	t	NOMBRE ALTERNATIVO ALBARÁN	Dirección albarán	00000	Ciudad	Provincia	00 000 00 00	00 000 00 00	CIF T-00000000 Reg.Mec. de ...	0	t	bvqi.gif	bvqi2.png	f	0.18	ROGAMOS NOS REMITAN COPIA DE ESTE PEDIDO SELLADO Y FIRMADO POR UDS.	ESTA MERCANCIA SE DEBE ENTREGAR...	PAGO A 120 DÍAS F.F. PAGO LOS 25.
4	Universal Pilates Vitality Studio	T-00.000.000	C/ Dirección de facturación	00000	Ciudad	Provincia	C/ Dirección postal	00000	Ciudad	Provincia	034 000 00 00 00	034 000 00 00 00	correo@electronico.com	España	España	000 000 000 000	000 000 000 000	Responsable De Compras	000 00 00 00	Nombre Contacto	Inscrita en el Registro Mercantil ...	resposable@compras.com	logo-inn.png		t	NOMBRE ALTERNATIVO ALBARÁN	Dirección albarán	00000	Ciudad	Provincia	00 000 00 00	00 000 00 00	CIF T-00000000 Reg.Mec. de ...	0	t	bvqi.gif	bvqi2.png	f	0.18	ROGAMOS NOS REMITAN COPIA DE ESTE PEDIDO SELLADO Y FIRMADO POR UDS.	ESTA MERCANCIA SE DEBE ENTREGAR...	PAGO A 120 DÍAS F.F. PAGO LOS 25.
5	Empresa	T-00.000.000	C/ Dirección de facturación	00000	Ciudad	Provincia	C/ Dirección postal	00000	Ciudad	Provincia	034 000 00 00 00	034 000 00 00 00	correo@electronico.com	España	España	000 000 000 000	000 000 000 000	Responsable De Compras	000 00 00 00	Nombre Contacto	Inscrita en el Registro Mercantil ...	resposable@compras.com	logo-inn.png		t	NOMBRE ALTERNATIVO ALBARÁN	Dirección albarán	00000	Ciudad	Provincia	00 000 00 00	00 000 00 00	CIF T-00000000 Reg.Mec. de ...	0	t	bvqi.gif	bvqi2.png	f	0.18	ROGAMOS NOS REMITAN COPIA DE ESTE PEDIDO SELLADO Y FIRMADO POR UDS.	ESTA MERCANCIA SE DEBE ENTREGAR...	PAGO A 120 DÍAS F.F. PAGO LOS 25.
\.


--
-- Data for Name: destino; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY destino (id, nombre, direccion, cp, ciudad, telefono, pais) FROM stdin;
1						
\.


--
-- Data for Name: documento; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY documento (id, nombre, nombre_fichero, observaciones, pedido_venta_id, albaran_salida_id, factura_venta_id, prefactura_id, pagare_cobro_id, pedido_compra_id, albaran_entrada_id, factura_compra_id, pagare_pago_id, empleado_id, cliente_id, proveedor_id, confirming_id) FROM stdin;
1	Factura escaneada (original)	factura_escaneada.pdf	Prueba. El contenido no es realmente una factura.	\N	\N	\N	\N	\N	\N	\N	2	\N	\N	\N	\N	\N
\.


--
-- Data for Name: empleado; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY empleado (id, categoria_laboral_id, centro_trabajo_id, nombre, apellidos, dni, planta, nomina, preciohora, activo, usuario_id) FROM stdin;
2	4	\N	José	Hierro	00000001-V	t	0.00	0.00	t	\N
4	2	\N	Federico	García Lorca		t	0.00	0.00	t	\N
1	1	\N	Juan Ramón	Jiménez	00000000-T	t	0.00	0.00	t	\N
3	3	\N	Gustavo Adolfo	Bécquer		t	0.00	0.00	t	\N
\.


--
-- Data for Name: estadistica; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY estadistica (id, usuario_id, ventana_id, veces, ultima_vez) FROM stdin;
12	1	90	3	2010-02-21 16:42:04
3	1	102	1	2010-02-12 18:22:50
4	1	88	1	2010-02-12 18:23:06
23	1	74	4	2010-02-21 15:17:26
27	1	89	2	2010-02-21 16:42:11
9	1	40	4	2010-02-21 16:47:26
2	1	27	7	2010-02-12 18:27:59
39	1	44	3	2010-02-21 15:24:25
54	1	73	1	2010-02-21 16:47:39
13	1	2	2	2010-02-15 16:51:15
55	1	30	1	2010-02-21 16:47:44
41	1	223	1	2010-02-21 15:25:54
8	1	4	4	2010-02-21 15:26:05
29	1	3	1	2010-02-21 14:31:16
10	1	29	2	2010-02-15 16:17:03
6	1	35	5	2010-02-21 16:48:52
42	1	6	1	2010-02-21 15:26:10
43	1	108	1	2010-02-21 15:26:15
40	1	224	2	2010-02-22 13:31:08
32	1	104	1	2010-02-21 14:42:30
44	1	5	2	2010-02-21 15:43:01
45	1	7	1	2010-02-21 15:53:36
16	1	1	4	2010-02-21 14:47:55
46	1	53	1	2010-02-21 15:54:56
19	1	106	2	2010-02-21 14:48:01
35	1	94	1	2010-02-21 14:48:08
47	1	54	1	2010-02-21 15:55:01
28	1	226	2	2010-02-21 14:48:53
21	1	112	2	2010-02-21 14:49:06
17	1	56	2	2010-02-21 15:55:05
36	1	105	1	2010-02-21 14:49:14
37	1	113	1	2010-02-21 14:54:05
48	1	57	1	2010-02-21 15:56:31
34	1	225	2	2010-02-22 18:01:38
11	1	11	2	2010-02-21 15:00:27
38	1	12	1	2010-02-21 15:00:32
31	1	103	3	2010-02-22 18:17:02
49	1	58	2	2010-02-21 15:57:26
33	1	69	2	2010-02-22 18:24:49
50	1	59	2	2010-02-21 15:58:55
30	1	87	2	2010-02-22 18:25:04
25	1	38	4	2010-02-21 15:59:17
15	1	101	3	2010-02-21 16:28:40
53	1	72	3	2010-02-22 18:27:48
5	1	36	3	2010-02-22 18:28:46
52	1	41	3	2010-02-22 18:37:18
18	1	43	5	2010-02-22 18:37:28
56	1	227	3	2010-02-25 20:26:49
20	1	110	7	2010-02-26 16:20:48
14	1	111	3	2010-02-21 16:41:30
51	1	39	2	2010-02-21 16:41:38
1	1	221	8	2010-02-26 16:21:35
26	1	42	6	2010-02-21 16:41:50
22	1	68	4	2010-02-26 16:22:23
24	1	98	3	2010-02-26 16:22:35
7	1	33	8	2010-02-26 16:22:52
\.


--
-- Data for Name: evento; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY evento (id, nombre, color_r, color_g, color_b) FROM stdin;
1	Festivos	255	0	0
2	Vacaciones	0	0	200
\.


--
-- Data for Name: factura_compra; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY factura_compra (id, proveedor_id, fecha, numfactura, descuento, cargo, iva, bloqueada, visto_bueno_director, visto_bueno_comercial, visto_bueno_tecnico, fecha_entrada, fecha_visto_bueno_director, fecha_visto_bueno_comercial, fecha_visto_bueno_tecnico, visto_bueno_usuario, fecha_visto_bueno_usuario, observaciones, vencimientos_confirmados) FROM stdin;
2	2	2010-02-15	F_EXT_0001	0	0.00	0.18	f	t	t	t	2010-02-15	2010-02-15	2010-02-15	2010-02-15	t	2010-02-15		t
\.


--
-- Data for Name: factura_de_abono; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY factura_de_abono (id, fecha) FROM stdin;
\.


--
-- Data for Name: factura_venta; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY factura_venta (id, cliente_id, fecha, numfactura, descuento, cargo, observaciones, iva, bloqueada, irpf) FROM stdin;
8	9	2010-02-15	F0008/2010	0	0.00		0.18	t	0
10	2	2010-02-20	F0010/2010	0	0.00		0.18	f	0
11	10	2010-02-20	F0011/2010	0	0.00		0.18	f	0
12	7	2010-02-20	F0012/2010	0	0.00		0.18	f	0
13	1	2010-02-20	F0013/2010	0	0.00		0.18	f	0
14	10	2010-02-20	F0014/2010	0	0.00		0.18	f	0
21	2	2010-02-20	F0015/2010	0	0.00		0.18	f	0
25	9	2010-02-20	F0016/2010	0	0.00		0.18	f	0
26	5	2010-02-20	F0017/2010	0	0.00		0.18	f	0
27	1	2010-02-20	F0018/2010	0	0.00	aifhas lk h	0.18	f	0
1	2	2010-02-12	F0001/2010	0	0.00		0.18	t	0
2	3	2010-02-12	F0002/2010	0	0.00		0.18	f	0
3	4	2010-02-12	F0003/2010	0	0.00		0.18	f	0
4	2	2010-02-12	F0004/2010	0	0.00		0.18	f	0
5	2	2010-02-12	F0005/2010	0	0.00		0.18	t	0
28	2	2010-02-21	F0019/2010	0	0.00		0.18	t	0
6	3	2010-02-12	F0006/2010	0	0.00		0.18	t	0
7	10	2010-02-15	F0007/2010	0	0.00		0.18	t	0
29	4	2010-02-21	F0021/2010	0	0.00		0.18	t	0
9	10	2010-02-20	F0009/2010	0	0.00		0.18	t	0
\.


--
-- Data for Name: festivo; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY festivo (id, calendario_laboral_id, fecha) FROM stdin;
\.


--
-- Data for Name: festivo_generico; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY festivo_generico (id, fecha) FROM stdin;
\.


--
-- Data for Name: grupo; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY grupo (id, nombre, jefeturno_id, operario1_id, operario2_id, observaciones) FROM stdin;
\.


--
-- Data for Name: grupo_alumnos; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY grupo_alumnos (id, nombre, color_r, color_g, color_b, cupo, empleado_id) FROM stdin;
6	Grupo de José	241	130	223	3	4
3	Grupo rehabilitacicón	139	222	211	5	1
2	Grupo de las mañanas (Federico)	128	255	128	0	\N
1	Solo mantenimiento	253	255	255	2	\N
5	Grupo de mayores	233	149	122	1	1
4	Grupo de las tardes	253	255	128	0	\N
\.


--
-- Data for Name: historial_existencias_compra; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY historial_existencias_compra (id, producto_compra_id, fecha, cantidad, observaciones, almacen_id) FROM stdin;
1	3	2009-02-01	-3	Cacheado automáticamente	1
2	3	2009-02-01	0	Cacheado automáticamente	2
3	2	2009-02-01	0	Cacheado automáticamente	1
4	2	2009-02-01	-2	Cacheado automáticamente	2
5	1	2009-02-01	-1	Cacheado automáticamente	1
6	1	2009-02-01	0	Cacheado automáticamente	2
7	3	2009-03-01	-3	Cacheado automáticamente	1
8	3	2009-03-01	0	Cacheado automáticamente	2
9	2	2009-03-01	0	Cacheado automáticamente	1
10	2	2009-03-01	-2	Cacheado automáticamente	2
11	1	2009-03-01	-1	Cacheado automáticamente	1
12	1	2009-03-01	0	Cacheado automáticamente	2
13	3	2009-04-01	-3	Cacheado automáticamente	1
14	3	2009-04-01	0	Cacheado automáticamente	2
15	2	2009-04-01	0	Cacheado automáticamente	1
16	2	2009-04-01	-2	Cacheado automáticamente	2
17	1	2009-04-01	-1	Cacheado automáticamente	1
18	1	2009-04-01	0	Cacheado automáticamente	2
19	3	2009-05-01	-3	Cacheado automáticamente	1
20	3	2009-05-01	0	Cacheado automáticamente	2
21	2	2009-05-01	0	Cacheado automáticamente	1
22	2	2009-05-01	-2	Cacheado automáticamente	2
23	1	2009-05-01	-1	Cacheado automáticamente	1
24	1	2009-05-01	0	Cacheado automáticamente	2
25	3	2009-06-01	-3	Cacheado automáticamente	1
26	3	2009-06-01	0	Cacheado automáticamente	2
27	2	2009-06-01	0	Cacheado automáticamente	1
28	2	2009-06-01	-2	Cacheado automáticamente	2
29	1	2009-06-01	-1	Cacheado automáticamente	1
30	1	2009-06-01	0	Cacheado automáticamente	2
31	3	2009-07-01	-3	Cacheado automáticamente	1
32	3	2009-07-01	0	Cacheado automáticamente	2
33	2	2009-07-01	0	Cacheado automáticamente	1
34	2	2009-07-01	-2	Cacheado automáticamente	2
35	1	2009-07-01	-1	Cacheado automáticamente	1
36	1	2009-07-01	0	Cacheado automáticamente	2
37	3	2009-08-01	-3	Cacheado automáticamente	1
38	3	2009-08-01	0	Cacheado automáticamente	2
39	2	2009-08-01	0	Cacheado automáticamente	1
40	2	2009-08-01	-2	Cacheado automáticamente	2
41	1	2009-08-01	-1	Cacheado automáticamente	1
42	1	2009-08-01	0	Cacheado automáticamente	2
43	3	2009-09-01	-3	Cacheado automáticamente	1
44	3	2009-09-01	0	Cacheado automáticamente	2
45	2	2009-09-01	0	Cacheado automáticamente	1
46	2	2009-09-01	-2	Cacheado automáticamente	2
47	1	2009-09-01	-1	Cacheado automáticamente	1
48	1	2009-09-01	0	Cacheado automáticamente	2
49	3	2009-10-01	-3	Cacheado automáticamente	1
50	3	2009-10-01	0	Cacheado automáticamente	2
51	2	2009-10-01	0	Cacheado automáticamente	1
52	2	2009-10-01	-2	Cacheado automáticamente	2
53	1	2009-10-01	-1	Cacheado automáticamente	1
54	1	2009-10-01	0	Cacheado automáticamente	2
55	3	2009-11-01	-3	Cacheado automáticamente	1
56	3	2009-11-01	0	Cacheado automáticamente	2
57	2	2009-11-01	0	Cacheado automáticamente	1
58	2	2009-11-01	-2	Cacheado automáticamente	2
59	1	2009-11-01	-1	Cacheado automáticamente	1
60	1	2009-11-01	0	Cacheado automáticamente	2
61	3	2009-12-01	-3	Cacheado automáticamente	1
62	3	2009-12-01	0	Cacheado automáticamente	2
63	2	2009-12-01	0	Cacheado automáticamente	1
64	2	2009-12-01	-2	Cacheado automáticamente	2
65	1	2009-12-01	-1	Cacheado automáticamente	1
66	1	2009-12-01	0	Cacheado automáticamente	2
67	3	2010-01-01	-3	Cacheado automáticamente	1
68	3	2010-01-01	0	Cacheado automáticamente	2
69	2	2010-01-01	0	Cacheado automáticamente	1
70	2	2010-01-01	-2	Cacheado automáticamente	2
71	1	2010-01-01	-1	Cacheado automáticamente	1
72	1	2010-01-01	0	Cacheado automáticamente	2
73	3	2010-02-01	-3	Cacheado automáticamente	1
74	3	2010-02-01	0	Cacheado automáticamente	2
75	2	2010-02-01	0	Cacheado automáticamente	1
76	2	2010-02-01	-2	Cacheado automáticamente	2
77	1	2010-02-01	-1	Cacheado automáticamente	1
78	1	2010-02-01	0	Cacheado automáticamente	2
79	4	2010-02-01	0	Cacheado automáticamente	1
80	4	2010-02-01	0	Cacheado automáticamente	2
81	4	2010-01-01	0	Cacheado automáticamente	1
82	4	2010-01-01	0	Cacheado automáticamente	2
83	5	2010-02-01	0	Cacheado automáticamente	1
84	5	2010-02-01	0	Cacheado automáticamente	2
85	5	2010-01-01	0	Cacheado automáticamente	1
86	5	2010-01-01	0	Cacheado automáticamente	2
\.


--
-- Data for Name: id_reciente; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY id_reciente (id, lista_objetos_recientes_id, objeto_id) FROM stdin;
1	1	2
2	2	1
\.


--
-- Data for Name: laborable; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY laborable (id, fecha, turno_id, calendario_laboral_id, grupo_id, observaciones) FROM stdin;
\.


--
-- Data for Name: linea_de_abono; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY linea_de_abono (id, linea_de_venta_id, abono_id, diferencia, cantidad, observaciones, servicio_id) FROM stdin;
\.


--
-- Data for Name: linea_de_compra; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY linea_de_compra (id, pedido_compra_id, albaran_entrada_id, factura_compra_id, producto_compra_id, cantidad, precio, descuento, entrega, iva) FROM stdin;
2	\N	1	\N	3	25	45	0.10000000000000001		0.18
1	\N	1	\N	1	50	25	0		0.18
3	1	1	\N	2	4	1.25	0		0.18
4	3	2	2	5	1	500	0		0.18
\.


--
-- Data for Name: linea_de_devolucion; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY linea_de_devolucion (id, abono_id, albaran_de_entrada_de_abono_id, albaran_salida_id, precio, observaciones) FROM stdin;
\.


--
-- Data for Name: linea_de_pedido; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY linea_de_pedido (id, pedido_venta_id, fechahora, cantidad, precio, descuento, fecha_entrega, texto_entrega, producto_compra_id, presupuesto_id, notas) FROM stdin;
1	1	2010-02-21 11:47:52.434423	3	400	0	\N		5	\N	
2	\N	2010-02-21 15:32:50.565985	2	500	0	\N		5	1	
3	3	2010-02-21 15:54:36	2	25	0	\N		1	\N	
\.


--
-- Data for Name: linea_de_pedido_de_compra; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY linea_de_pedido_de_compra (id, producto_compra_id, pedido_compra_id, fechahora, cantidad, precio, descuento, fecha_entrega, texto_entrega, notas) FROM stdin;
1	2	1	2010-02-15 15:49:43.876865	7	0	0	\N	\N	Creado a partir de la consulta de faltas.
2	4	2	2010-02-15 16:12:38.478877	1	0	0	\N	\N	Creado a partir de la consulta de faltas.
3	5	3	2010-02-15 16:18:59.402806	3	500	0	2010-02-20	Lo entregarán en horario de mañana.	Creado a partir de la consulta de faltas.\nSe van a solicitar más unidades de las que sugirió el software.
\.


--
-- Data for Name: linea_de_pedido_de_compra__linea_de_compra; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY linea_de_pedido_de_compra__linea_de_compra (linea_de_pedido_de_compra_id, linea_de_compra_id) FROM stdin;
\.


--
-- Data for Name: linea_de_venta; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY linea_de_venta (id, pedido_venta_id, albaran_salida_id, factura_venta_id, prefactura_id, fechahora, cantidad, precio, descuento, producto_compra_id, ticket_id, notas, descripcion_complementaria) FROM stdin;
1	\N	\N	2	\N	2010-02-12 18:39:19	2	25	0	1	1		
3	\N	\N	3	\N	2010-02-12 18:45:31	1	45.000000000000007	0	3	3		
4	\N	\N	4	\N	2010-02-12 18:45:57	-1	45.000000000000007	0	3	4		
5	\N	\N	5	\N	2010-02-12 18:50:02	2	5.2586206896551726	0	2	5		
2	\N	\N	6	\N	2010-02-12 18:40:13	-2	25	0	1	2		
6	\N	\N	\N	\N	2010-02-15 16:43:01	1	500.00000000000006	0	5	6		
7	\N	\N	7	\N	2010-02-15 16:44:35	3	45.000000000000007	0	3	7		
8	\N	\N	7	\N	2010-02-15 16:45:00	1	25	0	1	7		
10	1	2	28	\N	2010-02-21 12:11:22	3	400	0	5	\N		
12	\N	\N	\N	\N	2010-02-21 15:16:59	1	5.2586206896551726	0	2	8		
13	\N	\N	\N	\N	2010-02-21 15:17:11	1	45.000000000000007	0	3	8		
9	2	1	27	\N	2010-02-21 11:08:41.610465	2	500	0	5	\N		
11	3	3	29	\N	2010-02-21 14:30:41.421275	2	25	0	1	\N		
14	\N	\N	\N	\N	2010-02-26 16:21:48	1	5.2586206896551726	0	2	9		
\.


--
-- Data for Name: lista_objetos_recientes; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY lista_objetos_recientes (id, usuario_id, ventana_id) FROM stdin;
1	1	1
2	\N	6
\.


--
-- Data for Name: memo; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY memo (id, categoria_id, resumen, texto, fechahora) FROM stdin;
4	\N	Pedir DNI	Pedir DNI a nuevo alumno José Pérez para poderle enviar las facturas.\nVolverá por el gimnasio el martes que viene.	2010-02-22 17:50:02.513606
5	\N	Bla bla bla	Bla bla bla bla bleh.	2010-02-22 17:50:47.45323
\.


--
-- Data for Name: modulo; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY modulo (id, nombre, icono, descripcion) FROM stdin;
1	Administración	administracion.png	Administración
2	Comercial	comercial.png	Comercial
3	Almacén	almacen.png	Gestión de almacén
4	Laboratorio	laboratorio.png	Laboratorio
5	General	func_generales.png	Funciones generales
7	Ayuda	doc_y_ayuda.png	Documentación y ayuda
8	Producción	produccion.png	Producción
6	Consultas	costes.png	Costes e informes
9	DEBUG	debug.png	Utilidades de depuración para el administrador
\.


--
-- Data for Name: motivo; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY motivo (id, descripcion, descripcion_dias, retribuido, sin_retribuir, excedencia_maxima, convenio, penaliza) FROM stdin;
\.


--
-- Data for Name: nomina; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY nomina (id, empleado_id, fecha, cantidad, horas_extra, horas_nocturnidad, gratificacion, plus_jefe_turno, plus_no_absentismo, plus_festivo, plus_turnicidad, plus_mantenimiento_sabados, total_horas_extra, total_horas_nocturnidad, base, otros, fechaini, fechafin) FROM stdin;
\.


--
-- Data for Name: nota; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY nota (id, factura_venta_id, fechahora, texto, observaciones) FROM stdin;
\.


--
-- Data for Name: observaciones_nominas; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY observaciones_nominas (id, fecha, observaciones) FROM stdin;
\.


--
-- Data for Name: orden_empleados; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY orden_empleados (id, orden, empleado_id, fecha) FROM stdin;
\.


--
-- Data for Name: padecimiento; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY padecimiento (id, cliente_id, fecha, texto) FROM stdin;
1	6	2010-01-01	Artritis reumática.
2	7	2009-02-15	Dolor de espalda
3	9	2009-01-01	Dolor de espalda.
\.


--
-- Data for Name: pagare_cobro; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY pagare_cobro (id, codigo, fecha_recepcion, fecha_cobro, cantidad, cobrado, observaciones, fecha_cobrado, procesado) FROM stdin;
1	1234	2010-02-21	2010-02-21	145	145		2010-02-22	t
\.


--
-- Data for Name: pagare_pago; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY pagare_pago (id, codigo, fecha_emision, fecha_pago, cantidad, pagado, observaciones, procesado, fecha_cobrado) FROM stdin;
2	123456	2010-02-15	2010-05-25	580	-1	\nPagado mediante pagaré La Caixa. Imprimido el 15 de febrero de 2010.	f	\N
1		2010-02-15	2010-02-15	0	-1		t	2010-02-15
\.


--
-- Data for Name: pago; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY pago (id, factura_compra_id, fecha, importe, observaciones, pagare_pago_id, proveedor_id, cuenta_origen_id, cuenta_destino_id, concepto_libre) FROM stdin;
1	2	2010-05-25	580	Pagaré con fecha 15/02/2010 y vencimiento 25/05/2010 (pdte. de pago)	2	2	\N	\N	
2	2	2010-02-21	0		\N	2	1	2	
\.


--
-- Data for Name: pago_de_abono; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY pago_de_abono (id, factura_de_abono_id, factura_venta_id, prefactura_id, importe, pendiente) FROM stdin;
\.


--
-- Data for Name: pedido_compra; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY pedido_compra (id, proveedor_id, fecha, numpedido, iva, descuento, entregas, forma_de_pago, observaciones, bloqueado, cerrado, direccion_entrega0, direccion_entrega1, direccion_entrega2, responsable0, responsable1, portes0, portes1, observaciones0, observaciones1, observaciones2) FROM stdin;
1	\N	2010-02-15	1	0.18	0				f	f										
2	1	\N	2	0.18	0				f	f										
3	2	2010-02-15	3	0.18	0		90 D.F.F.		t	f										
\.


--
-- Data for Name: pedido_venta; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY pedido_venta (id, cliente_id, tarifa_id, transporte_a_cargo, fecha, numpedido, iva, descuento, bloqueado, cerrado, envio_direccion, envio_ciudad, envio_provincia, envio_cp, envio_pais, nombre_correspondencia, direccion_correspondencia, cp_correspondencia, ciudad_correspondencia, provincia_correspondencia, pais_correspondencia) FROM stdin;
1	2	\N	f	2010-02-21	1	0.18	0	t	t						Cliente 2					
2	1	\N	f	2010-02-21	12314	0.18	0	f	f											
3	4	\N	f	2010-02-21	12234	0.18	0	f	t											
\.


--
-- Data for Name: permiso; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) FROM stdin;
105	1	224	t	t	t	t
106	1	227	t	t	t	t
5	1	69	t	t	t	t
100	1	88	t	t	t	t
14	1	105	t	t	t	t
76	1	56	t	t	t	t
65	1	47	f	f	f	f
23	1	66	f	f	f	f
61	1	44	t	t	t	t
89	1	78	f	f	f	f
15	1	106	t	t	t	t
90	1	92	f	f	f	f
70	1	82	f	f	f	f
43	1	26	f	f	f	f
60	1	107	f	f	f	f
59	1	85	f	f	f	f
91	1	77	f	f	f	f
84	1	90	t	t	t	t
10	1	68	t	t	t	t
24	1	108	t	t	t	t
71	1	93	f	f	f	f
98	1	109	f	f	f	f
37	1	99	f	f	f	f
92	1	76	f	f	f	f
44	1	27	t	t	t	t
11	1	94	t	t	t	t
38	1	49	f	f	f	f
99	1	111	t	t	t	t
1	1	1	t	t	t	t
93	1	75	f	f	f	f
45	1	28	f	f	f	f
85	1	57	t	t	t	t
31	1	98	t	t	t	t
30	1	74	t	t	t	t
16	1	110	t	t	t	t
2	1	2	t	t	t	t
46	1	29	t	t	t	t
6	1	70	f	f	f	f
94	1	97	f	f	f	f
3	1	3	t	t	t	t
17	1	112	t	t	t	t
22	1	5	t	t	t	t
32	1	95	f	f	f	f
18	1	113	t	t	t	t
47	1	30	t	t	t	t
34	1	221	t	t	t	t
33	1	96	f	f	f	f
86	1	59	t	t	t	t
19	1	4	t	t	t	t
7	1	86	f	f	f	f
72	1	46	f	f	f	f
62	1	45	t	t	t	t
48	1	31	f	f	f	f
73	1	48	f	f	f	f
20	1	6	t	t	t	t
102	1	226	t	t	t	t
66	1	71	f	f	f	f
49	1	32	f	f	f	f
54	1	33	t	t	t	t
67	1	79	f	f	f	f
21	1	7	t	t	t	t
95	1	100	f	f	f	f
77	1	89	t	t	t	t
103	1	225	t	t	t	t
25	1	8	f	f	f	f
39	1	50	f	f	f	f
68	1	80	f	f	f	f
50	1	34	t	t	t	t
96	1	101	t	t	t	t
55	1	61	t	t	t	t
26	1	9	f	f	f	f
8	1	83	f	f	f	f
51	1	35	t	t	t	t
40	1	62	f	f	f	f
101	1	102	t	t	t	t
41	1	63	f	f	f	f
52	1	36	t	t	t	t
27	1	10	f	f	f	f
9	1	84	f	f	f	f
42	1	16	f	f	f	f
53	1	37	f	f	f	f
56	1	72	t	t	t	t
28	1	11	t	t	t	t
97	1	55	f	f	f	f
63	1	65	f	f	f	f
104	1	223	t	t	t	t
78	1	38	t	t	t	t
29	1	12	t	t	t	t
64	1	64	f	f	f	f
57	1	73	t	t	t	t
12	1	104	t	t	t	t
74	1	53	t	t	t	t
79	1	39	t	t	t	t
75	1	54	t	t	t	t
87	1	91	f	f	f	f
80	1	40	t	t	t	t
58	1	81	f	f	f	f
35	1	22	f	f	f	f
81	1	41	t	t	t	t
88	1	58	t	t	t	t
13	1	103	t	t	t	t
82	1	42	t	t	t	t
69	1	67	f	f	f	f
36	1	23	f	f	f	f
4	1	87	t	t	t	t
83	1	43	t	t	t	t
\.


--
-- Data for Name: precio; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY precio (id, tarifa_id, precio, producto_compra_id) FROM stdin;
1	1	520	5
2	1	6.0489999999999995	2
\.


--
-- Data for Name: prefactura; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY prefactura (id, cliente_id, fecha, numfactura, descuento, cargo, observaciones, iva, bloqueada, irpf) FROM stdin;
\.


--
-- Data for Name: presupuesto; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY presupuesto (id, cliente_id, fecha, persona_contacto, nombrecliente, direccion, ciudad, provincia, cp, pais, telefono, fax, texto, despedida, validez, numpresupuesto, descuento, obra) FROM stdin;
1	4	2010-02-21		Menganito		Sevilla	Sevilla		España			Muy Srs. Ntros.:\n\n    En relación con su petición de oferta...\n\n    El precio del producto es:	Muchas gracias y no dude en llamarnos para cualquier duda o problema.\n\nUn saludo,	6	\N	0	
\.


--
-- Data for Name: producto_compra; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY producto_compra (id, tipo_de_material_id, descripcion, codigo, unidad, minimo, existencias, precio_defecto, control_existencias, fvaloracion, observaciones, obsoleto) FROM stdin;
4	1	Magic Circle	0005	ud.	1	0	200	t			f
1	2	Pelota Pilates (TM)	0001	ud.	10	47	25	t			f
3	4	Camiseta elástica	0003	ud.	0	21	45	t			f
5	1	Pedi Pole	0008	ud.	2	-2	500	t			f
2	5	Jalea real	0002	l	5	0	5.2599999999999998	t		De venta a granel.	f
\.


--
-- Data for Name: proveedor; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY proveedor (id, nombre, cif, direccion, pais, ciudad, provincia, cp, telefono, fax, contacto, observaciones, direccionfacturacion, paisfacturacion, ciudadfacturacion, provinciafacturacion, cpfacturacion, email, formadepago, documentodepago, vencimiento, diadepago, correoe, web, banco, swif, iban, cuenta, inhabilitado, motivo, iva, nombre_banco) FROM stdin;
2	PilatesProv	00000001V						696 696 969		José Rodríguez Rodríguez	Proveedor de prueba.						sales@pilatesprov.es	90 D.F.F.	Pagaré	90 D.F.F.	25	sales@pilatesprov.es						f		0.18	
1	Proveedor de prueba	00000000T						699 666 999		Juan López Rodríguez		C/ Calle...	España	Sevilla	Sevilla	41010	proveedor@prov.net	120 D.F.F.	Pagaré	120 D.F.F.	25							f		0.18	
\.


--
-- Data for Name: recibo; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY recibo (id, numrecibo, anno, lugar_libramiento, fecha_libramiento, fecha_vencimiento, persona_pago, domicilio_pago, cuenta_origen_id, nombre_librado, direccion_librado, observaciones, cuenta_bancaria_cliente_id) FROM stdin;
1	1	2010	Marbella	2010-02-15	2010-03-25			\N	José López Pérez	, C/ calle..., Sevilla		\N
2	2	2010	Marbella	2010-02-15	2010-04-25			\N	José López Pérez	, C/ calle..., Sevilla		\N
3	3	2010	Marbella	2010-02-21	2010-03-25			\N	Cliente 2	, , 		1
\.


--
-- Data for Name: servicio; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY servicio (id, factura_venta_id, prefactura_id, albaran_salida_id, concepto, cantidad, precio, descuento, pedido_venta_id, presupuesto_id, notas, actividad_id) FROM stdin;
9	12	\N	\N	[13:31 - 14:31] Rehabilitación (refuerzo)	1	1	0	\N	\N		6
10	12	\N	\N	[13:31 - 14:50] Rehabilitación clase 3	1.3166666666666667	1	0	\N	\N		5
11	12	\N	\N	[13:31 - 14:31] Rehabilitación (clase 4)	1	1	0	\N	\N		7
12	12	\N	\N	[13:31 - 14:31] Rehabilitación (clase 5)	1	1	0	\N	\N		8
13	12	\N	\N	[13:31 - 14:31] Rehabilitación (clase 1)	1	1	0	\N	\N		9
1	1	\N	\N	Clases mes de enero 2.010	1	123	0	\N	\N		\N
2	8	\N	\N	Clases enero 2.010	1	250	0	\N	\N		\N
3	\N	\N	\N	Clases Pilates	2	1	0	\N	\N	[10:00 - 12:00] Clase especial Día de Andalucía	\N
4	\N	\N	\N	Clases Pilates	2	1	0	\N	\N	[10:00 - 12:00] Clase especial Día de Andalucía	\N
5	9	\N	\N	Clases Pilates	12.316666666666666	1	0	\N	\N	[13:31 - 14:31] Rehabilitación clase 1\n[13:31 - 14:31] Rehabilitación (refuerzo)\n[13:31 - 14:50] Rehabilitación clase 3\n[13:31 - 14:31] Rehabilitación (clase 4)\n[13:31 - 14:31] Rehabilitación (clase 5)\n[13:31 - 14:31] Rehabilitación (clase 1)\n[13:31 - 14:31] Rehabilitación (relajación)\n[13:31 - 14:31] Rehabilitación (clase 3)\n[13:31 - 14:31] Rehabilitación (clase 1)\n[13:31 - 14:31] Rehabilitación (clase 2)\n[13:31 - 14:31] Rehabilitación (clase 3)\n[13:31 - 14:31] Rehabilitación (clase 2)	\N
6	10	\N	\N	Clases Pilates	2	1	0	\N	\N	[10:00 - 12:00] Clase especial Día de Andalucía	\N
7	11	\N	\N	Clases Pilates	12.316666666666666	1	0	\N	\N	[13:31 - 14:31] Rehabilitación clase 1\n[13:31 - 14:31] Rehabilitación (refuerzo)\n[13:31 - 14:50] Rehabilitación clase 3\n[13:31 - 14:31] Rehabilitación (clase 4)\n[13:31 - 14:31] Rehabilitación (clase 5)\n[13:31 - 14:31] Rehabilitación (clase 1)\n[13:31 - 14:31] Rehabilitación (relajación)\n[13:31 - 14:31] Rehabilitación (clase 3)\n[13:31 - 14:31] Rehabilitación (clase 1)\n[13:31 - 14:31] Rehabilitación (clase 2)\n[13:31 - 14:31] Rehabilitación (clase 3)\n[13:31 - 14:31] Rehabilitación (clase 2)	\N
8	12	\N	\N	[13:31 - 14:31] Rehabilitación clase 1	1	1	0	\N	\N		3
14	12	\N	\N	[13:31 - 14:31] Rehabilitación (relajación)	1	1	0	\N	\N		11
15	12	\N	\N	[13:31 - 14:31] Rehabilitación (clase 3)	1	1	0	\N	\N		12
16	12	\N	\N	[13:31 - 14:31] Rehabilitación (clase 1)	1	1	0	\N	\N		14
17	12	\N	\N	[13:31 - 14:31] Rehabilitación (clase 2)	1	1	0	\N	\N		15
18	12	\N	\N	[13:31 - 14:31] Rehabilitación (clase 3)	1	1	0	\N	\N		16
19	12	\N	\N	[13:31 - 14:31] Rehabilitación (clase 2)	1	1	0	\N	\N		10
20	13	\N	\N	[12:30 - 13:30] Power Plate	1	1	0	\N	\N		24
21	13	\N	\N	[12:30 - 13:30] Power Plate (iniciación)	1	1	0	\N	\N		19
22	13	\N	\N	[10:00 - 14:00] Especial puertas abiertas Día de Andalucía	4	1	0	\N	\N		25
23	13	\N	\N	[12:30 - 13:00] Power Plate	0.5	1	0	\N	\N		20
24	13	\N	\N	[12:25 - 12:25] Calentamiento	0	1	0	\N	\N		2
25	13	\N	\N	[16:30 - 17:30] Power Plate 2	1	1	0	\N	\N		27
26	13	\N	\N	[16:30 - 17:30] Power Plate 2	1	1	0	\N	\N		28
28	13	\N	\N	[16:30 - 17:30] Power Plate 2 (primera clase)	1	1	0	\N	\N		26
29	13	\N	\N	[13:31 - 14:31] Rehabilitación clase 1	1	1	0	\N	\N		3
30	13	\N	\N	[13:31 - 14:31] Rehabilitación (refuerzo)	1	1	0	\N	\N		6
31	13	\N	\N	[13:31 - 14:50] Rehabilitación clase 3	1.3166666666666667	1	0	\N	\N		5
32	13	\N	\N	[13:31 - 14:31] Rehabilitación (clase 4)	1	1	0	\N	\N		7
33	13	\N	\N	[13:31 - 14:31] Rehabilitación (clase 5)	1	1	0	\N	\N		8
34	13	\N	\N	[13:31 - 14:31] Rehabilitación (clase 1)	1	1	0	\N	\N		9
35	13	\N	\N	[13:31 - 14:31] Rehabilitación (relajación)	1	1	0	\N	\N		11
36	13	\N	\N	[13:31 - 14:31] Rehabilitación (clase 3)	1	1	0	\N	\N		12
37	13	\N	\N	[13:31 - 14:31] Rehabilitación (clase 1)	1	1	0	\N	\N		14
38	13	\N	\N	[13:31 - 14:31] Rehabilitación (clase 2)	1	1	0	\N	\N		15
39	13	\N	\N	[13:31 - 14:31] Rehabilitación (clase 3)	1	1	0	\N	\N		16
40	13	\N	\N	[13:31 - 14:31] Rehabilitación (clase 2)	1	1	0	\N	\N		10
41	14	\N	\N	[13:31 - 14:31] Rehabilitación clase 1	1	1	0	\N	\N		3
42	14	\N	\N	[13:31 - 14:31] Rehabilitación (refuerzo)	1	1	0	\N	\N		6
43	14	\N	\N	[13:31 - 14:50] Rehabilitación clase 3	1.3166666666666667	1	0	\N	\N		5
44	14	\N	\N	[13:31 - 14:31] Rehabilitación (clase 4)	1	1	0	\N	\N		7
45	14	\N	\N	[13:31 - 14:31] Rehabilitación (clase 5)	1	1	0	\N	\N		8
46	14	\N	\N	[13:31 - 14:31] Rehabilitación (clase 1)	1	1	0	\N	\N		9
47	14	\N	\N	[13:31 - 14:31] Rehabilitación (relajación)	1	1	0	\N	\N		11
48	14	\N	\N	[13:31 - 14:31] Rehabilitación (clase 3)	1	1	0	\N	\N		12
49	14	\N	\N	[13:31 - 14:31] Rehabilitación (clase 1)	1	1	0	\N	\N		14
50	14	\N	\N	[13:31 - 14:31] Rehabilitación (clase 2)	1	1	0	\N	\N		15
51	14	\N	\N	[13:31 - 14:31] Rehabilitación (clase 3)	1	1	0	\N	\N		16
52	14	\N	\N	[13:31 - 14:31] Rehabilitación (clase 2)	1	1	0	\N	\N		10
171	25	\N	\N	[12:30 - 13:30] Power Plate	1	1	0	\N	\N		21
172	25	\N	\N	[12:30 - 13:30] Power Plate	1	1	0	\N	\N		22
173	25	\N	\N	[12:30 - 13:30] Power Plate	1	1	0	\N	\N		24
174	25	\N	\N	[12:30 - 13:30] Power Plate (iniciación)	1	1	0	\N	\N		19
175	25	\N	\N	[10:00 - 14:00] Especial puertas abiertas Día de Andalucía	4	1	0	\N	\N		25
176	25	\N	\N	[12:30 - 13:00] Power Plate	0.5	1	0	\N	\N		20
177	25	\N	\N	[16:30 - 17:30] Power Plate 2	1	1	0	\N	\N		27
178	25	\N	\N	[16:30 - 17:30] Power Plate 2	1	1	0	\N	\N		28
180	25	\N	\N	[16:30 - 17:30] Power Plate 2 (primera clase)	1	1	0	\N	\N		26
181	25	\N	\N	[13:31 - 14:31] Rehabilitación clase 1	1	1	0	\N	\N		3
182	25	\N	\N	[13:31 - 14:31] Rehabilitación (refuerzo)	1	1	0	\N	\N		6
183	25	\N	\N	[13:31 - 14:50] Rehabilitación clase 3	1.3166666666666667	1	0	\N	\N		5
184	25	\N	\N	[13:31 - 14:31] Rehabilitación (clase 4)	1	1	0	\N	\N		7
185	25	\N	\N	[13:31 - 14:31] Rehabilitación (clase 5)	1	1	0	\N	\N		8
186	25	\N	\N	[13:31 - 14:31] Rehabilitación (clase 1)	1	1	0	\N	\N		9
187	25	\N	\N	[13:31 - 14:31] Rehabilitación (relajación)	1	1	0	\N	\N		11
188	25	\N	\N	[13:31 - 14:31] Rehabilitación (clase 3)	1	1	0	\N	\N		12
189	25	\N	\N	[13:31 - 14:31] Rehabilitación (clase 1)	1	1	0	\N	\N		14
190	25	\N	\N	[13:31 - 14:31] Rehabilitación (clase 2)	1	1	0	\N	\N		15
191	25	\N	\N	[13:31 - 14:31] Rehabilitación (clase 3)	1	1	0	\N	\N		16
192	25	\N	\N	[13:31 - 14:31] Rehabilitación (clase 2)	1	1	0	\N	\N		10
193	26	\N	\N	[12:30 - 13:30] Power Plate	1	1	0	\N	\N		21
194	26	\N	\N	[12:30 - 13:30] Power Plate	1	1	0	\N	\N		22
195	26	\N	\N	[12:30 - 13:30] Power Plate	1	1	0	\N	\N		24
196	26	\N	\N	[12:30 - 13:30] Power Plate (iniciación)	1	1	0	\N	\N		19
197	26	\N	\N	[10:00 - 14:00] Especial puertas abiertas Día de Andalucía	4	1	0	\N	\N		25
198	26	\N	\N	[12:30 - 13:00] Power Plate	0.5	1	0	\N	\N		20
199	26	\N	\N	[16:30 - 17:30] Power Plate 2	1	1	0	\N	\N		27
200	26	\N	\N	[16:30 - 17:30] Power Plate 2	1	1	0	\N	\N		28
202	26	\N	\N	[16:30 - 17:30] Power Plate 2 (primera clase)	1	1	0	\N	\N		26
203	26	\N	\N	[13:31 - 14:31] Rehabilitación clase 1	1	1	0	\N	\N		3
204	26	\N	\N	[13:31 - 14:31] Rehabilitación (refuerzo)	1	1	0	\N	\N		6
205	26	\N	\N	[13:31 - 14:50] Rehabilitación clase 3	1.3166666666666667	1	0	\N	\N		5
206	26	\N	\N	[13:31 - 14:31] Rehabilitación (clase 4)	1	1	0	\N	\N		7
207	26	\N	\N	[13:31 - 14:31] Rehabilitación (clase 5)	1	1	0	\N	\N		8
208	26	\N	\N	[13:31 - 14:31] Rehabilitación (clase 1)	1	1	0	\N	\N		9
209	26	\N	\N	[13:31 - 14:31] Rehabilitación (relajación)	1	1	0	\N	\N		11
210	26	\N	\N	[13:31 - 14:31] Rehabilitación (clase 3)	1	1	0	\N	\N		12
211	26	\N	\N	[13:31 - 14:31] Rehabilitación (clase 1)	1	1	0	\N	\N		14
212	26	\N	\N	[13:31 - 14:31] Rehabilitación (clase 2)	1	1	0	\N	\N		15
213	26	\N	\N	[13:31 - 14:31] Rehabilitación (clase 3)	1	1	0	\N	\N		16
214	26	\N	\N	[13:31 - 14:31] Rehabilitación (clase 2)	1	1	0	\N	\N		10
215	27	\N	\N	[12:30 - 13:30] Power Plate	1	1	0	\N	\N		21
216	27	\N	\N	[12:30 - 13:30] Power Plate	1	1	0	\N	\N		22
217	28	\N	2	Clases junio	2	2	0	1	\N		\N
218	29	\N	3	tal	1	12	0	\N	\N		\N
219	\N	\N	\N	tal	3	23.449999999999999	0	\N	1		\N
\.


--
-- Data for Name: servicio_tomado; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY servicio_tomado (id, factura_compra_id, concepto, cantidad, precio, descuento, transporte_a_cuenta_id, iva) FROM stdin;
\.


--
-- Data for Name: stock_almacen; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY stock_almacen (id, almacen_id, producto_compra_id, existencias) FROM stdin;
1	2	1	2
2	2	3	0
3	2	2	-2
7	1	5	-2
4	1	1	47
5	1	3	21
6	1	2	2
\.


--
-- Data for Name: tarea; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY tarea (id, categoria_id, resumen, texto, fecha_limite, fecha_done, fechahora) FROM stdin;
3	\N	Llamada de teléfono	Llamar por teléfono a José Rodríguez.\nConfirmar reunión.	\N	2010-02-15	2010-02-22 17:50:12.161319
4	\N	Enviar mailing	Enviar un mailing a todos los clientes.	\N	\N	2010-02-22 17:50:12.161319
5	\N	Tarea 2	Tal y pam.	\N	\N	2010-02-22 17:51:22.928381
\.


--
-- Data for Name: tarifa; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY tarifa (id, nombre, observaciones, periodo_validez_ini, periodo_validez_fin) FROM stdin;
1	Tarifa venta	Tarifa estándar de venta.	\N	\N
\.


--
-- Data for Name: ticket; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY ticket (id, fechahora, numticket) FROM stdin;
1	2010-02-12 18:39:12.205347	1
2	2010-02-12 18:40:13.563336	2
3	2010-02-12 18:45:29.198811	3
4	2010-02-12 18:45:54.395199	4
5	2010-02-12 18:50:01.292383	5
6	2010-02-15 16:43:01.279659	6
7	2010-02-15 16:44:15.204868	7
8	2010-02-21 15:16:59.819329	8
9	2010-02-26 16:21:48.756991	9
\.


--
-- Data for Name: tipo_de_material; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY tipo_de_material (id, descripcion) FROM stdin;
1	Máquinas gimnasio
2	Accesorios gimnasio
4	Ropa deportiva
5	Alimentación
\.


--
-- Data for Name: transporte_a_cuenta; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY transporte_a_cuenta (id, concepto, precio, observaciones, fecha, albaran_salida_id, proveedor_id) FROM stdin;
\.


--
-- Data for Name: transportista; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY transportista (id, agencia, nombre, dni, telefono, matricula) FROM stdin;
1					
\.


--
-- Data for Name: turno; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY turno (id, nombre, horainicio, horafin, noche, observaciones, recuperacion) FROM stdin;
\.


--
-- Data for Name: usuario; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY usuario (id, usuario, passwd, nombre, cuenta, cpass, nivel, email, smtpserver, smtpuser, smtppassword, firma_total, firma_comercial, firma_director, firma_tecnico, firma_usuario, observaciones) FROM stdin;
1	admin	cee9be15784861e244ca2e58268343c8	Administrador	frbogado@vm-webhosting	gusa25	0	frbogado@novaweb.es	smtp.gea21.es	fbogado	dfg234..-	t	t	t	t	t	Administrador de la aplicación.
\.


--
-- Data for Name: vacaciones; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY vacaciones (id, calendario_laboral_id, fecha) FROM stdin;
\.


--
-- Data for Name: vencimiento_cobro; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY vencimiento_cobro (id, factura_venta_id, prefactura_id, fecha, importe, observaciones, cuenta_origen_id, recibo_id) FROM stdin;
1	1	\N	2010-08-25	142.68000000000001	Recibo bancario	\N	\N
2	4	\N	2010-03-14	-52.200000000000003	RECIBO DOMICILIADO, 30 los días 25. 	\N	\N
3	5	\N	2010-03-25	12.199999999999999	RECIBO DOMICILIADO, 30 los días 25. 	\N	\N
4	6	\N	2010-02-12	-58		\N	\N
5	7	\N	2010-02-15	185.59999999999999		\N	\N
6	8	\N	2010-03-25	145	Recibo domiciliado, 30-60 D.F.F. los días 25. Recibo bancario número 1 con fecha de emisión 15/02/2010.	\N	1
7	8	\N	2010-04-25	145	Recibo domiciliado, 30-60 D.F.F. los días 25. Recibo bancario número 2 con fecha de emisión 15/02/2010.	\N	2
8	9	\N	2010-02-20	14.289999999999999		\N	\N
10	27	\N	2010-08-25	1162.3199999999999	PAGARÉ, 180 D.F.F. los días 25. 	\N	\N
11	28	\N	2010-03-25	1744.6400000000001	RECIBO DOMICILIADO, 30 los días 25. Recibo bancario número 3 con fecha de emisión 21/02/2010.	\N	3
12	29	\N	2010-02-21	71.920000000000002		\N	\N
13	13	\N	2010-08-25	26.469999999999999	PAGARÉ, 180 D.F.F. los días 25. 	\N	\N
\.


--
-- Data for Name: vencimiento_pago; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY vencimiento_pago (id, factura_compra_id, fecha, importe, observaciones) FROM stdin;
1	2	2010-05-25	580	Pagaré, 90 D.F.F. los días 25. 
\.


--
-- Data for Name: ventana; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY ventana (id, modulo_id, descripcion, fichero, clase, icono) FROM stdin;
1	1	Facturas de compra	facturas_compra.py	FacturasDeEntrada	factura_compra.png
2	1	Facturas de venta	facturas_venta.py	FacturasVenta	factura_venta.png
3	1	Abonos sobre facturas de venta	abonos_venta.py	AbonosVenta	abonos_venta.png
4	2	Pedidos de compra (a proveedores)	pedidos_de_compra.py	PedidosDeCompra	pedido.png
6	2	Pedidos de venta (de clientes)	pedidos_de_venta.py	PedidosDeVenta	pedido.png
7	2	Ver ventas sin pedido asignado	lineas_sin_pedido.py	LineasDeVentaSinPedido	sin_pedido.png
8	3	Ver existencias de rollos en almacén	rollos_almacen.py	RollosAlmacen	rollos_en_almacen.png
9	3	Listado de balas fabricadas	listado_balas.py	ListadoBalas	
10	3	Listado de rollos fabricados	listado_rollos.py	ListadoRollos	
11	3	Albaranes de entrada de material	albaranes_de_entrada.py	AlbaranesDeEntrada	albaran.png
12	3	Albaranes de salida	albaranes_de_salida.py	AlbaranesDeSalida	albaran.png
53	6	Consulta de albaranes de clientes	consulta_albaranes_clientes.py	ConsultaAlbaranesCliente	informe.png
54	6	Consulta de cobros	consulta_cobros.py	ConsultaCobros	informe.png
22	4	Asignar directamente resultados de laboratorio a lote de fibra. (No guarda histórico)	lab_resultados_lote.py	LabResultadosLote	
23	4	Buscar lotes con valores determinados	busca_lote.py	BuscaLote	buscar.png
56	6	Consulta de pagos	consulta_pagos.py	ConsultaPagos	informe.png
26	5	Tipos de material de fibra	tipos_material_balas.py	TiposMaterialBala	tipos_de.png
27	5	Gestión de usuarios	usuarios.py	Usuarios	usuarios.png
28	5	Tipos de incidencia	tipos_incidencia.py	TiposIncidencia	tipos_de.png
29	5	Proveedores	proveedores.py	Proveedores	proveedores.png
30	5	Contadores para facturas de clientes	contadores.py	Contadores	contadores.png
31	5	Catálogo de productos de venta (geocompuestos)	productos_de_venta_rollos_geocompuestos.py	ProductosDeVentaRollosGeocompuestos	catalogo.png
32	5	Catálogo de productos de venta (fibra)	productos_de_venta_balas.py	ProductosDeVentaBalas	catalogo.png
89	6	Pedidos pendientes de servir	consulta_pendientes_servir.py	PendientesServir	informe.png
34	5	Empleados	empleados.py	Empleados	empleados.png
37	5	Catálogo de productos de venta (geotextiles)	productos_de_venta_rollos.py	ProductosDeVentaRollos	catalogo.png
38	6	Existencias de materiales en almacén	consulta_existencias.py	ConsultaExistencias	informe.png
39	6	Listado de albaranes facturados	consulta_albaranesFacturados.py	ConsultaAlbaranesFacturados	informe.png
40	6	Ver productos bajo mínimos	consulta_bajoMinimos.py	ConsultaBajoMinimos	informe.png
41	6	Listado de albaranes pendientes de facturar	consulta_albaranesPorFacturar.py	ConsultaAlbaranesPorFacturar	informe.png
42	6	Listado de compras	consulta_compras.py	ConsultaCompras	informe.png
43	6	Listado de ventas	consulta_ventas.py	ConsultaVentas	informe.png
44	7	Acerca de...	acerca_de.py	acerca_de	acerca.png
90	6	Pedidos pendientes de recibir	consulta_pendientes_recibir.py	PendientesRecibir	informe.png
99	4	Resultados fibra de cemento	resultados_cemento.py	ResultadosFibra	labo_fibra.png
49	4	Muestras pendientes de analizar	muestras_pendientes.py	MuestrasPendientes	estrella.png
57	6	Consulta de pedidos de clientes	consulta_pedidos_clientes.py	ConsultaPedidosCliente	informe.png
5	2	Tarifas de precios	tarifas_de_precios.py	TarifasDePrecios	tarifa.png
59	6	Consulta de vencimientos de pago	consulta_vencimientos_pago.py	ConsultaVencimientosPagos	informe.png
45	7	Ayuda on-line (mensajería instantánea)	gajim.py	gajim	gajim.png
33	5	Cartera de clientes	clientes.py	Clientes	clientes.png
50	4	Buscar partidas por características	busca_partida.py	BuscaPartida	buscar.png
61	5	Mis datos de usuario	ventana_usuario.py	Usuarios	usuarios.png
62	4	Resultados fibra	resultados_fibra.py	ResultadosFibra	labo_fibra.png
63	4	Resultados geotextiles	resultados_geotextiles.py	ResultadosGeotextiles	labo_rollos.png
16	4	Resultados de fluidez de granza (MFI)	resultados_fluidez.py	ResultadosFluidez	labo_mp.png
65	8	Horas de trabajo por empleado	horas_trabajadas.py	HorasTrabajadas	reloj.png
64	8	Partes pendientes de revisar	partes_no_bloqueados.py	PartesNoBloqueados	candado.png
91	6	Consumos	consulta_consumo.py	ConsultaConsumo	informe.png
58	6	Consulta de vencimientos de cobro	consulta_vencimientos_cobro.py	ConsultaVencimientosCobros	informe.png
87	1	Cheques y pagarés de pago	pagares_pagos.py	PagaresPagos	money.png
69	1	Efectos de cobro	pagares_cobros.py	PagaresCobros	money.png
47	8	Ver productividad global	consulta_productividad.py	ConsultaProductividad	productividad.png
78	6	Consulta partidas por producto	consulta_partidas_por_producto.py	ConsultaPartidasPorProducto	informe.png
92	6	Productos terminados	consulta_producido.py	ConsultaProducido	grafs.png
77	6	Consulta lotes por producto	consulta_lotes_por_producto.py	ConsultaLotesPorProducto	informe.png
76	6	Imprimir existencias de geotextiles	consulta_existenciasRollos.py	ConsultaExistencias	informe.png
75	6	Imprimir existencias de fibra	consulta_existenciasBalas.py	ConsultaExistencias	informe.png
74	3	Valoración de entradas en almacén	consulta_entradas_almacen.py	ConsultaEntradasAlmacen	informe.png
70	1	Ausencias	ausencias.py	Ausencias	ausencias.png
86	1	Cálculo de primas y nóminas	nominas.py	Nominas	nominas.png
71	8	Calendarios laborales	calendario_laboral.py	CalendarioLaboral	calendario.png
79	8	Formulación fibra	formulacion_fibra.py	FormulacionFibra	formulacion.png
80	8	Formulación geotextiles	formulacion_geotextiles.py	FormulacionGeotextiles	formulacion.png
83	1	Importar datos de LOGIC	importar_logic.py	ImportarLogic	logic.png
84	1	Mostrar datos de LOGIC existentes	mostrar_datos_logic.py	MostrarDatosLogic	logic.png
72	5	Configuración de categorías laborales	categorias_laborales.py	CategoriasLaborales	catcent.png
36	5	Familias de productos	tipos_material.py	TiposMaterial	tipos_de.png
73	5	Configuración de centros de trabajo	centros_de_trabajo.py	CentrosDeTrabajo	catcent.png
81	5	Configuración de grupos de trabajo	grupos.py	Grupos	catcent.png
67	8	Partes de trabajo (no producción)	partes_de_trabajo.py	PartesDeTrabajo	partestrabajo.png
88	9	Trazabilidad interna (DEBUG) - Sólo para el administrador	trazabilidad.py	Trazabilidad	trazabilidad.png
66	2	Trazabilidad de productos finales	trazabilidad_articulos.py	TrazabilidadArticulos	trazabilidad.png
82	8	Horas trabajadas por día	horas_trabajadas_dia.py	HorasTrabajadasDia	reloj.png
85	5	Configurar motivos de ausencia	motivos_ausencia.py	MotivosAusencia	motivos.png
68	1	Vencimientos pendientes por cliente	vencimientos_pendientes_por_cliente.py	VencimientosPendientesPorCliente	pendiente.png
20	\N	01.- Resultados de resistencia a alargamiento longitudinal	resultados_longitudinal.py	ResultadosLongitudinal	labo_rollos.png
93	8	Consumo de fibra por partida	consumo_balas_partida.py	ConsumoBalasPartida	
13	\N	04.- Resultados de perforación (cono)	resultados_perforacion.py	ResultadosPerforacion	labo_rollos.png
18	\N	06.- Resultados de permeabilidad	resultados_permeabilidad.py	ResultadosPermeabilidad	labo_rollos.png
51	\N	07.- Resultados de apertura de poros	resultados_poros.py	ResultadosPoros	labo_rollos.png
14	\N	02.- Resultados de resistencia a alargamiento transversal	resultados_transversal.py	ResultadosTransversal	labo_rollos.png
52	\N	05.- Resultados de espesor	resultados_espesor.py	ResultadosEspesor	labo_rollos.png
21	\N	03.- Resultados de compresión (CBR)	resultados_compresion.py	ResultadosCompresion	labo_rollos.png
17	\N	09.- Resultados de tenacidad sobre fibra	resultados_tenacidad.py	ResultadosTenacidad	labo_fibra.png
15	\N	10.- Resultados de elongación sobre fibra	resultados_elongacion.py	ResultadosElongacion	labo_fibra.png
25	\N	11.- Resultados encogimiento sobre fibra	resultados_encogimiento.py	ResultadosEncogimiento	labo_fibra.png
19	\N	12.- Resultados de grasa sobre fibra	resultados_grasa.py	ResultadosGrasa	labo_fibra.png
24	\N	13.- Resultados de rizo sobre fibra	resultados_rizo.py	ResultadosRizo	labo_fibra.png
60	\N	08.- Resultados de título (DTEX)	resultados_titulo.py	ResultadosTitulo	labo_fibra.png
94	1	Facturas pendientes de revisar e imprimir	facturas_no_bloqueadas.py	FacturasNoBloqueadas	facturas_no_bloqueadas.png
98	3	Historial de productos de compra	historico_existencias_compra.py	HistoricoExistenciasCompra	globe.png
97	6	Consumo de fibra de la línea de geotextiles	consumo_fibra_por_partida_gtx.py	ConsumoFibraPorPartidaGtx	informe.png
95	3	Estado de silos	silos.py	Silos	silos.png
96	3	Histórico de existencias de productos de venta	historico_existencias.py	HistoricoExistencias	globe.png
46	8	Partes de fabricación de fibra	partes_de_fabricacion_balas.py	PartesDeFabricacionBalas	balas.png
48	8	Partes de fabricación de geotextiles	partes_de_fabricacion_rollos.py	PartesDeFabricacionRollos	rollos.png
100	6	Resumen totales geotextiles por mes	consulta_totales_geotextiles.py	ConsultaTotalesGeotextiles	informe.png
101	6	Facturación por cliente y fecha	facturacion_por_cliente_y_fechas.py	FacturacionPorClienteYFechas	informe.png
102	9	Visor del log	logviewer.py	LogViewer	trazabilidad.png
55	6	Consulta incidencias en líneas de producción	consulta_incidencias.py	ConsultaIncidencias	grafs.png
104	1	Cuentas bancarias de proveedores	cuentas_destino.py	CuentasDestino	money.png
103	1	Cuentas bancarias de la empresa	cuentas_origen.py	CuentasOrigen	money.png
105	1	Pago por transferencia	transferencias.py	Transferencias	dollars.png
106	1	Facturas de compra pendientes de aprobación	consulta_pendientes_vto_bueno.py	ConsultaPendientesVtoBueno	firma.png
107	5	Productos de venta «especiales»	productos_de_venta_especial.py	ProductosDeVentaEspecial	catalogo.png
108	2	Presupuestos a clientes	presupuestos.py	Presupuestos	presupuesto.png
109	6	Informe de marcado CE	consulta_marcado_ce.py	ConsultaMarcadoCE	informe.png
111	6	Facturado y beneficio	consulta_beneficio.py	ConsultaBeneficio	informe.png
110	1	IVA devengado y soportado	iva.py	IVA	aeat.png
112	1	Listado datos modelo 347	modelo_347.py	Modelo347	aeat.png
113	1	Recibos bancarios	recibos.py	Recibos	money.png
221	3	Terminal Punto de Venta	tpv.py	TPV	tpv.png
223	2	Lista de asistencia	up_asistencia.py	Asistencias	
224	2	Agenda	up_calendario.py	Calendario	
225	1	Facturación por lotes	up_facturar.py	FacturacionAuto	
226	1	Libro de facturas	consulta_libro_iva.py	ConsultaLibroIVA	aeat.png
35	5	Productos	productos_compra.py	ProductosCompra	catalogo.png
227	6	Informe diario	up_report_diario.py	ReportDiario	pdfmail.png
\.


--
-- Name: abono_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY abono
    ADD CONSTRAINT abono_pkey PRIMARY KEY (id);


--
-- Name: actividad_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY actividad
    ADD CONSTRAINT actividad_pkey PRIMARY KEY (id);


--
-- Name: albaran_de_entrada_de_abono_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY albaran_de_entrada_de_abono
    ADD CONSTRAINT albaran_de_entrada_de_abono_pkey PRIMARY KEY (id);


--
-- Name: albaran_entrada_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY albaran_entrada
    ADD CONSTRAINT albaran_entrada_pkey PRIMARY KEY (id);


--
-- Name: albaran_salida_numalbaran_key; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY albaran_salida
    ADD CONSTRAINT albaran_salida_numalbaran_key UNIQUE (numalbaran);


--
-- Name: albaran_salida_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY albaran_salida
    ADD CONSTRAINT albaran_salida_pkey PRIMARY KEY (id);


--
-- Name: alerta_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY alerta
    ADD CONSTRAINT alerta_pkey PRIMARY KEY (id);


--
-- Name: almacen_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY almacen
    ADD CONSTRAINT almacen_pkey PRIMARY KEY (id);


--
-- Name: asistencia_pkey; Type: CONSTRAINT; Schema: public; Owner: bogado; Tablespace: 
--

ALTER TABLE ONLY asistencia
    ADD CONSTRAINT asistencia_pkey PRIMARY KEY (id);


--
-- Name: ausencia_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY ausencia
    ADD CONSTRAINT ausencia_pkey PRIMARY KEY (id);


--
-- Name: baja_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY baja
    ADD CONSTRAINT baja_pkey PRIMARY KEY (id);


--
-- Name: calendario_laboral_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY calendario_laboral
    ADD CONSTRAINT calendario_laboral_pkey PRIMARY KEY (id);


--
-- Name: categoria_laboral_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY categoria_laboral
    ADD CONSTRAINT categoria_laboral_pkey PRIMARY KEY (id);


--
-- Name: categoria_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY categoria
    ADD CONSTRAINT categoria_pkey PRIMARY KEY (id);


--
-- Name: centro_trabajo_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY centro_trabajo
    ADD CONSTRAINT centro_trabajo_pkey PRIMARY KEY (id);


--
-- Name: cliente_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY cliente
    ADD CONSTRAINT cliente_pkey PRIMARY KEY (id);


--
-- Name: cobro_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY cobro
    ADD CONSTRAINT cobro_pkey PRIMARY KEY (id);


--
-- Name: confirming_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY confirming
    ADD CONSTRAINT confirming_pkey PRIMARY KEY (id);


--
-- Name: contador_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY contador
    ADD CONSTRAINT contador_pkey PRIMARY KEY (id);


--
-- Name: cuenta_bancaria_cliente_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY cuenta_bancaria_cliente
    ADD CONSTRAINT cuenta_bancaria_cliente_pkey PRIMARY KEY (id);


--
-- Name: cuenta_destino_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY cuenta_destino
    ADD CONSTRAINT cuenta_destino_pkey PRIMARY KEY (id);


--
-- Name: cuenta_origen_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY cuenta_origen
    ADD CONSTRAINT cuenta_origen_pkey PRIMARY KEY (id);


--
-- Name: datos_de_la_empresa_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY datos_de_la_empresa
    ADD CONSTRAINT datos_de_la_empresa_pkey PRIMARY KEY (id);


--
-- Name: destino_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY destino
    ADD CONSTRAINT destino_pkey PRIMARY KEY (id);


--
-- Name: documento_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY documento
    ADD CONSTRAINT documento_pkey PRIMARY KEY (id);


--
-- Name: empleado_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY empleado
    ADD CONSTRAINT empleado_pkey PRIMARY KEY (id);


--
-- Name: estadistica_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY estadistica
    ADD CONSTRAINT estadistica_pkey PRIMARY KEY (id);


--
-- Name: evento_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY evento
    ADD CONSTRAINT evento_pkey PRIMARY KEY (id);


--
-- Name: factura_compra_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY factura_compra
    ADD CONSTRAINT factura_compra_pkey PRIMARY KEY (id);


--
-- Name: factura_de_abono_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY factura_de_abono
    ADD CONSTRAINT factura_de_abono_pkey PRIMARY KEY (id);


--
-- Name: factura_venta_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY factura_venta
    ADD CONSTRAINT factura_venta_pkey PRIMARY KEY (id);


--
-- Name: festivo_generico_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY festivo_generico
    ADD CONSTRAINT festivo_generico_pkey PRIMARY KEY (id);


--
-- Name: festivo_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY festivo
    ADD CONSTRAINT festivo_pkey PRIMARY KEY (id);


--
-- Name: grupo_alumnos_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY grupo_alumnos
    ADD CONSTRAINT grupo_alumnos_pkey PRIMARY KEY (id);


--
-- Name: grupo_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY grupo
    ADD CONSTRAINT grupo_pkey PRIMARY KEY (id);


--
-- Name: historial_existencias_compra_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY historial_existencias_compra
    ADD CONSTRAINT historial_existencias_compra_pkey PRIMARY KEY (id);


--
-- Name: id_reciente_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY id_reciente
    ADD CONSTRAINT id_reciente_pkey PRIMARY KEY (id);


--
-- Name: laborable_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY laborable
    ADD CONSTRAINT laborable_pkey PRIMARY KEY (id);


--
-- Name: linea_de_abono_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY linea_de_abono
    ADD CONSTRAINT linea_de_abono_pkey PRIMARY KEY (id);


--
-- Name: linea_de_compra_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY linea_de_compra
    ADD CONSTRAINT linea_de_compra_pkey PRIMARY KEY (id);


--
-- Name: linea_de_devolucion_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY linea_de_devolucion
    ADD CONSTRAINT linea_de_devolucion_pkey PRIMARY KEY (id);


--
-- Name: linea_de_pedido_de_compra_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY linea_de_pedido_de_compra
    ADD CONSTRAINT linea_de_pedido_de_compra_pkey PRIMARY KEY (id);


--
-- Name: linea_de_pedido_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY linea_de_pedido
    ADD CONSTRAINT linea_de_pedido_pkey PRIMARY KEY (id);


--
-- Name: linea_de_venta_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY linea_de_venta
    ADD CONSTRAINT linea_de_venta_pkey PRIMARY KEY (id);


--
-- Name: lista_objetos_recientes_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY lista_objetos_recientes
    ADD CONSTRAINT lista_objetos_recientes_pkey PRIMARY KEY (id);


--
-- Name: memo_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY memo
    ADD CONSTRAINT memo_pkey PRIMARY KEY (id);


--
-- Name: modulo_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY modulo
    ADD CONSTRAINT modulo_pkey PRIMARY KEY (id);


--
-- Name: motivo_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY motivo
    ADD CONSTRAINT motivo_pkey PRIMARY KEY (id);


--
-- Name: nomina_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY nomina
    ADD CONSTRAINT nomina_pkey PRIMARY KEY (id);


--
-- Name: nota_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY nota
    ADD CONSTRAINT nota_pkey PRIMARY KEY (id);


--
-- Name: observaciones_nominas_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY observaciones_nominas
    ADD CONSTRAINT observaciones_nominas_pkey PRIMARY KEY (id);


--
-- Name: orden_empleados_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY orden_empleados
    ADD CONSTRAINT orden_empleados_pkey PRIMARY KEY (id);


--
-- Name: padecimiento_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY padecimiento
    ADD CONSTRAINT padecimiento_pkey PRIMARY KEY (id);


--
-- Name: pagare_cobro_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY pagare_cobro
    ADD CONSTRAINT pagare_cobro_pkey PRIMARY KEY (id);


--
-- Name: pagare_pago_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY pagare_pago
    ADD CONSTRAINT pagare_pago_pkey PRIMARY KEY (id);


--
-- Name: pago_de_abono_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY pago_de_abono
    ADD CONSTRAINT pago_de_abono_pkey PRIMARY KEY (id);


--
-- Name: pago_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY pago
    ADD CONSTRAINT pago_pkey PRIMARY KEY (id);


--
-- Name: pedido_compra_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY pedido_compra
    ADD CONSTRAINT pedido_compra_pkey PRIMARY KEY (id);


--
-- Name: pedido_venta_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY pedido_venta
    ADD CONSTRAINT pedido_venta_pkey PRIMARY KEY (id);


--
-- Name: permiso_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY permiso
    ADD CONSTRAINT permiso_pkey PRIMARY KEY (id);


--
-- Name: precio_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY precio
    ADD CONSTRAINT precio_pkey PRIMARY KEY (id);


--
-- Name: prefactura_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY prefactura
    ADD CONSTRAINT prefactura_pkey PRIMARY KEY (id);


--
-- Name: presupuesto_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY presupuesto
    ADD CONSTRAINT presupuesto_pkey PRIMARY KEY (id);


--
-- Name: producto_compra_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY producto_compra
    ADD CONSTRAINT producto_compra_pkey PRIMARY KEY (id);


--
-- Name: proveedor_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY proveedor
    ADD CONSTRAINT proveedor_pkey PRIMARY KEY (id);


--
-- Name: recibo_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY recibo
    ADD CONSTRAINT recibo_pkey PRIMARY KEY (id);


--
-- Name: servicio_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY servicio
    ADD CONSTRAINT servicio_pkey PRIMARY KEY (id);


--
-- Name: servicio_tomado_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY servicio_tomado
    ADD CONSTRAINT servicio_tomado_pkey PRIMARY KEY (id);


--
-- Name: stock_almacen_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY stock_almacen
    ADD CONSTRAINT stock_almacen_pkey PRIMARY KEY (id);


--
-- Name: tarea_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY tarea
    ADD CONSTRAINT tarea_pkey PRIMARY KEY (id);


--
-- Name: tarifa_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY tarifa
    ADD CONSTRAINT tarifa_pkey PRIMARY KEY (id);


--
-- Name: ticket_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY ticket
    ADD CONSTRAINT ticket_pkey PRIMARY KEY (id);


--
-- Name: tipo_de_material_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY tipo_de_material
    ADD CONSTRAINT tipo_de_material_pkey PRIMARY KEY (id);


--
-- Name: transporte_a_cuenta_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY transporte_a_cuenta
    ADD CONSTRAINT transporte_a_cuenta_pkey PRIMARY KEY (id);


--
-- Name: transportista_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY transportista
    ADD CONSTRAINT transportista_pkey PRIMARY KEY (id);


--
-- Name: turno_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY turno
    ADD CONSTRAINT turno_pkey PRIMARY KEY (id);


--
-- Name: usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (id);


--
-- Name: usuario_usuario_key; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY usuario
    ADD CONSTRAINT usuario_usuario_key UNIQUE (usuario);


--
-- Name: vacaciones_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY vacaciones
    ADD CONSTRAINT vacaciones_pkey PRIMARY KEY (id);


--
-- Name: vencimiento_cobro_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY vencimiento_cobro
    ADD CONSTRAINT vencimiento_cobro_pkey PRIMARY KEY (id);


--
-- Name: vencimiento_pago_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY vencimiento_pago
    ADD CONSTRAINT vencimiento_pago_pkey PRIMARY KEY (id);


--
-- Name: ventana_pkey; Type: CONSTRAINT; Schema: public; Owner: pilates; Tablespace: 
--

ALTER TABLE ONLY ventana
    ADD CONSTRAINT ventana_pkey PRIMARY KEY (id);


--
-- Name: aid; Type: INDEX; Schema: public; Owner: pilates; Tablespace: 
--

CREATE INDEX aid ON stock_almacen USING btree (almacen_id);


--
-- Name: cliid; Type: INDEX; Schema: public; Owner: pilates; Tablespace: 
--

CREATE INDEX cliid ON albaran_salida USING btree (cliente_id);


--
-- Name: hec; Type: INDEX; Schema: public; Owner: pilates; Tablespace: 
--

CREATE UNIQUE INDEX hec ON historial_existencias_compra USING btree (producto_compra_id, almacen_id, fecha);


--
-- Name: prcid; Type: INDEX; Schema: public; Owner: pilates; Tablespace: 
--

CREATE INDEX prcid ON stock_almacen USING btree (producto_compra_id);


--
-- Name: prcid_aid; Type: INDEX; Schema: public; Owner: pilates; Tablespace: 
--

CREATE UNIQUE INDEX prcid_aid ON stock_almacen USING btree (producto_compra_id, almacen_id);


--
-- Name: tr_un_solo_almacen_ppal_pero_el_ultimo; Type: TRIGGER; Schema: public; Owner: pilates
--

CREATE TRIGGER tr_un_solo_almacen_ppal_pero_el_ultimo
    BEFORE INSERT OR UPDATE ON almacen
    FOR EACH ROW
    EXECUTE PROCEDURE un_solo_almacen_ppal_pero_el_ultimo();


--
-- Name: abono_almacen_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY abono
    ADD CONSTRAINT abono_almacen_id_fkey FOREIGN KEY (almacen_id) REFERENCES almacen(id);


--
-- Name: abono_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY abono
    ADD CONSTRAINT abono_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES cliente(id);


--
-- Name: abono_factura_de_abono_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY abono
    ADD CONSTRAINT abono_factura_de_abono_id_fkey FOREIGN KEY (factura_de_abono_id) REFERENCES factura_de_abono(id);


--
-- Name: actividad_evento_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY actividad
    ADD CONSTRAINT actividad_evento_id_fkey FOREIGN KEY (evento_id) REFERENCES evento(id);


--
-- Name: actividad_grupo_alumnos_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY actividad
    ADD CONSTRAINT actividad_grupo_alumnos_id_fkey FOREIGN KEY (grupo_alumnos_id) REFERENCES grupo_alumnos(id);


--
-- Name: albaran_entrada_almacen_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY albaran_entrada
    ADD CONSTRAINT albaran_entrada_almacen_id_fkey FOREIGN KEY (almacen_id) REFERENCES almacen(id);


--
-- Name: albaran_entrada_proveedor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY albaran_entrada
    ADD CONSTRAINT albaran_entrada_proveedor_id_fkey FOREIGN KEY (proveedor_id) REFERENCES proveedor(id);


--
-- Name: albaran_entrada_transportista_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY albaran_entrada
    ADD CONSTRAINT albaran_entrada_transportista_id_fkey FOREIGN KEY (transportista_id) REFERENCES transportista(id);


--
-- Name: albaran_salida_almacen_destino_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY albaran_salida
    ADD CONSTRAINT albaran_salida_almacen_destino_id_fkey FOREIGN KEY (almacen_destino_id) REFERENCES almacen(id);


--
-- Name: albaran_salida_almacen_origen_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY albaran_salida
    ADD CONSTRAINT albaran_salida_almacen_origen_id_fkey FOREIGN KEY (almacen_origen_id) REFERENCES almacen(id);


--
-- Name: albaran_salida_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY albaran_salida
    ADD CONSTRAINT albaran_salida_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES cliente(id);


--
-- Name: albaran_salida_destino_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY albaran_salida
    ADD CONSTRAINT albaran_salida_destino_id_fkey FOREIGN KEY (destino_id) REFERENCES destino(id);


--
-- Name: albaran_salida_transportista_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY albaran_salida
    ADD CONSTRAINT albaran_salida_transportista_id_fkey FOREIGN KEY (transportista_id) REFERENCES transportista(id);


--
-- Name: alerta_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY alerta
    ADD CONSTRAINT alerta_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES usuario(id);


--
-- Name: asistencia_actividad_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bogado
--

ALTER TABLE ONLY asistencia
    ADD CONSTRAINT asistencia_actividad_id_fkey FOREIGN KEY (actividad_id) REFERENCES actividad(id);


--
-- Name: asistencia_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bogado
--

ALTER TABLE ONLY asistencia
    ADD CONSTRAINT asistencia_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES cliente(id);


--
-- Name: ausencia_empleado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY ausencia
    ADD CONSTRAINT ausencia_empleado_id_fkey FOREIGN KEY (empleado_id) REFERENCES empleado(id);


--
-- Name: ausencia_motivo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY ausencia
    ADD CONSTRAINT ausencia_motivo_id_fkey FOREIGN KEY (motivo_id) REFERENCES motivo(id);


--
-- Name: baja_empleado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY baja
    ADD CONSTRAINT baja_empleado_id_fkey FOREIGN KEY (empleado_id) REFERENCES empleado(id);


--
-- Name: centro_trabajo_almacen_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY centro_trabajo
    ADD CONSTRAINT centro_trabajo_almacen_id_fkey FOREIGN KEY (almacen_id) REFERENCES almacen(id);


--
-- Name: cliente_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY cliente
    ADD CONSTRAINT cliente_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES cliente(id);


--
-- Name: cliente_contador_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY cliente
    ADD CONSTRAINT cliente_contador_id_fkey FOREIGN KEY (contador_id) REFERENCES contador(id);


--
-- Name: cliente_cuenta_origen_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY cliente
    ADD CONSTRAINT cliente_cuenta_origen_id_fkey FOREIGN KEY (cuenta_origen_id) REFERENCES cuenta_origen(id);


--
-- Name: cliente_grupo_alumnos_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY cliente_grupo_alumnos
    ADD CONSTRAINT cliente_grupo_alumnos_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES cliente(id);


--
-- Name: cliente_grupo_alumnos_grupo_alumnos_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY cliente_grupo_alumnos
    ADD CONSTRAINT cliente_grupo_alumnos_grupo_alumnos_id_fkey FOREIGN KEY (grupo_alumnos_id) REFERENCES grupo_alumnos(id);


--
-- Name: cliente_proveedor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY cliente
    ADD CONSTRAINT cliente_proveedor_id_fkey FOREIGN KEY (proveedor_id) REFERENCES proveedor(id);


--
-- Name: cliente_tarifa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY cliente
    ADD CONSTRAINT cliente_tarifa_id_fkey FOREIGN KEY (tarifa_id) REFERENCES tarifa(id);


--
-- Name: cobro_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY cobro
    ADD CONSTRAINT cobro_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES cliente(id);


--
-- Name: cobro_confirming_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY cobro
    ADD CONSTRAINT cobro_confirming_id_fkey FOREIGN KEY (confirming_id) REFERENCES confirming(id);


--
-- Name: cobro_factura_de_abono_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY cobro
    ADD CONSTRAINT cobro_factura_de_abono_id_fkey FOREIGN KEY (factura_de_abono_id) REFERENCES factura_de_abono(id);


--
-- Name: cobro_factura_venta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY cobro
    ADD CONSTRAINT cobro_factura_venta_id_fkey FOREIGN KEY (factura_venta_id) REFERENCES factura_venta(id);


--
-- Name: cobro_pagare_cobro_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY cobro
    ADD CONSTRAINT cobro_pagare_cobro_id_fkey FOREIGN KEY (pagare_cobro_id) REFERENCES pagare_cobro(id);


--
-- Name: cobro_prefactura_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY cobro
    ADD CONSTRAINT cobro_prefactura_id_fkey FOREIGN KEY (prefactura_id) REFERENCES prefactura(id);


--
-- Name: cuenta_bancaria_cliente_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY cuenta_bancaria_cliente
    ADD CONSTRAINT cuenta_bancaria_cliente_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES cliente(id);


--
-- Name: cuenta_destino_proveedor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY cuenta_destino
    ADD CONSTRAINT cuenta_destino_proveedor_id_fkey FOREIGN KEY (proveedor_id) REFERENCES proveedor(id);


--
-- Name: documento_albaran_entrada_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY documento
    ADD CONSTRAINT documento_albaran_entrada_id_fkey FOREIGN KEY (albaran_entrada_id) REFERENCES albaran_entrada(id);


--
-- Name: documento_albaran_salida_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY documento
    ADD CONSTRAINT documento_albaran_salida_id_fkey FOREIGN KEY (albaran_salida_id) REFERENCES albaran_salida(id);


--
-- Name: documento_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY documento
    ADD CONSTRAINT documento_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES cliente(id);


--
-- Name: documento_confirming_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY documento
    ADD CONSTRAINT documento_confirming_id_fkey FOREIGN KEY (confirming_id) REFERENCES confirming(id);


--
-- Name: documento_empleado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY documento
    ADD CONSTRAINT documento_empleado_id_fkey FOREIGN KEY (empleado_id) REFERENCES empleado(id);


--
-- Name: documento_factura_compra_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY documento
    ADD CONSTRAINT documento_factura_compra_id_fkey FOREIGN KEY (factura_compra_id) REFERENCES factura_compra(id);


--
-- Name: documento_factura_venta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY documento
    ADD CONSTRAINT documento_factura_venta_id_fkey FOREIGN KEY (factura_venta_id) REFERENCES factura_venta(id);


--
-- Name: documento_pagare_cobro_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY documento
    ADD CONSTRAINT documento_pagare_cobro_id_fkey FOREIGN KEY (pagare_cobro_id) REFERENCES pagare_cobro(id);


--
-- Name: documento_pagare_pago_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY documento
    ADD CONSTRAINT documento_pagare_pago_id_fkey FOREIGN KEY (pagare_pago_id) REFERENCES pagare_pago(id);


--
-- Name: documento_pedido_compra_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY documento
    ADD CONSTRAINT documento_pedido_compra_id_fkey FOREIGN KEY (pedido_compra_id) REFERENCES pedido_compra(id);


--
-- Name: documento_pedido_venta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY documento
    ADD CONSTRAINT documento_pedido_venta_id_fkey FOREIGN KEY (pedido_venta_id) REFERENCES pedido_venta(id);


--
-- Name: documento_prefactura_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY documento
    ADD CONSTRAINT documento_prefactura_id_fkey FOREIGN KEY (prefactura_id) REFERENCES prefactura(id);


--
-- Name: documento_proveedor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY documento
    ADD CONSTRAINT documento_proveedor_id_fkey FOREIGN KEY (proveedor_id) REFERENCES proveedor(id);


--
-- Name: empleado_categoria_laboral_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY empleado
    ADD CONSTRAINT empleado_categoria_laboral_id_fkey FOREIGN KEY (categoria_laboral_id) REFERENCES categoria_laboral(id);


--
-- Name: empleado_centro_trabajo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY empleado
    ADD CONSTRAINT empleado_centro_trabajo_id_fkey FOREIGN KEY (centro_trabajo_id) REFERENCES centro_trabajo(id);


--
-- Name: empleado_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY empleado
    ADD CONSTRAINT empleado_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES usuario(id);


--
-- Name: estadistica_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY estadistica
    ADD CONSTRAINT estadistica_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES usuario(id);


--
-- Name: estadistica_ventana_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY estadistica
    ADD CONSTRAINT estadistica_ventana_id_fkey FOREIGN KEY (ventana_id) REFERENCES ventana(id);


--
-- Name: factura_compra_proveedor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY factura_compra
    ADD CONSTRAINT factura_compra_proveedor_id_fkey FOREIGN KEY (proveedor_id) REFERENCES proveedor(id);


--
-- Name: factura_venta_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY factura_venta
    ADD CONSTRAINT factura_venta_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES cliente(id);


--
-- Name: festivo_calendario_laboral_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY festivo
    ADD CONSTRAINT festivo_calendario_laboral_id_fkey FOREIGN KEY (calendario_laboral_id) REFERENCES calendario_laboral(id);


--
-- Name: grupo_alumnos_empleado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY grupo_alumnos
    ADD CONSTRAINT grupo_alumnos_empleado_id_fkey FOREIGN KEY (empleado_id) REFERENCES empleado(id);


--
-- Name: grupo_jefeturno_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY grupo
    ADD CONSTRAINT grupo_jefeturno_id_fkey FOREIGN KEY (jefeturno_id) REFERENCES empleado(id);


--
-- Name: grupo_operario1_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY grupo
    ADD CONSTRAINT grupo_operario1_id_fkey FOREIGN KEY (operario1_id) REFERENCES empleado(id);


--
-- Name: grupo_operario2_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY grupo
    ADD CONSTRAINT grupo_operario2_id_fkey FOREIGN KEY (operario2_id) REFERENCES empleado(id);


--
-- Name: historial_existencias_compra_almacen_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY historial_existencias_compra
    ADD CONSTRAINT historial_existencias_compra_almacen_id_fkey FOREIGN KEY (almacen_id) REFERENCES almacen(id);


--
-- Name: historial_existencias_compra_producto_compra_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY historial_existencias_compra
    ADD CONSTRAINT historial_existencias_compra_producto_compra_id_fkey FOREIGN KEY (producto_compra_id) REFERENCES producto_compra(id);


--
-- Name: id_reciente_lista_objetos_recientes_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY id_reciente
    ADD CONSTRAINT id_reciente_lista_objetos_recientes_id_fkey FOREIGN KEY (lista_objetos_recientes_id) REFERENCES lista_objetos_recientes(id);


--
-- Name: laborable_calendario_laboral_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY laborable
    ADD CONSTRAINT laborable_calendario_laboral_id_fkey FOREIGN KEY (calendario_laboral_id) REFERENCES calendario_laboral(id);


--
-- Name: laborable_grupo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY laborable
    ADD CONSTRAINT laborable_grupo_id_fkey FOREIGN KEY (grupo_id) REFERENCES grupo(id);


--
-- Name: laborable_turno_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY laborable
    ADD CONSTRAINT laborable_turno_id_fkey FOREIGN KEY (turno_id) REFERENCES turno(id);


--
-- Name: linea_de_abono_abono_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY linea_de_abono
    ADD CONSTRAINT linea_de_abono_abono_id_fkey FOREIGN KEY (abono_id) REFERENCES abono(id);


--
-- Name: linea_de_abono_linea_de_venta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY linea_de_abono
    ADD CONSTRAINT linea_de_abono_linea_de_venta_id_fkey FOREIGN KEY (linea_de_venta_id) REFERENCES linea_de_venta(id);


--
-- Name: linea_de_abono_servicio_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY linea_de_abono
    ADD CONSTRAINT linea_de_abono_servicio_id_fkey FOREIGN KEY (servicio_id) REFERENCES servicio(id);


--
-- Name: linea_de_compra_albaran_entrada_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY linea_de_compra
    ADD CONSTRAINT linea_de_compra_albaran_entrada_id_fkey FOREIGN KEY (albaran_entrada_id) REFERENCES albaran_entrada(id);


--
-- Name: linea_de_compra_factura_compra_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY linea_de_compra
    ADD CONSTRAINT linea_de_compra_factura_compra_id_fkey FOREIGN KEY (factura_compra_id) REFERENCES factura_compra(id);


--
-- Name: linea_de_compra_pedido_compra_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY linea_de_compra
    ADD CONSTRAINT linea_de_compra_pedido_compra_id_fkey FOREIGN KEY (pedido_compra_id) REFERENCES pedido_compra(id);


--
-- Name: linea_de_compra_producto_compra_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY linea_de_compra
    ADD CONSTRAINT linea_de_compra_producto_compra_id_fkey FOREIGN KEY (producto_compra_id) REFERENCES producto_compra(id);


--
-- Name: linea_de_devolucion_abono_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY linea_de_devolucion
    ADD CONSTRAINT linea_de_devolucion_abono_id_fkey FOREIGN KEY (abono_id) REFERENCES abono(id);


--
-- Name: linea_de_devolucion_albaran_de_entrada_de_abono_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY linea_de_devolucion
    ADD CONSTRAINT linea_de_devolucion_albaran_de_entrada_de_abono_id_fkey FOREIGN KEY (albaran_de_entrada_de_abono_id) REFERENCES albaran_de_entrada_de_abono(id);


--
-- Name: linea_de_devolucion_albaran_salida_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY linea_de_devolucion
    ADD CONSTRAINT linea_de_devolucion_albaran_salida_id_fkey FOREIGN KEY (albaran_salida_id) REFERENCES albaran_salida(id);


--
-- Name: linea_de_pedido_de_compra__li_linea_de_pedido_de_compra_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY linea_de_pedido_de_compra__linea_de_compra
    ADD CONSTRAINT linea_de_pedido_de_compra__li_linea_de_pedido_de_compra_id_fkey FOREIGN KEY (linea_de_pedido_de_compra_id) REFERENCES linea_de_pedido_de_compra(id);


--
-- Name: linea_de_pedido_de_compra__linea_de_com_linea_de_compra_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY linea_de_pedido_de_compra__linea_de_compra
    ADD CONSTRAINT linea_de_pedido_de_compra__linea_de_com_linea_de_compra_id_fkey FOREIGN KEY (linea_de_compra_id) REFERENCES linea_de_compra(id);


--
-- Name: linea_de_pedido_de_compra_pedido_compra_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY linea_de_pedido_de_compra
    ADD CONSTRAINT linea_de_pedido_de_compra_pedido_compra_id_fkey FOREIGN KEY (pedido_compra_id) REFERENCES pedido_compra(id);


--
-- Name: linea_de_pedido_de_compra_producto_compra_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY linea_de_pedido_de_compra
    ADD CONSTRAINT linea_de_pedido_de_compra_producto_compra_id_fkey FOREIGN KEY (producto_compra_id) REFERENCES producto_compra(id);


--
-- Name: linea_de_pedido_pedido_venta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY linea_de_pedido
    ADD CONSTRAINT linea_de_pedido_pedido_venta_id_fkey FOREIGN KEY (pedido_venta_id) REFERENCES pedido_venta(id);


--
-- Name: linea_de_pedido_presupuesto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY linea_de_pedido
    ADD CONSTRAINT linea_de_pedido_presupuesto_id_fkey FOREIGN KEY (presupuesto_id) REFERENCES presupuesto(id);


--
-- Name: linea_de_pedido_producto_compra_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY linea_de_pedido
    ADD CONSTRAINT linea_de_pedido_producto_compra_id_fkey FOREIGN KEY (producto_compra_id) REFERENCES producto_compra(id);


--
-- Name: linea_de_venta_albaran_salida_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY linea_de_venta
    ADD CONSTRAINT linea_de_venta_albaran_salida_id_fkey FOREIGN KEY (albaran_salida_id) REFERENCES albaran_salida(id);


--
-- Name: linea_de_venta_factura_venta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY linea_de_venta
    ADD CONSTRAINT linea_de_venta_factura_venta_id_fkey FOREIGN KEY (factura_venta_id) REFERENCES factura_venta(id);


--
-- Name: linea_de_venta_pedido_venta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY linea_de_venta
    ADD CONSTRAINT linea_de_venta_pedido_venta_id_fkey FOREIGN KEY (pedido_venta_id) REFERENCES pedido_venta(id);


--
-- Name: linea_de_venta_prefactura_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY linea_de_venta
    ADD CONSTRAINT linea_de_venta_prefactura_id_fkey FOREIGN KEY (prefactura_id) REFERENCES prefactura(id);


--
-- Name: linea_de_venta_producto_compra_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY linea_de_venta
    ADD CONSTRAINT linea_de_venta_producto_compra_id_fkey FOREIGN KEY (producto_compra_id) REFERENCES producto_compra(id);


--
-- Name: linea_de_venta_ticket_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY linea_de_venta
    ADD CONSTRAINT linea_de_venta_ticket_id_fkey FOREIGN KEY (ticket_id) REFERENCES ticket(id);


--
-- Name: lista_objetos_recientes_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY lista_objetos_recientes
    ADD CONSTRAINT lista_objetos_recientes_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES usuario(id);


--
-- Name: lista_objetos_recientes_ventana_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY lista_objetos_recientes
    ADD CONSTRAINT lista_objetos_recientes_ventana_id_fkey FOREIGN KEY (ventana_id) REFERENCES ventana(id);


--
-- Name: memo_categoria_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY memo
    ADD CONSTRAINT memo_categoria_id_fkey FOREIGN KEY (categoria_id) REFERENCES categoria(id);


--
-- Name: nomina_empleado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY nomina
    ADD CONSTRAINT nomina_empleado_id_fkey FOREIGN KEY (empleado_id) REFERENCES empleado(id);


--
-- Name: nota_factura_venta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY nota
    ADD CONSTRAINT nota_factura_venta_id_fkey FOREIGN KEY (factura_venta_id) REFERENCES factura_venta(id);


--
-- Name: orden_empleados_empleado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY orden_empleados
    ADD CONSTRAINT orden_empleados_empleado_id_fkey FOREIGN KEY (empleado_id) REFERENCES empleado(id);


--
-- Name: padecimiento_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY padecimiento
    ADD CONSTRAINT padecimiento_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES cliente(id);


--
-- Name: pago_cuenta_destino_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY pago
    ADD CONSTRAINT pago_cuenta_destino_id_fkey FOREIGN KEY (cuenta_destino_id) REFERENCES cuenta_destino(id);


--
-- Name: pago_cuenta_origen_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY pago
    ADD CONSTRAINT pago_cuenta_origen_id_fkey FOREIGN KEY (cuenta_origen_id) REFERENCES cuenta_origen(id);


--
-- Name: pago_de_abono_factura_de_abono_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY pago_de_abono
    ADD CONSTRAINT pago_de_abono_factura_de_abono_id_fkey FOREIGN KEY (factura_de_abono_id) REFERENCES factura_de_abono(id);


--
-- Name: pago_de_abono_factura_venta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY pago_de_abono
    ADD CONSTRAINT pago_de_abono_factura_venta_id_fkey FOREIGN KEY (factura_venta_id) REFERENCES factura_venta(id);


--
-- Name: pago_de_abono_prefactura_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY pago_de_abono
    ADD CONSTRAINT pago_de_abono_prefactura_id_fkey FOREIGN KEY (prefactura_id) REFERENCES prefactura(id);


--
-- Name: pago_factura_compra_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY pago
    ADD CONSTRAINT pago_factura_compra_id_fkey FOREIGN KEY (factura_compra_id) REFERENCES factura_compra(id);


--
-- Name: pago_pagare_pago_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY pago
    ADD CONSTRAINT pago_pagare_pago_id_fkey FOREIGN KEY (pagare_pago_id) REFERENCES pagare_pago(id);


--
-- Name: pago_proveedor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY pago
    ADD CONSTRAINT pago_proveedor_id_fkey FOREIGN KEY (proveedor_id) REFERENCES proveedor(id);


--
-- Name: pedido_compra_proveedor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY pedido_compra
    ADD CONSTRAINT pedido_compra_proveedor_id_fkey FOREIGN KEY (proveedor_id) REFERENCES proveedor(id);


--
-- Name: pedido_venta_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY pedido_venta
    ADD CONSTRAINT pedido_venta_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES cliente(id);


--
-- Name: pedido_venta_tarifa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY pedido_venta
    ADD CONSTRAINT pedido_venta_tarifa_id_fkey FOREIGN KEY (tarifa_id) REFERENCES tarifa(id);


--
-- Name: permiso_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY permiso
    ADD CONSTRAINT permiso_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES usuario(id);


--
-- Name: permiso_ventana_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY permiso
    ADD CONSTRAINT permiso_ventana_id_fkey FOREIGN KEY (ventana_id) REFERENCES ventana(id);


--
-- Name: precio_producto_compra_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY precio
    ADD CONSTRAINT precio_producto_compra_id_fkey FOREIGN KEY (producto_compra_id) REFERENCES producto_compra(id);


--
-- Name: precio_tarifa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY precio
    ADD CONSTRAINT precio_tarifa_id_fkey FOREIGN KEY (tarifa_id) REFERENCES tarifa(id);


--
-- Name: prefactura_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY prefactura
    ADD CONSTRAINT prefactura_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES cliente(id);


--
-- Name: presupuesto_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY presupuesto
    ADD CONSTRAINT presupuesto_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES cliente(id);


--
-- Name: producto_compra_tipo_de_material_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY producto_compra
    ADD CONSTRAINT producto_compra_tipo_de_material_id_fkey FOREIGN KEY (tipo_de_material_id) REFERENCES tipo_de_material(id);


--
-- Name: recibo_cuenta_bancaria_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY recibo
    ADD CONSTRAINT recibo_cuenta_bancaria_cliente_id_fkey FOREIGN KEY (cuenta_bancaria_cliente_id) REFERENCES cuenta_bancaria_cliente(id);


--
-- Name: recibo_cuenta_origen_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY recibo
    ADD CONSTRAINT recibo_cuenta_origen_id_fkey FOREIGN KEY (cuenta_origen_id) REFERENCES cuenta_origen(id);


--
-- Name: servicio_actividad_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY servicio
    ADD CONSTRAINT servicio_actividad_id_fkey FOREIGN KEY (actividad_id) REFERENCES actividad(id);


--
-- Name: servicio_albaran_salida_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY servicio
    ADD CONSTRAINT servicio_albaran_salida_id_fkey FOREIGN KEY (albaran_salida_id) REFERENCES albaran_salida(id);


--
-- Name: servicio_factura_venta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY servicio
    ADD CONSTRAINT servicio_factura_venta_id_fkey FOREIGN KEY (factura_venta_id) REFERENCES factura_venta(id);


--
-- Name: servicio_pedido_venta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY servicio
    ADD CONSTRAINT servicio_pedido_venta_id_fkey FOREIGN KEY (pedido_venta_id) REFERENCES pedido_venta(id);


--
-- Name: servicio_prefactura_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY servicio
    ADD CONSTRAINT servicio_prefactura_id_fkey FOREIGN KEY (prefactura_id) REFERENCES prefactura(id);


--
-- Name: servicio_presupuesto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY servicio
    ADD CONSTRAINT servicio_presupuesto_id_fkey FOREIGN KEY (presupuesto_id) REFERENCES presupuesto(id);


--
-- Name: servicio_tomado_factura_compra_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY servicio_tomado
    ADD CONSTRAINT servicio_tomado_factura_compra_id_fkey FOREIGN KEY (factura_compra_id) REFERENCES factura_compra(id);


--
-- Name: servicio_tomado_transporte_a_cuenta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY servicio_tomado
    ADD CONSTRAINT servicio_tomado_transporte_a_cuenta_id_fkey FOREIGN KEY (transporte_a_cuenta_id) REFERENCES transporte_a_cuenta(id);


--
-- Name: stock_almacen_almacen_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY stock_almacen
    ADD CONSTRAINT stock_almacen_almacen_id_fkey FOREIGN KEY (almacen_id) REFERENCES almacen(id);


--
-- Name: stock_almacen_producto_compra_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY stock_almacen
    ADD CONSTRAINT stock_almacen_producto_compra_id_fkey FOREIGN KEY (producto_compra_id) REFERENCES producto_compra(id);


--
-- Name: tarea_categoria_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY tarea
    ADD CONSTRAINT tarea_categoria_id_fkey FOREIGN KEY (categoria_id) REFERENCES categoria(id);


--
-- Name: transporte_a_cuenta_albaran_salida_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY transporte_a_cuenta
    ADD CONSTRAINT transporte_a_cuenta_albaran_salida_id_fkey FOREIGN KEY (albaran_salida_id) REFERENCES albaran_salida(id);


--
-- Name: transporte_a_cuenta_proveedor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY transporte_a_cuenta
    ADD CONSTRAINT transporte_a_cuenta_proveedor_id_fkey FOREIGN KEY (proveedor_id) REFERENCES proveedor(id);


--
-- Name: vacaciones_calendario_laboral_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY vacaciones
    ADD CONSTRAINT vacaciones_calendario_laboral_id_fkey FOREIGN KEY (calendario_laboral_id) REFERENCES calendario_laboral(id);


--
-- Name: vencimiento_cobro_cuenta_origen_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY vencimiento_cobro
    ADD CONSTRAINT vencimiento_cobro_cuenta_origen_id_fkey FOREIGN KEY (cuenta_origen_id) REFERENCES cuenta_origen(id);


--
-- Name: vencimiento_cobro_factura_venta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY vencimiento_cobro
    ADD CONSTRAINT vencimiento_cobro_factura_venta_id_fkey FOREIGN KEY (factura_venta_id) REFERENCES factura_venta(id);


--
-- Name: vencimiento_cobro_prefactura_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY vencimiento_cobro
    ADD CONSTRAINT vencimiento_cobro_prefactura_id_fkey FOREIGN KEY (prefactura_id) REFERENCES prefactura(id);


--
-- Name: vencimiento_cobro_recibo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY vencimiento_cobro
    ADD CONSTRAINT vencimiento_cobro_recibo_id_fkey FOREIGN KEY (recibo_id) REFERENCES recibo(id);


--
-- Name: vencimiento_pago_factura_compra_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY vencimiento_pago
    ADD CONSTRAINT vencimiento_pago_factura_compra_id_fkey FOREIGN KEY (factura_compra_id) REFERENCES factura_compra(id);


--
-- Name: ventana_modulo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pilates
--

ALTER TABLE ONLY ventana
    ADD CONSTRAINT ventana_modulo_id_fkey FOREIGN KEY (modulo_id) REFERENCES modulo(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- Name: asistencia; Type: ACL; Schema: public; Owner: bogado
--

REVOKE ALL ON TABLE asistencia FROM PUBLIC;
REVOKE ALL ON TABLE asistencia FROM bogado;
GRANT ALL ON TABLE asistencia TO bogado;
GRANT ALL ON TABLE asistencia TO pilates;


--
-- Name: asistencia_id_seq; Type: ACL; Schema: public; Owner: bogado
--

REVOKE ALL ON SEQUENCE asistencia_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE asistencia_id_seq FROM bogado;
GRANT ALL ON SEQUENCE asistencia_id_seq TO bogado;
GRANT ALL ON SEQUENCE asistencia_id_seq TO pilates;


--
-- PostgreSQL database dump complete
--

