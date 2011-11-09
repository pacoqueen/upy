#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008  Francisco José Rodríguez Bogado,                   #
#                          (frbogado@novaweb.es)                              #
#                                                                             #
# This file is part of $NAME                                                  #
#                                                                             #
# $NAME     is free software; you can redistribute it and/or modify           #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation; either version 2 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# $NAME     is distributed in the hope that it will be useful,                #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with $NAME    ; if not, write to the Free Software                    #
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA  #
###############################################################################

###################################################################
## up_asistencia.py - Ventana de asistencia a clase.
###################################################################
## NOTAS:
## 
###################################################################
from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, datetime, time
import sys
from os.path import join as pathjoin
from up_calendario import escalar_a
try:
    import pclases
except ImportError:
    sys.path.append(pathjoin("..", "framework"))
    import pclases
sys.path.append('.')
import ventana_progreso
import re
from utils import _float as float
from graficas import charting

class Asistencias(Ventana):
    def __init__(self, objeto = None, usuario = None, fecha = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        if not isinstance(objeto, (list, tuple)):
            self.lista_empleados = [objeto]
        else:
            self.lista_empleados = objeto
        self.fecha = fecha
        Ventana.__init__(self, 'up_asistencia.glade', objeto)
        self.usuario = usuario
        connections = {'b_salir/clicked': self.salir,
                       'b_imprimir/clicked': self.imprimir,
                       'cb_empleadoID/changed': self.actualizar, 
                       'b_refrescar/clicked': self.actualizar, 
                       'b_fecha/clicked': self.set_fecha, 
                      }
        self.inicializar_ventana()
        self.wids['e_fecha'] = utils.str_fecha(datetime.date.today())
        self.dia_seleccionado = self.get_fecha_mostrada()
        self.add_connections(connections)
        self.actualizar()
        gtk.main()

    def set_fecha(self, boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'], 
            fecha_defecto = self.wids['e_fecha'].get_text())
        self.wids['e_fecha'].set_text(utils.str_fecha(temp))
        self.actualizar()
    
    def inicializar_ventana(self, objeto = None):
        """
        Inicializa los widgets de la ventana.
        """
        pixbuf_logo = gtk.gdk.pixbuf_new_from_file(
            pathjoin("..", "imagenes", "logo_up.gif"))
        pixbuf_logo = escalar_a(200, 100, pixbuf_logo)
        self.wids['logo'].set_from_pixbuf(pixbuf_logo)
        cols = (('Grupo', 'gobject.TYPE_STRING', False, True, True, None),
                ('Asistencia','gobject.TYPE_BOOLEAN', True, False, True, 
                    self.actualizar_asistencia),
                ('id', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_asistencias'], cols)
        self.wids['tv_asistencias'].set_headers_visible(False)
        self.wids['tv_asistencias'].connect("row-activated", self.abrir_grupo)
        cats = pclases.CategoriaLaboral.selectBy(daClases = True)
        if self.lista_empleados and self.lista_empleados[0] != None:
            empleados = self.lista_empleados
        else:
            empleados = []
            for c in cats:
                for e in c.empleados:
                    if e not in empleados: empleados.append(e)
            empleados.sort(key = lambda e: e.apellidos)
        opciones = ([(0, "Todos")] + 
                    [(e.id, e.get_nombre_completo()) for e in empleados])
        utils.rellenar_lista(self.wids['cb_empleadoID'], opciones)
        #self.grafica = charting.add_grafica_rangos(self.wids['vbox2'], [], [])
        if (self.lista_empleados and self.lista_empleados[0] != None 
            and len(self.lista_empleados) == 1):
            utils.combo_set_from_db(self.wids['cb_empleadoID'], 
                                    self.lista_empleados[0].id)
        else:
            utils.combo_set_from_db(self.wids['cb_empleadoID'], 0)
        if not self.fecha:
            self.fecha = datetime.datetime.today()
        self.wids['e_fecha'].set_text(utils.str_fecha(self.fecha))
        self.wids['ventana'].resize(
            int(self.wids['ventana'].get_size()[0]*2), 
            self.wids['ventana'].get_size()[1]*2)

    def abrir_grupo(self, tv, path, cv, dia):
        """
        Abre el grupo al que se le ha hecho doble clic. Recibe el día, pero 
        no se llega a usar.
        """
        model = tv.get_model()
        puid = model[path][-1]
        objeto = pclases.getObjetoPUID(puid)
        if isinstance(objeto, pclases.Actividad):
            actividad = objeto
            grupo = actividad.grupoAlumnos
        elif isinstance(objeto, pclases.Asistencia):
            grupo = objeto.actividad.grupo
        elif isinstance(objeto, pclases.Cliente):
            puidgrupo = model[path].parent[-1]
            grupo = pclases.getObjetoPUID(puidgrupo)
        else:
            grupo = objeto
        if grupo:   # Es posible que no esté asignado, aunque en ese caso no 
                    # aparecería en el TreeView, pero por si las moscas.
            import grupos_alumnos
            v = grupos_alumnos.GruposAlumnos(grupo, usuario = self.usuario)

    def rellenar_widgets(self):
        """
        Rellena la información de los widgets, que es básicamente el 
        TreeView de alumnos a través del evento "changed" del profesor.
        """
        id = utils.combo_get_value(self.wids['cb_empleadoID'])
        if id > 0:
            self.lista_empleados = [pclases.Empleado.get(id)]
        elif id == 0:
            self.lista_empleados = [e for e in pclases.Empleado.select()]
        else:
            self.lista_empleados = []
        fecha = self.get_fecha_mostrada()
        dict_clases = self.rellenar_asistencias(fecha)
        self.actualizar_grafica(dict_clases)
        self.wids['tv_asistencias'].expand_all()

    def actualizar_grafica(self, dict_clases): 
        claves = []
        valores = []
        for e in self.lista_empleados:
            try:
                valores.append(dict_clases[e])
            except KeyError:    
                pass    # El empleado no tiene clases. No valores.
            else:
                claves.append(e.nombre)
        #self.grafica.plot(claves, valores, start_time = 8 * 60, 
        #                                   end_time = 22 * 60) 

    def rellenar_asistencias(self, fecha):
        """
        Rellena el TreeView de asistencias con los grupos y alumnos del día 
        seleccionado y el profesor del combo.
        Devuelve un diccionario de profesores con una lista de listas de 
        horas de inicio y fin de sus clases.
        """
        A = pclases.Actividad
        acts = A.select(pclases.NOT(pclases.OR(
                A.q.fechahoraInicio >= fecha + datetime.timedelta(days = 1), 
                A.q.fechahoraFin < fecha)), 
            orderBy = "fechahoraInicio")
        model = self.wids['tv_asistencias'].get_model()
        model.clear()
        dprofs = {}
        for a in acts:
            if a.empleado and a.empleado in self.lista_empleados:
                alumnos = a.clientes
                todos_asisten = len(a.asistencias) == len(alumnos)
                strgrupos = ", ".join([g.nombre for g in a.gruposAlumnos])
                fila = ("%s (%s) [%s]" 
                            % (strgrupos, a.get_hora_y_descripcion(), 
                               a.empleado and a.empleado.get_nombre_completo() 
                                or "Sin monitor"), 
                        todos_asisten, 
                        a.get_puid())
                horas_clase = (a.fechahoraInicio.hour * 60 
                               + a.fechahoraInicio.minute, 
                               a.fechahoraFin.hour * 60 
                               + a.fechahoraFin.minute)
                try:
                    dprofs[a.empleado].append(horas_clase)
                except KeyError:
                    dprofs[a.empleado] = [horas_clase]
                padre = model.append(None, fila)
                for alumno in alumnos:
                    asistencia = pclases.Asistencia.select(pclases.AND(
                        pclases.Asistencia.q.clienteID == alumno.id, 
                        pclases.Asistencia.q.actividadID == a.id))
                    asiste = asistencia.count()
                    fila = (alumno.nombre, asiste, alumno.get_puid())
                    model.append(padre, fila)
        return dprofs

    def actualizar_calendario(self, calendario):
        datecalendario = list(calendario.get_date())
        datecalendario[1] += 1
        try:
            self.dia_seleccionado = datetime.datetime(*datecalendario)
        except ValueError:
            pass    # Se le ha ido la pinza al calendario y todavía no ha 
                    # actualizado el mes al pasar de uno a otro haciendo clic
                    # directamente en el día del mes siguiente.
        else:
            self.actualizar()

    def actualizar(self, *args, **kw):
        """
        Wrapper para actualizar_ventana.
        """
        id = utils.combo_get_value(self.wids['cb_empleadoID'])
        if id > 0:
            self.lista_empleados = [pclases.Empleado.get(id)]
        elif id == 0:
            self.lista_empleados = [e for e in pclases.Empleado.select()]
        else:
            self.lista_empleados = None
        #self.actualizar_ventana()
        self.rellenar_widgets()

    def chequear_cambios(self):
        pass

    def guardar_grafica(self, nomfichero):
        grafica = self.grafica
        ancho, alto = grafica.window.get_geometry()[2:4]
        #i = gtk.gdk.Image(gtk.gdk.IMAGE_FASTEST, grafica.window.get_visual(), 
        #                  ancho, alto)
        #pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, ancho, alto)
        #i = grafica.window.copy_to_image(i, src_x = 0, src_y = 0, 
        #                                 dest_x = ancho, dest_y = alto, 
        #                                 width = ancho, height = alto)
        #pb = gtk.gdk.Pixbuf.get_from_image(i, src_x = 0, src_y = 0, 
        #                                   dest_x = 0, dest_y = 0, 
        #                                   width = ancho, height = alto)
        pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, ancho, alto) #@UndefinedVariable
        pb = pb.get_from_drawable(grafica.window, 
                                  cmap = grafica.window.get_colormap(), 
                                  src_x = 0, src_y = 0, 
                                  dest_x = 0, dest_y = 0, 
                                  width = ancho, height = alto)
        pb.save(nomfichero, "png")

    def imprimir(self,boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        if not self.lista_empleados:
            return 
        import sys, os, tempfile
        tmpdir = tempfile.gettempdir()
        nomfgraf = "%s.png" % (datetime.date.today().toordinal() * 100
                               + datetime.datetime.now().second)  
        ruta_grafica = os.path.join(tmpdir, nomfgraf)
        self.guardar_grafica(ruta_grafica)
        sys.path.append(os.path.join("..", "informes"))
        from treeview2pdf import treeview2pdf
        from informes import abrir_pdf
        nombre_empleado = ", ".join(
            [e.get_nombre_completo() for e in self.lista_empleados])
        abrir_pdf(treeview2pdf(self.wids['tv_asistencias'], 
                  titulo = "Lista de asistencia: %s" 
                                % nombre_empleado, 
                  fecha = self.get_fecha_mostrada().strftime("%d/%m/%Y"), 
                  graficos = [ruta_grafica]))

    def get_fecha_mostrada(self):
        """
        Devuelve la fecha mostrada en el calendario, que es la que se usa 
        para rescatar y presentar registros en la ventana.
        """
        dia_seleccionado = utils.parse_fecha(self.wids['e_fecha'].get_text())
        return dia_seleccionado
    
    def ir_semana_anterior(self, boton):
        """
        Desplaza el calendario una semana hacia atrás.
        """
        fecha = self.dia_seleccionado
        fecha -= datetime.timedelta(days = 7)
        self.wids['calendario'].select_month(fecha.month - 1, fecha.year)
        self.wids['calendario'].select_day(fecha.day)

    def ir_semana_siguiente(self, boton):
        """
        Desplaza el calendario una semana hacia adelante.
        """
        fecha = self.dia_seleccionado
        fecha += datetime.timedelta(days = 7)
        self.wids['calendario'].select_month(fecha.month - 1, fecha.year)
        self.wids['calendario'].select_day(fecha.day)

    def ir_a_hoy(self, boton):
        hoy = datetime.date.today()
        self.wids['calendario'].select_month(hoy.month - 1, hoy.year)
        self.wids['calendario'].select_day(hoy.day)

    def actualizar_asistencia(self, cell, path):
        """
        Crea o elimina un registro pclases.Asistencia en función de si se 
        marca o se desmarca la casilla del TreeView.
        """
        model = self.wids['tv_asistencias'].get_model()
        model[path][1] = not model[path][1]
        if model[path].parent:
            clientes = [pclases.getObjetoPUID(model[path][-1])]
            actividad = pclases.getObjetoPUID(model[path].parent[-1])
            # Es un alumno, actualizo el padre si todos asisten.
            z = model[path][1] and 1 or -1
            model[path].parent[1] = (
                len(actividad.asistencias) + z == len(actividad.clientes))
        else:
            actividad = pclases.getObjetoPUID(model[path][-1])
            clientes = actividad.clientes
            # Es todo el grupo. Actualizo sus hijos.
            for iterhijo in model[path].iterchildren():
                iterhijo[1] = model[path][1]
        if model[path][1]:
            for cliente in clientes:
                if cliente not in [a.cliente for a in actividad.asistencias]:
                    pclases.Asistencia(cliente = cliente, 
                                       actividad = actividad, 
                                       fechahora = datetime.datetime.today(), 
                                       observaciones = "")
        else:
            asistencias = [a for a in actividad.asistencias 
                           if a.cliente in clientes]
            for asistencia in asistencias:
                asistencia.destroySelf()


if __name__ == '__main__':
    cats = pclases.CategoriaLaboral.selectBy(daClases = True)
    empleados = []
    for c in cats:
        for e in c.empleados:
            if e not in empleados: empleados.append(e)
    t = Asistencias(objeto = empleados, 
                    #fecha = datetime.date(2010, 5, 13))
                    fecha = datetime.date.today())

