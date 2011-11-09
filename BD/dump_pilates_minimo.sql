--
-- Data for Name: almacen; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO almacen VALUES (1, 'Almacén principal de Vitality Studio', '', '', 'Marbella', '', '', '', '', '', 'España', 1);

--
-- Data for Name: contador; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO contador VALUES (1, '', '', 1);

--
-- Data for Name: tarifa; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO tarifa VALUES (1, 'Tarifa venta', 'Tarifa estándar de venta.', NULL, NULL);


--
-- Data for Name: usuario; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO usuario VALUES (1, 'admin', 'cee9be15784861e244ca2e58268343c8', 'Administrador', 'frbogado@vm-webhosting', 'gusa25', 0, 'frbogado@novaweb.es', 'smtp.gea21.es', 'fbogado', '', 1, 1, 1, 1, 1, 'Administrador de la aplicación.');
INSERT INTO usuario VALUES (2, 'test', '098f6bcd4621d373cade4e832627b4f6', 'Usuario de prueba', '', '', 0, '', '', '', '', 1, 1, 1, 1, 1, '');


--
-- Data for Name: datos_de_la_empresa; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO datos_de_la_empresa VALUES (1, 'Nombre de la empresa', 'A-00.000.000', 'Dirección', '00000', 'Ciudad', 'Provincia', 'Dirección', '00000', 'Ciudad', 'Provincia', '000000000', '', 'info@novaweb.es', 'España', 'España', '000000000', '', '', '', '', '', '', 'logo_up.jpg', '', 0, '', '', '', '', '', '', '', '', 0, 1, '', '', 0, 0.18, '', '', 'Pago a 90 días f. f.');


--
-- Data for Name: modulo; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO modulo VALUES (2, 'Comercial', 'comercial.png', 'Comercial');
INSERT INTO modulo VALUES (3, 'Almacén', 'almacen.png', 'Gestión de almacén');
INSERT INTO modulo VALUES (5, 'General', 'func_generales.png', 'Funciones generales');
INSERT INTO modulo VALUES (7, 'Ayuda', 'doc_y_ayuda.png', 'Documentación y ayuda');
INSERT INTO modulo VALUES (6, 'Consultas', 'costes.png', 'Costes e informes');
INSERT INTO modulo VALUES (9, 'DEBUG', 'debug.png', 'Utilidades de depuración para el administrador');
INSERT INTO modulo VALUES (1, 'Administración', 'administracion.png', 'Administración');


