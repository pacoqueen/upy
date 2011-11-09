--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

--
-- Name: actividad_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('actividad_id_seq', 331, true);


--
-- Name: albaran_entrada_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('albaran_entrada_id_seq', 5, true);


--
-- Name: albaran_salida_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('albaran_salida_id_seq', 3, true);


--
-- Name: alerta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('alerta_id_seq', 1, false);


--
-- Name: almacen_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('almacen_id_seq', 2, true);


--
-- Name: asistencia_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('asistencia_id_seq', 53, true);


--
-- Name: categoria_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('categoria_id_seq', 3, true);


--
-- Name: categoria_laboral_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('categoria_laboral_id_seq', 4, true);


--
-- Name: centro_trabajo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('centro_trabajo_id_seq', 1, false);


--
-- Name: clase_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('clase_id_seq', 23, true);


--
-- Name: cliente_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('cliente_id_seq', 595, false);


--
-- Name: cobro_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('cobro_id_seq', 6, true);


--
-- Name: confirming_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('confirming_id_seq', 1, false);


--
-- Name: contador_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('contador_id_seq', 2, true);


--
-- Name: cuenta_bancaria_cliente_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('cuenta_bancaria_cliente_id_seq', 3, true);


--
-- Name: cuenta_destino_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('cuenta_destino_id_seq', 2, true);


--
-- Name: cuenta_origen_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('cuenta_origen_id_seq', 2, true);


--
-- Name: datos_de_la_empresa_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('datos_de_la_empresa_id_seq', 5, true);


--
-- Name: destino_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('destino_id_seq', 1, true);


--
-- Name: documento_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('documento_id_seq', 1, true);


--
-- Name: empleado_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('empleado_id_seq', 9, true);


--
-- Name: estadistica_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('estadistica_id_seq', 97, true);


--
-- Name: evento_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('evento_id_seq', 3, true);


--
-- Name: factura_compra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('factura_compra_id_seq', 3, true);


--
-- Name: factura_venta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('factura_venta_id_seq', 34, true);


--
-- Name: festivo_generico_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('festivo_generico_id_seq', 1, false);


--
-- Name: grupo_alumnos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('grupo_alumnos_id_seq', 19, true);


--
-- Name: historial_existencias_compra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('historial_existencias_compra_id_seq', 86, true);


--
-- Name: id_reciente_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('id_reciente_id_seq', 3, true);


--
-- Name: linea_de_compra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('linea_de_compra_id_seq', 14, true);


--
-- Name: linea_de_pedido_de_compra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('linea_de_pedido_de_compra_id_seq', 8, true);


--
-- Name: linea_de_pedido_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('linea_de_pedido_id_seq', 3, true);


--
-- Name: linea_de_venta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('linea_de_venta_id_seq', 19, true);


--
-- Name: lista_objetos_recientes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('lista_objetos_recientes_id_seq', 3, true);


--
-- Name: maquina_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('maquina_id_seq', 1, false);


--
-- Name: memo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('memo_id_seq', 10, true);


--
-- Name: modulo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('modulo_id_seq', 1, false);


--
-- Name: nota_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('nota_id_seq', 1, false);


--
-- Name: padecimiento_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('padecimiento_id_seq', 6, true);


--
-- Name: pagare_cobro_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('pagare_cobro_id_seq', 2, true);


--
-- Name: pagare_pago_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('pagare_pago_id_seq', 2, true);


--
-- Name: pago_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('pago_id_seq', 2, true);


--
-- Name: pedido_compra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('pedido_compra_id_seq', 5, true);


--
-- Name: pedido_venta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('pedido_venta_id_seq', 3, true);


--
-- Name: permiso_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('permiso_id_seq', 165, true);


--
-- Name: precio_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('precio_id_seq', 21, true);


--
-- Name: prefactura_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('prefactura_id_seq', 1, false);


--
-- Name: presupuesto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('presupuesto_id_seq', 1, true);


--
-- Name: producto_compra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('producto_compra_id_seq', 26, true);


--
-- Name: producto_contratado_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('producto_contratado_id_seq', 3, true);


--
-- Name: proveedor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('proveedor_id_seq', 2, true);


--
-- Name: recibo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('recibo_id_seq', 3, true);


--
-- Name: servicio_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('servicio_id_seq', 222, true);


--
-- Name: servicio_tomado_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('servicio_tomado_id_seq', 1, true);


--
-- Name: stock_almacen_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('stock_almacen_id_seq', 8, true);


--
-- Name: tarea_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('tarea_id_seq', 8, true);


--
-- Name: tarifa_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('tarifa_id_seq', 1, true);


--
-- Name: ticket_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('ticket_id_seq', 13, true);


--
-- Name: tipo_de_material_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('tipo_de_material_id_seq', 6, true);


--
-- Name: transporte_a_cuenta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('transporte_a_cuenta_id_seq', 1, false);


--
-- Name: transportista_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('transportista_id_seq', 1, true);


--
-- Name: usuario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('usuario_id_seq', 2, true);


--
-- Name: vencimiento_cobro_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('vencimiento_cobro_id_seq', 16, true);


--
-- Name: vencimiento_pago_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('vencimiento_pago_id_seq', 2, true);


--
-- Name: ventana_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pilates
--

SELECT pg_catalog.setval('ventana_id_seq', 229, true);


--

--
-- Data for Name: tarifa; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY tarifa (id, nombre, observaciones, periodo_validez_ini, periodo_validez_fin) FROM stdin;
1	Tarifa venta	Tarifa estándar de venta.	\N	\N
\.



--
-- Data for Name: proveedor; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY proveedor (id, nombre, cif, direccion, pais, ciudad, provincia, cp, telefono, fax, contacto, observaciones, direccionfacturacion, paisfacturacion, ciudadfacturacion, provinciafacturacion, cpfacturacion, email, formadepago, documentodepago, vencimiento, diadepago, correoe, web, banco, swif, iban, cuenta, inhabilitado, motivo, iva, nombre_banco) FROM stdin;
1	Universal Pilates	PENDIENTE																0	Recibo domicilado	0	0							f		0.18	
\.



--
-- Data for Name: transportista; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY transportista (id, agencia, nombre, dni, telefono, matricula) FROM stdin;
1					
\.



--
-- Data for Name: destino; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY destino (id, nombre, direccion, cp, ciudad, telefono, pais) FROM stdin;
1						
\.



--
-- Data for Name: pedido_compra; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY pedido_compra (id, proveedor_id, fecha, numpedido, iva, descuento, entregas, forma_de_pago, observaciones, bloqueado, cerrado, direccion_entrega0, direccion_entrega1, direccion_entrega2, responsable0, responsable1, portes0, portes1, observaciones0, observaciones1, observaciones2) FROM stdin;
5	1	2010-03-10	1	0.18	0.050000000000000003	Entregar por las mañanas.	PAGO A 120 DÍAS F.F. PAGO LOS 25.		t	f	Universal Pilates Vitality Studio	C/ Dirección postal	00000 Marbella (Marbella), España	Responsable De Compras 000 00 00 00	resposable@compras.com	PORTES PAGADOS	ENTREGA EN NUESTRA FÁBRICA DE MARBELLA	ROGAMOS NOS REMITAN COPIA DE ESTE PEDIDO SELLADO Y FIRMADO POR UDS.	ESTA MERCANCIA SE DEBE ENTREGAR...	PAGO A 120 DÍAS F.F. PAGO LOS 25.
\.



--
-- Data for Name: tipo_de_material; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY tipo_de_material (id, descripcion) FROM stdin;
1	Máquinas gimnasio
2	Accesorios gimnasio
4	Ropa deportiva
5	Alimentación
6	Clases
\.



--
-- Data for Name: producto_compra; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY producto_compra (id, tipo_de_material_id, descripcion, codigo, unidad, minimo, existencias, precio_defecto, control_existencias, fvaloracion, observaciones, obsoleto) FROM stdin;
4	1	Magic Circle	0005	ud.	1	30	200	t			f
1	2	Pelota Pilates (TM)	0001	ud.	10	56	25	t			f
5	1	Pedi Pole	0008	ud.	2	1	500	t			f
9	6	BONO 10 PRIVADAS HORAS VALLE		ud.	0	0	400	f			f
16	6	GRUPO 3 PAX 1 DIA SEMANA		ud.	0	0	100	f			f
8	6	BONO 10 PRIVADAS		ud.	0	0	525	f			f
6	6	Curso de iniciación + 1 mes en grupo	CINI1		0	0	150	f			f
7	6	Clases privadas viernes (borrar)	PRUEBA	ud.	0	0	0	f			f
11	6	BONO 10 PRIVADAS MASTER TRAINER		ud.	0	0	630	f			f
25	6	GR 6 PAX 5 X SEMANA		ud.	0	0	250	f			f
14	6	BONO 10 SEMIPRIVADAS (2 pax)			0	0	375	f			f
21	6	GRUPO 6 PAX 2 X SEMANA		ud.	0	0	130	f			f
17	6	GRUPO 3 PAX 3 VECES X SEMANA		ud.	0	0	270	f			f
12	6	CLASE PRIVADA		ud.	0	0	65	f			f
18	6	GRUPO 3 PAX 4 DIAS X SEMANA		ud.	0	0	340	f			f
26	6	GRUPO 1 DIA PILATES 1 DIA PP		ud.	0	0	80	f			f
22	6	GRUPO 6 PAX 3 X SEMANA		ud.	0	0	180	f			f
3	4	Camiseta elástica	0003	ud.	0	29	45	t			f
13	6	CLASE PRIVADA MASTER TRAINER		ud.	0	0	75	f			f
23	6			ud.	0	0	0	t			f
10	6	BONO 10 PRIVADAS POWER PLATE		ud.	0	0	400	f			f
15	6	GRUPO 3 PAX 2 VECES X SEMANA		ud.	0	0	190	f			f
19	6	GRUPO 3 PAX 5 X SEMANA		ud.	0	0	410	f			f
24	6	GRUPO 6 PAX 4 X SEMANA		ud.	0	0	215	f			f
20	6	GRUPO 6 PAX 1 DIA SEMANA		ud.	0	0	80	f			f
\.



--
-- Data for Name: clase; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY clase (id, producto_compra_id, num_clases_mes, num_clases_semana, pax, dia_semana, master_trainer, caducidad, num_clases_totales) FROM stdin;
2	6	8	3	0	MLX    	f	120	8
13	16	4	1	3	\N	f	120	4
21	25	20	5	6	\N	f	120	20
1	6	3	1	1	\N	f	120	3
22	26	8	2	6	\N	f	120	8
14	17	12	3	3	\N	f	120	12
8	11	1	1	1	\N	f	120	10
7	10	10	1	1	\N	f	120	10
6	9	10	1	1	\N	f	120	10
4	8	10	1	1	\N	f	120	10
15	18	16	4	3	\N	f	120	16
9	12	0	0	1	\N	f	120	1
10	13	0	0	1	\N	f	120	1
16	19	20	5	3	\N	f	120	20
11	14	0	0	2	\N	f	120	10
17	20	4	1	6	\N	f	120	4
12	15	8	2	3	\N	f	120	8
18	21	8	2	6	\N	f	120	8
19	22	12	3	6	\N	f	120	12
20	24	16	4	6	\N	f	120	16
\.



--
-- Data for Name: precio; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY precio (id, tarifa_id, precio, producto_compra_id) FROM stdin;
1	1	520	5
3	1	150	6
4	1	525	8
5	1	400	9
6	1	400	10
7	1	630	11
8	1	65	12
9	1	75	13
10	1	375	14
11	1	190	15
12	1	100	16
13	1	270	17
14	1	340	18
15	1	410	19
16	1	80	20
17	1	130	21
18	1	180	22
19	1	215	24
20	1	250	25
21	1	80	26
\.



--
-- Data for Name: categoria_laboral; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY categoria_laboral (id, codigo, puesto, da_clases) FROM stdin;
1	PPN1	Profesor Pilates nivel 1	t
4	PPN2	Profesor Pilates nivel 2	t
3	SLS	Tienda	f
2	ADM	Administrativo	f
\.



-- Data for Name: almacen; Type: TABLE DATA; Schema: public; Owner: pilates
-- Data for Name: almacen; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY almacen (id, nombre, observaciones, direccion, ciudad, provincia, cp, telefono, fax, email, pais, principal) FROM stdin;
1	Almacén principal de Vitality Studio			Marbella						España	t
2	Almacén de distribución				Sevilla					España	f
\.



--
-- Data for Name: albaran_entrada; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY albaran_entrada (id, proveedor_id, fecha, numalbaran, bloqueado, repuestos, almacen_id, transportista_id) FROM stdin;
4	1	2010-03-10	5214	f	f	1	\N
5	1	2010-03-24	123	f	f	1	\N
\.



--
-- Data for Name: historial_existencias_compra; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY historial_existencias_compra (id, producto_compra_id, fecha, cantidad, observaciones, almacen_id) FROM stdin;
1	3	2009-02-01	-3	Cacheado automáticamente	1
2	3	2009-02-01	0	Cacheado automáticamente	2
5	1	2009-02-01	-1	Cacheado automáticamente	1
6	1	2009-02-01	0	Cacheado automáticamente	2
7	3	2009-03-01	-3	Cacheado automáticamente	1
8	3	2009-03-01	0	Cacheado automáticamente	2
11	1	2009-03-01	-1	Cacheado automáticamente	1
12	1	2009-03-01	0	Cacheado automáticamente	2
13	3	2009-04-01	-3	Cacheado automáticamente	1
14	3	2009-04-01	0	Cacheado automáticamente	2
17	1	2009-04-01	-1	Cacheado automáticamente	1
18	1	2009-04-01	0	Cacheado automáticamente	2
19	3	2009-05-01	-3	Cacheado automáticamente	1
20	3	2009-05-01	0	Cacheado automáticamente	2
23	1	2009-05-01	-1	Cacheado automáticamente	1
24	1	2009-05-01	0	Cacheado automáticamente	2
25	3	2009-06-01	-3	Cacheado automáticamente	1
26	3	2009-06-01	0	Cacheado automáticamente	2
29	1	2009-06-01	-1	Cacheado automáticamente	1
30	1	2009-06-01	0	Cacheado automáticamente	2
31	3	2009-07-01	-3	Cacheado automáticamente	1
32	3	2009-07-01	0	Cacheado automáticamente	2
35	1	2009-07-01	-1	Cacheado automáticamente	1
36	1	2009-07-01	0	Cacheado automáticamente	2
37	3	2009-08-01	-3	Cacheado automáticamente	1
38	3	2009-08-01	0	Cacheado automáticamente	2
41	1	2009-08-01	-1	Cacheado automáticamente	1
42	1	2009-08-01	0	Cacheado automáticamente	2
43	3	2009-09-01	-3	Cacheado automáticamente	1
44	3	2009-09-01	0	Cacheado automáticamente	2
47	1	2009-09-01	-1	Cacheado automáticamente	1
48	1	2009-09-01	0	Cacheado automáticamente	2
49	3	2009-10-01	-3	Cacheado automáticamente	1
50	3	2009-10-01	0	Cacheado automáticamente	2
53	1	2009-10-01	-1	Cacheado automáticamente	1
54	1	2009-10-01	0	Cacheado automáticamente	2
55	3	2009-11-01	-3	Cacheado automáticamente	1
56	3	2009-11-01	0	Cacheado automáticamente	2
59	1	2009-11-01	-1	Cacheado automáticamente	1
60	1	2009-11-01	0	Cacheado automáticamente	2
61	3	2009-12-01	-3	Cacheado automáticamente	1
62	3	2009-12-01	0	Cacheado automáticamente	2
65	1	2009-12-01	-1	Cacheado automáticamente	1
66	1	2009-12-01	0	Cacheado automáticamente	2
67	3	2010-01-01	-3	Cacheado automáticamente	1
68	3	2010-01-01	0	Cacheado automáticamente	2
71	1	2010-01-01	-1	Cacheado automáticamente	1
72	1	2010-01-01	0	Cacheado automáticamente	2
73	3	2010-02-01	-3	Cacheado automáticamente	1
74	3	2010-02-01	0	Cacheado automáticamente	2
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
-- Data for Name: stock_almacen; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY stock_almacen (id, almacen_id, producto_compra_id, existencias) FROM stdin;
1	2	1	2
2	2	3	0
4	1	1	47
8	1	4	30
7	1	5	1
5	1	3	30
\.



--
-- Data for Name: centro_trabajo; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY centro_trabajo (id, nombre, almacen_id) FROM stdin;
\.



--
-- Data for Name: usuario; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY usuario (id, usuario, passwd, nombre, cuenta, cpass, nivel, email, smtpserver, smtpuser, smtppassword, firma_total, firma_comercial, firma_director, firma_tecnico, firma_usuario, observaciones) FROM stdin;
1	admin	cee9be15784861e244ca2e58268343c8	Administrador	frbogado@vm-webhosting	gusa25	0	frbogado@novaweb.es	smtp.gea21.es	fbogado	dfg234..-	t	t	t	t	t	Administrador de la aplicación.
2	adri	da2b65d46a86b8b6f54e68c2b34acd6a	Adriana			1					t	t	t	t	t	
\.



--
-- Data for Name: empleado; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY empleado (id, categoria_laboral_id, centro_trabajo_id, nombre, apellidos, dni, activo, usuario_id, color_r, color_g, color_b) FROM stdin;
3	3	\N	Gustavo Adolfo	Bécquer		t	\N	255	255	255
4	2	\N	Federico	García Lorca		t	\N	1	0	255
9	1	\N	Lucas	Velázquez Juan		t	\N	4	248	13
7	1	\N	Nadia	Bseiso Blanco		t	\N	247	245	2
1	1	\N	Ivana	Salvatto	00000000-T	t	\N	240	128	16
5	1	\N	Javier	Bseiso Blanco		t	\N	17	149	234
2	1	\N	Eleonora	Rosaminer	00000001-V	t	\N	171	24	224
6	1	\N	Guadalupe	Ruiz-Giménez de Aguilar		t	\N	243	7	7
8	\N	\N	Lucas	Velazquez juan		t	\N	4	248	13
\.



--
-- Data for Name: festivo_generico; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY festivo_generico (id, fecha) FROM stdin;
\.



--
-- Data for Name: contador; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY contador (id, prefijo, sufijo, contador) FROM stdin;
2			126
\.



--
-- Data for Name: cuenta_origen; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY cuenta_origen (id, nombre, banco, ccc, observaciones, contacto, fax, telefono) FROM stdin;
1	Tal	Cual	xx	sñkjdaj	x	x	xxxx
2	Cuenta principal	Caja Granada	20310188910115928707				
\.



