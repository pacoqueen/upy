#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2009-2010 Francisco José Rodríguez Bogado                     #
#                         (frbogado@novaweb.es)                               #
#                                                                             #
# This file is part of $NAME.                                                 #
#                                                                             #
# $NAME is free software; you can redistribute it and/or modify               #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation; either version 2 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# $NAME is distributed in the hope that it will be useful,                    #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with $NAME; if not, write to the Free Software                        #
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA  #
###############################################################################


###################################################################
## up_calendario.py - Ventana del calendario de actividades.
###################################################################
## NOTAS:
## TODO: Deseleccionar los TreeViews al terminar de editar o lo que 
##       sea para que no se quede en gris el evento.
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time
from os.path import join as pathjoin
try:
    import pclases
except ImportError:
    import sys
    sys.path.append(pathjoin("..", "framework"))
    import pclases
try:
    import geninformes
except ImportError:
    import sys
    sys.path.append('../informes')
    import geninformes
import time, datetime 
from utils import _float as float
from informes import abrir_pdf
from treeview2csv import get_campos_from_tv, get_datos_from_tv 
from treeview2pdf import treeview2pdf

class Calendario(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto). De no ser None, debe ser un 
        parte, y se mostrará la fecha correspondiente a ese parte.
        """
        self.usuario = usuario
        Ventana.__init__(self, 'up_calendario.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'calendario/day-selected': self.actualizar_calendario, 
                       'calendario/month-changed': self.actualizar_calendario, 
                       'b_hoy/clicked': self.ir_a_hoy, 
                       'b_add_todo/clicked': self.add_tarea, 
                       'b_drop_todo/clicked': self.drop_tarea, 
                       'b_add_memo/clicked': self.add_nota, 
                       'b_drop_memo/clicked': self.drop_nota, 
                       'b_nuevo/clicked': self.asignar_grupo_a_dia,
                       'b_borrar/clicked': self.borrar_actividad,
                       'b_atras/clicked': self.ir_semana_anterior, 
                       'b_atras2/clicked': self.ir_semana_anterior, 
                       'b_adelante/clicked': self.ir_semana_siguiente, 
                       'b_adelante2/clicked': self.ir_semana_siguiente, 
                       'cb_vista/changed': self.cambiar_vista, 
                       'b_imprimir/clicked': self.imprimir, 
                       'b_add_asistente/clicked': self.add_asistente, 
                       'b_drop_asistente/clicked': self.drop_asistente
                      }
        if not objeto:
            self.dia_seleccionado = datetime.date.today()
        else:
            self.dia_seleccionado = datetime.date(
                                      *objeto.fechahoraInicio.timetuple()[:3])
        self.inicializar_ventana(objeto)
        self.rellenar_widgets()
        self.add_connections(connections)
        gtk.main()

    def cambiar_vista(self, cb):
        vista = cb.get_active()
        if vista == 0:
            self.vista_diaria = True
        elif vista == 1:
            self.vista_diaria = False
        else:
            # PLAN: Montar vista mensual
            vista = 1
            self.vista_diaria = False
            cb.set_active(vista)
        self.rellenar_calendarios()

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

    def asignar_grupo_a_dia(self, boton):
        """
        Asigna un grupo a un día del calendario con la opción de repetirse 
        periódicamente en el tiempo mediante un objeto actividad.
        """
        #descripcion = utils.dialogo_entrada(titulo = "NUEVA ACTIVIDAD", 
        #    texto = "Introduzca un texto descriptivo:", 
        #    padre = self.wids['ventana'])
        opciones = [(g.id, g.nombre) 
                    for g in pclases.GrupoAlumnos.select(orderBy = "nombre")]
        opciones += [(-c.id, c.nombre) 
                    for c in pclases.Cliente.select(orderBy = "nombre")]
                # Debería ser pecado no guardar los apellidos por separado.
        idgrupo, texto = utils.dialogo_entrada_combo(
                    titulo = "NUEVA ACTIVIDAD", 
                    texto = "Seleccione un grupo de alumnos del despegable,\n"
                            "un alumno individual si se trata de una "
                            "sesión privada,\n"
                            "o un texto descriptivo:", 
                    padre = self.wids['ventana'], 
                    ops = opciones)
        if idgrupo != None and idgrupo > 0: # Es un grupo completo
            grupo = pclases.GrupoAlumnos.get(idgrupo)
            alumnos = [c for c in grupo.clientes 
                       if not grupo.en_lista_de_espera(c)]
            descripcion = grupo.nombre
            if not alumnos:
                utils.dialogo_info(titulo = "GRUPO VACÍO", 
                    texto = "El grupo %s no tiene alumnos. Se le\n"
                            "preguntará más adelante por los asistentes." 
                                % grupo.nombre, 
                    padre = self.wids['ventana'])
        elif idgrupo != None and idgrupo < 0:
            cliente = pclases.Cliente.get(-idgrupo)
            alumnos = [cliente]
            descripcion = cliente.nombre
        elif idgrupo == None and texto != None:
            alumnos = []
            descripcion = texto
        else:
            alumnos = []
            descripcion = None
        if not descripcion:
            return
        fecha_calendario = list(self.wids['calendario'].get_date()[::-1])
        fecha_calendario[1] += 1    # Empieza en mes 0 el gtk.Calendar
        fecha = utils.mostrar_calendario(fecha_calendario, 
                                         padre = self.wids['ventana'])
        fechadatetime = datetime.datetime(*fecha[::-1])
        int_diasemana = fechadatetime.weekday()
        for a in alumnos:
            if not getattr(a, pclases.Clase.listadias[int_diasemana]):
                utils.dialogo_info(titulo = "INCOMPATIBILIDAD DE HORARIOS", 
                    texto = "%s no puede asistir el %s (%s).\n"
                            "Revise su ficha de cliente." % (
                                a.nombre, 
                                pclases.Clase.listadias_str[int_diasemana], 
                                utils.str_fecha(fechadatetime)), 
                    padre = self.wids['ventana'])
                alumnos.remove(a)
        #if not alumnos:
        #    return
        # Debe poder seguir creando la actividad aunque no asista nadie. Ya 
        # se meterán alumnos más adelante.
        minutos_redondos=int(round(datetime.datetime.today().minute/10.0))*10
        horainicio = utils.mostrar_hora(horas = datetime.datetime.today().hour, 
                            minutos = minutos_redondos, 
                            titulo = "HORA DE INICIO", 
                            padre = self.wids['ventana'])
        if horainicio == None:
            return
        horafin = utils.mostrar_hora(int(horainicio.split(":")[0]) + 1, 
                                  minutos = int(horainicio.split(":")[1]), 
                                  titulo = "HORA DE FINALIZACIÓN", 
                                  padre = self.wids['ventana'])
        if horafin == None:
            return
        if not alumnos:
            opciones = [(g.id, g.nombre) for g 
                        in pclases.GrupoAlumnos.select(orderBy = "nombre")]
            opciones += [(-c.id, c.nombre) 
                        for c in pclases.Cliente.select(orderBy = "nombre")]
                    # Debería ser pecado no guardar los apellidos por separado.
            idgrupo = utils.dialogo_combo(titulo = "SELECCIONE ALUMNOS", 
                    texto = "Seleccione un grupo de alumnos del despegable \n"
                            "o un alumno individual si se trata de una "
                            "sesión privada:", 
                    padre = self.wids['ventana'], 
                    ops = opciones)
            if idgrupo != None and idgrupo > 0: # Es un grupo completo
                grupo = pclases.GrupoAlumnos.get(idgrupo)
                alumnos = [c for c in grupo.clientes 
                           if not grupo.en_lista_de_espera(c)]
            elif idgrupo != None and idgrupo < 0:
                cliente = pclases.Cliente.get(-idgrupo)
                alumnos = [cliente]
            else:
                alumnos = []
        opciones = [(e.id, e.nombre) 
                    for e in pclases.Evento.select(orderBy = "nombre")]
        opciones.insert(0, (0, "Sin evento relacionado"))
        idevento = utils.dialogo_combo(
                titulo = "SELECCIONE EVENTO RELACIONADO", 
                texto = "Seleccione un evento del despegable:", 
                    padre = self.wids['ventana'], 
                    ops = opciones, 
                    valor_por_defecto = 0)
        if idevento != None:
            if idevento != 0:
                evento = pclases.Evento.get(idevento)
            else:
                evento = None
            fecha = datetime.datetime(*fecha[::-1])
            repetir = utils.dialogo(titulo = "¿REPETIR ACTIVIDAD?", 
                texto = "¿Se repetirá la actividad periódicamente?", 
                padre = self.wids['ventana'])
            if repetir:
                hasta = utils.mostrar_calendario(
                                datetime.datetime.today() 
                                    + datetime.timedelta(days = 1) * 7,
                                titulo = "SELECIONE FECHA DE FINALIZACIÓN", 
                                padre = self.wids['ventana'])
                hasta = datetime.datetime(*hasta[::-1])
                #periodicidad = utils.dialogo_entrada(
                #    titulo = "INTRODUZCA PERIODICIDAD", 
                #    texto = "Introduzca el número de días entre cada"
                #            " repetición:", 
                #    valor_por_defecto = '1', 
                #    padre = self.wids['ventana'])
                periodicidad = 1
                dias = utils.dialogo_repeticion(padre = self.wids['ventana'])
                #if periodicidad == None:    # Canceló
                if dias == None:    # Canceló
                    return
                #try:
                #    periodicidad = utils.parse_numero(periodicidad)
                #except (ValueError, TypeError):
                #    utils.dialogo_info(titulo = "ERROR", 
                #        texto = "El texto «%s» no es un número.", 
                #        padre = self.wids['ventana'])
                #    return                  # Se equivocó
            else:
                hasta = fecha
                periodicidad = 1
                dias = range(7)
            while fecha <= hasta:
                #while fecha.weekday() >= 5:    # Es fin de semana
                #    fecha += datetime.timedelta(days = 1)
                while fecha.weekday() not in dias: 
                    fecha += datetime.timedelta(days = 1)
                fechahoraInicio = datetime.datetime(day = fecha.day, 
                                    month = fecha.month, 
                                    year = fecha.year, 
                                    hour = int(horainicio.split(":")[0]), 
                                    minute = int(horainicio.split(":")[1]))
                fechahoraFin = datetime.datetime(day = fecha.day, 
                                    month = fecha.month, 
                                    year = fecha.year, 
                                    hour = int(horafin.split(":")[0]), 
                                    minute = int(horafin.split(":")[1]))
                nueva_actividad = pclases.Actividad(evento = evento, 
                                  #grupoAlumnos = grupo, 
                                  fechahoraInicio = fechahoraInicio, 
                                  fechahoraFin = fechahoraFin, 
                                  descripcion = descripcion)
                for c in alumnos:
                    nueva_actividad.addCliente(c)
                fecha += datetime.timedelta(days = periodicidad)
            self.rellenar_calendarios()

    def borrar_actividad(self, boton):
        """
        Elimina la actividad que esté marcada en los TreeViews. Como 
        programáticamente se vigila que solo una actividad esté seleccionada a 
        la vez en los TreeViews, solo se eliminará esa. En cualquier caso, 
        si hubiera más, las eliminaría todas.
        """
        actualizar = False
        for dia in ("lunes", "martes", "miercoles", "jueves", "viernes", 
                    "sabado", "domingo"):
            tvdia = self.wids['tv_%s' % dia]
            sel = tvdia.get_selection()
            model, iter = sel.get_selected()
            if not iter:
                continue
            res = utils.dialogo(titulo = "¿BORRAR ACTIVIDAD?", 
                                texto = "¿Eliminar la actividad seleccionada?", 
                                padre = self.wids['ventana'])
            if not res:
                return
            puid = model[iter][-1]
            objeto = pclases.getObjetoPUID(puid)
            acts = buscar_actividades_periodicas_en_el_futuro(objeto)
            a_borrar = [objeto]
            if acts:
                res = utils.dialogo(titulo = "ACTIVIDAD PERIÓDICA", 
                    texto = "La actividad se repite %d veces en el futuro.\n"
                            "¿Desea eliminar esas repeticiones?" % len(acts), 
                    padre = self.wids['ventana'])
                if res:
                    a_borrar = [objeto] + acts
            for objeto in a_borrar:
                try:
                    objeto.destroySelf()
                    actualizar = True
                except Exception, e:
                    print e
                    if objeto.servicios:
                        fras = [srv.facturaVenta for srv in objeto.servicios]
                        numfactura = ", ".join([f.numfactura for f in fras])
                        res = utils.dialogo(
                            titulo = "¿BORRAR ACTIVIDAD FACTURADA?", 
                            texto = "La actividad se encuentra facturada.\n"
                                    "¿Desea eliminarla junto con los conceptos\n"
                                    "de las facturas: %s?" % (numfactura), 
                            padre = self.wids['ventana'])
                        if res:
                            if objeto.asistencias:
                                for a in objeto.asistencias:
                                    a.actividad = None
                                    a.destroySelf()
                            try:
                                objeto.destroy_en_cascada()
                            except Exception, e:
                                txt = "No se pudo borrar la actividad %s. "\
                                      "Excepción: %s" % (puid, e)
                                print txt
                                self.logger.error(txt)
                            else:
                                actualizar = True
                    if objeto.asistencias:
                        asis = [a.cliente.nombre for a in objeto.asistencias]
                        asistentes = ", ".join(asis)
                        res = utils.dialogo(
                            titulo = "¿BORRAR ACTIVIDAD?", 
                            texto = "A la actividad asistieron:.\n"
                                    "%s\n"
                                    "¿Aún desea borrarla?" % (asistentes), 
                            padre = self.wids['ventana'])
                        if res:
                            for a in objeto.asistencias:
                                a.actividad = None
                                a.destroySelf()
                            try:
                                objeto.destroy_en_cascada()
                            except Exception, e:
                                txt = "No se pudo borrar la actividad %s. "\
                                      "Excepción: %s" % (puid, e)
                                print txt
                                self.logger.error(txt)
                            else:
                                actualizar = True
        if actualizar:
            self.rellenar_calendarios()

    def add_nota(self, boton):
        model = self.wids['tv_notas'].get_model()
        resumen = utils.dialogo_entrada(titulo = "NUEVA NOTA", 
            texto = "Introduzca el resumen de la nueva nota:", 
            padre = self.wids['ventana'])
        if resumen == None:
            return
        texto = utils.dialogo_entrada(titulo = "NUEVA NOTA", 
            texto = "Introduzca el texto de la nueva nota:", 
            padre = self.wids['ventana'], 
            textview = True)
        if texto == None:
            return
        opciones = [(e.id, e.nombre) 
                    for e in pclases.Categoria.select(orderBy = "nombre")]
        opciones.insert(0, (0, "Sin categoría relacionada"))
        idcategoria = utils.dialogo_combo(titulo = "SELECCIONE CATEGORÍA:", 
            texto = "Seleccione una categoría de la lista:", 
            ops = opciones, 
            padre = self.wids['ventana'], 
            valor_por_defecto = 0)
        if idcategoria != None:
            if idcategoria == 0:
                categoria = None
            else:
                categoria = pclases.Categoria.get(idcategoria)
        else:
            return
        memo = pclases.Memo(categoria = categoria, 
                            resumen = resumen, 
                            texto = texto)
        model.append((memo.resumen, memo.texto, memo.get_puid()))

    def drop_nota(self, boton):
        sel = self.wids['tv_notas'].get_selection()
        model, iters = sel.get_selected_rows()
        if not iters:
            return
        res = utils.dialogo(titulo = "¿BORRAR ANOTACIÓN?", 
                            texto = "¿Eliminar la nota seleccionada?", 
                            padre = self.wids['ventana'])
        if not res:
            return
        for iter in iters:
            puid = model[iter][-1]
            objeto = pclases.getObjetoPUID(puid)
            try:
                objeto.destroySelf()
            except Exception, e:
                txt = "No se pudo borrar el memo %s. Excepción: %s" % (puid, e)
                print txt
                self.logger.error(txt)
        self.rellenar_notas()

    def add_tarea(self, boton):
        resumen = utils.dialogo_entrada(titulo = "NUEVA TAREA", 
            texto = "Introduzca el resumen de la nueva tarea:", 
            padre = self.wids['ventana'])
        if resumen == None:
            return
        texto = utils.dialogo_entrada(titulo = "NUEVA TAREA", 
            texto = "Introduzca el texto de la nueva tarea:", 
            padre = self.wids['ventana'], 
            textview = True)
        if texto == None:
            return
        model = self.wids['tv_tareas'].get_model()
        opciones = [(e.id, e.nombre) 
                    for e in pclases.Categoria.select(orderBy = "nombre")]
        opciones.insert(0, (0, "Sin categoría relacionada"))
        idcategoria = utils.dialogo_combo(titulo = "SELECCIONE CATEGORÍA:", 
            texto = "Seleccione una categoría de la lista:", 
            ops = opciones, 
            padre = self.wids['ventana'], 
            valor_por_defecto = 0)
        if idcategoria != None:
            if idcategoria == 0:
                categoria = None
            else:
                categoria = pclases.Categoria.get(idcategoria)
        else:
            return
        tarea = pclases.Tarea(categoria = categoria, 
                              resumen = resumen, 
                              texto = texto, 
                              fechaLimite = None, 
                              fechaDone = None)
        model.append((tarea.fechaDone != None, 
                      tarea.resumen, 
                      tarea.texto, 
                      utils.str_fecha(tarea.fechaLimite), 
                      tarea.get_puid()))

    def drop_tarea(self, boton):
        sel = self.wids['tv_tareas'].get_selection()
        model, iters = sel.get_selected_rows()
        if not iters:
            return
        res = utils.dialogo(titulo = "¿BORRAR TAREA?", 
                            texto = "¿Eliminar la tarea seleccionada?", 
                            padre = self.wids['ventana'])
        if not res:
            return
        for iter in iters:
            puid = model[iter][-1]
            objeto = pclases.getObjetoPUID(puid)
            try:
                objeto.destroySelf()
            except Exception, e:
                txt = "No se pudo borrar la tarea %s. Excepción: %s" % (puid, e)
                print txt
                self.logger.error(txt)
        self.rellenar_tareas()

    def add_asistente(self, boton):
        for dia in ("lunes", "martes", "miercoles", "jueves", "viernes", 
                    "sabado", "domingo"):
            tvdia = self.wids['tv_%s' % dia]
            sel = tvdia.get_selection()
            model, iter = sel.get_selected()
            if pclases.DEBUG:
                print dia, iter
            if not iter:
                continue
            # Añado a todos los iter seleccionados (en teoría solo 1)
            actividad = pclases.getObjetoPUID(model[model.get_path(iter)][-1])
            self.asignar_privada(None, self.wids['tv_asistentes'], 
                                 self.usuario, actividades = [actividad])

    def drop_asistente(self, boton):
        sel = self.wids['tv_asistentes'].get_selection()
        model, paths = sel.get_selected_rows()
        clientes = []
        for path in paths:
            clientes.append(pclases.getObjetoPUID(model[path][-1]))
        if clientes:
            for dia in ("lunes", "martes", "miercoles", "jueves", "viernes", 
                        "sabado", "domingo"):
                tvdia = self.wids['tv_%s' % dia]
                sel = tvdia.get_selection()
                model, iter = sel.get_selected()
                if pclases.DEBUG:
                    print dia, iter
                if not iter:
                    continue
                # Elimino de todos los iter seleccionados (en teoría solo 1)
                actividad = pclases.getObjetoPUID(
                    model[model.get_path(iter)][-1])
                for c in clientes:
                    actividad.removeCliente(c)
                # [21] Semiprivadas:
                if len(actividad.clientes) == 2:
                    actividad.descripcion = "[Semipriv.] %s + %s" % (
                        actividad.clientes[0].nombre, 
                        actividad.clientes[1].nombre)
                elif (len(actividad.clientes) == 1 
                      and "Semipriv" in actividad.descripcion):
                    actividad.descripcion = "[Priv.] %s" % (
                        actividad.clientes[0].nombre)
            self.actualizar_calendario()

    def finalizar_tarea(self, cell, path):
        model = self.wids['tv_tareas'].get_model()
        model[path][0] = not model[path][0]
        tarea = pclases.getObjetoPUID(model[path][-1])
        if model[path][0]:
            tarea.fechaDone = datetime.datetime.today()
        else:
            tarea.fechaDone = None
        tarea.sync()

    def ir_a_hoy(self, boton):
        hoy = datetime.date.today()
        self.wids['calendario'].select_month(hoy.month - 1, hoy.year)
        self.wids['calendario'].select_day(hoy.day)

    def actualizar_calendario(self, calendario = None):
        if calendario is None:
            calendario = self.wids['calendario']
        datecalendario = list(calendario.get_date())
        datecalendario[1] += 1
        self.dia_seleccionado = datetime.date(*datecalendario)
        self.rellenar_calendarios()

    # --------------- Funciones auxiliares ------------------------------
    def inicializar_ventana(self, objeto = None):
        """
        Inicializa los widgets de la ventana.
        """
        self.colores = {}
        # [02] Vista diaria por defecto:
        self.wids['cb_vista'].set_active(0)
        self.vista_diaria = True
        #self.wids['cb_vista'].set_active(1)
        # [02] EOVista diaria por defecto.
        self.wids['ventana'].set_title("CALENDARIO DE ACTIVIDADES")
        pixbuf_logo = gtk.gdk.pixbuf_new_from_file(
            pathjoin("..", "imagenes", "logo_up.gif"))
        pixbuf_logo = escalar_a(200, 100, pixbuf_logo)
        self.wids['logo'].set_from_pixbuf(pixbuf_logo)
        cols = (("Hora", "gobject.TYPE_STRING", True, False, False, 
                    self.cambiar_hora_actividad), 
                ("Actividad", "gobject.TYPE_STRING", True, False, False, 
                    self.cambiar_nombre_actividad),
               ("PUID", "gobject.TYPE_STRING", False, False, False, None))
        for dia in ("lunes", "martes", "miercoles", "jueves", "viernes", 
                    "sabado", "domingo"):
            tvdia = self.wids['tv_%s' % dia]
            utils.preparar_listview(tvdia, cols)
            tvdia.set_headers_visible(False)
            tvdia.connect("cursor-changed", self.quitar_seleccion, dia)
            tvdia.connect("row-activated", self.abrir_grupo, dia)
            self.attach_menu_asignar(tvdia, 
                                     self.wids['ventana'], 
                                     self.usuario)
        self.wids['calendario'].select_day(self.dia_seleccionado.day)
        self.wids['calendario'].select_month(self.dia_seleccionado.month - 1, 
                                             self.dia_seleccionado.year)
        # Inicialización de grupos y eventos.
        cols = (("Color", "gobject.TYPE_STRING", False, False, False, None), 
                ("Ver", "gobject.TYPE_BOOLEAN", True, True, False, 
                    self.ver_o_no_ver_grupo), 
                ("Nombre", "gobject.TYPE_STRING", True, True, True, 
                    self.cambiar_nombre_grupo),
                ("ID", "gobject.TYPE_STRING", False, False, False, None))
        utils.preparar_treeview(self.wids['tv_grupos'], cols)
        self.wids['tv_grupos'].set_headers_visible(False)
        col = self.wids['tv_grupos'].get_column(2)
        cells = col.get_cell_renderers()
        for cell in cells:
            col.set_attributes(cell, markup = 2)
        self.colorear_calendario()
        self.wids['tv_grupos'].connect("row-activated", 
                                       self.abrir_grupo_o_profesor)
        # Prefiero los botones atrás/adelante de arriba.
        self.wids['b_atras2'].set_property("visible", False)
        self.wids['b_adelante2'].set_property("visible", False)
        # Tareas
        cols = (("Finalizada", "gobject.TYPE_BOOLEAN", True, True, False, 
                    self.finalizar_tarea),
                ("Resumen", "gobject.TYPE_STRING", False, False, False, None), 
                ("Texto", "gobject.TYPE_STRING", False, False, False, None), 
                ("Fecha límite", "gobject.TYPE_STRING", 
                    False, False, False, None), 
                #("Fecha finalización", "gobject.TYPE_STRING", 
                #    False, False, False, None), 
                ("PUID", "gobject.TYPE_STRING", False, False, False, None))
        utils.preparar_listview(self.wids['tv_tareas'], cols)
        # Notas
        cols = (("Resumen", "gobject.TYPE_STRING", False, False, False, None), 
                ("Texto", "gobject.TYPE_STRING", False, False, False, None), 
                ("PUID", "gobject.TYPE_STRING", False, False, False, None))
        utils.preparar_listview(self.wids['tv_notas'], cols)
        self.wids['ventana'].maximize()
        self.wids['hpaned1'].set_position(
            int(self.wids['ventana'].get_screen().get_width()*0.7))
        # Asistentes:
        cols = (("Asistentes", "gobject.TYPE_STRING", 
                    False, False, False, None), 
                ("PUID", "gobject.TYPE_STRING", False, False, False, None))
        utils.preparar_listview(self.wids['tv_asistentes'], cols, multi = True)
        self.wids['tv_asistentes'].connect("row-activated", 
                                            self.abrir_cliente, dia)

    def abrir_grupo_o_profesor(self, tv, path, cv):
        """
        Abre la ventana de grupos o de profesores en función de la fila a 
        la que se le ha hecho doble clic.
        """
        model = tv.get_model()
        puid = model[path][-1]
        try:
            objeto = pclases.getObjetoPUID(puid)
        except:
            return # Es un nodo padre, no tiene objeto.
        if isinstance(objeto, pclases.GrupoAlumnos):
            import grupos_alumnos
            v = grupos_alumnos.GruposAlumnos(objeto, usuario = self.usuario)
            self.rebuild_cache_color()
        elif isinstance(objeto, pclases.Empleado):
            import empleados 
            v = empleados.Empleados(objeto, usuario = self.usuario)
            self.rebuild_cache_color_monitor(objeto)
        elif isinstance(objeto, pclases.Evento):
            import eventos
            v = eventos.Eventos(objeto, usuario = self.usuario)
            self.rebuild_cache_color()
        self.rellenar_widgets()

    def abrir_cliente(self, tv, path, cv, dia):
        """
        Abre el grupo al que se le ha hecho doble clic. Recibe el día, pero 
        no se llega a usar.
        """
        model = tv.get_model()
        puid = model[path][-1]
        cliente = pclases.getObjetoPUID(puid)
        import clientes
        v = clientes.Clientes(cliente, usuario = self.usuario)
        #self.rellenar_calendarios()

    def abrir_grupo(self, tv, path, cv, dia):
        """
        Abre el grupo al que se le ha hecho doble clic. Recibe el día, pero 
        no se llega a usar.
        """
        model = tv.get_model()
        puid = model[path][-1]
        actividad = pclases.getObjetoPUID(puid)
        grupos = actividad.gruposAlumnos
        import grupos_alumnos
        for grupo in grupos:
            v = grupos_alumnos.GruposAlumnos(grupo, usuario = self.usuario)
        self.rebuild_cache_color()
        self.rellenar_calendarios()

    def ver_o_no_ver_grupo(self, cell, path):
        """
        Desmarca como visible el grupo o evento seleccionado y actualiza el 
        calendario, mostrando solamente las actividades de los grupos y 
        eventos (categorías, en realidad) visibles.
        """
        model = self.wids['tv_grupos'].get_model()
        model[path][1] = not model[path][1]
        if not model[path].parent:
            for nodo_hijo in model[path].iterchildren():
                nodo_hijo[1] = model[path][1]
        self.rellenar_calendarios()

    def buscar_dia(self, cell):
        """
        Devuelve el nombre del día al que pertenece el cell.
        """
        for dia in ("lunes", "martes", "miercoles", "jueves", "viernes", 
                    "sabado", "domingo"):
            for ncol in range(2):
                col = self.wids['tv_%s' % dia].get_column(ncol)
                if cell in col.get_cell_renderers():
                    return dia
        raise ValueError, "¡El cell %s no está en ningún ListView!" % cell

    def cambiar_nombre_actividad(self, cell, path, newtext):
        dia = self.buscar_dia(cell)
        model = self.wids['tv_%s' % dia].get_model()
        puid = model[path][-1]
        if puid != "0":
            actividad = pclases.getObjetoPUID(puid)
            actividad.descripcion = newtext
            actividad.syncUpdate()
            model[path][1] = actividad.descripcion

    def cambiar_hora_actividad(self, cell, path, newtext):
        dia = self.buscar_dia(cell)
        model = self.wids['tv_%s' % dia].get_model()
        puid = model[path][-1]
        if puid != "0":
            horainicio, horafin = parse_horas(newtext)
            actividad = pclases.getObjetoPUID(puid)
            if horainicio != None:
                actividad.fechahoraInicio = datetime.datetime(
                    day = actividad.fechahoraInicio.day, 
                    month = actividad.fechahoraInicio.month, 
                    year = actividad.fechahoraInicio.year, 
                    hour = horainicio.seconds / (60*60), 
                    minute = (horainicio.seconds / 60) % 60)
            if horafin != None:
                actividad.fechahoraFin = datetime.datetime(
                    day = actividad.fechahoraFin.day, 
                    month = actividad.fechahoraFin.month, 
                    year = actividad.fechahoraFin.year, 
                    hour = horafin.seconds / (60*60), 
                    minute = (horafin.seconds / 60) % 60)
            actividad.syncUpdate()
            model[path][0] = actividad.get_str_horas()

    def cambiar_nombre_grupo(self, cell, path, newtext):
        model = self.wids['tv_grupos'].get_model()
        puid = model[path][-1]
        if puid != "0":
            try:
                grupo = pclases.getObjetoPUID(puid)
            except pclases.SQLObjectNotFound:
                return
            grupo.nombre = newtext
            grupo.syncUpdate()
            model[path][2] = grupo.nombre

    def rellenar_grupos(self):
        self.wids['ventana'].window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        while gtk.events_pending(): gtk.main_iteration(False)
        model = self.wids['tv_grupos'].get_model()
        model.clear()
        nodo_grupos = model.append(None, ("", True, 
            '<span background="light gray"><b><i>Grupos</i></b></span>', 0))
        for g in pclases.GrupoAlumnos.select(orderBy = "nombre"):
            g.sync()
            model.append(nodo_grupos, ("", True, g.nombre, g.get_puid()))
        nodo_eventos = model.append(None, ("", True, 
            '<span background="light gray"><b><i>Eventos</i></b></span>', 0))
        for e in pclases.Evento.select(orderBy = "nombre"):
            e.sync()
            model.append(nodo_eventos, ("", True, e.nombre, e.get_puid()))
        nodo_profesores = model.append(None, ("", True, 
            '<span background="light gray"><b><i>Monitores</i></b></span>', 0))
        for e in pclases.Empleado.select(orderBy = "apellidos"):
            e.sync()
            if e.es_profesor():
                model.append(nodo_profesores, ("", True, 
                                               e.get_nombre_completo(), 
                                               e.get_puid()))
        self.wids['tv_grupos'].expand_all()
        self.wids['ventana'].window.set_cursor(None)

    def rellenar_widgets(self):
        self.rellenar_grupos()
        self.rellenar_calendarios()

    def rellenar_tareas(self):
        model = self.wids['tv_tareas'].get_model()
        model.clear()
        hoy = datetime.datetime(*self.dia_seleccionado.timetuple()[:3])
        mannana = hoy + datetime.timedelta(days = 1)
        hace_una_semana = datetime.date(
            *(hoy - datetime.timedelta(days = 7)).timetuple()[:3])
        for t in pclases.Tarea.select():
            if (not t.fechaDone
                # Si la tarea no está completada, se muestra siempre.
                or (t.fechaDone and t.fechaDone > hace_una_semana)
                # Está completada y no ha pasado más de 1 semana desde 
                # entonces respecto a la fecha mostrada
                or (t.fechahora < mannana and t.fechahora >= hoy)
                # O bien es del día seleccionado en el calendario, esté o no 
                # completada.
               ):
                if t.fechahora >= hoy + datetime.timedelta(1):
                    # No muestro las tareas del "futuro". 
                    # Me da igual cómo estén.
                    continue
                model.append((t.fechaDone != None, 
                              t.resumen, 
                              t.texto, 
                              utils.str_fecha(t.fechaLimite), 
                              #utils.str_fecha(t.fechaDone), 
                              t.get_puid()))

    def rellenar_notas(self):
        model = self.wids['tv_notas'].get_model()
        model.clear()
        hoy = datetime.datetime(*self.dia_seleccionado.timetuple()[:3])
        mannana = hoy + datetime.timedelta(days = 1)
        for m in pclases.Memo.select(pclases.AND(
                pclases.Memo.q.fechahora >= hoy, 
                pclases.Memo.q.fechahora < mannana)):
            model.append((m.resumen, m.texto, m.get_puid())) 

    def rellenar_calendarios(self):
        """
        Rellena los calendarios de la semana del día seleccionado.
        """
        self.wids['ventana'].window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        while gtk.events_pending(): gtk.main_iteration(False)
        lunes = (self.dia_seleccionado 
                 - datetime.timedelta(days = self.dia_seleccionado.weekday()))
        lunes_siguiente = lunes + datetime.timedelta(days = 7)
        A = pclases.Actividad
        AND = pclases.AND
        OR = pclases.OR
        if not self.vista_diaria: 
            self.actividades = A.select(OR(
              AND(A.q.fechahoraInicio >= lunes,   # Las que empiezan esta semana
                  A.q.fechahoraInicio < lunes_siguiente), 
              AND(A.q.fechahoraFin >= lunes,      # Las que acaban esta semana
                  A.q.fechahoraFin < lunes_siguiente), 
              AND(A.q.fechahoraInicio < lunes,    # Las que duran todavía de 
                  A.q.fechahoraFin >= lunes_siguiente)), 
              orderBy = ["fechahoraInicio", "id"])  # semanas anteriores
        else:
            dia_siguiente = self.dia_seleccionado + datetime.timedelta(days=1)
            self.actividades = A.select(OR(
              AND(A.q.fechahoraInicio >= self.dia_seleccionado,   
                  A.q.fechahoraInicio < dia_siguiente), 
              AND(A.q.fechahoraFin >= self.dia_seleccionado,      
                  A.q.fechahoraFin < dia_siguiente), 
              AND(A.q.fechahoraInicio < self.dia_seleccionado,   
                  A.q.fechahoraFin >= dia_siguiente)), 
              orderBy = ["fechahoraInicio", "id"])  # semanas anteriores
        # Cambio los widgets de la ventana:
        #self.wids['calendario'].select_month(self.dia_seleccionado.month, 
        #                                     self.dia_seleccionado.year)
        #self.wids['calendario'].select_day(self.dia_seleccionado.day)
        anno, mes, dia = self.wids['calendario'].get_date()
        if (mes + 1 == datetime.date.today().month 
            and anno == datetime.date.today().year):
            self.wids['calendario'].mark_day(datetime.date.today().day)
        else:
            self.wids['calendario'].unmark_day(datetime.date.today().day)
        martes = lunes + datetime.timedelta(days = 1)
        miercoles = martes + datetime.timedelta(days = 1)
        jueves = miercoles + datetime.timedelta(days = 1)
        viernes = jueves + datetime.timedelta(days = 1)
        sabado = viernes + datetime.timedelta(days = 1)
        domingo = sabado + datetime.timedelta(days = 1)
        self.wids['l_lunes'].set_text(
            "<i>%s</i>" % lunes.strftime("%A %d de %B"))
        self.wids['l_martes'].set_text(
            "<i>%s</i>" % martes.strftime("%A %d de %B"))
        self.wids['l_miercoles'].set_text(
            "<i>%s</i>" % miercoles.strftime("%A %d de %B"))
        self.wids['l_jueves'].set_text(
            "<i>%s</i>" % jueves.strftime("%A %d de %B"))
        self.wids['l_viernes'].set_text(
            "<i>%s</i>" % viernes.strftime("%A %d de %B"))
        self.wids['l_sabado'].set_text(
            "<i>%s</i>" % sabado.strftime("%A %d de %B"))
        self.wids['l_domingo'].set_text(
            "<i>%s</i>" % domingo.strftime("%A %d de %B"))
        for n in ("lunes", "martes", "miercoles", "jueves", "viernes", 
                  "sabado", "domingo"):
            l = self.wids['l_%s' % n]
            l.set_use_markup(True)
        tvs_dias = {0: self.wids['tv_lunes'], 
                    1: self.wids['tv_martes'], 
                    2: self.wids['tv_miercoles'], 
                    3: self.wids['tv_jueves'], 
                    4: self.wids['tv_viernes'], 
                    5: self.wids['tv_sabado'], 
                    6: self.wids['tv_domingo']}
        for dia in tvs_dias:
            tvs_dias[dia].get_model().clear()
        # Filtro ahora:
        grupos, eventos, empleados = self.get_grupos_y_eventos_visibles()
        # OJO: Si hay actividades sin grupos (ni alumnos) se mostrarán aunque 
        # no haya ningún grupo activo en los filtros.
        for a in self.actividades:
            if a.evento and a.evento not in eventos:
                continue
            if a.empleado and a.empleado not in empleados:
                continue
            for grupo in a.gruposAlumnos:
                if grupo not in grupos:
                    continue
            dia = a.fechahoraInicio.weekday()
            tv = tvs_dias[dia]
            model = tv.get_model()
            desc_grupo = a.descripcion  
            desc_hora = a.get_str_horas()
            iterfila = model.append((desc_hora, 
                                     desc_grupo, 
                                     a.get_puid()))
            tooltip = gtk.Tooltip()
            txttooltip = a.get_txtinfoactividad()
            tooltip.set_text(txttooltip)
            tv.set_tooltip_row(tooltip, model.get_path(iterfila))
            # Aprovecho y muestro la descripción de la actividad seleccionada:
            sel = tv.get_selection()
            model, paths = sel.get_selected_rows()
            txttooltips = []
            for path in paths:
                puid = model[path][-1]
                a = pclases.getObjetoPUID(puid)
                txttooltips.append(a.get_txtinfoactividad(
                    incluir_asistentes = False))
            txttooltip = "\n\n".join(txttooltips)
            self.wids['txt_desc'].get_buffer().set_text(txttooltip)
            self.rellenar_asistentes(a)
        self.wids['tabla'].set_homogeneous(not self.vista_diaria)
        dias = ("lunes", "martes", "miercoles", "jueves", "viernes", "sabado", 
                "domingo")
        if self.vista_diaria:
            i = 0
            for dia in dias:
                tvdia = self.wids['tv_%s' % dia]
                contenedor = tvdia.parent.parent
                # [09] Caso especial para fines de semana. Comparten vbox.
                weekday_seleccionado = self.dia_seleccionado.weekday()
                visible = weekday_seleccionado == i
                if weekday_seleccionado >= 5 and i >= 5: 
                                    # Si sábado o domingo, el TreeView debe 
                                    # ocultarse o mostrarse según convenga
                    tvdia.parent.set_property("visible", visible)
                                    # Y el label, por supuesto.
                    try:
                        self.wids['l_%s' % dia].set_visible(visible)
                    except AttributeError:
                        self.wids['l_%s' % dia].set_property("visible", visible)
                    visible = True  # Pero el padre (común) debe verse en 
                                    # ambos casos.
                if pclases.DEBUG:
                    print "up_calendario >>>", weekday_seleccionado, i, visible
                contenedor.set_property("visible", visible)
                i += 1
        else:
            for dia in dias:
                self.wids['tv_%s' % dia].parent.parent.set_property("visible", 
                                                                    True)
        self.rellenar_notas()
        self.rellenar_tareas()
        self.wids['ventana'].window.set_cursor(None)

    def set_cache_color(self, puid):
        """
        Cambia o establece el color del "caché" a mostrar para la actividad 
        cuyo PUID recibe. El color lo obtiene del monitor, grupo o lo que 
        corresponda a la actividad en cada caso. 
        """
        if puid != "0":
            try:
                a = pclases.getObjetoPUID(puid)
            except pclases.SQLObjectNotFound:
                a = None    # Grupo eliminado
        else:
            a = None
        color = None
        if isinstance(a, pclases.Actividad):
            if a.evento:  # Tiene preferencia sobre color del grupo.
                color=gtk.gdk.Color(*a.evento.get_gdk_color_params())
            elif a.empleado:  # Tiene preferencia sobre color del grupo.
                color=gtk.gdk.Color(*a.empleado.get_gdk_color_params())
            elif a.gruposAlumnos:
                grupo = a.gruposAlumnos[0]# Si varios grupos, uso el 1º.
                color=gtk.gdk.Color(*grupo.get_gdk_color_params())
        elif isinstance(a, (pclases.Evento, pclases.GrupoAlumnos, 
                            pclases.Empleado)):
            color = gtk.gdk.Color(*a.get_gdk_color_params())
        self.colores[puid] = color
        return color

    def get_cache_color(self, puid):
        """
        Devuelve el color que corresponde a la actividad en el calendario. 
        Intenta sacarlo de un diccionario temporal para no consultar la BD 
        en cada refresco de pantalla.
        """
        if puid not in self.colores:
            color = self.set_cache_color(puid)
        else:
            color = self.colores[puid]
        return color

    def rebuild_cache_color_monitor(self, monitor):
        self.wids['ventana'].window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        while gtk.events_pending(): gtk.main_iteration(False)
        for a in self.actividades:
            if a in monitor.actividades:
                self.set_cache_color(a.get_puid())
        self.wids['ventana'].window.set_cursor(None)

    def rebuild_cache_color(self):
        """
        Reconstruye la caché de colores completa.
        """
        self.wids['ventana'].window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        while gtk.events_pending(): gtk.main_iteration(False)
        for a in self.actividades:
            self.set_cache_color(a)
        self.wids['ventana'].window.set_cursor(None)

    def colorear_calendario(self):
        #######################################################################
        # Contador de horas gastadas intentando optimizar esto: 4
        # Paco del futuro, incrementa este contador para convencerte a ti 
        # mismo cada vez que intentes volver a mejorar el rendimiento del 
        # calendario. 
        # Firmado, Paco del pasado.
        # Jur, jur, jur. Que te fucken, Paco del pasado. El Paco del presente 
        # lo ha conseguido. No es perfecto, pero va mucho más rápido. ¡Y solo 
        # cuatro horitas de nada! :(
        def cell_func(column, cell, model, itr, ncol):
            puid = model[itr][-1]
            color = self.get_cache_color(puid)
            cell.set_property("cell-background-gdk", color)
            return color
        #######################################################################
        for dia in ("lunes", "martes", "miercoles", "jueves", "viernes", 
                    "sabado", "domingo"):
            tvdia = self.wids['tv_%s' % dia]
            for ncol in range(2):
                column = tvdia.get_column(ncol)
                cells = column.get_cell_renderers()
                for cell in cells:
                    column.set_cell_data_func(cell, cell_func, ncol)
        column = self.wids['tv_grupos'].get_column(0)
        for cell in column.get_cell_renderers():
            column.set_cell_data_func(cell, cell_func, None)

    def get_grupos_y_eventos_visibles(self):
        """
        Devuelve dos listas: una de grupos visibles y otra de categorías.
        """
        model = self.wids['tv_grupos'].get_model()
        grupos = []
        eventos = []
        empleados = []
        for padre in model:
            for iter in padre.iterchildren():
                puid = iter[-1]
                if iter[1] and puid != "0":
                    try:
                        objeto = pclases.getObjetoPUID(puid)
                    except pclases.SQLObjectNotFound:
                        continue
                    if isinstance(objeto, pclases.GrupoAlumnos):
                        grupos.append(objeto)
                    elif isinstance(objeto, pclases.Evento):
                        eventos.append(objeto)
                    elif isinstance(objeto, pclases.Empleado):
                        empleados.append(objeto)
        return grupos, eventos, empleados

    # --------------- Manejadores de eventos ----------------------------
    def quitar_seleccion(self, tv, nombre_tv_a_dejar):
        """
        Deselecciona todos los treeviews a excepción del recibido.
        """
        for dia in ("lunes", "martes", "miercoles", "jueves", "viernes", 
                    "sabado", "domingo"):
            if dia == nombre_tv_a_dejar:
                continue
            tv_a_quitar = self.wids['tv_%s' % dia]
            sel = tv_a_quitar.get_selection()
            if sel:
                sel.unselect_all()
        # Aprovecho y muestro la descripción de la actividad seleccionada:
        sel = self.wids["tv_"+nombre_tv_a_dejar].get_selection()
        model, paths = sel.get_selected_rows()
        txttooltips = []
        for path in paths:
            puid = model[path][-1]
            a = pclases.getObjetoPUID(puid)
            txttooltips.append(a.get_txtinfoactividad(
                incluir_asistentes = False))
        txttooltip = "\n\n".join(txttooltips)
        self.wids['txt_desc'].get_buffer().set_text(txttooltip)
        try:
            self.rellenar_asistentes(a)
        except UnboundLocalError:   # Se ha deseleccionado todo
            self.wids['tv_asistentes'].get_model().clear()
    
    def rellenar_asistentes(self, actividad):
        """
        Rellena el model de asistentes a la clase.
        """
        model = self.wids['tv_asistentes'].get_model()
        model.clear()
        for cliente in actividad.clientes:
            model.append((cliente.nombre, 
                          cliente.get_puid()))

    # --------------- Manejadores de eventos del popup ------------------
    def attach_menu_asignar(self, tv, ventana_padre = None, usuario = None):
        """
        Agrega un menú contextual al TreeView con las opcines de asignar 
        monitor, asignar grupo, asignar persona para clase privada o asignar 
        máquinas de gimnasio.
        """
        actions = []
        ui_string = """<ui>
                        <popup name='Popup'>
                            <menu name="Asignar monitor" action="profesor">"""
        for e in pclases.Empleado.select(orderBy = "apellidos"):
            if e.es_profesor():
                ui_string += '<menuitem name="%s" action = "profesor_%d"/>'%(
                    e.get_nombre_completo(), e.id)
                actions.append(("profesor_%d" % e.id, 
                                gtk.STOCK_ORIENTATION_PORTRAIT, 
                                "Asignar a %s" % e.get_nombre_completo(), 
                                "", 
                                "Asigna a %s como profesor." 
                                    % e.get_nombre_completo(), 
                                self.asignar_monitor))
        ui_string += """    </menu>
                            <menuitem name="Asignar grupo completo" 
                                action="grupo" />
                            <menuitem name="Asignar clase privada" 
                                action="cliente" />
                            <menuitem name="Asignar clase recuperación" 
                                action="recupera" />
                            <menuitem name="Asignar máquinas" 
                                action="equipo" />
                        </popup>
                       </ui>"""
        ag = gtk.ActionGroup("WindowActions")
        actions += [('profesor', 
                    gtk.STOCK_ORIENTATION_PORTRAIT, 
                    "Asignar _monitor", 
                    "<Control>m", 
                    "Asigna un profesor a las clases seleccionadas.", 
                    ), #lambda *args, **kw: None), 
                   ('grupo', 
                    gtk.STOCK_DND_MULTIPLE, 
                    "Asignar _grupo", 
                    "<Control>g", 
                    "Asigna un grupo completo de alumnos a las clases "
                        "seleccionadas.", 
                    self.asignar_grupo), 
                   ('cliente', 
                    gtk.STOCK_DND, 
                    "Asignar clase _privada", 
                    "<Control>p", 
                    "Convierte la sesión en una clase privada con un único "
                        "cliente.", 
                    self.asignar_privada), 
                   ('recupera', 
                    gtk.STOCK_DND, 
                    "Asignar clase _recuperación", 
                    "<Control>r", 
                    "Añade a un alumno solamente para la clase seleccionada.", 
                    self.asignar_privada), 
                   ('equipo', 
                    gtk.STOCK_CONVERT, 
                    "Asignar máqui_nas", 
                    "<Control>n", 
                    "Asgina una o varias máquinas a una sesión.", 
                    self.asignar_maquina)]
        ag.add_actions(actions, (tv, usuario))
        ui = gtk.UIManager()
        ui.insert_action_group(ag, 0)
        ui.add_ui_from_string(ui_string)
        tv.connect('button_press_event', button_clicked, ui, tv, 
                                           ventana_padre) #Para los modales.
        menuitem = ui.get_widget("/Popup/Asignar máquinas")
        menuitem.set_sensitive(False)

    def asignar_monitor(self, action, tv, usuario, monitor = None):
        if monitor is None:
            id_profesor = action.get_name().split("_")[-1]
            monitor = pclases.Empleado.get(id_profesor)
        seleccion = tv.get_selection()
        model, paths = seleccion.get_selected_rows()
        for path in paths:
            iter = model.get_iter(path)
            puid = model[iter][-1]
            objeto = pclases.getObjetoPUID(puid)
            objeto.empleado = monitor
            objeto.sync()
            # [61] Refresco caché de colores.
            self.set_cache_color(puid)
            # EO [61]
        self.actualizar_calendario()

    def asignar_grupo(self, action, tv, usuario, grupo = None):
        seleccion = tv.get_selection()
        model, paths = seleccion.get_selected_rows()
        if grupo is None:
            alumnos, grupo = self.preguntar_grupo()
            try:
                profegrupo = grupo.empleado
            except AttributeError:
                profegrupo = None
        else:
            alumnos = grupo.get_alumnos()
            profegrupo = None
        for path in paths:
            iter = model.get_iter(path)
            puid = model[iter][-1]
            objeto = pclases.getObjetoPUID(puid)
            # Elimino grupos y asistentes anteriores:
            for cliente in objeto.clientes:
                objeto.removeCliente(cliente)
            # Y asigno los nuevos:
            for cliente in alumnos:
                if cliente not in objeto.clientes:
                    objeto.addCliente(cliente)
            objeto.sync()
            # [61] Refresco caché de colores.
            self.set_cache_color(puid)
            # EO [61]
        if paths and profegrupo:    # El grupo tiene un profesor por defecto, 
                                    # así que se lo asigno:
            objeto.empleado = profegrupo
        self.actualizar_calendario()

    def preguntar_grupo(self):
        opciones = [(g.id, g.nombre) 
                    for g in pclases.GrupoAlumnos.select(orderBy = "nombre")]
        idgrupo = utils.dialogo_combo(titulo = "SELECCIONE GRUPO", 
                    texto = "Seleccione un grupo de alumnos del despegable:",
                    padre = self.wids['ventana'], 
                    ops = opciones)
        grupo = None
        if idgrupo != None and idgrupo > 0: # Es un grupo completo
            grupo = pclases.GrupoAlumnos.get(idgrupo)
            alumnos = grupo.get_alumnos()
        elif idgrupo != None and idgrupo < 0:
            cliente = pclases.Cliente.get(-idgrupo)
            alumnos = [cliente]
        else:
            alumnos = []
        return alumnos, grupo
    
    def preguntar_alumno(self):
        opciones = [(-c.id, c.nombre) 
                    for c in pclases.Cliente.select(orderBy = "nombre")]
                # Debería ser pecado no guardar los apellidos por separado.
        idgrupo = utils.dialogo_combo(titulo = "SELECCIONE ALUMNO", 
                    texto = "Seleccione un alumno del desplegable:", 
                    padre = self.wids['ventana'], 
                    ops = opciones)
        if idgrupo != None and idgrupo > 0: # Es un grupo completo
            grupo = pclases.GrupoAlumnos.get(idgrupo)
            alumnos = grupo.get_alumnos()
        elif idgrupo != None and idgrupo < 0:
            cliente = pclases.Cliente.get(-idgrupo)
            alumnos = [cliente]
        else:
            alumnos = []
        return alumnos

    def asignar_privada(self, action, tv, usuario, alumno = None, 
                        actividades = []):
        seleccion = tv.get_selection()
        model, paths = seleccion.get_selected_rows()
        if alumno is None:
            alumnos = self.preguntar_alumno()
        else:
            alumnos = [alumno] 
        if not actividades:
            for path in paths:
                iter = model.get_iter(path)
                puid = model[iter][-1]
                objeto = pclases.getObjetoPUID(puid)
                actividades.append(objeto)
        for a in actividades:
            for cliente in alumnos:
                if cliente not in a.clientes:
                    a.addCliente(cliente)
                # [21] Semiprivadas:
                if len(a.clientes) == 1:
                    a.descripcion = "[Priv.] %s" % (a.clientes[0].nombre)
                if len(a.clientes) == 2:
                    a.descripcion = "[Semipriv.] %s + %s" % (
                        a.clientes[0].nombre, 
                        a.clientes[1].nombre)
                if len(a.clientes) > 2 and "Semipriv" in a.descripcion:
                    a.descripcion = ", ".join([c.nombre for c in a.clientes])
            a.sync()
            # [61] Refresco caché de colores.
            self.set_cache_color(a.get_puid())
            # EO [61]
        self.actualizar_calendario()

    def asignar_maquina(self, action, tv, usuario):
        seleccion = tv.get_selection()
        model, paths = seleccion.get_selected_rows()
        for path in paths:
            iter = model.get_iter(path)
            puid = model[iter][-1]
            objeto = pclases.getObjetoPUID(puid)
            # Hasta aquí es común a todos los asignar_*
            # TODO: Asignar la máquina.
            print objeto

    def imprimir(self, boton):
        """
        Genera un PDF con el calendario en pantalla.
        """
        import tempfile, os, gc
        if not self.vista_diaria: # Vista semanal. Captura.
            for dia in range(7):
                self.imprimir_vista_diaria(dia)
            # Ya no imprimmo la captura de pantalla:
            #tabla = self.wids['tabla']
            #ancho, alto = tabla.window.get_geometry()[2:4]
            #pb = gtk.gdk.Pixbuf.get_from_drawable(
            #    gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, ancho, alto), 
            #    tabla.window, 
            #    cmap = gtk.gdk.colormap_get_system(), 
            #    src_x = 0, src_y = 0, 
            #    dest_x = 0, dest_y = 0, 
            #    width = ancho, height = alto)
            #imagen_tmp = os.path.join(tempfile.gettempdir(), 
            #    "cal%s.png" % `time.time()`.replace(".", ""))
            #pb.save(imagen_tmp, "png") #, {"quality": "100"})
            #del pb
            #gc.collect()
            #pdf_tmp = os.path.join(tempfile.gettempdir(), "Agenda_%s" % 
            #    `time.time()`.replace(".", ""))
            ## Comentar estas 3 líneas y descomentar las otras 2 para que no se 
            ## imprima nada más que la parte de los días.
            #nombre_treeview = 'tv_notas'
            #datos = get_datos_from_tv(self.wids[nombre_treeview])
            #campos = get_campos_from_tv(self.wids[nombre_treeview])
            #campos = zip(campos, [100.0 / len(campos)] * len(campos))
            ##datos = []
            ##campos = [("", 100.0)]
            #if not datos:
            #    datos = [("",) * len(campos)]
            #if self.vista_diaria:
            #    str_fechas = utils.str_fecha(self.dia_seleccionado)
            #else:
            #    ultimo_dia = self.dia_seleccionado + datetime.timedelta(days=7)
            #    str_fechas = "Del %s a %s" % (
            #                    utils.str_fecha(self.dia_seleccionado),
            #                    utils.str_fecha(ultimo_dia))
            #agenda_pdf = geninformes.imprimir2(pdf_tmp, 
            #                "Agenda: %s" % str_fechas, 
            #                campos, 
            #                datos, 
            #                graficos = [imagen_tmp])
        else:   # Vista diaria. Datos, sin colores.
            self.imprimir_vista_diaria(None)

    def imprimir_vista_diaria(self, weekofday = None):
        lunes = (self.dia_seleccionado 
                 - datetime.timedelta(days = self.dia_seleccionado.weekday()))
        if weekofday == None:
            weekofday = self.dia_seleccionado.weekday() 
        fecha_a_imprimir = (lunes + datetime.timedelta(days = weekofday))
        dias = pclases.Clase.listadias
        nombredia = dias[weekofday]
        tv = self.wids['tv_%s' % nombredia]
        tv = utils.convertir_a_listview(utils.clone_treeview(tv))
        # The fucking colors:
        model = tv.get_model()
        for row in model:
            a = pclases.getObjetoPUID(row[-1])
            color = self.get_cache_color(a.get_puid())
            if color:
                str_color_rgb = "[color=RGB{%s,%s,%s}]"%(color.red_float, 
                                                         color.green_float,
                                                         color.blue_float)
            else:
                str_color_rgb = ""
            for col in range(2):
                row[col] += str_color_rgb
        # EOThe fucking colors
        agenda_pdf = treeview2pdf(tv, 
            titulo = "Agenda del %s"%fecha_a_imprimir.strftime("%A %d de %B"), 
            fecha = utils.str_fecha(fecha_a_imprimir)) 
        abrir_pdf(agenda_pdf) 


# Más funciones auxiliares:
def escalar_a(ancho, alto, pixbuf):
    """
    Devuelve un pixbuf escalado en proporción para que como máximo tenga 
    de ancho y alto las medidas recibidas.
    """
    if pixbuf.get_width() > ancho:
        nuevo_ancho = ancho
        nuevo_alto = int(pixbuf.get_height() 
                         * ((1.0 * ancho) / pixbuf.get_width()))
        colorspace = pixbuf.get_property("colorspace")
        has_alpha = pixbuf.get_property("has_alpha")
        bits_per_sample = pixbuf.get_property("bits_per_sample")
        pixbuf2 = gtk.gdk.Pixbuf(colorspace, 
                                 has_alpha, 
                                 bits_per_sample, 
                                 nuevo_ancho, 
                                 nuevo_alto)
        pixbuf.scale(pixbuf2, 
                     0, 0, 
                     nuevo_ancho, nuevo_alto, 
                     0, 0,
                     (1.0 * nuevo_ancho) / pixbuf.get_width(), 
                     (1.0 * nuevo_alto) / pixbuf.get_height(), 
                     gtk.gdk.INTERP_BILINEAR)
        pixbuf = pixbuf2
    if pixbuf.get_height() > alto:
        nuevo_alto = alto
        nuevo_ancho = int(pixbuf.get_width() 
                          * ((1.0 * alto) / pixbuf.get_height()))
        colorspace = pixbuf.get_property("colorspace")
        has_alpha = pixbuf.get_property("has_alpha")
        bits_per_sample = pixbuf.get_property("bits_per_sample")
        pixbuf2 = gtk.gdk.Pixbuf(colorspace, 
                                 has_alpha, 
                                 bits_per_sample, 
                                 nuevo_ancho, 
                                 nuevo_alto)
        pixbuf.scale(pixbuf2, 
                     0, 0, 
                     nuevo_ancho, nuevo_alto, 
                     0, 0,
                     (1.0 * nuevo_ancho) / pixbuf.get_width(), 
                     (1.0 * nuevo_alto) / pixbuf.get_height(), 
                     gtk.gdk.INTERP_BILINEAR)
        pixbuf = pixbuf2
    return pixbuf

def parse_horas(txt):
    """
    Devuelve una tupla con un par de horas a partir del texto recibido.
    Si no se puede interpretar alguna de las dos, devuelve None en su lugar.
    No lanza excepción de tipo ni valor.
    """
    _txt = ""
    for l in txt:
        if l in "0123456789:-": # Limpio de polvo y paja.
            _txt += l
    txt = _txt
    try:
        h1, h2 = txt.split("-")
    except (TypeError, ValueError):
        h1, h2 = None, None
    try:
        h1 = utils.parse_hora(h1)
    except (ValueError, TypeError):
        h1 = None
    try:
        h2 = utils.parse_hora(h2)
    except (ValueError, TypeError):
        h2 = None
    return h1, h2

def button_clicked(w, event, ui, tv, ventana_padre = None):
    if event.button == 3:
        seleccion = tv.get_selection()
        if seleccion != None:
            model, paths = seleccion.get_selected_rows()
            if len(paths) > 0:
                widget = ui.get_widget("/Popup")
                #single_selection = len(paths) == 1
                #menuitem = ui.get_widget("/Popup/Notas")
                #menuitem.set_sensitive(single_selection)
                widget.popup(None, None, None, event.button, event.time)

def buscar_actividades_periodicas_en_el_futuro(a):
    """
    Busca actividades iguales a la recibida pero que se produzcan en el futuro.
    """
    A = pclases.Actividad
    acts = A.select(pclases.AND(A.q.fechahoraInicio > a.fechahoraInicio, 
                                A.q.descripcion == a.descripcion))
    return pclases.SQLlist(acts)

if __name__=='__main__':
    a = Calendario()

