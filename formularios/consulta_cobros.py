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
## consulta_cobros.py - Cobros y vencimientos de cobro (pendientes o no).
###################################################################
## NOTAS:
## Procede de consulta_pagos. Se conserva el código Logic por si 
## fuera necesario en una próxima versión.
###################################################################
## Changelog:
## 4 de abril de 2006 -> Inicio
## 17 de julio de 2006 -> Puesta a punto.
###################################################################
from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time
import sys
try:
    import pclases
except ImportError:
    from os.path import join as pathjoin; sys.path.append(pathjoin("..", "framework"))
    import pclases
import datetime
try:
    import geninformes
except ImportError:
    sys.path.append('../informes')
    import geninformes
sys.path.append('.')
import ventana_progreso
import re
from utils import _float as float


class ConsultaCobros(Ventana):
    inicio = None
    fin = None
    resultado = []
        
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        global fin
        Ventana.__init__(self, 'consulta_cobros.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin, 
                       'b_exportar/clicked': self.exportar}
        self.add_connections(connections)
        cols = (('Fecha','gobject.TYPE_STRING',False,True, True, None),
                ('Vencimientos','gobject.TYPE_STRING',False,False,False,None),
                ('Factura(Cliente)', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Cobros','gobject.TYPE_STRING',False,False,False,None),
                ('Factura(Cliente)', 'gobject.TYPE_STRING',
                    False, True, False, None),
                ('id','gobject.TYPE_STRING',False,False,False,None))
        utils.preparar_treeview(self.wids['tv_datos'], cols)
        col = self.wids['tv_datos'].get_column(1)
        for cell in col.get_cell_renderers():
            cell.set_property("xalign", 1)
        col = self.wids['tv_datos'].get_column(3)
        for cell in col.get_cell_renderers():
            cell.set_property("xalign", 1)
        cols2 = (('Forma de pago', 'gobject.TYPE_STRING', 
                    False, True, True, None),
                ('Factura', 'gobject.TYPE_STRING', False, False, False, None),
                ('Cliente', 'gobject.TYPE_STRING', False, True, False, None),
                ('Importe', 'gobject.TYPE_STRING', False, False, False, None),
                ('PUID', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_datos_cobros_formapago'], cols2)
        self.wids['tv_datos_cobros_formapago'].connect(
            "row-activated", self.abrir_factura)
        utils.preparar_treeview(self.wids['tv_datos_vtos_formapago'], cols2)
        self.wids['tv_datos_vtos_formapago'].connect(
            "row-activated", self.abrir_factura)
        temp = time.localtime()
        self.fin = str(temp[0])+'/'+str(temp[1])+'/'+str(temp[2])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        tempinicio = datetime.date.today() - datetime.timedelta(days = 1) * 30
        tempinicio = utils.str_fecha(tempinicio)
        self.inicio = tempinicio
        self.wids['e_fechainicio'].set_text(tempinicio)
        self.wids['e_estimados'].set_property('visible', False)
        self.wids['label8'].set_property('visible', False)
        gtk.main()

    def abrir_factura(self, tv, path, cv):
        """
        Abre la factura relacionada con el cobro o el vencimiento.
        """
        model = tv.get_model()
        puid = model[path][-1]
        if puid:
            objeto = pclases.getObjetoPUID(puid)
            factura = objeto.get_factura_o_prefactura()
            if isinstance(factura, pclases.FacturaVenta):
                import facturas_venta
                v = facturas_venta.FacturasVenta(factura, 
                                                 usuario = self.usuario)
            elif isinstance(factura, pclases.Prefactura):
                import prefacturas 
                v = prefacturas.Prefacturas(factura, 
                                            usuario = self.usuario)

    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        import sys, os
        sys.path.append(os.path.join("..", "informes"))
        from treeview2csv import treeview2csv
        from informes import abrir_csv
        tv = self.wids['tv_datos']
        abrir_csv(treeview2csv(tv))
        tv = self.wids['tv_datos_vtos_formapago']
        abrir_csv(treeview2csv(tv))
        tv = self.wids['tv_datos_cobros_formapago']
        abrir_csv(treeview2csv(tv))

    def chequear_cambios(self):
        pass

    def corregir_nombres_fecha(self, s):
        """
        Porque todo hombre debe enfrentarse al menos una 
        vez en su vida a dos tipos de sistemas operativos: 
        los que tienen en cuenta las locales y los que se 
        lo pasan por el forro.
        """
        trans = {'Monday': 'lunes',
                 'Tuesday': 'martes',
                 'Wednesday': 'miércoles',
                 'Thursday': 'jueves',
                 'Friday': 'viernes',
                 'Saturday': 'sábado',
                 'Sunday': 'domingo',
                 'January': 'enero',
                 'February': 'febrero',
                 'March': 'marzo',
                 'April': 'abril',
                 'May': 'mayo',
                 'June': 'junio',
                 'July': 'julio',
                 'August': 'agosto',
                 'September': 'septiembre',
                 'October': 'octubre',
                 'November': 'noviembre',
                 'December': 'diciembre'}
        for in_english in trans:
            s = s.replace(in_english, trans[in_english])
        return s

    def rellenar_tabla_por_forma_de_pago(self, cobros_por_forma_de_pago):
        model_cobros = self.wids['tv_datos_cobros_formapago'].get_model()
        model_vtos = self.wids['tv_datos_vtos_formapago'].get_model()
        model_cobros.clear()
        model_vtos.clear()
        for formadepago in cobros_por_forma_de_pago:
            if cobros_por_forma_de_pago[formadepago]['cobros']:
                padre = model_cobros.append(None, (formadepago, 
                                                   "", 
                                                   "", 
                                                   "0.0", 
                                                   None))
                for cobro in cobros_por_forma_de_pago[formadepago]['cobros']:
                    fra = cobro.get_factura_o_prefactura()
                    model_cobros.append(padre, ("", 
                                                fra.numfactura,
                                                fra.cliente.nombre, 
                                                cobro.importe, 
                                                cobro.get_puid()))
                    model_cobros[padre][3] = utils.float2str(utils.parse_float(
                        model_cobros[padre][3]) + cobro.importe)
            if cobros_por_forma_de_pago[formadepago]['vencimientos']:
                padre = model_vtos.append(None, (formadepago, 
                                                 "", 
                                                 "", 
                                                 "0.0", 
                                                 None))
                for vto in cobros_por_forma_de_pago[formadepago]['vencimientos']:
                    fra = vto.get_factura_o_prefactura()
                    model_vtos.append(padre, ("", 
                                              fra.numfactura,
                                              fra.cliente.nombre, 
                                              vto.importe, 
                                              vto.get_puid()))
                    model_vtos[padre][3] = utils.float2str(
                        utils.parse_float(model_vtos[padre][3]) + vto.importe)

    def rellenar_tabla_por_fecha(self, cobros_por_fecha):
    	"""
        Rellena el model con los items de la consulta.
        Elementos es un diccionario con objetos fecha como claves y 
        un diccionaro de dos cobros_por_fecha como valor. El segundo diccionario
        debe tener dos claves: 'cobros' y 'vencimientos'. En cada
        una de ellas se guarda una lista de objetos de la clase correspondiente.
        """        
    	model = self.wids['tv_datos'].get_model()
    	model.clear()
        cobros = 0
        vencimientos = 0
    	for fecha in cobros_por_fecha:
            sumvtos = 0 
            frasvtos = []
            cobrosvencimientos = cobros_por_fecha[fecha]
            for p in cobrosvencimientos['vencimientos']:
                if p.facturaVenta != None:
                    frasvtos.append("%s(%s)" % (p.facturaVenta.numfactura,                                             p.facturaVenta.cliente 
                                            and p.facturaVenta.cliente.nombre 
                                            or ""))
                if p.prefactura != None:
                    frasvtos.append("%s(%s)" % (p.prefactura.numfactura, 
                                        p.prefactura.cliente 
                                            and p.prefactura.cliente.nombre 
                                            or ""))
                sumvtos += p.importe
            sumcobros = 0 
            frascobros = []
            for p in cobrosvencimientos['cobros']:
                if p.facturaVenta != None:
                    frascobros.append("%s(%s)" % (p.facturaVenta.numfactura, 
                                        p.facturaVenta.cliente 
                                            and p.facturaVenta.cliente.nombre 
                                            or ""))
                if p.prefactura != None:
                    frascobros.append("%s(%s)" % (p.prefactura.numfactura, 
                                        p.prefactura.cliente 
                                            and p.prefactura.cliente.nombre 
                                            or ""))
                sumcobros += p.importe
            cobros += sumcobros
            vencimientos += sumvtos
            fras = ", ".join([f[:f.index("(")] for f in frasvtos])
            vtos = ", ".join([f[:f.index("(")] for f in frascobros])
            MAX_LINEA = 50
            padre = model.append(None, (utils.str_fecha(fecha), 
                                        utils.float2str(sumvtos), 
                                        len(fras) > MAX_LINEA 
                                            and "%s..." % fras[:MAX_LINEA-3] 
                                            or fras,
                                        utils.float2str(sumcobros),
                                        len(vtos) > MAX_LINEA 
                                            and "%s..." % vtos[:MAX_LINEA-3] 
                                            or vtos,
                                        ""))
            for i in xrange(max(len(cobrosvencimientos['cobros']), 
                                len(cobrosvencimientos['vencimientos']))):
                if i < len(cobrosvencimientos['cobros']):
                    p = cobrosvencimientos['cobros'][i]
                    if p.facturaVenta != None:
                        fracobro = "%s(%s)" % (p.facturaVenta.numfactura, 
                                        p.facturaVenta.cliente 
                                            and p.facturaVenta.cliente.nombre 
                                            or "")
                    if p.prefactura != None:
                        fracobro = "%s(%s)" % (p.prefactura.numfactura, 
                                        p.prefactura.cliente 
                                            and p.prefactura.cliente.nombre 
                                            or "")
                    importecobro = p.importe
                else:
                    importecobro = ""
                    fracobro = ""
                if i < len(cobrosvencimientos['vencimientos']):
                    p = cobrosvencimientos['vencimientos'][i]
                    if p.facturaVenta != None:
                        fravto = "%s(%s)" % (p.facturaVenta.numfactura, 
                                        p.facturaVenta.cliente 
                                            and p.facturaVenta.cliente.nombre 
                                            or "")
                    if p.prefactura != None:
                        fravto = "%s(%s)" % (p.prefactura.numfactura, 
                                        p.prefactura.cliente 
                                            and p.prefactura.cliente.nombre 
                                            or "")
                    importevto = p.importe
                else:
                    j = i - len(cobrosvencimientos['vencimientos'])
                    importevto = ""
                    fravto = ""
                model.append(padre, ("", 
                    importevto != "" and utils.float2str(importevto) or "",
                    fravto,
                    importecobro != "" and utils.float2str(importecobro) or "",
                    fracobro,
                    ""))
        total_pendiente = vencimientos - cobros
        self.wids['e_total'].set_text("%s €"%utils.float2str(total_pendiente))
        self.wids['e_cobros'].set_text("%s €" % utils.float2str(cobros))
        self.wids['e_vencimientos'].set_text(
            "%s €" % utils.float2str(vencimientos))
        
    def set_inicio(self,boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechainicio'].set_text(utils.str_fecha(temp))
        self.inicio = str(temp[2])+'/'+str(temp[1])+'/'+str(temp[0])

    def set_fin(self,boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        self.fin = str(temp[2])+'/'+str(temp[1])+'/'+str(temp[0])

    def por_fecha(self,e1,e2):
        """
        Permite ordenar una lista de cadenas de fecha
        """
        fecha1 = time.strptime(e1[0],"%d/%m/%Y")
        fecha2 = time.strptime(e2[0],"%d/%m/%Y")
        if fecha1 < fecha2:
            return -1
        elif fecha1 > fecha2:
            return 1
        else:
            return 0

    def buscar_cobros_y_vencimientos(self):
        """
        Busca y devuelve los objetos cobros y vencimientos entre las fechas 
        especificadas en la ventana.
        """
        if self.inicio == None:
            cobros = pclases.Cobro.select(
                pclases.Cobro.q.fecha <= self.fin, orderBy = 'fecha')
        else:
            cobros = pclases.Cobro.select(
                        pclases.AND(pclases.Cobro.q.fecha >= self.inicio,
                                    pclases.Cobro.q.fecha <= self.fin), 
                        orderBy = 'fecha')
        if self.inicio == None:
            vencimientos = pclases.VencimientoCobro.select(
                        pclases.VencimientoCobro.q.fecha <= self.fin, 
                        orderBy = 'fecha')
        else:
            vencimientos = pclases.VencimientoCobro.select(
                pclases.AND(pclases.VencimientoCobro.q.fecha >= self.inicio,
                pclases.VencimientoCobro.q.fecha <= self.fin), 
                orderBy = 'fecha')
        return cobros, vencimientos
        
    def buscar(self, boton):
        self.buscar_por_fecha()
        self.buscar_por_formapago()
    
    def buscar_por_fecha(self):
        """
        Busca cobros y vencimientos, los agrupa por fecha y rellena el 
        TreeView oportuno.
        """
        cobros, vencimientos = self.buscar_cobros_y_vencimientos()
        cobros_por_fecha = {}
        for item in cobros:
            if item.fecha not in cobros_por_fecha:
                cobros_por_fecha[item.fecha] = {'cobros': [], 
                                                'vencimientos': []} 
            cobros_por_fecha[item.fecha]['cobros'].append(item)
        for item in vencimientos:
            if item.fecha not in cobros_por_fecha:
                cobros_por_fecha[item.fecha] = {'cobros': [], 
                                                'vencimientos': []} 
            cobros_por_fecha[item.fecha]['vencimientos'].append(item)
        self.rellenar_tabla_por_fecha(cobros_por_fecha)
        
    def buscar_por_formapago(self):
        """
        Busca cobros y vencimientos, los agrupa por forma de pago y rellena el 
        TreeView oportuno.
        """
        cobros, vencimientos = self.buscar_cobros_y_vencimientos()
        cobros_por_forma_de_pago = {}
        for cobro in cobros:
            formadepago = cobro.get_formadepago()
            try:
                cobros_por_forma_de_pago[formadepago]['cobros'].append(cobro)
            except KeyError:
                cobros_por_forma_de_pago[formadepago] = {'cobros': [cobro], 
                                                         'vencimientos': []} 
        for vto in vencimientos:
            formadepago = vto.get_formadepago()
            try:
                cobros_por_forma_de_pago[formadepago]['vencimientos'].append(
                    vto)
            except KeyError:
                cobros_por_forma_de_pago[formadepago] = {'cobros': [], 
                                                         'vencimientos': [vto]} 
        self.rellenar_tabla_por_forma_de_pago(cobros_por_forma_de_pago)

    def imprimir(self,boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        import sys, os
        sys.path.append(os.path.join("..", "informes"))
        from treeview2pdf import treeview2pdf
        from informes import abrir_pdf
        strdiaini = self.wids['e_fechainicio'].get_text()
        strdiafin = self.wids['e_fechafin'].get_text()
        self.wids['tv_datos_cobros_formapago'].expand_all()
        self.wids['tv_datos_vtos_formapago'].expand_all()
        memento = self.wids['notebook1'].get_current_page()
        self.wids['notebook1'].set_current_page(1)
        while gtk.events_pending(): gtk.main_iteration(False)
        self.wids['notebook1'].set_current_page(2)
        while gtk.events_pending(): gtk.main_iteration(False)
        self.wids['notebook1'].set_current_page(memento)
        abrir_pdf(treeview2pdf(self.wids['tv_datos'], 
                        titulo = "Vencimientos y cobros por fecha", 
                        fecha = "Del %s al %s" % (strdiaini, strdiafin), 
                        extra_data = (("", "", "TOTAL COBROS: ", 
                                       self.wids['e_cobros'].get_text()), 
                                      ("", "", "TOTAL VENCIMIENTOS: ", 
                                       self.wids['e_vencimientos'].get_text()),
                                      ("", "", "TOTAL PENDIENTE DE COBRO: ", 
                                       self.wids['e_total'].get_text()))))
        abrir_pdf(treeview2pdf(self.wids['tv_datos_cobros_formapago'], 
                        titulo = "Cobros por forma de pago", 
                        fecha = "Del %s al %s" % (strdiaini, strdiafin), 
                        extra_data = ["TOTAL COBROS: ", 
                                      self.wids['e_cobros'].get_text()]))
        abrir_pdf(treeview2pdf(self.wids['tv_datos_vtos_formapago'], 
                        titulo = "Vencimientos por forma de pago", 
                        fecha = "Del %s al %s" % (strdiaini, strdiafin), 
                        extra_data = ["TOTAL VENCIMIENTOS: ", 
                                      self.wids['e_vencimientos'].get_text()]))


if __name__ == '__main__':
    t = ConsultaCobros()