--
-- Data for Name: cliente; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY cliente (id, tarifa_id, contador_id, telefono, nombre, cif, direccion, pais, ciudad, provincia, cp, iva, direccionfacturacion, paisfacturacion, ciudadfacturacion, provinciafacturacion, cpfacturacion, nombref, email, contacto, observaciones, vencimientos, formadepago, documentodepago, diadepago, inhabilitado, motivo, porcentaje, enviar_correo_albaran, enviar_correo_factura, enviar_correo_packing, fax, cuenta_origen_id, riesgo_asegurado, riesgo_concedido, packing_list_con_codigo, facturar_con_albaran, copias_factura, fecha_alta, fecha_nacimiento, sexo_masculino) FROM stdin;
47	\N	\N	666506905	NICOLA	GODFREY	X2419511A			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-11-01	1974-01-29	f
48	\N	\N	629610809		NIDIA	RODRIGUEZ			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-10-22	1900-01-01	f
49	\N	\N	671642822	NOELIA NAVARRO PIÑA URB. EL	MIRADOR	C/RETAMA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-11-01	1976-06-07	f
50	\N	\N	690353121	ASUNCION DEL REAL RODRIGUEZ LOS NARANJOS BL.2 4oC	NVA.ALCANTARA	SAN			PEDRO	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-07	1900-01-01	f
51	\N	\N	609230423	ISABEL ZUMTOBEL C/8 PARCELA 105 GUADALMINA	BAJA	SAN			PEDRO	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-07	1900-11-11	f
52	\N	\N	657913799	ITZIAR CHAVARRI SAINZ URB.LOMAS MARBELLA CLUB KING	HILL	F-0			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-07	1900-11-01	f
53	\N	\N	677508555	KIRSTEN FLEIG CARRIL DE LA GRANADILLA	3	SAN			PEDRO	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-07	1965-02-27	f
54	\N	\N	680425006	Ma JOSE MEDINA JARDINES ATALAYA	No	16			ESTEPONA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-07	1972-02-28	f
55	\N	\N	687046909	MARIANO DELLA PAOLERA URB.GUADALMINA ALTA No	477	SAN			PEDRO	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-07	1961-04-30	t
56	\N	\N	671642822	NOELIA NAVARRO PIÑA URB.EL MIRADOR	C/RETAMA	17			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-07	1976-06-07	f
57	\N	\N	627521592	PALOMA IZQUIERDO FRUTOS URB.RIO REAL	PARCELA	101			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-07	1965-11-01	f
58	\N	\N	629825101	PAQUITA BARRERO GRAL. LOPEZ	DOMINGUEZ	36F			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-07	1976-02-10	f
59	\N	\N	609916695	PAQUI ROSA URBANEJA C/ANTEQUERA No	41B	SAN			PEDRO	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-07	1959-01-14	f
60	\N	\N	670973718	PURIFICACION	MOLINELLO	MARBELLA-MADRID			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-07	1900-01-01	f
61	\N	\N	629423532	RODOLFO BALDRICH PACHECO RIBERA DE GUADALMINA CASA 12	G.BAJA	SAN			PEDRO	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-07	1947-05-22	t
62	\N	\N	658256921	SIMONA URB.LA QUINTA,LOS TAJOS	16	SAN			PEDRO	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-07	1986-10-19	f
63	\N	\N	617888861	SILVIA HIDE URB. LINDASOL	RESCIAL.	CARAMBUCO			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-07	1970-12-12	f
64	\N	\N	607605857	TERESA GANCEDO URB.TERRAZAS DE LOMAS	MARB.CLUB	1-5			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-07	1949-02-24	f
65	\N	\N	600003946	VANESA RODRIGUEZ URB.BELLASOL C/ZEUS BLQ.2	4oIZDO	MIJAS			COSTA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-07	1978-07-15	f
66	\N	\N	629827993	VENANCIO SANZ ROJO UBR.BELLAVISTA FASE II No	40	SAN			PEDRO	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-07	1961-05-16	t
67	\N	\N	690083113	VIVIAN CALLE 23B CASA 481 GUADALMINA	ALTA	SAN			PEDRO	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-07	1900-01-01	f
68	\N	\N	657924736	VICTORIA LOPEZ DE RODA URB.LAS CHAPAS,AVDA.EL	LIMONAR	143			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-07	1956-09-12	f
69	\N	\N	699776614	YUVAL RATNER GUADALMINA BAJA	CALLE	8			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-07	1900-01-01	t
70	\N	\N	29602		PEDRO	ANTONO			RODRIGUEZ	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-07	1900-01-01	t
71	\N	\N	609003593	RAFAEL RUIZ LLACH LOS NARANJOS 158.LINDA VISTA	BAJA	SAN			PEDRO	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-07	1948-09-09	t
72	\N	\N	952906462	XANDRA DE VOS NVA ATALAYA.EDIF. GOLF	PARK	F-11			ESTEPONA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-07	1900-01-01	f
73	\N	\N	609532524	ROCIO GOMEZ TEMBOURY C/PIZARRA.EDIF.EL RETIRO	DE	NAGUELES			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-07	1952-05-07	f
74	\N	\N	952884747	YVETTE BERGER GUADALMINA BAJA	C/8	SAN			PEDRO	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-07	1900-01-01	f
75	\N	\N	609750782	JAVIER BURGUES HOYOS C/MORALEJA No4 URB.COTO DE	LA	SERENA			ESTEPONA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-01	1900-02-02	t
76	\N	\N	619273341	OROSI SANTOFIMIA LOMAS DE SIERRA BLANCA,CASA	MALAGA	1oB			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-01	1900-01-01	f
77	\N	\N	645815794	DANIELA REICHERT CARIB	PLAYA-ALANDA	30B			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-01	1978-10-30	f
78	\N	\N	670621213	MINA MOENS CASA LA	MINA-MANCHONES	BAJOS			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-17	9000-01-01	f
79	\N	\N	609234541	GISELLA NUVOLONE C/ESTEBANEZ CALDERON EDIF	NEREIDA	5C			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-17	1963-03-02	f
80	\N	\N	656855990	- URB.LAS PETUNIAS.EDIF.LOCRISUR ESC.	33oD	SAN			PEDRO	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-17	1900-01-01	t
81	\N	\N	679370982	ESTHER FRATES GARCIA C/ESPERANTO EDIF.ALMENA	No12	11oA			MALAGA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-01	1975-05-28	f
83	\N	\N	610266704		SUSANA	CONDE			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-18	1900-01-01	f
86	\N	\N	615640264	ELENA PEZZANI X2796097X C/ PINO 76 B URB.	EL	REAL			MARBELLA	29603	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-19	1962-03-05	f
87	\N	\N	29602	PILAR BENITEZ	PILATES	LINDA			VISTA	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-19	1900-01-01	f
88	\N	\N	29602	MAITE	ACERA	COMPLETAR			DATOS	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-19	1900-01-01	f
89	\N	\N	29602	ALMUDENA	RIERA	COMPLETAR			DATOS	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-19	1900-01-01	f
90	\N	\N	649839998	AUDREY BOYSON COMPLETAR DATOS(4	EN	SEPTIEMBRE)			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-19	1900-01-01	f
91	\N	\N	607943144	KARIN KLEIN CASA LA TORRE MARBELLA	HILL	CLUB			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-19	1950-02-22	f
92	\N	\N	630282362	ERIKA INEICHEN C/SIERRA NEVADA 64B,LOMAS	MARBELLA	CLUB			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-19	1956-09-02	f
244	\N	\N	29602		GAIL	SOLO			TERAPIA	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-05-07	1900-01-01	f
246	\N	\N	29679	JOSE ANTONIO ITARTE 15192268D LA ZAGALETA-CTRA. DE	RONDA,	PARCELA			E-2o	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-05-15	1939-09-14	t
247	\N	\N	660865962	SANDRA CHESTER DATOS X	CONFIRMAR	952808874			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-05-15	1940-12-02	f
249	\N	\N	952766080	ANNE HILDE SKAR X1813167P PALM BEACH	21	C			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-05-19	1963-09-26	f
250	\N	\N	952832901	MILAGROS POSTIGO MONTEGORDO 08921620N PSO. DEL BRASIL No	1,	ELVIRIA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-05-20	1975-09-07	f
251	\N	\N	952832901	JOSE LUIS BLANES RIOS 27341071M PSO. DEL BRASIL No 1, URB/	PUEBLO	SUECO			ELVIRIA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-05-20	1972-08-21	t
252	\N	\N	952455655	VICTORIA SULTAN DATOS	X	CONFIRMAR			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-05-20	1977-07-07	f
253	\N	\N	952771197	ALEJANDRA HALIN B92800234 FELIX RODRIGUEZ DE LA FUENTE 2	OFICINA	9			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-05-23	1967-01-15	f
254	\N	\N	659398285	CRISTINA FERNANDEZ SANDOVAL DATOS	X	CONFIRMAR			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-05-23	1900-01-01	f
256	\N	\N	627252750	BAHIA DATOS	X	CONFIRMSAR			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-05-23	1900-01-01	f
258	\N	\N	652932977	MERCEDES SAN ALBERTO URB.	AGUAMARINA	No44			ESTEPONA	29680	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-05-23	1900-01-01	f
259	\N	\N	649090979	ASUNCION VILLAGRA SEVERO	OCHOA	24.1o3			MARBELLA	29603	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-05-23	1900-01-01	f
262	\N	\N	607011444	MARITZA PLATA ZABALA OASIS DE NAGUELES	No	19			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-05-23	1979-10-12	f
264	\N	\N	609179050	GABRIEL ROCAMORA URB.MIRADOR.LOMAS RIO	VERDE	ALTO			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-05-23	1900-01-01	f
266	\N	\N	29602	LEO SHIRIQUI URB SIERRA BLANCA, LOS	GRANADOS	No			135	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-05-27	1900-10-10	t
267	\N	\N	637311576	RAQUEL ALBA URB BUENHORIZONTE FASE	2,NUMERO	22			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-05-31	1979-01-05	f
268	\N	\N	952815971	KHALED KADDOURA LOS MONTEROS APTDO.CORREOS 2013	MARBELLA,	LAS			CHAPAS	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-06-02	1974-03-01	t
270	\N	\N	29602	MARGARITA JHONS	DATOS	POR			COMPLETAR	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-06-04	1900-01-01	f
271	\N	\N	29602	VANESSA URB. GUADALMINA ALTA,C/19	P831	SAN			PEDRO	ALCANTARA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-06-04	1989-11-10	f
272	\N	\N	952860404	BOB BRONSON ESTEBANEZ CALDERON, No8	EDF.NAYADE	1o-D			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-06-04	1900-01-01	t
273	\N	\N	29602	LUIS GATOO BERRIZBEITIA 27343433K URB.JARDINES DEL	SOL	CASA			G.9	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-06-06	1973-04-03	t
275	\N	\N	616995092	LIVIA HOTEL	PUENTE	ROMANO			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-06-10	1900-01-01	f
276	\N	\N	679997588	BERNARD SOULTAN HOTEL	PUENTE	ROMANO			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-06-10	1900-01-01	t
277	\N	\N	662461885		ADRIAN	RINGUEDAL			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-06-12	1900-01-01	t
279	\N	\N	29602	CARLITOS	(SHIVA)DATOS	POR			CONFIRMAR	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-06-12	1900-01-01	t
281	\N	\N	952785786	PABLO MENA ESCRIBANO C/MALVAS	17	NUEVA			ANDALUCIA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-06-30	1991-08-14	t
282	\N	\N	650382099	MANUEL MENA ESCRIBANO C/EUCALIPTOS,LOS MAGNOLIOS	1,LINDA	VISTA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-07-02	1900-01-01	t
283	\N	\N	699419497	JOSE MEDIO RETIRO DE NAGUELES	112	C/PIZARRA			MARBELLA	29601	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-07-02	1900-01-01	t
285	\N	\N	616398193	RULA ABIRAFEH URB.SIERRA BLANCA CRTA.ISTAN	TOLEDO	4			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-07-07	1900-01-01	f
286	\N	\N	29602	JACKELINE Y NICK	DATO	POR			CONFIRMAR	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-07-08	1900-01-01	t
291	\N	\N	29602	REEM JALLAD,BLOQ.16,APTO.1	MONTE	PARAISO			COUNTRYCLUB	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-07-21	1900-01-01	f
292	\N	\N	29602	LORENCE	HOTEL	PUENTE			ROMANO	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-07-21	1900-01-01	f
293	\N	\N	29602		BABETTE	PUENTE			ROMANO	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-07-21	1900-01-01	f
296	\N	\N	670068609	MARY DUNNE HOTEL	PUENTE	ROMANO(PANORAMA)			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-07-23	1900-01-01	f
297	\N	\N	609178551	NURIA SEBASTIAN SIERRA DE CAZORLA.RCIAL.LA	CASCADA	BLQ.1			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-07-23	1900-01-01	f
299	\N	\N	29602		ESTRELLA	Y			MARIDO	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-07-29	1900-01-01	f
300	\N	\N	29602		UNA(SE	LLAMA			UNA)	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-07-29	1900-01-01	f
301	\N	\N	49	RENATO RUEGER URB. LA CAPELLANIA	CASA	SHALIMAR			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-07-30	1900-01-01	t
302	\N	\N	649395625		FRANCISCO	ORTIZ			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-08-01	1980-05-01	t
303	\N	\N	29602	AMPELIO PLAZA 1396887M	URB.LAS	GOLONDRINAS,CASA			No9	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-08-04	1953-08-26	t
304	\N	\N	29602	MONIR SATTARIPOUR	DATOS	POR			CONFIRMAR	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-08-05	1900-01-01	f
305	\N	\N	658619233	RANA SATTARIPOUR DATOS	POR	CONFIRMAR			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-08-05	1900-01-01	f
306	\N	\N	29602	JOANNA DOGMOCH 356408612 MARBELLA	HILL	CLUB			2	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-08-05	1900-01-01	f
307	\N	\N	29602	ALEXANDER ORDWAY	DATOS	POR			CONFIRMAR	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-08-05	1900-01-01	t
2	\N	\N	29602		ADRIANA	LOPEZ			.	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-10-21	1977-09-20	f
3	\N	\N	627944435	ANA CERVAN RODRIGUEZ 78970303X AVDA.JOSE MANUEL VALLES No	30	-2-2-4oD			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-10-22	1981-04-14	f
4	\N	\N	627429016	EDUARDO GOMEZ CABEZAS C/LEON No 23	GUADALMINA	BAJA			SAN	PEDRO	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-10-26	1967-08-12	t
5	\N	\N	952900020	ADRIENNE BARNETT URB LOMAS DE S. BLANCA BL	JAEN	2A.			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-10-30	1900-01-01	f
6	\N	\N	627518834	ANITA HORRY	URB.EL	MIRADOR			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-10-22	1976-05-15	f
7	\N	\N	667497415	ANTONIO MOYA MARTIN LOS CIPRESES 46 (ALTA	VISTA)	SAN			PEDRO	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-10-22	1956-04-18	t
8	\N	\N	952818141	ASTRID THOMAS URB.LAS PETUNIAS.EDIF.LOCRISUR	11D	SAN			PEDRO	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-10-22	1900-01-01	f
9	\N	\N	651199889		CARMELO	MANZANARES			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-11-01	1949-06-06	t
10	\N	\N	952799807	CARMEN	KRUMNIKL	SAN			PEDRO	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-11-16	1951-10-18	f
11	\N	\N	627925417	CATHERINE THOMPSON LA GAVIA 2 ATICO 2B NVA	ALCANTARA	SAN			PEDRO	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-10-22	1979-07-18	f
12	\N	\N	650382099	CARMEN ESCRIBANO C/EUCALIPTOS,LOS MAGNOLIOS 1	LINDAVISTA	SAN			PEDRO	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-11-01	1961-02-02	f
13	\N	\N	667547166	CARLOS AGUILAR AVDA.JACINTO	BENAVENTE	37-2oA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-11-01	1953-10-09	t
14	\N	\N	600585727	CUCHI	SAINZ	BALSA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-11-16	1900-01-01	f
15	\N	\N	618743744	DANIEL QUINTEROS MARTINEZ C/SIERRA DE CAZORLA SN	LA	CASCADA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-10-22	1966-01-31	t
16	\N	\N	677751077	ERIKA KUCK HACIENDA	DEL	SOL			ESTEPONA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-10-22	1957-11-24	f
17	\N	\N	646289963	ESTELA SAYAR RIVAS URB.EL RETIRO DE NAGUELES	APTO	132			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-11-01	1974-12-03	f
18	\N	\N	659458013	ESTER FLAÑO URB.ALHAMBRA DEL	GOLF	25-1oIZDA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-10-22	1900-01-01	f
20	\N	\N	639772581	EUGENIA NAVARRO OLARTE C/TOLEDO.EDIF ROSAMAR	P19-3oA	SAN			PEDRO	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-11-01	1976-05-23	f
21	\N	\N	610716168	EVA BERGMAN AVDA. CARMEN	SEVILLA	32			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-10-22	1955-06-18	f
22	\N	\N	629717995	FABIANNA CORNET AVDA.CONSTITUCION	22B	SAN			PEDRO	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-10-22	1958-11-30	f
23	\N	\N	608601277	FELIX DE BARRIO LA	QUINTA-MIRADOR	II			BENAHAVIS	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-10-22	1928-12-14	t
24	\N	\N	607779747	GINES GARCIA URB.LOCRIMAR	II	ESC.4-2oA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-10-22	1964-06-19	t
25	\N	\N	676234753	GRACIA BAJO 27332733Q C/ LOS JAZMINES 191,	NUEVA	ANDALUCIA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-11-19	1900-02-19	f
26	\N	\N	626673963	INMA ARESPACOCHAGA EL QUETZAL No 1 APTO	9	SAN			PEDRO	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-11-19	1946-03-02	f
27	\N	\N	629826051	JANE AUGIER C/VIVALDI, SIERRA	BLANCA	66/69			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-10-22	1935-06-22	f
28	\N	\N	670973718	JESUS JAVIER DE LA	PEÑA	BARTHEL			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-11-01	1900-01-01	t
29	\N	\N	636661477		JUDITH	WALSH			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-10-22	1900-01-01	f
30	\N	\N	676900100	KOSTAS EDIF GOLF,PARCELA FII	(NUEVA	ATALAYA)			BENAHAVIS	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-10-22	1973-08-15	t
31	\N	\N	609514344	Ma JOSE TORRABADELLAS URB. EL PARAISO ALTO.C/BONSAI No	309	VIL			BENAHAVIS	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-10-22	1900-01-01	f
32	\N	\N	609909689	MADELON VERHEUL ISLA DE GUADALMINA VILLA	12	SAN			PEDRO	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-10-22	1964-12-05	f
33	\N	\N	629070807	Ma LUISA FERNANDEZ C/GALICIA No 81 (LOS	CARACOLILLOS)	SAN			PEDRO	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-10-22	1954-07-11	f
34	\N	\N	616061568		MAGDELEINE	ANDERSON			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-11-01	1900-01-01	f
35	\N	\N	630075833	MARINA GOMEZ MOLINA URB.SIERRA BLANCA	C/WAGNER	115-B			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-10-22	1970-07-10	f
36	\N	\N	636123412	MARTINE VAN OOSTERUM URB.LA HEREDIA	C/PARLADE	25			BENAHAVIS	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-11-01	1973-11-06	f
37	\N	\N	609512374	MARIELLA BRUNO LOS GRANADOS GOLF	501-LAS	BRISAS			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-11-01	1964-01-01	f
38	\N	\N	630878498		MONTSE	HOCES			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-11-01	1959-08-19	f
39	\N	\N	645881531	MaCARMEN MARTIN LORENTE AVD DE ANDALUCIA	8	BENAHAVIS			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-11-19	1900-01-01	f
40	\N	\N	606962563	MaROSA PEREZ EDIF.AGUILA REAL APTO 8 GUDALMINA	ALTA	SAN			PEDRO	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-10-22	1900-01-01	f
41	\N	\N	639780253	MALOU LAGUNA URB. SOLENO	GOLF	71			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-10-22	1948-01-03	f
42	\N	\N	952883410	MaJESUS	BAJO	PARRA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-10-22	1900-01-01	f
43	\N	\N	680442717	MARGARITA ROMAN URB.CERRO BLANCO 0. 1	No	7			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-10-22	1953-02-11	f
44	\N	\N	669807189	MERCEDES AGUERA GUTIERREZ C/HERMANOS	MAYEN	SAN			PEDRO	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-10-22	1900-01-01	f
45	\N	\N	620680187	MERCEDES MORILLA JIMENEZ URB. MALIBU APT 15 BL.2	RODEO	BEACH			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-11-21	1900-01-01	f
46	\N	\N	637521611	MICHAEL BARNETT LOMAS S.BLANCA BLQ.JAEN	AT.2A	DUPLEX			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-10-22	1900-01-01	t
93	\N	\N	607521036	ANNALISA ALBRIGHI AVDA.ESPAÑA-VILLA	OREHIA	(ELVIRIA)			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-21	1962-10-30	f
94	\N	\N	629582088	LORRAINE	ANN	WELFORD			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-22	1900-01-01	f
97	\N	\N	29602		MIGUEL	ANGEL			GARRE	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-22	1900-01-01	t
98	\N	\N	645188406	VIVIANA RUPIL 4513259S URB LOS	VIÑEDOS,APT	502,OJEN			MARBELLA	29610	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-22	1963-07-29	f
101	\N	\N	686356092		JUAN	SERGIO			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2007-12-22	1900-01-01	t
102	\N	\N	664542961		HELEN	ALDERTON			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-02	1900-01-01	f
103	\N	\N	609580872	NATALIA CREDI APREA URB. NARANJOS DE MARBELLA	F.II	15			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-02	1965-03-23	f
104	\N	\N	619041001	ANA Ma PARRA ROJAS URB. OASIS DE	NAGUELES	17			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-02	1900-01-01	f
105	\N	\N	649821525	ANA MORENO	MERINO	OK			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-02	1900-01-01	f
106	\N	\N	656628370	CAROLYN IRENE GUY LAS	POYETES	S/N			MONDA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-02	1946-12-06	f
107	\N	\N	952865158	BEBE DE FOUQUIERES PLZA. ARRAYANES 1G	SEÑORIO	MARBELLA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-02	1900-01-01	f
108	\N	\N	618819018	MARTINA CABRERA ALTOS DEL RODEO.EDI.LOCRIMAR FASE	V	1oAB			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-02	9000-01-01	f
109	\N	\N	29602	MARIA	SUELVES	CLIENTA			ESPORADICA	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-03	1900-01-01	f
110	\N	\N	686064280	MANUEL CAÑIZARES URB.COSTA NAGUELES III	BLQ.	4-3oG			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-03	1900-01-01	t
111	\N	\N	649821525	ANA MORENO MEDINO- REPE, NO METAIS PAGOS 27338315D C/CALVARIO EDIF. LA CONCHA 35	1o	1			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-04	1969-05-30	f
112	\N	\N	654349435	UBALDINA CAMPOS TORRES FINCA LA PANOCHA.CASA	LA	GAVIOTA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-04	1948-05-11	f
113	\N	\N	629669645	BIANCA HANAU MARBELLA HILL	CLUB.CASA	HANAN			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-08	1956-04-24	f
114	\N	\N	629890908	LOURDES GONZALEZ CANDELA UBR.CUMBRES DEL	RODEO.CASA	75			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-08	1900-01-01	f
115	\N	\N	699228244	MELANIE MARTIN RUNCHEL C/JOSE URBANEJA 811	URB.SITIO	CALAHONDA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-10	1989-04-08	f
116	\N	\N	696439780	ANA GARCIA HERRERA C/PESCADORES, VILLA	LA	ROMANTICA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-10	1900-01-01	f
117	\N	\N	609186965	LUIS ALBERTO GALVEZ 78969465T CTRA. COM. RIO VERDE OF.1	C.N.340	KM			NUEVA	29660	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-10	1900-01-01	t
118	\N	\N	692456997	INMA CUSTONCO AVDA.LOLA FLORES 2	MEDINA	GARDEN			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-10	1900-01-01	f
121	\N	\N	609555715		OLGA	PLATON			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-11	1900-01-01	f
122	\N	\N	29602	BLANCA ARES C/ BENAOJAN No	44,	URB.MARBELLA			MONTAÑA	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-12	1970-12-30	f
123	\N	\N	616977722	SERGIO SCARIOLO	NAGUELES.C/BENAOJAN	44			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-12	1900-01-01	t
124	\N	\N	627521752	JULIAN LARA RUIZ URB.GOLF RIO	REAL.PARCELA	101			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-12	1900-01-01	t
125	\N	\N	607430043	CARMEN	ROPERO-	REPE-			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-12	1900-01-01	f
126	\N	\N	607685915		MANUEL	SANTAELLA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-12	1900-01-01	t
127	\N	\N	686206698	NATALIA MONTES DE OCA URB. COTO LA SERENA C LA	MORALEJA	No4			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-14	1964-10-10	f
128	\N	\N	607430043	CARMEN ROPERO URB.ELVIRIA	RESID.TRAMIRE	4oB			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-15	1900-01-01	f
129	\N	\N	639230470	MARGARET BUNCHE C/MOZART 9.URB.MARBELLA	SIERRA	BLANCA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-15	1900-01-01	f
130	\N	\N	609710477	IRENE MOLINA REPE URB.JARDINES DEL	SOL	9-9			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-15	1900-01-01	f
131	\N	\N	629416527	LUCIA EJEA SERNA C/PICASO No2 URB.ATALAYA	RIO	VERDE			ESTEPONA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-18	1900-01-01	f
132	\N	\N	686454112	MONICA ARNEDO ALCALDE MAGNA	MARBELLA.EDIF.GOYA	148			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-18	1963-05-16	f
133	\N	\N	690670504	GEMA GAVIRA TOMAS APDO. CORREOS	2084-LAS	CHAPAS			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-18	1962-05-14	f
134	\N	\N	951965224		KRISTINE	VANOUDENDYCKE			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-18	1900-01-01	f
135	\N	\N	607449035	GORKA ARRINDA AVDA.REYES CATOLICOS No	2	3oF			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-19	1900-01-01	t
136	\N	\N	679973963	IVONNE JONES AVDA.REYES CATOLICOS	No2	3oF			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-19	1900-01-01	f
137	\N	\N	617422541	JOAQUIN SANTOS SUAREZ AVDA.GENERALIFE 10	H	B			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-21	1950-05-11	t
138	\N	\N	617422571	REGINA CALVO AVDA.GENERALIFE	10-H	B			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-21	1957-12-22	f
139	\N	\N	637134438	ANN GARRY CASA 49.COMPLEJO EL RIO.AZALEA	BEACH	SAN			PEDRO	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-21	1959-10-26	f
140	\N	\N	616531852	SARAH STEIGER 121 ROCIO DE	NAGUELES	C/CASARES			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-21	1900-01-01	f
141	\N	\N	619197190		MARIBEL	TROYANO			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-21	1900-01-01	f
142	\N	\N	629041273	RAQUEL NAVARRO SANCHEZ CONDADO DE SIERRA BLANCA	ATICO	E			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-22	1963-05-05	f
143	\N	\N	639346640	ADA LOBATO LA CASACADA C/SIERRA BLANCA	4	B4			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-22	1965-04-22	f
144	\N	\N	619247606	SUSANA ALTOS DE PUENTE ROMANO.C/ALGORTA	No	10			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-23	1961-04-17	f
145	\N	\N	609002852	BARBARA RIOS LARRAIN EL CISNE No7	BL	7-2oA			MADRID	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-23	1958-09-22	f
146	\N	\N	679924364	VICTORIA LUQUE READER C/SIERRA DE	CAZORLA	S/N			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-23	1969-06-22	f
147	\N	\N	607674067		ELISABETH	MORBACK			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-23	1900-01-01	f
149	\N	\N	952888240	RICARDO CHARRO GUADALMINA BAJA	PARCELA	156			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-24	1945-01-30	t
150	\N	\N	639163998	ENRIQUE ALVAREZ URB. LA CAROLINA, C/	CLAVELES	5			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-24	1900-03-03	t
151	\N	\N	699958535	ISABEL HAGENMEYER CRTA.DE RONDA S/N	(LA	ZAGALETA)			BENAHAVIS	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-29	1900-01-01	f
152	\N	\N	653660001	LUISA REVUELTA 36953318T C/VIVALDI 68,	SIERRA	BLANCA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-29	1949-05-20	f
153	\N	\N	679503650	ROXANA REHBERGER URB.MONTEBELLO	SIERRA	BLANCA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-29	1961-11-03	f
156	\N	\N	645791362	ELENA LYUBARINA GUADALMINA ALTA.MEDITERRANEO	6	SAN			PEDRO	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-29	1900-01-01	f
157	\N	\N	629171111	JOSE LUMBRERAS FERNANDEZ DE CORDOBA 51056820V LA CASCADA C/ SIERRA CAZORLA	4	B4			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-31	1955-05-20	t
158	\N	\N	649592194	JAMES MARSDEN SIERRA BLANCA C/ MOZART	No	9			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-31	1950-04-25	t
159	\N	\N	952815098	HIAM BOHSALI LOS GRANADOS No 2	APT.	601			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-01-31	1946-10-05	f
160	\N	\N	659405996	MARIA IZABEL TAMBASCO GENEROSO 78978729H C/PIZARRA S/N ED EL RETIRO	APTO	101			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-02-01	1954-12-24	f
161	\N	\N	952771472	CHARO LOPEZ D ESTIVARIZ X0729103 NUESTRA SRA DE GRACIA N	28	2oD			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-02-01	1950-01-19	f
162	\N	\N	650810078	RAFAEL CRUZ CONDE ROCA 44368006V URB ISLA DE GUADALMINA, VILLA	No	10			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-02-12	1978-07-29	t
164	\N	\N	670990307	FRANCISCO SUSINO 24297012L JARDINES DE LAS LOMAS,	CASA	21			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-02-12	1961-11-16	t
165	\N	\N	654563502	MAITE ACERA GUTIERREZ 27330569Z URB LA MONTUA,	ALTAVISTA	No1			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-02-12	1964-04-30	f
166	\N	\N	952864969	GIULIA INEICHEN C/ SIERRA NEVADA 64B, LOMAS DE	MB	CLUB			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-02-12	1995-06-13	f
167	\N	\N	952775384	CAROLINA FERNANDEZ MARCO RESIDENCIAL GRAN DUCADO,	BAJO	E			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-02-12	1971-05-10	f
168	\N	\N	952785674	MARIA TREMENDAD JUAREZ C/ PEPE	OSORIO,	36			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-02-12	1900-01-01	f
169	\N	\N	952811565	PASTORA NICOLAS ARRIGORRIAGA JU830651C URB LA ALCAZABA,	APTO	613			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-02-12	1958-09-30	f
170	\N	\N	952812984	CANDELARIA HENS SERENA 30475195B JUAN BELMONTE LOS TOREROS	No	8			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-02-12	1961-04-01	f
171	\N	\N	691976488	KRISTINA ERGO SL291721 LA ALZAMBRA FASE	3,	19			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-02-12	1977-03-07	f
172	\N	\N	952837330	DOMINIQUE LAMBERT PUERTO DE CABOPINO, REST.	LA	DESPENSA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-02-12	1961-03-12	f
173	\N	\N	687944107	DANNA CHOLVADOVA MOHAMMED PARAISO ALTO,	C/	SAUCE			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-02-13	1972-01-24	f
174	\N	\N	659483430	JANET HORN URB EL	TOMILLAR	C/37			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-02-13	1965-01-29	f
175	\N	\N	674580346	GUSTAVO ORIBE CRTA DE ISTAN	KM	0.9			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-02-13	1977-02-26	f
176	\N	\N	656829695	LUNA KRUM MOLLER X0038328X LOS HIBISCUS, CASA 3, MARBELLA	HILL	CLUB			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-02-13	1945-07-01	f
177	\N	\N	637865755	SUSAN LEAKEY CASA	26	NAGUELES			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-02-14	1959-08-11	f
178	\N	\N	696668875	MARIA ADRIANA BEEKS X2482087 LOMAS DE SIERRA BLANCA 1A	EDIF.	SEVILLA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-02-18	1965-01-24	f
179	\N	\N	661626305	ELISABETH HAZELEGER ARTURO	RUBINSTEIN,	8			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-02-18	1959-01-15	f
180	\N	\N	952864705	FARIMAH GRIFFIN 78977408P ANCON SIERRA	FASE	4			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-02-21	1959-11-04	f
181	\N	\N	952864705	JHON PATRICK GRIFFIN X0169653N ANCON SIERRA	FASE	4			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-02-21	1956-12-09	t
182	\N	\N	29602	JOSE MARIA MORENO RUIZ 27340587G C/ CUENCA No 8 PISO	4	21			B	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-02-21	1972-05-10	t
183	\N	\N	29602	AITOR GAZTELM HERNAIZ 30558143K MAGNA MARBELLA	EDF/	GOYA			148	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-02-21	1961-05-03	t
184	\N	\N	29602	LUKE WINGFIELD DIGBY X5711684W LES BELVEDERES	C6,	NUEVA			ANDALUCIA	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-02-22	1983-06-24	t
185	\N	\N	29602	JHON GARRY	DATOS	POR			COMPLTAR	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-02-27	1900-01-01	t
186	\N	\N	629086464	JOSE LUIS DE LA VIÑA DATOS	POR	COMPLETAR			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-02-27	1900-01-01	t
187	\N	\N	29602	PAULA GARCIA MARTINEZ 78965829K	DATOS	POR			COMPLETAR	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-03-04	1977-02-26	f
188	\N	\N	952862277	Ma CRUZ LIS 19821903C URB/ ALHAMBRA DEL	MAR	19-11			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-03-04	1953-01-26	f
189	\N	\N	637550305	PATRICIA MELGAR ORTEGA PLZA.ADOLFO	LUQUE	CHICOTE			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-03-04	1978-06-27	f
190	\N	\N	605900912		LUIS	RODRIGUEZ			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-03-04	1900-01-01	t
191	\N	\N	696668115	DANNY DE HAAS CRTA.DE ISTAN O.7KM.LOMAS DE	SIERRA	BLAN			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-03-04	1992-02-19	f
192	\N	\N	952778560	TERESA GOMEZ OASIS DE	NAGÜELES,25	652772636			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-03-04	1969-12-03	f
193	\N	\N	352781404	MILES TUNNICLIFF URB/LOS ARQUEROS,JACARANDAS B9 A1 SAN	PEDRO	DE			ALCANTARA	29670	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-03-05	1968-07-30	t
194	\N	\N	952781404	ENCARNACION LEIVA MORON 27340265F URB/LOS ARQUEROS,JACARANDA,Bo A1 SAN	PEDRO	DE			ALCANTARA	29670	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-03-05	1972-02-16	f
196	\N	\N	952782890	BERNARDETTE MARTINEZ MARTINEZ X0674628Z C7LOS LIMONES 22,LINDAVISTA BAJA SAN	PEDRO	DE			ALCANTARA	29670	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-03-11	1939-05-20	f
197	\N	\N	29602	LAMIA EL HINATI	C.C.	LA			CAÑADA	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-03-13	1968-11-16	f
198	\N	\N	655700677	ZOE BROWINING LES BELVEDERES APT	C6,NUEVA	ANDALUCIA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-03-14	1965-12-30	f
199	\N	\N	29602		RAQUEL	SIN			APELLIDO	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-03-15	1900-01-01	f
200	\N	\N	952882875	TERESA GARCIA AVIAL 671232T GUADALMINA BAJA C/25 E,	SAN	PEDRO			ALCANTARA	29670	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-03-18	1957-04-21	f
205	\N	\N	699151928	MONICA GIL TORRES URB. CAMPOS DE GUADALMINA	EDIF.	XALLOS			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-03-25	1972-12-02	f
206	\N	\N	29670	JANE WATERS X605070S C/LOS NARANJOS, LINDA VISTA BAJA	SAN	PEDRO			DE	ALCANTARA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-03-27	1963-12-08	f
208	\N	\N	610439245	BELEN PEREZ FERREIRO DATOS	POR	COFIRMAR			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-04-01	1950-03-26	f
209	\N	\N	952904207	MARTA DIAZ DE BUSTAMANTE 50404911C "EL AGUILA REAL" GUADALMINA ALAT,C/19S/N SAN	PEDRO	DE			ALCANTARA	29670	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-04-01	1951-05-25	f
211	\N	\N	686950774	FELIPE RECORDON DATOS	POR	CONFIRMAR			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-04-01	1999-01-10	t
212	\N	\N	952781476	ESTIBALIZ IÑARRITU 30630818Q LOS ALMENDROS2 BLOQ.7	BAJO	D			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-04-01	1967-05-10	f
213	\N	\N	617710655	MARIA SANCHEZ LIZANA TORRE DE ALOHA.EDIF.ZUMAYA	APTO	305			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-04-01	1963-08-17	f
214	\N	\N	686950774	FELIPE RECORDON MARTIN CENTRO COMERCIAL RIO	VERDE	OF.9			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-04-01	1953-08-19	t
215	\N	\N	952822252	BEATRIZ BEIL DATOS	POR	CONFIRMAR			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-04-02	1900-01-01	f
216	\N	\N	29602	ANDREA SERRANO LOMAS DE	MARBELLA	CLUBPUEBLO,C/REAL			7	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-04-02	1969-03-25	f
217	\N	\N	952833232	ENCARNACION VALDERRAMA JIMENEZ 24862054C URB/EL ARENAL	No	47			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-04-03	1956-03-01	f
219	\N	\N	952815971	SABRINA LOS MONTEROS	APTDO.CORREOS	2013			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-04-04	1900-01-01	f
220	\N	\N	605096654	Ma LUISA BOULOH DATOS	X	CONFIRMAR			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-04-08	1900-01-01	f
223	\N	\N	952864970	ELINA UUSMAA X0705565V URB. SIERRA BLANCA C/ WAGNER S/N	6	BAJOA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-04-10	1966-02-28	f
224	\N	\N	29602	DIANA O`CONNOR	COMECAPA	1,			SELWO	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-04-11	1970-07-18	f
225	\N	\N	697209817	LEAH BEDFORD VILLA 19 LA ALZAMBRA	PTO	BANUS			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-04-11	1900-01-01	t
226	\N	\N	662461885	SHIVA RINGDAL DATOS	X	CONFIRMAR			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-04-14	1900-01-01	f
228	\N	\N	619534918	JEANFAUSTO DATOS	X	CONFIRMAR			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-04-16	2000-10-10	t
229	\N	\N	952835957	ALICIA ARRIBAS URB HACIENDA LAS CHAPAS, AV.	2,	PARC.126			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-04-18	1969-08-06	f
230	\N	\N	952838238	ANIA SCHEELE X3626016C URB/ JARDINES DE LOS	PINOS	13			MARBELLA	29604	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-04-18	1970-04-18	f
231	\N	\N	952886995	GILLIAN REYNARD GUADALMINA BAJA C/ 13, 7B SAN	PEDRO	DE			ALCANTARA	29670	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-04-25	1957-03-14	f
232	\N	\N	952782281	SUSANA CURRY 22975961L URB. EL MADROÑAL 3	"LA	BUGANBILLA"			BENAHABIS	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-04-25	1969-02-11	f
233	\N	\N	29670	AMANDA GACHOT URB. EL MADROÑAL, ENTRADA	6,	CASA			MONTE	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-04-25	1971-06-20	f
234	\N	\N	696262690		PEDRO	SERRAN			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-04-25	1900-01-01	f
235	\N	\N	671618823	ANNA GLUSHCHENCO LOMAS DE SIERRA	BLANCA.CASA	21			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-04-25	1900-01-01	f
236	\N	\N	619206596		DAVID	GOZALO			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-04-25	1900-01-01	f
237	\N	\N	649395625	FRANCISCO ORTIN	VON	BIJMARCH			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-04-25	1980-05-01	f
238	\N	\N	952907594	LUDMILA BJOSTRAND AVD.VALLE DEL GOLF	No	13			MARBELLA-NUEVA	29670	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-04-28	1958-03-01	f
239	\N	\N	610272799	BEGOÑA MARTIN-LEYES RESIDENCIA HOTEL DEL GOLF	APTO	204			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-04-29	1956-09-30	f
240	\N	\N	609592623	MIREN	VALLE	C/CENTAURO			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-04-30	1900-01-01	f
241	\N	\N	609580865	JORGE HAENELT SAN JAVIER No 24	ALOHA	GOLF			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-05-07	1900-01-01	t
242	\N	\N	607472017	FATIMA BAQUERIZO SOBRINO SAN JAVIER No 24	ALOHA	GOLF			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-05-07	1900-01-01	f
308	\N	\N	952860885	ELINKA ORDWAY DATOS	POR	CONFIRMAR			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-08-05	1900-01-01	f
309	\N	\N	647612752	LORENA ABAD 51076205J	C/BOADILLA	DEL			CAMINO,3	MADRID	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-08-07	1976-12-05	f
310	\N	\N	29602	MAJID	DATOS	X			CONFIRMAR	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-08-07	1900-01-01	t
311	\N	\N	29602	NEREA LIZARRALDE URB.	ALHAMBRA	DEL			MAR	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-08-11	1971-09-29	f
312	\N	\N	29602	ANA	PEREZ-ULLIVARRI	01491844V			URB.COSTACITA	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-08-11	1960-11-17	f
313	\N	\N	629217918	OLGA PUIGCARBO 483418G ESTEBANEZ CALDERON	No	8			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-08-11	1900-01-01	f
314	\N	\N	629225659	FERNAANDO JANSEN ESTEBANEZ CALDERON	No	8			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-08-11	1900-01-01	t
315	\N	\N	693259223	RITA FORTUNATO CTRA. ISTAN TOLEDO CLUB SIERRA	No	9			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-08-13	1959-08-11	f
316	\N	\N	952810247	FIONA WEEKS X1179933X APTO.508 CASA "S"	PTO.	BANUS			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-08-13	1963-07-05	f
318	\N	\N	29602	NURIA CODES REQUENA	DATOS	POR			CONFIRMAR	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-08-18	1900-01-01	f
319	\N	\N	952778828	ELOY GUERRERO 24674807	TESON	11			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-08-18	1941-04-04	t
320	\N	\N	627113988	LUISA PAROLINI MARINA PUENTE	ROMANO	K31			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-08-18	1947-06-21	f
321	\N	\N	29602	MIGUEL RUIZ	DATOS	POR			CONFIRMAR	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-08-19	1900-01-01	t
322	\N	\N	29602	ELENA EMBARAZADA(GUADI)	DATOS	POR			CONFIRMAR	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-08-20	1900-01-01	f
323	\N	\N	29602	ZACARIAS	DATOS	POR			CONFIRMAR	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-08-22	1900-01-01	f
324	\N	\N	29602	SANTIAGO RAMON Y CAJAL	DATOS	POR			CONFIRMAR	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-08-22	1900-01-01	t
325	\N	\N	29602	JORDAN	DATOS	X			CONFIRMAR	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-08-25	1900-01-01	t
326	\N	\N	952855237	ROSE MARY CATTLIFFF DATOS	POR	CONFIRMAR			BENAHABIS	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-08-26	1900-01-01	f
327	\N	\N	952906179	ANNE VYSTAVEL URB LOREA PLAYA 10 CASA	ROSA	NUEVA			ANDALUCIA	29660	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-08-28	1963-06-21	f
328	\N	\N	29602		CARMEN	TERAPIA			MADRID	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-08-28	1900-01-01	f
329	\N	\N	29602	BLANCA ARAGON	DATOS	X			CONFIRMAR	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-09-04	1900-01-01	f
330	\N	\N	627537379	MaVICTORIA SAN GIL DATOS	POR	CONFIRMAR			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-09-05	1900-01-01	f
331	\N	\N	661279568		NENI	D`VITTORI			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-09-09	1900-01-01	f
332	\N	\N	649942086	MERCEDES MENGIBAR TORRES CRTA.LA ALCAPARRA S/N CASA	PLUMARIA	MIJA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-09-09	1954-03-31	f
333	\N	\N	952887833	ELOISA CASTELLS TRAIN 25136698K URB/CLEVEDON,18	N.	ATALAYA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-09-10	1963-07-06	f
334	\N	\N	952867556	RANI ARJAN HARJANI X2419537Y JACINTO	BENAVENTE	Na5			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-09-23	1958-01-26	f
335	\N	\N	686751982	CARMEN LLAMAS MAURI SIERRA DE CAZORLA.URB.	LAS	CASCADAS			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-09-30	1972-02-09	f
336	\N	\N	629524218	Ma JOSE MARTINEZ LINARES URB. LAS PETUNIAS II. FASE	No	10			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-09-30	1963-02-01	f
337	\N	\N	690692671	PATRICIA IZQUIERDO 78984507T C/5F LA QUINTA VILLAGE 1201	N.	ANDALUCIA			MARBELLA	29660	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-09-30	1975-06-02	f
338	\N	\N	618612412	MATILDE GONZALEZ CASTRO X2968408M C/ MOZART No	5	URB			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-10-03	1975-01-19	f
339	\N	\N	609702431	M EUGENIA MENENDEZ GONZALEZ ATALAYA RIO VERDE, C P PICASSO	CASA	7			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-10-06	1900-01-01	f
341	\N	\N	609960837	EUGENIA GALVAN BOHORQUEZ C/ LIBRA 7H , U. SEÑORIO	GONZAGA	16-13			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-10-06	1975-11-20	f
342	\N	\N	696811876	MARIA CASTAÑON	COMPLETAR	DATOS			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-10-07	1900-01-01	f
343	\N	\N	952818596	ANGELA CID 38820249K C/RAFAEL GOMEZ EL GALLO, CASA	549	NUEVA			ANDALUCIA	29660	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-10-07	1971-11-11	f
344	\N	\N	29602	ELISABETTA OCHIO	DATOS	X			CONFIRMAR	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-10-07	1900-01-01	f
345	\N	\N	952776704	PAOLA UBIALI X3216693M C/LAGO DE LOS	CISNES	1			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-10-14	1965-03-19	f
346	\N	\N	0163128833	ANNE CHRAN WIENERSTR	25	(ALEMANIA)			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-10-15	1968-03-15	f
347	\N	\N	629705315	AMAYA ZALBIDEGOITIA CORPION 722238857 C PARIS, 40	NUEVA	ANDALUCIA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-10-15	1949-02-06	f
348	\N	\N	952889452	VIVIAN LOEKKEN AVD DE RONDA 196,	LA	QUINTA			MARBELLA952889452	29660	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-10-21	1951-04-15	f
349	\N	\N	637547419	LIV MOSTUE URB ALBATROS HILL No30	C/2H	MARBELLA,			NUEVA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-10-21	1957-06-21	f
350	\N	\N	606754956	KINVARA VAUGHAN CASA SUR 5 MARBELLA	HILL	VILLAGE			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-10-22	1976-05-26	f
351	\N	\N	607456841	MARIA MENENDEZ ALVAREZ 5342686Q PSEO DE LA ESPERANZA	17	1oB			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-10-22	1956-03-13	f
352	\N	\N	666661924	FARAH ANNOUR AVD DE LAS NACIONES UNIDAS 43B	P.	BANUS			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-10-22	1900-01-01	f
353	\N	\N	619224443	ELSA MOONEN X621831A MONTE PARAISO BL E ALAMEDA	2o	PISO			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-10-22	1900-09-21	f
354	\N	\N	607706727	EVANINA MORCILLO MAKOW URB CASCADAS 121	SUPERMANZANA	H			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-10-27	1975-08-21	f
355	\N	\N	677243123	ANNY BELLINVIA C FERNANDO VII URB JAR. DE LA REPRE	F	2			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-10-28	1968-04-22	f
356	\N	\N	952813953	HAM EUN KYUNG C/ALCALA 15D SUPERMANZANA D	N.	ANDALUCIA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-10-30	1900-01-01	f
357	\N	\N	696531370	YOUSIF ALOMAR C ALCALA 15D SUPERMANZANA D	N.	ANDALUCIA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-10-30	1900-01-01	t
358	\N	\N	610849690	OLGA BOBROVA URB ARCO	IRIS	2-12			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-10-30	1980-01-02	f
359	\N	\N	630066688	ERNESTO FRANCO CARLANDER 24818710P RICARDO SORIANO 65	4o	3			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-11-04	1954-02-25	t
360	\N	\N	29602	LUCIEN AUGIER	DATOS	JANE			AUGIER	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-11-04	1900-01-01	t
361	\N	\N	29602	JAMES JORDAN HANS AMIGO DE LUKE,	DATOS	X			CONFIRMAR	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-11-04	1900-01-01	t
362	\N	\N	952776451	SANDRA BISMARK MARBELLA	HILL	CLUB			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-11-05	1941-12-31	f
363	\N	\N	29602	KAREN HARDCASTLE EL NARANJAL	55,	NUEVA			ANDALUCIA	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-11-10	1900-01-01	f
364	\N	\N	609571225	RICARDO MANCHO GAITE 12688635H C LOS LIRIOS 8	NUEVA	ANDALUCIA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-11-11	1949-08-07	t
365	\N	\N	627253150	YUNES U ALBATROS HILL C/LA CERQUILLA 51 P9	1oI	MARBELLA			(NUEVA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-11-14	1901-01-01	t
366	\N	\N	952775398	GONZALO LASSO FERNANDEZ URB RESERVA	DE	VALDEOLLETAS			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-11-20	1997-07-10	t
367	\N	\N	639210170	GUNNEL BERGMAN X5411667C APTO 239 SAN PEDRO	DE	ALCANTARA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-12-01	1967-06-22	f
368	\N	\N	626896862	JEANNINE SANCHEZ REIFEURATH 78982795J C/ LAS AMAPOLAS No 448B	No	ANDALUCIA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-12-03	1984-01-14	f
369	\N	\N	619992507	MAYTE CARRASTAZU ZAMORA 13618584P HUERTA DEL	PRADO	26			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-12-04	1940-05-08	f
370	\N	\N	609509912	FRANCISCO ROMERO GAVIRA 32040944N JARDINES DE SIERRA BLANCA DUPLEX K	BL	4			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-12-04	1970-10-20	t
371	\N	\N	609043639	ROBERTO PIZZAMIGLIO DATOS	X	COMPLETAR			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-12-12	1900-01-01	f
372	\N	\N	659192002	ALEXANDRA MOYA URB LOS PINOS DE ALOHA	GOLF	11B			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-12-19	1900-12-14	f
373	\N	\N	637866987	JEANINE SCHULZE LAS TERRAZAS DE	LAS	LOMAS			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-01-05	1987-08-13	f
374	\N	\N	952777983	MAGGY DENNIS DATOS	X	COMPLETAR			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-01-09	1900-01-01	f
375	\N	\N	952905028	MARIA ANTONIA ANIORTE DATOS	X	COMPLETAR			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-01-09	1900-01-01	f
376	\N	\N	952774568	JOSE TOVAR 27371795R C / CONDE DE	ORGAZ,	34			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-01-13	1973-12-14	t
377	\N	\N	622035123	HELENA EDIN ALTOS REALES A	No	27			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-01-13	1964-12-26	f
378	\N	\N	672044969	LORENZO CIVIERO URB CUMBRES	DEL	RODEO			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-01-13	1973-01-17	t
379	\N	\N	606278228	NOELIA GARCIA SANCHEZ 27348135P C RODRIGO DE	TRIANA	10-19			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-01-14	1977-11-13	f
380	\N	\N	670712132	CARMEN CASTELLANO X1846429N URB TOMILLAR DE	NAGUELES	31			MARBELLA	29600	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-01-15	1964-08-27	f
381	\N	\N	29602	ANA CHAPARRO CUÑADA DE CARMEN	LLAMAS,	MISMOS			DATOS	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-01-21	1900-01-01	f
382	\N	\N	902506060	M EUGENIA GODIA SANTANACH 391587805 CRTA	340KM	176			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-01-28	1962-01-28	f
383	\N	\N	646168887	DANIELLA GALLI X2841634F URB COSTA NAGUELES 1	P1	4D			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-01-28	1961-12-10	f
384	\N	\N	669892449	EMMANUELLE BAILLY CRTA DE	ISTAN	824			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-01-28	1975-07-08	f
385	\N	\N	670097097	ERIC ALBERT ZOHAR X2249261 CRTA DE	ISTAN	824			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-01-28	1962-08-30	t
386	\N	\N	952857768	NELLY MUNTE COTO REAL	APTO	29			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-01-30	1900-01-01	f
387	\N	\N	676455804	ISABEL NAVARRO MARTIN ANCON SIERRA LOMAS DE MC	RIVERA	P1			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-01-30	1900-09-14	f
388	\N	\N	677263390	ALLEGRA COLUSSI SERRAVALLO	LES	ROCHES			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-02-02	1984-04-07	f
389	\N	\N	697507125	LEDYS JIMENEZ X2782668 URB	BAHIA	ALCANTARA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-02-03	1900-01-01	f
391	\N	\N	616678536	NOEMI MOZO AGUILAR 78966586L AV ANTONIO BELON 16,	1o	3			MARBELLA	29600	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-02-04	1978-09-08	f
392	\N	\N	679169272	CONCHI AGUILAR BUENO 24851946D AVD ANTONIO BELON	16	3oA			MARBELLA	29600	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-02-04	1957-02-18	f
393	\N	\N	620897985	KAREN ANN PENFOLD X2396312B C/ DEL TEJON No2,	LOS	MONTEROS			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-02-04	1972-02-02	f
394	\N	\N	649079924	ANASTASIA BAYANOVA X2571991Q LAS LOMAS DE PTE	ROMANO	13			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-02-05	1984-05-12	f
395	\N	\N	952905028	YAIZA HERROJO ANIORTE 78970185F MUELLE RIVERA 101,	PTO	BANUS			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-02-05	1979-12-08	f
396	\N	\N	670676772	AIDA GOMEZ PALMA URB. LOS	PINOS-ALOHA	GOLF-CASA15D			MARBELLA	29660	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-02-10	1960-03-06	f
397	\N	\N	670676772	ITZIAR FAY URB. LOS PINOS ALOHA	GOLF,NUEVA	ANDALUCI			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-02-10	1993-05-07	f
399	\N	\N	679592810	M ANTONIA FORTIS AYLLON 24174776M Ma	AUXILIADORA,	5			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-02-16	1959-06-11	f
400	\N	\N	670419823	SARA MARTIN BLANCO 79026654B AV JESUS CAUTIVO 51, LANCE OFI SOL	I	8A			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-02-19	1983-07-15	f
401	\N	\N	652646786	JOHN GREGORY LOMAS DE MARBELLA CLUB 15,	LA	JOYA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-02-19	1979-10-15	t
402	\N	\N	649307804	CAROLINA SALEM X1652043E URB JARD DE LA QUINTA PINSAPO 2	AP	17			MARBELLA	29679	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-02-20	1976-06-28	f
403	\N	\N	663962438	TATI SIDORENKO AVD. DE LAS	CUMBRES	13-14			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-02-23	1975-05-03	f
404	\N	\N	637866987	ELLEN SCHULZE LAS LOMAS DE LOS TOROS,	MARBELLA	CLUB			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-02-27	1957-05-29	f
405	\N	\N	696807046	MERCEDES PEÑA VAZQUEZ 25596428G C/ JEREZ No 4	6oC	RONDA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-02-27	1976-05-12	f
406	\N	\N	656826339	NIEVES MONTERO TIRADO RESERVA DE LOS GRANADOS 402 FINCA	LA	CAR			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-02	1959-05-24	f
407	\N	\N	670785111	JUAN ANTONIO ROMERO BUSTAMANTE AVD GNRAL LOPEZ DOMINGUEZ 2 P	C	5oA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-02	1963-08-25	t
408	\N	\N	679402909	EVA CAPARROS ABELLAN URB JARDINES DOÑA	MARIA	7			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-02	1971-10-19	f
409	\N	\N	630310767	MARISELA CASTRO ABAD ALONSO DE BAZAN 8,	5o-OFI	39			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-02	1900-08-15	f
411	\N	\N	630803048	SAMAR EL	KAHWAJ	X4926254			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-03	1978-07-31	f
412	\N	\N	609600774	SILVIA MARTINEZ HURTADO 44576249H URB LA ALZAMBRA FASE III ESC	12	APT56			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-03	1975-12-15	f
413	\N	\N	657815158	JAVIER NIETO HOTEL PTE ROMANO 13	Y	14			MARBELLA	29600	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-03	1974-03-03	t
414	\N	\N	609464865	ELENA ILCHENKO X2275546 URB LOS MONTEROS PALM BEACH	APT	6AO			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-04	1972-11-25	f
415	\N	\N	628659756	LAILA CHAKIL	X6894764P	LCHAKIL@UK2.NET			MARBELLA	29600	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-05	1981-03-21	f
416	\N	\N	29602	KATRINA	SECHASTNOVA	COMPLETAR			DATOS	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-05	1900-01-01	f
417	\N	\N	952813533	ESMERALDA MARTINEZ CONDE MORENO 50270898M AVDA. DEL	PRADO	38T			MARBELLA	29660	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-06	1948-04-17	f
418	\N	\N	666278800		KATRINA	SEMICHASTNOVA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-06	1988-02-01	f
419	\N	\N	626287090	ASTRID GRUTMAN FRYNS X1716385X CRTRA. CADIZ	KM	179			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-04-02	1973-05-26	f
420	\N	\N	629693212	MARIA BERMUDO PIÑERO C JACINTO	BENAVENTE	11			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-09	1972-12-06	f
421	\N	\N	606156161	BRENDAM DOMLING NO	VIVE	AQUI			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-10	1900-01-01	t
422	\N	\N	677460043	CARLA CRUYLES 4765866R JOSE BERTRAN	9,PISO	6,1			BARCELONA	08021	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-10	1981-04-27	f
423	\N	\N	609280914		ELIZABETH	DOMINGUEZ			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2008-05-14	2000-12-11	f
424	\N	\N	607404444	ELINE ABOUTAKA X1014130Z CASA 31-32 ATALAYA DE	RIO	VERDE			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-10	1974-04-03	f
425	\N	\N	628897330	DEBORA	DUARRI	DEBORA@EUROPEAN-MAGAZINE.COM			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-10	1999-10-20	f
426	\N	\N	952883470	DAVID PASCOE 25 LAS LOMAS DEL MONTE	BIARRITZ	ATALAYA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-10	1999-10-20	t
427	\N	\N	609178551	GUSTAVO SEBASTIAN MILLAN SIERRA DE CAZORLA,RES.	LA	CASCADA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-10	1999-10-10	t
428	\N	\N	629558101	LUCIO GONZALEZ ESPADA 27339863A C/CARRERA	16,	OJEN			MARBELLA	29610	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-11	1973-01-22	t
429	\N	\N	952779224	LUCIEN AUGIER	C/VIVALDI	66			MARBELLA	29608	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-11	1925-04-02	t
430	\N	\N	639776170	JORGE LERIA 46123354M CRTA DE CADIZ KM 175	LA	ALCAZABA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-12	1946-12-14	t
431	\N	\N	634298525	MARJANNE MOTAMEDI SEÑORIO DE MARBELLA CAMINO DE	LA	CRUZ			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-12	2000-10-10	f
432	\N	\N	606373521	Ma CARMEN QUIJANO URB LOS GRANADOS 19,FASE	1,PTO	BANUS			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-12	2000-10-10	f
433	\N	\N	952882313	MARGARET GAWLAK JOHNS GUADALMINA BAJA,CALLE 8 P 19 CASA	DEL	RI			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-12	1959-05-06	f
434	\N	\N	952783410	JOHN MC CALLUM X2885524J URB. LOS ALMENDROS	52,LOS	ARQUEROS			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-12	1962-10-30	t
435	\N	\N	+194963668	JACQUELINE BRENDER 302	COTTONWOOD	CRT.			PIERMONT	10968	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-12	1968-08-20	f
436	\N	\N	697464721	KUIKAS	FALTAN	DATOS			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-12	2000-10-10	f
437	\N	\N	686012214	VANESA MANGE C19,P831 URB GUADALMINA ALTA	MARBELLA	SAN			PEDRO	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-12	1989-11-10	f
438	\N	\N	639778624	ROBERTO LAYA URB. SIERRA BLANCA,CALLE	MOZART	1			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-16	1948-02-18	t
439	\N	\N	690353121	ASUNCION DEL REAL RODRIGUEZ NUEVA ALCANTARA.LOS NARANJOS,BL	2,	4C			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-17	1943-09-18	f
440	\N	\N	952771197	ALEJANDRA HALLIN 92800234H FELIX RODRIGUEA DE LA FUENTE	2-OFIC	9			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-17	1967-01-15	f
441	\N	\N	660893928		ANA	CORTES			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-17	1975-02-01	f
442	\N	\N	952784921	ANTONIO MOYA 74809473H LOS	CIPRESES	46			MARBELLA	29627	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-17	1956-04-18	t
443	\N	\N	627518834	ANITA HORRY 6971541B URB EL MIRADOR DEL RODEO BL	6	APT613			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-17	1976-05-15	f
444	\N	\N	952782890	BERNADETTE	MARTINEZ	0674628Z			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-17	1939-05-20	f
445	\N	\N	952880031		CARMELO	72867677C			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-17	1949-06-06	t
446	\N	\N	672004711		CARLOTA	VISTABEL			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-17	1946-02-01	f
448	\N	\N	609230423	ISABEL ZUMTOBEL C/8 PARCELA 105	GUADALMINA	BAJA			MARBELLA	29678	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-18	1976-06-01	f
449	\N	\N	670973718	JESUS JAVIER DE LA PEÑA	BARTHEL	50284920Z			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-18	1970-05-04	f
450	\N	\N	952883803	MoLUISA FERNADEZ CORUGFDO Y GARCIA C/GALICIA 81,LOS	CARACOLILLOS	MARBELLA-SAN			PEDRO	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-19	1954-07-11	f
451	\N	\N	609514344	Mo JOSE TORRABADELLA URB EL PARAISO APTO.C/BONSAI	309	MARBELLA-			BENAHAVIS	29675	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-19	1940-06-20	f
452	\N	\N	609909689	MADELON VERHEUL ISLA	DE	GUADALMINA			MARBELLA	29670	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-19	1964-12-05	f
453	\N	\N	620680187	MERCEDES MORILLA URB MALIBU, APTO 15 BLOQ	2(RODEO	BEACH)			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-19	1950-05-01	f
454	\N	\N	952799978	EVA BERGMAN ANDERSSON AVD. CARMEN	SEVILLA	32			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-20	1948-06-05	f
455	\N	\N	646289963	ESTELA SAYAR RIVAS 1933926V URB EL RETIRO DE NAGÜELES	AP	132,C/PIZAR			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-20	1974-12-03	f
456	\N	\N	618743744	DANIEL	QUINTERO	MARTINEZ			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-20	1966-01-31	t
457	\N	\N	+194963239	NICK HILL 302 COTTON WOOD	CRT	PIERMONT			NY	10968	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-20	1966-06-02	t
458	\N	\N	639257685	VANESA CLASE	DE	PRUEBA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-20	1900-01-01	f
459	\N	\N	659925583	MAYTE CERVERA RODRIGUEZ 27336934P URB OASIS DE	NAGUELES	12			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-24	1966-05-03	f
460	\N	\N	952907824	MARI CARMEN VALLEJO RIVACOBA URB. PARCELAS DEL	GOLF,78	NUEVA			ANDALUCIA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-24	1950-10-15	f
461	\N	\N	952907824	UWE TESSEMER URB. PARCELAS DEL	GOLF,78	NUEVA			ANDALUCIA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-03-24	1947-06-23	t
462	\N	\N	29602	SILVANA ALEJANDRA DE	LEON	COMPLETAR			DATOS	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-04-01	1900-01-01	f
463	\N	\N	670550630	ALEJANDRO HUTCHINSON CLUB SIERRA, EDF GRANADA 15	CRTA	ISTAN			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-04-01	1949-05-05	t
464	\N	\N	609552519	BEGOÑA GARCIA-VAQUERO LAS CAÑAS BEACH FASE 1 PO 6	BAJO	B-C			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-04-06	1966-04-28	f
465	\N	\N	649412993	CHANTAL LAMBRECHTS MARBELLA HILL CLUB, LOS	HIBISCUS	1			MARBELLA	29600	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-04-08	1958-01-06	f
466	\N	\N	607483938	JESUS IBAÑEZ	SOLANO	15793211P			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-04-13	1954-05-29	t
467	\N	\N	609230423	ISABEL ZUMTOBEL C/8 P105 GUADALMINA	BAJA	SAN			PEDRO	29678	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-04-14	1961-09-24	f
468	\N	\N	603701818	ELIZABETH STAGEL	VICTORIA	SULTAN			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-04-22	1111-02-01	f
469	\N	\N	629523397	GUADALUPE PALOMO MURILLO 30198105 OASIS	DE	NAGUELES,5			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-04-30	1962-08-17	f
470	\N	\N	610666916	SILVANA DE LEON X4520241M SORIA Na1 6o	A	SAN			PEDRO	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-05-05	1979-11-29	f
471	\N	\N	636990005	CHRISTER JANSON C/CENTAURO No 1	NUEVA	ANDALUCIA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-05-05	1900-05-31	t
472	\N	\N	699308909	ALMUT ACHOETTLEN 356077984 AZAHARA	II,	10A			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-05-06	1968-05-07	f
473	\N	\N	666761633	MILAGROS FIGUEROA ROJAS X5249837H URB LOMAS DE LOS	MONTEROS	16CO			MARBELLA	29603	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-05-06	1974-07-22	f
474	\N	\N	637741542	GABRIELA LOBO ARGOTTE 09075663R LOS NARANJOS DE MARBELLA, MANZ	3&7	MARBELLA			NUEVA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-05-06	1970-06-05	f
475	\N	\N	691908749	SLAVA	LARIONOVA	63N576810			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-05-06	2000-10-10	f
476	\N	\N	691908479	ALINA KONNOVA 125,MOSCOW	FODEEVA	9			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-05-06	2000-10-10	f
477	\N	\N	607979449	BEATRICE VON RICHTHOFEN LAS BRISAS DEL GOLF C/	ALCAZAR	16			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-05-07	1993-09-09	f
478	\N	\N	672173043	MAYKA PEREZ PONCE 45736133N ARTURO RUBISTEIN 6 DON GONZALO E	5o	IZQU			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-05-12	1982-10-06	f
479	\N	\N	670640525	JOAN LOPIES MIRADOR	DEL	PARAISO			BENAHAVIS	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-05-13	2009-10-10	f
480	\N	\N	678630999	ITZIAR DE MENDIETA FLORES 78965482L GUADALMINA BAJA C/4	PARCELA	156			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-05-14	1967-06-05	f
481	\N	\N	620734653	ZUZANA NOVOTNA 0656881 URB BELLEVUE CASA 1	SUPERMANZANA	H			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-05-15	1975-04-08	f
482	\N	\N	607979449	BEATRIZ VON RICHTHOFEN LAS BRISAS DEL GOLF CALLE	ALCAZAR	16D			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-05-20	1993-09-09	f
483	\N	\N	619415811	JESSICA BERIRO VILLA CANDELARIA 16 U MARBELLA H	CLUB	II			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-05-26	1973-06-29	f
484	\N	\N	670625009	JOSE URBANO 27358857G AVD. PUERTA	DEL	MAR,5			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-06-08	1961-04-09	t
485	\N	\N	6708664115		RICHARD	OHMAN			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-06-10	1970-02-11	t
486	\N	\N	627578888	LUBA	COMPLETAR	DATOS			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-06-15	1900-01-01	f
487	\N	\N	629270235	MAURICE BERIRO	COMPLETAR	DATOS			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-06-18	1900-01-01	t
488	\N	\N	679587649	YOLANDA LOPEZ ALVAREZ 44288595W AVD JUAN CARLOS	I,4	ISTAN			MARBELLA	29611	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-06-19	1973-12-23	f
489	\N	\N	661005115	LEJLA IMAMOVIC C ALONSO DE QUIJADA OASIS	BANUS	302			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-06-23	1977-09-06	f
490	\N	\N	609311098	ANGELIKA LEGOWIK C/ VIVALDI 130	SIERRA	BLANCA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-06-23	1900-01-01	f
491	\N	\N	0796747903	MUSTAFA HIZO CLASE DE PRUEBA, NO ES	DE	AQUI			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-06-25	1900-01-01	t
492	\N	\N	636971126	MARIA MEDIO CACHAFEIRO 10800023M SINGLE HOME NAGUELES BL D	AT	IZQ			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-06-29	1955-05-03	f
493	\N	\N	655019199	Ma CARMEN CARRERA RODRIGUEZ 24804207H C/STROCO 25 URB	LOMAS	POZUELO			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-07-02	1955-07-04	f
494	\N	\N	609036327	MIGUEL PEREZ CUSTO ATALAYA RIO VERDE C PABLO	PICASSO	7			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-07-03	1952-08-01	t
495	\N	\N	609071818	DOLORES RUIZ-HAPPURI 33521001L URB CASABLANCA,	C/	YOGA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-07-08	1960-04-29	f
496	\N	\N	639125812	CAROLINA ROMERO CALDERON AVD SEVERO	OCHOA	24			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-07-08	1977-09-23	f
497	\N	\N	951317809	DEBBIE WOLFF 21	CHESTER	LANE			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-07-13	1900-01-01	f
498	\N	\N	680659004	ANDREA	COMPLETAR	DATOS			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-07-16	1900-01-01	f
499	\N	\N	609321951	MARTIN ENRICH BALSELLS 37601908J RB ST ISIDRE	59	IGUALADA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-07-17	1942-10-22	t
500	\N	\N	4477142042	SVETLANA LOMAS DE	SIERRA	BLANCA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-07-20	1980-04-02	f
501	\N	\N	678887958	ANGELA LOPEZ ALHAMBRA DEL MAR	No	17-21			MARBELLA	29600	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-07-24	1900-01-01	f
502	\N	\N	658619233	LADAN SATTARIPOUR DATOS X	CONFIRMAR,	VACACIONES			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-07-27	1900-01-01	f
503	\N	\N	655834313	CRISTINA VIYUELA AZCONA 835394B PSEO DE LOS PARQUES 6 PORTAL	5	2oC			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-07-28	1971-12-15	f
504	\N	\N	0778892254	AMANDA	COMPLETAR	DATOS			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-07-28	1900-01-01	f
505	\N	\N	29602	OUMAR	FATHI	COMPLETAR			DATOS	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-08-03	1900-01-01	t
506	\N	\N	29602		SALMAN	SHAHAB			COMPLETAR	DATOS	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-08-04	1900-01-01	t
507	\N	\N	609323257	JUAN CALLEJA URSINO 07212405L URB LOMAS SIERRA	BLANCA,EDF	MALAGA1oA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-08-04	1962-02-12	t
508	\N	\N	622115591	ASSEL KABYLOVA DATOS	X	COMPL			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-08-04	1900-01-01	f
509	\N	\N	609701510	ANTONIA PRATS VALLS SRA DE	MARTIN	ENRICH			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-08-07	1900-01-01	f
510	\N	\N	669797314	VICENTE GONZALEZ MANRIQUE 8800276Q BADAJOZ, VIENE	DE	VACAS			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-08-10	1962-08-28	t
511	\N	\N	952864371	EDITH ETTEDGUI OASIS DE BANUS, AMIGA DE ERIC	Y	ENMANUEL			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-08-10	1900-01-01	f
512	\N	\N	661720432	ANGELES SANTOS BERGUA 17775550T PADRE	DAMIAN	37			MADRID	28036	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-08-11	1936-06-07	f
513	\N	\N	638955267	BEATRIZ TERUELO URB AZALEA BEACH, EL	RIO	100			MARBELLA-NUEVA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-08-25	1977-07-31	f
514	\N	\N	0798360968	CRAIG FELDMAN EL OASIS DE MARBELLA	APTO	9JB			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-08-28	1900-01-01	t
515	\N	\N	693940351	ZAKIA ZOUGGAR PLAZA MARINA	BANUS	27-28			MARBELLA	29660	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-09-10	1973-05-02	f
516	\N	\N	649432305	JOSE LUIS TEJUCA GARCIA 25092398L RICARDO SORIANA	72,2o	G			MARBELLA	29600	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-09-10	1965-06-11	t
517	\N	\N	649432306	LUIS ALGAR CALDERON 18932796R RICARDO	SORIANA	72C,2oG			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-09-10	1961-09-14	t
518	\N	\N	625997732	MARIA IGNACIA BUENO LAPIEZA SIERRA DE CAZORLA	COTO	REAL2,APTO421			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-09-10	1959-12-12	f
519	\N	\N	607340288	JANA BELETSKY 255448174 LOS	MONTEROS	PARK			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-09-14	1986-01-25	f
520	\N	\N	633256994	VICTORIA KIRILENKO URB. ALZAMBRA BLOQ	3,AP	53			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-09-14	1978-06-11	f
522	\N	\N	617383655	CHELO MASMONTORIO ROCIO DE	NAGUELES	"PECHECHEPE"			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-09-22	1942-05-20	f
523	\N	\N	952810415	PATRICIO MC CADDEN C/ ATENAS No	8	SUPERMANZANA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-09-25	1954-08-02	t
524	\N	\N	660584774		ANTONIO	OROZCO			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-09-29	2000-10-10	t
525	\N	\N	687832538	PATRICIA NAVARRO JIMENEZ-AMPOSTA 78964372J AVD. DEL MAR,	20,	8a6			MARBELLA	29600	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-10-01	1976-12-18	f
526	\N	\N	670766426	GEMA BERZAL MONTES URB. ALTAVISTA BLOQ 5	BJ	C			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-10-01	1971-06-16	f
527	\N	\N	952860472		EBBE	CANTAMESSA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-10-01	1900-01-01	f
528	\N	\N	649295959	LOLA GONZALEZ MATEU 78973035M URB BAHIA DE MARBELLA AVD DE LA	INF	23			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-10-02	1962-04-28	f
529	\N	\N	29602	GRACIANA	MADRE	DE			ANGELIKA	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-10-02	1800-10-10	f
530	\N	\N	639579218	INES GALLO LEGUIZAMON 78985897X MARBELLA PUEBLO CASA	No	7			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-10-05	1960-05-15	f
531	\N	\N	29602	ANTONIO OROZCO ROSADO 25586161H URB. LAS TERRAZAS DE BEL AIR	BLO	5			P-2	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-10-05	1971-07-05	t
532	\N	\N	630572869	AMELIE VON	LIMBURG	STIRUM			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-10-06	1900-01-01	f
533	\N	\N	629587279	DULCE PACHECO PULIDO HACIENDA REAL 14	N.	ANDALUCIA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-10-07	1960-08-02	f
534	\N	\N	609512281	LLANOS ESPINOSA COBO 404690M ALTOS DE PTE	ROMANO	12			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-10-15	1962-11-20	f
535	\N	\N	952811817	SUSANA ARRIBAS 51639624R AVD. RIO VERDE URB ALZAMBRA	HILL	CLUB			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-10-20	1960-09-03	f
536	\N	\N	689552210		LARA	GARDENER			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-10-20	1900-01-01	f
537	\N	\N	667565657	DANIELA WARZEE ALBATROS HILL	C/	PLEYADES			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-10-21	1949-07-15	f
538	\N	\N	639464313	DIEGO DAVID MOYA TLF TRABJ671518748 X4457255Q URB. LOS VIÑEDOS	502	OJEN			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-10-28	1900-01-01	t
539	\N	\N	609550659	FRANK WESTERMANN X0587378H C/	MIRAMAR	14			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-10-28	1958-01-18	t
540	\N	\N	616469014	PEDRO FABREGA JAQMART MARBELLA HILL	CLUB	1			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-11-09	2000-10-10	t
541	\N	\N	610532398		SILVIA	SATUNAU			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-11-09	1954-04-10	f
542	\N	\N	660448313	IVONNE PANHAVIS URB ALDEA DORADA No 11	SUPERMANZANA	J			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-11-16	1966-05-05	f
543	\N	\N	605043552	ADAM NASH BUENA VISTA DE LA	5o	N.ANDALUCIA			MARBELLA	29660	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-11-18	1971-01-22	t
544	\N	\N	696547982	NATALIE NASH BUENA VISTA DE LA	5o	,1021			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-11-18	1973-04-06	f
545	\N	\N	659571362	BRYAN MCMULLEN MONTE PARAISO	COUNTRY	CLUB			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-11-23	1900-01-01	t
546	\N	\N	952908628	HIGH CARE CASA STA ISABEL S/N URB. LAS	MIMOSAS	MARBELLA,			NUEVA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-11-25	1900-01-01	t
547	\N	\N	952858648	INMACULADA MARINA ZUFIA C MOZART 1,URB.	SIERRA	BLANCA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-11-30	1963-12-07	f
548	\N	\N	659571362		EMMA	JONES			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-11-30	2000-12-30	f
549	\N	\N	951275156	VALA VALGERDUR FRANKLINS EL MADROÑAL 6,CASA GOYA	75	BENAHAVIS			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-12-12	1972-09-25	f
550	\N	\N	649409156	BERTA GARCIA AGUSTIN URB. LAS PETUÑAS FASE 2	CASA	2			MARBELLA	29670	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-12-14	1952-06-27	f
551	\N	\N	651833062	SUSANNE BEAUJEAN FLORENT SUPERMANZANA H URB. LE VILLAGE ARLES	7	NUEVA			ANDALUCIA	29660	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-12-14	1952-08-25	f
552	\N	\N	687426125	HAFIZ ZOUBIK PARCELA 6A MARBELLA	HILL	CLUB			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-12-18	1900-01-01	t
553	\N	\N	952117730		DANI	TUCKER			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-12-18	1983-08-21	f
554	\N	\N	610787859	CARMEN AGUILERA	EL	ROSARIO			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-12-22	1900-01-01	f
555	\N	\N	667634047	M JESUS TROYANO BAJO 78986813 GUADALMINA ALTA C/ 18 A	No	815			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2009-12-28	1991-01-10	f
556	\N	\N	605294700	FRANCE CHOA 40	KOLNIGSWATER,	SANYRES			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-01-08	1938-03-07	f
557	\N	\N	609512286	ANTONIO ROMAN	MARTIN	CORDETONI@GMAIL.COM			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-01-14	1900-01-01	t
558	\N	\N	696696194	YURI SU MUJER ES	CARMEN	AGUILERA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-01-14	1900-01-01	t
559	\N	\N	639384038	MANUEL PIÑERO	LA	QUINTA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-01-19	1952-09-01	t
560	\N	\N	678541659	BRIGITTE SIEBENVORN GUADALMINA BAJA C/7 CORTIJO	SAN	PEDRO			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-01-20	1959-11-28	f
561	\N	\N	654487790	PAQUI MUÑOZ MARTINEZ 522977605 C FRAY JUNIPERO SERRA 2 ESC	2	3A			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-01-20	1974-10-04	f
562	\N	\N	610571498	PAOLO GHIRELLI X0069228K AVD JULIO IGLESIAS CASA Y/Z APTO	36	BANU			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-01-21	1900-01-01	t
563	\N	\N	610393285	MARIA ALICIA DATOS	X	COMPLETAR			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-01-21	1900-01-01	f
564	\N	\N	952766448	MARIA ALICE MARLENIUK X4611596G C	LISAT	56			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-01-22	1977-07-11	f
565	\N	\N	629199506	MIREN ALONSO IDIÑA URB. LOS GRANADOS 1 APTO.	2211	PUERTO			BANUS	29660	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-01-25	1964-07-11	f
566	\N	\N	660309564	CARMEN VARELA ADANERO URB. CLUB SIERRA	TOLEDO	7			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-01-26	1963-07-16	f
567	\N	\N	605952187	ALLA KLYNOVA CALLE LAS	ADELFAS	235			MARBELLA	29670	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-01-28	1977-10-25	f
568	\N	\N	616505317	PAQUI MORILLA MACIAS URB. EL REAL BAJO	C/CLAVELES	59			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-01-29	1962-01-31	f
570	\N	\N	649749075	REMEDIOS FERNANDEZ RODRIGUEZ DATOS	X	COMPLETAR			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-02-04	1900-01-01	f
571	\N	\N	609543380	LOURDES DE LA VEGA COMPLETAR DATOS, AMIGA DE	PAOLO	GUIRELI			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-02-08	1900-01-01	f
572	\N	\N	952778531	ROCIO BARBA LISTE 31254616P URB GUADALPARK FASE 2	CASA	13			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-02-10	1969-04-19	f
573	\N	\N	669807187	MERCEDES GUERRERO AGUERA 7897345D C/HERMANOS	MAYEN	81N			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-02-12	1984-08-02	f
574	\N	\N	669807188	SILVIA GUERRERO AGUERA 78973454X C BADAJOZ 1	1a	A			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-02-12	1979-12-18	f
575	\N	\N	608251337	FRANKIE RAYNE 34D	LAS	ALAMANDAS			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-02-17	1958-07-06	f
576	\N	\N	608251337	BOBBIE RAYNE 34D	LAS	ALAMANDAS			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-02-17	1900-01-01	f
577	\N	\N	699449899	NAZ MEDHAT X5303913K LOMAS DE PTE ROMANO	CASA	12			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-02-18	1975-11-05	f
578	\N	\N	634043023	MERCEDES DE LASSALETTG	X63623425	C/NENUFAR,2			FUENGIROLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-02-20	1980-04-03	f
579	\N	\N	608381478		TINA	PATEL			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-02-23	1974-10-10	f
580	\N	\N	29602	JUAN ANTONIO JUANTEGUI	DATOS	POR			COMPLETAR	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-03-03	1890-01-01	t
581	\N	\N	617088756	IRINA LAZURENKO ALTOS REALES	10	A2			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-03-04	1957-12-14	f
582	\N	\N	636616500	EMILY ALEXANDRA SARROUF X1929810H MARBELLA HILL CLUB	PASEO	HIBISCUS,1			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-03-08	1988-08-10	f
583	\N	\N	679174656	ELIA DURAN GARCIA PRINCIPE DE VERGARA A EDIF	PROA	5D			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-03-16	1977-04-18	f
584	\N	\N	607949343	TATIANA TRIACCA ALTOS PTE. ROMANO C/VIRGEN	DE	BEGOÑA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-03-19	2010-01-01	f
586	\N	\N	639825657	GALINA KHRAMOVA X2813850F 102,CALLE CASARES,URB. ROCIO	DE	NAGUELES			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-03-26	1964-05-24	f
587	\N	\N	609250300	MARCOS GARCIA MONTES 21829828	NAZARÉ	No1			MADRID	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-03-31	1948-08-21	t
588	\N	\N	671697873	CLARA KRISTENSEN C/ ORION 58,	NUEVA	ANDALUCIA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-04-06	1995-01-04	f
589	\N	\N	667928778	PATRICIA MCDONALD	COMPLETAR	DATOS			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-04-12	1900-01-01	f
590	\N	\N	616394287	ANTONIO VISCONTI SANZ BERET Y ALVARADO 17818300Q EL MADROÑAL.C/VISCONTI	ENTRADA	6.			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-04-12	1960-12-09	t
591	\N	\N	609682228	LUISA HAFNER REIN 33392596T LOMAS DE MARBELLA	CLUB,COTO	REAL,12A			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-04-12	1956-12-30	f
592	\N	\N	29602	MARIE	GARNETT	COMPLETAR			DATOS	MARBELLA	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-04-13	1900-01-01	f
593	\N	\N	670733644	MARIE DE TROOSTEMBERGH "LOS ANGELITOS"	LA	MONTUA			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-04-14	1953-05-02	f
594	\N	\N	693537516	LILIYA SEMYKINA UB LOMAS R. VERDE CR ISTAN 10	LES	ROCHES			MARBELLA	29602	0.18														f		0	f	f	f		\N	-1	-1	f	t	0	2010-04-16	1988-01-03	f
\.



--
-- Data for Name: producto_contratado; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY producto_contratado (id, cliente_id, producto_compra_id, fecha_contratacion) FROM stdin;
\.



--
-- Data for Name: cuenta_bancaria_cliente; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY cuenta_bancaria_cliente (id, cliente_id, observaciones, banco, swif, iban, cuenta) FROM stdin;
\.



--
-- Data for Name: pedido_venta; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY pedido_venta (id, cliente_id, tarifa_id, transporte_a_cargo, fecha, numpedido, iva, descuento, bloqueado, cerrado, envio_direccion, envio_ciudad, envio_provincia, envio_cp, envio_pais, nombre_correspondencia, direccion_correspondencia, cp_correspondencia, ciudad_correspondencia, provincia_correspondencia, pais_correspondencia) FROM stdin;
\.



--
-- Data for Name: presupuesto; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY presupuesto (id, cliente_id, fecha, persona_contacto, nombrecliente, direccion, ciudad, provincia, cp, pais, telefono, fax, texto, despedida, validez, numpresupuesto, descuento) FROM stdin;
\.



--
-- Data for Name: albaran_salida; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY albaran_salida (id, numalbaran, transportista_id, cliente_id, fecha, nombre, direccion, cp, ciudad, telefono, pais, observaciones, facturable, motivo, bloqueado, destino_id, almacen_origen_id, almacen_destino_id) FROM stdin;
\.



--
-- Data for Name: factura_venta; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY factura_venta (id, cliente_id, fecha, numfactura, descuento, cargo, observaciones, iva, bloqueada, irpf) FROM stdin;
\.



--
-- Data for Name: prefactura; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY prefactura (id, cliente_id, fecha, numfactura, descuento, cargo, observaciones, iva, bloqueada, irpf) FROM stdin;
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
10	2010-03-10 18:23:40.45723	10
11	2010-03-10 18:28:13.316183	11
12	2010-03-24 13:57:33.448021	12
13	2010-04-20 14:08:36.380543	13
\.



--
-- Data for Name: linea_de_venta; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY linea_de_venta (id, pedido_venta_id, albaran_salida_id, factura_venta_id, prefactura_id, fechahora, cantidad, precio, descuento, producto_compra_id, ticket_id, notas, descripcion_complementaria) FROM stdin;
19	\N	\N	\N	\N	2010-04-20 14:08:36	1	45.000000000000007	0	3	13		
\.



--
-- Data for Name: linea_de_pedido; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY linea_de_pedido (id, pedido_venta_id, fechahora, cantidad, precio, descuento, fecha_entrega, texto_entrega, producto_compra_id, presupuesto_id, notas) FROM stdin;
\.



--
-- Data for Name: evento; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY evento (id, nombre, color_r, color_g, color_b) FROM stdin;
1	Cursos	0	120	255
3	Festivos	22	249	244
2	Vacaciones	200	0	131
\.



--
-- Data for Name: grupo_alumnos; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY grupo_alumnos (id, empleado_id, nombre, color_r, color_g, color_b, cupo) FROM stdin;
7	\N	GR 10A L-X-V	248	245	2	6
5	1	GR 8A M-J	23	222	51	6
1	\N	GR 10B L-X-V	171	24	224	6
11	1	GR 14 A L-X	240	128	16	6
8	\N	GR 10C M-J	248	245	2	6
15	1	GR 17B M-J	240	128	2	6
6	2	Gr 9A L-X-V	243	112	15	6
19	\N	GR 9D M-J	19	247	12	3
2	\N	GR 9B L-X-V	231	25	30	6
10	\N	GR 10D M-J	4	248	13	6
9	\N	GR 11 L-X	4	248	13	6
12	7	GR 14B M-J	248	245	2	6
16	\N	GR 18A M-J	248	245	2	6
3	1	GR 8B X-V	243	7	7	3
4	\N	GR 9.15 C M-J	248	245	2	6
17	\N	GR 18B M-V	240	128	16	6
14	\N	GR 17A M-J	248	245	2	6
13	9	GR 14.30 C L-X	4	248	13	6
18	\N	GR 20 L-X	248	245	2	6
\.



--
-- Data for Name: servicio; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY servicio (id, factura_venta_id, prefactura_id, albaran_salida_id, concepto, cantidad, precio, descuento, pedido_venta_id, presupuesto_id, notas) FROM stdin;
\.



--
-- Data for Name: actividad; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY actividad (id, evento_id, fechahora_inicio, fechahora_fin, descripcion, empleado_id, servicio_id) FROM stdin;
53	\N	2010-04-20 14:30:00	2010-04-20 15:30:00	adri	5	\N
259	\N	2010-04-22 17:00:00	2010-04-22 18:00:00	GR 17A M-J	\N	\N
260	\N	2010-04-27 17:00:00	2010-04-27 18:00:00	GR 17A M-J	\N	\N
261	\N	2010-04-29 17:00:00	2010-04-29 18:00:00	GR 17A M-J	\N	\N
262	\N	2010-05-04 17:00:00	2010-05-04 18:00:00	GR 17A M-J	\N	\N
263	\N	2010-05-06 17:00:00	2010-05-06 18:00:00	GR 17A M-J	\N	\N
264	\N	2010-05-11 17:00:00	2010-05-11 18:00:00	GR 17A M-J	\N	\N
265	\N	2010-05-13 17:00:00	2010-05-13 18:00:00	GR 17A M-J	\N	\N
266	\N	2010-05-18 17:00:00	2010-05-18 18:00:00	GR 17A M-J	\N	\N
267	\N	2010-05-20 17:00:00	2010-05-20 18:00:00	GR 17A M-J	\N	\N
268	\N	2010-05-25 17:00:00	2010-05-25 18:00:00	GR 17A M-J	\N	\N
269	\N	2010-05-27 17:00:00	2010-05-27 18:00:00	GR 17A M-J	\N	\N
270	\N	2010-06-01 17:00:00	2010-06-01 18:00:00	GR 17A M-J	\N	\N
271	\N	2010-06-03 17:00:00	2010-06-03 18:00:00	GR 17A M-J	\N	\N
272	\N	2010-06-08 17:00:00	2010-06-08 18:00:00	GR 17A M-J	\N	\N
273	\N	2010-06-10 17:00:00	2010-06-10 18:00:00	GR 17A M-J	\N	\N
274	\N	2010-06-15 17:00:00	2010-06-15 18:00:00	GR 17A M-J	\N	\N
275	\N	2010-06-17 17:00:00	2010-06-17 18:00:00	GR 17A M-J	\N	\N
276	\N	2010-06-22 17:00:00	2010-06-22 18:00:00	GR 17A M-J	\N	\N
277	\N	2010-06-24 17:00:00	2010-06-24 18:00:00	GR 17A M-J	\N	\N
278	\N	2010-06-29 17:00:00	2010-06-29 18:00:00	GR 17A M-J	\N	\N
279	\N	2010-07-01 17:00:00	2010-07-01 18:00:00	GR 17A M-J	\N	\N
280	\N	2010-07-06 17:00:00	2010-07-06 18:00:00	GR 17A M-J	\N	\N
281	\N	2010-07-08 17:00:00	2010-07-08 18:00:00	GR 17A M-J	\N	\N
282	\N	2010-07-13 17:00:00	2010-07-13 18:00:00	GR 17A M-J	\N	\N
283	\N	2010-07-15 17:00:00	2010-07-15 18:00:00	GR 17A M-J	\N	\N
284	\N	2010-07-20 17:00:00	2010-07-20 18:00:00	GR 17A M-J	\N	\N
285	\N	2010-07-22 17:00:00	2010-07-22 18:00:00	GR 17A M-J	\N	\N
286	\N	2010-07-27 17:00:00	2010-07-27 18:00:00	GR 17A M-J	\N	\N
287	\N	2010-07-29 17:00:00	2010-07-29 18:00:00	GR 17A M-J	\N	\N
288	\N	2010-08-03 17:00:00	2010-08-03 18:00:00	GR 17A M-J	\N	\N
289	\N	2010-08-05 17:00:00	2010-08-05 18:00:00	GR 17A M-J	\N	\N
290	\N	2010-08-10 17:00:00	2010-08-10 18:00:00	GR 17A M-J	\N	\N
291	\N	2010-08-12 17:00:00	2010-08-12 18:00:00	GR 17A M-J	\N	\N
292	\N	2010-08-17 17:00:00	2010-08-17 18:00:00	GR 17A M-J	\N	\N
293	\N	2010-08-19 17:00:00	2010-08-19 18:00:00	GR 17A M-J	\N	\N
294	\N	2010-08-24 17:00:00	2010-08-24 18:00:00	GR 17A M-J	\N	\N
295	\N	2010-08-26 17:00:00	2010-08-26 18:00:00	GR 17A M-J	\N	\N
296	\N	2010-08-31 17:00:00	2010-08-31 18:00:00	GR 17A M-J	\N	\N
297	\N	2010-09-02 17:00:00	2010-09-02 18:00:00	GR 17A M-J	\N	\N
298	\N	2010-09-07 17:00:00	2010-09-07 18:00:00	GR 17A M-J	\N	\N
299	\N	2010-09-09 17:00:00	2010-09-09 18:00:00	GR 17A M-J	\N	\N
300	\N	2010-09-14 17:00:00	2010-09-14 18:00:00	GR 17A M-J	\N	\N
301	\N	2010-09-16 17:00:00	2010-09-16 18:00:00	GR 17A M-J	\N	\N
302	\N	2010-09-21 17:00:00	2010-09-21 18:00:00	GR 17A M-J	\N	\N
303	\N	2010-09-23 17:00:00	2010-09-23 18:00:00	GR 17A M-J	\N	\N
304	\N	2010-09-28 17:00:00	2010-09-28 18:00:00	GR 17A M-J	\N	\N
305	\N	2010-09-30 17:00:00	2010-09-30 18:00:00	GR 17A M-J	\N	\N
306	\N	2010-10-05 17:00:00	2010-10-05 18:00:00	GR 17A M-J	\N	\N
307	\N	2010-10-07 17:00:00	2010-10-07 18:00:00	GR 17A M-J	\N	\N
308	\N	2010-10-12 17:00:00	2010-10-12 18:00:00	GR 17A M-J	\N	\N
309	\N	2010-10-14 17:00:00	2010-10-14 18:00:00	GR 17A M-J	\N	\N
310	\N	2010-10-19 17:00:00	2010-10-19 18:00:00	GR 17A M-J	\N	\N
311	\N	2010-10-21 17:00:00	2010-10-21 18:00:00	GR 17A M-J	\N	\N
312	\N	2010-10-26 17:00:00	2010-10-26 18:00:00	GR 17A M-J	\N	\N
313	\N	2010-10-28 17:00:00	2010-10-28 18:00:00	GR 17A M-J	\N	\N
314	\N	2010-11-02 17:00:00	2010-11-02 18:00:00	GR 17A M-J	\N	\N
315	\N	2010-11-04 17:00:00	2010-11-04 18:00:00	GR 17A M-J	\N	\N
316	\N	2010-11-09 17:00:00	2010-11-09 18:00:00	GR 17A M-J	\N	\N
317	\N	2010-11-11 17:00:00	2010-11-11 18:00:00	GR 17A M-J	\N	\N
318	\N	2010-11-16 17:00:00	2010-11-16 18:00:00	GR 17A M-J	\N	\N
319	\N	2010-11-18 17:00:00	2010-11-18 18:00:00	GR 17A M-J	\N	\N
320	\N	2010-11-23 17:00:00	2010-11-23 18:00:00	GR 17A M-J	\N	\N
321	\N	2010-11-25 17:00:00	2010-11-25 18:00:00	GR 17A M-J	\N	\N
322	\N	2010-11-30 17:00:00	2010-11-30 18:00:00	GR 17A M-J	\N	\N
323	\N	2010-12-02 17:00:00	2010-12-02 18:00:00	GR 17A M-J	\N	\N
324	\N	2010-12-07 17:00:00	2010-12-07 18:00:00	GR 17A M-J	\N	\N
325	\N	2010-12-09 17:00:00	2010-12-09 18:00:00	GR 17A M-J	\N	\N
326	\N	2010-12-14 17:00:00	2010-12-14 18:00:00	GR 17A M-J	\N	\N
327	\N	2010-12-16 17:00:00	2010-12-16 18:00:00	GR 17A M-J	\N	\N
328	\N	2010-12-21 17:00:00	2010-12-21 18:00:00	GR 17A M-J	\N	\N
329	\N	2010-12-23 17:00:00	2010-12-23 18:00:00	GR 17A M-J	\N	\N
330	\N	2010-12-28 17:00:00	2010-12-28 18:00:00	GR 17A M-J	\N	\N
331	\N	2010-12-30 17:00:00	2010-12-30 18:00:00	GR 17A M-J	\N	\N
258	\N	2010-04-20 17:00:00	2010-04-20 18:00:00	GR 17A M-J	1	\N
3	\N	2010-02-11 13:31:00	2010-02-11 14:31:00	Rehabilitación clase 1	\N	\N
30	\N	2010-03-19 14:28:00	2010-03-19 15:28:00	Prueba	2	\N
150	\N	2010-08-06 10:00:00	2010-08-06 11:00:00	GR 10B L-X-V	\N	\N
151	\N	2010-08-09 10:00:00	2010-08-09 11:00:00	GR 10B L-X-V	\N	\N
152	\N	2010-08-11 10:00:00	2010-08-11 11:00:00	GR 10B L-X-V	\N	\N
153	\N	2010-08-13 10:00:00	2010-08-13 11:00:00	GR 10B L-X-V	\N	\N
154	\N	2010-08-16 10:00:00	2010-08-16 11:00:00	GR 10B L-X-V	\N	\N
155	\N	2010-08-18 10:00:00	2010-08-18 11:00:00	GR 10B L-X-V	\N	\N
156	\N	2010-08-20 10:00:00	2010-08-20 11:00:00	GR 10B L-X-V	\N	\N
6	\N	2010-02-14 13:31:00	2010-02-14 14:31:00	Rehabilitación (refuerzo)	\N	\N
5	\N	2010-02-13 13:31:00	2010-02-13 14:50:00	Rehabilitación clase 3	\N	\N
7	\N	2010-02-15 13:31:00	2010-02-15 14:31:00	Rehabilitación (clase 4)	\N	\N
8	\N	2010-02-16 13:31:00	2010-02-16 14:31:00	Rehabilitación (clase 5)	\N	\N
9	\N	2010-02-17 13:31:00	2010-02-17 14:31:00	Rehabilitación (clase 1)	\N	\N
11	\N	2010-02-19 13:31:00	2010-02-19 14:31:00	Rehabilitación (relajación)	\N	\N
15	\N	2010-02-23 13:31:00	2010-02-23 14:31:00	Rehabilitación (clase 2)	\N	\N
10	\N	2010-02-18 13:31:00	2010-02-18 14:31:00	Rehabilitación (clase 2)	\N	\N
12	\N	2010-02-20 13:31:00	2010-02-20 14:31:00	Rehabilitación (clase 3)	2	\N
14	\N	2010-02-22 13:31:00	2010-02-22 14:31:00	Rehabilitación (clase 1)	\N	\N
157	\N	2010-08-23 10:00:00	2010-08-23 11:00:00	GR 10B L-X-V	\N	\N
158	\N	2010-08-25 10:00:00	2010-08-25 11:00:00	GR 10B L-X-V	\N	\N
159	\N	2010-08-27 10:00:00	2010-08-27 11:00:00	GR 10B L-X-V	\N	\N
160	\N	2010-08-30 10:00:00	2010-08-30 11:00:00	GR 10B L-X-V	\N	\N
161	\N	2010-09-01 10:00:00	2010-09-01 11:00:00	GR 10B L-X-V	\N	\N
35	\N	2010-03-26 10:00:00	2010-03-26 11:00:00	Clases lunes PH	\N	\N
32	\N	2010-03-23 10:00:00	2010-03-23 11:00:00	Clases lunes PH	1	\N
34	\N	2010-03-25 10:00:00	2010-03-25 11:00:00	Clases lunes PH	2	\N
38	\N	2010-03-25 12:10:00	2010-03-25 13:10:00	Clase 2	\N	\N
37	\N	2010-03-23 12:10:00	2010-03-23 13:10:00	Clase 2	2	\N
36	\N	2010-03-23 12:00:00	2010-03-23 13:00:00	Clase 1	2	\N
121	\N	2010-05-31 10:00:00	2010-05-31 11:00:00	GR 10B L-X-V	\N	\N
40	\N	2010-03-25 14:30:00	2010-03-25 15:30:00	adri	\N	\N
41	\N	2010-03-27 14:30:00	2010-03-27 15:30:00	adri	\N	\N
42	\N	2010-03-29 14:30:00	2010-03-29 15:30:00	adri	\N	\N
43	\N	2010-03-31 14:30:00	2010-03-31 15:30:00	adri	\N	\N
44	\N	2010-04-02 14:30:00	2010-04-02 15:30:00	adri	\N	\N
45	\N	2010-04-04 14:30:00	2010-04-04 15:30:00	adri	\N	\N
46	\N	2010-04-06 14:30:00	2010-04-06 15:30:00	adri	\N	\N
47	\N	2010-04-08 14:30:00	2010-04-08 15:30:00	adri	\N	\N
48	\N	2010-04-10 14:30:00	2010-04-10 15:30:00	adri	\N	\N
49	\N	2010-04-12 14:30:00	2010-04-12 15:30:00	adri	\N	\N
50	\N	2010-04-14 14:30:00	2010-04-14 15:30:00	adri	\N	\N
51	\N	2010-04-16 14:30:00	2010-04-16 15:30:00	adri	\N	\N
52	\N	2010-04-18 14:30:00	2010-04-18 15:30:00	adri	\N	\N
54	\N	2010-04-22 14:30:00	2010-04-22 15:30:00	adri	\N	\N
55	\N	2010-04-24 14:30:00	2010-04-24 15:30:00	adri	\N	\N
56	\N	2010-04-26 14:30:00	2010-04-26 15:30:00	adri	\N	\N
57	\N	2010-04-28 14:30:00	2010-04-28 15:30:00	adri	\N	\N
58	\N	2010-04-30 14:30:00	2010-04-30 15:30:00	adri	\N	\N
59	\N	2010-05-02 14:30:00	2010-05-02 15:30:00	adri	\N	\N
60	\N	2010-05-04 14:30:00	2010-05-04 15:30:00	adri	\N	\N
61	\N	2010-05-06 14:30:00	2010-05-06 15:30:00	adri	\N	\N
62	\N	2010-05-08 14:30:00	2010-05-08 15:30:00	adri	\N	\N
63	\N	2010-05-10 14:30:00	2010-05-10 15:30:00	adri	\N	\N
64	\N	2010-05-12 14:30:00	2010-05-12 15:30:00	adri	\N	\N
65	\N	2010-05-14 14:30:00	2010-05-14 15:30:00	adri	\N	\N
66	\N	2010-05-16 14:30:00	2010-05-16 15:30:00	adri	\N	\N
67	\N	2010-05-18 14:30:00	2010-05-18 15:30:00	adri	\N	\N
68	\N	2010-05-20 14:30:00	2010-05-20 15:30:00	adri	\N	\N
69	\N	2010-05-22 14:30:00	2010-05-22 15:30:00	adri	\N	\N
70	\N	2010-05-24 14:30:00	2010-05-24 15:30:00	adri	\N	\N
71	\N	2010-05-26 14:30:00	2010-05-26 15:30:00	adri	\N	\N
72	\N	2010-05-28 14:30:00	2010-05-28 15:30:00	adri	\N	\N
73	\N	2010-05-30 14:30:00	2010-05-30 15:30:00	adri	\N	\N
74	\N	2010-06-01 14:30:00	2010-06-01 15:30:00	adri	\N	\N
75	\N	2010-06-03 14:30:00	2010-06-03 15:30:00	adri	\N	\N
76	\N	2010-06-05 14:30:00	2010-06-05 15:30:00	adri	\N	\N
77	\N	2010-06-07 14:30:00	2010-06-07 15:30:00	adri	\N	\N
78	\N	2010-06-09 14:30:00	2010-06-09 15:30:00	adri	\N	\N
79	\N	2010-06-11 14:30:00	2010-06-11 15:30:00	adri	\N	\N
80	\N	2010-06-13 14:30:00	2010-06-13 15:30:00	adri	\N	\N
81	\N	2010-06-15 14:30:00	2010-06-15 15:30:00	adri	\N	\N
82	\N	2010-06-17 14:30:00	2010-06-17 15:30:00	adri	\N	\N
83	\N	2010-06-19 14:30:00	2010-06-19 15:30:00	adri	\N	\N
84	\N	2010-06-21 14:30:00	2010-06-21 15:30:00	adri	\N	\N
85	\N	2010-06-23 14:30:00	2010-06-23 15:30:00	adri	\N	\N
86	\N	2010-06-25 14:30:00	2010-06-25 15:30:00	adri	\N	\N
87	\N	2010-06-27 14:30:00	2010-06-27 15:30:00	adri	\N	\N
88	\N	2010-06-29 14:30:00	2010-06-29 15:30:00	adri	\N	\N
122	\N	2010-06-02 10:00:00	2010-06-02 11:00:00	GR 10B L-X-V	\N	\N
39	\N	2010-03-23 14:30:00	2010-03-23 15:30:00	adri	2	\N
123	\N	2010-06-04 10:00:00	2010-06-04 11:00:00	GR 10B L-X-V	\N	\N
124	\N	2010-06-07 10:00:00	2010-06-07 11:00:00	GR 10B L-X-V	\N	\N
125	\N	2010-06-09 10:00:00	2010-06-09 11:00:00	GR 10B L-X-V	\N	\N
126	\N	2010-06-11 10:00:00	2010-06-11 11:00:00	GR 10B L-X-V	\N	\N
127	\N	2010-06-14 10:00:00	2010-06-14 11:00:00	GR 10B L-X-V	\N	\N
128	\N	2010-06-16 10:00:00	2010-06-16 11:00:00	GR 10B L-X-V	\N	\N
129	\N	2010-06-18 10:00:00	2010-06-18 11:00:00	GR 10B L-X-V	\N	\N
31	\N	2010-03-22 10:00:00	2010-03-22 11:00:00	Clases lunes PH	\N	\N
130	\N	2010-06-21 10:00:00	2010-06-21 11:00:00	GR 10B L-X-V	\N	\N
131	\N	2010-06-23 10:00:00	2010-06-23 11:00:00	GR 10B L-X-V	\N	\N
132	\N	2010-06-25 10:00:00	2010-06-25 11:00:00	GR 10B L-X-V	\N	\N
133	\N	2010-06-28 10:00:00	2010-06-28 11:00:00	GR 10B L-X-V	\N	\N
91	\N	2010-03-24 11:00:00	2010-03-24 12:00:00	ana cortesia	9	\N
33	\N	2010-03-24 10:00:00	2010-03-24 11:00:00	grupo 10 A	7	\N
93	\N	2010-03-26 10:00:00	2010-03-26 11:00:00	GR 10B L-X-V	\N	\N
94	\N	2010-03-29 10:00:00	2010-03-29 11:00:00	GR 10B L-X-V	\N	\N
95	\N	2010-03-31 10:00:00	2010-03-31 11:00:00	GR 10B L-X-V	\N	\N
96	\N	2010-04-02 10:00:00	2010-04-02 11:00:00	GR 10B L-X-V	\N	\N
97	\N	2010-04-05 10:00:00	2010-04-05 11:00:00	GR 10B L-X-V	\N	\N
98	\N	2010-04-07 10:00:00	2010-04-07 11:00:00	GR 10B L-X-V	\N	\N
99	\N	2010-04-09 10:00:00	2010-04-09 11:00:00	GR 10B L-X-V	\N	\N
100	\N	2010-04-12 10:00:00	2010-04-12 11:00:00	GR 10B L-X-V	\N	\N
101	\N	2010-04-14 10:00:00	2010-04-14 11:00:00	GR 10B L-X-V	\N	\N
102	\N	2010-04-16 10:00:00	2010-04-16 11:00:00	GR 10B L-X-V	\N	\N
103	\N	2010-04-19 10:00:00	2010-04-19 11:00:00	GR 10B L-X-V	\N	\N
104	\N	2010-04-21 10:00:00	2010-04-21 11:00:00	GR 10B L-X-V	\N	\N
105	\N	2010-04-23 10:00:00	2010-04-23 11:00:00	GR 10B L-X-V	\N	\N
106	\N	2010-04-26 10:00:00	2010-04-26 11:00:00	GR 10B L-X-V	\N	\N
107	\N	2010-04-28 10:00:00	2010-04-28 11:00:00	GR 10B L-X-V	\N	\N
108	\N	2010-04-30 10:00:00	2010-04-30 11:00:00	GR 10B L-X-V	\N	\N
109	\N	2010-05-03 10:00:00	2010-05-03 11:00:00	GR 10B L-X-V	\N	\N
110	\N	2010-05-05 10:00:00	2010-05-05 11:00:00	GR 10B L-X-V	\N	\N
111	\N	2010-05-07 10:00:00	2010-05-07 11:00:00	GR 10B L-X-V	\N	\N
112	\N	2010-05-10 10:00:00	2010-05-10 11:00:00	GR 10B L-X-V	\N	\N
113	\N	2010-05-12 10:00:00	2010-05-12 11:00:00	GR 10B L-X-V	\N	\N
114	\N	2010-05-14 10:00:00	2010-05-14 11:00:00	GR 10B L-X-V	\N	\N
115	\N	2010-05-17 10:00:00	2010-05-17 11:00:00	GR 10B L-X-V	\N	\N
116	\N	2010-05-19 10:00:00	2010-05-19 11:00:00	GR 10B L-X-V	\N	\N
117	\N	2010-05-21 10:00:00	2010-05-21 11:00:00	GR 10B L-X-V	\N	\N
118	\N	2010-05-24 10:00:00	2010-05-24 11:00:00	GR 10B L-X-V	\N	\N
119	\N	2010-05-26 10:00:00	2010-05-26 11:00:00	GR 10B L-X-V	\N	\N
120	\N	2010-05-28 10:00:00	2010-05-28 11:00:00	GR 10B L-X-V	\N	\N
134	\N	2010-06-30 10:00:00	2010-06-30 11:00:00	GR 10B L-X-V	\N	\N
135	\N	2010-07-02 10:00:00	2010-07-02 11:00:00	GR 10B L-X-V	\N	\N
136	\N	2010-07-05 10:00:00	2010-07-05 11:00:00	GR 10B L-X-V	\N	\N
137	\N	2010-07-07 10:00:00	2010-07-07 11:00:00	GR 10B L-X-V	\N	\N
138	\N	2010-07-09 10:00:00	2010-07-09 11:00:00	GR 10B L-X-V	\N	\N
139	\N	2010-07-12 10:00:00	2010-07-12 11:00:00	GR 10B L-X-V	\N	\N
140	\N	2010-07-14 10:00:00	2010-07-14 11:00:00	GR 10B L-X-V	\N	\N
141	\N	2010-07-16 10:00:00	2010-07-16 11:00:00	GR 10B L-X-V	\N	\N
142	\N	2010-07-19 10:00:00	2010-07-19 11:00:00	GR 10B L-X-V	\N	\N
143	\N	2010-07-21 10:00:00	2010-07-21 11:00:00	GR 10B L-X-V	\N	\N
144	\N	2010-07-23 10:00:00	2010-07-23 11:00:00	GR 10B L-X-V	\N	\N
145	\N	2010-07-26 10:00:00	2010-07-26 11:00:00	GR 10B L-X-V	\N	\N
146	\N	2010-07-28 10:00:00	2010-07-28 11:00:00	GR 10B L-X-V	\N	\N
147	\N	2010-07-30 10:00:00	2010-07-30 11:00:00	GR 10B L-X-V	\N	\N
148	\N	2010-08-02 10:00:00	2010-08-02 11:00:00	GR 10B L-X-V	\N	\N
149	\N	2010-08-04 10:00:00	2010-08-04 11:00:00	GR 10B L-X-V	\N	\N
162	\N	2010-09-03 10:00:00	2010-09-03 11:00:00	GR 10B L-X-V	\N	\N
163	\N	2010-09-06 10:00:00	2010-09-06 11:00:00	GR 10B L-X-V	\N	\N
164	\N	2010-09-08 10:00:00	2010-09-08 11:00:00	GR 10B L-X-V	\N	\N
165	\N	2010-09-10 10:00:00	2010-09-10 11:00:00	GR 10B L-X-V	\N	\N
166	\N	2010-09-13 10:00:00	2010-09-13 11:00:00	GR 10B L-X-V	\N	\N
167	\N	2010-09-15 10:00:00	2010-09-15 11:00:00	GR 10B L-X-V	\N	\N
168	\N	2010-09-17 10:00:00	2010-09-17 11:00:00	GR 10B L-X-V	\N	\N
169	\N	2010-09-20 10:00:00	2010-09-20 11:00:00	GR 10B L-X-V	\N	\N
170	\N	2010-09-22 10:00:00	2010-09-22 11:00:00	GR 10B L-X-V	\N	\N
171	\N	2010-09-24 10:00:00	2010-09-24 11:00:00	GR 10B L-X-V	\N	\N
172	\N	2010-09-27 10:00:00	2010-09-27 11:00:00	GR 10B L-X-V	\N	\N
173	\N	2010-09-29 10:00:00	2010-09-29 11:00:00	GR 10B L-X-V	\N	\N
174	\N	2010-03-24 12:00:00	2010-03-24 13:00:00	Adriana López Sánchez	2	\N
177	\N	2010-03-30 09:00:00	2010-03-30 10:00:00	GR 9D M-J	\N	\N
178	\N	2010-04-01 09:00:00	2010-04-01 10:00:00	GR 9D M-J	\N	\N
179	\N	2010-04-06 09:00:00	2010-04-06 10:00:00	GR 9D M-J	\N	\N
180	\N	2010-04-08 09:00:00	2010-04-08 10:00:00	GR 9D M-J	\N	\N
181	\N	2010-04-13 09:00:00	2010-04-13 10:00:00	GR 9D M-J	\N	\N
182	\N	2010-04-15 09:00:00	2010-04-15 10:00:00	GR 9D M-J	\N	\N
184	\N	2010-04-22 09:00:00	2010-04-22 10:00:00	GR 9D M-J	\N	\N
185	\N	2010-04-27 09:00:00	2010-04-27 10:00:00	GR 9D M-J	\N	\N
186	\N	2010-04-29 09:00:00	2010-04-29 10:00:00	GR 9D M-J	\N	\N
187	\N	2010-05-04 09:00:00	2010-05-04 10:00:00	GR 9D M-J	\N	\N
188	\N	2010-05-06 09:00:00	2010-05-06 10:00:00	GR 9D M-J	\N	\N
189	\N	2010-05-11 09:00:00	2010-05-11 10:00:00	GR 9D M-J	\N	\N
190	\N	2010-05-13 09:00:00	2010-05-13 10:00:00	GR 9D M-J	\N	\N
191	\N	2010-05-18 09:00:00	2010-05-18 10:00:00	GR 9D M-J	\N	\N
192	\N	2010-05-20 09:00:00	2010-05-20 10:00:00	GR 9D M-J	\N	\N
193	\N	2010-05-25 09:00:00	2010-05-25 10:00:00	GR 9D M-J	\N	\N
194	\N	2010-05-27 09:00:00	2010-05-27 10:00:00	GR 9D M-J	\N	\N
195	\N	2010-06-01 09:00:00	2010-06-01 10:00:00	GR 9D M-J	\N	\N
196	\N	2010-06-03 09:00:00	2010-06-03 10:00:00	GR 9D M-J	\N	\N
197	\N	2010-06-08 09:00:00	2010-06-08 10:00:00	GR 9D M-J	\N	\N
198	\N	2010-06-10 09:00:00	2010-06-10 10:00:00	GR 9D M-J	\N	\N
199	\N	2010-06-15 09:00:00	2010-06-15 10:00:00	GR 9D M-J	\N	\N
200	\N	2010-06-17 09:00:00	2010-06-17 10:00:00	GR 9D M-J	\N	\N
201	\N	2010-06-22 09:00:00	2010-06-22 10:00:00	GR 9D M-J	\N	\N
202	\N	2010-06-24 09:00:00	2010-06-24 10:00:00	GR 9D M-J	\N	\N
203	\N	2010-06-29 09:00:00	2010-06-29 10:00:00	GR 9D M-J	\N	\N
204	\N	2010-07-01 09:00:00	2010-07-01 10:00:00	GR 9D M-J	\N	\N
205	\N	2010-07-06 09:00:00	2010-07-06 10:00:00	GR 9D M-J	\N	\N
206	\N	2010-07-08 09:00:00	2010-07-08 10:00:00	GR 9D M-J	\N	\N
207	\N	2010-07-13 09:00:00	2010-07-13 10:00:00	GR 9D M-J	\N	\N
208	\N	2010-07-15 09:00:00	2010-07-15 10:00:00	GR 9D M-J	\N	\N
209	\N	2010-07-20 09:00:00	2010-07-20 10:00:00	GR 9D M-J	\N	\N
210	\N	2010-07-22 09:00:00	2010-07-22 10:00:00	GR 9D M-J	\N	\N
211	\N	2010-07-27 09:00:00	2010-07-27 10:00:00	GR 9D M-J	\N	\N
212	\N	2010-07-29 09:00:00	2010-07-29 10:00:00	GR 9D M-J	\N	\N
213	\N	2010-08-03 09:00:00	2010-08-03 10:00:00	GR 9D M-J	\N	\N
214	\N	2010-08-05 09:00:00	2010-08-05 10:00:00	GR 9D M-J	\N	\N
215	\N	2010-08-10 09:00:00	2010-08-10 10:00:00	GR 9D M-J	\N	\N
216	\N	2010-08-12 09:00:00	2010-08-12 10:00:00	GR 9D M-J	\N	\N
217	\N	2010-08-17 09:00:00	2010-08-17 10:00:00	GR 9D M-J	\N	\N
218	\N	2010-08-19 09:00:00	2010-08-19 10:00:00	GR 9D M-J	\N	\N
219	\N	2010-08-24 09:00:00	2010-08-24 10:00:00	GR 9D M-J	\N	\N
220	\N	2010-08-26 09:00:00	2010-08-26 10:00:00	GR 9D M-J	\N	\N
221	\N	2010-08-31 09:00:00	2010-08-31 10:00:00	GR 9D M-J	\N	\N
222	\N	2010-09-02 09:00:00	2010-09-02 10:00:00	GR 9D M-J	\N	\N
223	\N	2010-09-07 09:00:00	2010-09-07 10:00:00	GR 9D M-J	\N	\N
224	\N	2010-09-09 09:00:00	2010-09-09 10:00:00	GR 9D M-J	\N	\N
225	\N	2010-09-14 09:00:00	2010-09-14 10:00:00	GR 9D M-J	\N	\N
226	\N	2010-09-16 09:00:00	2010-09-16 10:00:00	GR 9D M-J	\N	\N
227	\N	2010-09-21 09:00:00	2010-09-21 10:00:00	GR 9D M-J	\N	\N
228	\N	2010-09-23 09:00:00	2010-09-23 10:00:00	GR 9D M-J	\N	\N
229	\N	2010-09-28 09:00:00	2010-09-28 10:00:00	GR 9D M-J	\N	\N
230	\N	2010-09-30 09:00:00	2010-09-30 10:00:00	GR 9D M-J	\N	\N
231	\N	2010-10-05 09:00:00	2010-10-05 10:00:00	GR 9D M-J	\N	\N
232	\N	2010-10-07 09:00:00	2010-10-07 10:00:00	GR 9D M-J	\N	\N
233	\N	2010-10-12 09:00:00	2010-10-12 10:00:00	GR 9D M-J	\N	\N
234	\N	2010-10-14 09:00:00	2010-10-14 10:00:00	GR 9D M-J	\N	\N
235	\N	2010-10-19 09:00:00	2010-10-19 10:00:00	GR 9D M-J	\N	\N
236	\N	2010-10-21 09:00:00	2010-10-21 10:00:00	GR 9D M-J	\N	\N
237	\N	2010-10-26 09:00:00	2010-10-26 10:00:00	GR 9D M-J	\N	\N
238	\N	2010-10-28 09:00:00	2010-10-28 10:00:00	GR 9D M-J	\N	\N
239	\N	2010-11-02 09:00:00	2010-11-02 10:00:00	GR 9D M-J	\N	\N
240	\N	2010-11-04 09:00:00	2010-11-04 10:00:00	GR 9D M-J	\N	\N
241	\N	2010-11-09 09:00:00	2010-11-09 10:00:00	GR 9D M-J	\N	\N
242	\N	2010-11-11 09:00:00	2010-11-11 10:00:00	GR 9D M-J	\N	\N
243	\N	2010-11-16 09:00:00	2010-11-16 10:00:00	GR 9D M-J	\N	\N
244	\N	2010-11-18 09:00:00	2010-11-18 10:00:00	GR 9D M-J	\N	\N
245	\N	2010-11-23 09:00:00	2010-11-23 10:00:00	GR 9D M-J	\N	\N
246	\N	2010-11-25 09:00:00	2010-11-25 10:00:00	GR 9D M-J	\N	\N
247	\N	2010-11-30 09:00:00	2010-11-30 10:00:00	GR 9D M-J	\N	\N
248	\N	2010-12-02 09:00:00	2010-12-02 10:00:00	GR 9D M-J	\N	\N
249	\N	2010-12-07 09:00:00	2010-12-07 10:00:00	GR 9D M-J	\N	\N
250	\N	2010-12-09 09:00:00	2010-12-09 10:00:00	GR 9D M-J	\N	\N
251	\N	2010-12-14 09:00:00	2010-12-14 10:00:00	GR 9D M-J	\N	\N
252	\N	2010-12-16 09:00:00	2010-12-16 10:00:00	GR 9D M-J	\N	\N
253	\N	2010-12-21 09:00:00	2010-12-21 10:00:00	GR 9D M-J	\N	\N
254	\N	2010-12-23 09:00:00	2010-12-23 10:00:00	GR 9D M-J	\N	\N
255	\N	2010-12-28 09:00:00	2010-12-28 10:00:00	GR 9D M-J	\N	\N
256	\N	2010-12-30 09:00:00	2010-12-30 10:00:00	GR 9D M-J	\N	\N
176	\N	2010-03-25 09:00:00	2010-03-25 10:00:00	GR 9D M-J	9	\N
92	\N	2010-03-24 10:00:00	2010-03-24 11:00:00	GR 10B L-X-V	6	\N
257	\N	2010-03-25 18:00:00	2010-03-25 19:00:00	Adriana López Sánchez	\N	\N
183	\N	2010-04-20 09:00:00	2010-04-20 10:00:00	GR 9D M-J	7	\N
\.



--
-- Data for Name: actividad_cliente; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY actividad_cliente (cliente_id, actividad_id) FROM stdin;
\.



--
-- Data for Name: maquina; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY maquina (id, nombre, fecha_compra, numserie) FROM stdin;
\.



--
-- Data for Name: actividad_maquina; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY actividad_maquina (actividad_id, maquina_id) FROM stdin;
\.



--
-- Data for Name: factura_compra; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY factura_compra (id, proveedor_id, fecha, numfactura, descuento, cargo, iva, bloqueada, visto_bueno_director, visto_bueno_comercial, visto_bueno_tecnico, fecha_entrada, fecha_visto_bueno_director, fecha_visto_bueno_comercial, fecha_visto_bueno_tecnico, visto_bueno_usuario, fecha_visto_bueno_usuario, observaciones, vencimientos_confirmados) FROM stdin;
3	1	2010-03-24	123	0	0.00	0.18	f	f	f	f	2010-03-24	\N	\N	\N	t	2010-03-24		f
\.



--
-- Data for Name: linea_de_compra; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY linea_de_compra (id, pedido_compra_id, albaran_entrada_id, factura_compra_id, producto_compra_id, cantidad, precio, descuento, entrega, iva) FROM stdin;
12	5	4	\N	5	2	500	0		0.18
13	5	4	\N	3	1	47	0		0.18
11	5	4	\N	4	30	200	0		0.18
14	\N	5	\N	3	15	8	0		0.18
\.



--
-- Data for Name: linea_de_pedido_de_compra; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY linea_de_pedido_de_compra (id, producto_compra_id, pedido_compra_id, fechahora, cantidad, precio, descuento, fecha_entrega, texto_entrega, notas) FROM stdin;
5	4	5	2010-03-10 18:08:34.083468	35	200	0.10000000000000001	2010-03-10	Embalar bien. Frágil.	
7	5	5	2010-03-10 18:14:04.463307	2	500	0	\N		
8	3	5	2010-03-10 18:14:08.811835	1	45	0	\N		
\.



--
-- Data for Name: linea_de_pedido_de_compra__linea_de_compra; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY linea_de_pedido_de_compra__linea_de_compra (linea_de_pedido_de_compra_id, linea_de_compra_id) FROM stdin;
\.



--
-- Data for Name: transporte_a_cuenta; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY transporte_a_cuenta (id, concepto, precio, observaciones, fecha, albaran_salida_id, proveedor_id) FROM stdin;
\.



--
-- Data for Name: servicio_tomado; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY servicio_tomado (id, factura_compra_id, concepto, cantidad, precio, descuento, transporte_a_cuenta_id, iva) FROM stdin;
1	3	linea de telefono	1	0	0	\N	0.18
\.



--
-- Data for Name: vencimiento_pago; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY vencimiento_pago (id, factura_compra_id, fecha, importe, observaciones) FROM stdin;
2	3	2010-03-24	0	Recibo domicilado, los días 0. 
\.



--
-- Data for Name: pagare_pago; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY pagare_pago (id, codigo, fecha_emision, fecha_pago, cantidad, pagado, observaciones, procesado, fecha_cobrado) FROM stdin;
2	123456	2010-02-15	2010-05-25	580	-1	\nPagado mediante pagaré La Caixa. Imprimido el 15 de febrero de 2010.	f	\N
1		2010-02-15	2010-02-15	0	-1		t	2010-02-15
\.



--
-- Data for Name: cuenta_destino; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY cuenta_destino (id, nombre, observaciones, banco, swif, iban, cuenta, nombre_banco, proveedor_id) FROM stdin;
\.



--
-- Data for Name: pago; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY pago (id, factura_compra_id, fecha, importe, observaciones, pagare_pago_id, proveedor_id, cuenta_origen_id, cuenta_destino_id, concepto_libre) FROM stdin;
\.



--
-- Data for Name: recibo; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY recibo (id, numrecibo, anno, lugar_libramiento, fecha_libramiento, fecha_vencimiento, persona_pago, domicilio_pago, cuenta_origen_id, nombre_librado, direccion_librado, observaciones, cuenta_bancaria_cliente_id) FROM stdin;
\.



--
-- Data for Name: vencimiento_cobro; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY vencimiento_cobro (id, factura_venta_id, prefactura_id, fecha, importe, observaciones, cuenta_origen_id, recibo_id) FROM stdin;
\.



--
-- Data for Name: pagare_cobro; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY pagare_cobro (id, codigo, fecha_recepcion, fecha_cobro, cantidad, cobrado, observaciones, fecha_cobrado, procesado) FROM stdin;
1	1234	2010-02-21	2010-02-21	145	145		2010-03-24	t
\.



--
-- Data for Name: confirming; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY confirming (id, codigo, fecha_recepcion, fecha_cobro, cantidad, cobrado, observaciones, fecha_cobrado, procesado) FROM stdin;
\.



--
-- Data for Name: cobro; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY cobro (id, factura_venta_id, prefactura_id, fecha, importe, observaciones, pagare_cobro_id, cliente_id, confirming_id) FROM stdin;
\.



--
-- Data for Name: modulo; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY modulo (id, nombre, icono, descripcion) FROM stdin;
2	Comercial	comercial.png	Comercial
3	Almacén	almacen.png	Gestión de almacén
5	General	func_generales.png	Funciones generales
7	Ayuda	doc_y_ayuda.png	Documentación y ayuda
6	Consultas	costes.png	Costes e informes
9	DEBUG	debug.png	Utilidades de depuración para el administrador
1	Administración	administracion.png	Administración
\.



--
-- Data for Name: ventana; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY ventana (id, modulo_id, descripcion, fichero, clase, icono) FROM stdin;
1	1	Facturas de compra	facturas_compra.py	FacturasDeEntrada	factura_compra.png
2	1	Facturas de venta	facturas_venta.py	FacturasVenta	factura_venta.png
4	2	Pedidos de compra (a proveedores)	pedidos_de_compra.py	PedidosDeCompra	pedido.png
6	2	Pedidos de venta (de clientes)	pedidos_de_venta.py	PedidosDeVenta	pedido.png
7	2	Ver ventas sin pedido asignado	lineas_sin_pedido.py	LineasDeVentaSinPedido	sin_pedido.png
11	3	Albaranes de entrada de material	albaranes_de_entrada.py	AlbaranesDeEntrada	albaran.png
12	3	Albaranes de salida	albaranes_de_salida.py	AlbaranesDeSalida	albaran.png
53	6	Consulta de albaranes de clientes	consulta_albaranes_clientes.py	ConsultaAlbaranesCliente	informe.png
54	6	Consulta de cobros	consulta_cobros.py	ConsultaCobros	informe.png
56	6	Consulta de pagos	consulta_pagos.py	ConsultaPagos	informe.png
27	5	Gestión de usuarios	usuarios.py	Usuarios	usuarios.png
29	5	Proveedores	proveedores.py	Proveedores	proveedores.png
30	5	Contadores para facturas de clientes	contadores.py	Contadores	contadores.png
89	6	Pedidos pendientes de servir	consulta_pendientes_servir.py	PendientesServir	informe.png
34	5	Empleados	empleados.py	Empleados	empleados.png
38	6	Existencias de materiales en almacén	consulta_existencias.py	ConsultaExistencias	informe.png
39	6	Listado de albaranes facturados	consulta_albaranesFacturados.py	ConsultaAlbaranesFacturados	informe.png
40	6	Ver productos bajo mínimos	consulta_bajoMinimos.py	ConsultaBajoMinimos	informe.png
41	6	Listado de albaranes pendientes de facturar	consulta_albaranesPorFacturar.py	ConsultaAlbaranesPorFacturar	informe.png
42	6	Listado de compras	consulta_compras.py	ConsultaCompras	informe.png
43	6	Listado de ventas	consulta_ventas.py	ConsultaVentas	informe.png
44	7	Acerca de...	acerca_de.py	acerca_de	acerca.png
90	6	Pedidos pendientes de recibir	consulta_pendientes_recibir.py	PendientesRecibir	informe.png
57	6	Consulta de pedidos de clientes	consulta_pedidos_clientes.py	ConsultaPedidosCliente	informe.png
5	2	Tarifas de precios	tarifas_de_precios.py	TarifasDePrecios	tarifa.png
59	6	Consulta de vencimientos de pago	consulta_vencimientos_pago.py	ConsultaVencimientosPagos	informe.png
33	5	Cartera de clientes	clientes.py	Clientes	clientes.png
61	5	Mis datos de usuario	ventana_usuario.py	Usuarios	usuarios.png
58	6	Consulta de vencimientos de cobro	consulta_vencimientos_cobro.py	ConsultaVencimientosCobros	informe.png
87	1	Cheques y pagarés de pago	pagares_pagos.py	PagaresPagos	money.png
69	1	Efectos de cobro	pagares_cobros.py	PagaresCobros	money.png
74	3	Valoración de entradas en almacén	consulta_entradas_almacen.py	ConsultaEntradasAlmacen	informe.png
72	5	Configuración de categorías laborales	categorias_laborales.py	CategoriasLaborales	catcent.png
36	5	Familias de productos	tipos_material.py	TiposMaterial	tipos_de.png
73	5	Configuración de centros de trabajo	centros_de_trabajo.py	CentrosDeTrabajo	catcent.png
80	\N	Formulación geotextiles	formulacion_geotextiles.py	FormulacionGeotextiles	formulacion.png
8	\N	Ver existencias de rollos en almacén	rollos_almacen.py	RollosAlmacen	rollos_en_almacen.png
22	\N	Asignar directamente resultados de laboratorio a lote de fibra. (No guarda histórico)	lab_resultados_lote.py	LabResultadosLote	
23	\N	Buscar lotes con valores determinados	busca_lote.py	BuscaLote	buscar.png
79	\N	Formulación fibra	formulacion_fibra.py	FormulacionFibra	formulacion.png
50	\N	Buscar partidas por características	busca_partida.py	BuscaPartida	buscar.png
99	\N	Resultados fibra de cemento	resultados_cemento.py	ResultadosFibra	labo_fibra.png
62	\N	Resultados fibra	resultados_fibra.py	ResultadosFibra	labo_fibra.png
63	\N	Resultados geotextiles	resultados_geotextiles.py	ResultadosGeotextiles	labo_rollos.png
26	\N	Tipos de material de fibra	tipos_material_balas.py	TiposMaterialBala	tipos_de.png
28	\N	Tipos de incidencia	tipos_incidencia.py	TiposIncidencia	tipos_de.png
31	\N	Catálogo de productos de venta (geocompuestos)	productos_de_venta_rollos_geocompuestos.py	ProductosDeVentaRollosGeocompuestos	catalogo.png
32	\N	Catálogo de productos de venta (fibra)	productos_de_venta_balas.py	ProductosDeVentaBalas	catalogo.png
37	\N	Catálogo de productos de venta (geotextiles)	productos_de_venta_rollos.py	ProductosDeVentaRollos	catalogo.png
76	\N	Imprimir existencias de geotextiles	consulta_existenciasRollos.py	ConsultaExistencias	informe.png
75	\N	Imprimir existencias de fibra	consulta_existenciasBalas.py	ConsultaExistencias	informe.png
88	9	Trazabilidad interna (DEBUG) - Sólo para el administrador	trazabilidad.py	Trazabilidad	trazabilidad.png
68	1	Vencimientos pendientes por cliente	vencimientos_pendientes_por_cliente.py	VencimientosPendientesPorCliente	pendiente.png
20	\N	01.- Resultados de resistencia a alargamiento longitudinal	resultados_longitudinal.py	ResultadosLongitudinal	labo_rollos.png
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
101	6	Facturación por cliente y fecha	facturacion_por_cliente_y_fechas.py	FacturacionPorClienteYFechas	informe.png
102	9	Visor del log	logviewer.py	LogViewer	trazabilidad.png
104	1	Cuentas bancarias de proveedores	cuentas_destino.py	CuentasDestino	money.png
103	1	Cuentas bancarias de la empresa	cuentas_origen.py	CuentasOrigen	money.png
105	1	Pago por transferencia	transferencias.py	Transferencias	dollars.png
106	1	Facturas de compra pendientes de aprobación	consulta_pendientes_vto_bueno.py	ConsultaPendientesVtoBueno	firma.png
108	2	Presupuestos a clientes	presupuestos.py	Presupuestos	presupuesto.png
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
228	5	Grupos	grupos_alumnos.py	GruposAlumnos	
66	\N	Trazabilidad de productos finales	trazabilidad_articulos.py	TrazabilidadArticulos	trazabilidad.png
95	\N	Estado de silos	silos.py	Silos	silos.png
96	\N	Histórico de existencias de productos de venta	historico_existencias.py	HistoricoExistencias	globe.png
81	\N	Configuración de grupos de trabajo	grupos.py	Grupos	catcent.png
85	\N	Configurar motivos de ausencia	motivos_ausencia.py	MotivosAusencia	motivos.png
107	\N	Productos de venta «especiales»	productos_de_venta_especial.py	ProductosDeVentaEspecial	catalogo.png
229	1	Imprimir ticket a partir de factura	up_consulta_facturas.py	UPConsultaFacturas	informe.png
\.



--
-- Data for Name: permiso; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) FROM stdin;
105	1	224	t	t	t	t
106	1	227	t	t	t	t
100	1	88	t	t	t	t
76	1	56	t	t	t	t
23	1	66	f	f	f	f
61	1	44	t	t	t	t
43	1	26	f	f	f	f
60	1	107	f	f	f	f
59	1	85	f	f	f	f
84	1	90	t	t	t	t
24	1	108	t	t	t	t
37	1	99	f	f	f	f
92	1	76	f	f	f	f
44	1	27	t	t	t	t
99	1	111	t	t	t	t
93	1	75	f	f	f	f
45	1	28	f	f	f	f
85	1	57	t	t	t	t
31	1	98	t	t	t	t
30	1	74	t	t	t	t
46	1	29	t	t	t	t
22	1	5	t	t	t	t
32	1	95	f	f	f	f
47	1	30	t	t	t	t
34	1	221	t	t	t	t
33	1	96	f	f	f	f
86	1	59	t	t	t	t
19	1	4	t	t	t	t
48	1	31	f	f	f	f
20	1	6	t	t	t	t
49	1	32	f	f	f	f
54	1	33	t	t	t	t
67	1	79	f	f	f	f
21	1	7	t	t	t	t
77	1	89	t	t	t	t
25	1	8	f	f	f	f
39	1	50	f	f	f	f
68	1	80	f	f	f	f
50	1	34	t	t	t	t
96	1	101	t	t	t	t
55	1	61	t	t	t	t
51	1	35	t	t	t	t
40	1	62	f	f	f	f
101	1	102	t	t	t	t
41	1	63	f	f	f	f
52	1	36	t	t	t	t
53	1	37	f	f	f	f
56	1	72	t	t	t	t
28	1	11	t	t	t	t
104	1	223	t	t	t	t
78	1	38	t	t	t	t
29	1	12	t	t	t	t
57	1	73	t	t	t	t
74	1	53	t	t	t	t
79	1	39	t	t	t	t
75	1	54	t	t	t	t
80	1	40	t	t	t	t
58	1	81	f	f	f	f
35	1	22	f	f	f	f
81	1	41	t	t	t	t
88	1	58	t	t	t	t
82	1	42	t	t	t	t
36	1	23	f	f	f	f
83	1	43	t	t	t	t
109	2	44	t	t	t	t
118	2	81	t	t	f	f
11	1	94	t	t	t	t
123	2	34	t	t	t	t
107	2	33	t	t	t	t
155	2	40	t	t	t	t
114	2	61	t	t	t	t
115	2	72	t	t	t	t
12	1	104	t	t	t	t
116	2	36	t	t	t	t
127	2	1	t	t	t	t
156	2	41	t	t	t	t
125	2	2	t	t	t	t
117	2	73	t	t	t	t
128	2	87	t	t	t	t
126	2	69	t	t	t	t
120	2	35	t	t	t	t
129	2	68	t	t	t	t
130	2	94	t	t	t	t
144	2	11	t	t	t	t
131	2	104	t	t	t	t
119	2	228	t	t	t	t
132	2	103	t	t	t	t
145	2	12	t	t	t	t
133	2	105	t	t	t	t
134	2	106	t	t	t	t
146	2	74	t	t	t	t
135	2	110	t	t	t	t
147	2	98	t	t	t	t
136	2	112	t	t	t	t
139	2	4	t	t	t	t
112	2	221	t	t	t	t
140	2	6	t	t	t	t
137	2	113	t	t	t	t
141	2	7	t	t	t	t
124	2	225	t	t	t	t
142	2	5	t	t	t	t
157	2	42	t	t	t	t
143	2	108	t	t	t	t
138	2	226	t	t	t	t
110	2	223	t	t	t	t
13	1	103	t	t	t	t
111	2	224	t	t	t	t
158	2	43	t	t	t	t
14	1	105	t	t	t	t
165	2	229	t	t	t	t
159	2	90	t	t	t	t
15	1	106	t	t	t	t
149	2	53	t	t	t	t
160	2	57	t	t	t	t
150	2	54	t	t	t	t
161	2	59	t	t	t	t
162	2	58	t	t	t	t
148	2	27	t	t	t	t
151	2	56	t	t	t	t
108	2	29	t	t	t	t
113	2	30	t	t	t	t
163	2	101	t	t	t	t
16	1	110	t	t	t	t
122	2	111	t	t	t	t
121	2	227	t	t	t	t
152	2	89	t	t	t	t
1	1	1	t	t	t	t
153	2	38	t	t	t	t
17	1	112	t	t	t	t
2	1	2	t	t	t	t
154	2	39	t	t	t	t
4	1	87	t	t	t	t
18	1	113	t	t	t	t
5	1	69	t	t	t	t
10	1	68	t	t	t	t
103	1	225	t	t	t	t
102	1	226	t	t	t	t
164	1	229	t	t	t	t
\.



