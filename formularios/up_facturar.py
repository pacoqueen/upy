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
## up_facturar.py - Ventana para facturar clases "automáticamente".
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

class FacturacionAuto(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        Ventana.__init__(self, 'up_facturar.glade', objeto)
        self.objeto = objeto
        self.usuario = usuario
        connections = {'b_salir/clicked': self.salir,
                       'b_imprimir/clicked': self.imprimir,
                       'b_buscar/clicked': self.rellenar_widgets, 
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin, 
                       'b_facturar/clicked': self.facturar_seleccionado, 
                       'b_facturar_todo/clicked': self.facturar_todo, 
                       'b_clear_fechainicio/clicked': self.limpiar_fecha, 
                       'b_clear_fechafin/clicked': self.limpiar_fecha, 
                      }
        self.add_connections(connections)
        self.inicializar_ventana()
        if self.objeto:
            utils.combo_set_from_db(self.wids['cbe_cliente'], objeto.id)
            self.rellenar_widgets()
        else:
            utils.combo_set_from_db(self.wids['cbe_cliente'], None)
        self.wids['e_fechainicio'].set_text(
            utils.str_fecha(utils.primero_de_mes()))
        gtk.main()

    def limpiar_fecha(self, boton):
        """
        Borra la fecha del entry correspondiente al botón.
        """
        nombre_entry = "e_" + boton.name.split("_")[-1]
        self.wids[nombre_entry].set_text("")

    def set_inicio(self,boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'], 
            fecha_defecto = self.wids['e_fechainicio'].get_text())
        self.wids['e_fechainicio'].set_text(utils.str_fecha(temp))
        self.inicio = str(temp[2])+'/'+str(temp[1])+'/'+str(temp[0])

    def set_fin(self,boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'],
            fecha_defecto = self.wids['e_fechafin'].get_text())
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        self.fin = str(temp[2])+'/'+str(temp[1])+'/'+str(temp[0])

    def inicializar_ventana(self, objeto = None):
        """
        Inicializa los widgets de la ventana.
        """
        cols = (('Cliente', 'gobject.TYPE_STRING', False, True, True, None),
                ('Importe','gobject.TYPE_STRING', False, False, True, None), 
                ('PUID', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_datos'], cols, multi = True)
        self.wids['tv_datos'].connect("row-activated", self.abrir_cliente)
        clientes = pclases.Cliente.select(
            pclases.Cliente.q.inhabilitado == False, 
            orderBy = "nombre")
        opciones = [(c.id, c.nombre) for c in clientes]
        utils.rellenar_lista(self.wids['cbe_cliente'], opciones)
        col = self.wids['tv_datos'].get_column(1)
        for cell in col.get_cell_renderers():
            cell.set_property("xalign", 1)
        self.wids['b_imprimir'].set_property("visible", False)
        self.wids['b_exportar'].set_property("visible", False)

    def abrir_cliente(self, tv, path, cv):
        """
        Abre el cliente seleccionado en una nueva ventana.
        """
        model = tv.get_model()
        while model[path].parent:
            path = model[path].parent.path
        puid = model[path][-1]
        objeto = pclases.getObjetoPUID(puid)
        import clientes
        v = clientes.Clientes(objeto, usuario = self.usuario)
        

    def rellenar_widgets(self, *args, **kw):
        """
        Rellena la información de los widgets, que es básicamente el 
        TreeView de alumnos a través del evento "changed" del profesor.
        """
        try:
            self.objeto = pclases.Cliente.get(
                utils.combo_get_value(self.wids['cbe_cliente']))
        except:
            self.objeto = None
        try:
            fechaini = utils.parse_fecha(self.wids['e_fechainicio'].get_text())
        except ValueError:
            fechaini = None
        try:
            fechafin = utils.parse_fecha(self.wids['e_fechafin'].get_text())
        except ValueError:
            fechafin = None
        self.resultado = buscar_clases(self.objeto, fechaini, fechafin, 
                                       self.wids['ventana'])
        self.rellenar_tabla(self.resultado)
        if self.objeto:
            self.wids['tv_datos'].expand_all()

    def rellenar_tabla(self, res):
        """
        Rellena la tabla de datos con los resultados del diccionario.
        """
        model = self.wids['tv_datos'].get_model()
        model.clear()
        if not res:
            self.wids['e_total'].set_text("")
            return
        total = 0.0
        productos = {}  # Para facturar solo una vez cada producto a 
                        # cada cliente.
                        # TO-DO: OJO: Si se deja más de un producto sin 
                        # facturar en el mismo periodo de la consulta, solo se 
                        # va a ver una vez.
        for cliente in res:
            if cliente not in productos:
                productos[cliente] = []
            abuelo = model.append(None, (cliente.nombre, 
                                         "0.00", 
                                         cliente.get_puid()))
            for p in res[cliente]:
                try:
                    descripcion_producto = p.descripcion
                    puid_producto = p.get_puid()
                except AttributeError:
                    descripcion_producto = "Sin producto relacionado "\
                                           "(clases sueltas)"
                    puid_producto = ""
                padre = model.append(abuelo, (descripcion_producto, 
                                              "0.00", 
                                              puid_producto))
                for a in res[cliente][p]:
                    producto = a.get_or_guess_productoCompra()
                    if producto not in productos[cliente]:
                        importe = a.get_precio(cliente)
                        model.append(padre, (a.get_hora_y_descripcion(), 
                                             utils.float2str(importe), 
                                             a.get_puid()))
                        model[padre][1] = utils.float2str(
                            utils._float(model[padre][1]) + importe)
                        model[abuelo][1] = utils.float2str(
                            utils._float(model[abuelo][1]) + importe)
                        total += importe
                        productos[cliente].append(producto)
        self.wids['e_total'].set_text(utils.float2str(total))

    def chequear_cambios(self):
        pass

    def imprimir(self,boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        if not self.objeto:
            return 
        import sys, os
        sys.path.append(os.path.join("..", "informes"))
        from treeview2pdf import treeview2pdf
        from informes import abrir_pdf
        fechaini = self.wids['e_fechainicio'].get_text().strip()
        fechafin = self.wids['e_fechafin'].get_text().strip()
        if not fechaini and not fechafin:
            cadfecha = ""
        elif fechaini and not fechafin:
            cadfecha = fechaini
        elif not fechaini and fechafin:
            cadfecha = fechafin
        else:
            cadfecha = "De " + fechaini + " a " + fechafin
        abrir_pdf(treeview2pdf(self.wids['tv_datos'], 
                  titulo = "Facturación pendiente", 
                  fecha = cadfecha))

    def facturar_seleccionado(self, boton):
        """
        Factura las actividades seleccionadas.
        """
        sel = self.wids['tv_datos'].get_selection()
        model, iters = sel.get_selected_rows()
        a_facturar = {}
        for iter in iters:
            puid = model[iter][-1]
            try:
                objeto = pclases.getObjetoPUID(puid)
            except ValueError:
                continue    # Es una clase sin producto relacionado.
            if isinstance(objeto, pclases.Cliente):
                # Facturar todas las actividades del cliente.
                for iterproducto in model[iter].iterchildren():
                    iterproducto = iterproducto.iter
                    for iteractividad in model[iterproducto].iterchildren():
                        try:
                            actividad=pclases.getObjetoPUID(iteractividad[-1])
                        except ValueError:
                            continue # Es una clase sin producto relacionado.
                        try:
                            a_facturar[objeto].append(actividad)
                        except KeyError:
                            a_facturar[objeto] = [actividad]
            elif isinstance(objeto, pclases.ProductoCompra):
                producto = objeto
                puidcliente = model[iter].parent[-1]
                cliente = pclases.getObjetoPUID(puidcliente)
                for iterhijo in model[iter].iterchildren():
                    try:
                        actividad = pclases.getObjetoPUID(iterhijo[-1])
                    except ValueError:
                        continue    # Es una clase sin producto relacionado.
                    try:
                        a_facturar[cliente].append(actividad)
                    except KeyError:
                        a_facturar[cliente] = [actividad]
            elif isinstance(objeto, pclases.Actividad):
                actividad = objeto
                puid = model[iter].parent.parent[-1]
                cliente = pclases.getObjetoPUID(puid)
                try:
                    a_facturar[cliente].append(actividad)
                except KeyError:
                    a_facturar[cliente] = [actividad]
            # Como solo muestro una actividad por producto, para no 
            # multiplicar por el número de clases el importe del producto 
            # completo, ahora tengo que mandar a facturar todas las 
            # actividades del mismo producto que no han entrado en el model 
            # pero que están en self.resultado.
            try:
                producto = actividad.get_or_guess_productoCompra()
            except UnboundLocalError:   # No hay actividad a facturar. El 
                pass                    # cliente no tenía hijos o vete tú 
            else:                       # a saber.
                a_facturar[cliente] += self.resultado[cliente][producto]
        self.crear_facturas(a_facturar)

    def facturar_todo(self, boton):
        """
        Factura todo lo mostrado en la consulta
        """
        self.wids['tv_datos'].get_selection().select_all()
        self.facturar_seleccionado(None)

    def crear_facturas(self, a_facturar):
        """
        Crea una factura por cliente con las actividades como servicios.
        Abre una ventana por factura creada para revisar e imprimir.
        """
        for cliente in a_facturar:
            facturar(cliente, a_facturar[cliente], self.usuario, 
                     self.wids['ventana'], 
                     abrir_ventana_facturas = True)
        self.rellenar_widgets()

def facturar(cliente, actividades, usuario = None, ventana_padre = None, 
             abrir_ventana_facturas = False, 
             intentar_marcar_como_cobrada = True, 
             servicios = [], 
             fecha = None):
    """
    Crea una factura con los servicios correspondientes a las actividades.
    Abre una ventana para la nueva factura.
    
    @param cliente: Cliente al que se le hará la factura. Si no tiene 
                    contador, dará un error por pantalla.
    @param actividades: Actividades a facturar.
    @param usuario: Usuario de la ventana. Se usará para determinar los 
                    permisos de la ventana de facturas de venta.
    @param ventana_padre: Ventana padre para hacer modal los diálogos.
    @param abrir_ventana_facturas: Si True, abre una ventana nueva con 
                                   la factura creada.
    @param intentar_marcar_como_cobrada: Si True y la forma de pago es 
                                         efectivo o metálico, creará los 
                                         cobros correspondientes.
    @param servicios: Añade los servicios recibidos a la factura. Ignorará 
                      entonces las actividades. Si no se recibe, creará un 
                      servicio para todas las actividades pasadas.
    """
    # PLAN: ¿Tal vez debería generar los PDF y abrirlos y ya está? Para eso 
    # tendría que crear los vencimientos también. Ojo.
    # OJO: TODO: No chequea las restricciones de riesgo para facturar al 
    # cliente ni nada de eso. "Muncho" cuidado.
    if not cliente.contador:
        utils.dialogo_info(titulo = "CLIENTE SIN CONTADOR", 
            texto = "El cliente %s no tiene contador asignado.\n"
                    "Debe asignarle uno desde la ventana correspondiente."
                    % cliente.nombre,
            padre = ventana_padre)
        return
    # 0.- Compruebo que tengo datos mínimos suficientes: cliente y líneas 
    # que facturar.
    if not servicios:
        servicios = generar_servicios(actividades, descripcion = None)
    # 7.- Creo la factura de venta.
    fra = crear_nueva_factura_venta(cliente, fecha)
    # 8.- Asocio los servicios del albarán a la factura.
    for srv in servicios:
        srv.facturaVenta = fra
    # 9.- Si la forma de pago es efectivo, marcar como cobrada por defecto:ç
    if intentar_marcar_como_cobrada:
        marcar_como_cobrada_si_procede(fra)
    # 10.- Abro la factura en una ventana nueva. Se cerrará sola 
    #      cuando el usuario la imprima.
    if abrir_ventana_facturas:
        import facturas_venta
        vfras = facturas_venta.FacturasVenta(objeto = fra, 
                                             usuario = usuario)
    return fra

def crear_nueva_factura_venta(cliente, fecha = None):
    """
    Crea una factura de venta con los datos por defecto obtenidos del cliente.
    OJO: No se chequea que el cliente o no tenga contador asignado.
    """
    contador = cliente.contador
    last_fra = contador.get_last_factura_creada()
    if not fecha:
        fecha = datetime.date.today()
    if last_fra:
        if last_fra.fecha <= fecha:
            fecha = fecha
        else:
            if last_fra.fecha > datetime.date.today():
                fecha = last_fra.fecha
            else:
                fecha = datetime.date.today()
            # fecha = max(last_fra.fecha, datetime.date.today()) <- Esto falla con el psyco de U.P. Me curro mi propio max.
    else:
        fecha = fecha 
    dde = pclases.DatosDeLaEmpresa.select()[0]
    numfactura = contador.get_next_numfactura(commit = True)
    fra = pclases.FacturaVenta(
        cliente = cliente, 
        fecha = fecha, 
        numfactura = numfactura, 
        descuento = 0.0, 
        observaciones = "", 
        iva = cliente.iva, 
        bloqueada = False, 
        irpf = dde.irpf)
    return fra

def marcar_como_cobrada_si_procede(fra):
    """
    Si la forma de pago es "EFECTIVO", "CONTADO" o "METÁLICO", marca la 
    factura como cobrada.
    Para ello crea los vencimientos por defecto, etc.
    """
    vtos = fra.crear_vencimientos_por_defecto()
    for vto in vtos:    # Un cobro por vencimiento.
        formacobro = vto.observaciones.strip().upper()
        if ("EFECTIVO" in formacobro or "CONTADO" in formacobro or 
            ("MET" in formacobro and "LICO" in formacobro)):
            pclases.Cobro(facturaVenta = fra, 
                          importe = vto.importe, 
                          observaciones = "Marcada como cobrada "
                            "automáticamente desde ventana de facturación "
                            "por lotes", 
                          cliente = fra.cliente)

def generar_servicios(actividades, descripcion = "Clases Pilates", 
                      precio = None):
    """
    Crea una línea de servicio al precio indicado por cada actividad.
    Agrupa las actividades en función de la descripción y el precio. Todas 
    las actividades con la misma descripción y el mismo precio 
    conformarán un único servicio.
    """
    srvs = {}
    for a in actividades:
        if not isinstance(a, pclases.Actividad):
            continue    # Es un nodo producto, pasando.
        if not descripcion:
            descripcion = a.get_hora_y_descripcion()
        if not a.get_or_guess_productoCompra():    
            # Clase suelta o algo así, cuento horas.
            horas = a.calcular_duracion()
        else:
            horas = 1 #Facturo cada bono o lote de clases como una sola unidad.
        if precio is None:
            precio = a.get_precio()
        if descripcion not in srvs:
            srvs[descripcion] = {}
        if precio not in srvs[descripcion]:
            srv = pclases.Servicio(facturaVenta = None, prefactura = None, 
                               albaranSalida = None, concepto = descripcion, 
                               cantidad = horas, precio = precio, 
                               descuento = 0.0, pedidoVenta = None, 
                               presupuesto = None, #actividad = a,  
                               notas = "") 
            srvs[descripcion][precio] = srv
        else:
            if not a.get_or_guess_productoCompra(): # Si tiene producto, 
                srv = srvs[descripcion][precio]     # cuenta como 1. No sigo 
                srv.cantidad += horas               # sumando cantidades.
        a.servicio = srv
        a.servicio.notas += a.get_fecha_hora_y_descripcion() + "\n"
        a.sync()
    servicios = []
    for descripcion in srvs:
        for precio in srvs[descripcion]:
            servicios.append(srvs[descripcion][precio])
    return servicios

def buscar_clases(cliente, fechaini, fechafin, ventana_padre = None):
    """
    Busca todas las clases no facturadas del cliente (de todos, si es None) 
    entre las fechas fechaini y fechafin (o todas, si son None).
    Devuelve los resultados en forma de diccionario con listas por cliente.
    """
    vpro = ventana_progreso.VentanaProgreso(padre = ventana_padre)
    txtpro = "Buscando actividades no facturadas..."
    vpro.set_valor(0.0, txtpro)
    vpro.mostrar()
    acts = pclases.Actividad.buscar_actividades_de(cliente, fechaini, fechafin)
    tot = acts.count()
    # Inicialización de diccionario de resultados.
    res = {}
    if not cliente:
        for c in pclases.Cliente.select():
            res[c] = {}
    elif isinstance(cliente, pclases.Cliente):
        res[cliente] = {}
    else:
        for c in cliente:
            res[c] = {}
    i = 0.0
    try:
        tot = len(acts)
    except TypeError:
        tot = acts.count()
    for a in acts:
        if pclases.DEBUG:
            print " >>> up_facturar::buscar_clases"
            print "\t%s (%d clientes)" % (a.get_info(), len(a.clientes))
        i += 1
        vpro.set_valor(i / tot, txtpro + " [%d]" % a.id)
        a.sync()
        for c in a.clientes:
            if pclases.DEBUG:
                print "\t\t%s..." % (c.get_info()),
            if c not in res:
                if pclases.DEBUG:
                    print "El cliente no interesa."
                continue    # No es el cliente que ha pedido el usuario.
                #res[c] = {}
            if a.esta_facturado_para(c):
                if pclases.DEBUG:
                    print "La clase ya está facturada." 
                continue    # Ya se le facturó al cliente.
            producto = a.get_or_guess_productoCompra(cliente = c)
            if pclases.DEBUG:
                print "Se facturará la clase como %s." % (
                    producto and producto.get_info() or "*clase suelta*")
            try:
                res[c][producto].append(a)
            except KeyError:
                res[c][producto] = [a]
    vpro.ocultar()
    if pclases.DEBUG:
        try:
            cantidad_clientes = len(cliente)
        except:
            if isinstance(cliente, pclases.Cliente):
                cantidad_clientes = 1
            else:
                cantidad_clientes = pclases.Cliente.select().count()
        print " <<< %d clases encontradas para %d clientes. "\
              "fechaini: %s; fechafin: %s" % (len(res), cantidad_clientes,
                                              fechaini, fechafin)
    return res


if __name__ == '__main__':
    t = FacturacionAuto()

