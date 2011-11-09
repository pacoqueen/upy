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
## up_report_diario.py - Ventana de asistencia a clase.
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
import sys, os, tempfile

class ReportDiario(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        Ventana.__init__(self, 'up_report_diario.glade', objeto)
        self.objeto = objeto
        self.usuario = usuario
        self.inicializar_ventana()
        connections = {'b_salir/clicked': self.salir,
                       'b_imprimir/clicked': self.imprimir,
                       'b_refrescar/clicked': self.actualizar, 
                       'b_send/clicked': self.enviar_por_correoe, 
                       'b_fecha_ini/clicked': self.set_inicio, 
                       'b_fecha_fin/clicked': self.set_fin, 
                      }
        self.add_connections(connections)
        hoy = datetime.datetime.today()
        self.wids['e_fecha_ini'].set_text(utils.str_fecha(hoy))
        self.wids['e_fecha_fin'].set_text(utils.str_fecha(hoy))
        self.dia_seleccionado, self.fechafin = self.get_fechas_mostradas()
        self.fechaini = self.dia_seleccionado
        self.actualizar()
        gtk.main()

    def set_inicio(self,boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'], 
            fecha_defecto = self.wids['e_fecha_ini'].get_text())
        self.wids['e_fecha_ini'].set_text(utils.str_fecha(temp))
        self.inicio = str(temp[2])+'/'+str(temp[1])+'/'+str(temp[0])

    def set_fin(self,boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'],
            fecha_defecto = self.wids['e_fecha_fin'].get_text())
        self.wids['e_fecha_fin'].set_text(utils.str_fecha(temp))
        self.fin = str(temp[2])+'/'+str(temp[1])+'/'+str(temp[0])

    def inicializar_ventana(self, objeto = None):
        """
        Inicializa los widgets de la ventana.
        """
        pixbuf_logo = gtk.gdk.pixbuf_new_from_file(
            pathjoin("..", "imagenes", "logo_up.gif"))
        pixbuf_logo = escalar_a(200, 100, pixbuf_logo)
        self.wids['logo'].set_from_pixbuf(pixbuf_logo)
        cols = (('Concepto', 'gobject.TYPE_STRING', False, True, True, None),
                ('Importe','gobject.TYPE_FLOAT', False, False, True, None),
                ('PUID', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_datos'], cols)
        self.wids['tv_datos'].connect("row-activated", self.abrir_calendario)
        self.wids['tv_datos'].set_headers_visible(False)
        colores = {}
        for g in pclases.GrupoAlumnos.select():
            color = gtk.gdk.Color(*g.get_gdk_color_params())
            colores[g.nombre] = color.to_string()
        self.grafica = charting.add_grafica_barras_verticales(
                                    self.wids['a_grafica'], [], [], 
                                    ver_botones_colores = False, 
                                    ver_etiquetas_montones = True, 
                                    colores = colores)
        self.grafica_rangos = charting.add_grafica_rangos(
                                    self.wids['a_grafica_rangos'], [], [])
        self.grafica_horas = charting.add_grafica_simple(
                                    self.wids['a_grafica_horas'], 
                                    map(lambda h: "%02d:00" % h, xrange(24)), 
                                    [0.0] * 24)
        self.wids['ventana'].resize(1024, 600)

    def abrir_calendario(self, tv, path, cv):
        """
        Abre el calendario con el día del evento seleccionado.
        """
        model = tv.get_model()
        puid = model[path][-1]
        if puid:
            objeto = pclases.getObjetoPUID(puid)
            if hasattr(objeto, "fechahoraInicio"):
                import up_calendario 
                v = up_calendario.Calendario(usuario = self.usuario, 
                                             objeto = objeto)
            elif isinstance(objeto, pclases.Cobro):
                fra = objeto.facturaVenta
                import facturas_venta
                v = facturas_venta.FacturasVenta(usuario = self.usuario, 
                                                 objeto = fra)

    def rellenar_widgets(self):
        """
        Rellena la información de los widgets, que es básicamente el 
        TreeView de alumnos a través del evento "changed" del profesor.
        """
        fechaini, fechafin = self.get_fechas_mostradas()
        self.rellenar_tabla(fechaini, fechafin)
        self.wids['tv_datos'].expand_all()
        self.actualizar_graficas(fechaini, fechafin)
    
    def actualizar_graficas(self, fechaini, fechafin):
        self.monitores = []
        self.horas = {}
        self.grupos = []
        acts = buscar_actividades(fechaini, fechafin) 
        for a in acts:
            nombre_monitor = (a.empleado 
                              and a.empleado.get_nombre_completo() 
                              or "Sin monitor asignado")
            if nombre_monitor not in self.monitores:
                self.monitores.append(nombre_monitor)
            grupo = "+".join([g.nombre for g in a.gruposAlumnos])
            if not grupo:
                grupo = a.descripcion
            if grupo not in self.grupos:
                self.grupos.append(grupo)
            try:
                self.horas[nombre_monitor][grupo] += a.calcular_duracion()
            except KeyError:
                try:
                    self.horas[nombre_monitor][grupo] = a.calcular_duracion()
                except KeyError:
                    self.horas[nombre_monitor] = {grupo: a.calcular_duracion()}
        self.monitores.sort()
        self.grupos.sort()
        valores = []
        for m in self.monitores:
            barra = []
            for g in self.grupos:
                try:
                    d = self.horas[m][g]
                except KeyError:
                    d = 0
                barra.append(d)
            valores.append(barra)
        claves = self.monitores
        montones = self.grupos
        self.grafica.plot(claves, valores, montones)
        # Gráfica rangos
        claves = []
        valores = []
        for e in self.clases_por_empleado.keys():
            try:
                valores.append(self.clases_por_empleado[e])
            except KeyError:    
                pass    # El empleado no tiene clases. No valores.
            else:
                claves.append(e and e.nombre or "Sin monitor")
        self.grafica_rangos.plot(claves, valores, start_time = 8 * 60, 
                                 end_time = 22 * 60)
        # Gráfica importes medios por hora
        valores = []
        for h in xrange(24):
            try:
                valores.append(["%02d:00" % h, self.data_graf_horas[h]])
            except KeyError:
                valores.append(["%02d:00" % h, 0.0])
        claves = map(lambda h: "%02d:00" % h, xrange(24))
        self.grafica_horas.plot(valores)

    def guardar_graficas_en(self, nomfichero1, nomfichero2, nomfichero3):
        for grafica, nomfichero in ((self.grafica, nomfichero1), 
                                    (self.grafica_rangos, nomfichero2), 
                                    (self.grafica_horas, nomfichero3)):
            ancho, alto = grafica.window.get_geometry()[2:4]
            pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, ancho, alto) #@UndefinedVariable
            pb = pb.get_from_drawable(grafica.window, 
                                      cmap = grafica.window.get_colormap(), 
                                      src_x = 0, src_y = 0, 
                                      dest_x = 0, dest_y = 0, 
                                      width = ancho, height = alto)
            pb.save(nomfichero, "png")

    def rellenar_tabla(self, fechaini, fechafin):
        """
        Rellena el TreeView con los datos del día: memos, to-dos y asistencias.
        """
        # TODO: Mostrar también los gastos del día (de las facturas de compra).
        model = self.wids['tv_datos'].get_model()
        model.clear()
        padres = {"Prospects": model.append(None, ("Eventos", 0.0, "")), 
                  "Clases": model.append(None, ("Clases", 0.0, "")), 
                  "TOTAL": model.append(None, ("Total", 0.0, "")), 
                  "Importe medio por hora": 
                    model.append(None, ("Importe medio por hora", 0.0, "")), 
                  "Horas": model.append(None, ("Horas", 0.0, "")), 
                  "Cobros": model.append(None, ("Cobros", 0.0, ""))}
        self.rellenar_resto(fechaini, fechafin, padres)
        self.rellenar_clases(fechaini, fechafin, padres)
        self.rellenar_horas(fechaini, fechafin, padres)
        self.rellenar_cobros(fechaini, fechafin, padres)
    
    def rellenar_resto(self, fechaini, fechafin, padres):
        """
        Rellena el resto de información de la tabla: memos y tareas.
        """
        nodos_categorias = {}
        model = self.wids['tv_datos'].get_model()
        M = pclases.Memo
        memos = M.select(pclases.AND(
                            M.q.fechahora >= fechaini, 
                            M.q.fechahora < 
                                fechafin + datetime.timedelta(days=1)), 
                         orderBy = "fechahora")
        for m in memos:
            try:
                nodo_categoria = nodos_categorias[m.categoria]
            except KeyError:
                categoria = m.categoria
                nodo_categoria = model.append(padres["Prospects"], 
                    (categoria and categoria.nombre or "Sin clasificar", 
                     0, None))
            fila = (m.resumen, 0, m.get_puid())
            model.append(nodo_categoria, fila)
        T = pclases.Tarea
        tareas = T.select(pclases.AND(
                            T.q.fechahora >= fechaini, 
                            T.q.fechahora < 
                                fechafin + datetime.timedelta(days=1)), 
                         orderBy = "fechahora")
        for t in tareas:
            try:
                nodo_categoria = nodos_categorias[t.categoria]
            except KeyError:
                categoria = t.categoria
                nodo_categoria = model.append(padres["Prospects"], 
                    (categoria and categoria.nombre or "Sin clasificar", 
                     0, None))
            fila = (t.resumen, 0, t.get_puid())
            model.append(nodo_categoria, fila)

    def rellenar_horas(self, fechaini, fechafin, padres):
        """
        Introduce las horas trabajadas por cada empleado en el día recibido. 
        Saca la información a partir del calendario (tabla «actividad»).
        """
        self.empleados = []
        model = self.wids['tv_datos'].get_model()
        fechaini, fechafin = self.get_fechas_mostradas()
        actividades = buscar_actividades(fechaini, fechafin) 
        data = {}
        dprofs = {}
        for a in actividades:
            horas_clase = (a.fechahoraInicio.hour * 60 
                               + a.fechahoraInicio.minute, 
                               a.fechahoraFin.hour * 60 
                               + a.fechahoraFin.minute)
            try:
                data[a.empleado] += a.calcular_duracion()
                dprofs[a.empleado].append(horas_clase)
            except KeyError:
                data[a.empleado] = a.calcular_duracion()
                dprofs[a.empleado] = [horas_clase]
        for e in data:
            if e is None:
                nombre = "Sin monitor"
            else:
                nombre = e.get_nombre_completo()
            fila = (nombre, data[e], e and e.get_puid() or "")
            model.append(padres["Horas"], fila)
            model[padres['Horas']][1] += fila[1]
        self.clases_por_empleado = dprofs

    def rellenar_cobros(self, fechaini, fechafin, padres):
        """
        Extrae de la tabla de cobros todos aquellos con fecha coincidente con 
        la recibida.
        """
        model = self.wids['tv_datos'].get_model()
        C = pclases.Cobro
        cobros = C.select(pclases.AND(
            C.q.fecha >= fechaini, 
            C.q.fecha < fechafin + datetime.timedelta(days = 1)))
        por_formapago = {}
        for c in cobros:
            formapago = c.get_formadepago()
            try:
                padre = por_formapago[formapago]
            except KeyError:
                rowformapago = (formapago, 0.0, None)
                padre = por_formapago[formapago] = model.append(
                    padres["Cobros"], rowformapago)
            concepto_fra = ""
            if c.facturaVenta:
                concepto_fra = "Factura %s (%s) [%s]" % (
                                    c.facturaVenta.numfactura, 
                                    c.cliente.nombre, 
                                    utils.str_fecha(c.facturaVenta.fecha))
            fila = (concepto_fra, 
                    c.importe,  
                    c.get_puid())
            model.append(padre, fila)
            model[padre][1] += c.importe
            model[padres["Cobros"]][1] += c.importe

    def rellenar_clases(self, fechaini, fechafin, padres):
        """
        Rellena el TreeView con los datos del día: memos, to-dos y asistencias.
        """
        acts = buscar_actividades(fechaini, fechafin)
        model = self.wids['tv_datos'].get_model()
        horas = {}
        total = 0.0
        self.data_graf_horas = {}
        filas_horas = []
        for a in acts:
            hora = a.fechahoraInicio.hour
            try:
                padre = horas[hora]
            except KeyError:
                padre = model.append(padres["Clases"], 
                                     ("%02d:00" % (hora),
                                      0.0, ""))
                horas[hora] = padre
                self.data_graf_horas[hora] = 0.0
                filas_horas.append(padre)
            numalmunos = len(a.clientes)
            producto = a.get_or_guess_productoCompra()
            try:
                importe_clase = producto.calcular_precio_medio_clase()
            except AttributeError:
                importe_clase = 0    # XXX: TODO: FIXME: ES TEMPORAL. ¡CAMBIAR POR UNA SOLUCIÓN DE VERDAD SI NO ENCUENTRO EL PRODUCTO RELACIONADO CON LA CLASE!
                if pclases.DEBUG:
                    print a.get_puid(), "Producto no encontrado para la actividad", a
            importe_clase *= len(a.clientes)
            nombre_monitor = (a.empleado 
                              and a.empleado.get_nombre_completo() 
                              or "Sin monitor asignado")
            fila = (a.descripcion + " (%d pax) [%s]" % (numalmunos, 
                                                        nombre_monitor),  
                    importe_clase, 
                    a.get_puid())
            total += importe_clase
            self.data_graf_horas[hora] += importe_clase
            # DONE: Aunque alguien no haya asistido, se le va a cobrar igual.
            #       Se le cobra el bono, así que sí, se cobra.
            nodo = model.append(padre, fila)
            model[nodo].parent[1] += importe_clase
            model[nodo].parent.parent[1] += importe_clase
            # NOTA: ¿Le gustará los totales así a Javier Bseiso? Seguro que no 
            # quiere que aparezcan los ceros en Prospect ni el desglose de 
            # subtotales por hora.
        model[padres["TOTAL"]][1] = total
        try:
            media_por_hora = total / len(horas)
        except ZeroDivisionError:
            media_por_hora = 0
        model[padres["Importe medio por hora"]][1] = media_por_hora
        # Ahora porcentajes:
        for fila in filas_horas:
            try:
                porcentaje = model[fila][1] / total
            except ZeroDivisionError:
                porcentaje = 0.0
            model[fila][0] += " (%s %%)" % utils.float2str(porcentaje*100.0, 1)

    def actualizar(self, *args, **kw):
        self.rellenar_widgets()

    def chequear_cambios(self):
        pass

    def imprimir(self,boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        from treeview2pdf import treeview2pdf
        from informes import abrir_pdf
        sys.path.append(os.path.join("..", "informes"))
        fechaini, fechafin = self.get_fechas_mostradas()
        if fechaini == fechafin:
            strfecha = fechaini.strftime("%d/%m/%Y")
        else:
            strfecha = "De %s a %s" % (fechaini.strftime("%d/%m/%Y"), 
                                       fechafin.strftime("%d/%m/%Y"))
        abrir_pdf(treeview2pdf(self.wids['tv_datos'], 
                  titulo = "Informe diario",  
                  fecha = strfecha))

    def get_fechas_mostradas(self):
        """
        Devuelve la fecha inicial y final de los datos mostrados.
        """
        fini = self.wids['e_fecha_ini'].get_text()
        fini = utils.parse_fecha(fini)
        ffin =  self.wids['e_fecha_fin'].get_text()
        ffin = utils.parse_fecha(ffin)
        return fini, ffin

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

    def guardar_graficas(self):
        tmpdir = tempfile.gettempdir()
        nomfgraf1 = "g%s_1.png" % (datetime.date.today().toordinal() * 100
                                  + datetime.datetime.now().second)  
        nomfgraf2 = "g%s_2.png" % (datetime.date.today().toordinal() * 100
                                  + datetime.datetime.now().second)
        nomfgraf3 = "g%s_3.png" % (datetime.date.today().toordinal() * 100
                                  + datetime.datetime.now().second)
        ruta_grafica1 = os.path.join(tmpdir, nomfgraf1)
        ruta_grafica2 = os.path.join(tmpdir, nomfgraf2)
        ruta_grafica3 = os.path.join(tmpdir, nomfgraf3)
        self.guardar_graficas_en(ruta_grafica1, ruta_grafica2, ruta_grafica3)
        return ruta_grafica1, ruta_grafica2, ruta_grafica3

    def enviar_por_correoe(self, boton):
        """
        Envía el informe por correo electrónico.
        """
        import treeview2csv
        fcsv = treeview2csv.treeview2csv(self.wids['tv_datos'], 
                                         filtro_ceros = [1])
        #txt = "\n".join(open(fcsv).readlines())
        txt = csv2html(fcsv)
        dests = ["javier@universalpilates.es", "alopez@universalpilates.es"]
        # 20101119: Adri quiere que solo le llegue a ella.
        dests = ["alopez@universalpilates.es"]
        self.wids['ventana'].window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        while gtk.events_pending(): gtk.main_iteration(False)
        try:
            fechaini, fechafin = self.get_fechas_mostradas()
            if fechaini == fechafin:
                asunto = "Informe diario: %s" % fechaini.strftime(
                                            "%d/%m/%Y")
            else:
                asunto = "Informe de %s a %s" % (
                    fechaini.strftime("%d/%m/%Y"), 
                    fechafin.strftime("%d/%m/%Y"))
            adjuntos = self.guardar_graficas()
            # TODO: Harcoded no, por favor. Meter en algún tipo de 
            # configuración o algo.
            res = utils.enviar_correoe("alopez@universalpilates.es", 
                                       dests, 
                                       asunto = asunto,
                                       texto = txt, 
                                       servidor = "smtp.universalpilates.es", 
                                       password = "Lope48", 
                                       usuario = "tbs349c", 
                                       ssl = False, 
                                       html = True, 
                                       adjuntos = adjuntos)
        except:
            res = False
        finally:
            self.wids['ventana'].window.set_cursor(None)
        if res:
            utils.dialogo_info(titulo = "CORREO-E ENVIADO", 
                texto = "El informe se envió correctamente a:\n%s" 
                            % "\n".join(dests), 
                padre = self.wids['ventana'])
        else:
            utils.dialogo_info(titulo = "ERROR AL ENVIAR CORREO-E", 
                texto = "Ocurrió un error al enviar el correo electrónico.\n"
                        "Verifique que tiene conexión a Internet, que la\n"
                        "configuración es válida y que no tiene ningún\n"
                        "cortafuegos o antivirus bloqueando las conexiones\n"
                        "salientes por el puerto 25.", 
                padre = self.wids['ventana'])

def buscar_actividades(fini, ffin):
    A = pclases.Actividad
    acts = A.select(pclases.NOT(
                        pclases.OR(
                            A.q.fechahoraFin < fini, 
                            A.q.fechahoraInicio > 
                                ffin + datetime.timedelta(days=1))), 
                        orderBy = "fechahoraInicio")
    #acts = utils.unificar([i for i in acts])   # Para no 
        # contar dos veces una actividad que empieza y acaba en el mismo 
        # día (que serán todas, presumiblemente).
    return acts

def csv2html(fcsv):
    import csv
    f = open(fcsv)
    reader = csv.reader(f, delimiter = ";", lineterminator = "\n")
    html = "<title>Report Universal Pilates</title>\n"
    html = "<table border=1 bordercolor=gray>"
    for row in reader:
        html += '<tr>'
        numcol = 0
        for column in row:
            if numcol == 1:
                try:
                    column = '<p align="right">%s</p>' % (
                        utils.float2str(utils.parse_float(column), 2))
                except:
                    pass
            else:
                if not ">" in column:
                    column = "<p><b>%s</b></p>" % column
                else:
                    column = column.replace(">", "&nbsp; &nbsp;")
            html += '<td>' + column + '</td>\n'
            numcol += 1
        html += '</tr>'
    html += '</table>'
    f.close()
    return html

if __name__ == '__main__':
    t = ReportDiario()

