#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008  Francisco José Rodríguez Bogado,                   #
#                          Diego Muñoz Escalante.                             #
# (pacoqueen@users.sourceforge.net, escalant3@users.sourceforge.net)          #
#                                                                             #
# This file is part of GeotexInn.                                             #
#                                                                             #
# GeotexInn is free software; you can redistribute it and/or modify           #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation; either version 2 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# GeotexInn is distributed in the hope that it will be useful,                #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with GeotexInn; if not, write to the Free Software                    #
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA  #
###############################################################################


###################################################################
## clientes.py - Alta, baja, consulta y mod. de clientes. 
###################################################################
## NOTAS:
##  Los vencimientos se introducen y almacenan en la BD como un 
##  texto. No se verifica formato ninguno (!). Es tarea de la 
##  ventana de facturas el parsear correctamente los vencimientos.
##  El texto debe ser de la forma "30-60", "30-60-90", etc...
## ----------------------------------------------------------------
##  
###################################################################
## Changelog:
## 11 de octubre de 2005 -> Inicio
## 11 de octubre de 2005 -> 99% funcional
## 20 de octubre de 2005 -> Añadidos vencimientos por defecto.
## 9 de diciembre de 2005 -> Añadidos campos adicionales (#0000025)
## 9 de diciembre de 2005 -> Añadido IVA por defecto
## 29 de enero de 2005 -> Portado a versión 02.
## 7 de febrero de 2005 -> Añadida la funcionalidad de los pagos
## 13 de febrero de 2005 -> Añadida funcionalidad de contadores
## 4 de julio de 2006 -> CIF como campo obligatorio.
###################################################################
## PLAN: Sería interesante abrir las ventanas de pedidos y produc-
##       tos desde las búsquedas del "expander" «Consultas».
###################################################################

import os
from ventana import Ventana
import utils
import pygtk
import gobject
pygtk.require('2.0')
import gtk, gtk.glade, time
try:
    import pclases
except ImportError:
    import sys
    from os.path import join as pathjoin
    sys.path.append(pathjoin("..", "framework"))
    import pclases
try:
    import geninformes
except ImportError:
    import sys
    sys.path.append('../informes')
    import geninformes
from utils import _float as float
from informes import abrir_pdf, abrir_csv
from ventana_progreso import VentanaActividad
import pclase2tv
import datetime
from up_facturar import buscar_clases, generar_servicios, facturar
from up_consulta_facturas import imprimir_ticket_from_factura

PAGE_COBROS = 7

