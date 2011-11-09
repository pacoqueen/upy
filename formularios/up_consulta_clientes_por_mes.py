#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008  Francisco José Rodríguez Bogado,                   #
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
## 
###################################################################
## NOTAS:
##
###################################################################
## Changelog:
## 
##
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time, sqlobject
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

# TODO: Filtro activo/inactivo/todos y total de clientes.

class ConsultaClientesPorMes(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'up_consulta_clientes_por_mes.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_fechainicio/clicked': self.set_inicio,
                       'b_fechafin/clicked': self.set_fin,
                       'b_exportar/clicked': self.exportar}
        self.add_connections(connections)
        cols = (('Mes', 'gobject.TYPE_STRING', False, True, False, None),
                ('Cliente', 'gobject.TYPE_STRING', False, True, True, None),
                ('Clases a las que asistió', 
                    'gobject.TYPE_STRING', False, True, False, None),
                ('PUDI_cliente', 'gobject.TYPE_STRING', 
                    False, False, False, None))
        utils.preparar_treeview(self.wids['tv_datos'], cols)
        col = self.wids['tv_datos'].get_column(2)
        for cell in col.get_cell_renderers():
            cell.set_property("xalign", 1)
        hoy = datetime.date.today()
        self.fechainicio = datetime.date(hoy.year, hoy.month, 1)
        for i in range(28, 32):
            try:
                self.fechafin = datetime.date(hoy.year, hoy.month, i)
            except ValueError:
                pass
        self.wids['e_fechainicio'].set_text(utils.str_fecha(self.fechainicio))
        self.wids['e_fechafin'].set_text(utils.str_fecha(self.fechafin))
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

    def chequear_cambios(self):
        pass

    def rellenar_tabla(self, items):
        """
        Rellena el model con los items de la consulta
        """
        model = self.wids['tv_datos'].get_model()
        model.clear()
        for anno in items:
            for mes in items[anno]:
                padre = model.append(None, ("%02d/%d" % (mes, anno), 
                                            "", 
                                            "", 
                                            ""))
                for cliente in items[anno][mes]:
                    asistencias = items[anno][mes][cliente]
                    model.append(padre, ("", cliente.nombre, asistencias, 
                                         cliente.get_puid()))

    def set_inicio(self, boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'], 
                                        fecha_defecto = self.fechainicio)
        self.wids['e_fechainicio'].set_text(utils.str_fecha(temp))
        self.fechainicio = datetime.date(*temp[::-1])

    def set_fin(self, boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'], 
                                        fecha_defecto = self.fechafin)
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        self.fechafin = datetime.date(*temp[::-1])

    def buscar(self, boton):
        """
        Dadas fecha de inicio y de fin, lista todos los albaranes
        pendientes de facturar.
        """
        res = {}
        asistencias = pclases.Asistencia.select(pclases.AND(
            pclases.Asistencia.q.fechahora >= self.fechainicio, 
            pclases.Asistencia.q.fechahora < (self.fechafin 
                                              + datetime.timedelta(days = 1))))
        for a in asistencias:
            anno = a.fechahora.year
            mes = a.fechahora.month
            if anno not in res:
                res[anno] = {}
            if mes not in res[anno]:
                res[anno][mes] = {}
            cliente = a.cliente
            try:
                res[anno][mes][cliente] += 1
            except KeyError:
                res[anno][mes][cliente] = 1
        self.rellenar_tabla(res)
        self.wids['tv_datos'].expand_all()

    def imprimir(self, boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        import sys, os
        sys.path.append(os.path.join("..", "informes"))
        from treeview2pdf import treeview2pdf
        from informes import abrir_pdf
        tv = self.wids['tv_datos']
        abrir_pdf(treeview2pdf(tv, apaisado = False, 
                               titulo = "Clientes activos", 
                               numcols_a_totalizar = [1, 2]))


if __name__ == '__main__':
    t = ConsultaClientesPorMes()

