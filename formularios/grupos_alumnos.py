#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2007  Francisco José Rodríguez Bogado,                   #
#                          (pacoqueen@users.sourceforge.net                   #
#                                                                             #
# This file is part of F.P.-INN .                                             #
#                                                                             #
# F.P.-INN  is free software; you can redistribute it and/or modify           #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation; either version 2 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# F.P.-INN  is distributed in the hope that it will be useful,                #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with F.P.-INN ; if not, write to the Free Software                    #
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA  #
###############################################################################


###################################################################
## skel.py - Esqueleto para ventanas.
###################################################################
## NOTAS:
##  Usar ESTA ventana a partir de ahora para crear nuevas.
##  Hereda de ventana y ventana genérica, y la mayoría de funciones
##  están automatizadas partiendo tan solo de la clase y un 
##  diccionario que empareje widgets y atributos.
## ----------------------------------------------------------------
##  
###################################################################
## Changelog:
## 17 de diciembre de 2007 -> Inicio
## 
###################################################################

import sys, os
from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time, datetime
try:
    import pclases
    from seeker import VentanaGenerica 
except ImportError:
    sys.path.append(os.path.join('..', 'framework'))
    import pclases
    from seeker import VentanaGenerica 
from utils import _float as float
import adapter
import datetime


class GruposAlumnos(Ventana, VentanaGenerica):
    CLASE = pclases.GrupoAlumnos
    VENTANA = os.path.join("grupos_alumnos.glade")
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        self.clase = self.CLASE
        Ventana.__init__(self, self.VENTANA, objeto)
        self.dic_campos = self.__build_dic_campos()
        self.adaptador = adapter.adaptar_clase(self.clase, self.dic_campos)
        connections = {'b_salir/clicked': self.salir,
                       'b_nuevo/clicked': self.nuevo,
                       'b_borrar/clicked': self.borrar,
                       'b_actualizar/clicked': self.actualizar_ventana,
                       'b_guardar/clicked': self.guardar,
                       'b_buscar/clicked': self.buscar,
                       'b_color/color-set': self.select_color, 
                       'b_add_cliente/clicked': self.add_cliente, 
                       'b_drop_cliente/clicked': self.drop_cliente, 
                       'b_add_actividad/clicked': self.add_actividad, 
                       'b_drop_actividad/clicked': self.drop_actividad, 
                      }
        self.add_connections(connections)
        self.inicializar_ventana()
        if self.objeto == None:
            self.ir_a_primero()
        else:
            self.ir_a(objeto)
        gtk.main()

    def add_cliente(self, boton):
        texto = utils.dialogo_entrada(titulo = "BUSCAR ALUMNO", 
            texto = "Introduzca el nombre o el DNI del cliente:", 
            padre = self.wids['ventana'])
        if texto != None:
            clientes = pclases.Cliente.select(pclases.OR(
                pclases.Cliente.q.nombre.contains(texto), 
                pclases.Cliente.q.cif.contains(texto)))
            clientes = [c for c in clientes if c not in self.objeto.clientes]
            if clientes:
                filas_res = []
                for r in clientes:
                    filas_res.append((r.id, r.nombre, r.cif))
                ids = utils.dialogo_resultado(filas_res,
                        titulo = 'SELECCIONE ALUMNO',
                        cabeceras = ('ID', 'Nombre', 'DNI'), 
                        padre = self.wids['ventana'], 
                        multi = True)
                for id in ids:
                    if len(self.objeto.clientes) >= self.objeto.cupo:
                        res = utils.dialogo(titulo = "CUPO SOBREPASADO", 
                            texto = "El cupo del grupo está completo.\n"
                                    "¿Desea agregar a la lista de espera?", 
                            padre = self.wids['ventana'])
                        if not res:
                            break
                    cliente = pclases.Cliente.get(id)
                    if cliente not in self.objeto.clientes:
                        cliente.addGrupoAlumnos(self.objeto)
                        # Y asigno a todas las actividades no impartidas del 
                        # grupo:
                        if not self.objeto.en_lista_de_espera(cliente):
                            acts_pdtes=self.objeto.get_actividades_pendientes()
                            for a in acts_pdtes:
                                a.addCliente(cliente)
                if ids:
                    self.rellenar_tabla_clientes()
            else:
                utils.dialogo_info(titulo = "SIN RESULTADOS", 
                    texto = "No se encontraron alumnos.", 
                    padre = self.wids['ventana'])
    
    def quitar_seleccion(self, tv, nombre_tv_a_quitar):
        tv_a_quitar = self.wids[nombre_tv_a_quitar]
        sel = tv_a_quitar.get_selection()
        if sel:
            sel.unselect_all()

    def drop_cliente(self, boton):
        for tvname in ("tv_clientes", "tv_espera"):
            sel = self.wids[tvname].get_selection()
            model, iters = sel.get_selected_rows()
            for iter in iters:
                puid = model[iter][-1]
                cliente = pclases.getObjetoPUID(puid)
                # Lo elimino de las clases no dadas:
                if not self.objeto.en_lista_de_espera(cliente):
                    acts = self.objeto.get_actividades_pendientes()
                    for a in acts:
                        a.removeCliente(cliente)
                cliente.removeGrupoAlumnos(self.objeto)
        self.rellenar_tabla_clientes()

    def add_actividad(self, boton):
        texto = utils.dialogo_entrada(titulo = "NUEVA ACTIVIDAD", 
            texto = 
                "Introduzca la descripción de la nueva actividad deportiva:", 
            padre = self.wids['ventana'])
        if texto != None:
            opciones = [(e.id, e.nombre) 
                        for e in pclases.Evento.select(orderBy = "nombre")]
            opciones.insert(0, (0, "Sin evento relacionado"))
            idevento = utils.dialogo_combo(titulo = "SELECCIONE EVENTO:", 
                texto = "Seleccione un evento de la lista:", 
                ops = opciones, 
                padre = self.wids['ventana'], 
                valor_por_defecto = 0)
            if idevento != None:
                if idevento == 0:
                    evento = None
                else:
                    evento = pclases.Evento.get(idevento)
                actividad = pclases.Actividad(descripcion = texto, 
                                evento = evento, 
                                fechahoraInicio = datetime.datetime.today(),
                                fechahoraFin = datetime.datetime.today(),
                                grupoAlumnos = self.objeto)
                model = self.wids['tv_actividades'].get_model()
                model.append((actividad.descripcion, 
                              actividad.evento 
                                and actividad.evento.nombre or "", 
                              utils.str_fechahora(actividad.fechahoraInicio), 
                              utils.str_fechahora(actividad.fechahoraFin), 
                              actividad.get_puid()))

    def drop_actividad(self, boton):
        sel = self.wids['tv_actividades'].get_selection()
        model, iters = sel.get_selected_rows()
        for iter in iters:
            puid = model[iter][-1]
            actividad = pclases.getObjetoPUID(puid)
            actividad.destroySelf()
        self.rellenar_tabla_actividades()

    def select_color(self, boton):
        """
        Muestra un diálogo de selección de color y establece los valores 
        R, G y B al color seleccionado.
        """
        gdkcolor = boton.get_color()
        self.objeto.set_gdk_color_params(gdkcolor.red, 
                                         gdkcolor.green, 
                                         gdkcolor.blue)
        self.wids['sp_colorR'].set_value(self.objeto.colorR)
        self.wids['sp_colorG'].set_value(self.objeto.colorG)
        self.wids['sp_colorB'].set_value(self.objeto.colorB)
        self.guardar(None)

    def __build_dic_campos(self):
        """
        Devuelve un diccionario de campos de la clase de pclases y 
        su widget relacionado.
        El widget y el atributo deben llamarse igual, o en todo caso
        ser del tipo "e_nombre", "cb_nombre", etc.
        Los atributos para los que no se encuentre widget en el glade
        se ignorarán (cuando se adapten mediante el módulo adapter se
        les creará un widget apropiado a estas columnas ignoradas aquí).
        """
        res = {}
        for colname in self.clase.sqlmeta.columns:
            col = self.clase.sqlmeta.columns[colname]
            for widname_glade in self.wids.keys():
                if "_" in widname_glade:
                    widname = widname_glade.split("_")[-1]
                else:
                    widname = widname_glade
                if widname == colname:
                    w = self.wids[widname_glade]
                    res[col] = w
        return res

    def es_diferente(self):
        """
        Devuelve True si algún valor en ventana difiere de 
        los del objeto.
        """
        if self.objeto == None:
            igual = True
        else:
            adaptadores = self.adaptador.get_adaptadores()
            igual = self.objeto != None
            for col in adaptadores:
                fcomp = adaptadores[col]['comparar']
                igual = igual and fcomp(self.objeto)
                if not igual:
                    if pclases.DEBUG:
                        print col.name, 
                        en_pantalla = adaptadores[col]['leer']()
                        en_objeto = getattr(self.objeto, col.name)
                        print "En pantalla:", en_pantalla, type(en_pantalla),
                        print "En objeto:", en_objeto, type(en_objeto), 
                        print fcomp(self.objeto)
                    break
        return not igual
    
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
        self.wids['ventana'].set_title(self.clase.sqlmeta.table.upper())
        # Inicialización del resto de widgets:
        cols = (('Nombre', 'gobject.TYPE_STRING', False, True, True, None),
                ('PUID', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_listview(self.wids['tv_clientes'], cols, multi = True)
        cols = (('Nombre', 'gobject.TYPE_STRING', False, True, True, None),
                ('PUID', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_listview(self.wids['tv_espera'], cols, multi = True)
        self.wids['tv_espera'].connect("cursor-changed", 
            self.quitar_seleccion, 'tv_clientes')
        self.wids['tv_espera'].connect("row-activated", self.abrir_cliente)
        self.wids['tv_clientes'].connect("cursor-changed", 
            self.quitar_seleccion, 'tv_espera')
        self.wids['tv_clientes'].connect("row-activated", self.abrir_cliente)
        cols = (('Descripción', 'gobject.TYPE_STRING', True, True, True, 
                    self.cambiar_descripcion_actividad),
                ('Evento', 'gobject.TYPE_STRING', False, True, False, None),
                    # TODO: ¿Cambiar por combo?
                ('Inicio', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_inicio_actividad),
                ('Fin', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_fin_actividad),
                ('PUID', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_listview(self.wids['tv_actividades'], cols, multi=True)
        self.wids['b_color'].set_use_alpha(False)
        utils.rellenar_lista(self.wids['cbe_empleadoID'], 
                             [(e.id, e.get_nombre_completo()) 
                              for e in pclases.Empleado.select(
                                                orderBy = "apellidos")]
                            )

    def abrir_cliente(self, tv, path, cv):
        model = tv.get_model()
        puid = model[path][-1]
        print puid
        if puid:
            objeto = pclases.getObjetoPUID(puid)
            import clientes
            v = clientes.Clientes(usuario = self.usuario, 
                                  objeto = objeto)

    def cambiar_inicio_actividad(self, cell, path, text):
        model = self.wids['tv_actividades'].get_model()
        puid = model[path][-1]
        p = pclases.getObjetoPUID(puid)
        try:
            p.fechahoraInicio = utils.parse_fechahora(text)
            p.syncUpdate()
        except (TypeError, ValueError):
            utils.dialogo_info(titulo = "ERROR DE FORMATO", 
                               texto = "La fecha %s no es correcta." % text, 
                               padre = self.wids['ventana'])
        else:
            model[path][2] = utils.str_fechahora(p.fechahoraInicio)

    def cambiar_fin_actividad(self, cell, path, text):
        model = self.wids['tv_actividades'].get_model()
        puid = model[path][-1]
        p = pclases.getObjetoPUID(puid)
        try:
            p.fechahoraFin = utils.parse_fechahora(text)
            p.syncUpdate()
        except (TypeError, ValueError):
            utils.dialogo_info(titulo = "ERROR DE FORMATO", 
                               texto = "La fecha %s no es correcta." % text, 
                               padre = self.wids['ventana'])
        else:
            model[path][3] = utils.str_fechahora(p.fechahoraFin)

    def cambiar_descripcion_actividad(self, cell, path, text):
        model = self.wids['tv_actividades'].get_model()
        puid = model[path][-1]
        p = pclases.getObjetoPUID(puid)
        p.descripcion = text
        p.syncUpdate()
        model[path][0] = p.descripcion

    def activar_widgets(self, s, chequear_permisos = True):
        """
        Activa o desactiva (sensitive=True/False) todos 
        los widgets de la ventana que dependan del 
        objeto mostrado.
        Entrada: s debe ser True o False. En todo caso
        se evaluará como boolean.
        """
        if self.objeto == None:
            s = False
        ws = tuple(["b_borrar"] + ['b_color'] + 
                   [self.adaptador.get_adaptadores()[col]['widget'].name 
                    for col in self.adaptador.get_adaptadores().keys()])
            # b_nuevo y b_buscar no se activan/desactivan aquí, sino en el
            # chequeo de permisos.
        for w in ws:
            try:
                self.wids[w].set_sensitive(s)
            except Exception, msg:
                print "Widget problemático:", w, "Excepción:", msg
                #import traceback
                #traceback.print_last()
        if chequear_permisos:
            self.check_permisos(nombre_fichero_ventana = "grupos_alumnos.py")

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
            filas_res.append((r.id, r.nombre))
        id = utils.dialogo_resultado(filas_res,
                titulo = 'SELECCIONE %s' % self.clase.sqlmeta.table.upper(),
                cabeceras = ('ID', 'Nombre'), 
                padre = self.wids['ventana'])
        if id < 0:
            return None
        else:
            return id

    def rellenar_widgets(self):
        """
        Introduce la información del grupo actual
        en los widgets.
        No se chequea que sea != None, así que
        hay que tener cuidado de no llamar a 
        esta función en ese caso.
        """
        adaptadores = self.adaptador.get_adaptadores()
        for col in adaptadores.keys():
            adaptadores[col]['mostrar'](self.objeto)
        self.clientes_en_espera = [c for c in self.objeto.clientes 
                                   if self.objeto.en_lista_de_espera(c)]
        self.rellenar_tabla_clientes()
        self.rellenar_tabla_actividades()
        self.wids['b_color'].set_color(gtk.gdk.Color(
            *self.objeto.get_gdk_color_params()))
        self.objeto.make_swap()
        self.wids['ventana'].set_title(self.objeto.get_info())

    def rellenar_tabla_clientes(self):
        modelclientes = self.wids['tv_clientes'].get_model()
        modelespera = self.wids['tv_espera'].get_model()
        modelclientes.clear()
        modelespera.clear()
        total = 0
        for p in self.objeto.clientes:
            if self.objeto.en_lista_de_espera(p):
                model = modelespera
            else:
                model = modelclientes
                total += 1
            model.append((p.nombre, 
                          p.get_puid()))
        self.wids['e_total_alumnos'].set_text(str(total))
        # Compruebo los que acaban de entrar en lista de espera.
        if pclases.DEBUG:
            print self.clientes_en_espera
        for c in self.clientes_en_espera:
            if not self.objeto.en_lista_de_espera(c):
                if pclases.DEBUG:
                    print "Este acaba de entrar:", c.nombre    
                # Lo añado a las actividades pendientes:
                acts_pdtes = self.objeto.get_actividades_pendientes()
                for a in acts_pdtes:
                    a.addCliente(cliente)
        self.clientes_en_espera = [c for c in self.objeto.clientes 
                                   if self.objeto.en_lista_de_espera(c)]
    
    def rellenar_tabla_actividades(self):
        model = self.wids['tv_actividades'].get_model()
        model.clear()
        for c in self.objeto.clientes:
            if not self.objeto.en_lista_de_espera(c):
                for p in c.actividades:
                    model.append((p.descripcion, 
                                  p.evento and p.evento.nombre or "", 
                                  utils.str_fechahora(p.fechahoraInicio), 
                                  utils.str_fechahora(p.fechahoraFin), 
                                  p.get_puid()))
            
    def nuevo(self, widget):
        """
        Función callback del botón b_nuevo.
        Pide los datos básicos para crear un nuevo objeto.
        Una vez insertado en la BD hay que hacerlo activo
        en la ventana para que puedan ser editados el resto
        de campos que no se hayan pedido aquí.
        """
        objeto_anterior = self.objeto
        if objeto_anterior != None:
            objeto_anterior.notificador.desactivar()
        self.objeto = self.clase(nombre = "Nuevo grupo de alumnos", 
                                 cupo = 0)  
        self.objeto.notificador.activar(self.aviso_actualizacion)
        self._objetoreciencreado = self.objeto
        self.activar_widgets(True)
        self.actualizar_ventana(objeto_anterior = objeto_anterior)
        utils.dialogo_info('NUEVO %s CREADO' % self.clase.sqlmeta.table.upper(), 
                           'Se ha creado un nuevo %s.\nA continuación complete la información del misma y guarde los cambios.' % self.clase.sqlmeta.table.lower(), 
                           padre = self.wids['ventana'])

    def buscar(self, widget):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        a_buscar = utils.dialogo_entrada(
            titulo = "BUSCAR %s" % self.clase.sqlmeta.table.upper(), 
            texto = "Introduzca nombre:", 
            padre = self.wids['ventana']) 
        if a_buscar != None:
            try:
                ida_buscar = int(a_buscar)
            except ValueError:
                ida_buscar = -1
            campos_busqueda = (self.clase.q.nombre, ) 
            subsubcriterios = []
            sqlower = pclases.sqlbuilder.func.lower
            for cb in campos_busqueda:
                ssc = [sqlower(cb).contains(t.lower()) 
                        for t in a_buscar.split()]
                if ssc:
                    subsubcriterios.append(pclases.AND(*ssc))
                else:
                    subsubcriterios.append(
                        sqlower(cb).contains(a_buscar.lower()))
            if len(subsubcriterios) > 1:
                subcriterios = pclases.OR(*subsubcriterios)
            else:
                subcriterios = subsubcriterios
            criterio = pclases.OR(subcriterios, 
                                  self.clase.q.id == ida_buscar)
            resultados = self.clase.select(criterio)
            if resultados.count() > 1:
                ## Refinar los resultados
                id = self.refinar_resultados_busqueda(resultados)
                if id == None:
                    return
                resultados = [self.clase.get(id)]
                # Me quedo con una lista de resultados de un único objeto 
                # ocupando la primera posición.
                # (Más abajo será cuando se cambie realmente el objeto actual 
                # por este resultado.)
            elif resultados.count() < 1:
                ## Sin resultados de búsqueda
                utils.dialogo_info(titulo = 'SIN RESULTADOS', 
                                   texto = 'La búsqueda no produjo resultados.\nPruebe a cambiar el texto buscado o déjelo en blanco para ver una lista completa.\n(Atención: Ver la lista completa puede resultar lento si el número de elementos es muy alto)',
                                   padre = self.wids['ventana'])
                return
            ## Un único resultado
            # Primero anulo la función de actualización
            if self.objeto != None:
                self.objeto.notificador.desactivar()
            # Pongo el objeto como actual
            try:
                self.objeto = resultados[0]
            except IndexError:
                utils.dialogo_info(titulo = "ERROR", 
                                   texto = "Se produjo un error al recuperar la información.\nCierre y vuelva a abrir la ventana antes de volver a intentarlo.", 
                                   padre = self.wids['texto'])
                return
            # Y activo la función de notificación:
            self.objeto.notificador.activar(self.aviso_actualizacion)
            self.activar_widgets(True)
        self.actualizar_ventana()

    def guardar(self, widget):
        """
        Guarda el contenido de los entry y demás widgets de entrada
        de datos en el objeto y lo sincroniza con la BD.
        """
        # Desactivo el notificador momentáneamente
        self.objeto.notificador.desactivar()
        # Actualizo los datos del objeto
        adaptadores = self.adaptador.get_adaptadores()
        for col in adaptadores:
            setattr(self.objeto, col.name, adaptadores[col]['leer']())
        # Fuerzo la actualización de la BD y no espero a que SQLObject 
        # lo haga por mí:
        self.objeto.syncUpdate()
        self.objeto.sync()
        # Vuelvo a activar el notificador
        self.objeto.notificador.activar(self.aviso_actualizacion)
        self.actualizar_ventana()
        self.wids['b_guardar'].set_sensitive(False)

    def borrar(self, widget):
        """
        Elimina la cuenta de la tabla pero NO
        intenta eliminar ninguna de sus relaciones,
        de forma que si se incumple alguna 
        restricción de la BD, cancelará la eliminación
        y avisará al usuario.
        """
        if not utils.dialogo('¿Eliminar %s?'%self.clase.sqlmeta.table.lower(), 
                             'BORRAR', 
                             padre = self.wids['ventana']):
            return
        self.objeto.notificador.desactivar()
        try:
            self.objeto.destroySelf()
        except Exception, e:
            self.logger.error("grupos_alumnos.py::borrar -> %s ID %d no se "
                              "pudo eliminar. Excepción: %s." % (
                                self.objeto.sqlmeta.table, self.objeto.id, e))
            utils.dialogo_info(
                titulo = "%s NO BORRADO" % self.clase.sqlmeta.table.upper(), 
                texto = "%s no se pudo eliminar.\n\nSe generó un informe de "
                        "error en el «log» de la aplicación." % (
                            self.clase.sqlmeta.table.title()),
                padre = self.wids['ventana'])
            self.actualizar_ventana()
            return
        self.objeto = None
        self.ir_a_primero()

if __name__ == "__main__":
    p = GruposAlumnos()

