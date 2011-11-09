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
import gtk, gtk.glade
try:
    import pclases
except ImportError:
    import sys
    from os.path import join as pathjoin
    sys.path.append(pathjoin("..", "framework"))
    import pclases
import datetime
try:
    import geninformes
except ImportError:
    import sys
    sys.path.append('../informes')
    import geninformes
from graficas import charting

RANGOS_EDAD = (0, 10, 20, 30, 40, 50, 60, 70, 80, 90) 
def build_str_rangos_edad(r):
    res = []
    i = 0
    for i in range(len(r)):
        try:
            cad = "De %d a %d" % (r[i], r[i+1] - 1) 
        except IndexError:
            cad = "Más de %d" % r[i] 
        res.append(cad)
    return res
STR_RANGOS_EDAD = build_str_rangos_edad(RANGOS_EDAD)


class EstadisticasClientes(Ventana):
    def __init__(self, objeto = None, usuario = None):
        self.usuario = usuario
        Ventana.__init__(self, 'up_estadisticas_clientes.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_exportar/clicked': self.exportar}
        self.add_connections(connections)
        cols = (('Variable', 'gobject.TYPE_STRING', False, True, True, None),
                ('Frecuencia', 'gobject.TYPE_INT', False, True, False, None),
                ('Porcentaje', 
                    'gobject.TYPE_STRING', False, True, False, None),
                ('PUID', 'gobject.TYPE_STRING', 
                    False, False, False, None))
        self.nombres_tv = ("tv_edad", "tv_profesion", "tv_sexo", "tv_clases", 
                           "tv_padecimientos")
        for nombre_tv in self.nombres_tv:
            utils.preparar_listview(self.wids[nombre_tv], cols)
        self.g_edad = charting.add_grafica_simple(self.wids['h_graficas1'], 
                                                  STR_RANGOS_EDAD, 
                                                  [0] * len(RANGOS_EDAD))
        #profesiones = [c.profesion.upper().strip() 
        #               for c in pclases.Cliente.select()]
        profesiones = []
        self.g_profesion = charting.add_grafica_barras_verticales(
            self.wids['h_grafica_p'], 
            profesiones, [0] * len(profesiones), 
            ver_botones_colores = False)
        self.g_sexo = charting.add_grafica_barras_horizontales(
            self.wids['h_graficas1'], 
            ("Masculino", "Femenino"), 
            [0, 0])
        #productos = [p.descripcion for p in pclases.ProductoCompra.select()]
        productos = []
        self.g_clases = charting.add_grafica_barras_verticales(
            self.wids['h_grafica_c'], 
            productos, [0] * len(productos), 
            ver_botones_colores = False)
        #padecimientos = [p.texto.upper().strip() 
        #                 for p in pclases.Padecimiento.select()] 
        padecimientos = []
        self.g_padecimientos = charting.add_grafica_barras_verticales(
            self.wids['h_grafica_d'], 
            padecimientos, [0] * len(padecimientos), 
            ver_botones_colores = False)
        self.wids['ventana'].maximize()
        gtk.main()

    def chequear_cambios(self):
        pass

    def rellenar_tabla(self, nombre_tv, items):
        """
        Rellena el model con los items de la consulta
        """
        model = self.wids[nombre_tv].get_model()
        model.clear()
        total = (sum([items[k] for k in items]))/100.0
        claves = items.keys()
        claves.sort()
        for var in claves:
            model.append((var, 
                          items[var], 
                          "%s %%" % utils.float2str(items[var]/total), 
                          ""))

    def buscar(self, boton):
        """
        Dadas fecha de inicio y de fin, lista todos los albaranes
        pendientes de facturar.
        """
        from ventana_progreso import VentanaProgreso
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        i = 0.0
        clientes = pclases.Cliente.selectBy(inhabilitado = False)
        tot = clientes.count()
        por_edad = dict(zip(STR_RANGOS_EDAD, map(lambda x: 0, STR_RANGOS_EDAD)))
        por_profesion = {}
        por_sexo = {"Masculino": 0, "Femenino": 0}
        por_clases = {}
        por_padecimientos = {}
        for c in clientes:
            vpro.set_valor(i / tot, "Generando estadísticas...")
            c.sync()    # Por si ha habido cambios en algún cliente.
            # Edad:
            rango_edad = determinar_rango_edad(c, RANGOS_EDAD)
            clave_edad = STR_RANGOS_EDAD[RANGOS_EDAD.index(rango_edad)]
            por_edad[clave_edad] += 1
            # Profesión: 
            profesion = c.profesion.upper().strip()
            try:
                por_profesion[profesion] += 1
            except KeyError:
                por_profesion[profesion] = 1
            # Clases:
            for pc in c.productosContratados:
                p = pc.productoCompra.descripcion
                try:
                    por_clases[p] += 1
                except KeyError:
                    por_clases[p] = 1
            # Sexo: 
            if c.sexoMasculino:
                por_sexo["Masculino"] += 1
            else:
                por_sexo["Femenino"] += 1
            # Padecimientos: 
            for pad in c.padecimientos:
                p = pad.texto.upper().strip()
                try:
                    por_padecimientos[p] += 1
                except KeyError:
                    por_padecimientos[p] = 1
            i += 1

        for ntv, res, graf in (("tv_edad", por_edad, self.g_edad), 
                               ("tv_profesion", 
                                por_profesion, 
                                self.g_profesion), 
                               ("tv_sexo", por_sexo, self.g_sexo), 
                               ("tv_clases", por_clases, self.g_clases), 
                               ("tv_padecimientos", 
                                por_padecimientos, 
                                self.g_padecimientos)):
            self.rellenar_tabla(ntv, res)
            self.actualizar_grafica(graf, res)
        vpro.ocultar()

    def actualizar_grafica(self, g, datos):
        claves = datos.keys()
        claves.sort()
        valores = [datos[k] for k in claves]
        try:
            g.plot(claves, valores)
        except TypeError, m:   # Es la gráfica simple. Otro formato de data.
            valores = [(k, datos[k]) for k in claves]
            g.plot(valores)

    def imprimir(self, boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        import sys, os
        sys.path.append(os.path.join("..", "informes"))
        from treeview2pdf import treeview2pdf
        from informes import abrir_pdf
        for ntv, grafica, titulo in zip(self.nombres_tv, 
                                        (self.g_edad, 
                                         self.g_profesion, 
                                         self.g_sexo, 
                                         self.g_clases, 
                                         self.g_padecimientos), 
                                        ("Clientes por edad", 
                                         "Clientes por profesión", 
                                         "Clientes por sexo", 
                                         "Clases contratadas", 
                                         "Padecimientos de clientes")):
            tv = self.wids[ntv]
            f_grafica = guardar_grafica(grafica)
            abrir_pdf(treeview2pdf(tv, 
                                   titulo = titulo, 
                                   graficos = [f_grafica]))

    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        import sys, os
        sys.path.append(os.path.join("..", "informes"))
        from treeview2csv import treeview2csv
        from informes import abrir_csv
        for ntv in self.nombres_tv:
            tv = self.wids[ntv]
            abrir_csv(treeview2csv(tv))


def guardar_grafica(grafica):
    """
    Guarda la gráfica en un PNG en el disco duro y devuelve el nombre del 
    archivo.
    """
    import tempfile
    tmpdir = tempfile.gettempdir()
    nomfichero = "%s%d.png" % (datetime.date.today().toordinal() * 100
                                + datetime.datetime.now().second, 
                               hash(grafica))
    ancho, alto = grafica.window.get_geometry()[2:4]
    pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, ancho, alto) 
    pb = pb.get_from_drawable(grafica.window, 
                              cmap = grafica.window.get_colormap(), 
                              src_x = 0, src_y = 0, 
                              dest_x = 0, dest_y = 0, 
                              width = ancho, height = alto)
    pb.save(nomfichero, "png")
    return nomfichero


def determinar_rango_edad(c, extremos):
    if isinstance(c, int):
        edad = c
    else:
        edad = c.calcular_edad()
    res  = 0
    for pivote in extremos:
        if pivote > edad:
            break
        res = pivote
    return res

if __name__ == '__main__':
    t = EstadisticasClientes()

