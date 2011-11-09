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
## consulta_compras.py -- 
###################################################################
##  
###################################################################
## Changelog:
## 27 de marzo de 2006 -> Inicio
## 18 de septiembre de 2006 -> Cambiada toda la ventana para 
##                             mostrar información más útil y de 
##                             otra manera.
###################################################################
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
from consulta_ventas_por_producto import convertir_a_listview    

class ConsultaCompras(Ventana):
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
        Ventana.__init__(self, 'consulta_compras.glade', objeto, usuario = usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_fecha_inicio/clicked': self.set_fecha,
                       'b_fecha_fin/clicked': self.set_fecha, 
                       'cbe_proveedor/changed': lambda *args, **kw: self.wids['tv_datos'].get_model().clear(), 
                       "b_exportar/clicked": self.exportar}
        self.add_connections(connections)
        cols = (('Fecha','gobject.TYPE_STRING',False,True,False,None),
                ('Albarán','gobject.TYPE_STRING',False,True,False,None),
                ('Código', 'gobject.TYPE_STRING', False, True, False, None),
                ('Descripción', 'gobject.TYPE_STRING', False, True, False, None),
                ('Cantidad', 'gobject.TYPE_STRING', False, True, False, None),
                ('Precio', 'gobject.TYPE_STRING', False, True, False, None),
                ('IVA', 'gobject.TYPE_STRING', False, True, False, None),
                ('Descuento', 'gobject.TYPE_STRING', False, True, False, None),
                ('Subtotal s/IVA', 'gobject.TYPE_STRING', False, True, False, None),
                ('Subtotal c/IVA', 'gobject.TYPE_STRING', False, True, False, None),
                ('Pedido', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Factura', 'gobject.TYPE_STRING', False, True, False, None), 
                ('IDLDC','gobject.TYPE_INT64',False,False,False,None))
        utils.preparar_treeview(self.wids['tv_datos'], cols)
        self.wids['tv_datos'].get_column(4).get_cell_renderers()[0].set_property('xalign', 1.0)
        self.wids['tv_datos'].get_column(5).get_cell_renderers()[0].set_property('xalign', 1.0)
        self.wids['tv_datos'].get_column(6).get_cell_renderers()[0].set_property('xalign', 1.0)
        self.wids['tv_datos'].get_column(7).get_cell_renderers()[0].set_property('xalign', 1.0)
        self.wids['tv_datos'].get_column(8).get_cell_renderers()[0].set_property('xalign', 1.0)
        self.wids['tv_datos'].get_column(9).get_cell_renderers()[0].set_property('xalign', 1.0)
        self.wids['tv_datos'].get_column(10).get_cell_renderers()[0].set_property('xalign', 0.5)
        self.wids['tv_datos'].get_column(11).get_cell_renderers()[0].set_property('xalign', 0.5)
        cols = (('Proveedor', 'gobject.TYPE_STRING', False, True, True, False), 
                ('Cantidad', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Total sin IVA','gobject.TYPE_STRING',False,True,False,False),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_proveedor'], cols)
        self.wids['tv_proveedor'].get_column(1).get_cell_renderers()[0].set_property('xalign', 1.0)
        self.wids['tv_proveedor'].get_column(2).get_cell_renderers()[0].set_property('xalign', 1.0)
        utils.rellenar_lista(self.wids['cbe_proveedor'], [(-1, "Todos los proveedores")] + [(p.id, p.nombre) 
            for p in pclases.Proveedor.select(pclases.Proveedor.q.inhabilitado == False, orderBy = "nombre")])
        self.fin = datetime.date.today()
        self.inicio = datetime.date(day = 1, month = self.fin.month, year = self.fin.year)
        self.wids['e_fechainicio'].set_text(utils.str_fecha(self.inicio))
        self.wids['e_fechafin'].set_text(utils.str_fecha(self.fin))
        gtk.main()

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
        tv = self.wids['tv_proveedor']
        abrir_csv(treeview2csv(tv))

    def chequear_cambios(self):
        pass

    def rellenar_tabla(self, 
                       albaranes, 
                       sin_albaran_por_proveedor, 
                       albaranesSalida):
    	"""
        Rellena el model con los items de la consulta
        """        
    	model = self.wids['tv_datos'].get_model()
    	model.clear()
        total = 0
    	for albaran in albaranes:
            padre = model.append(None, (utils.str_fecha(albaran.fecha), 
                                        albaran.numalbaran,
                                        "", 
                                        albaran.proveedor and albaran.proveedor.nombre or "") 
                                        + ("", )*8 + (albaran.id, ))
            totalalbaran = 0
            for ldc in albaran.lineasDeCompra:
                model.append(padre, ("", 
                                     "", 
                                     ldc.productoCompra.codigo, 
                                     ldc.productoCompra.descripcion, 
                                     utils.float2str(ldc.cantidad), 
                                     utils.float2str(ldc.precio, 4, autodec = True), 
                                     "%d %%" % (ldc.iva * 100), 
                                     "%s %%" % utils.float2str(ldc.descuento * 100, autodec = True), 
                                     utils.float2str(ldc.get_subtotal(iva = False), 3, autodec = False),
                                     utils.float2str(ldc.get_subtotal(iva = True), 3, autodec = False),
                                     ldc.pedidoCompra and ldc.pedidoCompra.numpedido or "", 
                                     ldc.facturaCompra and ldc.facturaCompra.numfactura or "", 
                                     ldc.id
                                    ))
                totalalbaran += ldc.get_subtotal(iva = True)
            model[padre][9] = utils.float2str(totalalbaran, 2)
            total += totalalbaran
        for proveedor in sin_albaran_por_proveedor:
            padre_sin_alb = model.append(None, ("", 
                                                "Facturas sin albarán",
                                                "", 
                                                proveedor != None 
                                                    and proveedor.nombre 
                                                    or "SIN PROVEEDOR") 
                                                + ("", )*8 + (proveedor.id, ))
            for factura in sin_albaran_por_proveedor[proveedor]:
                factura_padre = model.append(padre_sin_alb, 
                                                (utils.str_fecha(factura.fecha),
                                                 "", 
                                                 "", 
                                                 factura.proveedor 
                                                   and factura.proveedor.nombre 
                                                   or "")
                                                 + ("", ) * 5
                                                 + (utils.float2str(factura.calcular_importe_total()),)
                                                 + ("", )
                                                 + (factura.numfactura, 
                                                    factura.id))
                for ldc_o_srv in sin_albaran_por_proveedor[proveedor][factura]:
                    if isinstance(ldc_o_srv, pclases.LineaDeCompra):
                        total += self.insertar_en_model_ldc(ldc_o_srv, factura_padre, model)
                    elif isinstance(ldc_o_srv, pclases.ServicioTomado):
                        total += self.insertar_en_model_srv(ldc_o_srv, factura_padre, model)
        for albaran in albaranesSalida:
            padre = model.append(None, (utils.str_fecha(albaran.fecha), 
                                        albaran.numalbaran,
                                        "TRANSPORTE", 
                                        "Transporte no facturado (%s)." % (
                                            albaran.cliente 
                                            and albaran.cliente.nombre 
                                            or "Albarán sin cliente")) 
                                        + ("", )*8 + (albaran.id, ))
            totalalbaran = 0
            # Transportes no facturados aún:
            # OJO: Se supone, 1 transporte, 1 servicioTomado = 1 facturaCompra
            for ta in albaran.transportesACuenta:
                if not ta.serviciosTomados:
                    model.append(padre, ("", 
                                         "", 
                                         "", 
                                         ta.concepto, 
                                         "", 
                                         utils.float2str(ta.precio), 
                                         utils.float2str(ta.precio * 1.18), 
                                         "", 
                                         utils.float2str(ta.precio), 
                                         utils.float2str(ta.precio * 1.18), 
                                         "", 
                                         "", 
                                         ta.id))
                    totalalbaran += ta.precio * 1.18
            model[padre][9] = utils.float2str(totalalbaran, 2)
            total += totalalbaran
        self.wids['e_total'].set_text("%s €" % utils.float2str(total))

    def insertar_en_model_ldc(self, ldc, nodo_padre, model):
        model.append(nodo_padre, ("", 
                                  "", 
                                  ldc.productoCompra.codigo, 
                                  ldc.productoCompra.descripcion, 
                                  utils.float2str(ldc.cantidad), 
                                  utils.float2str(ldc.precio, 4, autodec = True), 
                                  "%d %%" % (ldc.iva * 100), 
                                  "%s %%" % utils.float2str(ldc.descuento * 100, autodec = True), 
                                  utils.float2str(ldc.get_subtotal(iva = False), 3, autodec = False),
                                  utils.float2str(ldc.get_subtotal(iva = True), 3, autodec = False),
                                  ldc.pedidoCompra and ldc.pedidoCompra.numpedido or "", 
                                  "", # Ya aparece en el nodo padre: ldc.facturaCompra and ldc.facturaCompra.numfactura or "", 
                                  ldc.id
                                 ))
        return ldc.get_subtotal(iva = True)

    def insertar_en_model_srv(self, servicio, nodo_padre, model):
        if servicio.transporteACuentaID != None:
            NumAlbaranSalida = servicio.transporteACuenta.albaranSalida.numalbaran
            albaran_salida = "Ntro. Alb. %s" % (NumAlbaranSalida)
            pedido = ""
        else:
            albaran_salida = ""
            pedido = ""
        totservicio = servicio.get_subtotal(iva = False)
        model.append(nodo_padre, ("", 
                                  albaran_salida,  
                                  "SERVICIO", 
                                  servicio.qconcepto, 
                                  utils.float2str(servicio.qcantidad), 
                                  utils.float2str(servicio.qprecio, 4, autodec = True), 
                                  "%s %%" % (utils.float2str(servicio.iva * 100, 0)), 
                                  "%s %%" % (utils.float2str(servicio.qdescuento * 100, 0)), 
                                  utils.float2str(totservicio, 3, autodec = True),
                                  utils.float2str(servicio.get_subtotal(iva = True), 3, autodec = True),
                                  pedido, 
                                  "", # Ya aparece en el nodo padre: servicio.facturaCompra and servicio.facturaCompra.numfactura or "", 
                                  servicio.id))
        return totservicio 

    def set_fecha(self, boton):
        """
        Muestra un calendario y pone la fecha seleccionada en el entry 
        que le corresponde al botón pulsado.
        """
        nombreboton = boton.get_name()
        if nombreboton == "b_fecha_inicio":
            entry = self.wids["e_fechainicio"]
        elif nombreboton == "b_fecha_fin":
            entry = self.wids["e_fechafin"]
        else:
            return
        fecha = utils.mostrar_calendario(fecha_defecto = utils.parse_fecha(entry.get_text()), padre = self.wids['ventana'])
        entry.set_text(utils.str_fecha(fecha))
        dia, mes, anno = fecha
        if nombreboton == "b_fecha_inicio":
            self.inicio = datetime.date(day = dia, month = mes, year = anno)
        elif nombreboton == "b_fecha_fin":
            self.fin = datetime.date(day = dia, month = mes, year = anno)

    def buscar(self,boton):
        """
        Dadas fecha de inicio y de fin, lista todos los albaranes
        pendientes de facturar.
        """
        idproveedor = utils.combo_get_value(self.wids['cbe_proveedor'])
        sin_albaran_por_proveedor = {}
        if idproveedor > 1:
            albaranes = pclases.AlbaranEntrada.select(
                pclases.AND(
                    pclases.AlbaranEntrada.q.fecha >= self.inicio,
                    pclases.AlbaranEntrada.q.fecha <= self.fin, 
                    pclases.AlbaranEntrada.q.proveedorID == idproveedor), 
                orderBy='fecha')
            ldcs = pclases.LineaDeCompra.select(
                pclases.AND(
                    pclases.LineaDeCompra.q.albaranEntradaID == None, 
                    pclases.LineaDeCompra.q.facturaCompraID 
                        == pclases.FacturaCompra.q.id, 
                    pclases.FacturaCompra.q.proveedorID == idproveedor, 
                    pclases.FacturaCompra.q.fecha >= self.inicio, 
                    pclases.FacturaCompra.q.fecha <= self.fin))
            srvs = pclases.ServicioTomado.select(
                pclases.AND(
                    pclases.ServicioTomado.q.facturaCompraID 
                        == pclases.FacturaCompra.q.id, 
                    pclases.FacturaCompra.q.proveedorID == idproveedor, 
                    pclases.FacturaCompra.q.fecha >= self.inicio, 
                    pclases.FacturaCompra.q.fecha <= self.fin))
        else:
            albaranes = pclases.AlbaranEntrada.select(
                pclases.AND(
                    pclases.AlbaranEntrada.q.fecha >= self.inicio,
                    pclases.AlbaranEntrada.q.fecha <= self.fin), 
                orderBy='fecha')
            ldcs = pclases.LineaDeCompra.select(
                pclases.AND(
                    pclases.LineaDeCompra.q.albaranEntradaID == None, 
                    pclases.LineaDeCompra.q.facturaCompraID 
                        == pclases.FacturaCompra.q.id, 
                    pclases.FacturaCompra.q.fecha >= self.inicio, 
                    pclases.FacturaCompra.q.fecha <= self.fin))
            srvs = pclases.ServicioTomado.select(
                pclases.AND(
                    pclases.ServicioTomado.q.facturaCompraID 
                        == pclases.FacturaCompra.q.id, 
                    pclases.FacturaCompra.q.fecha >= self.inicio, 
                    pclases.FacturaCompra.q.fecha <= self.fin))
        albaranesSalida = pclases.AlbaranSalida.select(
            pclases.AND(
                pclases.AlbaranSalida.q.fecha >= self.inicio,
                pclases.AlbaranSalida.q.fecha <= self.fin), 
            orderBy='fecha')
        albaranesSalida = [a for a in albaranesSalida if a.transportesACuenta]
        for ldc in ldcs:
            proveedor = ldc.facturaCompra.proveedor
            if proveedor not in sin_albaran_por_proveedor:
                sin_albaran_por_proveedor[proveedor]={ldc.facturaCompra: [ldc]}
            else:
                if ldc.facturaCompra not in sin_albaran_por_proveedor[proveedor]:
                    sin_albaran_por_proveedor[proveedor][ldc.facturaCompra] = [ldc]
                else:
                    sin_albaran_por_proveedor[proveedor][ldc.facturaCompra].append(ldc)
        for srv in srvs:
            proveedor = srv.facturaCompra.proveedor
            if proveedor not in sin_albaran_por_proveedor:
                sin_albaran_por_proveedor[proveedor] = {srv.facturaCompra: [srv]}
            else:
                if srv.facturaCompra not in sin_albaran_por_proveedor[proveedor]:
                    sin_albaran_por_proveedor[proveedor][srv.facturaCompra] = [srv]
                else:
                    sin_albaran_por_proveedor[proveedor][srv.facturaCompra].append(srv)
        self.resultado = list(albaranes)
        self.rellenar_tabla(self.resultado, 
                            sin_albaran_por_proveedor, 
                            albaranesSalida)
        self.rellenar_por_proveedor(self.resultado, 
                                    sin_albaran_por_proveedor, 
                                    albaranesSalida)

    def rellenar_por_proveedor(self, 
                               albaranes, 
                               sin_albaran_por_proveedor, 
                               albaranesSalida):
        """
        Rellena un TreeView donde los nodos padre son proveedores y los 
        hijos los productos comprados (por albarán o facturados -en el 
        diccionario sin_albaran_por_proveedor-), junto con un total en 
        euros.
        """
        proveedores = {}
        for p in sin_albaran_por_proveedor:
            if p not in proveedores:
                proveedores[p] = {}
            for factura in sin_albaran_por_proveedor[p]:
                for srv_o_ldc in sin_albaran_por_proveedor[p][factura]:
                    if isinstance(srv_o_ldc, pclases.ServicioTomado):
                        producto = srv_o_ldc.concepto
                    elif isinstance(srv_o_ldc, pclases.LineaDeCompra):
                        producto = srv_o_ldc.productoCompra.descripcion
                    else:
                        txt = "consulta_compras.py::rellenar_por_proveedor -> Ignorando objeto ID %d (%s) al mostrar compras por proveedor." % (srv_o_ldc.id, srv_o_ldc)
                        print "WARNING:", txt
                        self.logger.warning(txt)
                        continue
                    total_sin_iva = srv_o_ldc.get_subtotal()
                    if producto not in proveedores[p]:
                        proveedores[p][producto] = {
                            'euros_euros_dubidu': total_sin_iva, 
                            'cantidubidubida': srv_o_ldc.cantidad, 
                            'unidad': ""}
                    else:
                        proveedores[p][producto]['euros_euros_dubidu'] += total_sin_iva
                        proveedores[p][producto]['cantidubidubida'] += srv_o_ldc.cantidad
        for a in albaranes:
            p = a.proveedor
            if p not in proveedores:
                proveedores[p] = {}
            for ldc in a.lineasDeCompra:
                producto = ldc.productoCompra.descripcion
                total_sin_iva = ldc.get_subtotal()
                if producto not in proveedores[p]:
                    proveedores[p][producto] = {
                        'euros_euros_dubidu': total_sin_iva, 
                        'cantidubidubida': ldc.cantidad, 
                        'unidad': ldc.productoCompra.unidad}
                else:
                    proveedores[p][producto]['euros_euros_dubidu']+=total_sin_iva
                    proveedores[p][producto]['cantidubidubida'] += ldc.cantidad
        for a in albaranesSalida:
            p = None
            if p not in proveedores:
                proveedores[p] = {}
            for tac in a.transportesACuenta:
                producto = tac.concepto
                total_sin_iva = tac.precio
                if producto not in proveedores[p]:
                    proveedores[p][producto] = {
                        'euros_euros_dubidu': total_sin_iva, 
                        'cantidubidubida': ldc.cantidad, 
                        'unidad': ldc.productoCompra.unidad}
                else:
                    proveedores[p][producto]['euros_euros_dubidu']+=total_sin_iva
                    proveedores[p][producto]['cantidubidubida'] += ldc.cantidad
        model = self.wids['tv_proveedor'].get_model()
        model.clear()
        for p in proveedores:
            tot_prov = 0.0
            padre = model.append(None, (p and p.nombre or "Sin proveedor",
                                        "", 
                                        utils.float2str(tot_prov),
                                        p and p.id or -1))
            for desc_producto in proveedores[p]:
                tot_linea = proveedores[p][desc_producto]['euros_euros_dubidu']
                tot_cantidad = proveedores[p][desc_producto]['cantidubidubida']
                model.append(padre, (desc_producto, 
                                     "%s %s" % (
                                       utils.float2str(tot_cantidad), 
                                       proveedores[p][desc_producto]['unidad']),
                                     utils.float2str(tot_linea), 
                                     0))
                tot_prov += tot_linea
            model[padre][2] = utils.float2str(tot_prov)

    def imprimir(self,boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        from treeview2pdf import treeview2pdf
        from informes import abrir_pdf
        strfecha = "%s - %s" % (self.wids['e_fechainicio'].get_text(), self.wids['e_fechafin'].get_text())
        resp = utils.dialogo(titulo = "¿IMPRIMIR DESGLOSE?", 
                             texto = "Puede imprimir únicamente los albaranes o toda la información de la ventana.\n¿Desea imprimir también el contenido de los albaranes?", 
                             padre = self.wids['ventana'])
        if resp:
            tv = self.wids['tv_datos']
            tv.expand_all()
            while gtk.events_pending(): gtk.main_iteration(False)
            itertotal = tv.get_model().append(None, ("",)*8 + ("TOTAL", self.wids['e_total'].get_text()) + ("", )*2 + (0, ))
        else:
            tv = self.wids['tv_datos']
            tv.collapse_all()
            while gtk.events_pending(): gtk.main_iteration(False)
            tv = convertir_a_listview(tv)
            # Me sobran algunas columnas
            tv.remove_column(tv.get_columns()[2])
            tv.remove_column(tv.get_columns()[3])
            tv.remove_column(tv.get_columns()[3])
            tv.remove_column(tv.get_columns()[3])
            tv.remove_column(tv.get_columns()[3])
            tv.remove_column(tv.get_columns()[3])
            tv.remove_column(tv.get_columns()[-1])
            tv.remove_column(tv.get_columns()[-1])
            tv.get_column(2).set_title("Proveedor")
            model = tv.get_model()
            # Chapuza para mover los datos de la columna, pensaba que se eliminaban al quitar las columnas del TV.
            for fila in model:
                fila[2], fila[3] = fila[3],fila[9]
            itertotal = model.append(("", "", "TOTAL", self.wids['e_total'].get_text()) + ("", )*8 + (0, ) )
        idproveedor = utils.combo_get_value(self.wids['cbe_proveedor'])
        if idproveedor > 1:
            try:
                nomproveedor = pclases.Proveedor.get(idproveedor).nombre
            except:
                nomproveedor = "?"
        else:
            nomproveedor = "proveedores"
        abrir_pdf(treeview2pdf(tv, titulo = "Compras a %s" % (nomproveedor), fecha = strfecha))
        tv.get_model().remove(itertotal)
        if self.wids['notebook1'].get_current_page() == 0:
            self.wids['notebook1'].next_page()
            self.wids['notebook1'].realize()
            while gtk.events_pending(): gtk.main_iteration(False)
            self.wids['notebook1'].prev_page()
        abrir_pdf(treeview2pdf(self.wids['tv_proveedor'], 
                               titulo = "Compras por proveedor y producto", 
                               fecha = strfecha))

if __name__ == '__main__':
    t = ConsultaCompras()    