--
-- Data for Name: ventana; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO ventana VALUES (1, 1, 'Facturas de compra', 'facturas_compra.py', 'FacturasDeEntrada', 'factura_compra.png');
INSERT INTO ventana VALUES (2, 1, 'Facturas de venta', 'facturas_venta.py', 'FacturasVenta', 'factura_venta.png');
INSERT INTO ventana VALUES (4, 2, 'Pedidos de compra (a proveedores)', 'pedidos_de_compra.py', 'PedidosDeCompra', 'pedido.png');
INSERT INTO ventana VALUES (6, 2, 'Pedidos de venta (de clientes)', 'pedidos_de_venta.py', 'PedidosDeVenta', 'pedido.png');
INSERT INTO ventana VALUES (7, 2, 'Ver ventas sin pedido asignado', 'lineas_sin_pedido.py', 'LineasDeVentaSinPedido', 'sin_pedido.png');
INSERT INTO ventana VALUES (11, 3, 'Albaranes de entrada de material', 'albaranes_de_entrada.py', 'AlbaranesDeEntrada', 'albaran.png');
INSERT INTO ventana VALUES (12, 3, 'Albaranes de salida', 'albaranes_de_salida.py', 'AlbaranesDeSalida', 'albaran.png');
INSERT INTO ventana VALUES (53, 6, 'Consulta de albaranes de clientes', 'consulta_albaranes_clientes.py', 'ConsultaAlbaranesCliente', 'informe.png');
INSERT INTO ventana VALUES (54, 6, 'Consulta de cobros', 'consulta_cobros.py', 'ConsultaCobros', 'informe.png');
INSERT INTO ventana VALUES (56, 6, 'Consulta de pagos', 'consulta_pagos.py', 'ConsultaPagos', 'informe.png');
INSERT INTO ventana VALUES (27, 5, 'Gestión de usuarios', 'usuarios.py', 'Usuarios', 'usuarios.png');
INSERT INTO ventana VALUES (29, 5, 'Proveedores', 'proveedores.py', 'Proveedores', 'proveedores.png');
INSERT INTO ventana VALUES (30, 5, 'Contadores para facturas de clientes', 'contadores.py', 'Contadores', 'contadores.png');
INSERT INTO ventana VALUES (89, 6, 'Pedidos pendientes de servir', 'consulta_pendientes_servir.py', 'PendientesServir', 'informe.png');
INSERT INTO ventana VALUES (34, 5, 'Empleados', 'empleados.py', 'Empleados', 'empleados.png');
INSERT INTO ventana VALUES (38, 6, 'Existencias de materiales en almacén', 'consulta_existencias.py', 'ConsultaExistencias', 'informe.png');
INSERT INTO ventana VALUES (39, 6, 'Listado de albaranes facturados', 'consulta_albaranesFacturados.py', 'ConsultaAlbaranesFacturados', 'informe.png');
INSERT INTO ventana VALUES (40, 6, 'Ver productos bajo mínimos', 'consulta_bajoMinimos.py', 'ConsultaBajoMinimos', 'informe.png');
INSERT INTO ventana VALUES (41, 6, 'Listado de albaranes pendientes de facturar', 'consulta_albaranesPorFacturar.py', 'ConsultaAlbaranesPorFacturar', 'informe.png');
INSERT INTO ventana VALUES (42, 6, 'Listado de compras', 'consulta_compras.py', 'ConsultaCompras', 'informe.png');
INSERT INTO ventana VALUES (43, 6, 'Listado de ventas', 'consulta_ventas.py', 'ConsultaVentas', 'informe.png');
INSERT INTO ventana VALUES (44, 7, 'Acerca de...', 'acerca_de.py', 'acerca_de', 'acerca.png');
INSERT INTO ventana VALUES (90, 6, 'Pedidos pendientes de recibir', 'consulta_pendientes_recibir.py', 'PendientesRecibir', 'informe.png');
INSERT INTO ventana VALUES (57, 6, 'Consulta de pedidos de clientes', 'consulta_pedidos_clientes.py', 'ConsultaPedidosCliente', 'informe.png');
INSERT INTO ventana VALUES (5, 2, 'Tarifas de precios', 'tarifas_de_precios.py', 'TarifasDePrecios', 'tarifa.png');
INSERT INTO ventana VALUES (59, 6, 'Consulta de vencimientos de pago', 'consulta_vencimientos_pago.py', 'ConsultaVencimientosPagos', 'informe.png');
INSERT INTO ventana VALUES (33, 5, 'Cartera de clientes', 'clientes.py', 'Clientes', 'clientes.png');
INSERT INTO ventana VALUES (61, 5, 'Mis datos de usuario', 'ventana_usuario.py', 'Usuarios', 'usuarios.png');
INSERT INTO ventana VALUES (58, 6, 'Consulta de vencimientos de cobro', 'consulta_vencimientos_cobro.py', 'ConsultaVencimientosCobros', 'informe.png');
INSERT INTO ventana VALUES (87, 1, 'Cheques y pagarés de pago', 'pagares_pagos.py', 'PagaresPagos', 'money.png');
INSERT INTO ventana VALUES (69, 1, 'Efectos de cobro', 'pagares_cobros.py', 'PagaresCobros', 'money.png');
INSERT INTO ventana VALUES (74, 3, 'Valoración de entradas en almacén', 'consulta_entradas_almacen.py', 'ConsultaEntradasAlmacen', 'informe.png');
INSERT INTO ventana VALUES (72, 5, 'Configuración de categorías laborales', 'categorias_laborales.py', 'CategoriasLaborales', 'catcent.png');
INSERT INTO ventana VALUES (36, 5, 'Familias de productos', 'tipos_material.py', 'TiposMaterial', 'tipos_de.png');
INSERT INTO ventana VALUES (73, 5, 'Configuración de centros de trabajo', 'centros_de_trabajo.py', 'CentrosDeTrabajo', 'catcent.png');
INSERT INTO ventana VALUES (80, NULL, 'Formulación geotextiles', 'formulacion_geotextiles.py', 'FormulacionGeotextiles', 'formulacion.png');
INSERT INTO ventana VALUES (8, NULL, 'Ver existencias de rollos en almacén', 'rollos_almacen.py', 'RollosAlmacen', 'rollos_en_almacen.png');
INSERT INTO ventana VALUES (22, NULL, 'Asignar directamente resultados de laboratorio a lote de fibra. (No guarda histórico)', 'lab_resultados_lote.py', 'LabResultadosLote', '');
INSERT INTO ventana VALUES (23, NULL, 'Buscar lotes con valores determinados', 'busca_lote.py', 'BuscaLote', 'buscar.png');
INSERT INTO ventana VALUES (79, NULL, 'Formulación fibra', 'formulacion_fibra.py', 'FormulacionFibra', 'formulacion.png');
INSERT INTO ventana VALUES (50, NULL, 'Buscar partidas por características', 'busca_partida.py', 'BuscaPartida', 'buscar.png');
INSERT INTO ventana VALUES (99, NULL, 'Resultados fibra de cemento', 'resultados_cemento.py', 'ResultadosFibra', 'labo_fibra.png');
INSERT INTO ventana VALUES (62, NULL, 'Resultados fibra', 'resultados_fibra.py', 'ResultadosFibra', 'labo_fibra.png');
INSERT INTO ventana VALUES (63, NULL, 'Resultados geotextiles', 'resultados_geotextiles.py', 'ResultadosGeotextiles', 'labo_rollos.png');
INSERT INTO ventana VALUES (26, NULL, 'Tipos de material de fibra', 'tipos_material_balas.py', 'TiposMaterialBala', 'tipos_de.png');
INSERT INTO ventana VALUES (28, NULL, 'Tipos de incidencia', 'tipos_incidencia.py', 'TiposIncidencia', 'tipos_de.png');
INSERT INTO ventana VALUES (31, NULL, 'Catálogo de productos de venta (geocompuestos)', 'productos_de_venta_rollos_geocompuestos.py', 'ProductosDeVentaRollosGeocompuestos', 'catalogo.png');
INSERT INTO ventana VALUES (32, NULL, 'Catálogo de productos de venta (fibra)', 'productos_de_venta_balas.py', 'ProductosDeVentaBalas', 'catalogo.png');
INSERT INTO ventana VALUES (37, NULL, 'Catálogo de productos de venta (geotextiles)', 'productos_de_venta_rollos.py', 'ProductosDeVentaRollos', 'catalogo.png');
INSERT INTO ventana VALUES (76, NULL, 'Imprimir existencias de geotextiles', 'consulta_existenciasRollos.py', 'ConsultaExistencias', 'informe.png');
INSERT INTO ventana VALUES (75, NULL, 'Imprimir existencias de fibra', 'consulta_existenciasBalas.py', 'ConsultaExistencias', 'informe.png');
INSERT INTO ventana VALUES (88, 9, 'Trazabilidad interna (DEBUG) - Sólo para el administrador', 'trazabilidad.py', 'Trazabilidad', 'trazabilidad.png');
INSERT INTO ventana VALUES (68, 1, 'Vencimientos pendientes por cliente', 'vencimientos_pendientes_por_cliente.py', 'VencimientosPendientesPorCliente', 'pendiente.png');
INSERT INTO ventana VALUES (20, NULL, '01.- Resultados de resistencia a alargamiento longitudinal', 'resultados_longitudinal.py', 'ResultadosLongitudinal', 'labo_rollos.png');
INSERT INTO ventana VALUES (13, NULL, '04.- Resultados de perforación (cono)', 'resultados_perforacion.py', 'ResultadosPerforacion', 'labo_rollos.png');
INSERT INTO ventana VALUES (18, NULL, '06.- Resultados de permeabilidad', 'resultados_permeabilidad.py', 'ResultadosPermeabilidad', 'labo_rollos.png');
INSERT INTO ventana VALUES (51, NULL, '07.- Resultados de apertura de poros', 'resultados_poros.py', 'ResultadosPoros', 'labo_rollos.png');
INSERT INTO ventana VALUES (14, NULL, '02.- Resultados de resistencia a alargamiento transversal', 'resultados_transversal.py', 'ResultadosTransversal', 'labo_rollos.png');
INSERT INTO ventana VALUES (52, NULL, '05.- Resultados de espesor', 'resultados_espesor.py', 'ResultadosEspesor', 'labo_rollos.png');
INSERT INTO ventana VALUES (21, NULL, '03.- Resultados de compresión (CBR)', 'resultados_compresion.py', 'ResultadosCompresion', 'labo_rollos.png');
INSERT INTO ventana VALUES (17, NULL, '09.- Resultados de tenacidad sobre fibra', 'resultados_tenacidad.py', 'ResultadosTenacidad', 'labo_fibra.png');
INSERT INTO ventana VALUES (15, NULL, '10.- Resultados de elongación sobre fibra', 'resultados_elongacion.py', 'ResultadosElongacion', 'labo_fibra.png');
INSERT INTO ventana VALUES (25, NULL, '11.- Resultados encogimiento sobre fibra', 'resultados_encogimiento.py', 'ResultadosEncogimiento', 'labo_fibra.png');
INSERT INTO ventana VALUES (19, NULL, '12.- Resultados de grasa sobre fibra', 'resultados_grasa.py', 'ResultadosGrasa', 'labo_fibra.png');
INSERT INTO ventana VALUES (24, NULL, '13.- Resultados de rizo sobre fibra', 'resultados_rizo.py', 'ResultadosRizo', 'labo_fibra.png');
INSERT INTO ventana VALUES (60, NULL, '08.- Resultados de título (DTEX)', 'resultados_titulo.py', 'ResultadosTitulo', 'labo_fibra.png');
INSERT INTO ventana VALUES (94, 1, 'Facturas pendientes de revisar e imprimir', 'facturas_no_bloqueadas.py', 'FacturasNoBloqueadas', 'facturas_no_bloqueadas.png');
INSERT INTO ventana VALUES (98, 3, 'Historial de productos de compra', 'historico_existencias_compra.py', 'HistoricoExistenciasCompra', 'globe.png');
INSERT INTO ventana VALUES (101, 6, 'Facturación por cliente y fecha', 'facturacion_por_cliente_y_fechas.py', 'FacturacionPorClienteYFechas', 'informe.png');
INSERT INTO ventana VALUES (102, 9, 'Visor del log', 'logviewer.py', 'LogViewer', 'trazabilidad.png');
INSERT INTO ventana VALUES (104, 1, 'Cuentas bancarias de proveedores', 'cuentas_destino.py', 'CuentasDestino', 'money.png');
INSERT INTO ventana VALUES (103, 1, 'Cuentas bancarias de la empresa', 'cuentas_origen.py', 'CuentasOrigen', 'money.png');
INSERT INTO ventana VALUES (105, 1, 'Pago por transferencia', 'transferencias.py', 'Transferencias', 'dollars.png');
INSERT INTO ventana VALUES (106, 1, 'Facturas de compra pendientes de aprobación', 'consulta_pendientes_vto_bueno.py', 'ConsultaPendientesVtoBueno', 'firma.png');
INSERT INTO ventana VALUES (108, 2, 'Presupuestos a clientes', 'presupuestos.py', 'Presupuestos', 'presupuesto.png');
INSERT INTO ventana VALUES (111, 6, 'Facturado y beneficio', 'consulta_beneficio.py', 'ConsultaBeneficio', 'informe.png');
INSERT INTO ventana VALUES (110, 1, 'IVA devengado y soportado', 'iva.py', 'IVA', 'aeat.png');
INSERT INTO ventana VALUES (112, 1, 'Listado datos modelo 347', 'modelo_347.py', 'Modelo347', 'aeat.png');
INSERT INTO ventana VALUES (113, 1, 'Recibos bancarios', 'recibos.py', 'Recibos', 'money.png');
INSERT INTO ventana VALUES (221, 3, 'Terminal Punto de Venta', 'tpv.py', 'TPV', 'tpv.png');
INSERT INTO ventana VALUES (223, 2, 'Lista de asistencia', 'up_asistencia.py', 'Asistencias', '');
INSERT INTO ventana VALUES (224, 2, 'Agenda', 'up_calendario.py', 'Calendario', '');
INSERT INTO ventana VALUES (225, 1, 'Facturación por lotes', 'up_facturar.py', 'FacturacionAuto', '');
INSERT INTO ventana VALUES (226, 1, 'Libro de facturas', 'consulta_libro_iva.py', 'ConsultaLibroIVA', 'aeat.png');
INSERT INTO ventana VALUES (35, 5, 'Productos', 'productos_compra.py', 'ProductosCompra', 'catalogo.png');
INSERT INTO ventana VALUES (227, 6, 'Informe diario', 'up_report_diario.py', 'ReportDiario', 'pdfmail.png');
INSERT INTO ventana VALUES (228, 5, 'Grupos', 'grupos_alumnos.py', 'GruposAlumnos', '');
INSERT INTO ventana VALUES (66, NULL, 'Trazabilidad de productos finales', 'trazabilidad_articulos.py', 'TrazabilidadArticulos', 'trazabilidad.png');
INSERT INTO ventana VALUES (95, NULL, 'Estado de silos', 'silos.py', 'Silos', 'silos.png');
INSERT INTO ventana VALUES (96, NULL, 'Histórico de existencias de productos de venta', 'historico_existencias.py', 'HistoricoExistencias', 'globe.png');
INSERT INTO ventana VALUES (81, NULL, 'Configuración de grupos de trabajo', 'grupos.py', 'Grupos', 'catcent.png');
INSERT INTO ventana VALUES (85, NULL, 'Configurar motivos de ausencia', 'motivos_ausencia.py', 'MotivosAusencia', 'motivos.png');
INSERT INTO ventana VALUES (107, NULL, 'Productos de venta «especiales»', 'productos_de_venta_especial.py', 'ProductosDeVentaEspecial', 'catalogo.png');
INSERT INTO ventana VALUES (229, 1, 'Imprimir ticket a partir de factura', 'up_consulta_facturas.py', 'UPConsultaFacturas', 'informe.png');