class Clientes(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        self._objetoreciencreado = None
        Ventana.__init__(self, 'clientes.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_pedidos/clicked': self.ver_pedidos,
                       'b_productos/clicked': self.ver_productos,
                       'b_nuevo/clicked': self.crear_nuevo_cliente,
                       'b_actualizar/clicked': self.actualizar_ventana,
                       'b_guardar/clicked': self.guardar,
                       'b_borrar/clicked': self.borrar,
                       'b_nuevo_contador/clicked': self.crear_nuevo_contador,
                       'cmb_contador/changed': self.seleccionar_contador,
                       'b_tarifa/clicked': self.asignar_tarifa,
                       'b_buscar/clicked': self.buscar_cliente,
                       'b_listado/clicked': self.listado_clientes, 
                       'b_listado_riesgos/clicked': self.listado_riesgos, 
                       'b_presupuestos/clicked': self.ver_presupuestos, 
                       'b_ayuda_formapago/clicked': self.ayuda_forma_pago, 
                       'b_add_cuenta/clicked': self.add_cuenta, 
                       'b_drop_cuenta/clicked': self.drop_cuenta, 
                       'b_por_sexo_y_edad/clicked': 
                            self.listar_por_sexo_y_edad, 
                       'b_proforma/clicked': self.listar_facturas_proforma, 
                       'b_facturas/clicked': self.listar_facturas, 
                       'b_productos_proforma/clicked': 
                            self.listar_productos_proforma, 
                       'notebook1/switch-page': self.actualizar_riesgo, 
                       'ch_ign_asegurado/toggled': self.cambiar_ch_asegurado, 
                       'ch_ign_concedido/toggled': self.cambiar_ch_concedido, 
                       'b_add_padecimiento/clicked': self.add_padecimiento, 
                       'b_drop_padecimiento/clicked': self.drop_padecimiento, 
                       "e_pais/key-release-event": self.cambiar_iva, 
                       "e_paisfacturacion/key-release-event": self.cambiar_iva, 
                       'b_add_producto/clicked': self.add_producto, 
                       'b_drop_producto/clicked': self.drop_producto, 
                       'b_correos/clicked': exportar_correos, 
                       'b_telefonos/clicked': self.exportar_telefonos, 
                       'b_fechaNacimiento/clicked': self.set_fechaNacimiento, 
                       'b_fechaAlta/clicked': self.set_fechaAlta, 
                       'b_foto/clicked': self.set_foto, 
                       'b_cobrar/clicked': self._cobrar, 
                       #'tv_nofacturado/cursor-changed': self.refresh_importe,
                       'b_fechacobro/clicked': self.set_fechacobro,
                       'e_fechacobro/focus-out-event': 
                                                self.actualizar_fechacobro, 
                       'notebook1/switch-page': self.actualizar_pestanna, 
                       'b_deep_refresh/clicked': self.deep_refresh, 
                       'b_abonar/clicked': self.anular_factura, 
                       'e_importe/changed': self.actualizar_importe_civa, 
                      }  
        self.add_connections(connections)
        self.inicializar_ventana()
        sel = self.wids['tv_nofacturado'].get_selection()
        sel.connect("changed", self.refresh_importe)
        if self.objeto == None:
            self.ir_a_primero()
        else:
            self.ir_a(objeto)
        gtk.main()

    def actualizar_importe_civa(self, *args, **kw):
        """
        Muestra el importe multiplicado por el IVA del cliente en el entry
        de importe con IVA.
        """
        try:
            total = utils._float(self.wids['e_importe'].get_text())
        except (TypeError, ValueError):
            total = 0.0
        try:
            iva = self.objeto.iva
        except AttributeError:
            iva = 0.0
        self.wids['e_importe_civa'].set_text(utils.float2str(total*(1+iva)))

    def anular_factura(self, boton):
        """
        Elimina las facturas completas seleccionadas. 
        """
        sel = self.wids['tv_facturado'].get_selection()
        model, rows = sel.get_selected_rows()
        if not utils.dialogo(titulo = "¿ANULAR FACTURAS?", 
                             texto = "Está a punto de eliminar %d factura%s.\n"
                                     "Esta acción no se puede deshacer.\n"
                                     "¿Está seguro?"  % (
                                        len(rows), 
                                        len(rows) > 1 and "s" or ""),  
                             padre = self.wids['ventana']):
            return
        fras_a_abonar = set()
        for row in rows:
            puid = model[row][-1]
            obj = pclases.getObjetoPUID(puid)
            if isinstance(obj, pclases.SuperFacturaVenta):
                fras_a_abonar.add(obj)
            else:
                fra = obj.get_factura_o_prefactura()
                fras_a_abonar.add(fra)
        actualizar_tv = False
        for fra in fras_a_abonar:
            actualizar_tv = True
            # Borro líneas de venta.
            for ldv in fra.lineasDeVenta:
                ldv.destroySelf()
            # Elimino servicios.
            for srv in fra.servicios:
                for a in srv.actividades:
                    a.servicio = None
                srv.destroySelf()
            # Elimino vencimientos.
            # Elimino cobros.
            # Elimino documentos adjuntos.
            # Elimino notas... con el en_cascada. Ya no debería fallar.
            fra.destroy_en_cascada()
        if actualizar_tv:
            #self.rellenar_facturado()
            self.deep_refresh()
    
    def actualizar_fechacobro(self, w, event): 
        """
        Intenta parsear la fecha del entry y la reescribe correctamente.
        """
        valor_fallback = None
        if isinstance(valor_fallback, type("cadena")):
            try:
                valor_fallback = utils.parse_fecha(valor_fallback)
            except (ValueError, TypeError):
                valor_fallback = None
        if valor_fallback == None:
            valor_fallback = datetime.date.today()
        txt = w.get_text()
        try:
            fecha = utils.parse_fecha(txt)
        except (ValueError, TypeError):
            fecha = valor_fallback
        w.set_text(utils.str_fecha(fecha))
    
    def _cobrar(self, boton):
        """
        Wrapper para cobrar. Solo para poder poner el cursor en "pensando..."
        """
        self.wids['ventana'].window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        while gtk.events_pending(): gtk.main_iteration(False)
        try:
            self.cobrar(boton)
        finally:
            self.wids['ventana'].window.set_cursor(None)
    
    def cobrar(self, boton):
        """
        Para los productos seleccionados en el TV de no facturados crea una 
        factura de venta y asigna un cobro a la misma con la forma de pago 
        e importe introducido.
        """
        sel = self.wids['tv_nofacturado'].get_selection()
        model, rows = sel.get_selected_rows()
        try:
            importe = utils._float(self.wids['e_importe'].get_text())
        except (TypeError, ValueError):
            utils.dialogo_info("ERROR EN FORMATO NUMÉRICO", 
                               texto = "El texto «%s» no es un número válido."
                                % self.wids['e_importe'].get_text(), 
                               padre = self.wids['ventana'])
        else:
            actividades_a_facturar = []
            for row in rows:
                puid = model[row][-1]
                if not puid:
                    continue    # Clase suelta o vete tú a saber qué, 
                                # pero sin producto.
                producto = pclases.getObjetoPUID(puid)
                try:
                    actividades = self._actividades_por_producto[self.objeto][producto]
                except KeyError:
                    if pclases.DEBUG:
                        print "clientes::cobrar -> Producto listado %s no "\
                              "tiene actividades sin facturar." % puid
                else:
                    actividades_a_facturar += actividades
            # Aquí ya tengo mis actividades listas para asociarlas a un 
            # servicio y facturarlo.
            if actividades_a_facturar:
                srvs = generar_servicios(actividades_a_facturar, 
                                         precio = importe)
                try:
                    fecha = utils.parse_fecha(self.wids['e_fechacobro'].get_text())
                except (ValueError, TypeError):
                    fecha = datetime.date.today()
                    self.wids['e_fechacobro'].set_text(utils.str_fecha(fecha))
                fra = facturar(self.objeto, actividades_a_facturar, 
                               usuario = self.usuario, 
                               ventana_padre = self.wids['ventana'], 
                               abrir_ventana_facturas = False, 
                               intentar_marcar_como_cobrada = False, 
                               servicios = srvs, 
                               fecha = fecha)
                formapago = self.wids['cbe_formadepago'].child.get_text()
                vtos = fra.crear_vencimientos_por_defecto(formapago)
                # Como es posible que la fecha de la factura no sea la 
                # especificada si hay alguna factura ya dada de alta con fecha 
                # posterior; el cobro sí que lo creo a la fecha indicada para 
                # que aparezca en el "report diario" de ese día.
                for vto in vtos:    # Un cobro por vencimiento. 
                    pclases.Cobro(facturaVenta = fra, 
                                  importe = vto.importe, 
                                  observaciones = "Marcada como cobrada "
                                    "automáticamente desde ventana de "
                                    "clientes.", 
                                  cliente = fra.cliente, 
                                  fecha = fecha)
                if utils.dialogo(titulo = "¿IMPRIMIR TICKET?", 
                        texto = "¿Desea imprimir un ticket con el importe?\n"
                            "\n\n"
                            "Tenga en cuenta que es necesaria una impresora\n"
                            "de tickets conectada al puerto paralelo del \n"
                            "ordenador.", 
                        padre = self.wids['ventana'], 
                        defecto = False, 
                        tiempo = 30):
                    imprimir_ticket_from_factura(fra)
                if utils.dialogo(titulo = "FACTURA CREADA", 
                        texto = "Factura %s creada y marcada como\n" 
                            "cobrada mediante %s por un importe\n"
                            "total de %s.\n\n"
                            "Si desea anular el cobro, elimine\n"
                            "la factura desde la ventana de "
                            "facturas de venta\n\n\n"
                            "¿Quiere abrir la factura en ventana ahora?" % (
                                fra.numfactura, 
                                formapago, 
                                utils.float2str(fra.calcular_importe_total())), 
                        padre = self.wids['ventana'], 
                        defecto = False, 
                        tiempo = 30):
                    import facturas_venta
                    vfras=facturas_venta.FacturasVenta(objeto = fra, 
                                                       usuario = self.usuario)
                self.rellenar_no_facturado()
                self.rellenar_facturado()
    
    def refresh_importe(self, selection_or_tv):
        """
        Recalcula el importe en función de los productos seleccionados y 
        actualiza el entry de la pestaña «Cobros».
        """
        if isinstance(selection_or_tv, gtk.TreeView):
            tv = selection_or_tv
        elif isinstance(selection_or_tv, gtk.TreeSelection):
            tv = selection_or_tv.get_tree_view()
        else:
            return
        model, rows = tv.get_selection().get_selected_rows()
        total = 0.0
        for row in rows:
            importe = utils._float(model[row][1])
            total += importe
        self.wids['e_importe'].set_text(utils.float2str(total))
    
    def set_foto(self, boton):
        """
        Cambia la foto seleccionada para el cliente.
        """
        nomfich = utils.dialogo_abrir(titulo = "BUSCAR FOTOGRAFÍA CLIENTE", 
                                      filtro_imagenes = True, 
                                      padre = self.wids['ventana'])
        if nomfich != None:
            fich = open(nomfich, "rb")
            imagedata = ""
            binchunk = fich.read()
            while binchunk:
                imagedata += binchunk
                binchunk = fich.read()
            fich.close()
            if not self.objeto.fotos:                                        
                imagen = pclases.Foto(cliente = self.objeto, 
                                      data = imagedata)
            else:
                imagen = self.objeto.fotos[-1]
                imagen.store_from_file(nomfich)
            self.actualizar_ventana()

    def set_fechaNacimiento(self, boton):
        """
        Introduce la fecha seleccionada de un diálogo calendario en el entry.
        """
        self.wids['e_fechaNacimiento'].set_text(utils.str_fecha(
            utils.mostrar_calendario(
                fecha_defecto = self.objeto and self.objeto.fechaNacimiento 
                                or None, 
                padre = self.wids['ventana'])
            )
        )
    
    def set_fechaAlta(self, boton):
        """
        Introduce la fecha seleccionada de un diálogo calendario en el entry.
        """
        self.wids['e_fechaAlta'].set_text(utils.str_fecha(
            utils.mostrar_calendario(
                fecha_defecto = self.objeto and self.objeto.fechaAlta or None, 
                padre = self.wids['ventana'])
            )
        )

    def set_fechacobro(self, boton):
        """
        Introduce la fecha seleccionada de un diálogo calendario en el entry.
        """
        w = self.wids['e_fechacobro']
        w.set_text(utils.str_fecha(
            utils.mostrar_calendario(
                fecha_defecto = w.get_text(), 
                padre = self.wids['ventana'])
            )
        )

    def add_producto(self, boton):
        """
        Añade un producto al cliente.
        """
        productos_clases = []
        for pc in pclases.ProductoCompra.select():
            if pc.clases:
                productos_clases.append(pc)
        idproducto = utils.dialogo_combo(
            titulo = "SELECCIONE PRODUCTO", 
            texto = "Seleccione el tipo de clases contratada por el alumno:",
            ops = [(p.id, p.descripcion) for p in productos_clases], 
            padre = self.wids['ventana'])
        if idproducto:
            pc = pclases.ProductoCompra.get(idproducto)
            pclases.ProductoContratado(productoCompra = pc, 
                                    cliente = self.objeto, 
                                    fechaContratacion = datetime.date.today())
            self.rellenar_productos()

    def drop_producto(self, boton):
        """
        Elimina uno o varios productos contratados por el cliente.
        """
        sel = self.wids['tv_contratadas'].get_selection()
        model, iters = sel.get_selected_rows()
        if iters and utils.dialogo(titulo = "ELIMINAR CONTRATACIÓN", 
                texto = "¿Está seguro de eliminar las clases seleccionadas\n"
                        "de la lista de clases contratadas?", 
                padre = self.wids['ventana']):
            for iter in iters:
                producto_contratado = pclases.getObjetoPUID(model[iter][-1])
                producto_contratado.destroySelf()
            self.rellenar_productos()

    def cambiar_iva(self, editable, event):
        """
        Si el país es diferente a España, pone el IVA a 0%.
        """
        txt = editable.get_text()
        #print txt, txt.upper(), txt.lower()
        if txt.upper() != "ESPAÑA" and txt.lower() != "españa" and txt:
            self.wids['e_iva'].set_text("0")
        elif (txt.upper() == "ESPAÑA" or txt.lower() == "españa") and txt:
            self.wids['e_iva'].set_text("18")

    def globalizar_contacto(self, boton):
        """
        Añade los contactos seleccionados a todas las obras del cliente.
        """
        sel = self.wids['tv_contactos'].get_selection()
        model, iters = sel.get_selected_rows()
        if not iters:
            utils.dialogo_info(titulo = "SELECCIONE CONTACTO", 
                texto = "Debe seleccionar al menos un contacto \n"
                        "para hacerlo global a todas las obras \n"
                        "del cliente.", 
                padre = self.wids['ventana'])
        else:
            for iter in iters:
                copiadas = 0
                idcontacto = model[iter][-1]
                contacto = pclases.Contacto.get(idcontacto)
                for obra in self.objeto.obras:
                    if contacto not in obra.contactos:
                        obra.addContacto(contacto)
                        copiadas += 1
            utils.dialogo_info(titulo = "CONTACTO COPIADO", 
                texto = "El contacto se copió a %d obras." % copiadas, 
                padre = self.wids['ventana'])
            # No hace falta recargar. Cuando mueva el cursor lo verá, y en la 
            # obra actual ya estaba, así que lo sigue viendo.

    def add_contacto(self, boton):
        """
        Añade un contacto al cliente a través de la(s) obra(s) seleccionada en 
        el TreeView de obras. Si no hay seleccionada ninguna mostrará un 
        mensaje al usuario para que lo haga.
        """
        sel = self.wids['tv_obras'].get_selection()
        model, iters = sel.get_selected_rows()
        if not iters:
            utils.dialogo_info(titulo = "SELECCIONE OBRA", 
                texto = "Debe seleccionar al menos una obra con la que\n"
                        "relacionar el nuevo contacto.", 
                padre = self.wids['ventana'])
        else:
            nombre = utils.dialogo_entrada(titulo = "NOMBRE", 
                texto = "Introduzca el nombre -sin apellidos- del "
                        "nuevo contacto:", 
                padre = self.wids['ventana'])
            if nombre:
                apellidos = utils.dialogo_entrada(titulo = "APELLIDOS", 
                    texto = "Introduzca ahora los apellidos:", 
                    padre = self.wids['ventana'])
                if apellidos != None:
                    c = self.buscar_contacto_existente(nombre, apellidos)
                    if not c:
                        c = pclases.Contacto(nombre = nombre, 
                                             apellidos = apellidos)
                    for iter in iters:
                        #idobra = model[iter][-1]
                        #obra = pclases.Obra.get(idobra)
                        #c.addObra(obra)
                        pass
                    self.rellenar_contactos()

    def buscar_contacto_existente(self, _nombre, _apellidos):
        """
        Busca un contacto con los nombres y apellidos recibidos. Si lo 
        encuentra lo sugiere y devuelve el objeto contacto. En caso contrario 
        devuelve None.
        """
        try:
            import spelling
        except ImportError:
            import sys, os
            sys.path.append(os.path.join("..", "utils"))
            import spelling
        nombres_bd = []
        apellidos_bd = []
        for c in pclases.Contacto.select():
            for n in c.nombre.split():
                nombres_bd.append(n.lower())
            for a in c.apellidos.split():
                apellidos_bd.append(a.lower())
        corrnombre = spelling.SpellCorrector(" ".join(nombres_bd))
        corrapellidos = spelling.SpellCorrector(" ".join(apellidos_bd))
        nombres = [n.lower() for n in _nombre.split()]
        apellidos = [a.lower() for a in _apellidos.split()]
        nomcorregido = []
        apecorregido = []
        for nombre in nombres: 
            sugerencia = corrnombre.correct(nombre)
            nomcorregido.append(sugerencia)
        for apellido in apellidos:
            sugerencia = corrapellidos.correct(apellido)
            apecorregido.append(sugerencia)
        nombre = " ".join(nomcorregido)
        apellidos = " ".join(apecorregido)
        #contacto = pclases.Contacto.select(pclases.AND(
        #                pclases.Contacto.q.nombre == nombre, 
        #                pclases.Contacto.q.apellidos == apellidos))
        contacto = pclases.Contacto.select(""" 
            nombre ILIKE '%s' AND apellidos ILIKE '%s' """ 
            % (nombre, apellidos))
        if contacto.count() == 0:
            res = None
        else:
            res = contacto[0]
            if not utils.dialogo(titulo = "BUSCAR CONTACTO", 
                    texto = "¿El contacto que está buscando es:\n"
                        "%s %s\nCargo: %s\nTeléfono:%s?" % (
                        res.nombre, res.apellidos, 
                        res.cargo and res.cargo 
                            or '"sin cargo definido"', 
                        res.telefono and res.telefono 
                            or '"sin teléfono definido"'), 
                    padre = self.wids['ventana']):
                res = None
        return res

    def drop_contacto(self, boton):
        """
        Elimina el contacto seleccionado, desvinculándolo previamente de 
        cuantas obras tuviera.
        """
        sel = self.wids['tv_contactos'].get_selection()
        model, iters = sel.get_selected_rows()
        if not iters:
            return
        res = utils.dialogo(titulo = "ELIMINAR CONTACTO", 
            texto = "¿Desea eliminar el contacto por completo?\n"
                "\nSi pulsa «Sí» se eliminará el contacto.\n"
                "Si pulsa «No» se desvinculará de la obra seleccionada\n"
                "pero no se eliminará el contacto de otras posibles obras.\n"
                "Si pulsa «Cancelar» no se hará nada.", 
            padre = self.wids['ventana'], 
            cancelar = True, 
            defecto = gtk.RESPONSE_CANCEL, 
            bloq_temp = [gtk.RESPONSE_YES, gtk.RESPONSE_NO])
        if res != gtk.RESPONSE_CANCEL:
            for iter in iters:
                id = model[iter][-1]
                c = pclases.Contacto.get(id)
                if res == True:
                    for o in c.obras:
                        o.removeContacto(c)
                    c.destroySelf()
                else:
                    sel = self.wids['tv_obras'].get_selection()
                    modelobras, itersobras = sel.get_selected_rows() 
                    for iterobras in itersobras:
                        #idobra = modelobras[iterobras][-1]
                        #obra = pclases.Obra.get(idobra)
                        #obra.removeContacto(c)
                        # No lo borro aunque no le queden obras por si lo 
                        # busca en el futuro.
                        pass
            self.rellenar_contactos()

    def add_padecimiento(self, boton):
        """
        Añade un nuevo padecimiento al cliente.
        """
        texto = utils.dialogo_entrada(titulo = "NUEVO PADECIMIENTO", 
            texto = "Introduzca la nueva dolencia:", 
            padre = self.wids['ventana'])
        if texto:
            padecimiento = pclases.Padecimiento(texto = texto, 
                                            fecha = datetime.datetime.today(), 
                                            clienteID = self.objeto)
            model = self.wids['tv_padecimientos'].get_model()
            model.append((utils.str_fecha(padecimiento.fecha), 
                          padecimiento.texto, 
                          padecimiento.get_puid()))

    def drop_padecimiento(self, boton):
        """
        Elimina los padecimientos seleccionados.
        """
        sel = self.wids['tv_padecimientos'].get_selection()
        model, iters = sel.get_selected_rows()
        se_borro_algo = False
        for iter in iters:
            puid = model[iter][-1]
            padecimiento = pclases.getObjetoPUID(puid)
            try:
                padecimiento.destroySelf()
                se_borro_algo = True
            except Exception, e:
                txt = "No se pudo borrar el padecimiento %s. Excepción: %s" % (puid, e)
                print txt
                self.logger.error(txt)
        if se_borro_algo:
            self.rellenar_padecimientos()

    def rellenar_padecimientos(self):
        """
        Rellena la tabla de padecimienos del cliente.
        """
        if self.objeto:
            model = self.wids['tv_padecimientos'].get_model()
            model.clear()
            for p in self.objeto.padecimientos:
                model.append((utils.str_fecha(p.fecha), 
                              p.texto, 
                              p.get_puid()))
    
    def rellenar_productos(self):
        """
        Rellena la tabla de productos contratados, clases asignadas y 
        clases disponibles del cliente.
        """
        if self.objeto:
            disponibles = {}
            # Clases contratadas:
            model = self.wids['tv_contratadas'].get_model()
            model.clear()
            for p in self.objeto.productosContratados:
                padre = model.append(None, 
                                        (p.productoCompra.descripcion, 
                                         0, 
                                         utils.str_fecha(p.fechaContratacion), 
                                         p.get_puid()))
                for clase in p.productoCompra.clases:
                    numclases = clase.numClasesTotales
                    model.append(padre, (pclases.Clase.siglas_to_dias(
                                            clase.diaSemana), 
                                         numclases, 
                                         "", 
                                         clase.get_puid()))
                    model[padre][1] += numclases
                    # Para las disponibles:
                    try:
                        disponibles[p.productoCompra] += numclases
                    except KeyError:
                        disponibles[p.productoCompra] = numclases 
            # Clases asignadas:
            model = self.wids['tv_asignadas'].get_model()
            model.clear()
            for a in self.objeto.actividades:
                asiste = a.asistio(self.objeto)
                producto = a.get_or_guess_productoCompra()
                model.append((utils.str_fecha(a.fechahoraInicio), 
                              utils.str_hora_corta(a.fechahoraInicio), 
                              asiste, 
                              producto and producto.descripcion or "", 
                              a.esta_facturado_para(self.objeto), 
                              a.get_puid()))
                #  Para las disponibles:
                producto = a.get_or_guess_productoCompra()
                try:
                    disponibles[producto] -= 1
                except KeyError:
                    pass    # No la contrató.
            # Clases disponibles:
            model = self.wids['tv_disponibles'].get_model()
            model.clear()
            for p in disponibles:
                for i in range(disponibles[p]):
                    desc_clase = "1 clase (%s)" % p.descripcion
                    model.append((desc_clase, p.get_puid()))
            # Grupos
            actuales = self.objeto.get_grupos()
            model = self.wids['tv_grupos_actuales'].get_model()
            model.clear()
            for actual in actuales:
                model.append((actual.nombre, actual.get_puid()))
            model = self.wids['tv_grupos_anteriores'].get_model()
            model.clear()
            for g in self.objeto.gruposAlumnos:
                if g not in actuales:
                    model.append((g.nombre, g.get_puid()))

    def cambiar_fecha_padecimiento(self, cell, path, text):
        model = self.wids['tv_padecimientos'].get_model()
        puid = model[path][-1]
        p = pclases.getObjetoPUID(puid)
        try:
            p.fecha = utils.parse_fecha(text)
            p.syncUpdate()
        except (TypeError, ValueError):
            utils.dialogo_info(titulo = "ERROR DE FORMATO", 
                               texto = "La fecha %s no es correcta." % text, 
                               padre = self.wids['ventana'])
        else:
            model[path][0] = utils.str_fecha(p.fecha)

    def cambiar_dolencia(self, cell, path, text):
        model = self.wids['tv_padecimientos'].get_model()
        puid = model[path][-1]
        p = pclases.getObjetoPUID(puid)
        p.texto = text
        p.syncUpdate()
        model[path][1] = p.texto

    def cambiar_importe_nofacturado(self, cell, path, text):
        try:
            importe = utils._float(text)
        except (ValueError, TypeError):
            utils.dialogo_info(titulo = "ERROR EN FORMATO NUMÉRICO", 
                texto = "El texto «%s» tecleado no es un número." % (text), 
                padre = self.wids['ventana'])
        else:
            model = self.wids['tv_nofacturado'].get_model()
            model[path][1] = utils.float2str(importe)
            self.refresh_importe(self.wids['tv_nofacturado'])

    def rellenar_contactos(self, *args, **kw):
        """
        Rellena la tabla de contactos en función de las obras seleccionadas 
        en el primer TreeView.
        """
        return
        if self.objeto:
            ##################################################################
            def filtro_pertenece_a_obra(objeto, obras, contactos_ya_puestos):
                """
                Devuelve True si alguna de las obras del objeto está en la 
                lista recibida.
                """
                res = False
                for obra in objeto.obras:
                    if (obra in obras 
                        and objeto.id not in contactos_ya_puestos):
                        res = True
                        break
                return res
            ##################################################################
            selection = self.wids['tv_obras'].get_selection()
            model,iters = selection.get_selected_rows()
            if not model:
                return  
            if not iters:
                model = self.wids['tv_obras'].get_model()
                iters = []
                iter = model.get_iter_first()
                while iter:
                    iters.append(iter)
                    iter = model.iter_next(iter)
            obras = []
            contactos_ya_puestos = []
            primera_obra = True
            for iter in iters:
                idobra = model[iter][-1]
                obra = pclases.Obra.get(idobra)
                obras.append(obra)
                self.tvcontactos.rellenar_tabla(
                                filtro = filtro_pertenece_a_obra, 
                                padre = self.wids['ventana'], 
                                limpiar_model = primera_obra, 
                                obras = obras, 
                                contactos_ya_puestos = contactos_ya_puestos)
                contactos_ya_puestos += [c.id for c in obra.contactos]
                primera_obra = False

    def cambiar_ch_asegurado(self, ch):
        self.wids['e_riesgoAsegurado'].set_sensitive(not ch.get_active())
        if ch.get_active():
            self.wids['e_riesgoAsegurado'].set_text(utils.float2str(-1))
        else:
            self.wids['e_riesgoAsegurado'].set_text(utils.float2str(0))

    def cambiar_ch_concedido(self, ch):
        self.wids['e_riesgoConcedido'].set_sensitive(not ch.get_active())
        if ch.get_active():
            self.wids['e_riesgoConcedido'].set_text(utils.float2str(-1))
        else:
            self.wids['e_riesgoConcedido'].set_text(utils.float2str(0))

    def actualizar_riesgo(self, nb, ptr_pag, num_pag):
        """
        Si el notebook ha cambiado la página a la de gestión de riesgos, 
        actualiza y muestra la información. 
        Así evito cargarla desde el principio y ralentizar la ventana completa 
        en espera de esos datos.
        OJO: Nada de prefacturas. Solo facturas oficiales.
        """
        if num_pag == 4:
            self.rellenar_riesgo_campos_objeto()
            if not(#self.wids['ch_ign_asegurado'].get_active() and 
                   self.wids['ch_ign_concedido'].get_active()):
                self.rellenar_riesgo_campos_calculados()

    def rellenar_riesgo_campos_objeto(self):
        self.wids['ch_ign_concedido'].set_active(self.objeto.riesgoConcedido<0)
        self.wids['ch_ign_asegurado'].set_active(self.objeto.riesgoAsegurado<0)
        self.wids['e_riesgoConcedido'].set_text(utils.float2str(
            self.objeto.riesgoConcedido))
        self.wids['e_riesgoAsegurado'].set_text(utils.float2str(
            self.objeto.riesgoAsegurado))
        # Esto lo machacará el rellenar_...calculados si fuera oportuno.
        self.wids['e_pdte_cobro'].set_text("")
        self.wids['e_pdte_vencido'].set_text("")
        self.wids['e_credito'].set_text("N/A")
        self.wids['tv_pdte'].get_model().clear()

    def rellenar_riesgo_campos_calculados(self):
        self.wids['ventana'].window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        vpro = VentanaActividad(texto = "Esta operación puede tardar unos "
                                        "minutos...", 
                                padre = self.wids['ventana'])
        global seguir 
        seguir = True
        def mover_progreso(vpro):
            global seguir
            vpro.mover()
            while gtk.events_pending(): gtk.main_iteration(False)
            return seguir
        gobject.timeout_add(50, mover_progreso, vpro, 
                            priority = gobject.PRIORITY_HIGH_IDLE + 20)
        vpro.mostrar()
        while gtk.events_pending(): gtk.main_iteration(False)
        
        # TODO: Esto es EXTREMADAMENTE lento en clientes con muchas facturas.

        # XXX
        #import time
        #antes = time.time()
        # XXX

        model = self.wids['tv_pdte'].get_model()
        model.clear()
        cliente = self.objeto
        pdte_vencido, dicfras = cliente.calcular_pendiente_cobro_vencido()
        self.wids['e_pdte_vencido'].set_text(utils.float2str(pdte_vencido))
        for f in dicfras:
            model.append((f.numfactura, 
                          utils.str_fecha(f.fecha), 
                          utils.float2str(f.calcular_importe_total()), 
                          utils.float2str(dicfras[f][0]), 
                          utils.float2str(dicfras[f][1]), 
                          f.get_str_estado(), 
                          f.id))
            vpro.mover()
        # XXX
        #print "1.-", time.time() - antes
        #antes = time.time()
        # XXX
        pdte_cobro = self.objeto.calcular_pendiente_cobro()
        self.wids['e_pdte_cobro'].set_text(utils.float2str(pdte_cobro))
        # XXX
        #print "2.-", time.time() - antes
        # XXX
        credito = self.objeto.calcular_credito_disponible(pdte_cobro)
        self.wids['e_credito'].set_text(utils.float2str(credito))
        if credito <= 0:
            self.wids['e_credito'].modify_text(gtk.STATE_NORMAL, 
                self.wids['e_credito'].get_colormap().alloc_color("red"))
        else:
            self.wids['e_credito'].modify_text(gtk.STATE_NORMAL, None)
        seguir = False
        vpro.ocultar()
        self.wids['ventana'].window.set_cursor(None)

    def listar_facturas_proforma(self, boton):
        """
        Lista todas las facturas proforma del cliente en un diálogo de 
        resultados de búsqueda.
        """
        if self.objeto:
            proformas = pclases.Prefactura.select(
                pclases.Prefactura.q.clienteID == self.objeto.id, 
                orderBy = "fecha")
            fras = [(f.id, 
                     f.numfactura, 
                     utils.str_fecha(f.fecha), 
                     utils.float2str(f.calcular_importe_total()), 
                     f.bloqueada)
                    for f in proformas]
            fra = utils.dialogo_resultado(fras,
                                          titulo = 'FACTURAS PROFORMA',
                                          cabeceras = ('ID', 
                                                       'Número', 
                                                       'Fecha', 
                                                       'Total', 
                                                       'Bloqueada'), 
                                          padre = self.wids['ventana'])
            if fra and fra > 0:
                try:
                    fra = pclases.Prefactura.get(fra)
                except:
                    return
                import prefacturas
                v = prefacturas.Prefacturas(objeto=fra, usuario=self.usuario)

    def listar_facturas(self, boton):
        """
        Lista todas las facturas del cliente en un diálogo de 
        resultados de búsqueda.
        """
        if self.objeto:
            facturas = pclases.FacturaVenta.select(
                pclases.FacturaVenta.q.clienteID == self.objeto.id, 
                orderBy = "fecha")
            fras = [(f.id, 
                     f.numfactura, 
                     utils.str_fecha(f.fecha), 
                     utils.float2str(f.calcular_importe_total()), 
                     utils.float2str(f.calcular_pendiente_cobro()), 
                     f.bloqueada)
                    for f in facturas]
            fra = utils.dialogo_resultado(fras,
                        titulo = 'FACTURAS DE %s' % self.objeto.nombre,
                        cabeceras = ('ID', 
                                     'Número', 
                                     'Fecha', 
                                     'Total (IVA incl.)', 
                                     'Pendiente de cobro', 
                                     'Bloqueada'), 
                        padre = self.wids['ventana'])
            if fra and fra > 0:
                try:
                    fra = pclases.FacturaVenta.get(fra)
                except:
                    return
                import facturas_venta
                v = facturas_venta.FacturasVenta(objeto = fra, 
                                                 usuario = self.usuario)

    def listar_productos_proforma(self, boton):
        """
        Muestra los productos comprados en prefacturas, junto con sus totales, 
        y abre el seleccionado en la ventana correspondiente.
        """
        if self.objeto:
            proformas = pclases.Prefactura.select(
                pclases.Prefactura.q.clienteID == self.objeto.id, 
                orderBy = "fecha")
            productos = {}
            for fra in proformas:
                for ldv in fra.lineasDeVenta:
                    producto = ldv.producto
                    if producto not in productos:
                        productos[producto] = {
                                        "cantidad": ldv.cantidad, 
                                        "subtotal": ldv.calcular_subtotal(), 
                                        "beneficio": ldv.calcular_beneficio()}
                    else:
                        productos[producto]["cantidad"] += ldv.cantidad
                        productos[producto]["subtotal"] \
                            += ldv.calcular_subtotal() 
                        productos[producto]["beneficio"] \
                            += ldv.calcular_beneficio()
            pros = [("%s:%d" % (
                        isinstance(p, pclases.ProductoVenta) and "PV" or "PC", 
                        p.id), 
                     p.codigo, 
                     p.descripcion, 
                     utils.float2str(productos[p]["cantidad"]),
                     utils.float2str(productos[p]["subtotal"]),
                     utils.float2str(productos[p]["beneficio"]),
                    ) 
                    for p in productos]
            pro = utils.dialogo_resultado(pros,
                                    titulo = 'PRODUCTOS EN FACTURAS PROFORMA',
                                    cabeceras = ('ID', 
                                                 'Código', 
                                                 'Descripción', 
                                                 'Cantidad total', 
                                                 'Importe total', 
                                                 'Beneficio calculado'), 
                                    padre = self.wids['ventana'])
            if pro and pro > 0:
                idproducto = pro
                try:
                    if "PV" in idproducto:
                        producto = pclases.ProductoVenta.get(
                            idproducto.split(":")[1])
                        if producto.es_rollo():
                            import productos_de_venta_rollos
                            ventana_producto = productos_de_venta_rollos.ProductosDeVentaRollos(producto, usuario = self.usuario)
                        elif producto.es_bala() or producto.es_bigbag():
                            import productos_de_venta_balas
                            ventana_producto = productos_de_venta_balas.ProductosDeVentaBalas(producto, usuario = self.usuario)
                    elif "PC" in idproducto:
                        producto = pclases.ProductoCompra.get(
                            idproducto.split(":")[1])
                        import productos_compra
                        ventana_producto = productos_compra.ProductosCompra(producto, usuario = self.usuario)
                except:
                    pass

    def abrir_pedido(self, tv):
        """
        Abre una ventana con el pedido marcado en el TreeView recibido.
        """
        model, iter = tv.get_selection().get_selected()
        if iter != None:
            id = model[iter][0]
            pedido = pclases.PedidoVenta.get(id)
            import pedidos_de_venta
            ventana = pedidos_de_venta.PedidosDeVenta(objeto = pedido, 
                                                      usuario = self.usuario)

    def ayuda_forma_pago(self, boton):
        """
        Muestra un texto de ayuda.
        """
        utils.dialogo_info(titulo = "FORMA DE PAGO", 
                           texto = """
        D.F.F.: Días a partir de la fecha de factura.                               
        D.F.R.: Días a partir de la fecha de recepción de la factura (en la         
                práctica es similar a D.F.F.).                                      
        D.U.D.M.F.F.: Días a partir del último día del mes de la fecha de          
                factura.                                                            
        Si usa otras siglas se ignorarán, teniendo en cuenta solo los días          
        indicados en número. Si los vencimientos son múltiples (por ejemplo,        
        a «30, 60 y 120 días fecha factura», puede usar guiones, comas o            
        espacios como separación: «30-60-120 D.F.F.».                               
                           """, 
                           padre = self.wids['ventana'])

    def listado_clientes(self, boton):
        """
        Muestra un listado de todos los clientes 
        habilitados.
        """
        campos = [(0, "nombre", "Nombre"), 
                  (1, ["pais", "provincia", "ciudad", "cp", "nombre"], 
                      "Ciudad y provincia"), 
                    # BUG: En SQL Barcelona < ALICANTE < BARCELONA
                  (2, ["formadepago", "nombre"], "Forma de pago")]
        orden = utils.dialogo_combo(
                  titulo = "ORDEN DEL LISTADO", 
                  texto = "Seleccione el campo por el que ordenar el informe.",
                  ops = [(c[0], c[2]) for c in campos], 
                  padre = self.wids['ventana'], 
                  valor_por_defecto = 0)
        if orden != None:
            filtro = utils.dialogo_combo(
                titulo = "FILTRO DE CLIENTES", 
                texto = "Seleccione los clientes a listar:", 
                ops = [(0, "Todos los clientes"), 
                       (1, "Clientes activos"), 
                       (2, "Clientes deshabilitados")], 
                padre = self.wids['ventana'], 
                valor_por_defecto = 1)
            if filtro != None:
                self.wids['ventana'].window.set_cursor(
                    gtk.gdk.Cursor(gtk.gdk.WATCH))
                while gtk.events_pending(): gtk.main_iteration(False)
                try:
                    if filtro == 0:
                        clientes = pclases.Cliente.select(
                                    orderBy = campos[orden][1])
                        titulo = "" # Así conserva el valor por defecto del 
                                    # listado en geninformes.
                    elif filtro == 1:
                        clientes = pclases.Cliente.select(
                                    pclases.Cliente.q.inhabilitado == False, 
                                    orderBy = campos[orden][1])
                        titulo = "Clientes activos"
                    elif filtro == 2:
                        clientes = pclases.Cliente.select(
                                    pclases.Cliente.q.inhabilitado == True, 
                                    orderBy = campos[orden][1])
                        titulo = "Clientes inhabilitados"
                    listado = geninformes.listado_clientes(clientes, titulo)
                    abrir_pdf(listado)
                finally:
                    self.wids['ventana'].window.set_cursor(None)

    def listado_riesgos(self, boton):
        """
        Muestra un listado de todos los clientes 
        habilitados con los riesgos asegurados y concedidos.
        """
        campos = [(0, "nombre", "Nombre"), 
                  (1, ["pais", "provincia", "ciudad", "cp", "nombre"], "Ciudad y provincia"), 
                    # BUG: En SQL Barcelona < ALICANTE < BARCELONA
                  (2, ["formadepago", "nombre"], "Forma de pago")]
        orden = utils.dialogo_combo(
                  titulo = "ORDEN DEL LISTADO", 
                  texto = "Seleccione el campo por el que ordenar el informe.",
                  ops = [(c[0], c[2]) for c in campos], 
                  padre = self.wids['ventana'], 
                  valor_por_defecto = 0)
        if orden != None:
            clientes = pclases.Cliente.select(
                        pclases.Cliente.q.inhabilitado == False, 
                        orderBy = campos[orden][1])
            listado = geninformes.listado_clientes_solo_riesgos(clientes)
            abrir_pdf(listado)

    def listar_por_sexo_y_edad(self, boton):
        """
        Muestra un listado de todos los clientes 
        habilitados.
        """
        opciones = ((1, "Masculino"), 
                    (2, "Femenino"))
        sexo = utils.dialogo_combo(titulo = "SELECCIONE SEXO", 
                                     texto = "Seleccione:", 
                                     ops = opciones, 
                                     padre = self.wids['ventana'])
        if sexo != None and isinstance(sexo, int):
            clientes = pclases.Cliente.select(
                pclases.Cliente.q.sexoMasculino == (sexo == 1), 
                orderBy = "-fechaNacimiento")
            listado = geninformes.listado_clientes(clientes)
            abrir_pdf(listado)

    # --------------- Funciones auxiliares ------------------------------
    def es_diferente(self):
        """
        Devuelve True si la información en pantalla es distinta a la
        del objeto en memoria.
        """
        cliente = self.objeto
        if cliente == None: return False    # Si no hay cliente activo, 
                        # devuelvo que no hay cambio respecto a la ventana
        condicion = True
        lista = [cli for cli in cliente.sqlmeta.columnList
                    if cli.name!='tarifaID' 
                        and cli.name!='contadorID' 
                        and cli.name!='formadepago' 
                        and cli.name != "clienteID" 
                        and cli.name != "porcentaje" 
                        and cli.name != "enviarCorreoAlbaran" 
                        and cli.name != "enviarCorreoFactura" 
                        and cli.name != "enviarCorreoPacking" 
                        and cli.name != "proveedorID" 
                        and cli.name != "cuentaOrigenID" 
                        and cli.name != "riesgoConcedido" 
                        and cli.name != "riesgoAsegurado"
                        and cli.name != "copiasFactura" 
                        and cli.name != "fechaNacimiento"
                        and cli.name != "fechaAlta"
                        and cli.name != "sexoMasculino"
                        and cli.name != "lunes"
                        and cli.name != "martes"
                        and cli.name != "miercoles"
                        and cli.name != "jueves"
                        and cli.name != "viernes"
                        and cli.name != "sabado"
                        and cli.name != "domingo" 
                        and cli.name != "codigo"] 
            # Quito la columna tarifa que no se muestra en el formulario 
            # de clientes
        for c in lista:
            textobj = str(eval('cliente.%s' % c.name))
            # NOTA: El str es para comparar todo como texto (para evitar una 
            #       comparación especial del campo IVA, que es el único 
            #       numérico).
            if c.name == 'iva':
                try:
                    ivaparseado = utils.parse_porcentaje(
                        self.wids['e_iva'].get_text(), fraccion = True)
                except ValueError:
                    ivaparseado = 0
                textven = str(ivaparseado)
            else:
                textven = self.leer_valor(self.wids['e_%s' % c.name])
            if isinstance(textven, bool):
                if (c.name == "packingListConCodigo" 
                    or c.name == "facturarConAlbaran"):
                    condicion = condicion and textven == getattr(cliente, 
                                                                 c.name)
                else:
                    condicion = condicion and textven == getattr(cliente, 
                                                               "inhabilitado")
            else:
                condicion = condicion and textobj == textven
            if not condicion:
                break
        try:
            condicion = (condicion 
                         and cliente.contador.prefijo 
                                == self.wids['e_prefijo'].get_text())
            condicion = (condicion 
                         and cliente.contador.sufijo 
                                == self.wids['e_sufijo'].get_text())
        except:
            pass        
        condicion = condicion and utils.combo_get_value(self.wids['cbe_cuenta']) == cliente.cuentaOrigenID
        condicion = condicion and self.wids['e_porcentaje'].get_text() == "%s %%" % (utils.float2str(cliente.porcentaje * 100))
        condicion = condicion and self.wids['ch_envio_albaran'].get_active() == cliente.enviarCorreoAlbaran
        condicion = condicion and self.wids['ch_envio_factura'].get_active() == cliente.enviarCorreoFactura
        condicion = condicion and self.wids['ch_envio_packing'].get_active() == cliente.enviarCorreoPacking
        condicion = condicion and self.wids['e_riesgoConcedido'].get_text() == utils.float2str(self.objeto.riesgoConcedido)
        condicion = condicion and self.wids['e_riesgoAsegurado'].get_text() == utils.float2str(self.objeto.riesgoAsegurado)
        condicion = condicion and self.wids['sp_copias'].get_value() == cliente.copiasFactura
        condicion = condicion and self.wids['e_fechaNacimiento'].get_text() == utils.str_fecha(cliente.fechaNacimiento)
        condicion = condicion and self.wids['e_fechaAlta'].get_text() == utils.str_fecha(cliente.fechaAlta)
        sexo = utils.combo_get_value(self.wids['cb_sexoMasculino'])
        if sexo == 0:
            sexo = None
        elif sexo == 1:
            sexo = True
        else:
            sexo = False
        condicion = condicion and sexo == cliente.sexoMasculino
        for dia in ("lunes", "martes", "miercoles", "jueves", "viernes", 
                    "sabado", "domingo"):
            valor_dia_ventana = self.wids["ch_%s" % dia].get_active()
            valor_dia_objeto = getattr(self.objeto, dia)
            condicion = condicion and valor_dia_ventana == valor_dia_objeto
        try:
            codigo = int(self.wids['e_codigo'].get_text())
        except (TypeError, ValueError):
            codigo = None
        condicion = condicion and codigo == self.objeto.codigo
        return not condicion    # Concición verifica que sea igual

    def aviso_actualizacion(self):
        """
        Muestra una ventana modal con el mensaje de objeto 
        actualizado.
        """
        utils.dialogo_info('ACTUALIZAR',
                           'El cliente ha sido modificado remotamente.\nDebe actualizar la información mostrada en pantalla.\nPulse el botón «Actualizar»',
                           padre = self.wids['ventana'])
        b_actualizar = self.wids['b_actualizar']
        if b_actualizar != None:
            b_actualizar.set_sensitive(True)

    def inicializar_ventana(self):
        """
        Inicializa los controles de la ventana, estableciendo sus
        valores por defecto, deshabilitando los innecesarios,
        rellenando los combos, formateando el TreeView -si lo hay-...
        """
        # Inicialmente no se muestra NADA. Sólo se le deja al
        # usuario la opción de buscar o crear nuevo.
        self.activar_widgets(False)
        self.wids['b_actualizar'].set_sensitive(False)
        self.wids['b_guardar'].set_sensitive(False)
        self.wids['b_nuevo'].set_sensitive(True)
        self.wids['b_buscar'].set_sensitive(True)
        contadores = []
        for contador in pclases.Contador.select(orderBy = "prefijo"):
            if contador.prefijo == None:
                contador.prefijo = ""
            if contador.sufijo == None:
                contador.sufijo = ""
            contadores.append((contador.id, "%s | %s (Valor actual: %s)" % (
                contador.prefijo, contador.sufijo, contador.get_info())))
        utils.rellenar_lista(self.wids['cmb_contador'], contadores)
        utils.rellenar_lista(self.wids['cbe_cuenta'], 
            [(c.id, "%s: %s %s" % (c.nombre, c.banco, c.ccc)) 
                for c in pclases.CuentaOrigen.select(orderBy = "nombre")])
        cols = (('Banco', 'gobject.TYPE_STRING', 
                    True, True, True, self.cambiar_banco), 
                ('Swif', 'gobject.TYPE_STRING', 
                    True, True, False, self.cambiar_swif), 
                ('Iban', 'gobject.TYPE_STRING', 
                    True, True, False, self.cambiar_iban), 
                ('CCC', 'gobject.TYPE_STRING', 
                    True, True, False, self.cambiar_cuenta), 
                ('Observaciones', 'gobject.TYPE_STRING', 
                    True, True, False, self.cambiar_observaciones), 
                ('IDCuentaBancariaCliente', 'gobject.TYPE_INT64', 
                    False, True, False, None))
        utils.preparar_listview(self.wids['tv_cuentas'], cols)
        self.wids['tv_cuentas'].get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        cols = (('Fecha', 'gobject.TYPE_STRING', 
                    True, True, False, self.cambiar_fecha_padecimiento), 
                ('Dolencia', 'gobject.TYPE_STRING', 
                    True, True, True, self.cambiar_dolencia), 
                ('PUID', 'gobject.TYPE_STRING', 
                    False, True, False, None))
        utils.preparar_listview(self.wids['tv_padecimientos'], cols)
        self.wids['tv_cuentas'].get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        cols = (("Nº. Factura", 'gobject.TYPE_STRING', False,True,True,None), 
                ("Fecha", 'gobject.TYPE_STRING', False, True, False, None), 
                ("Importe", 'gobject.TYPE_STRING', False, True, False, None), 
                ("Vencido", 'gobject.TYPE_STRING', False, True, False, None), 
                ("Cobrado", 'gobject.TYPE_STRING', False, True, False, None), 
                ("Estado", 'gobject.TYPE_STRING', False, True, False, None), 
                ("ID", 'gobject.TYPE_INT64', False, True, False, None))
        utils.preparar_listview(self.wids['tv_pdte'], cols)
        self.wids['tv_pdte'].connect("row-activated", self.abrir_factura)
        getcol = self.wids['tv_pdte'].get_column
        getcol(2).get_cell_renderers()[0].set_property('xalign', 1.0)
        getcol(3).get_cell_renderers()[0].set_property('xalign', 1.0)
        getcol(4).get_cell_renderers()[0].set_property('xalign', 1.0)
        cols = (('Descripción', 'gobject.TYPE_STRING', False,True,True,None), 
                ('# clases', 'gobject.TYPE_INT', False, True, False, None), 
                ('Fecha contratación', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('PUID', 'gobject.TYPE_STRING', False, True, False, None))
        utils.preparar_treeview(self.wids['tv_contratadas'], cols, multi=True)
        self.wids['tv_contratadas'].connect("row-activated", 
                                            self.abrir_producto)
        cols = (('Fecha', 'gobject.TYPE_STRING', False,True,True,None), 
                ('Hora', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Asistencia', 'gobject.TYPE_BOOLEAN', False,True,False,None), 
                ('Producto factura', 'gobject.TYPE_STRING', 
                    False, False, False, None), 
                ('Facturado', 'gobject.TYPE_BOOLEAN', 
                    False, True, False, None),
                ('PUID', 'gobject.TYPE_STRING', False, True, False, None))
        utils.preparar_listview(self.wids['tv_asignadas'], cols)
        cols = (('Descripción', 'gobject.TYPE_STRING', False,True,True,None), 
                ('PUID', 'gobject.TYPE_STRING', False, True, False, None))
        utils.preparar_listview(self.wids['tv_disponibles'], cols)
        utils.rellenar_lista(self.wids['cb_sexoMasculino'], 
            ((0, ""), (1, "Hombre"), (2, "Mujer")))
        cols = (('Nombre', 'gobject.TYPE_STRING', False,True, True, None), 
                ('PUID', 'gobject.TYPE_STRING', False, True, False, None))
        utils.preparar_listview(self.wids['tv_grupos_actuales'], cols)
        self.wids['tv_grupos_actuales'].set_headers_visible(False)
        self.wids['tv_grupos_actuales'].connect("row-activated", 
                                                self.abrir_grupo)
        utils.preparar_listview(self.wids['tv_grupos_anteriores'], cols)
        self.wids['tv_grupos_anteriores'].set_headers_visible(False)
        self.wids['tv_grupos_anteriores'].connect("row-activated", 
                                                  self.abrir_grupo)
        cols = (('Concepto', 'gobject.TYPE_STRING', False,True, True, None), 
                ('Importe', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_importe_nofacturado),
                #('Facturar como', 'gobject.TYPE_STRING', True, True, False, 
                #    self.cambiar_producto_a_facturar),
                ('PUID', 'gobject.TYPE_STRING', False, True, False, None))
        utils.preparar_listview(self.wids['tv_nofacturado'], cols, multi=True)
        self.wids['tv_nofacturado'].connect("row-activated", self.abrir_producto)
        self.formaspago = [i for i in enumerate(pclases.get_formas_de_pago())]
        utils.rellenar_lista(self.wids['cbe_formadepago'], self.formaspago)
        utils.combo_set_from_db(self.wids['cbe_formadepago'], 0)
        self.wids['e_importe'].set_text("0,00")
        cols = (('Número de factura', 'gobject.TYPE_STRING', 
                    False, True, True, None), 
                ('Fecha', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Importe', 'gobject.TYPE_STRING', False, True, False, None), 
                ('PUID', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_facturado'], cols, multi = True)
        self.wids['tv_facturado'].connect("row-activated", self.abrir_factura)
        self.wids['e_fechacobro'].set_text(utils.str_fecha(datetime.date.today()))

    def abrir_grupo(self, tv, path, view_column):
        model = tv.get_model()
        puid = model[path][-1]
        grupo = pclases.getObjetoPUID(puid)
        import grupos_alumnos
        ventanagrupos = grupos_alumnos.GruposAlumnos(grupo)

    def abrir_factura(self, tv, path, view_column):
        model = tv.get_model()
        while model[path].parent:
            path = model[path].parent.path
        id = model[path][-1]
        if isinstance(id, str) and id[0] not in "0123456789":
            fra = pclases.getObjetoPUID(id)
        else:
            fra = pclases.FacturaVenta.get(id)
        import facturas_venta
        ventanafacturas = facturas_venta.FacturasVenta(fra)
        self.rellenar_no_facturado()
        self.rellenar_facturado()

    def abrir_producto(self, tv, path, view_column):
        model = tv.get_model()
        puid = model[path][-1]
        objeto = pclases.getObjetoPUID(puid)
        if isinstance(objeto, pclases.Clase):
            productoContratado = pclases.getObjetoPUID(model[path].parent[-1])
        else:
            productoContratado = objeto
        if isinstance(productoContratado, pclases.Producto):
            producto = productoContratado
        elif isinstance(productoContratado, pclases.ProductoContratado):
            producto = productoContratado.productoCompra
        else:
            return  # Es una clase suelta sin producto.
        import productos_compra
        ventanaprods = productos_compra.ProductosCompra(producto, 
                                                        usuario = self.usuario)

    def abrir_cliente(self, tv, path, view_column):
        """
        Abre el cliente seleccionado en el TreeView en una nueva ventana.
        """
        idcliente = tv.get_model()[path][-1]
        cliente = pclases.Cliente.get(idcliente)
        nueva_ventana = Clientes(cliente)

    def activar_widgets(self, s, chequear_permisos = True):
        """
        Activa o desactiva (sensitive=True/False) todos 
        los widgets de la ventana que dependan del 
        objeto mostrado.
        Entrada: s debe ser True o False. En todo caso
        se evaluará como boolean.
        """
        ws = ('b_borrar','expander1','vbox2','vbox3','vbox4')  
        for w in ws:
            self.wids[w].set_sensitive(s)
        if chequear_permisos:
            self.check_permisos(nombre_fichero_ventana = "clientes.py")

    def ir_a_primero(self):
        """
        Hace que el primer registro -si lo hay- de la tabla implicada
        en el objeto del formulario sea el objeto activo.
        """
        anterior = cliente = self.objeto
        try:
            # Anulo el aviso de actualización del envío que deja de ser activo.
            if cliente != None: cliente.notificador.set_func(lambda : None)
            cliente = pclases.Cliente.select(orderBy = "-id")[0]        # Selecciono todos y me quedo con el primero de la lista
            cliente.notificador.set_func(self.aviso_actualizacion)      # Activo la notificación
        except:
            cliente = None  
        self.objeto = cliente
        self.actualizar_ventana(objeto_anterior = anterior)

    def refinar_resultados_busqueda(self, resultados):
        """
        Muestra en una ventana de resultados todos los
        registros de "resultados".
        Devuelve el id (primera columna de la ventana
        de resultados) de la fila seleccionada o None
        si se canceló.
        """
        filas_res = []
        for r in resultados:
            filas_res.append((r.id, 
                              r.codigo, 
                              r.nombre, 
                              r.cif, 
                              r.get_direccion_completa()))
        idcliente = utils.dialogo_resultado(filas_res,
                                            titulo = 'Seleccione Cliente',
                                            cabeceras = ('ID Interno', 
                                                         'Código', 
                                                         'Nombre', 
                                                         'CIF', 
                                                         'Dirección'), 
                                            padre = self.wids['ventana'])
        if idcliente < 0:
            return None
        else:
            return idcliente

    def escribir_valor(self, widget, valor):
        """
        Con respecto al widget: intenta escribir el valor como si 
        fuera un Entry. Si no lo consigue lo intenta como si fuera
        un TextView.
        En cuanto al valor, lo convierte en cadena antes de escribirlo.
        """
        try:
            widget.set_text(str(valor))
        except AttributeError: # No tiene el set_text, por tanto no es un Entry.
            widget.get_buffer().set_text(valor)

    def leer_valor(self, widget):
        """
        Intenta leer el valor como si fuera un Entry. Si no lo 
        consigue lo hace suponiendo que es un TextView.
        Devuelve el valor leído _como cadena_.
        """
        if isinstance(widget, (gtk.ToggleButton, gtk.CheckButton)):
            res = widget.get_active()
        else:
            try:
                res = widget.get_text()
            except AttributeError:
                try:
                    buffer = widget.get_buffer()
                    res = buffer.get_text(buffer.get_bounds()[0], buffer.get_bounds()[1])
                except AttributeError:
                    res = widget.child.get_text()
        return res

    def deep_refresh(self, boton = None):
        """
        Actualiza todos los datos de la ventana haciendo un "deep refresh" en 
        el objeto y enlaces relacionados.
        """
        self.actualizar_objeto_y_enlaces()

    def rellenar_widgets(self):
        """
        Introduce la información del cliente actual
        en los widgets.
        No se chequea que sea != None, así que
        hay que tener cuidado de no llamar a 
        esta función en ese caso.
        """
        if not self.objeto:
            self.activar_widgets(False)
            return
        cliente = self.objeto
        self.wids['ventana'].set_title("Clientes - %s" % (cliente.nombre))
        self.wids['e_telefono'].set_text(cliente.telefono or '')
        self.wids['e_nombre'].set_text(cliente.nombre or '')
        self.wids['e_cif'].set_text(cliente.cif or '')
        self.wids['e_direccion'].set_text(cliente.direccion or '')
        self.wids['e_pais'].set_text(cliente.pais or '')
        self.wids['e_ciudad'].set_text(cliente.ciudad or '')
        self.wids['e_provincia'].set_text(cliente.provincia or '')
        self.wids['e_cp'].set_text(cliente.cp or '')
        if cliente.iva == None or cliente.iva == '':
            cliente.notificador.desactivar()
            cliente.iva = 0.18
            cliente.sync()
            cliente.notificador.activar(self.aviso_actualizacion)
        self.wids['e_iva'].set_text(utils.float2str(cliente.iva * 100, 0)+' %')
        self.wids['e_nombref'].set_text(cliente.nombref or '')
        self.wids['e_direccionfacturacion'].set_text(
            cliente.direccionfacturacion or '')
        self.wids['e_paisfacturacion'].set_text(cliente.paisfacturacion or '')
        self.wids['e_ciudadfacturacion'].set_text(
            cliente.ciudadfacturacion or '')
        self.wids['e_provinciafacturacion'].set_text(
            cliente.provinciafacturacion or '')
        self.wids['e_cpfacturacion'].set_text(cliente.cpfacturacion or '')
        self.wids['e_email'].set_text(cliente.email or '')
        self.wids['e_contacto'].set_text(cliente.contacto or '')
        #self.wids['e_vencimientos'].set_text(cliente.vencimientos or '')
        self.wids['e_vencimientos'].child.set_text(cliente.vencimientos or '')
        self.wids['e_diadepago'].set_text(cliente.diadepago or '')
        self.wids['e_documentodepago'].set_text(cliente.documentodepago or '')
        self.wids['e_motivo'].set_text(cliente.motivo)
        self.wids['e_inhabilitado'].set_active(cliente.inhabilitado)
        if cliente.contador != None:
            self.wids['e_prefijo'].set_text(cliente.contador.prefijo)
            self.wids['e_sufijo'].set_text(cliente.contador.sufijo)
            utils.combo_set_from_db(self.wids['cmb_contador'], 
                                    cliente.contadorID)
        else:
            self.wids['e_prefijo'].set_text('')
            self.wids['e_sufijo'].set_text('')
            utils.combo_set_from_db(self.wids['cmb_contador'], None)
        if cliente.tarifa != None:
            self.wids['e_tarifa'].set_text(cliente.tarifa.nombre)
        else:
            self.wids['e_tarifa'].set_text('')
        buffer = self.wids['e_observaciones'].get_buffer()
        buffer.set_text(cliente.observaciones)
        utils.combo_set_from_db(self.wids['cbe_cuenta'], 
                                cliente.cuentaOrigenID)
        self.wids['e_porcentaje'].set_text(
            "%s %%" % (utils.float2str(cliente.porcentaje * 100)))
        self.wids['ch_envio_albaran'].set_active(cliente.enviarCorreoAlbaran)
        self.wids['ch_envio_factura'].set_active(cliente.enviarCorreoFactura)
        self.wids['ch_envio_packing'].set_active(cliente.enviarCorreoPacking)
        self.wids['e_packingListConCodigo'].set_active(
            cliente.packingListConCodigo)
        self.wids['e_facturarConAlbaran'].set_active(
            cliente.facturarConAlbaran)
        self.wids['e_fax'].set_text(cliente.fax != None and cliente.fax or '')
        self.wids['hbox_comercial'].set_property("visible", False)
        self.rellenar_cuentas()
        self.rellenar_riesgo_campos_objeto()
        if (self.wids['notebook1'].get_current_page() == 4 
            and not self.wids['ch_ign_concedido'].get_active()):
            self.rellenar_riesgo_campos_calculados()
        self.rellenar_contactos()
        self.wids['sp_copias'].set_value(cliente.copiasFactura)
        self.rellenar_padecimientos()
        self.rellenar_productos()
        if self.wids['notebook1'].get_current_page() == PAGE_COBROS:
            self.rellenar_no_facturado()
            self.rellenar_facturado()
        self.wids['e_fechaNacimiento'].set_text(
            self.objeto.fechaNacimiento 
            and utils.str_fecha(self.objeto.fechaNacimiento) 
            or "")
        self.wids['e_fechaAlta'].set_text(
            self.objeto.fechaAlta
            and utils.str_fecha(self.objeto.fechaAlta) 
            or "")
        utils.combo_set_from_db(self.wids['cb_sexoMasculino'], 
            (self.objeto.sexoMasculino and 1) 
            or (self.objeto.sexoMasculino == False and 2)   
                # None evalúa como False
            or 0)
        # Afote:
        try:
            foto = self.objeto.fotos[-1]
        except IndexError:
            gtkfoto = get_pixbuf(None, maximo = 125)
        else:
            gtkfoto = get_pixbuf(foto, maximo = 125)
        self.wids['i_foto'].set_from_pixbuf(gtkfoto)
        # XXX === Combo productos en clases asignadas.
        opciones = [(p.productoCompra.descripcion, p.productoCompra.get_puid()) 
                    for p in self.objeto.productosContratados]
        utils.cambiar_por_combo(self.wids['tv_asignadas'], 
            3, 
            opciones, 
            pclases.Actividad, 
            "productoCompra", 
            self.wids['ventana'], 
            func_filtro = 
                lambda obj, valor: not obj.esta_facturado_para(self.objeto))
        # XXX
        for dia in ("lunes", "martes", "miercoles", "jueves", "viernes", 
                    "sabado", "domingo"):
            self.wids["ch_%s" % dia].set_active(getattr(self.objeto, dia))
        self.wids['e_profesion'].set_text(self.objeto.profesion)
        self.wids['e_codigo'].set_text(
            self.objeto.codigo and `self.objeto.codigo` or "")
        self.objeto.make_swap()

    def actualizar_pestanna(self, nb, ptr_pag, num_pag):
        if num_pag == PAGE_COBROS:
            self.rellenar_no_facturado()
            self.rellenar_facturado()

    def rellenar_facturado(self):
        model = self.wids['tv_facturado'].get_model()
        model.clear()
        for f in self.objeto.facturasVenta:
            padre = model.append(None, 
                                 (f.numfactura, 
                                  utils.str_fecha(f.fecha), 
                                  utils.float2str(f.calcular_importe_total()), 
                                  f.get_puid()))
            for ldv in f.lineasDeVenta:
                model.append(padre, 
                             (ldv.producto.descripcion, 
                              "", 
                              utils.float2str(ldv.calcular_subtotal(iva=True)),
                              ldv.get_puid()))
            for srv in f.servicios:
                model.append(padre, 
                             (srv.concepto, 
                              "", 
                              utils.float2str(srv.calcular_subtotal(iva=True)),
                              srv.get_puid()))

    def rellenar_no_facturado(self):
        """
        Introduce en el model de productos no facturados todos los 
        productos contratados y no facturados del cliente.
        """
        if pclases.DEBUG:
            antes = time.time()
        # Clases contratadas:
        res = buscar_clases(self.objeto, None, None, 
                            ventana_padre = self.wids['ventana'])
        model = self.wids['tv_nofacturado'].get_model()
        model.clear()
        total = 0.0
        productos = {}  # Para facturar solo una vez cada producto a 
                        # cada cliente.
                        # TO-DO: OJO: Si se deja más de un producto sin 
                        # facturar en el mismo periodo de la consulta, solo se 
                        # va a ver una vez.
        self._actividades_por_producto = res # Aquí voy a guardar las 
            # actividades de cada producto que se va a listar; para que, 
            # a la hora de facturar, sepa qué actividades van a 
            # formar el servicio final.
        for cliente in res:
            if cliente not in productos:
                productos[cliente] = []
            for p in res[cliente]:
                try:
                    descripcion_producto = p.descripcion
                    puid_producto = p.get_puid()
                except AttributeError:
                    descripcion_producto = "Sin producto relacionado "\
                                           "(clases no contratadas)"
                    puid_producto = ""
                nodo = model.append((descripcion_producto, 
                    "0.00",    # FIXME: ¿Una clase suelta y no cuesta un pavo?
                    puid_producto))
                for a in res[cliente][p]:
                    producto = a.get_or_guess_productoCompra()
                    if producto not in productos[cliente]:
                        try:
                            importe = a.get_precio(cliente)
                        except TypeError:
                            importe = 0.0   # Producto es None
                        model[nodo][1] = utils.float2str(
                            utils._float(model[nodo][1]) + importe)
                        total += importe
                        productos[cliente].append(producto)
        if pclases.DEBUG:
            print "clientes.py::rellenar_no_facturado -> %d segundos "\
                  "(%d registros)" % (time.time()-antes, 
                                      self.objeto in res 
                                        and res[self.objeto] 
                                        and len(res[self.objeto])
                                        or 0)

    def rellenar_cuentas(self):
        """
        Introduce las cuentas bancarias del cliente en el ListView
        """
        if self.objeto != None:
            model = self.wids['tv_cuentas'].get_model()
            model.clear()
            cuentas = self.objeto.cuentasBancariasCliente[:]
            cuentas.sort(lambda c1, c2: (c1.id < c2.id and -1) or (c1.id > c2.id and 1) or 0)
            for c in cuentas:
                model.append((c.banco, c.swif, c.iban, c.cuenta, c.observaciones, c.id))

    def add_cuenta(self, boton):
        """
        Crea una nueva cuenta asociada con el cliente.
        """
        if self.objeto != None:
            c = pclases.CuentaBancariaCliente(clienteID = self.objeto.id, 
                                              banco = "Nueva cuenta bancaria", 
                                              observaciones = "Introduzca la información de la cuenta.")
            self.rellenar_cuentas()

    def drop_cuenta(self, boton):
        """
        Elimina la(s) cuenta(s) seleccionadas.
        """
        model, paths = self.wids['tv_cuentas'].get_selection().get_selected_rows()
        if  paths != None and paths != [] and utils.dialogo(titulo = "¿BORRAR CUENTAS SELECCIONADAS?", 
                                                            texto = "¿Está seguro de que desea eliminar las cuentas seleccionadas?", 
                                                            padre = self.wids['ventana']):
            for path in paths:
                id = model[path][-1]
                c = pclases.CuentaBancariaCliente.get(id)
                try:
                    c.destroySelf()
                except:
                    txt = """
                    La cuenta está implicada en operaciones, cobro de 
                    recibos, etc.
                    ¿Desea eliminar la cuenta y todas estas operaciones?
                    
                    NOTA: Los borrados masivos en cascada no son aconsejables.
                          Si no está completamente seguro, responda «No» y 
                          cambie la cuenta por otra allí donde aparezca antes 
                          de volver a intentar eliminarla.
                    """
                    if utils.dialogo(titulo = "ERROR: CUENTA USADA", 
                                     texto = txt, 
                                     padre = self.wids['ventana']):
                        #for r in c.recibos:
                        #    r.cuentaBancariaCliente = None
                        c.destroy_en_cascada()
            self.rellenar_cuentas()

    # --------------- Manejadores de eventos ----------------------------
    def cambiar_banco(self, cell, path, text):
        """
        Cambia el banco de la cuentaBancariaCliente.
        """
        model = self.wids['tv_cuentas'].get_model()
        id = model[path][-1]
        c = pclases.CuentaBancariaCliente.get(id)
        c.banco = text
        self.rellenar_cuentas()

    def cambiar_swif(self, cell, path, text):
        """
        Cambia el SWIF de la cuentaBancariaCliente.
        """
        model = self.wids['tv_cuentas'].get_model()
        id = model[path][-1]
        c = pclases.CuentaBancariaCliente.get(id)
        c.swif = text
        self.rellenar_cuentas()

    def cambiar_iban(self, cell, path, text):
        """
        Cambia el IBAN de la cuentaBancariaCliente.
        """
        model = self.wids['tv_cuentas'].get_model()
        id = model[path][-1]
        c = pclases.CuentaBancariaCliente.get(id)
        c.iban = text
        self.rellenar_cuentas()

    def cambiar_cuenta(self, cell, path, text):
        """
        Cambia la cuenta de la cuentaBancariaCliente.
        """
        model = self.wids['tv_cuentas'].get_model()
        id = model[path][-1]
        c = pclases.CuentaBancariaCliente.get(id)
        c.cuenta = text
        self.rellenar_cuentas()

    def cambiar_observaciones(self, cell, path, text):
        """
        Cambia las observaciones de la cuentaBancariaCliente.
        """
        model = self.wids['tv_cuentas'].get_model()
        id = model[path][-1]
        c = pclases.CuentaBancariaCliente.get(id)
        c.observaciones = text
        self.rellenar_cuentas()


    def crear_nuevo_cliente(self, widget):
        """
        Función callback del botón b_nuevo.
        Pide los datos básicos para crear un nuevo objeto.
        Una vez insertado en la BD hay que hacerlo activo
        en la ventana para que puedan ser editados el resto
        de campos que no se hayan pedido aquí.
        """
        anterior = cliente = self.objeto
        nombre = utils.dialogo_entrada(
                    texto = 'Introduzca el nombre del cliente:', 
                    titulo = 'NOMBRE', 
                    padre = self.wids['ventana'])
        if nombre != None:
            if cliente != None:
                cliente.notificador.set_func(lambda : None)
            tarifa_por_defecto = pclases.Tarifa.get_tarifa_defecto()
            contador_defecto = pclases.Contador.get_contador_por_defecto()
            self.objeto = pclases.Cliente(nombre = nombre,
                                          tarifa = tarifa_por_defecto,
                                          contador = contador_defecto,
                                          telefono = '',
                                          cif = 'PENDIENTE',
                                          direccion = '',
                                          pais = '',
                                          ciudad = '',
                                          provincia = '',
                                          cp = '',
                                          vencimientos = '0',
                                          iva = 0.18,
                                          direccionfacturacion = '',
                                          nombref = '',
                                          paisfacturacion = '',
                                          ciudadfacturacion = '',
                                          provinciafacturacion = '',
                                          cpfacturacion = '',
                                          email = '',
                                          contacto = '',
                                          observaciones = '',
                                          documentodepago = 'EFECTIVO',
                                          diadepago = '',
                                          formadepago = 'EFECTIVO',
                                          inhabilitado = False, 
                                          porcentaje = 0.0, 
                                          enviarCorreoAlbaran = False, 
                                          enviarCorreoFactura = False, 
                                          enviarCorreoPacking = False, 
                                          fax = '', 
                                          packingListConCodigo = False, 
                                          facturarConAlbaran = True, 
                                          lunes = True, 
                                          martes = True, 
                                          miercoles = True, 
                                          jueves = True, 
                                          viernes = True, 
                                          sabado = True, 
                                          domingo = True, 
                                          profesion = "", 
                                          codigo = None)
            self._objetoreciencreado = self.objeto
            self.objeto.notificador.set_func(self.aviso_actualizacion)
            self.actualizar_ventana(objeto_anterior = anterior)
            utils.dialogo_info(titulo = 'CLIENTE CREADO', 
                texto = 'Inserte el resto de la información del cliente.', 
                padre = self.wids['ventana'])

    def buscar_cliente(self, widget):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        anterior = cliente = self.objeto
        a_buscar = utils.dialogo_entrada(titulo = "BUSCAR CLIENTE", texto = "Introduzca nombre o CIF del cliente:", padre = self.wids['ventana']) 
        if a_buscar != None:
            criterio = pclases.OR(pclases.Cliente.q.nombre.contains(a_buscar),
                                  pclases.Cliente.q.cif.contains(a_buscar))
            try:
                a_buscar = int(a_buscar)
            except (ValueError, TypeError):
                pass
            else:
                criterio = pclases.OR(criterio, 
                                      pclases.Cliente.q.codigo == a_buscar)
            resultados = pclases.Cliente.select(criterio) 
            if resultados.count() > 1:
                ## Refinar los resultados
                idcliente = self.refinar_resultados_busqueda(resultados)
                if idcliente == None:
                    return
                resultados = [pclases.Cliente.get(idcliente)]
            elif resultados.count() < 1:
                ## Sin resultados de búsqueda
                utils.dialogo_info('SIN RESULTADOS', 
                                   'La búsqueda no produjo resultados.\nPruebe a cambiar el texto buscado o déjelo en blanco para ver una lista completa.\n(Atención: Ver la lista completa puede resultar lento si el número de elementos es muy alto)', 
                                   padre = self.wids['ventana'])
                return
            ## Un único resultado
            # Primero anulo la función de actualización
            if cliente != None:
                cliente.notificador.set_func(lambda : None)
            # Pongo el objeto como actual
            cliente = resultados[0]
            # Y activo la función de notificación:
            cliente.notificador.set_func(self.aviso_actualizacion)
            self.objeto = cliente
            self.actualizar_ventana(objeto_anterior = anterior)

    def guardar(self, widget = None):
        """
        Guarda el contenido de los entry y demás widgets de entrada
        de datos en el objeto y lo sincroniza con la BD.
        """
        cliente = self.objeto
        bakcif = cliente.cif
        # Si no tiene dirección de facturación se copia la postal.
        copiar = True
        for wpostal, wfacturacion in (
            (self.wids['e_direccion'], self.wids['e_direccionfacturacion']), 
            (self.wids['e_nombre'], self.wids['e_nombref']), 
            (self.wids['e_pais'], self.wids['e_paisfacturacion']),
            (self.wids['e_provincia'], self.wids['e_provinciafacturacion']),
            (self.wids['e_ciudad'], self.wids['e_ciudadfacturacion']),
            (self.wids['e_cp'], self.wids['e_cpfacturacion'])):
            copiar = copiar and (
                wfacturacion.get_text() == "" 
                or wfacturacion.get_text() == None)
        if copiar:
            for wpostal, wfacturacion in (
                (self.wids['e_direccion'], self.wids['e_direccionfacturacion']),
                (self.wids['e_nombre'], self.wids['e_nombref']), 
                (self.wids['e_pais'], self.wids['e_paisfacturacion']),
                (self.wids['e_provincia'], self.wids['e_provinciafacturacion']),
                (self.wids['e_ciudad'], self.wids['e_ciudadfacturacion']),
                (self.wids['e_cp'], self.wids['e_cpfacturacion'])):
                wfacturacion.set_text(wpostal.get_text())
        datos = {}
        for c in [c.name for c in cliente.sqlmeta.columnList
                  if c.name != 'tarifaID' 
                      and c.name != 'contadorID' 
                      and c.name != 'formadepago' 
                      and c.name != "clienteID" 
                      and c.name != "porcentaje" 
                      and c.name != "enviarCorreoAlbaran" 
                      and c.name != "enviarCorreoFactura" 
                      and c.name != "enviarCorreoPacking" 
                      and c.name != "proveedorID" 
                      and c.name != "cuentaOrigenID"
                      and c.name != "copiasFactura" 
                      and c.name != "sexoMasculino" 
                      and c.name != "fechaNacimiento" 
                      and c.name != "fechaAlta"
                      and c.name != "lunes"
                      and c.name != "martes"
                      and c.name != "miercoles"
                      and c.name != "jueves"
                      and c.name != "viernes"
                      and c.name != "sabado"
                      and c.name != "domingo" 
                      and c.name != "codigo"]: 
                      # Omito columna tarifa
            datos[c] = self.leer_valor(self.wids['e_%s' % c])
        # Desactivo el notificador momentáneamente
        cliente.notificador.set_func(lambda: None)
        # Actualizo los datos del objeto
        for c in datos:
            # OJO: Hay que tener cuidado con los campos numéricos:
            if c == 'iva':
                try:
                    ivaparseado = utils.parse_porcentaje(datos[c], 
                                                         fraccion = True)
                    cliente.set(iva = ivaparseado)
                except:
                    self.logger.warning("clientes.py-> El IVA no se pudo conv"
                                      "ertir a entero. Pongo IVA por defecto.")
                    cliente.set(iva = 0.18)
            elif c == "riesgoConcedido":
                try:
                    cliente.riesgoConcedido = utils._float(datos[c])
                except (ValueError, TypeError):
                    cliente.riesgoCondedido = -1
            elif c == "riesgoAsegurado":
                try:
                    cliente.riesgoAsegurado = utils._float(datos[c])
                except (ValueError, TypeError):
                    cliente.riesgoAsegurado = -1
            else:
                setattr(cliente, c, datos[c])
                # eval('cliente.set(%s = "%s")' % (c, datos[c]))
        # CWT: Chequeo que tenga CIF, y si no lo tiene, lo pido por 
        #      diálogo ad eternum.
        while utils.parse_cif(cliente.cif) == "":
            cliente.cif = utils.dialogo_entrada(texto = "El CIF del cliente "
                            "no puede estar en blanco ni tener el valor «%s»"
                            ".\nEs un campo obligatorio.\nIntroduzca un CIF c"
                            "orrecto:" % cliente.cif,
                            titulo = "CIF",
                            padre = self.wids['ventana'])
            if cliente.cif == None:
                cliente.cif = bakcif
                break
        if cliente.cif != bakcif:
            cliente.cif = utils.parse_cif(cliente.cif)
        # formadepago ya no se muestra en ventana, pero es posible que se 
        # use en algún sitio, así que lo igualo a vencimientos,
        # que es el campo que ha unificado los dos Entries originales:
        cliente.formadepago = cliente.vencimientos

        #cliente.clienteID = utils.combo_get_value(self.wids['cbe_comercial'])
        #cliente.proveedorID = utils.combo_get_value(self.wids['cbe_proveedor'])
        cliente.cuentaOrigenID = utils.combo_get_value(self.wids['cbe_cuenta'])
        try:
            cliente.porcentaje = utils.parse_porcentaje(
                self.wids['e_porcentaje'].get_text(), 
                fraccion = True)
        except ValueError:
            cliente.porcentaje = 0
        cliente.enviarCorreoAlbaran = self.wids['ch_envio_albaran'].get_active()
        cliente.enviarCorreoFactura = self.wids['ch_envio_factura'].get_active()
        cliente.enviarCorreoPacking = self.wids['ch_envio_packing'].get_active()
        try:
            copias = int(self.wids['sp_copias'].get_value())
        except (ValueError, TypeError):
            copias = 0
        cliente.copiasFactura = copias 
        sexo = utils.combo_get_value(self.wids['cb_sexoMasculino'])
        if sexo == 0:
            sexo = None
        elif sexo == 1:
            sexo = True
        else:
            sexo = False
        cliente.sexoMasculino = sexo 
        try:
            cliente.fechaAlta = utils.parse_fecha(
                self.wids['e_fechaAlta'].get_text())
        except ValueError:
            pass    # Mala fecha, vuelvo a la que tenía guardada antes.
        try:
            cliente.fechaNacimiento = utils.parse_fecha(
                self.wids['e_fechaNacimiento'].get_text())
        except (ValueError, TypeError):
            pass    # Mala fecha, vuelvo a la que tenía guardada antes.
        for dia in ("lunes", "martes", "miercoles", "jueves", "viernes", 
                    "sabado", "domingo"):
            setattr(self.objeto, dia, self.wids["ch_%s" % dia].get_active())
        try:
            codigo = int(self.wids['e_codigo'].get_text())
        except (TypeError, ValueError):
            codigo = None
        try:
            self.objeto.codigo = codigo
        except:     # IntegrityError
            dar_error_codigo = True
        else:
            dar_error_codigo = False
        # Fuerzo la actualización de la BD y no espero a que SQLObject lo 
        # haga por mí:
        cliente.syncUpdate()
        # Vuelvo a activar el notificador
        cliente.notificador.set_func(self.aviso_actualizacion)
        self.actualizar_ventana()
        self.wids['b_guardar'].set_sensitive(False)
        if cliente.es_extranjero() and cliente.iva != 0:
            utils.dialogo_info(titulo = "ADVERTENCIA", 
                texto="El IVA para los clientes extranjeros debería ser 0 %.", 
                padre = self.wids['ventana'])
        if dar_error_codigo:
            utils.dialogo_info(titulo = "ERROR CÓDIGO CLIENTE", 
                texto = "El código %s ya existe." 
                    % self.wids['e_codigo'].get_text(), 
                padre = self.wids['ventana'])

    def borrar(self, widget):
        """
        Elimina el cliente en pantalla.
        """
        cliente = self.objeto
        if cliente != None:
            if utils.dialogo('¿Está seguro de eliminar el cliente actual?', 'BORRAR CLIENTE'):
                cliente.notificador.set_func(lambda : None)
                try:
                    cliente.destroySelf()
                    self.ir_a_primero()
                except:
                    txt = """
                    El cliente no se eliminó por tener pedidos relacionados.     
                    Si desea eliminarlo, borre antes los pedidos asignados      
                    al cliente.
                    Los pedidos relacionados son: 
                    """
                    for p in cliente.pedidosVenta:
                        txt += "Pedido número %s. Fecha %s.\n" % (p.numpedido, p.fecha.strftime('%d/%m/%y'))
                    utils.dialogo_info(titulo = 'ERROR: NO SE PUDO BORRAR',
                                       texto = txt, 
                                       padre = self.wids['ventana'])

    def _ver_pedidos(self, boton):
        """
        Muestra todos los pedidos asignados
        al cliente actual.
        """
        cliente = self.objeto
        if cliente == None: return
        pedidosventa = pclases.PedidoVenta.select(
                        pclases.PedidoVenta.q.clienteID == cliente.id, 
                        orderBy = "fecha")
        pedidos = [(p.id, p.numpedido, utils.str_fecha(p.fecha)) 
                   for p in pedidosventa]
        idpedido = utils.dialogo_resultado(pedidos, 
                                           'PEDIDOS HECHOS POR EL CLIENTE',
                                           cabeceras = ('ID', 
                                                        'Número de pedido', 
                                                        'Fecha'), 
                                           padre = self.wids['ventana'], 
                                           func_change = self.abrir_pedido)
        if idpedido > 0:
            import pedidos_de_venta
            p = pedidos_de_venta.PedidosDeVenta(pclases.PedidoVenta.get(idpedido), usuario = self.usuario)
    
    def ver_pedidos(self, boton):
        """
        Nuevo ver pedidos. Sustituye al diálogo resultado que se abría antes.
        Ahora se abre la consulta adecuada con el cliente de la ventana.
        CWT
        """
        import consulta_pedidos_clientes
        ventana = consulta_pedidos_clientes.ConsultaPedidosCliente(
                    usuario = self.usuario, 
                    objeto = self.objeto)

    def ver_presupuestos(self, boton):
        """
        Muestra todos los presupuestos hechos 
        al cliente actual.
        """
        cliente = self.objeto
        if cliente == None:
            return
        presupuestos = [(p.id, utils.str_fecha(p.fecha), p.nombrecliente, p.personaContacto, ", ".join([pedido.numpedido for pedido in p.get_pedidos()])) for p in cliente.presupuestos]
        idpresupuesto = utils.dialogo_resultado(presupuestos, 
                                                'OFERTAS HECHAS AL CLIENTE %s' % (cliente.nombre),
                                                cabeceras = ('ID', 'Fecha', "Cliente final", "Contacto", "Pedidos relacionados"), 
                                                padre = self.wids['ventana'])
        if idpresupuesto > 0:
            import presupuestos
            p = presupuestos.Presupuestos(objeto = pclases.Presupuesto.get(idpresupuesto), usuario = self.usuario)
        
    def ver_productos(self, boton):
        import consulta_productos_comprados
        ventana = consulta_productos_comprados.ConsultaProductosComprados(
                    usuario = self.usuario, 
                    objeto = self.objeto)

    def _ver_productos(self, boton):
        """
        Muestra todos los productos relacionados
        con el cliente actual a través de las
        Facturas<->LDV<->Artículos.
        """
        cliente = self.objeto
        if cliente == None: return
        productos = {}
        #for pedido in cliente.pedidosVenta:
        for factura in cliente.facturasVenta:
            for ldv in factura.lineasDeVenta:
                producto = ldv.producto
                if ldv.productoVenta != None:
                    linea_producto = ["PV:%d" % (ldv.productoVenta.id), 
                                      ldv.productoVenta.codigo, 
                                      ldv.productoVenta.descripcion, 
                                      ldv.cantidad]
                elif ldv.productoCompra != None:
                    linea_producto = ["PC:%d" % (ldv.productoCompra.id), 
                                      ldv.productoCompra.codigo, 
                                      ldv.productoCompra.descripcion, 
                                      ldv.cantidad]
                else:
                    continue
                if not producto in productos:
                    productos[producto] = linea_producto
                else:
                    productos[producto][-1] += linea_producto[-1]
        productos = [tuple(productos[p][:-1]) + ("%s %s" % (
                        utils.float2str(productos[p][-1], autodec = True), 
                        p.unidad),)
                     for p in productos]
        idproducto = utils.dialogo_resultado(productos, 
                        'PRODUCTOS COMPRADOS POR EL CLIENTE',
                        cabeceras=('ID', 'Código', 'Descripción', "Facturado"), 
                        padre = self.wids['ventana'])
        if idproducto not in (-1, -2):
            if "PV" in idproducto:
                producto = pclases.ProductoVenta.get(idproducto.split(":")[1])
                if producto.es_rollo():
                    import productos_de_venta_rollos
                    ventana_producto = productos_de_venta_rollos.ProductosDeVentaRollos(producto, usuario = self.usuario)
                elif producto.es_bala() or producto.es_bigbag():
                    import productos_de_venta_balas
                    ventana_producto = productos_de_venta_balas.ProductosDeVentaBalas(producto, usuario = self.usuario)
            elif "PC" in idproducto:
                producto = pclases.ProductoCompra.get(idproducto.split(":")[1])
                import productos_compra
                ventana_producto = productos_compra.ProductosCompra(producto, usuario = self.usuario)

    def crear_nuevo_contador(self,boton):
        """
        Crea un nuevo contador y lo asocia al cliente actual
        """
        prefijo = utils.dialogo_entrada(titulo = 'PREFIJO', 
                    texto = 'Introduzca el prefijo para el contador', 
                    padre = self.wids['ventana'])
        sufijo = utils.dialogo_entrada(titulo = 'SUFIJO', 
                    texto = 'Introduzca el sufijo para el contador', 
                    padre = self.wids['ventana'])
        if prefijo != None and sufijo != None:
            contador = pclases.Contador(contador = 0, prefijo = prefijo, 
                                        sufijo = sufijo)
        else:
            return
        cliente = self.objeto
        cliente.notificador.set_func(lambda: None)
        cliente.contador = contador
        cliente.syncUpdate()
        # Vuelvo a activar el notificador
        cliente.notificador.set_func(self.aviso_actualizacion)
        self.actualizar_ventana(objeto_anterior = cliente)
        self.wids['cmb_contador'].clear()
        utils.rellenar_lista(self.wids['cmb_contador'], 
            [(c.id, 'Prefijo:'+c.prefijo +' |Sufijo:'+c.sufijo) 
             for c in pclases.Contador.select(orderBy="prefijo")])

    def seleccionar_contador(self, wid):
        """
        Asigna el contador seleccionado mediante el combo al cliente
        """
        # DONE: Hacer que si tenía ya un contador seleccionado, se actualicen 
        # todas sus facturas cambiando (si es posible) el prefijo y sufijo del antiguo por el nuevo.
        idcontador = utils.combo_get_value(wid)
        if idcontador != None:
            contador = pclases.Contador.get(idcontador)
            cliente = self.objeto
            contador_antiguo = cliente.contador
            cliente.notificador.set_func(lambda : None)
            if self.wids['b_guardar'].get_property("sensitive") == True:
                self.guardar()
            cliente.contador = contador
            cliente.syncUpdate()
            # for fra in cliente.facturasVenta:
            #     numfactura = fra.numfactura
            #     numfactura = numfactura.replace(contador_antiguo.prefijo, '')
            #     numfactura = numfactura.replace(contador_antiguo.sufijo, '')
            #     numfactura = "%s%s%s" % (contador.prefijo, numfactura, contador.sufijo)
            #     fra.numfactura = numfactura
            cliente.notificador.set_func(self.aviso_actualizacion)
            # self.actualizar_ventana(objeto_anterior = cliente)    # XXX: Temporalmente, hasta que pruebe al 100% esa parte del actualizar_ventana (ver ventana.py)
            if contador_antiguo != contador:
                self.actualizar_ventana()

    def asignar_tarifa(self,wid):
        """
        Muestra las tarifas registradas en el sistema y 
        permite asignársela a un cliente
        """
        tarifas = pclases.Tarifa.select()
        ops = []
        for t in tarifas:
            ops.append((t.id,t.nombre))
        if ops == []:
            utils.dialogo_info(titulo = 'ERROR', 
                texto = 'No hay tarifas registradas en el sistema', 
                padre = self.wids['ventana'])
            return
        self.objeto.tarifa = utils.dialogo_combo(titulo = 'Seleccione tarifa', 
            ops = ops, 
            padre = self.wids['ventana'])
        self.actualizar_ventana()
        
    def exportar_telefonos(self, boton):
        """
        Exporta los teléfonos de todos los clientes a un CSV para poder enviar 
        SMS masivos desde un programa de terceros.
        """
        saltar_fijos = utils.dialogo(titulo = "¿FILTRAR FIJOS?", 
            texto = "¿Desea exportar solo números de teléfono móvil?", 
            padre = self.wids['ventana'])
        import csv, tempfile, os, random
        nomarchivo = os.path.join(tempfile.gettempdir(), "phones_%s.csv" % (
            `random.random()`.replace(".", "")))
        archivo = open(nomarchivo, "w")
        # Formato "excel" por defecto:
        escritor = csv.writer(archivo, delimiter = ";", lineterminator = "\n")
        for c in pclases.Cliente.select(
            pclases.NOT(pclases.Cliente.q.inhabilitado)):
            if c.telefono.strip():
                if c.telefono.strip().startswith('9') and saltar_fijos:
                    continue
                escritor.writerow([c.nombre.strip(), c.telefono.strip()])
        archivo.close()
        abrir_csv(archivo.name)


def exportar_correos(boton):
    """
    Exporta los correos electrónicos de todos los clientes a un CSV.
    """
    import csv, tempfile, os, random
    nomarchivo = os.path.join(tempfile.gettempdir(), "emails_%s.csv" % (
        `random.random()`.replace(".", "")))
    archivo = open(nomarchivo, "w")
    # Formato "excel" por defecto:
    escritor = csv.writer(archivo, delimiter = ";", lineterminator = "\n")
    for c in pclases.Cliente.select(
        pclases.NOT(pclases.Cliente.q.inhabilitado)):
        if c.email.strip():
            escritor.writerow(c.email.strip())
    archivo.close()
    abrir_csv(archivo.name)

def get_pixbuf(foto, maximo = None):
#def get_gtkimage(foto, maximo = None):
    """
    Devuelve una GtkImage de la foto del empleado o de la foto por 
    defecto si no tiene.
    Si maximo != None reescala la imagen para que ninguna de sus dos 
    dimensiones supere esa cantidad
    """
    if foto and foto.data:
        impil = foto.to_pil()
    else:
        from PIL import Image
        impil = Image.open(os.path.join("..", "imagenes", "users.png"))
    ancho, alto = impil.size
    escala = (float(maximo) / max(ancho, alto))
    impil = impil.resize((int(ancho * escala), 
                          int(alto * escala)), 
                          resample = 1)
    pixbuf = utils.image2pixbuf(impil)
    #gtkimage = gtk.Image()
    #gtkimage.set_from_pixbuf(pixbuf)
    #return gtkimage
    return pixbuf


if __name__ == '__main__':
    try:
        v = Clientes(
                usuario = pclases.Usuario.selectBy(usuario = "enrique")[0])
    except:
        v = Clientes()