--
-- Data for Name: alerta; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY alerta (id, usuario_id, mensaje, fechahora, entregado) FROM stdin;
\.



--
-- Data for Name: datos_de_la_empresa; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY datos_de_la_empresa (id, nombre, cif, dirfacturacion, cpfacturacion, ciudadfacturacion, provinciafacturacion, direccion, cp, ciudad, provincia, telefono, fax, email, paisfacturacion, pais, telefonofacturacion, faxfacturacion, nombre_responsable_compras, telefono_responsable_compras, nombre_contacto, registro_mercantil, email_responsable_compras, logo, logo2, bvqi, nomalbaran2, diralbaran2, cpalbaran2, ciualbaran2, proalbaran2, telalbaran2, faxalbaran2, regalbaran2, irpf, es_sociedad, logoiso1, logoiso2, recargo_equivalencia, iva, ped_compra_texto_fijo, ped_compra_texto_editable, ped_compra_texto_editable_con_nivel1) FROM stdin;
1	Universal Pilates, S. L.	B-92.554.682	Avda. El Rosario, 414	29604	Marbella	Málaga	Ctra. de Istán, km 0.9 - C. C. Le Village	29602	Marbella	Málaga	952902362		jlopez@universalpilates.es	España	España	952902362		Javier Bseiso Blanco	658318870	Adriana López		javier@universalpilates.es	logo_up.jpg		f								CIF T-00000000 Reg.Mec. de ...	0	t			f	0.18	Rogamos nos remitan copia de este pedido sellado y firmado por uds.	Esta mercancía debe entregarse en...	Pago a 90 días f. f.
\.



