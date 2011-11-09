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
## tpv.py - Ventana de Terminal Punto de Venta.
###################################################################
## TODO:
## ¿Necesito en la ventana de buscar ticket una opción para 
## borrarlo, modificarlo o pasarlo a la ventana de TPV principal?
## No sé si faltaría un desplegable para elegir el almacén del que 
## descontar existencias. No se va a usar de momento el TPV más 
## que para el almacén principal, pero no descartaría la opción 
## de momento.
###################################################################

try:
    import psyco
    psyco.full()
except ImportError:
    pass

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time
try:
    import pclases
except ImportError:
    import sys
    from os.path import join as pathjoin; sys.path.append(pathjoin("..", "framework"))
    import pclases
import datetime
try:
    import geninformes
except ImportError:
    import sys
    sys.path.append('../informes')
    import geninformes
import pango
import gobject
from facturas_venta import debe_generar_recibo, generar_recibo

def intentar_imprimir_ticket(ticket):
    """
    Intenta imprimir un ticket por la impresota de tickets. Si no puede, 
    abre un fichero de texto plano con el contenido.
    """
    try:
        imprimir_ticket(ticket)
    except Exception, msg:
        utils.dialogo_info(titulo = "ERROR IMPRESORA", 
                           texto = "Ocurrió un error al acceder a la impresora de tickets.\nEl ticket se mostrará como fichero de texto plano.\n\nInformación de depuración:\n%s" % msg)
        import tempfile, os
        fdest = os.path.join(tempfile.gettempdir(), 
                             "ticket_%d.txt" % ticket.numticket)
        dest = file(fdest, "w")
        volcar_texto_ticket(ticket, dest)
        dest.close()
        import multi_open
        multi_open.open(fdest)

def volcar_texto_ticket(ticket, dest):
    """
    Vuelca el texto que se imprimiría por ticketera en el fichero «fdest».
    """
    try:
        dde = pclases.DatosDeLaEmpresa.select()[0]
    except IndexError:
        print "tpv::imprimir_ticket -> No se encontraron los datos de la empresa. Abortando impresión..."
    else:
        ANCHO = pclases.config.get_anchoticket()
        linea0 = (" ", "RS")
        linea1 = (dde.nombre.center(ANCHO), "RSC")
        modo = "RC"
        if pclases.config.get_mostrarcontactoenticket():
            linea2 = (dde.nombreContacto.center(ANCHO), modo)
        else:
            linea2 = ("", "")
        linea3 = (("NIF %s" % (dde.cif)).center(ANCHO), modo)
        linea4 = (("%s. Tlf: %s" % (dde.direccion, dde.telefono)).center(ANCHO), modo)
        linea5 = ("", [])
        lineas = [linea1, linea2, linea3, linea4, linea5]
        lineas.append((("Ticket %d - %s %s" % (ticket.numticket, 
                                               utils.str_fecha(ticket.fechahora), 
                                               utils.str_hora(ticket.fechahora))).center(ANCHO), "SI"))
        for ldv in ticket.lineasDeVenta:
            lineas.append((cortar_linea_ticket(ldv, ANCHO, "\n"), ">"))
        lineas.append((total_ticket(ticket, ANCHO), "A"))
        lineas.append(("\nIVA incluido - Gracias por su visita", ""))
        dest.writelines(l[0]+"\n" for l in lineas)

def ventana_ticket(ticket, usuario, padre = None):
    """
    Muestra una ventana con la información del ticket recibido y los botones de 
    facturar e imprimir.
    """
    v = Ventana("ticket.glade", ticket, usuario = usuario)
    v.add_connections({"b_salir/clicked": v.salir,
                       "b_imprimir/clicked": 
                            lambda boton: intentar_imprimir_ticket(ticket), 
                       }) 
    v.wids['ventana'].set_transient_for(padre)
    v.wids['ventana'].show_all()
    v.wids['b_facturar'].set_property("visible", False) # TODO: Cuando haga falta, lo implementaré.
    v.wids['ventana'].set_title("TICKET %d" % ticket.numticket)
    v.wids['ventana'].resize(640, 480)
    cols = (('Venta', 'gobject.TYPE_STRING', False, True, True, None),
            ('Código', 'gobject.TYPE_STRING', False, True, False, None),
            ('Producto', 'gobject.TYPE_STRING', False, True, False, None),
            ('P.V.P.', 'gobject.TYPE_STRING', False, True, False, None),
            ('Cantidad', 'gobject.TYPE_STRING', False, True, False, None),
            ('Total', 'gobject.TYPE_STRING', False, True, False, None),
            ('Factura', 'gobject.TYPE_STRING', False, True, False, None),
            ('IDLDV', 'gobject.TYPE_INT64', False, False, False, None))
    utils.preparar_treeview(v.wids['tv_ldvs'], cols)
    model = v.wids["tv_ldvs"].get_model()
    model.clear()
    totalticket = 0.0
    padre = model.append(None, (ticket.numticket, 
                                utils.str_fecha(ticket.fechahora), 
                                utils.str_hora(ticket.fechahora),
                                "", 
                                "", 
                                #"%s €" % (utils.float2str(
                                #    totalticket)), 
                                "", 
                                ", ".join([fra.numfactura for fra 
                                            in ticket.get_facturas()]), 
                                ticket.id))
    for ldv in ticket.lineasDeVenta:
        descripcion = ldv.producto.descripcion
        if len(descripcion) > 30:
            descripcion = utils.wrap(descripcion, 30)
        totalldv = ldv.get_subtotal(iva = False) * 1.18
        model.append(padre, 
                      ("", 
                       ldv.producto.codigo, 
                       descripcion, 
                       "%s €" % (utils.float2str(ldv.precio * 1.18)),
                        # P.V.P. lleva 18% de IVA.
                       "%s" % utils.float2str(ldv.cantidad), 
                       "%s €" % utils.float2str(totalldv),
                        # Ventas de ticket llevan 18% de IVA. 
                        # Lo calculo aquí porque la 
                        # función toma el IVA en función del 
                        # cliente del pedido/albarán/factura.
                       ldv.get_factura_o_prefactura() 
                        and ldv.get_factura_o_prefactura().numfactura 
                        or "", 
                       ldv.id))
        totalticket += totalldv
    model[padre][5] = "%s €" % utils.float2str(totalticket)
    v.wids['tv_ldvs'].expand_all()
    gtk.main()

