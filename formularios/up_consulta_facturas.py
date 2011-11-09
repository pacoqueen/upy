#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008  Francisco José Rodríguez Bogado                    #
#                          (pacoqueen@users.sourceforge.net)                  #
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
## consulta_facturas.py 
###################################################################
## NOTAS:
##  - No cuenta tickets de caja ni prefacturas.
###################################################################
## Changelog:
## 
###################################################################
## 
###################################################################
from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time, sqlobject
import sys, os
try:
    import pclases
except ImportError:
    sys.path.append(os.path.join('..', 'framework'))
    import pclases
import datetime
try:
    import geninformes
except ImportError:
    sys.path.append(os.path.join('..', 'informes'))
    import geninformes
try:
    from treeview2pdf import treeview2pdf
except ImportError:
    sys.path.append(os.path.join("..", "informes"))
    from treeview2pdf import treeview2pdf
try:
    from treeview2csv import treeview2csv
except ImportError:
    sys.path.append(os.path.join("..", "informes"))
    from treeview2pdf import treeview2pdf
from informes import abrir_pdf, abrir_csv
import ventana_progreso
from tpv import cortar_linea_ticket, LPT, LPTOKI, total_ticket

class UPConsultaFacturas(Ventana):
    def __init__(self, objeto = None, usuario = None):
        Ventana.__init__(self, 'up_consulta_facturas.glade', objeto)
        self.usuario = usuario
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_exportar/clicked': self.exportar,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin, 
                       'b_ticket/clicked': self.imprimir_ticket, 
                       'tv_datos/cursor-changed': self.mostrar_info_factura}
        self.add_connections(connections)
        cols = (('Cliente','gobject.TYPE_STRING', False, True, False, None),
                ('Importe','gobject.TYPE_STRING', False, True, False, None),
                ('Fecha','gobject.TYPE_STRING', False, True, False, None),
                ('Pendiente de cobro','gobject.TYPE_STRING', 
                    False, True, False, None),
                ('PUID','gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_datos'], cols)
        self.wids['tv_datos'].connect("row-activated", self.abrir_factura)
        for col in (self.wids['tv_datos'].get_column(1), 
                    self.wids['tv_datos'].get_column(3)):
            for cell in col.get_cell_renderers():
                cell.set_property("xalign", 1.0)
        self.fin = datetime.date.today()
        self.inicio = datetime.date(day = 1, month = self.fin.month, 
                                    year = self.fin.year)
        self.wids['e_fechafin'].set_text(utils.str_fecha(self.fin))
        self.wids['e_fechainicio'].set_text(utils.str_fecha(self.inicio))
        gtk.main()

    def abrir_factura(self, tv, path, view_column):
        model = tv.get_model()
        puid = model[path][-1]
        if puid:
            objeto = pclases.getObjetoPUID(puid)
            if isinstance(objeto, pclases.FacturaVenta):
                fra = objeto 
                try:
                    import facturas_venta
                except ImportError:
                    from os.path import join as pathjoin
                    from sys import path
                    path.insert(0, pathjoin("..", "formularios"))
                    import facturas_venta
                ventana = facturas_venta.FacturasVenta(fra, self.usuario)
            elif isinstance(objeto, pclases.Cliente):
                cliente = objeto 
                try:
                    import clientes
                except ImportError:
                    from os.path import join as pathjoin
                    from sys import path
                    path.insert(0, pathjoin("..", "formularios"))
                    import clientes
                ventana_clientes = clientes.Clientes(cliente, self.usuario)


    def chequear_cambios(self):
        pass

    def rellenar_tabla(self, facturas):
        """
        Rellena el model con los items de la consulta
        """        
        model = self.wids['tv_datos'].get_model()
        model.clear()
        self.wids['tv_datos'].freeze_child_notify()
        self.wids['tv_datos'].set_model(None)
        for cliente in facturas:
            padre = model.append(None, (cliente and cliente.nombre 
                                            or "Sin cliente", 
                                        "0.00", 
                                        "", 
                                        "0.00", 
                                        cliente and cliente.get_puid() or ""))
            for factura in facturas[cliente]:
                formapago = factura.get_forma_de_pago()
                importe = factura.calcular_total()
                pdte = factura.calcular_pendiente_de_documento_de_pago()
                model[padre][1] = utils.float2str(utils._float(model[padre][1])
                    + importe)
                model[padre][3] = utils.float2str(utils._float(model[padre][3])
                    + pdte)
                model.append(padre, (factura.numfactura, 
                                     utils.float2str(importe), 
                                     utils.str_fecha(factura.fecha), 
                                     utils.float2str(pdte), 
                                     factura.get_puid()))
        self.wids['tv_datos'].set_model(model)
        self.wids['tv_datos'].thaw_child_notify()

    def set_inicio(self, boton):
        temp = utils.mostrar_calendario(fecha_defecto = self.inicio, 
                                        padre = self.wids['ventana'])
        self.inicio = datetime.date(day = temp[0], month = temp[1], 
                                    year = temp[2])
        self.wids['e_fechainicio'].set_text(utils.str_fecha(self.inicio))

    def set_fin(self, boton):
        temp = utils.mostrar_calendario(fecha_defecto = self.fin, 
                                        padre = self.wids['ventana'])
        self.fin = temp
        self.fin = datetime.date(day = temp[0], month = temp[1], 
                                 year = temp[2])
        self.wids['e_fechafin'].set_text(utils.str_fecha(self.fin))

    def buscar(self,boton):
        vpro = ventana_progreso.VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        self.resultado = {}
        facturas = pclases.FacturaVenta.select(pclases.AND(
            pclases.FacturaVenta.q.fecha >= self.inicio, 
            pclases.FacturaVenta.q.fecha <= self.fin))
        act = 0.0; tot = facturas.count()
        for f in facturas:
            vpro.set_valor(act/tot, "Buscando facturas...")
            cliente = f.cliente
            try:
                self.resultado[cliente].append(f)
            except KeyError:
                self.resultado[cliente] = [f]
        for c in self.resultado:
            self.resultado[c].sort(
                lambda f1, f2: utils.orden_por_campo_o_id(f1, f2, "fecha"))
        self.rellenar_tabla(self.resultado)
        vpro.ocultar()

    def imprimir(self, boton):
        """
        Prepara la vista preliminar para la impresión del informe.
        """
        tv = self.wids['tv_datos']
        strfecha = "De %s a %s" % (self.wids['e_fechainicio'].get_text(), 
                                   self.wids['e_fechafin'].get_text())
        abrir_pdf(treeview2pdf(tv, titulo = "Beneficio sobre tarifa", 
                               fecha = strfecha))

    def exportar(self, boton):
        """
        Exporta el TreeView a CSV.
        """
        abrir_csv(treeview2csv(self.wids['tv_datos']))

    def imprimir_ticket(self, boton):
        """
        Genera un ticket en texto plano y lo lanza a la impresora de tickets.
        """
        tv = self.wids['tv_datos']
        model, iter = tv.get_selection().get_selected()
        path = model.get_path(iter)
        puid = model[path][-1]
        if puid:
            try:
                objeto = pclases.getObjetoPUID(puid)
            except:
                return
            if isinstance(objeto, pclases.FacturaVenta):
                fra = objeto
                if utils.dialogo(titulo = "¿IMPRIMIR TICKET?", 
                        texto = "¿Desea imprimir el ticket?\n\n\n"
                                "Necesitará una impresora de tickets \n"
                                "encendida y conectada al puerto paralelo.\n"
                                "En otro caso se provocará un error.", 
                        padre = self.wids['ventana'], 
                        defecto = True, 
                        tiempo = 20): 
                    imprimir_ticket_from_factura(fra)
                self.preguntar_si_cobrado(fra)

    def preguntar_si_cobrado(self, factura):
        """
        Pregunta si marcar la factura como cobrada o dejarla pendiente si 
        la factura tiene algo efectivamente pendiente de cobro.
        """
        if not factura.calcular_pendiente_cobro():
            return
        res = utils.dialogo(titulo = "¿FACTURA COBRADA?", 
            texto = "¿Marcar la factura %s como cobrada?\n\nResponda «No» "
                    "para dejar los vencimientos como pendientes de cobro.\n"
                    "Responda «Sí» si ha cobrado el importe total de la "
                    "factura." % factura.numfactura, 
            padre = self.wids['ventana'])
        if res:
            for v in factura.vencimientosCobro:
                c = pclases.Cobro(prefactura = None, 
                    pagareCobro = None, 
                    facturaVenta = factura, 
                    cliente = factura.cliente, 
                    fecha = v.fecha, 
                    importe = v.importe, 
                    observaciones = 
                        "Cobrado desde ventana de tickets de factura.")

    def mostrar_info_factura(self, tv):
        """
        Rellena la información de la factura en los "entries": importe y forma 
        de pago.
        """
        model, iter = tv.get_selection().get_selected()
        if iter:
            path = model.get_path(iter)
            puid = model[path][-1]
            if puid:
                try:
                    objeto = pclases.getObjetoPUID(puid)
                except:
                    return
                if isinstance(objeto, pclases.FacturaVenta):
                    fra = objeto 
                    importe = fra.calcular_total()
                    formapago = fra.get_forma_de_pago()
                    self.wids['e_importe'].set_text(utils.float2str(importe))
                    self.wids['e_formapago'].set_text(formapago)

def imprimir_ticket_from_factura(fra):
    try:
        dde = pclases.DatosDeLaEmpresa.select()[0]
    except IndexError:
        print "tpv::imprimir_ticket -> No se encontraron los datos de la empresa. Abortando impresión..."
    else:
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
            lineas.append((("%s - %s" % (fra.numfactura, 
                                         utils.str_fecha(fra.fecha))
                           ).center(ANCHO), 
                          "SI")
                         )
            for ldv in fra.lineasDeVenta:
                lineas.append((cortar_linea_ticket(ldv, ANCHO), ">"))
            for srv in fra.servicios:
                lineas.append((cortar_linea_ticket(srv, ANCHO), ">"))
            lineas.append((total_ticket(fra, ANCHO), "A"))
            lineas.append(("\nIVA incluido", ""))
            if pclases.DEBUG:
                print "\n".join(lineas)
            for linea, modo in lineas:
                ticketera.escribir(linea, modo)
            for lineas_blanco in range(pclases.config.get_largoticket()):
                ticketera.escribir("", "")
            ticketera.cortar()
        finally:
            ticketera.cerrar()


if __name__ == '__main__':
    t = UPConsultaFacturas()