--
-- Data for Name: documento; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY documento (id, nombre, nombre_fichero, observaciones, pedido_venta_id, albaran_salida_id, factura_venta_id, prefactura_id, pagare_cobro_id, pedido_compra_id, albaran_entrada_id, factura_compra_id, pagare_pago_id, empleado_id, cliente_id, proveedor_id, confirming_id) FROM stdin;
\.



--
-- Data for Name: estadistica; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY estadistica (id, usuario_id, ventana_id, veces, ultima_vez) FROM stdin;
12	1	90	3	2010-02-21 16:42:04
3	1	102	1	2010-02-12 18:22:50
4	1	88	1	2010-02-12 18:23:06
27	1	89	2	2010-02-21 16:42:11
9	1	40	4	2010-02-21 16:47:26
39	1	44	3	2010-02-21 15:24:25
54	1	73	1	2010-02-21 16:47:39
42	1	6	1	2010-02-21 15:26:10
43	1	108	1	2010-02-21 15:26:15
32	1	104	1	2010-02-21 14:42:30
45	1	7	1	2010-02-21 15:53:36
16	1	1	4	2010-02-21 14:47:55
19	1	106	2	2010-02-21 14:48:01
35	1	94	1	2010-02-21 14:48:08
28	1	226	2	2010-02-21 14:48:53
21	1	112	2	2010-02-21 14:49:06
36	1	105	1	2010-02-21 14:49:14
37	1	113	1	2010-02-21 14:54:05
48	1	57	1	2010-02-21 15:56:31
31	1	103	3	2010-02-22 18:17:02
33	1	69	2	2010-02-22 18:24:49
50	1	59	2	2010-02-21 15:58:55
30	1	87	2	2010-02-22 18:25:04
53	1	72	3	2010-02-22 18:27:48
52	1	41	3	2010-02-22 18:37:18
18	1	43	5	2010-02-22 18:37:28
20	1	110	7	2010-02-26 16:20:48
14	1	111	3	2010-02-21 16:41:30
51	1	39	2	2010-02-21 16:41:38
22	1	68	4	2010-02-26 16:22:23
24	1	98	3	2010-02-26 16:22:35
10	1	29	3	2010-02-26 18:04:37
38	1	12	2	2010-02-26 18:09:29
1	1	221	16	2010-03-10 18:58:37
5	1	36	4	2010-03-10 17:51:30
55	1	30	3	2010-03-10 19:00:11
44	1	5	3	2010-03-10 17:54:54
26	1	42	7	2010-03-10 17:57:30
8	1	4	6	2010-03-10 18:05:54
11	1	11	4	2010-03-10 18:17:32
23	1	74	5	2010-03-10 18:21:29
25	1	38	6	2010-03-10 18:22:13
34	1	225	3	2010-03-10 18:48:27
13	1	2	5	2010-03-10 18:56:58
77	2	106	1	2010-03-24 13:37:56
92	2	27	2	2010-03-25 13:07:44
79	2	94	1	2010-03-24 13:39:07
41	1	223	7	2010-03-23 13:20:06
6	1	35	14	2010-03-23 19:19:27
96	2	61	1	2010-03-25 13:08:13
81	2	110	1	2010-03-24 13:39:47
91	2	228	2	2010-03-25 13:08:26
82	2	226	1	2010-03-24 13:41:42
46	1	53	3	2010-04-20 16:59:38
80	2	112	2	2010-03-24 13:41:52
17	1	56	3	2010-04-20 16:59:46
62	2	36	2	2010-03-24 17:35:23
83	2	105	1	2010-03-24 13:42:28
84	2	113	1	2010-03-24 13:42:36
47	1	54	4	2010-04-20 16:59:51
85	2	68	1	2010-03-24 13:43:11
56	1	227	9	2010-04-20 13:14:55
69	2	53	1	2010-03-24 13:11:08
86	2	11	1	2010-03-24 13:51:46
70	2	54	1	2010-03-24 13:11:38
93	2	72	1	2010-03-24 17:36:44
59	1	34	4	2010-03-23 19:10:39
87	2	98	1	2010-03-24 13:55:38
60	2	224	47	2010-04-20 17:28:07
71	2	56	1	2010-03-24 13:12:10
72	2	58	1	2010-03-24 13:12:35
94	2	73	1	2010-03-24 17:38:10
88	2	221	6	2010-04-20 17:35:17
58	2	29	5	2010-03-24 13:15:54
95	2	30	1	2010-03-24 17:38:28
89	2	74	1	2010-03-24 14:02:21
61	2	34	3	2010-03-24 17:38:51
73	2	1	3	2010-03-24 13:31:23
78	2	2	2	2010-04-20 14:07:39
90	2	5	1	2010-03-24 17:24:57
97	2	229	5	2010-04-20 17:40:09
74	2	87	2	2010-03-24 13:34:48
75	2	103	1	2010-03-24 13:35:05
66	2	225	4	2010-04-20 17:40:39
49	1	58	3	2010-04-20 15:36:30
76	2	104	2	2010-03-24 13:35:37
15	1	101	4	2010-04-20 15:36:47
65	2	69	2	2010-03-24 13:37:25
64	2	227	17	2010-04-20 17:43:26
7	1	33	16	2010-04-20 17:48:55
67	2	111	3	2010-03-24 18:45:50
2	1	27	21	2010-04-20 16:22:50
68	2	223	7	2010-03-24 18:51:49
40	1	224	10	2010-04-20 16:26:43
57	2	33	24	2010-03-24 18:52:07
63	2	35	16	2010-03-24 19:18:41
\.