class TPV(Ventana):

    DIAS_TREEVIEW = pclases.config.get_diastpv()

    def __init__(self, objeto = None, usuario = None):
        self.usuario = usuario
        Ventana.__init__(self, 'tpv.glade', objeto, usuario = self.usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_articulo/clicked': self.add_ldv, 
                       'b_venta/clicked': self.cerrar_venta, 
                       'b_drop_venta/clicked': self.borrar_venta, 
                       'b_facturar/clicked': self.facturar, 
                       'b_actualizar/clicked': self.actualizar_ventana, 
                       'b_cajon/clicked': self.abrir_cajon, 
                       'b_buscarticket/clicked': self.buscar_ticket, 
                       'b_arqueo/clicked': self.arqueo
                      }
        self.add_connections(connections)
        self.inicializar_ventana()
        #import thread
        #gtk.gdk.threads_init()
        #thread.start_new_thread(gtk.main, ())
        # https://arco.inf-cr.uclm.es/pipermail/python/2005-January/000105.html
        gtk.main()

    def buscar_ticket(self, boton):
        """
        Busca un ticket por número o fecha y muestra una ventana desde la que 
        se puede imprimir o facturar el ticket. No se permite eliminarlo ni 
        editarlo, ya que modificaría el arqueo de caja del día al que pertenece.
        Si fuera un ticket actual, el usuario puede editarlo desde el propio TPV, 
        así que no tiene por qué recurrir a esta ventana para ello.
        """
        ticket_o_fecha = utils.dialogo_entrada(
            titulo = "TPV: BUSCAR TICKET", 
            texto = "Introduzca número de ticket o fecha en formato dd/mm/aaaa:", 
            padre = self.wids['ventana'])
        if ticket_o_fecha:
            try:
                fecha = utils.parse_fecha(ticket_o_fecha)
                tickets = pclases.Ticket.select(pclases.AND(
                    pclases.Ticket.q.fechahora >= fecha, 
                    pclases.Ticket.q.fechahora 
                        < fecha + datetime.timedelta(days = 1)))
            except ValueError:
                tickets = pclases.Ticket.select(
                    pclases.Ticket.q.numticket == ticket_o_fecha)
            if tickets.count() > 0:
                resultados = [(t.id, 
                               t.numticket, 
                               utils.str_fechahora(t.fechahora), 
                               utils.float2str(t.calcular_total(iva_incluido = True)), 
                               len(t.lineasDeVenta)) for t in tickets]
                ticket = utils.dialogo_resultado(resultados, 
                                                 "Seleccione un ticket:", 
                                                 multi = False, 
                                                 padre = self.wids['ventana'], 
                                                 cabeceras = ("ID", 
                                                              "Número", 
                                                              "Fecha y hora", 
                                                              "Total", 
                                                              "Líneas"))
                if ticket:
                    ticket = pclases.Ticket.get(ticket)
                    ventana_ticket(ticket, 
                                   self.usuario, 
                                   padre = self.wids['ventana'])
            else:
                utils.dialogo_info(titulo = "SIN RESULTADOS", 
                                   texto = "No se encontraron tickets.", 
                                   padre = self.wids['ventana'])

    def inicializar_ventana(self):
        """
        Inicializa controles, TreeViews, etc.
        """
        self.comprobar_boton_facturar()
        cols = (('Venta', 'gobject.TYPE_STRING', True, True, True, 
                    self.cambiar_numventa),
                ('Código', 'gobject.TYPE_STRING', False, True, False, None),
                ('Producto', 'gobject.TYPE_STRING', False, True, False, None),
                ('P.V.P.', 'gobject.TYPE_STRING', False, True, False, None),
                ('Cantidad', 'gobject.TYPE_STRING', False, True, False, None),
                ('Total', 'gobject.TYPE_STRING', False, True, False, None),
                ('Factura', 'gobject.TYPE_STRING', False, True, False, None),
                ('IDLDV', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_ventas'], cols)
        self.wids['tv_ventas'].get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        self.wids['tv_ventas'].connect("row-activated", self.activar_ticket)
        for col in (self.wids['tv_ventas'].get_columns()[0:1]
                    + self.wids['tv_ventas'].get_columns()[3:6]):
            for cell in col.get_cell_renderers():
                cell.set_property("xalign", 1.0)
        tarifas = [(t.id, t.nombre) 
                    for t in pclases.Tarifa.select(orderBy = "nombre") 
                    if ((t.periodoValidezIni == None 
                         or t.periodoValidezIni <= datetime.datetime.today()) 
                        and (t.periodoValidezFin == None 
                             or t.periodoValidezFin>=datetime.datetime.today()))]
        utils.rellenar_lista(self.wids['cbe_tarifa'], tarifas)
        self.wids['cbe_tarifa'].connect("changed", self.mostrar_info_producto)
        self.rellenar_ultimas_ventas()
        self.wids['e_cantidad'].set_text('1')
        self.producto = None
        #try:
        #    self.ticket = pclases.Ticket.select(orderBy = "-id")[0]
        #except:
        #    self.ticket = None
        self.ticket = None  
            # Prefiero que empiece por uno nuevo, que ya me conozco al 
            # personal y fijo que lo meten todo en el último ticket. Si 
            # quieren segurilo, que le hagan doble clic.
        self.mostrar_info_ticket()
        # Aquí se redefinen algunas señales que interfieren con el movimiento 
        # del foco de los entry que se hace en la clase padre. Desconecto los 
        # "activate" de los entry:
        for w in self.wids.keys():
            if w in self.handlers_id and "activate" in self.handlers_id[w]:
                for h_id in self.handlers_id[w]["activate"]:
                    self.wids[w].disconnect(h_id)
        # Y ahora hago las conexiones que me interesan:
        self.wids['e_precio'].connect("changed", self.actualizar_subtotal)
        self.wids['e_precio'].connect("key_press_event", 
                                      pasar_foco_enter, 
                                      self.wids, 
                                      'b_articulo')
        self.wids['e_cantidad'].connect("changed", self.actualizar_subtotal)
        self.handler_buscador_codigo = self.wids['e_codigo'].connect("changed", 
            self.intentar_determinar_producto)
        #self.wids['e_cantidad'].connect("key_press_event", pasar_foco_enter, self.wids['b_articulo'])
        self.wids['e_cantidad'].connect("key_press_event", 
                                        pasar_foco_enter_cantidad, 
                                        self.wids['b_articulo'], 
                                        self.wids['e_codigo'])
        #self.wids['e_codigo'].connect("key_press_event", 
        #                              pasar_foco_enter, 
        #                              self.wids['b_articulo'])
        self.wids['e_codigo'].connect("key_press_event", 
                                      pasar_foco_enter, 
                                      self.wids, 
                                      'e_cantidad') # CWT
        self.wids['e_codigo'].connect("key-release-event", 
                                      self.resaltar_resto_codigo)
        font_desc = pango.FontDescription("Sans Bold 32")
        self.wids['e_total'].modify_font(font_desc)
        font_desc = pango.FontDescription("Sans Bold 24")
        self.wids['e_subtotal'].modify_font(font_desc)
        self.mostrar_tarifa_defecto()
        self.wids['e_codigo'].grab_focus()
        self.wids['b_articulo'].connect("key-press-event", 
            self.pasar_a_cant_si_es_numero)
        self.wids['e_codigo'].connect("focus-in-event", self.limpiar_si_escape)
        self.wids['b_buscar'].connect("focus-in-event", 
            lambda *args, **kw: self.wids['e_codigo'].grab_focus())
        try:
            from socket import gethostname
            hostname = gethostname()
            if hostname not in ("nostromo", "melchor"):
                # ¡HARTO de restaurar la ventana en desarrollo!
                self.wids['ventana'].maximize()
        except:
            self.wids['ventana'].maximize()

    def limpiar_si_escape(self, w, e):
        #w.select_region(0,-1)
        #print e.send_event
        pass

    def resaltar_resto_codigo(self, w, e):
        #print e.keyval, e.string
        if e.keyval == 65307:   # Escape
            w.select_region(0, -1)
        else:
            if (self.producto 
               and w.get_text() in self.producto.codigo 
               and e.string):
                pos_fin_anterior = w.get_position()
                w.set_text(self.producto.codigo)
                w.select_region(pos_fin_anterior, -1)

    def pasar_a_cant_si_es_numero(self, w, e):
        # print e.string, e.keyval, gtk.gdk.keyval_name(e.keyval)
        if e.string in [str(i) for i in range(10)]:
            self.wids['e_cantidad'].set_text(e.string)
            self.wids['e_cantidad'].grab_focus()
            self.wids['e_cantidad'].set_position(-1)

    def mostrar_tarifa_defecto(self):
        """
        La tarifa por defecto para el TPV se debe llamar 
        tarifa venta público 
        o 
        tarifa 1
        (aproximadamente) y por este orden de preferencia.
        """
        tarifa = pclases.Tarifa.get_tarifa_defecto()
        if tarifa != None:
            utils.combo_set_from_db(self.wids['cbe_tarifa'], tarifa.id)
        else:
            utils.combo_set_from_db(self.wids['cbe_tarifa'], None)

    def intentar_determinar_producto(self, gtkeditable):
        """
        Intenta localizar el producto buscando el texto del Entry 
        en el código o la descripción. Si encuentra un único resultado 
        lo coloca en ventana.
        """
        texto = gtkeditable.get_text()
        pcs = pclases.ProductoCompra.select(
            pclases.OR(pclases.ProductoCompra.q.codigo.contains(texto), 
                       pclases.ProductoCompra.q.descripcion.contains(texto)))
        #pvs = pclases.ProductoVenta.select(
        #    pclases.OR(pclases.ProductoVenta.q.codigo.contains(texto), 
        #               pclases.ProductoVenta.q.descripcion.contains(texto)))
        pcscount = pcs.count()
        #pvscount = pvs.count()
        if pcscount == 1: #+ pvscount == 1:
            if pcscount == 1:
                self.producto = pcs[0]
                self.mostrar_info_producto(machacar_codigo = False)
            #elif pvscount == 1:
            #    self.producto = pvs[0]
            #    self.mostrar_info_producto(machacar_codigo = False)
            else:
                print "tpv::intentar_determinar_producto -> Error. ¡No se pudo determinar si el producto encontrado es PC o PV !"
        else:
            self.producto = None
            self.wids['txt_descripcion'].get_buffer().set_text("")

    def actualizar_subtotal(self, gtkeditable):
        """
        Actualiza el campo subtotal de la ventana con el 
        resultado de multiplicar la cantidad actual por el 
        precio actual.
        Actualiza también el total de compra.
        """
        try:
            cantidad = utils._float(self.wids['e_cantidad'].get_text())
        except (ValueError, TypeError):
            cantidad = 0.0
        try:
            precio = utils._float(self.wids['e_precio'].get_text())
        except (ValueError, TypeError):
            precio = 0.0
        subtotal = cantidad * precio    # * 1.18 (El precio es PVP, ya lleva el IVA)
        self.wids['e_subtotal'].set_text((utils.float2str(subtotal)))
        self.mostrar_totales()

    def activar_ticket(self, tv, path, vc):
        """
        Hace activo el ticket seleccionado.
        """
        model = tv.get_model()
        if model[path].parent != None:
            idticket = model[path].parent[-1]
            idldv = model[path][-1]
            ldv = pclases.LineaDeVenta.get(idldv)
            cantidad = ldv.cantidad
            precio = ldv.precio
            self.wids['e_cantidad'].set_text(utils.float2str(cantidad, 2, autodec = True))
            self.wids['e_precio'].set_text(utils.float2str(precio * 1.18, 2, autodec = True))
            self.producto = ldv.producto
            try:
                ldv.destroySelf()
            except:
                texto = "tpv::activar_ticket -> No se pudo eliminar LDV ID %d al hacerle doble clic para editarla." % (ldv.id)
                self.logger.error(texto)
                print texto
            else:
                actualizar_existencias(self.producto, -cantidad)
        else:
            idticket = model[path][-1]
        self.ticket = pclases.Ticket.get(idticket)
        self.actualizar_ventana(machacar_precio_producto = False)

    def _wrap_actualizar_ventas(self, func):
        """
        Wrapper para lanzar el _actualizar_ventana (el original) 
        """
        gobject.idle_add(func, 
                         priority = gobject.PRIORITY_LOW)

    def actualizar_ventana(self, boton=None, machacar_precio_producto=True):
        DEBUG = False
        #DEBUG = True
        # XXX
        if DEBUG:
            import time
            inicio = time.time()
        # XXX
        self.comprobar_boton_facturar()
        # XXX
        if DEBUG:
            print "Tras comprobar botón facturar.", time.time() - inicio
        # XXX
        self.mostrar_info_ticket()
        # XXX
        if DEBUG:
            print "Tras comprobar datos ticket actual.", time.time() - inicio
        # XXX
        if boton != None:
            #self._rellenar_ultimas_ventas()
            self._wrap_actualizar_ventas(self._rellenar_ultimas_ventas)
            self.wids['e_codigo'].grab_focus()
            # XXX
            if DEBUG:
                print "Tras rellenar últimas ventas (no opt.).", time.time() - inicio
            # XXX
        else:
            #self.rellenar_ultimas_ventas()
            self._wrap_actualizar_ventas(self.rellenar_ultimas_ventas)
            # XXX
            if DEBUG:
                print "Tras rellenar últimas ventas (opt.).", time.time() - inicio
            # XXX
        self.mostrar_info_producto(
            machacar_precio_producto = machacar_precio_producto)
        # XXX
        if DEBUG:
            print "Tras mostrar datos producto.", time.time() - inicio
        # XXX
        self.mostrar_totales()
        # XXX
        if DEBUG:
            print "Tras mostrar totales.", time.time() - inicio
            print "=== End Of Actualizar_ventana ==="
        # XXX

    def comprobar_boton_facturar(self):
        """
        Comprueba y activa o desactiva el botón de facturar 
        tickets en función de si el usuario tiene permiso para 
        crear nuevas facturas.
        """
        try:
            permiso_facturar = self.usuario.get_permiso(pclases.Ventana.selectBy(
                                                fichero = "facturas_venta.py")[0])
        except AttributeError:  # Usuario es None o no es un usuario.
            permiso_facturar = False
        puede_facturar = self.usuario != None and permiso_facturar != None and permiso_facturar.nuevo
        if not self.usuario:
            puede_facturar = True # Para pruebas cuando se arranca de consola.
        self.wids['b_facturar'].set_sensitive(puede_facturar)

    def mostrar_totales(self):
        """
        Muestra el subtotal del precio actual por la 
        cantidad actual en pantalla y el total del 
        ticket.
        """
        if self.producto != None:
            try:
                precio = utils._float(self.wids['e_precio'].get_text())
            except ValueError:
                precio = 0.0
            try:
                cantidad = utils._float(self.wids['e_cantidad'].get_text())
            except ValueError:
                cantidad = 0.0
            subtotal = precio * cantidad
        else:
            subtotal = 0.0
        if self.ticket != None:
            total = self.ticket.calcular_total()
            self.wids['e_total'].set_text("%s €" % (utils.float2str(total + subtotal)))
        else:
            self.wids['e_total'].set_text("")

    def mostrar_info_ticket(self):
        """
        Muestra la información del ticket actual en ventana:
        """
        if self.ticket == None:
            self.wids['e_numventa'].set_text("")
            self.wids['e_fecha'].set_text("")
        else:
            self.wids['e_numventa'].set_text(str(self.ticket.numticket))
            self.wids['e_fecha'].set_text("%s - %s" % (utils.str_fecha(self.ticket.fechahora), 
                                                       utils.str_hora(self.ticket.fechahora)))

    def _rellenar_ultimas_ventas(self):
        """
        Introduce en el TreeView las ventas de TPV de los últimos días que 
        indique DIAS_TREEVIEW.
        """
        tickets = pclases.Ticket.select(
            pclases.Ticket.q.fechahora >= 
                (datetime.datetime.today() - 
                    (datetime.timedelta(days = 1) * self.DIAS_TREEVIEW)), 
            orderBy = "-id")
        model = self.wids['tv_ventas'].get_model()
        model.clear()
        self.wids['tv_ventas'].freeze_child_notify()
        self.wids['tv_ventas'].set_model(None)
        for ticket in tickets:
            #totalticket = ticket.calcular_total()
            totalticket = 0.0
            padre = model.append(None, (ticket.numticket, 
                                        utils.str_fecha(ticket.fechahora), 
                                        utils.str_hora(ticket.fechahora),
                                        "", 
                                        "", 
                                        #"%s €" % (utils.float2str(
                                        #    totalticket)), 
                                        "", 
                                        ", ".join([fra.numfactura for fra 
                                                    in ticket.get_facturas()]), 
                                        ticket.id))
            for ldv in ticket.lineasDeVenta:
                descripcion = ldv.producto.descripcion
                if len(descripcion) > 30:
                    descripcion = utils.wrap(descripcion, 30)
                totalldv = ldv.get_subtotal(iva = False) * 1.18
                model.append(padre, 
                              ("", 
                               ldv.producto.codigo, 
                               descripcion, 
                               "%s €" % (utils.float2str(ldv.precio * 1.18)),
                                # P.V.P. lleva 18% de IVA.
                               "%s" % utils.float2str(ldv.cantidad), 
                               "%s €" % utils.float2str(totalldv),
                                # Ventas de ticket llevan 18% de IVA. 
                                # Lo calculo aquí porque la 
                                # función toma el IVA en función del 
                                # cliente del pedido/albarán/factura.
                               ldv.get_factura_o_prefactura() 
                                and ldv.get_factura_o_prefactura().numfactura 
                                or "", 
                               ldv.id))
                totalticket += totalldv
            model[padre][5] = "%s €" % utils.float2str(totalticket)
        self.wids['tv_ventas'].set_model(model)
        self.wids['tv_ventas'].thaw_child_notify()
        try:
            self.wids['tv_ventas'].expand_row(model[0].path, False)
        except IndexError:
            pass    # El model está "vacido".
        if pclases.config.get_desplegar_tickets():
            self.wids['tv_ventas'].expand_all() #CWT

    def rellenar_ultimas_ventas(self):
        """
        Introduce en el TreeView las ventas de TPV de los últimos días (según
        indique el valor de DIAS_TREEVIEW).
        """
        tickets = pclases.Ticket.select(
            pclases.Ticket.q.fechahora >= 
                (datetime.datetime.today() - 
                    (datetime.timedelta(days = 1) * self.DIAS_TREEVIEW)), 
            orderBy = "-id")
        model = self.wids['tv_ventas'].get_model()
        #model.clear()
        fila = 0
        self.wids['tv_ventas'].freeze_child_notify()
        self.wids['tv_ventas'].set_model(None)
        for ticket in tickets:
            try:
                actual_en_model = model[fila]
            except IndexError:
                actual_en_model = None
            if actual_en_model and actual_en_model[-1] == ticket.id:
                totalticket = ticket.calcular_total()
                if "%s €" % utils.float2str(totalticket) == actual_en_model[5]:
                    #ldvs = len(ticket.lineasDeVenta)
                    ldvs = ticket._connection.queryOne(
                        "SELECT COUNT(id) "
                        "FROM linea_de_venta "
                        "WHERE ticket_id = %d" % ticket.id)[0]
                    iter = model.get_iter(fila)
                    en_model = model.iter_n_children(iter)
                    if ldvs == en_model:
                        fila += 1
                        # Si el ID es el mismo, el total también y el número 
                        # de líneas del ticket (importante para precio == 0 o 
                        # cantidad = 0 en la nueva LDV), no lo toco.
                        continue
            self.insertar_ticket_completo(model, fila, actual_en_model, ticket)
            fila += 1
        self.wids['tv_ventas'].set_model(model)
        self.wids['tv_ventas'].thaw_child_notify()
        try:
            self.wids['tv_ventas'].expand_row(model[0].path, False)
        except IndexError:
            pass    # El model está "vacido".
        if pclases.config.get_desplegar_tickets():
            self.wids['tv_ventas'].expand_all() #CWT

    def insertar_ticket_completo(self, model, fila, actual_en_model, ticket):
        """
        Inserta un ticket con sus LDVs en el model en la posición «fila».
        Si actual_en_model != None y tiene el mismo ID que el ticket que 
        queremos insertar, hay que sustituirlo por el ticket nuevo.
        """
        if actual_en_model and actual_en_model[-1] == ticket.id:
            del model[fila]
        totalticket = 0.0
        padre = model.insert(None, 
                             fila, 
                             (ticket.numticket, 
                              utils.str_fecha(ticket.fechahora), 
                              utils.str_hora(ticket.fechahora),
                              "", 
                              "", 
                              "", 
                              ", ".join([fra.numfactura for fra 
                                         in ticket.get_facturas()]), 
                              ticket.id))
        for ldv in ticket.lineasDeVenta:
            descripcion = ldv.producto.descripcion
            if len(descripcion) > 30:
                descripcion = utils.wrap(descripcion, 30)
            totalldv = ldv.get_subtotal(iva = False) * 1.18
            model.append(padre, 
                          ("", 
                           ldv.producto.codigo, 
                           descripcion, 
                           "%s €" % (utils.float2str(ldv.precio * 1.18)),
                            # P.V.P. lleva 18% de IVA.
                           "%s" % utils.float2str(ldv.cantidad), 
                           "%s €" % utils.float2str(totalldv),
                            # Ventas de ticket llevan 18% de IVA. 
                            # Lo calculo aquí porque la 
                            # función toma el IVA en función del 
                            # cliente del pedido/albarán/factura.
                           ldv.get_factura_o_prefactura() 
                            and ldv.get_factura_o_prefactura().numfactura 
                            or "", 
                           ldv.id))
            totalticket += totalldv
        model[padre][5] = "%s €" % utils.float2str(totalticket)

    def buscar(self, boton):
        """
        Busca un producto por descripción e introduce el código, descripción, 
        precio, etc. en los entries correspondientes
        """
        idtarifa = utils.combo_get_value(self.wids['cbe_tarifa'])
        if idtarifa != None:
            tarifa = pclases.Tarifa.get(idtarifa)
        else:
            tarifa = None
        # self.producto = buscar_producto(padre = self.wids['ventana'], tarifa = tarifa, texto_defecto = self.wids['e_codigo'].get_text())
        productos = utils.buscar_producto_general(padre = self.wids['ventana'], 
                                                  mostrar_precios = True, 
                                                  texto_defecto = self.wids['e_codigo'].get_text(), 
                                                  incluir_sin_iva = False)
        try:
            self.producto = productos[0]
        except (IndexError, TypeError):
            self.producto = None
        if self.producto != None:
            self.mostrar_info_producto()

    def mostrar_info_producto(self, machacar_codigo = True, 
                              machacar_precio_producto = True):
        """
        Coloca el código, descripción y precio en los entries.
        """
        idtarifa = utils.combo_get_value(self.wids['cbe_tarifa'])
        if idtarifa != None:
            tarifa = pclases.Tarifa.get(idtarifa)
        else:
            tarifa = None
        if self.producto != None:
            self.producto.sync()
            codigo = self.producto.codigo
            descripcion = self.producto.descripcion
            if tarifa != None:
                precio = tarifa.obtener_precio(self.producto, 
                         tarifa_defecto = pclases.Tarifa.get_tarifa_defecto())
            else:
                if hasattr(self.producto, "precioPorDefecto"):
                    precio = self.producto.precioPorDefecto
                elif hasattr(self.producto, "precioDefecto"):
                    precio = self.producto.precioDefecto
                else:
                    txt = "%stpv::mostrar_info_producto::No se pudo determinar el precio de: %s" % (self.usuario and self.usuario + ": " or "", self.producto)
                    self.logger.error(txt)
                    print txt
                    precio = 0.0
            precio_con_iva = precio * 1.18
                # En tickets se debe mostrar siempre el P.V.P. con 18% de IVA.
            if (hasattr(self.producto, "controlExistencias") 
                and self.producto.controlExistencias):
                existencias = utils.float2str(self.producto.existencias, 
                                              autodec = True)
            else:
                existencias = "-"
        else:
            codigo = ""
            descripcion = ""
            precio_con_iva = 0
            existencias = "-"
        if machacar_codigo:
            self.wids['e_codigo'].disconnect(self.handler_buscador_codigo)
                # Para que no me machaque el producto actual
            self.wids['e_codigo'].set_text(codigo)
            self.handler_buscador_codigo = self.wids['e_codigo'].connect(
                                "changed", self.intentar_determinar_producto)
        self.wids['txt_descripcion'].get_buffer().set_text(descripcion)
        if machacar_precio_producto:
            self.wids['e_precio'].set_text(utils.float2str(precio_con_iva))
                # Siempre PVP
        self.wids['e_existencias'].set_text(existencias)

    def add_ldv(self, boton):
        """
        Crea una LDV de TPV con el producto, precio y cantidad que están en 
        pantalla.
        Al finalizar, borra la información del producto para introducir el 
        siguiente y pone la cantidad al valor por defecto (1).
        """
        DEBUG = False
        #DEBUG = True
        if DEBUG:
            import time
            inicio = time.time()
        if self.producto != None:
            # XXX
            if DEBUG:
                print "Tras comprobar producto != None", time.time() - inicio
            # XXX
            if self.ticket == None:
                self.ticket = pclases.Ticket()
                # XXX
                if DEBUG:
                    print "Tras crear nuevo ticket", time.time() - inicio
                # XXX
            #if isinstance(self.producto, pclases.ProductoVenta): 
            #    productoVenta = self.producto
            #    productoCompra = None
            if isinstance(self.producto, pclases.ProductoCompra): 
                productoVenta = None
                productoCompra = self.producto
            # XXX
            if DEBUG:
                print "Tras determinar tipo de producto.", time.time() - inicio
            # XXX
            try:
                cantidad = utils._float(self.wids['e_cantidad'].get_text())
            except ValueError:
                cantidad = 0.0
            if cantidad > 99999:    # Me aseguro de que no haya metido un 
                cantidad = 1        # código en la cantidad.
            try:
                precio = utils._float(self.wids['e_precio'].get_text()) / 1.18  
                # En la LDV no debe llevar IVA.
            except ValueError:
                precio = 0.0
            descuento = 0.0  # "Impepinablemente" (hasta que se decida otra 
                        # cosa, grrr...), no hay descuentos en ventas de caja.
            # XXX
            if DEBUG:
                print "Tras determinar cantidad y precio.", time.time() - inicio
            # XXX
            self.producto.sync()
            # XXX
            if DEBUG:
                print "Tras sincronizar producto.", time.time() - inicio
            # XXX
            #if isinstance(self.producto, pclases.ProductoVenta):
            #    existencias = self.producto.stock
            if isinstance(self.producto, pclases.ProductoCompra):
                existencias = self.producto.existencias
            # XXX
            if DEBUG:
                print "Tras instanciar existencias.", time.time() - inicio
            # XXX
            if (existencias - cantidad < 0 
                and hasattr(self.producto, "controlExistencias") 
                and self.producto.controlExistencias):
                str_existencias = crear_str_existencias(self.producto)
                #if utils.dialogo(titulo = "EXISTENCIAS INSUFICIENTES", 
                #                 texto = "Existencias de %s: %s.\n\nPulse «sí» para continuar la venta usando %s como cantidad.\nPulse «no» para cancelar." % (self.producto.descripcion, str_existencias, utils.float2str(existencias)), 
                #                 padre = self.wids['ventana']):
                #    cantidad = existencias
                if not utils.dialogo(titulo = "EXISTENCIAS INSUFICIENTES", 
                                     texto = "Existencias de %s: %s.\n\nPulse «sí» para continuar la venta o «no» para cancelar." % (self.producto.descripcion, str_existencias), 
                                     padre = self.wids['ventana']):
                    return
            # XXX
            if DEBUG:
                print "Tras comprobar existencias suficientes.", time.time() - inicio
            # XXX
            ldv_existente = None
            for linea in self.ticket.lineasDeVenta:
                if (
                    linea.productoCompra == productoCompra 
                    and round(linea.precio, 2) == round(precio, 2)): 
                    ldv_existente = linea
                    break
            # XXX
            if DEBUG:
                print "Tras verificar si actualiza LDV.", time.time() - inicio
            # XXX
            if ldv_existente != None:
                ldv = ldv_existente
                ldv.cantidad += cantidad
                # XXX
                if DEBUG:
                    print "Tras actualizar cantidad en LDV.", time.time() - inicio
                # XXX
            else:
                ldv = pclases.LineaDeVenta(productoCompra = productoCompra, 
                                           ticket = self.ticket, 
                                           pedidoVenta = None, 
                                           facturaVenta = None, 
                                           #productoVenta = productoVenta, 
                                           albaranSalida = None, 
                                           fechahora = datetime.datetime.today(), 
                                           cantidad = cantidad, 
                                           precio = precio, 
                                           descuento = descuento)
                # XXX
                if DEBUG:
                    print "Tras crear nueva LDV.", time.time() - inicio
                # XXX
            actualizar_existencias(self.producto, cantidad)
            # XXX
            if DEBUG:
                print "Tras actualizar existencias en producto.", time.time() - inicio
            # XXX
            self.producto = None
            self.wids['e_cantidad'].set_text("1")
            self.mostrar_tarifa_defecto()
            # XXX
            if DEBUG:
                print "Tras mostrar la tarifa por defecto.", time.time() - inicio
            # XXX
            self.actualizar_ventana()
            # XXX
            if DEBUG:
                print "Tras actualizar ventana.", time.time() - inicio
            # XXX
        self.wids['e_codigo'].grab_focus()

    def cerrar_venta(self, boton):
        """
        Cierra la venta, muestra el total e imprime el ticket.
        Si el último producto aún no se ha añadido a la venta, 
        lo introduce antes de cerrarla.
        Muestra en pantalla el siguiente número de venta, que 
        corresponderá a la venta nueva que se inicia.
        """
        if self.producto != None:
            self.add_ldv(None)
        self.abrir_cajon()
        self.mostrar_ventana_total_venta()
        self.ticket = None
        self.producto = None
        self.actualizar_ventana()
        self.wids['e_codigo'].grab_focus()

    def mostrar_ventana_total_venta(self):
        # TODO: Mejorar y hacer como en el TPV antiguo.
        if self.ticket == None:
            return
        dialog = gtk.Dialog("TOTAL DE VENTA TICKET %d" % (self.ticket.numticket),
                            self.wids['ventana'],
                            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                            (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))

        info = gtk.Entry()
        font_desc = pango.FontDescription("Sans Bold 32")
        info.modify_font(font_desc)
        info.set_text(self.wids['e_total'].get_text())
        info.set_property("editable", False)

        hbox = gtk.HBox(spacing = 5)
        icono = gtk.Image()
        icono.set_from_stock(gtk.STOCK_DIALOG_INFO, gtk.ICON_SIZE_DIALOG)
        hbox.pack_start(icono)
        hbox.pack_start(info)
        dialog.vbox.pack_start(hbox)
        hbox.show_all()
        dialog.set_transient_for(self.wids['ventana'])
        dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        dialog.action_area.get_children()[0].grab_focus()
        dialog.resize(500, 200)
        dialog.run()
        dialog.destroy()
        

    def chequear_cambios(self):
        pass

    def imprimir(self, boton):
        """
        Imprime un ticket por puerto paralelo y abre el cajón.
        """
        tickets_a_imprimir = []
        if self.wids['tv_ventas'].get_selection().count_selected_rows() != 0: 
            if utils.dialogo(titulo = "IMPRIMIR TICKETS", 
                             texto = "¿Imprimir tickets seleccionados?", 
                             padre = self.wids['ventana']):
                model, paths = self.wids['tv_ventas'].get_selection().get_selected_rows()
                for path in paths:
                    iter = model.get_iter(path)
                    if model[iter].parent == None:  # Es un ticket
                        idticket = model[iter][-1]
                        ticket = pclases.Ticket.get(idticket)
                        tickets_a_imprimir.append(ticket)
                    else:   # Es una LDV
                        idldv = model[iter][-1] 
                        ldv = pclases.LineaDeVenta.get(idldv)
                        ticket = ldv.ticket
                        if ticket != None and ticket not in tickets_a_imprimir:
                            tickets_a_imprimir.append(ticket)
        else:
            num_a_buscar = utils.dialogo_entrada(titulo = "¿NÚMERO DE TICKET?", 
                                                 texto = "Introduzca el número del ticket a buscar:", 
                                                 padre = self.wids['ventana'])
            if num_a_buscar != None and num_a_buscar != "":
                try:
                    numticket = int(num_a_buscar)
                    ticket = pclases.Ticket.select(pclases.Ticket.q.numticket == numticket)[0]
                except (IndexError, ValueError):
                    utils.dialogo_info(titulo = "TICKET NO ENCONTRADO", 
                                       texto = "El ticket no se encontró o el texto «%s» no es un número de ticket válido." % (num_a_buscar), 
                                       padre = self.wids['ventana'])
                else:
                    tickets_a_imprimir.append(ticket)
        for ticket in tickets_a_imprimir:
            try:
                imprimir_ticket(ticket)
            except Exception, msg:
                utils.dialogo_info(titulo = "ERROR IMPRESORA", 
                                   texto = "Ocurrió un error al acceder a la impresora de tickets.\n\nInformación de depuración:\n%s" % msg, 
                                   padre = self.wids['ventana'])

    def abrir_cajon(self, boton = None):
        """
        Abre el cajón portamonedas.
        """
        puerto_lpt = pclases.config.get_puerto_ticketera()
        if pclases.config.get_oki():
            printer = LPTOKI(puerto_lpt)
        else:
            printer = LPT(puerto_lpt)
        try:
            printer.abrir(set_codepage = pclases.config.get_codepageticket())
            printer.abrir_cajon(pclases.config.get_cajonserie())
            printer.cerrar()
        except:
            print "No se pudo operar sobre el cajón/ticketera."

    def cambiar_numventa(self, cell, path, texto):
        """
        Cambia el número del ticket siempre y cuando no exista ya 
        otro ticket con ese número y del mismo año.
        """
        model = self.wids['tv_ventas'].get_model()
        if model[path].parent == None:  # Es un ticket
            try:
                numventa = int(texto)
            except (ValueError, TypeError):
                utils.dialogo_info(titulo = "VALOR INCORRECTO", 
                                   texto = "El texto %s no es un número correcto." % (texto), 
                                   padre = self.wids['ventana'])
            else:
                ticket = pclases.Ticket.get(model[path][-1])
                tickets = pclases.Ticket.select(""" numticket = %d AND date_part('year', fechahora) = %d """ % (numventa, ticket.fechahora.year))
                if tickets.count() > 0:
                    utils.dialogo_info(titulo = "NÚMERO DE TICKET REPETIDO", 
                                       texto = "El ticket %d ya existe en el año %d." % (numventa, ticket.fechahora.year), 
                                       padre = self.wids['ventana'])
                else:
                    ticket.numticket = numventa
                    ticket.sync()
                    model[path][0] = ticket.numticket
                    #self.rellenar_ultimas_ventas()
                    self.mostrar_info_ticket()
                        # Por si han cambiado el número del ticket actual.

    def borrar_venta(self, boton):
        """
        Borra un ticket completo a una línea dependiendo 
        de la selección del TreeView.
        """
        if (self.wids['tv_ventas'].get_selection().count_selected_rows() != 0 
            and utils.dialogo(titulo = "BORRAR TICKETS", 
                              texto = "¿Está seguro de querer borrar las ventas seleccionadas?", 
                              padre = self.wids['ventana'])):
            model, paths = self.wids['tv_ventas'].get_selection().get_selected_rows()
            for path in paths:
                iter = model.get_iter(path)
                if model[iter].parent == None:  # Es un ticket
                    idticket = model[iter][-1]
                    ticket = pclases.Ticket.get(idticket)
                    facturas_ticket = ticket.get_facturas()
                    if facturas_ticket != []:
                        utils.dialogo_info(titulo = "VENTA FACTURADA", 
                                           texto = "La venta ya ha sido facturada en %s.\nElimine primero las facturas antes de cancelar la venta." % ([fra.numfactura for fra in facturas_ticket]))
                    else:
                        for ldv in ticket.lineasDeVenta:
                            actualizar_existencias(ldv.producto, -ldv.cantidad)
                        if ticket == self.ticket:   # Estoy borrando el actual:
                            self.ticket = None
                            self.mostrar_info_ticket()
                        ticket.destroy_en_cascada()
                else:   # Es una LDV
                    idldv = model[iter][-1]
                    try: 
                        ldv = pclases.LineaDeVenta.get(idldv)
                    except:  # Es posible que ya se haya borrado
                        continue
                    if ldv.get_factura_o_prefactura() != None:
                        utils.dialogo_info(titulo = "VENTA FACTURADA", 
                                           texto = "La venta ya ha sido facturada en %s.\nCancele la venta en la factura antes de eliminarla del ticket." % (ldv.get_factura_o_prefactura().numfactura))
                    else:
                        try:
                            producto = ldv.producto
                            cantidad = ldv.cantidad
                            ldv.destroySelf()
                        except Exception, msg:
                            utils.dialogo_info(titulo = "ERROR DE BORRADO", 
                                               texto = "La venta no se pudo eliminar.\nTal vez esté implicada en otras operaciones que impiden su borrado.\n\n\nInformación de depuración:\n%s" % (msg))
                        else:
                            actualizar_existencias(producto, -cantidad)
            self.rellenar_ultimas_ventas()

    # XXX: Código a refactorizar que se usa únicamente para generar la factura. (se repite en al menos 3 ventanas)
    def crear_vencimientos_por_defecto(self, factura):
        """
        Crea e inserta los vencimientos por defecto
        definidos por el cliente en la factura
        actual y en función de las LDV que tenga
        en ese momento (concretamente del valor
        del total de la ventana calculado a partir
        de las LDV.)
        """
        ok = False
        # NOTA: Casi-casi igual al de facturas_venta.py. Si cambia algo importante aquí, cambiar también allí y viceversa.
        cliente = factura.cliente
        if cliente.vencimientos != None and cliente.vencimientos != '':
            try:
                vtos = cliente.get_vencimientos(factura.fecha)
            except:
                utils.dialogo_info(titulo = 'ERROR VENCIMIENTOS POR DEFECTO', 
                                   texto = 'Los vencimientos por defecto del cliente no se pudieron procesar correctamente.\nVerifique que están bien escritos y el formato es correcto en la ventana de clientes.', 
                                   padre = self.wids['ventana'])
                return ok   # Los vencimientos no son válidos o no tiene.
            self.borrar_vencimientos_y_estimaciones(factura)
            total = self.rellenar_totales(factura)
            numvtos = len(vtos)
            cantidad = total/numvtos
            if factura.fecha == None:
                factura.fecha = time.localtime()
            if (cliente.diadepago != None 
               and cliente.diadepago != ''
               and cliente.diadepago.strip() != "-"):
                diaest = cliente.get_dias_de_pago()
            else:
                diaest = False
            for incr in vtos:
                fechavto = factura.fecha + (incr * datetime.timedelta(days = 1))
                vto = pclases.VencimientoCobro(fecha = fechavto,
                                               importe = float(cantidad),
                                               facturaVenta = factura, 
                                               observaciones = factura.cliente and factura.cliente.textoformacobro or "", 
                                               cuentaOrigen = factura.cliente and factura.cliente.cuentaOrigen or None)
                if diaest:
# XXX 24/05/06
                    # Esto es más complicado de lo que pueda parecer a simple vista. Ante poca inspiración... ¡FUERZA BRUTA!
                    fechas_est = []
                    for dia_estimado in diaest:
                        while True:
                            try:
                                fechaest = datetime.date(day = dia_estimado, month = fechavto.month, year = fechavto.year)
                                break
                            except:
                                dia_estimado -= 1
                                if dia_estimado <= 0:
                                    dia_estimado = 31
                        if fechaest < fechavto:     # El día estimado cae ANTES del día del vencimiento. 
                                                    # No es lógico, la estimación debe ser posterior.
                                                    # Cae en el mes siguiente, pues.
                            mes = fechaest.month + 1
                            anno = fechaest.year
                            if mes > 12:
                                mes = 1
                                anno += 1
                            try:
                                fechaest = datetime.date(day = dia_estimado, month = mes, year = anno)
                            except ValueError:
                                # La ley de comercio dice que se pasa al último día del mes:
                                fechaest = datetime.date(day = -1, month = mes, year = anno)
                        fechas_est.append(fechaest)
                    fechas_est.sort()
                    fechaest = fechas_est[0]
                    vto.fecha = fechaest 
            ok = True
        else:
            utils.dialogo_info(titulo = "SIN DATOS", 
                               texto = "El cliente no tiene datos suficientes para crear vencimientos por defecto.", 
                               padre = self.wids['ventana'])
        return ok
    
    def borrar_vencimientos_y_estimaciones(self, factura):
        for vto in factura.vencimientosCobro:
            vto.factura = None
            vto.destroySelf()
        #for est in factura.estimacionesCobro:
        #    est.factura = None
        #    est.destroySelf()
    
    def rellenar_totales(self, factura):
        """
        Calcula los totales de la factura a partir de 
        las LDVs, servicios, cargo, descuento y abonos.
        """
        subtotal = self.total_ldvs(factura) + self.total_srvs(factura)
        tot_dto = utils.ffloat(-1 * (subtotal + factura.cargo) * factura.descuento)
        tot_iva = self.total_iva(factura.iva, subtotal, tot_dto, factura.cargo)
        return self.total(subtotal, factura.cargo, tot_dto, tot_iva)

    def total(self, subtotal, cargo, dto, iva):
        return utils.ffloat(subtotal + cargo + dto + iva)

    def total_iva(self, iva, subtotal, tot_dto, cargo):
        return utils.ffloat(subtotal + tot_dto + cargo) * iva

    def total_ldvs(self, factura):
        """
        Total de las líneas de venta. Sin IVA.
        """
        return sum([utils.ffloat((l.cantidad * l.precio) * (1 - l.descuento)) for l in factura.lineasDeVenta])
        
    def total_srvs(self, factura):
        """
        Total de servicios. Sin IVA.
        """
        return sum([utils.ffloat((s.precio * s.cantidad) * (1 - s.descuento)) for s in factura.servicios])
    # XXX: EOCódigo a refactorizar que se usa únicamente para generar la factura. (se repite en al menos 3 ventanas)

    def facturar(self, boton):
        """
        Pide un cliente y crea una factura con los 
        tickets seleccionados.
        Al terminar, pregunta si desea eliminar los 
        tickets o no (CWT: BP lo quiere así porque no 
        quiere separar los tickets facturados a la 
        hora de llevarlos a la gestoría).
        """
        if self.wids['tv_ventas'].get_selection().count_selected_rows() != 0: 
            clientes = [(c.id, c.nombre) for c in pclases.Cliente.select(orderBy = "nombre")]
            idcliente, nombrecliente = utils.dialogo_entrada_combo(
                titulo = "SELECCIONE UN CLIENTE", 
                texto = "Si el cliente no se encuentra en el desplegable, \n"
                        "teclee el nombre comercial; se le pedirá el resto \n"
                        "de información necesaria para crearlo.", 
                ops = clientes, 
                padre = self.wids['ventana'])
            if nombrecliente != None and idcliente == None:
                clientes = pclases.Cliente.select("nombre ILIKE('%s')" 
                                                    % nombrecliente)
                # Es posible que lo haya escrito en mayúsculas y esté en 
                # la BD en minúsculas, etc.
                if clientes.count() > 0:
                    idcliente = clientes[0].id
                else:
                    idcliente = None
                    if utils.dialogo(titulo = "¿CREAR NUEVO?", 
                            texto = "El cliente %s no existe, ¿desea crearlo?" 
                                % nombrecliente, 
                            padre = self.wids['ventana'], 
                            defecto = True, 
                            tiempo = 10):
                        idcliente = crear_nuevo_cliente(nombrecliente, 
                                                        self.wids['ventana'])
            if idcliente != None:
                cliente = pclases.Cliente.get(idcliente)
                factura = crear_factura(cliente, padre = self.wids['ventana'])
                if factura != None:
                    model, paths = self.wids['tv_ventas'].get_selection().get_selected_rows()
                    ldvs_facturadas = []
                    for path in paths:
                        iter = model.get_iter(path)
                        if model[iter].parent == None:  # Es un ticket
                            idticket = model[iter][-1]
                            ticket = pclases.Ticket.get(idticket)
                            for ldv in ticket.lineasDeVenta:
                                if ldv.get_factura_o_prefactura() == None:
                                    ldv.facturaVenta = factura
                                    ldvs_facturadas.append(ldv)
                                elif ldv.get_factura_o_prefactura() != factura:
                                    txt = "tpv::facturar -> La LDV ID %d ya está facturada en %s. No se añadirá a %s." % (ldv.id, ldv.get_factura_o_prefactura().numfactura, factura.numfactura)
                                    print txt
                                    self.logger.warning(txt)
                        else:   # Es una LDV
                            idldv = model[iter][-1] 
                            ldv = pclases.LineaDeVenta.get(idldv)
                            if ldv.get_factura_o_prefactura() == None:
                                ldv.facturaVenta = factura
                                ldvs_facturadas.append(ldv)
                            elif ldv.get_factura_o_prefactura() != factura:   # Se acaba de facturar en el bucle de arriba.
                                txt = "tpv::facturar -> La LDV ID %d ya está facturada en %s. No se añadirá a %s." % (ldv.id, ldv.get_factura_o_prefactura().numfactura, factura.numfactura)
                                print txt
                                self.logger.warning(txt)
                    if ldvs_facturadas != []:
                        ok = self.crear_vencimientos_por_defecto(factura)
                        if not ok:
                            import facturas_venta
                            utils.dialogo_info(titulo = "FACTURA CREADA", 
                                               texto = "Se creó con éxito la factura %s.\n\nA continuación se abrirá en una nueva ventana.\nVerifique todos los datos y cree los vencimientos antes de imprimir y bloquear la factura." % (factura.numfactura), 
                                               padre = self.wids['ventana'])
                            ventana = facturas_venta.FacturasVenta(objeto = factura, usuario = self.usuario)
                        else:
                            if utils.dialogo(titulo = "¿COBRAR?", 
                                             texto = "¿Marcar factura como cobrada?\n\nResponda «No» para dejar los vencimientos como pendientes de cobro.\nResponda «Sí» si ha cobrado el importe total de la factura.", 
                                             padre = self.wids['ventana']):
                                # Creo tantos cobros como vencimientos creados:
                                for v in factura.vencimientosCobro:
                                    c = pclases.Cobro(prefactura = None, 
                                        pagareCobro = None, 
                                        facturaVenta = factura, 
                                        cliente=factura.cliente, 
                                        fecha = v.fecha, 
                                        importe = v.importe, 
                                        observaciones = "Cobrado al facturar"
                                                        " desde TPV.")
                            if debe_generar_recibo(factura, 
                                                   self.wids['ventana']):
                                generar_recibo(factura, 
                                               self.usuario, 
                                               self.logger, 
                                               self.wids['ventana'])
                            factura.bloqueada = True
                            from informes import mandar_a_imprimir_con_foxit
                            from albaranes_de_salida import imprimir_factura
                            mandar_a_imprimir_con_foxit(
                                imprimir_factura(factura, self.usuario, False))
                            # CWT: 2 copias.
                            #mandar_a_imprimir_con_foxit(
                            #    imprimir_factura(factura, self.usuario, False)) 
                        if utils.dialogo(titulo = "ELIMINAR LÍNEAS FACTURADAS", 
                                         texto = "¿Desea desvincular del TPV "
                                                 "las ventas de caja y tickets"
                                                 " facturados?", 
                                         padre = self.wids['ventana']):
                            for ldv in ldvs_facturadas:
                                if len(ldv.ticket.lineasDeVenta) == 1:  
                                    # Sólo quedo yo, elimino para que no 
                                    # queden tickets vacíos.
                                    ticket = ldv.ticket
                                    ldv.ticket = None
                                    ticket.destroySelf()
                                ldv.ticket = None
                                if ldv.albaranSalida==ldv.facturaVenta==None:
                                    ldv.destroySelf()
                            #self.actualizar_ventana()
                            #self._rellenar_ultimas_ventas()
                            self.wids['b_actualizar'].clicked()
                    else:
                        utils.dialogo_info(titulo = "NO SE CREÓ LA FACTURA", 
                            texto = "Todas las líneas seleccionadas ya se "
                                    "encuentran facturadas.\nNo se pueden "
                                    "volver a facturar.", 
                            padre = self.wids['ventana'])
                        factura.destroySelf()
                    self.actualizar_ventana()

    def arqueo(self, boton):
        """
        Imprime números de ticket y totales de la caja del día seleccionado.
        """
        fecha = utils.mostrar_calendario(padre = self.wids['ventana'])
        fecha = datetime.date(*(fecha[::-1]))
        dias = self.wids['sp_dias'].get_value()
        fecha_fin = fecha + datetime.timedelta(days = dias)
        tickets = pclases.Ticket.select(
            pclases.AND(
                pclases.Ticket.q.fechahora >= fecha, 
                pclases.Ticket.q.fechahora < fecha_fin), 
            orderBy = "fechahora")
        #for t in tickets:
        #    print (t.numticket, 
        #           utils.str_fechahora(t.fechahora), 
        #           utils.float2str(t.calcular_total()))
        imprimir_arqueo(tickets)

def crear_factura(cliente, padre = None):
    """
    Crea una factura vacía para el cliente recibido.
    Devuelve None si la factura no se pudo crear.
    """
    factura = None
    try:
        irpf = pclases.DatosDeLaEmpresa.select()[0].irpf
    except (IndexError, AttributeError), msg:
        print "tpv::crear_factura -> No se pudo obtener el IRPF de la empresa de la tabla datos_de_la_empresa. Excepción: %s" % (msg)
        irpf = .0
    if cliente.contador == None:
        print "tpv::crear_factura -> El cliente no tiene contador. No se creará factura"
        utils.dialogo_info(titulo = "FACTURA NO CREADA", 
                           texto = "La factura no se pudo crear por no tener contador el cliente %s." % cliente.nombre, 
                           padre = padre)
    else:
        try:
            factura = pclases.FacturaVenta(cliente = cliente, 
                                           numfactura = cliente.contador.get_next_numfactura(), 
                                           fecha = datetime.datetime.today(), 
                                           descuento = 0.0, 
                                           cargo = 0.0, 
                                           observaciones = "", 
                                           iva = 0.18, 
                                           bloqueada = False, 
                                           irpf = irpf)
        except Exception, msg:
            factura = None
            print "tpv::crear_factura -> No se pudo crear la factura. Excepción: %s." % msg
        if factura != None:
            # TODO: Quedaría comprobar las restricciones de secuencialidad y esas cosas y borrar la factura si no las cumpliera.
            cliente.contador.get_and_commit_numfactura()
    return factura

def buscar_producto(padre = None, tarifa = None, texto_defecto = ""):
    """
    Recibe la ventana padre y devuelve una lista de 
    objetos producto de compra o de venta o una lista 
    vacía si no se encuentra.
    Muestra una ventana donde introducir un código, código de 
    Composan, descripción completa o nombre y realiza la 
    búsqueda en las tablas de producto_compra y producto_venta.
    """
    import sys, os
    sys.path.append(os.path.join("..", "framework"))
    import pclases
    res = None 
    a_buscar = utils.dialogo_entrada(titulo = "BUSCAR PRODUCTO", 
                                     texto = "Introduzca código o descripción del producto:", 
                                     padre = padre, 
                                     valor_por_defecto = texto_defecto)
    if a_buscar != None:
        productos_compra = utils.buscar_productos_compra(a_buscar)
        productos_venta = utils.buscar_productos_venta(a_buscar)
        resultados = []
        for pc in productos_compra:
            if tarifa != None:
                precio = tarifa.obtener_precio(pc, 
                         tarifa_defecto = pclases.Tarifa.get_tarifa_defecto())
            else:
                precio = pc.precioDefecto
            resultados.append(("PC:%d" % (pc.id), pc.codigo, pc.descripcion, "%s €" % (utils.float2str(precio * 1.18)), "%s %s" % (utils.float2str(pc.existencias), pc.unidad)))
        for pv in productos_venta:
            if tarifa != None:
                precio = tarifa.obtener_precio(pv, 
                         tarifa_defecto = pclases.Tarifa.get_tarifa_defecto())
            else:
                precio = pv.precioDefecto
            resultados.append(("PV:%d" % (pv.id), pv.codigo, pv.descripcion, "%s €" % (utils.float2str(precio * 1.18)), pv.get_str_stock()))
        resultados.sort(func_ordenar_por_item_dos)
        idproducto = utils.dialogo_resultado(resultados, 
                                             "Seleccione un producto:", 
                                             multi = False, 
                                             padre = padre, 
                                             cabeceras = ("ID", "Código", "Descripción", "P.V.P.", "Existencias"))
        if idproducto > 0:
            tipo, id = idproducto.split(":")
            try:
                id = int(id)
            except ValueError:
                res = None
            if tipo == "PC":
                res = pclases.ProductoCompra.get(id)
            #elif tipo == "PV":
            #    res = pclases.ProductoVenta.get(id)
        elif idproducto != -1:
            utils.dialogo_info(titulo = "NO ENCONTRADO", 
                               texto = "No se econtraron productos con la búsqueda %s." % (a_buscar),
                               padre = padre)
    return res

def func_ordenar_por_item_dos(p1, p2):
    """
    Función para ordenar por el segundo elemento de las dos listas recibidas.
    Se usa en la búsqueda de productos para ordenar por descripción.
    Ignora mayúsculas y minúsculas.
    """
    d1 = p1[2].upper()
    d2 = p2[2].upper()
    if d1 < d2:
        return -1
    if d1 > d2:
        return 1
    return 0

def crear_str_existencias(producto):
    """
    Devuelve una cadena con las existencias y unidades del 
    producto recibido.
    """
    res = "?"
    try:
        res = producto.get_str_existencias()
    except AttributeError:
        if isinstance(producto, pclases.ProductoCompra):
            res = "%s %s" % (utils.float2str(producto.existencias), producto.unidad)
        else:
            if hasattr(producto, existencias):
                res = utils.float2str(producto.existencias)
            else:
                print "No sé cómo acceder a las existencias del producto %s" % (producto)
    return res
    

def actualizar_existencias(producto, cantidad):
    """
    Resta la cantidad recibida a las existencias del producto.
    Si es un producto de venta con artículos... ¿cómo lo hago?
    """
    producto.sync()
    if hasattr(producto, "controlExistencias") and producto.controlExistencias:
        if cantidad != 0:   # Para evitar tráfico innecesario. Si no hay 
                # cambios en las existencias de los productos, no los toco.
            producto.sync()
            if isinstance(producto, pclases.ProductoCompra):
                producto.existencias -= cantidad
                # Ajusto también las existencias del almacén origen.
                almacenorigen = pclases.Almacen.get_almacen_principal()
                producto.add_existencias(-cantidad, almacenorigen)
            else:
                print "No sé cómo descontar existencias de esto: %s. Debería "\
                      "restar %s" % (producto, cantidad)
            producto.syncUpdate()
        producto.sync()
    
def imprimir_ticket(ticket):
    """
    Imprime el objeto ticket recibido por el puerto paralelo.
    """
    try:
        dde = pclases.DatosDeLaEmpresa.select()[0]
    except IndexError:
        print "tpv::imprimir_ticket -> No se encontraron los datos de la empresa. Abortando impresión..."
    else:
        # ANCHO = 48
        ANCHO = pclases.config.get_anchoticket()
        puerto_lpt = pclases.config.get_puerto_ticketera()
        if pclases.config.get_oki():
            ticketera = LPTOKI(puerto_lpt)
        else:
            ticketera = LPT(puerto_lpt)
        try:
            ticketera.abrir(set_codepage = pclases.config.get_codepageticket())
            linea0 = (" ", "RS")
            linea1 = (dde.nombre.center(ANCHO), "RSC")
            if isinstance(ticketera, LPTOKI):
                modo = ""
            else:
                modo = "RC"
            if pclases.config.get_mostrarcontactoenticket():
                linea2 = (dde.nombreContacto.center(ANCHO), modo)
            else:
                linea2 = ("", "")
            linea3 = (("NIF %s" % (dde.cif)).center(ANCHO), modo)
            linea4 = (("%s. Tlf: %s" % (dde.direccion, dde.telefono)).center(ANCHO), modo)
            linea5 = ("", [])
            lineas = [linea1, linea2, linea3, linea4, linea5]
            lineas.append((("Ticket %d - %s %s" % (ticket.numticket, 
                                                   utils.str_fecha(ticket.fechahora), 
                                                   utils.str_hora(ticket.fechahora))).center(ANCHO), "SI"))
            for ldv in ticket.lineasDeVenta:
                lineas.append((cortar_linea_ticket(ldv, ANCHO), ">"))
            lineas.append((total_ticket(ticket, ANCHO), "A"))
            lineas.append(("\nIVA incluido - Gracias por su visita", ""))
            for linea, modo in lineas:
                ticketera.escribir(linea, modo)
            for lineas_blanco in range(pclases.config.get_largoticket()):
                ticketera.escribir("", "")
            ticketera.cortar()
        finally:
            ticketera.cerrar()

def imprimir_arqueo(tickets):
    """
    Imprime las "cabeceras" de los tickets recibidos, agrupados por 
    fecha y el total de cada fecha.
    """
    DEBUG = pclases.DEBUG
    tickets = list(tickets)
    tickets.sort(lambda t1, t2: (t1.fechahora < t2.fechahora and -1) or
                                (t1.fechahora > t2.fechahora and 1) or
                                0)
    dias = {}
    total_totaloso = 0.0
    for t in tickets:
        dia = datetime.date(day = t.fechahora.day, 
                            month = t.fechahora.month, 
                            year = t.fechahora.year)
        if dia not in dias:
            dias[dia] = [t]
        else:
            dias[dia].append(t)
    ANCHO = pclases.config.get_anchoticket()
    puerto_lpt = pclases.config.get_puerto_ticketera()
    dias_in_orden = dias.keys()
    dias_in_orden.sort()
    if pclases.config.get_oki():
        ticketera = LPTOKI(puerto_lpt)
    else:
        ticketera = LPT(puerto_lpt)
    if DEBUG:
        from tempfile import gettempdir
        import os
        ticketera = LPT(os.path.join(gettempdir(), "salida_tpv.txt"))
    try:
        try:
            ticketera.abrir(set_codepage = pclases.config.get_codepageticket())
        except IOError, msg:
            utils.dialogo_info(titulo = "ERROR ABRIENDO PUERTO PARALELO", 
                               texto = "Ocurrió un error al abrir el puerto paralelo.\nProbablemente no cuente con permisos suficientes. Contacte con el administrador.") 
            raise IOError, msg
        for dia in dias_in_orden:
            total_dia = 0.0
            linea0 = (" ", "RS")
            linea1 = (utils.str_fecha(dia), "RSC")
            lineas = [linea0, linea1]
            for t in dias[dia]:
                texto = "%d - %s" % (t.numticket, 
                                     utils.str_hora(t.fechahora))
                subtotal = utils.float2str(t.calcular_total())
                texto += " "*(ANCHO - len(texto) - len(subtotal)) + subtotal
                lineas.append((texto, ">"))
                total_dia += t.calcular_total()
            total_totaloso += total_dia
            txt_total = utils.float2str(total_dia)
            linea_total = "TOTAL: %s" % txt_total
            lineas.append((linea_total, "DNA"))
            lineas.append(("", ""))
            for linea, modo in lineas:
                ticketera.escribir(linea, modo)
                if DEBUG: print linea, modo
        if len(dias.keys()) > 1:
            linea, modo = utils.float2str(total_totaloso), "CANS"
            ticketera.escribir(linea, modo)
            if DEBUG: print linea, modo
        for lineas_blanco in range(pclases.config.get_largoticket()):
            ticketera.escribir("", "")
        ticketera.cortar()
    finally:
        ticketera.cerrar()

def total_ticket(ticket, ancho):
    """
    Devuelve una cadena con el total del ticket.
    """
    total = "%s Euros" % (utils.float2str(ticket.calcular_total()))
    cad_total = "TOTAL %s" % total
    return "\n" + " " * (ancho - len(cad_total)) + cad_total

def cortar_linea_ticket(ldv, ancho, separador_lineas = ""):
    """
    Devuelve una cadena con la cantidad, producto y subtotal de 
    línea de la línea de venta.
    """
    IZQ = 5
    DER = 7
    CENDER = 6    # Centro derecha (precio unitario)
    CEN = ancho - IZQ - DER - CENDER - 3
    cant = utils.float2str(ldv.cantidad, 2, autodec = True)
    cant = " " * (IZQ - len(cant)) + cant
    precio = utils.float2str(ldv.precio * 1.18)
    precio = " " * (CENDER - len(precio)) + precio
    tot = utils.float2str(ldv.get_subtotal(iva = False) * 1.18)
    tot = " " * (DER - len(tot)) + tot
    try:
        desc = ldv.producto.descripcion
    except AttributeError:
        desc = ldv.concepto  # ¿Tal vez es un servicio?
    lineas = []
    i = 0
    while i < len(desc):
        lineas.append([" " * IZQ, desc[i:i+CEN], " " * CENDER, " " * DER])
        i += CEN
    lineas[0][0] = cant
    lineas[-1][1] = lineas[-1][1] + " " * (CEN - len(lineas[-1][1]))
    lineas[-1][2] = precio
    lineas[-1][3] = tot
    for i in xrange(len(lineas)):
        lineas[i] = "%s %s % s %s" % (lineas[i][0], lineas[i][1], lineas[i][2], lineas[i][3])
    texto = separador_lineas.join(lineas)
    return texto


# PLAN: Esto tiene pinta de que acabará en una clase aparte:
import os, tempfile
class LPT:
    """
    Clase para encapsular las operaciones con el puerto paralelo para 
    imprimir tickets.
    Si no se puede abrir el puerto porque no existe o no tiene una 
    impresora conectada, volcará todo a un fichero temporal para no 
    provocar errores en capas superiores.
    Si se desea saber si va a volcar datos a la impresora de tickets se 
    debe usar la función check() o bien usar el parámetro del constructor 
    «throw_exception» para capturar la excepción cuando no se encontró 
    impresora.
    """
    # FIXME: Al final el truco del os.open no vale. Si hay puerto paralelo, lo 
    # abre aunque después se quede esperando al hacerle el flush porque no 
    # haya dispositivo conectado a él para recoger esos datos. Al menos me 
    # he quitado el error cuando no hay o se intenta abrir el que no es.  
    def __init__(self, puerto = "/dev/lp0", throw_exception = False):
        self.__puerto = puerto
        self.__f = None
        try:
            self.__file_descriptor = os.open(puerto, os.O_WRONLY)
            os.close(self.__file_descriptor)
        except OSError, msg:
            if throw_exception:
                raise OSError, msg
            self.__file_descriptor = None
            self.__puerto = None

    def check(self):
        """
        Devuelve True si hay algo conectado al puerto abierto a lo que poder 
        escribir como si fuera un fichero.
        False si debes perder toda esperanza de que la impresora escupa un 
        mísero carácter en el rollo (más que nada porque fijo que no hay 
        impresora alguna).
        """
        return self.__file_descriptor != None

    def abrir(self, set_codepage = True):
        """
        Si set_codepage es False no intenta establecer la 
        codificación por defecto para la impresora.
        """
        try:
            self.__f = open(self.__puerto, "w")
        except TypeError:   # Lo da cuando open(None)
            self.__f = tempfile.TemporaryFile()
        if set_codepage:
            character_set = chr(0x1B) + chr(0x52) + chr(11)
            character_set = ""
            codepage = chr(0x1B) + chr(0x47) + chr(2)
            self.__f.write(character_set + codepage)
            self.__f.write("\n")
            self.__f.flush()

    def cortar(self, avanzar = True):
        if avanzar:
            self.avanzar(3)
        texto = chr(0x1B) + chr(0x6D)
        self.__f.write(texto)
        self.__f.write("\n")
        self.__f.flush()

    def abrir_cajon(self, serie = False):
        if not serie:
            #texto = chr(27) + chr(112) + chr(0) + chr(60) + chr(240)
            texto = chr(0x1B) + chr(0x70) + chr(0) + chr(60) + chr(240)
            #texto = chr(0x10) + chr(0x14) + chr(1) + chr(0) + chr(20)
            self.__f.write(texto)
            #self.__f.write("\n")
            self.__f.flush()
        else:
            import serial
            try:
                s = serial.Serial("COM1")
            except:
                s = serial.Serial("/dev/ttyS0")
            s.open()
            s.write("1")    # Cualquier cosa vale para activar el pin.
            s.close()
            del(s)

    def retroceder(self, n = 1):
        for i in xrange(n):
            texto = chr(0x1B) + chr(0x65) + chr(4)
            self.__f.write(texto)
            self.__f.write("\n")
            self.__f.flush()

    def insertar_retorno_de_carro(self):
        """
        Proof of concept. No usar.
        """
        texto = chr(0xA)
        self.__f.write(texto)
        self.__f.flush()

    def avanzar(self, n = 1):
        for i in xrange(n):
            texto = chr(0x1B) + chr(0x64) + chr(1)
            self.__f.write(texto)
            self.__f.write("\n")
            self.__f.flush()

    def _reset_textmode(self):
        "Modos normales para los modos soportados."
        textmode = ""
        textmode += chr(0x1B) + chr(0x61) + chr(0)
        textmode += chr(0x1B) + chr(0x47) + chr(0)
        textmode += chr(0x1B) + chr(0x45) + chr(0)
        textmode += chr(0x1B) + chr(0x2D) + chr(0)
        textmode += chr(0x1D) + "!" + chr(0x00)
        self.__f.write(textmode)
        self.__f.flush()        

    def _reparar_texto(self, t):
        """
        Devuelve el texto con las tildes y eñes reemplazadas 
        por caracteres ascii estándar.
        """
        return t.encode("cp850", "replace")

    def escribir(self, texto, modo = []):
        texto = self._reparar_texto(texto)
        textmode = ""
        if "R" in modo or "r" in modo:      # Resaltado
            textmode += chr(0x1B) + chr(0x45) + chr(1)
        else:
            textmode += chr(0x1B) + chr(0x45) + chr(0)
        if "N" in modo or "n" in modo:      # Negrita (doble resaltado)
            textmode += chr(0x1B) + chr(0x47) + chr(1)
        else:
            textmode += chr(0x1B) + chr(0x47) + chr(0)
        if "S" in modo or "s" in modo:      # Subrayado
            textmode += chr(0x1B) + chr(0x2D) + chr(1)
        else:
            textmode += chr(0x1B) + chr(0x2D) + chr(0)
        if "A" in modo or "a" in modo:      # Ancho (caracteres doble de ancho)
            textmode += chr(0x1D) + "!" + chr(0x11)
        else:
            textmode += chr(0x1D) + "!" + chr(0x00)
        if "I" in modo or "i" in modo:      # Texto justificado a la izquierda
            textmode += chr(0x1B) + chr(0x61) + chr(0)
            texto = texto.strip()   # No tienen sentido los espacios 
                # adicionales si la máquina lo va a justificar en el papel 
                # antes de imprimir la línea.
        if "C" in modo or "c" in modo:      # Texto centrado
            textmode += chr(0x1B) + chr(0x61) + chr(1)
            texto = texto.strip()   # No tienen sentido los espacios 
                # adicionales si la máquina lo va a centrar en el papel 
                # antes de imprimir la línea.
        if "D" in modo or "d" in modo:      # Texto justificado a la derecha
            textmode += chr(0x1B) + chr(0x61) + chr(2)
            texto = texto.strip()   # No tienen sentido los espacios 
                # adicionales si la máquina lo va a justificar en el papel 
                # antes de imprimir la línea.
        if not modo:
            textmode += chr(0x1B) + chr(0x61) + chr(0)
            textmode += chr(0x1B) + chr(0x47) + chr(0)
            textmode += chr(0x1B) + chr(0x45) + chr(0)
            textmode += chr(0x1B) + chr(0x2D) + chr(0)
            textmode += chr(0x1D) + "!" + chr(0x00)
        # Empezamos con los casos especiales. Si el modo es ">" el texto 
        # va con tipografía normal excepto la última palabra que va en negrita.
        if ">" in modo:
            self._reset_textmode()
            textmode = ""
            normal = chr(0x1B) + chr(0x47) + chr(0)
            negrita = chr(0x1B) + chr(0x47) + chr(1)
            hasta_ultimo_espacio = texto[:texto.rindex(" ")]
            ultima_palabra = texto[texto.rindex(" "):]
            texto = normal + hasta_ultimo_espacio + negrita + ultima_palabra
        self.__f.write(textmode + texto)
        self.__f.write("\n")
        self.__f.flush()
        #print(texto)

    def cerrar(self):
        try:
            self.__f.close()
        except AttributeError, msg:
            print "No se pudo cerrar el puerto porque probablemente no estaba abierto. AttributeError: %s" % (msg)

class LPTOKI(LPT):
    def __init__(self, puerto = "/dev/lp0"):
        self.__puerto = puerto
        self.__f = None

    def abrir(self, set_codepage = True):
        """
        Si set_codepage es False no intenta establecer la 
        codificación por defecto para la impresora.
        """
        self.__f = open(self.__puerto, "w")
        if set_codepage:
            codepage = chr(0x1B) + chr(0x1D) + chr(0x74) + chr(4)
            character_set = chr(0x1B) + chr(0x52) + chr(7)
            self.__f.write(character_set + codepage)
            self.__f.write("\n")
            self.__f.flush()

    def cortar(self, avanzar = True):
        if avanzar:
            self.avanzar(4)
        self.__f.write("\n")
        self.__f.flush()

    def abrir_cajon(self, serie = False):
        if not serie:
            texto = chr(0x1c) + chr(0x07) + chr(20) + chr(20)
            self.__f.write(texto)
            self.__f.flush()
        else:
            import serial
            try:
                s = serial.Serial("COM1")
            except:
                s = serial.Serial("/dev/ttyS0")
            s.open()
            s.write("1")    # Cualquier cosa vale para activar el pin.
            s.close()
            del(s)

    def retroceder(self, n = 1):
        self.__f.flush()

    def avanzar(self, n = 1):
        for i in xrange(n):
            texto = chr(0x1B) + chr(0x64) + chr(1)
            self.__f.write(texto)
            self.__f.write("\n")
            self.__f.flush()

    def _reset_textmode(self):
        "Modos normales para los modos soportados."
        textmode = ""
        textmode += chr(0x1B) + chr(0x4D)   # Fuente 7x9 (half dots).
        textmode += chr(0x14) # Cancela impresión expandida.
        textmode += chr(0x1B) + chr(0x68) + chr(0)  # Cancela altura doble.
        textmode += chr(0x1B) + chr(0x46) # Cancela negritas.
        textmode += chr(0x1B) + chr(0x2D) + chr(0) # Cancela subrayado.
        self.__f.write(textmode)
        self.__f.flush()        

    def _reparar_texto(self, t):
        """
        Devuelve el texto con las tildes y eñes reemplazadas 
        por caracteres ascii estándar.
        """
        return t.encode("cp850", "replace")

    def escribir(self, texto, modo = []):
        texto = self._reparar_texto(texto)
        textmode = ""
        if "R" in modo or "r" in modo:      # Resaltado (ancho doble)
            textmode += chr(0x1B) + chr(0x57) + chr(1)
        else:
            textmode += chr(0x1B) + chr(0x57) + chr(0)
        if "N" in modo or "n" in modo:      # Negrita (doble resaltado)
            textmode += chr(0x1B) + chr(0x45) 
        else:
            textmode += chr(0x1B) + chr(0x46) 
        if "S" in modo or "s" in modo:      # Subrayado
            textmode += chr(0x1B) + chr(0x2D) + chr(1)
        else:
            textmode += chr(0x1B) + chr(0x2D) + chr(0)
        if "A" in modo or "a" in modo:      # Ancho (caracteres doble de alto)
            textmode += chr(0x1B) + chr(0x68) + chr(1)
        else:
            textmode += chr(0x1B) + chr(0x68) + chr(0) 
        if "I" in modo or "i" in modo:      # Texto justificado a la izquierda
            textmode += chr(0x1B) + chr(0x1d) + chr(0x61) + chr(0)
            texto = texto.strip()   # No tienen sentido los espacios 
                # adicionales si la máquina lo va a justificar en el papel 
                # antes de imprimir la línea.
        if "C" in modo or "c" in modo:      # Texto centrado
            textmode += chr(0x1B) + chr(0x1d) + chr(0x61) + chr(1)
            texto = texto.strip()   # No tienen sentido los espacios 
                # adicionales si la máquina lo va a centrar en el papel 
                # antes de imprimir la línea.
        if "D" in modo or "d" in modo:      # Texto justificado a la derecha
            textmode += chr(0x1B) + chr(0x1d) + chr(0x61) + chr(2)
            texto = texto.strip()   # No tienen sentido los espacios 
                # adicionales si la máquina lo va a justificar en el papel 
                # antes de imprimir la línea.
        if not modo:
            textmode += chr(0x1B) + chr(0x68) + chr(0) 
            textmode += chr(0x1B) + chr(0x46) 
            textmode += chr(0x1B) + chr(0x2D) + chr(0)
            textmode += chr(0x1B) + chr(0x57) + chr(0)
        # Empezamos con los casos especiales. Si el modo es ">" el texto 
        # va con tipografía normal excepto la última palabra que va en negrita.
        if ">" in modo:
            self._reset_textmode()
            textmode = ""
            normal = chr(0x1B) + chr(0x46)
            negrita = chr(0x1B) + chr(0x45)
            hasta_ultimo_espacio = texto[:texto.rindex(" ")]
            ultima_palabra = texto[texto.rindex(" "):]
            texto = normal + hasta_ultimo_espacio + negrita + ultima_palabra
        self.__f.write(textmode + texto)
        self.__f.write("\n")
        self.__f.flush()
        #print(texto)

    def cerrar(self):
        try:
            self.__f.close()
        except AttributeError, msg:
            print "No se pudo cerrar el puerto porque probablemente no estaba abierto. AttributeError: %s" % (msg)

def pasar_foco_enter_cantidad(widget, event, boton, entry):
    """
    TODO: Falta docstring.
    """
    if event.keyval == 65293 or event.keyval == 65421:
        boton.clicked()
        entry.grab_focus()

def pasar_foco_enter(widget, event, wids, destino):
    """
    Pasa el foco al widget destino.
    """
    if event.keyval == 65293 or event.keyval == 65421:
        destino = wids[destino]    # Para evitar:
        # <gtk.Entry object at 0x1473aa0 (uninitialized at 0x0)>
        destino.grab_focus() 

def dialogo_nuevo_cliente(nombre, padre = None):
    res = [None]
    de = gtk.Dialog("DATOS DEL CLIENTE",
                    padre,
                    gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                    (gtk.STOCK_OK, gtk.RESPONSE_OK,
                     gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
    #-----------------------------------------------------------#
    def _respuesta_ok_cancel(dialog, response, res):
        if response == gtk.RESPONSE_OK:
            valores = []
            tabla_valores = dialog.vbox.get_children()[1]
            for hijo in tabla_valores.get_children():
                if isinstance(hijo, gtk.Entry):
                    entry = hijo
                    valores.append(entry.get_text())
            res[0] = valores.pop(0)
            for v in valores:
                res.append(v)
        else:
            res[0] = False
    #-----------------------------------------------------------#
    de.connect("response", _respuesta_ok_cancel, res)
    txt = gtk.Label("Introduzca los datos del nuevo cliente:")
    hbox = gtk.HBox(spacing = 5)
    icono = gtk.Image()
    icono.set_from_stock(gtk.STOCK_DIALOG_QUESTION, gtk.ICON_SIZE_DIALOG)
    hbox.pack_start(icono)
    hbox.pack_start(txt)
    de.vbox.pack_start(hbox)
    hbox.show_all()

    tabla = gtk.Table(7, 2)
    tabla.attach(gtk.Label("Nombre: "), 0, 1, 0, 1)
    tabla.attach(gtk.Label("CIF: "), 0, 1, 1, 2)
    tabla.attach(gtk.Label("Dirección: "), 0, 1, 2, 3)
    tabla.attach(gtk.Label("Código postal: "), 0, 1, 3, 4)
    tabla.attach(gtk.Label("Ciudad: "), 0, 1, 4, 5)
    tabla.attach(gtk.Label("Provincia: "), 0, 1, 5, 6)
    tabla.attach(gtk.Label("País: "), 0, 1, 6, 7)
    tabla.attach(gtk.Entry(), 1, 2, 0, 1)
    tabla.get_children()[0].set_text(nombre) # La lista de get_children es LIFO.
    tabla.attach(gtk.Entry(), 1, 2, 1, 2)
    tabla.attach(gtk.Entry(), 1, 2, 2, 3)
    tabla.attach(gtk.Entry(), 1, 2, 3, 4)
    tabla.attach(gtk.Entry(), 1, 2, 4, 5)
    tabla.get_children()[0].set_text("Marbella")
    tabla.attach(gtk.Entry(), 1, 2, 5, 6)
    tabla.get_children()[0].set_text("Málaga")
    tabla.attach(gtk.Entry(), 1, 2, 6, 7)
    tabla.get_children()[0].set_text("España")

    de.vbox.pack_start(tabla)
    tabla.show_all()
    de.set_transient_for(padre)
    de.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
    de.run()
    de.destroy()
    if res[0]==False:
        return None
    return res[::-1]

def crear_nuevo_cliente(nombre, padre = None):
    """
    Recibe un nombre y pide el resto de datos para 
    crear un nuevo cliente.
    Devuelve el id del cliente creado o None si se 
    cancela.
    «padre» es la ventana padre para los diálogos.
    """
    idcliente = None
    res = dialogo_nuevo_cliente(nombre, padre)
    if res != None:
        try:
            nombre, cif, direccion, cp, ciudad, provincia, pais = res
        except:
            nombre = None
    else:
        nombre = None
    if nombre:
        contadores = pclases.Contador.select(orderBy = "-id")
        if contadores.count():
            contador = contadores[0]
        else:
            contador = None
        try:
            cliente = pclases.Cliente(nombre = nombre,
                                      tarifaID = None,
                                      contador = contador,
                                      telefono = '',
                                      cif = cif,
                                      direccion = direccion,
                                      pais = pais,
                                      ciudad = ciudad,
                                      provincia = provincia,
                                      cp = cp,
                                      vencimientos = "0",
                                      iva = 0.18,
                                      direccionfacturacion = direccion,
                                      nombref = nombre,
                                      paisfacturacion = pais,
                                      ciudadfacturacion = ciudad,
                                      provinciafacturacion = provincia,
                                      cpfacturacion = cp,
                                      email = '',
                                      contacto = '',
                                      observaciones = "Creado desde el TPV.",
                                      documentodepago = "",
                                      diadepago = '',
                                      formadepago = '0',
                                      inhabilitado = False, 
                                      porcentaje = 0.0, 
                                      enviarCorreoAlbaran = False, 
                                      enviarCorreoFactura = False, 
                                      enviarCorreoPacking = False, 
                                      fax = '')
            idcliente = cliente.id
        except Exception, msg: # CIF duplicado o cualquier historia así.
            utils.dialogo_info(titulo = "ERROR", 
                texto = "Se produjo un error al crear el cliente:\n\n%s" % msg,
                padre = padre)
    return idcliente 

if __name__ == '__main__':
    t = TPV()