--
-- Data for Name: permiso; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO permiso VALUES (105, 1, 224, 1, 1, 1, 1);
INSERT INTO permiso VALUES (106, 1, 227, 1, 1, 1, 1);
INSERT INTO permiso VALUES (100, 1, 88, 1, 1, 1, 1);
INSERT INTO permiso VALUES (76, 1, 56, 1, 1, 1, 1);
INSERT INTO permiso VALUES (23, 1, 66, 0, 0, 0, 0);
INSERT INTO permiso VALUES (61, 1, 44, 1, 1, 1, 1);
INSERT INTO permiso VALUES (43, 1, 26, 0, 0, 0, 0);
INSERT INTO permiso VALUES (60, 1, 107, 0, 0, 0, 0);
INSERT INTO permiso VALUES (59, 1, 85, 0, 0, 0, 0);
INSERT INTO permiso VALUES (84, 1, 90, 1, 1, 1, 1);
INSERT INTO permiso VALUES (24, 1, 108, 1, 1, 1, 1);
INSERT INTO permiso VALUES (37, 1, 99, 0, 0, 0, 0);
INSERT INTO permiso VALUES (92, 1, 76, 0, 0, 0, 0);
INSERT INTO permiso VALUES (44, 1, 27, 1, 1, 1, 1);
INSERT INTO permiso VALUES (99, 1, 111, 1, 1, 1, 1);
INSERT INTO permiso VALUES (93, 1, 75, 0, 0, 0, 0);
INSERT INTO permiso VALUES (45, 1, 28, 0, 0, 0, 0);
INSERT INTO permiso VALUES (85, 1, 57, 1, 1, 1, 1);
INSERT INTO permiso VALUES (31, 1, 98, 1, 1, 1, 1);
INSERT INTO permiso VALUES (30, 1, 74, 1, 1, 1, 1);
INSERT INTO permiso VALUES (46, 1, 29, 1, 1, 1, 1);
INSERT INTO permiso VALUES (22, 1, 5, 1, 1, 1, 1);
INSERT INTO permiso VALUES (32, 1, 95, 0, 0, 0, 0);
INSERT INTO permiso VALUES (47, 1, 30, 1, 1, 1, 1);
INSERT INTO permiso VALUES (34, 1, 221, 1, 1, 1, 1);
INSERT INTO permiso VALUES (33, 1, 96, 0, 0, 0, 0);
INSERT INTO permiso VALUES (86, 1, 59, 1, 1, 1, 1);
INSERT INTO permiso VALUES (19, 1, 4, 1, 1, 1, 1);
INSERT INTO permiso VALUES (48, 1, 31, 0, 0, 0, 0);
INSERT INTO permiso VALUES (20, 1, 6, 1, 1, 1, 1);
INSERT INTO permiso VALUES (49, 1, 32, 0, 0, 0, 0);
INSERT INTO permiso VALUES (54, 1, 33, 1, 1, 1, 1);
INSERT INTO permiso VALUES (67, 1, 79, 0, 0, 0, 0);
INSERT INTO permiso VALUES (21, 1, 7, 1, 1, 1, 1);
INSERT INTO permiso VALUES (77, 1, 89, 1, 1, 1, 1);
INSERT INTO permiso VALUES (25, 1, 8, 0, 0, 0, 0);
INSERT INTO permiso VALUES (39, 1, 50, 0, 0, 0, 0);
INSERT INTO permiso VALUES (68, 1, 80, 0, 0, 0, 0);
INSERT INTO permiso VALUES (50, 1, 34, 1, 1, 1, 1);
INSERT INTO permiso VALUES (96, 1, 101, 1, 1, 1, 1);
INSERT INTO permiso VALUES (55, 1, 61, 1, 1, 1, 1);
INSERT INTO permiso VALUES (51, 1, 35, 1, 1, 1, 1);
INSERT INTO permiso VALUES (40, 1, 62, 0, 0, 0, 0);
INSERT INTO permiso VALUES (101, 1, 102, 1, 1, 1, 1);
INSERT INTO permiso VALUES (41, 1, 63, 0, 0, 0, 0);
INSERT INTO permiso VALUES (52, 1, 36, 1, 1, 1, 1);
INSERT INTO permiso VALUES (53, 1, 37, 0, 0, 0, 0);
INSERT INTO permiso VALUES (56, 1, 72, 1, 1, 1, 1);
INSERT INTO permiso VALUES (28, 1, 11, 1, 1, 1, 1);
INSERT INTO permiso VALUES (104, 1, 223, 1, 1, 1, 1);
INSERT INTO permiso VALUES (78, 1, 38, 1, 1, 1, 1);
INSERT INTO permiso VALUES (29, 1, 12, 1, 1, 1, 1);
INSERT INTO permiso VALUES (57, 1, 73, 1, 1, 1, 1);
INSERT INTO permiso VALUES (74, 1, 53, 1, 1, 1, 1);
INSERT INTO permiso VALUES (79, 1, 39, 1, 1, 1, 1);
INSERT INTO permiso VALUES (75, 1, 54, 1, 1, 1, 1);
INSERT INTO permiso VALUES (80, 1, 40, 1, 1, 1, 1);
INSERT INTO permiso VALUES (58, 1, 81, 0, 0, 0, 0);
INSERT INTO permiso VALUES (35, 1, 22, 0, 0, 0, 0);
INSERT INTO permiso VALUES (81, 1, 41, 1, 1, 1, 1);
INSERT INTO permiso VALUES (88, 1, 58, 1, 1, 1, 1);
INSERT INTO permiso VALUES (82, 1, 42, 1, 1, 1, 1);
INSERT INTO permiso VALUES (36, 1, 23, 0, 0, 0, 0);
INSERT INTO permiso VALUES (83, 1, 43, 1, 1, 1, 1);
INSERT INTO permiso VALUES (109, 2, 44, 1, 1, 1, 1);
INSERT INTO permiso VALUES (118, 2, 81, 1, 1, 0, 0);
INSERT INTO permiso VALUES (11, 1, 94, 1, 1, 1, 1);
INSERT INTO permiso VALUES (123, 2, 34, 1, 1, 1, 1);
INSERT INTO permiso VALUES (107, 2, 33, 1, 1, 1, 1);
INSERT INTO permiso VALUES (155, 2, 40, 1, 1, 1, 1);
INSERT INTO permiso VALUES (114, 2, 61, 1, 1, 1, 1);
INSERT INTO permiso VALUES (115, 2, 72, 1, 1, 1, 1);
INSERT INTO permiso VALUES (12, 1, 104, 1, 1, 1, 1);
INSERT INTO permiso VALUES (116, 2, 36, 1, 1, 1, 1);
INSERT INTO permiso VALUES (127, 2, 1, 1, 1, 1, 1);
INSERT INTO permiso VALUES (156, 2, 41, 1, 1, 1, 1);
INSERT INTO permiso VALUES (125, 2, 2, 1, 1, 1, 1);
INSERT INTO permiso VALUES (117, 2, 73, 1, 1, 1, 1);
INSERT INTO permiso VALUES (128, 2, 87, 1, 1, 1, 1);
INSERT INTO permiso VALUES (126, 2, 69, 1, 1, 1, 1);
INSERT INTO permiso VALUES (120, 2, 35, 1, 1, 1, 1);
INSERT INTO permiso VALUES (129, 2, 68, 1, 1, 1, 1);
INSERT INTO permiso VALUES (130, 2, 94, 1, 1, 1, 1);
INSERT INTO permiso VALUES (144, 2, 11, 1, 1, 1, 1);
INSERT INTO permiso VALUES (131, 2, 104, 1, 1, 1, 1);
INSERT INTO permiso VALUES (119, 2, 228, 1, 1, 1, 1);
INSERT INTO permiso VALUES (132, 2, 103, 1, 1, 1, 1);
INSERT INTO permiso VALUES (145, 2, 12, 1, 1, 1, 1);
INSERT INTO permiso VALUES (133, 2, 105, 1, 1, 1, 1);
INSERT INTO permiso VALUES (134, 2, 106, 1, 1, 1, 1);
INSERT INTO permiso VALUES (146, 2, 74, 1, 1, 1, 1);
INSERT INTO permiso VALUES (135, 2, 110, 1, 1, 1, 1);
INSERT INTO permiso VALUES (147, 2, 98, 1, 1, 1, 1);
INSERT INTO permiso VALUES (136, 2, 112, 1, 1, 1, 1);
INSERT INTO permiso VALUES (139, 2, 4, 1, 1, 1, 1);
INSERT INTO permiso VALUES (112, 2, 221, 1, 1, 1, 1);
INSERT INTO permiso VALUES (140, 2, 6, 1, 1, 1, 1);
INSERT INTO permiso VALUES (137, 2, 113, 1, 1, 1, 1);
INSERT INTO permiso VALUES (141, 2, 7, 1, 1, 1, 1);
INSERT INTO permiso VALUES (124, 2, 225, 1, 1, 1, 1);
INSERT INTO permiso VALUES (142, 2, 5, 1, 1, 1, 1);
INSERT INTO permiso VALUES (157, 2, 42, 1, 1, 1, 1);
INSERT INTO permiso VALUES (143, 2, 108, 1, 1, 1, 1);
INSERT INTO permiso VALUES (138, 2, 226, 1, 1, 1, 1);
INSERT INTO permiso VALUES (110, 2, 223, 1, 1, 1, 1);
INSERT INTO permiso VALUES (13, 1, 103, 1, 1, 1, 1);
INSERT INTO permiso VALUES (111, 2, 224, 1, 1, 1, 1);
INSERT INTO permiso VALUES (158, 2, 43, 1, 1, 1, 1);
INSERT INTO permiso VALUES (14, 1, 105, 1, 1, 1, 1);
INSERT INTO permiso VALUES (165, 2, 229, 1, 1, 1, 1);
INSERT INTO permiso VALUES (159, 2, 90, 1, 1, 1, 1);
INSERT INTO permiso VALUES (15, 1, 106, 1, 1, 1, 1);
INSERT INTO permiso VALUES (149, 2, 53, 1, 1, 1, 1);
INSERT INTO permiso VALUES (160, 2, 57, 1, 1, 1, 1);
INSERT INTO permiso VALUES (150, 2, 54, 1, 1, 1, 1);
INSERT INTO permiso VALUES (161, 2, 59, 1, 1, 1, 1);
INSERT INTO permiso VALUES (162, 2, 58, 1, 1, 1, 1);
INSERT INTO permiso VALUES (148, 2, 27, 1, 1, 1, 1);
INSERT INTO permiso VALUES (151, 2, 56, 1, 1, 1, 1);
INSERT INTO permiso VALUES (108, 2, 29, 1, 1, 1, 1);
INSERT INTO permiso VALUES (113, 2, 30, 1, 1, 1, 1);
INSERT INTO permiso VALUES (163, 2, 101, 1, 1, 1, 1);
INSERT INTO permiso VALUES (16, 1, 110, 1, 1, 1, 1);
INSERT INTO permiso VALUES (122, 2, 111, 1, 1, 1, 1);
INSERT INTO permiso VALUES (121, 2, 227, 1, 1, 1, 1);
INSERT INTO permiso VALUES (152, 2, 89, 1, 1, 1, 1);
INSERT INTO permiso VALUES (1, 1, 1, 1, 1, 1, 1);
INSERT INTO permiso VALUES (153, 2, 38, 1, 1, 1, 1);
INSERT INTO permiso VALUES (17, 1, 112, 1, 1, 1, 1);
INSERT INTO permiso VALUES (2, 1, 2, 1, 1, 1, 1);
INSERT INTO permiso VALUES (154, 2, 39, 1, 1, 1, 1);
INSERT INTO permiso VALUES (4, 1, 87, 1, 1, 1, 1);
INSERT INTO permiso VALUES (18, 1, 113, 1, 1, 1, 1);
INSERT INTO permiso VALUES (5, 1, 69, 1, 1, 1, 1);
INSERT INTO permiso VALUES (10, 1, 68, 1, 1, 1, 1);
INSERT INTO permiso VALUES (103, 1, 225, 1, 1, 1, 1);
INSERT INTO permiso VALUES (102, 1, 226, 1, 1, 1, 1);
INSERT INTO permiso VALUES (164, 1, 229, 1, 1, 1, 1);

