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


class ConsultaClientesPorMes(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'up_listado_grupos.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_exportar/clicked': self.exportar}
        self.add_connections(connections)
        cols = (('Grupo', 'gobject.TYPE_STRING', False, True, False, None),
                ('Monitor', 'gobject.TYPE_STRING', False, True, True, None),
                ('Alumnos', 
                    'gobject.TYPE_STRING', False, True, False, None),
                ('PUID', 'gobject.TYPE_STRING', 
                    False, False, False, None))
        utils.preparar_treeview(self.wids['tv_datos'], cols)
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
        for g in items:
            alumnos = g.get_alumnos()
            padre = model.append(None, 
                        (g.nombre, 
                         g.empleado and g.empleado.get_nombre_completo(), 
                         "%d alumnos. Cupo: %d. En lista de espera: %d" % (
                            len(alumnos), g.cupo, 
                            len(g.clientes) - len(alumnos)), 
                         g.get_puid()))
            for cliente in alumnos:
                model.append(padre, ("", "", cliente.nombre, 
                                     cliente.get_puid()))

    def buscar(self, boton):
        """
        Dadas fecha de inicio y de fin, lista todos los albaranes
        pendientes de facturar.
        """
        grupos = pclases.GrupoAlumnos.select(orderBy = "nombre")
        self.rellenar_tabla(grupos)

    def imprimir(self, boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        import sys, os
        sys.path.append(os.path.join("..", "informes"))
        from treeview2pdf import treeview2pdf
        from informes import abrir_pdf
        tv = self.wids['tv_datos']
        abrir_pdf(treeview2pdf(tv))


if __name__ == '__main__':
    t = ConsultaClientesPorMes()