--
-- Data for Name: lista_objetos_recientes; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY lista_objetos_recientes (id, usuario_id, ventana_id) FROM stdin;
1	1	1
2	\N	6
3	2	1
\.



--
-- Data for Name: id_reciente; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY id_reciente (id, lista_objetos_recientes_id, objeto_id) FROM stdin;
1	1	2
2	2	1
3	3	3
\.



--
-- Data for Name: nota; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY nota (id, factura_venta_id, fechahora, texto, observaciones) FROM stdin;
\.



--
-- Data for Name: categoria; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY categoria (id, nombre, color_r, color_g, color_b) FROM stdin;
1	Prospect	255	255	255
2	Citas	255	255	255
3	Varios	255	255	255
\.



--
-- Data for Name: cliente_grupo_alumnos; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY cliente_grupo_alumnos (cliente_id, grupo_alumnos_id) FROM stdin;
\.



--
-- Data for Name: asistencia; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY asistencia (id, cliente_id, actividad_id, fechahora, observaciones) FROM stdin;
\.



--
-- Data for Name: tarea; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY tarea (id, categoria_id, resumen, texto, fecha_limite, fecha_done, fechahora) FROM stdin;
4	\N	Enviar mailing	Enviar un mailing a todos los clientes.	\N	\N	2010-02-22 17:50:12.161319
5	\N	Tarea 2	Tal y pam.	\N	\N	2010-02-22 17:51:22.928381
6	\N	q adri se ponga las pilas con el programa		\N	2010-03-23	2010-03-23 13:54:26.329187
3	\N	Llamada de teléfono	Llamar por teléfono a José Rodríguez.\nConfirmar reunión.	\N	2010-03-23	2010-02-22 17:50:12.161319
7	2	llamar a pepe		\N	\N	2010-03-24 12:52:27.386227
8	3	lalala	\n\n	\N	\N	2010-03-24 18:49:26.033818
\.



--
-- Data for Name: memo; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY memo (id, categoria_id, resumen, texto, fechahora) FROM stdin;
4	\N	Pedir DNI	Pedir DNI a nuevo alumno José Pérez para poderle enviar las facturas.\nVolverá por el gimnasio el martes que viene.	2010-02-22 17:50:02.513606
5	\N	Bla bla bla	Bla bla bla bla bleh.	2010-02-22 17:50:47.45323
6	\N	julio, vino a ver el centro		2010-03-23 14:06:35.617458
7	\N	tatata		2010-03-24 12:49:02.902594
8	1	julio marion		2010-03-24 12:50:48.252137
9	2	maria 		2010-03-24 12:51:03.44302
10	\N	ADRI ES LA MAS WAPA!		2010-03-24 19:32:41.671077
\.



--
-- Data for Name: padecimiento; Type: TABLE DATA; Schema: public; Owner: pilates
--

COPY padecimiento (id, cliente_id, fecha, texto) FROM stdin;
\.



-- PostgreSQL database dump complete
--


