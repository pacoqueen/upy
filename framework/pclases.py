#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008 Francisco José Rodríguez Bogado,                    #
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

###############################################################################
# BUG localizado: El gc no puede eliminar objetos de memoria (o al menos sus
#                 hilos) por estar las hebras pendientes del "signal" aunque el
#                 objeto persistente ya no se use más en adelante.
#                 Ver weakref y en especial este código:
#                 http://osdir.com/ml/python.general.castellano/2004-03
#                   /msg00116.html
###############################################################################

# DONE: Aún colea de vez en cuando el error en los hilos al salir del 
# intérprete de python a pesar de que ya he solucionado otros muy parecidos 
# que salían también.

# DONE: URGENTE: Con el mismo objeto en dos ventanas funciona bien. Cuando hay 
# tres (o más, supongo) empieza a fallar a veces y se queda bloqueada la 
# ventana de "Actualizar".
# Esto de arriba ocurre con las señales. Tal y como se hace ahora (ver NOTAS) 
# no hay problema.

# PLAN: El _init se podría haber heredado. GAÑANAZO.

# NOTAS:
#  Ahora mismo todo esto es un batiburrillo. Las notificaciones de cambios 
# remotos, el IPC, la persistencia y todo eso de momento queda en el aire. Lo 
# voy a hacer a la forma "tradicional".
#  El ye olde check: Cada cierto tiempo comprobar si hay cambios entre los 
# atributos del objeto y los de la caché local (que aquí se llama swap por 
# motivos que no vienen a cuento), y si los hay lanzo la función definida en 
# el notificador y puto pelota.
#  ¿Qué es lo que hay que hacer entonces en cada ventana? Pues cada vez que se 
# muestren datos en pantalla se llama al make_swap y con un timeout_add que 
# chequean los cambios de vez en cuando con .chequear_cambios(). Fácil, ¿no? 
# PUES NO ME GUSTA. Prefería las notificaciones y las señales de la BD, su 
# hilo con su conexión IPC, etc...

"""
    Catálogo de clases persistentes.
"""


DEBUG = False
#DEBUG = True   # Se puede activar desde ipython después de importar con 
                # pclases.DEBUG = True
VERBOSE = True  # Activar para mostrar por pantalla progreso al cargar clases.
VERBOSE = False

if DEBUG or VERBOSE:
    print "IMPORTANDO PCLASES"

import sys, os
try:
    from sqlobject import *
except ImportError, msg:
    print "Error importando SQLObject: %s" % (msg)
    sys.exit(1)

sys.path.append(os.path.join('..', 'formularios'))
try:
    import utils
except ImportError, msg:
    print "WARNING: No se pudo importar utils. Si usa las funciones "\
          "es_nocturno() de los partes de trabajo y fabricación, o "\
          "el envío de correos electrónicos -de facturas, por ejemplo-"\
          ", saltará una excepción.\n%s" % (msg)

try:
    from utils_administracion import id_propia_empresa_cliente
except ImportError, msg:
    print "WARNING: No se pudo importar utils. Si usa el metodo es_i"\
          "nterno() de los albaranes de salida saltará una excepción"\
          ".\n%s" % (msg)

try:
    import notificacion
except:
    sys.path.append(os.path.join('..', 'formularios'))
    try:
        import notificacion
    except:
        sys.path.append('.')
        import notificacion
  
import threading#, psycopg
from select import select

from configuracion import ConfigConexion

import datetime 

# GET FUN !

config = ConfigConexion()

#conn = '%s://%s:%s@%s/%s' % (config.get_tipobd(), 
#                             config.get_user(), 
#                             config.get_pass(), 
#                             config.get_host(), 
#                             config.get_dbname())

# HACK: No reconoce el puerto en el URI y lo toma como parte del host. Lo 
# añado detrás y colará en el dsn cuando lo parsee. 
if "sqlite" in config.get_tipobd():
    connstring = """%s:///%s""" % (config.get_tipobd(), config.get_dbname())
    sqlhub.processConnection = connectionForURI(connstring, 
                                                use_table_info = True)
else:
    connstring = '%s://%s:%s@%s/%s port=%s' % (config.get_tipobd(), 
                                         config.get_user(), 
                                         config.get_pass(), 
                                         config.get_host(), 
                                         config.get_dbname(), 
                                         config.get_puerto()) 
    sqlhub.processConnection = connectionForURI(connstring)


class SQLtuple(tuple):
    """
    Básicamemte una tupla, pero con la función .count() para hacerla 
    "compatible" con los SelectResults de SQLObject.
    """
    def __init__(self, *args, **kw):
        self.elbicho = tuple(*args, **kw)
        tuple.__init__(*args, **kw)
    #def __new__(self, *args, **kw):
    #    self.elbicho = tuple(*args, **kw)
    #    tuple.__new__(*args, **kw)
    def count(self):
        return len(self)
    def sum(self, campo):
        res = 0.0
        for item in self.elbicho:
            res += getattr(item, campo)
        return res

class SQLlist(list):
    """
    Básicamemte una lista, pero con la función .count() para hacerla 
    "compatible" con los SelectResults de SQLObject.
    """
    def __init__(self, *args, **kw):
        self.rocio = list(*args, **kw)
        list.__init__(self, *args, **kw)
    def count(self):
        return len(self.rocio)
    # DISCLAIMER: Paso de otra clase base para solo 2 funciones que se repiten.
    def sum(self, campo):
        res = 0.0
        for item in self.rocio:
            res += getattr(item, campo)
        return res
    def append(self, *args, **kw):
        raise TypeError, "No se pueden añadir elementos a un SelectResults"
    def extend(self, *args, **kw):
        raise TypeError, "No se puede extender un SelectResults."
    def insert(self, *args, **kw):
        raise TypeError, "No se pueden insertar elementos en un SelectResults."
    def pop(self, *args, **kw):
        raise TypeError, "No se pueden eliminar elementos de un SelectResults."
    def remove(self, *args, **kw):
        raise TypeError, "No se pueden eliminar elementos de un SelectResults."


# HACK:
# Hago todas las consultas case-insensitive machacando la función de 
# sqlbuilder:
_CONTAINSSTRING = sqlbuilder.CONTAINSSTRING
def CONTAINSSTRING(expr, pattern):
    try:
        nombre_clase = SQLObject.sqlmeta.style.dbTableToPythonClass(
                        expr.tableName)
        clase = globals()[nombre_clase]
        columna = clase.sqlmeta.columns[expr.fieldName]
    except (AttributeError, KeyError):
        return _CONTAINSSTRING(expr, pattern)
    if isinstance(columna, (SOStringCol, SOUnicodeCol)):
        op = sqlbuilder.SQLOp("ILIKE", expr, 
                                '%' + sqlbuilder._LikeQuoted(pattern) + '%')
    elif isinstance(columna, (SOFloatCol, SOIntCol, SODecimalCol, 
                              SOMediumIntCol, SOSmallIntCol, SOTinyIntCol)):
        try:
            pattern = str(float(pattern))
        except ValueError:
            pattern = None
        if not pattern:
            op = sqlbuilder.SQLOp("IS NOT", expr, None)
        else:
            op = sqlbuilder.SQLOp("=", expr, 
                                    sqlbuilder._LikeQuoted(pattern))
    else:
        op = sqlbuilder.SQLOp("LIKE", expr, 
                                '%' + sqlbuilder._LikeQuoted(pattern) + '%')
    return op
sqlbuilder.CONTAINSSTRING = CONTAINSSTRING


class SQLObjectChanged(Exception):
    """ User-defined exception para ampliar la funcionalidad
    de SQLObject y que soporte objetos persistentes."""
    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return repr(self.value)

class PRPCTOO:
    """ 
    Clase base para heredar y no repetir código.
    Únicamente implementa los métodos para iniciar un hilo de 
    sincronización y para detenerlo cuando ya no sea necesario.
    Ningún objeto de esta clase tiene utilidad "per se".
    """
    # El nombre viene de todo lo que NO hace pero para lo que es útil:
    # PersistentRemoteProcessComunicatorThreadingObservadorObservado. TOOOOOMA.
    def __init__(self, nombre_clase_derivada = ''):
        """
        El nombre de la clase derivada pasado al 
        constructor es para la metainformación 
        del hilo.
        Si no se han construido correctamente las claves ajenas para sqlite al 
        tirar de la base de datos lo corrijo y hago aquí.
        """
        if sqlhub.getConnection().dbName == "sqlite":
            self.__repare_FK()
        self.__oderivado = nombre_clase_derivada
        self.swap = {}

    def __repare_FK(self):
        """
        Si no se han creado los campos a las claves ajenas porque viene de 
        sqlite con fromDatabase activado, las creo aquí partiendo de las 
        columnas ID.
        """
        raise NotImplementedError, "Soporte sqlite en desarrollo."
        for nombre_columna in self.sqlmeta.columns.keys()[:]:
            if nombre_columna.endswith("ID"):
                fkname = nombre_columna[:-2]
                print nombre_columna, fkname
                if fkname not in dir(self):
                    nombre_clase_ajena = fkname[0].upper() + fkname[1:]
                    self.sqlmeta.delColumn(nombre_columna)
                    self.sqlmeta.addColumn(ForeignKey(nombre_clase_ajena))
                    col = self.sqlmeta.columns[nombre_columna + "ID"]
                    col.name = fkname
                    col.dbName = fkname + "_id"

    def abrir_conexion(self):
        """
        Abre una conexión con la BD y la asigna al 
        atributo conexión de la clase.
        No sale del método hasta que consigue la
        conexión.
        """
        while 1:
            try:
                self.conexion = sqlhub.getConnection()
                txt = "pclases::PRPCTOO.abrir_conexion --> Conexión abierta."
                if DEBUG: print txt
                return
            except Exception, msg:
                txt = "pclases::PRPCTOO.abrir_conexion --> ERROR "\
                      "estableciendo conexión secundaria para IPC. Vuelvo a"\
                      " intentar. Excepción: %s" % msg
                print txt 
    
    def abrir_cursor(self):
        self.cursor = self.conexion.cursor()
        if DEBUG: print [self.cursor!=None and self.cursor or "El cursor devuelto es None."][0], self.conexion, len(self.conexion.cursors)

    def make_swap(self):
        # Antes del sync voy a copiar los datos a un swap temporal, para 
        # poder comparar:
        for campo in self.sqlmeta.columns:
            self.swap[campo] = getattr(self, campo)
        
    def comparar_swap(self):
        """
        Lanza una excepción propia para indicar que algún valor ha cambiado 
        remotamente en el objeto, comparando la caché en memoria local con 
        los valores de la BD. Como mensaje de la excepción devuelve el nombre 
        del campo que ha cambiado.
        Si han cambiado varios, saltará con el primero de ellos.
        """
        # Y ahora sincronizo:
        self.sync()
        # y comparo:
        for campo in self.sqlmeta.columns:
            # print self.swap[campo], eval('self.%s' % campo) 
            #if self.swap[campo] != eval('self.%s' % campo): 
            if self.swap[campo] != getattr(self, campo): 
                raise SQLObjectChanged(self)

    def cerrar_cursor(self):
        self.cursor.close()

    def cerrar_conexion(self):
        self.conexion.close()
        if DEBUG: print " <-- Conexión cerrada."

    ## Código del hilo:
    def esperarNotificacion(self, nomnot, funcion=lambda: None):
        """
        Código del hilo que vigila la notificación.
        self -> Objeto al que pertenece el hilo.
        nomnot es el nombre de la notificación a esperar.
        funcion es una función opcional que será llamada cuando se
        produzca la notificación.
        """
        if DEBUG: print "Inicia ejecución hilo"
        while self != None and self.continuar_hilo:   # XXX
            if DEBUG: print "Entra en la espera bloqueante: %s" % nomnot
            self.abrir_cursor()
            self.cursor.execute("LISTEN %s;" % nomnot)
            self.conexion.commit()
            if select([self.cursor], [], [])!=([], [], []):
                if DEBUG: print "Notificación recibida"
                try:
                    self.comparar_swap()
                except SQLObjectChanged:
                    if DEBUG: print "Objeto cambiado"
                    funcion()
                except SQLObjectNotFound:
                    if DEBUG: print "Registro borrado"
                    funcion()
                # self.cerrar_cursor()
        else:
            if DEBUG: print "Hilo no se ejecuta"
        if DEBUG: print "Termina ejecución hilo"

    def chequear_cambios(self):
        try:
            self.comparar_swap()
            # print "NO CAMBIA"
        except SQLObjectChanged:
            # print "CAMBIA"
            if DEBUG: print "Objeto cambiado"
            # print self.notificador
            self.notificador.run()
        except SQLObjectNotFound:
            if DEBUG: print "Registro borrado"
            self.notificador.run()

    def ejecutar_hilo(self):
        ## ---- Código para los hilos:
        self.abrir_conexion()
        self.continuar_hilo = True
        nombre_clase = self.__oderivado
        self.th_espera = threading.Thread(target = self.esperarNotificacion, 
                    args = ("IPC_%s" % nombre_clase, self.notificador.run), 
                    name="Hilo-%s" % nombre_clase)
        self.th_espera.setDaemon(1)
        self.th_espera.start()

    def parar_hilo(self):
        self.continuar_hilo = False
        if DEBUG: print "Parando hilo..."
        self.cerrar_conexion()

    def destroy_en_cascada(self):
        """
        Destruye recursivamente los objetos que dependientes y 
        finalmente al objeto en sí.
        OJO: Es potencialmente peligroso y no ha sido probado en profundidad.
             Puede llegar a provocar un RuntimeError por alcanzar la 
             profundidad máxima de recursividad intentando eliminarse en 
             cascada a sí mismo por haber ciclos en la BD. 
        """
        for join in self.sqlmeta.joins:
            lista = join.joinMethodName
            for dependiente in getattr(self, lista):
                if dependiente is self:
                    continue
            # for dependiente in eval("self.%s" % (lista)):
                if DEBUG:
                    print "Eliminando %s..." % dependiente
                try:
                    dependiente.destroy_en_cascada()
                except RuntimeError: # maximum recursion depth exceeded in cmp
                    fremove = "remove%s" % self.__class__.__name__
                    if hasattr(dependiente, fremove):
                        func_fremove = getattr(dependiente, fremove)
                        func_fremove(self)
                    else:
                        setattr(dependiente, self.__class__.__name__, None)
                    dependiente.destroySelf()
        self.destroySelf()

    def copyto(self, obj, eliminar = False):
        """
        Copia en obj los datos del objeto actual que en obj sean 
        nulos.
        Enlaza también las relaciones uno a muchos para evitar 
        violaciones de claves ajenas, ya que antes de terminar, 
        si "eliminar" es True se borra el registro de la BD.
        PRECONDICIÓN: "obj" debe ser del mismo tipo que "self".
        POSTCONDICIÓN: si "eliminar", self debe quedar eliminado.
        """
        DEBUG = False
        assert type(obj) == type(self) and obj != None, "Los objetos deben pertenecer a la misma clase y no ser nulos."
        for nombre_col in self.sqlmeta.columns:
            valor = getattr(obj, nombre_col)
            if valor == None or (isinstance(valor, str) and valor.strip() == ""):
                if DEBUG:
                    print "Cambiando valor de columna %s en objeto destino." % (nombre_col)
                setattr(obj, nombre_col, getattr(self, nombre_col))
        for col in self._SO_joinList:
            atributo_lista = col.joinMethodName
            lista_muchos = getattr(self, atributo_lista)
            nombre_clave_ajena = repr(self.__class__).replace("'", ".").split(".")[-2] + "ID" # HACK (y de los feos)
            nombre_clave_ajena = nombre_clave_ajena[0].lower() + nombre_clave_ajena[1:]       # HACK (y de los feos)
            for propagado in lista_muchos:
                if DEBUG:
                    print "Cambiando valor de columna %s en objeto destino." % (nombre_clave_ajena)
                    print "   >>> Antes: ", getattr(propagado, nombre_clave_ajena)
                setattr(propagado, nombre_clave_ajena, obj.id)
                if DEBUG:
                    print "   >>> Después: ", getattr(propagado, nombre_clave_ajena)
        if eliminar:
            try:
                self.destroySelf()
            except:     # No debería. Pero aún así, me aseguro de que quede 
                        # eliminado (POSTCONDICIÓN).
                self.destroy_en_cascada()

    def clone(self, *args, **kw):
        """
        Crea y devuelve un objeto idéntico al actual.
        Si se pasa algún parámetro adicional se intentará enviar 
        tal cual al constructor de la clase ignorando los 
        valores del objeto actual para esos parámetros.
        """
        parametros = {}
        for campo in self.sqlmeta.columns:
            valor = getattr(self, campo)
            parametros[campo] = valor
        for campo in kw:
            valor = kw[campo]
            parametros[campo] = valor
        nuevo = self.__class__(**parametros)
        return nuevo

    # PLAN: Hacer un full_clone() que además de los atributos, clone también 
    # los registros relacionados.

    def get_info(self):
        """
        Devuelve información básica (str) acerca del objeto. Por ejemplo, 
        si es un pedido de venta, devolverá el número de pedido, fecha y 
        cliente.
        Este método se hereda por todas las clases y debería ser redefinido.
        """
        try:
            return "%s ID %d (PUID %s)"%(self.sqmeta.table, self.id, 
                                         self.get_puid())
        except AttributeError:
            try:
                return "%s ID %d (PUID %s)" % (self.sqlmeta.table, self.id, 
                                               self.get_puid())
            except:
                pass
        return "Información no disponible."

    def get_puid(self):
        """
        Devuelve un identificador único (¿único? I don't think so) para toda 
        la base de datos.
        Las clases pueden redefinir este método. Y de hecho deberían de acorde 
        a la lógica de negocio.
        """
        #pre = "".join([l for l in self.__class__.__name__ if l.isupper()])
        # Muncho mejore asina:
        pre = self.__class__.__name__
        id = self.id
        puid = "%s:%d" % (pre, id)
        return puid


def starter(objeto, *args, **kw):
    """
    Método que se ejecutará en el constructor de todas las 
    clases persistentes.
    Inicializa el hilo y la conexión secundaria para IPC, 
    así como llama al constructor de la clase padre SQLObject.
    """
    objeto.continuar_hilo = False
    objeto.notificador = notificacion.Notificacion(objeto)
    SQLObject._init(objeto, *args, **kw)
    PRPCTOO.__init__(objeto, objeto.sqlmeta.table)
    objeto.make_swap()    # Al crear el objeto hago la primera caché de datos, 
                          # por si acaso la ventana se demora mucho e intenta 
                          # compararla antes de crearla.

def actualizar_estado_cobro_de(clase):
    """
    Actualiza el estado de confirming o pagarés dependiendo de la fecha de 
    vencimiento y la del sistema. Por defecto marcará todo lo vencido como 
    cobrado.
    """
    for p in clase.select(clase.q.procesado == False):
        if datetime.date.today() >= p.fechaVencimiento:
            if DEBUG:
                print "Actualizando el estado de %s..." % p.get_puid(),
                try:
                    sys.stdout.flush()
                except AttributeError:
                    pass    # Consola de depuración o algo. No tiene flush.
            p.fechaCobrado = p.fechaVencimiento
            p.cobrado = p.cantidad
            p.procesado = True
            p.syncUpdate()
            try:
                cobros = p.cobros
            except AttributeError:
                cobros = p.pagos
            for c in cobros:
                c.fecha = p.fechaCobrado
                c.syncUpdate()
            if DEBUG:
                print "DONE."
                assert not p.pendiente

## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

class Almacen(SQLObject, PRPCTOO):
    albaranesSalidaServidos = MultipleJoin('AlbaranSalida', 
                                   joinColumn = "almacen_origen_id")
    albaranesSalidaRecibidos = MultipleJoin('AlbaranSalida', 
                                   joinColumn = "almacen_destino_id")
    stocksAlmacen = MultipleJoin("StockAlmacen")
    centrosTrabajo = MultipleJoin("CentroTrabajo")

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def _get_almacen_principal():
        ppal = Almacen.selectBy(principal = True)
        assert ppal.count() == 1
        ppal = ppal[0]
        return ppal

    def _get_almacen_principal_or_none():
        """
        Para casos muy concretos en los que no puedo permitir que una 
        excepción no tratada cuelgue la aplicación (por ejemplo, con el 
        default de AlbaranSalida. Si no hay almacén principal, no podría ni 
        llegar a cargar pclases para crearlo).
        """
        try:
            return Almacen.get_almacen_principal()
        except:
            return None
    
    def _get_almacen_principal_id_or_none():
        """
        Para casos muy concretos en los que no puedo permitir que una 
        excepción no tratada cuelgue la aplicación (por ejemplo, con el 
        default de AlbaranSalida. Si no hay almacén principal, no podría ni 
        llegar a cargar pclases para crearlo).
        """
        try:
            return Almacen.get_almacen_principal().id
        except:
            return None

    get_almacen_principal = staticmethod(_get_almacen_principal)
    get_almacen_principal_or_none = staticmethod(_get_almacen_principal_or_none)
    get_almacen_principal_id_or_none = staticmethod(_get_almacen_principal_id_or_none)

    def get_existencias(self, producto):
        """
        Devuelve las existencias actuales del producto en el almacén o 
        None si no hay registro que los relacione.
        """
        if isinstance(producto, ProductoCompra):
            try:
                sa = StockAlmacen.select(AND(
                        StockAlmacen.q.almacen == self.id, 
                        StockAlmacen.q.productoCompra == producto.id))[0]
            except IndexError:
                res = None
            else:
                sa.sync()
                res = sa.existencias
        else:
            #raise TypeException, "El parámetro debe ser un ProductoCompra."
            # Versión lenta. «premature optimization is the root of all evil»
            cantidades_en_almacen = [a.get_cantidad() for a in self.articulos 
                                    if a.productoVenta == producto]
            res = sum(cantidades_en_almacen)
        return res

    def set_existencias(self, producto, existencias):
        """
        Establece las existencias actuales del producto en el almacén.
        Crea un registro si fuera necesario.
        """
        if isinstance(producto, ProductoCompra):
            try:
                sa = StockAlmacen.select(AND(
                        StockAlmacen.q.almacen == self.id, 
                        StockAlmacen.q.productoCompra == producto.id))[0]
            except IndexError:
                sa = StockAlmacen(almacen = self.id, 
                                  productoCompra = producto, 
                                  existencias = existencias)
            sa.existencias = existencias
        else:
            raise TypeException, "El parámetro debe ser un ProductoCompra."


class CacheExistencias:
    def get_existencias(clase, producto, fecha, almacen):
        """
        Devuelve las existencias en bultos en la fecha dada y el almacén 
        especificado.
        Si no existe devuelve None.
        """
        rec = clase.get_registro(producto, fecha, almacen)
        if rec:
            return rec.bultos
        return None
        
    def get_stock(clase, producto, fecha, almacen):
        """
        Devuelve las existencias en las unidades del producto en la fecha dada 
        y el almacén especificado.
        Si no existe devuelve None.
        """
        rec = clase.get_registro(producto, fecha, almacen)
        if rec:
            return rec.cantidad
        return None
    
    def get_registro(clase, producto, fecha, almacen):
        """
        Devuelve el registro de caché relacionado con el producto en la fecha 
        dada y el almacén especificado.
        Si no existe devuelve None.
        """
        recs = clase.select(AND(clase.q.productoVenta == producto.id, 
                                clase.q.fecha == fecha, 
                                clase.q.almacen == almacen.id))
        if recs.count() == 1:
            return recs[0]
        elif recs.count > 1:
            # Error de coherencia. Más de un reg. de caché. Borro todos.
            for r in recs:
                r.destroySelf()
            return None
        else:   # recs.count() == 0
            return None
   
    def actualizar(clase, producto, bultos, cantidad, fecha, almacen):
        """
        Actualizar el registro de caché para el producto, fecha y almacén.
        Si existen varios elimina los que sobren. Si no existe lo crea. Y si 
        solo existe uno, lo actualiza y sincroniza.
        """
        cache = clase.select(AND(clase.q.productoVenta == producto.id, 
                                 clase.q.fecha == fecha, 
                                 clase.q.almacen == almacen.id))
        if cache.count() == 1:
            cache = cache[0]
        else:   # cache.count() > 1 or cache.count() == 0:
            for c in cache:
                c.destroySelf()
            cache = clase(productoVenta = producto, 
                          fecha = fecha, 
                          almacen = almacen, 
                          cantidad = 0, 
                          bultos = 0)
        cache.cantidad = cantidad
        cache.bultos = bultos
        cache.syncUpdate()

    get_existencias = classmethod(get_existencias)
    get_stock = classmethod(get_stock)
    get_registro = classmethod(get_registro)
    actualizar = classmethod(actualizar)


class FacturaCompra(SQLObject, PRPCTOO):
    lineasDeCompra = MultipleJoin('LineaDeCompra')
    vencimientosPago = MultipleJoin('VencimientoPago')
    pagos = MultipleJoin('Pago')
    serviciosTomados = MultipleJoin('ServicioTomado')
    documentos = MultipleJoin('Documento')

    codigos_no_validacion = {0: "Visto bueno automático correcto.", 
        1: "Existen líneas sin pedido.", 
        2: "Existen líneas sin albarán.", 
        3: "Los precios no coinciden.", 
        4: "La cantidad servida es superior a la solicitada.", 
        5: "Factura mixta de servicios y mercancía.", 
        6: "Servicios no se corresponden con transporte ni comisión.", 
        -1: "N/D", 
        7: "Cantidad tecleada por usuario no coincide con total de factura.", 
        8: "Más de un proveedor en albaranes y pedidos.", 
        9: "Proveedor de albaranes no coincide con el de pedidos.", 
        10: "Factura vacía."}

    codigos_no_validacion = staticmethod(codigos_no_validacion)

    def get_info(self):
        if self.proveedor:
            proveedor = self.proveedor.nombre
        else:
            proveedor = "sin proveedor"
        if self.bloqueado:
            bloqueado = "bloqueada"
        else:
            bloqueado = "no bloqueada"
        return "Factura %s (%s) de %s. %s." % (self.numfactura, 
                                                   utils.str_fecha(self.fecha), 
                                                   proveedor, 
                                                   bloqueado.title())

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    bloqueado = property(lambda self: self.bloqueada, lambda self, valor: setattr(self, "bloqueada", valor))

    def calcular_importe_total(self):
        """
        Calcula y devuelve el importe total, incluyendo IVA, de la factura.
        """
        total = 0
        for ldc in self.lineasDeCompra:
            total += ldc.get_subtotal(iva = False)
        for s in self.serviciosTomados:
            total += s.get_subtotal(iva = False)
        total *= (1 - self.descuento)
        total += float(self.cargo)
        #total = round(total, 2)         # Por ley la base imponible debe llevar 2 decimales y el IVA es el x% de la 
                                        # B.I., también con 2 decimales.
        # La ley dirá lo que quiera, pero menudos dolores de cabeza me está dando.
        #print "Con redondeo: %s. Sin redondeo: %s" % (utils.float2str(total + self.importeIva, 2), 
        #                                              utils.float2str(round(total, 2) + self.importeIva))
        total += self.importeIva        # Este método ya tiene en cuenta los distintos tipos de IVA, por línea, etc.
        return total

    def calcular_importe_iva(self):
        """
        Calcula el importe del IVA de la factura a partir de 
        las LDC y servicios de la misma.
        Antes de devolverlo comprueba si todas las LDC y 
        servicios tienen el mismo IVA y coinciden con el 
        de la factura. En ese caso lanza una excepción si 
        el importe calculado a partir de las LDC y servicios 
        no es igual al subtotal de la factura por su propio IVA.
        Si el IVA de la factura tampoco coincide con el de las 
        líneas de compra, se añade al IVA total (para el caso, 
        por ejemplo, de las facturas con 16 + 4% por régimen de 
        equivalencia).
        """
        totiva = 0.0
        #subtotal = self.cargo  # El cargo no entra en el IVA
        subtotal = 0.0
        ivas = []
        for ldc in self.lineasDeCompra + self.serviciosTomados:
            subtotalldc = ldc.get_subtotal(iva = False)
            totiva += subtotalldc * ldc.iva
            subtotal += subtotalldc
            if ldc.iva not in ivas:
                ivas.append(ldc.iva)
        #subtotal = round(subtotal, 2)   # Por ley la B.I. debe llevar 2 decimales y el IVA se calcula en base a ello.
        if len(ivas) == 1: 
            if self.iva == ivas[0]:
                try:
                    msg = "El IVA total de la factura de compra %d no coincide con el IVA de sus líneas de venta USANDO ÚNICAMENTE 2 DÍGITOS DE PRECISIÓN: %s != %s." % (self.id, subtotal * self.iva, totiva)
                    assert round(subtotal * self.iva, 2) == round(totiva, 2), msg ## Este es el assert que usaba hasta ahora, pero da más problemas que soluciones el propagarlo y capturarlo fuera.
                except AssertionError, msg:
                    print msg
                # assert subtotal * self.iva == totiva, "El IVA total de la factura de compra %d no coincide con el IVA de sus líneas de venta: %s != %s." % (self.id, subtotal * self.iva, totiva)
            else:
                totiva += subtotal * self.iva
        totiva = round(totiva, 2)       # Al igual que la base imponible, el total de IVA se redondea a 2 decimales.
        return totiva

    importeIva = property(calcular_importe_iva, doc = calcular_importe_iva.__doc__)
    importeTotal = property(calcular_importe_total, doc = calcular_importe_total.__doc__)

    def iva_es_correcto(self):
        """
        Devuelve True sii el IVA de la factura y el IVA de las 
        LDCs y servicios es el mismo.
        Si el IVA de todas las líneas es el mismo pero difiere del 
        de la factura, cambia este último por el iva de las LDC.
        """
        ivas = []
        res = True
        for linea in self.lineasDeCompra + self.serviciosTomados:
            linea_iva = linea.iva
            if linea_iva not in ivas:
                ivas.append(linea_iva)
            if self.iva != linea_iva:
                res = False
        if len(ivas) == 1:
            self.iva = ivas[0]
            self.syncUpdate()
            res = True
        return res
    
    def iva_homogeneo(self):
        """
        Devuelve True sii el IVA de todas las LDC y servicios 
        de la factura es el mismo (o no tiene).
        """
        ivas = []
        for linea in self.lineasDeCompra + self.serviciosTomados:
            linea_iva = linea.iva
            if linea_iva not in ivas:
                ivas.append(linea_iva)
        return len(ivas) <= 1

    def generar_numero_control(self):
        """
        Devuelve una cadena con un número de control de 6 
        cifras relacionado unívocamente con la factura.
        """
        res = None
        if self.proveedorID and self.vistoBuenoComercial and self.vistoBuenoDirector:
            from hashlib import md5
            m = md5(self.numfactura+self.proveedor.nombre)  # OJO: NUNCA NUNCA se debe cambiar el nombre del proveedor una 
                                                                # vez tenga algo facturado y con visto bueno.
            digest = m.hexdigest()   
            res = digest[::6].upper() # Vale. No parece muy buena. Pero de una muestra aleatoria de 1 millón de cadenas, 
                                      # tan solo se han producido un 0.0038990426457789383 % de colisiones. No puedo hacer más si 
                                      # uno de los requisitos del cliente es que tenga exactamente 6 dígitos.
        return res

    numeroControl = property(generar_numero_control, 
                             doc = "Número de control unívoco para la factura."
                                   " Vale None si la factura de compra no es"
                                   " válida.")

    def get_codigo_validacion_visto_bueno(self):
        """
        Devuelve el código de validación del visto bueno
        en lugar de solamente True o False.
        Para obtener el visto bueno debe cumplir que:
        1.- Todas las líneas que contiene pertenecen a un pedido.
        2.- Todas esas mismas líneas pertenecen también a un albarán.
        3.- Los precios de las líneas de compra son iguales a los de las líneas de pedido. Si hay 
            varios, la cantidad servida a cada precio debe ser inferior o igual a la cantidad 
            pedida del mismo producto a cada precio.
        4.- La cantidad recibida en los albaranes es igual o inferior a la cantidad solicitada
            en el pedido.
        O BIEN (NEW! 24/01/07):
        1.- Solo contiene líneas de servicio.
        2.- Las líneas de servicio tienen un transporte o una comisión.
        """
        code = None
        if self.serviciosTomados and not self.lineasDeCompra:
            vto = len(self.serviciosTomados) == len([s for s in self.serviciosTomados if #s.comision or s.transporteACuenta])
        s.transporteACuenta])
            if not vto:
                code = 6
        else:
            vto = len(self.lineasDeCompra) > 0
            if not vto:
                code = 10 
            else:
                vto = vto and self.vistoBuenoUsuario    # Comenzamos con el chequeo del visto bueno del total del usuario.
                if not vto:
                    code = 7
            productos = {}
            pedidos = []
            proveedores_de_pedidos = []
            proveedores_de_albaranes = []
            if self.serviciosTomados:
                vto = False     # TODO: Si los servicios -mezclados con compras en esta factura- provienen de una factura de venta por 
                                # ser comisión... ¿habría que chequearlo también?.
                code = 5
            for ldc in self.lineasDeCompra:
                vto = vto \
                and ldc.pedidoCompraID != None \
                and ldc.albaranEntradaID != None #\
                # and ldc.pedidoCompra.get_menor_precio(ldc.productoCompra) == ldc.precio 
                if not vto:
                    if ldc.pedidoCompra == None:
                        code = 1
                    elif ldc.albaranEntrada == None:
                        code = 2
                    break
                if ldc.productoCompra not in productos:
                    productos[ldc.productoCompra] = {'pedida': 0, 
                                                     'servida': ldc.cantidad, 
                                                     'precios_servido': {ldc.precioConDescuento: ldc.cantidad},  # Precios a los que fueron 
                                             # servidos los productos y cantidad servida total de cada uno de esos precios para ese producto.
                                                     'precios_pedido': {ldc.precioConDescuento: 0}
                                                    }
                else:
                    productos[ldc.productoCompra]['servida'] += ldc.cantidad
                    if ldc.precioConDescuento not in productos[ldc.productoCompra]['precios_servido']:
                        productos[ldc.productoCompra]['precios_servido'][ldc.precioConDescuento] = ldc.cantidad
                    else:
                        productos[ldc.productoCompra]['precios_servido'][ldc.precioConDescuento] += ldc.cantidad
                if ldc.pedidoCompra not in pedidos:
                    pedidos.append(ldc.pedidoCompra)
            if vto:
                for pedido in pedidos:
                    # Se ignora si el pedido está cerrado o no porque la diferencia entre un pedido 
                    # no cerrado y uno cerrado es que la cantidad pedida sería mayor, lo cual no 
                    # afecta al criterio de visto bueno.
                    if pedido.proveedor not in proveedores_de_pedidos:
                        proveedores_de_pedidos.append(pedido.proveedor)
                    for ldpc in pedido.lineasDePedidoDeCompra:
                        if ldpc.productoCompra not in productos:
                            productos[ldpc.productoCompra] = {'pedida': ldpc.cantidad, 
                                                              'servida': 0, 
                                                              'precios_pedido': {ldpc.precioConDescuento: ldpc.cantidad}, 
                                                              'precios_servido': {ldpc.precioConDescuento: 0}}
                        else:
                            productos[ldpc.productoCompra]['pedida'] += ldpc.cantidad
                            if ldpc.precioConDescuento not in productos[ldpc.productoCompra]['precios_pedido']:
                                productos[ldpc.productoCompra]['precios_pedido'][ldpc.precioConDescuento] = ldpc.cantidad
                            else:
                                productos[ldpc.productoCompra]['precios_pedido'][ldpc.precioConDescuento] += ldpc.cantidad
                for producto in productos:
                    vto = vto and productos[producto]['servida'] <= productos[producto]['pedida']
                    if not vto:
                        code = 4
                        break
                    for precio in productos[producto]['precios_servido']:
                        try:
                            vto = vto and productos[producto]['precios_servido'][precio] <= productos[producto]['precios_pedido'][precio]
                            if not vto:
                                code = 3
                        except KeyError:    # Si no está el precio que sea en el diccionario, directamente no doy visto bueno.
                            vto = False
                            code = 3
            # DONE: Quedaría una comprobación adicional: El proveedor del albarán debe ser el mismo que el del pedido.
            if vto:
                for ldc in self.lineasDeCompra:
                    if ldc.albaranEntrada.proveedor not in proveedores_de_albaranes:
                        proveedores_de_albaranes.append(ldc.albaranEntrada.proveedor)
                vto = vto and (len(proveedores_de_albaranes) == len(proveedores_de_pedidos) == 1)
                if not vto:
                    code = 8
                vto = vto and (self.proveedor == proveedores_de_pedidos[0] == proveedores_de_albaranes[0])
                if not vto:
                    code = 9
        if not vto: 
            if not code:
                code = -1
        else:
            code = 0
        return code

    def get_visto_bueno_automatico(self):
        """
        Devuelve True si la factura obtiene el visto bueno 
        automático.
        (Ver documentación de get_codigo_validacion_visto_bueno 
        para las condiciones de visto bueno automático.)
        """
        return self.get_codigo_validacion_visto_bueno() == 0

    def get_visto_bueno_pago(self):
        """
        Devuelve True si la factura tiene el visto bueno para 
        el pago. Se consigue si:
        Tiene el visto bueno automático (incluye la confirmación del total por el usuario).
        O bien si tiene el visto bueno del director comercial, técnico y gerente.
        """
        return (self.vistoBuenoComercial and self.vistoBuenoDirector) or (self.vistoBuenoAutomatico)

    vistoBuenoAutomatico = property(get_visto_bueno_automatico, doc = get_visto_bueno_automatico.__doc__)
    vistoBuenoPago = property(get_visto_bueno_pago, doc = get_visto_bueno_pago.__doc__)

    def emparejar_vencimientos(self):
        """
        Devuelve un diccionario con los vencimientos y cobros de la factura 
        emparejados.
        El diccionario es de la forma:
        {vencimiento1: [cobro1], 
         vencimiento2: [cobro2], 
         vencimiento3: [], 
         'vtos': [vencimiento1, vencimiento2, vencimiento3...], 
         'cbrs': [cobro1, cobro2]}
        Si tuviese más cobros que vencimientos, entonces se devolvería un diccionario tal que:
        {vencimiento1: [cobro1], 
         vencimiento2: [cobro2],
         None: [cobro3, cobro4...], 
         'vtos': [vencimiento1, vencimiento2], 
         'cbrs': [cobro1, cobro2, cobro3, cobro4...]}
        'vtos' y 'cbrs' son copias ordenadas de las listas de vencimientos y cobros.
        El algoritmo para hacerlo es:
        1.- Construyo el diccionario con todos los vencimientos.
        2.- Construyo una lista auxiliar con los cobros ordenados por fecha.
        3.- Recorro el diccionario de vencimientos por orden de fecha.
            3.1.- Saco y asigno el primer cobro de la lista al vencimiento tratado en la iteración.
            3.2.- Si no quedan vencimientos por asignar, creo una clave None y agrego los cobros restantes.
        """
        res = {}
        cbrs = self.pagos[:]
        cbrs.sort(utils.cmp_fecha_id)
        vtos = self.vencimientosPago[:]
        vtos.sort(utils.cmp_fecha_id)
        res['vtos'] = vtos[:]
        res['cbrs'] = cbrs[:]
        for vto in vtos:
            try:
                cbr = cbrs.pop()
            except IndexError:
                res[vto] = []
            else:
                res[vto] = [cbr]
        if cbrs != []:
            res[None] = cbrs
        return res

    def get_importe_primer_vencimiento_pendiente(self):
        """
        Devuelve el importe del primer vencimiento pendiente de pagar 
        de la factura o 0 si no quedan.
        """
        res = 0.0
        pares = self.emparejar_vencimientos()
        for vto in pares['vtos']:       # pares['vtos'] está ordenado por fecha
            if pares[vto] == []:
                res = vto.importe
                break
        return res

    def anular_vistos_buenos(self):
        """
        Anula los vistos buenos de la factura.
        (Útil por ejemplo para cuando se modifica el 
        contenido de una factura después de haber 
        obtenido el visto bueno).
        """
        self.vistoBuenoComercial = self.vistoBuenoDirector = self.vistoBuenoUsuario = False
        self.fechaVistoBuenoUsuario = self.fechaVistoBuenoDirector = self.fechaVistoBuenoTecnico = self.fechaVistoBuenoComercial = None
        self.syncUpdate()


class LineaDeCompra(SQLObject, PRPCTOO):
    lineasDePedidoDeCompra = RelatedJoin('LineaDePedidoDeCompra', 
                joinColumn='linea_de_compra_id', 
                otherColumn='linea_de_pedido_de_compra_id', 
                intermediateTable='linea_de_pedido_de_compra__linea_de_compra')

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_fecha_albaran(self):
        """
        Devuelve la fecha del albarán al que pertenece la línea de compra
        o None si no tiene.
        """
        if self.albaranEntradaID != None:
            fecha = self.albaranEntrada.fecha
        else:
            fecha = None
        return fecha

    def get_precio_con_descuento(self):
        """
        Precio total de la línea incluyendo descuento, pero sin incluir el IVA.
        """
        return self.precio * (1 - self.descuento)

    precioConDescuento = property(get_precio_con_descuento, doc = get_precio_con_descuento.__doc__)

    def get_proveedor(self):
        return self.albaranEntrada and self.albaranEntrada.proveedor or None
        
    def get_nombre_proveedor(self):
        proveedor = self.get_proveedor() 
        return proveedor and proveedor.nombre or ""

    def get_descripcion_productoCompra(self):
        return self.productoCompra and self.productoCompra.descripcion or ""

    proveedor = property(get_proveedor, doc = "Objeto proveedor del albarán de la línea de compra o None si no tiene.")
    nombre_proveedor = property(get_nombre_proveedor, 
                                doc = 'Nombre del proveedor de la línea de compra del albarán o "" si no tiene.')
    descripcion_productoCompra = property(get_descripcion_productoCompra, 
                                          doc = 'Descripción del producto de compra de la LDC o "" si no tiene.')

    def es_igual_salvo_cantidad(self, ldp):
        """
        Compara la LDP con otra recibida. Devuelve True si los valores 
        son iguales para los campos:
          - pedidoCompraID
          - albaranEntradaID
          - facturaCompraID
          - productoCompraID
          - precio
          - descuento
          - entrega
          - siloID
          - cargaSiloID 
        """
        campos = ("pedidoCompraID", 
                  "albaranEntradaID", 
                  "facturaCompraID", 
                  "productoCompraID", 
                  "precio", 
                  "descuento", 
                  "entrega", 
                  )
        for campo in campos:
            if getattr(self, campo) != getattr(ldp, campo):
                return False
        return True

    def get_subtotal(self, iva = False):
        """
        Devuelve el subtotal con o sin IVA (según se indique) de 
        la línea de compra: precio * cantidad - descuento.
        NOTA: No se aplica redondeo en el subtotal antes de aplicar el 
        IVA. Me permito trabajar con varios decimales en el contenido 
        de la factura, pero a partir del subtotal neto de la factura 
        completa solo se permite trabajar con céntimos de euro como 
        fracción máxima (ver aeat.es).
        """
        res = self.cantidad * self.precio * (1 - self.descuento)
        if iva:
            res *= 1 + self.iva
        # Las líneas ya tienen IVA propio, no se usa más el IVA del pedido.
        # if iva and self.pedidoCompraID: 
        #    res *= (1 + self.pedidoCompra.iva)
        return res


class VencimientoPago(SQLObject, PRPCTOO):

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def calcular_importe_pdte(self):
        """
        Devuelve el importe total o parcial del vencimiento que está 
        pendiente de pago.
        El algoritmo que usa es:
            1.- Ordena los vtos. por fecha de manera que si queda algo 
                pendiente siempre sea en los últimos vencimientos.
            2.- Suma el importe total pagado de la factura.
            3.- Anula los vencimientos por orden de fecha con los pagos 
                realizados hasta completar todos o agotar la cantidad pagada.
        OJO: O(n) en el peor caso.
        """
        fra = self.facturaCompra
        cant_pagada = abs(sum([p.importe for p in fra.pagos]))
        vencimientos_pendientes = fra.vencimientosPago[:]
        vencimientos_pendientes.sort(utils.cmp_fecha_id)
        while cant_pagada > 0 and vencimientos_pendientes:
            v = vencimientos_pendientes.pop(0)
            if cant_pagada < abs(v.importe):
                # Si no cubre al vencimiento lo devuelvo a la lista de pdtes.
                vencimientos_pendientes.insert(0, v)
            cant_pagada -= v.importe
        if self in vencimientos_pendientes:
            if self == vencimientos_pendientes[0] and cant_pagada < 0:
                res = -cant_pagada
            else:   # No es el primer vencimiento (único sospechoso de estar 
                    # pagado parcialmente sólo) o los pagos y vencimientos han 
                    # cuadrado hasta donde han llegado (cant_pagada == 0).
                res = self.importe
        else:
            res = 0.0
        return res


class Pago(SQLObject, PRPCTOO):

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_concepto(self):
        """
        Devuelve el número de factura o el nombre de la cuenta 
        LOGIC, dependiendo de a qué esté asociado el pago.
        """
        concepto = "-"
        if self.facturaCompra != None:
            concepto = "Factura %s" % (self.facturaCompra.numfactura)
        elif self.logicMovimientos != None:
            concepto  = "Cuenta LOGIC %s: %s" % (self.logicMovimientos.cuenta, self.logicMovimientos.comentario)
        return concepto
    
    concepto = property(get_concepto, doc = "Factura o cuenta LOGIC relacionada con el pago.") 

    def es_transferencia(self):
        """
        Devuelve True si el pago se puede considerar una transferencia.
        Se considera una transferencia si cuentaOrigen o cuentaDestino 
        no son None. Al menos una de las dos debe estar instanciada.
        """
        return self.cuentaOrigen != None or self.cuentaDestino != None


class VencimientoCobro(SQLObject, PRPCTOO):

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_factura_o_prefactura(self):
        """
        Devuelve la factura relacionada, tanto si es facturaVenta
        como prefactura, o None si no tiene ninguna de ellas.
        Como no debería tener ambos valores distintos de nulo a 
        la vez, tiene preferencia facturaVenta sobre prefactura.
        """
        return self.facturaVenta or self.prefactura

    def get_formadepago(self):
        """
        Devuelve la forma de pago del vencimiento. 
        Está almacenado en el atributo «observaciones» "for historical 
        reasons". Pero previendo que esto cambiará me hago un método para 
        que la transición sea después más su-su-suave.
        """
        return self.observaciones and self.observaciones.upper().strip() or ""


class PagarePago(SQLObject, PRPCTOO):
    pagos = MultipleJoin('Pago')
    # fechaCobro = ... default=None.     NOTA: No lo pilla por defecto de la 
    #   BD. En la creación de objetos en las ventanas habrá que decirle 
    # explícitamente que será None.    
    documentos = MultipleJoin('Documento')

    # Por compatibilidad con Pagarés de cobro y confirmings. (Por menos que 
    # esto he hecho superclases. Esta vez tengo prisa. Pero que sepas que 
    # deberías tener un class DocumentoPago del que heredar).
    def set_fechaPago(self, fecha):
        self.fechaPago = fecha
    fechaVencimiento = property(lambda self: self.fechaPago, set_fechaPago)
    def set_fechaCobrado(self, fecha):
        self.fechaCobrado = fecha
    fechaPagado = property(lambda self: self.fechaCobrado, set_fechaCobrado)

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)
    
    def esta_pendiente(self):
        return self.cantidad > self.pagado
    
    def get_cantidad_pendiente(self):
        return self.cantidad - self.pagado
    
    def set_cantidad_pendiente(self, pendiente):
        """
        Modifica la cantidad cobrada para que quede como pendiente
        la cantidad recibida.
        """
        self.pagado = self.cantidad - pendiente

    pendiente = property(esta_pendiente, doc = "Valor booleano que devuelve si el pagaré está completamente pagado (False) o no -tiene algo o todo pendiente de pagar (True)-.")
    cantidad_pendiente = property(get_cantidad_pendiente, set_cantidad_pendiente, doc = "Cantidad pendiente de pagar del total del pagaré")

    def actualizar_estado_cobro(clase):
        """
        Marca por defecto como cobrados todos los pagarés vencidos, pero 
        respetando aquellos que ya se marcaron manualmente como pendientes.
        """
        actualizar_estado_cobro_de(clase) 
    
    actualizar_estado_cobro = classmethod(actualizar_estado_cobro)


class Cobro(SQLObject, PRPCTOO):
    
    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_factura_o_prefactura(self):
        """
        Devuelve la factura relacionada, tanto si es facturaVenta
        como prefactura, o None si no tiene ninguna de ellas.
        Como no debería tener ambos valores distintos de nulo a 
        la vez, tiene preferencia facturaVenta sobre prefactura.
        """
        return self.facturaVenta or self.prefactura

    def get_numfactura(self):
        """
        Devuelve el número de la factura de venta relacionada con el cobro 
        actual.
        Devuelve la cadena vacía si no tiene relación con 
        ninguna de las dos cosas.
        """
        if self.facturaVentaID != None:
            return self.facturaVenta.numfactura
        return ""

    def get_cliente(self):
        """
        Devuelve el objeto cliente relacionado con el cobro 
        o None si no se encontró.
        """
        if self.facturaVentaID != None:
            return self.facturaVenta.cliente
        if self.prefacturaID != None:
            return self.prefactura.cliente
        return None

    def set_cliente(self, cliente):
        """
        Hace que el cliente de la factura de venta 
        relacionada con el cobro tengan como
        cliente el objeto cliente recibido.
        """
        if self.facturaVentaID != None:
            self.facturaVenta.cliente = cliente
        if self.prefacturaID != None:
            self.prefactura.cliente = cliente

    cliente = property(get_cliente, set_cliente, 
                       doc = "Cliente relacionado con el cobro.")
    numfactura = property(get_numfactura, doc = get_numfactura.__doc__)

    def esta_cobrado(self, fecha_base = None, gato_en_talega = False):
        """
        Devuelve True si el cobro está realmente pagado en la fecha indicada 
        (o en cualquier fecha, si no se especifica), esto es:
            - Si es una transferencia.
            - Si es en efectivo. 
            - Si es un cheque.
            - Si es un confirming.
            - Si es un pagaré no vencido.
            - Si es un pagaré no pendiente.
        Pero si gato_en_talega es True solo cuento que un cobro está cobrado 
        cuando el gato está en la talega. Gatus in talegui. Esto es, cuando 
        el ninerito lo tengo yo ya, aunque sea un confirming del mismísimo 
        Emilio Botín, o está confirmado por el usuario que ya no está 
        pendiente o no lo cuento como cobro. 
        """
        cobrado = 0.0
        if not self.confirmingID and not self.pagareCobroID:
            # Cualquier otro cobro que no implique futuribles, está cobrado 
            # desde el momento en que se introduce en el sistema.
            if not fecha_base or fecha_base >= self.fecha:
                cobrado += self.importe 
        elif self.pagareCobro:
            compromiso_cobro = self.pagareCobro
            compromiso_cobro.sync()
            if not fecha_base:
                if not compromiso_cobro.pendiente:
                    cobrado += compromiso_cobro.cantidad
                else:
                    if not gato_en_talega:
                        # Además de no estar pendiente(arriba), lo considero 
                        # cobrado si no ha vencido aún aunque esté pendiente.
                        if (compromiso_cobro.fechaVencimiento 
                            > datetime.datetime.now()):
                            cobrado += compromiso_cobro.cantidad
            else:
                if (compromiso_cobro.fechaCobrado 
                    and fecha_base >= compromiso_cobro.fechaCobrado
                    and compromiso_cobro.cobrado >= compromiso_cobro.cantidad):
                    cobrado += compromiso_cobro.cantidad
                else:
                    if not gato_en_talega:
                        # Cobrado si no ha vencido en fecha base y ya existía.
                        if (compromiso_cobro.fechaVencimiento < fecha_base and 
                            compromiso_cobro.fechaRecepcion >= fecha_base):
                            cobrado += compromiso_cobro.cantidad
        elif self.confirming:
            compromiso_cobro = self.confirming
            compromiso_cobro.sync()
            if not fecha_base:
                if not compromiso_cobro.pendiente:
                    cobrado += compromiso_cobro.cantidad
                else:
                    if not gato_en_talega:
                        # Además de no estar pendiente(arriba), lo considero 
                        # cobrado siempre porque si no responde el cliente, 
                        # responde el banco, por lo que el cobro lo tengo 
                        # asegurado como proveedor.
                        cobrado += compromiso_cobro.cantidad
            else:
                if (compromiso_cobro.fechaCobrado 
                    and fecha_base >= compromiso_cobro.fechaCobrado
                    and compromiso_cobro.cobrado >= compromiso_cobro.cantidad):
                    cobrado += compromiso_cobro.cantidad
                else:
                    if not gato_en_talega:
                        # Cobrado si ya existía.
                        if compromiso_cobro.fechaRecepcion >= fecha_base:
                            cobrado += compromiso_cobro.cantidad
        return cobrado  # 0.0 es False.

    def get_vencimiento(self):
        """
        Devuelve el vencimiento que corresponde al cobro o None.
        """
        res = None
        f = self.get_factura_o_prefactura()
        if f:
            dic_cobros_y_vtos = f.emparejar_vencimientos()
            for vto in dic_cobros_y_vtos.keys():
                if not isinstance(vto, VencimientoCobro):
                    continue    # Es la lista de cobros y vencimientos, no la 
                                # de los cobros agrupados por vencimiento.
                                # Ver "emparejar_vencimientos".
                if self in dic_cobros_y_vtos[vto]:
                    res = vto
                    break
        return res

    def get_formadepago(self):
        """
        Devuelve la forma de pago del vencimiento al que corresponde el cobro. 
        Si no encuentra el vencimiento, devuelve la forma de cobro por 
        defecto del cliente.
        La forma de pago es un string. Si no se encuentra en la factura, 
        vencimiento o cliente, devuelve la cadena vacía.
        """
        try:
            res = self.get_vencimiento().observaciones
        except AttributeError:
            res = self.cliente and self.cliente.formadepago or ""
        try:
            res = res.upper().strip()
        except AttributeError:  # De algún lado ha venido un None o algo peor.
            res = ""
        return res

class PagareCobro(SQLObject, PRPCTOO):
    cobros = MultipleJoin('Cobro')
    # fechaCobro = ... default=None.     NOTA: No lo pilla por defecto de la BD. En la creación de objetos en las 
    #                                    ventanas habrá que decirle explícitamente que será None.    
    documentos = MultipleJoin('Documento')

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_puid(self):
        """
        Devuelve un identificador único, etcétera, etcétera
        """
        return "%s:%d" % ("PAGC", self.id)

    def esta_pendiente(self):
        return self.cantidad > self.cobrado
    
    def get_cantidad_pendiente(self):
        return self.cantidad - self.cobrado
    
    def set_cantidad_pendiente(self, pendiente):
        """
        Modifica la cantidad cobrada para que quede como pendiente
        la cantidad recibida.
        """
        self.cobrado = self.cantidad - pendiente

    def get_cliente(self):
        """
        Devuelve el objeto cliente relacionado con el pagaré a través de 
        "cobros". Si no tiene, devuelve None.
        """
        res = None
        if len(self.cobros) > 0:
            res = self.cobros[0].cliente
        return res

    def get_fechaCobro(self):
        return self.fechaCobro
    
    def set_fechaCobro(self, fecha):
        self.fechaCobro = fecha
        self.syncUpdate()

    pendiente = property(esta_pendiente, doc = "Valor booleano que devuelve si el pagaré está completamente pagado (False) o no -tiene algo o todo pendiente de cobrar (True)-.")
    cantidad_pendiente = property(get_cantidad_pendiente, set_cantidad_pendiente, doc = "Cantidad pendiente de cobrar del total del pagaré")
    cliente = property(get_cliente, doc = "Devuelve el objeto Cliente relacionado con el pagaré.")
    fechaVencimiento = property(get_fechaCobro, set_fechaCobro) # Por si 
    # alguien se lía con el nombre, que no queda muy claro a qué se refiere.

    def actualizar_estado_cobro(clase):
        """
        Marca por defecto como cobrados todos los pagarés vencidos, pero 
        respetando aquellos que ya se marcaron manualmente como pendientes.
        """
        actualizar_estado_cobro_de(clase) 
    
    actualizar_estado_cobro = classmethod(actualizar_estado_cobro)

class Confirming(SQLObject, PRPCTOO):
    cobros = MultipleJoin('Cobro')
    documentos = MultipleJoin('Documento')

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)
    
    def esta_pendiente(self, fecha_base = datetime.date.today()):
        """
        Devuelve True si el confirming ya se ha cobrado completamente.
        OJO: Un confirming está cobrado si la cantidad de cobro no es menor 
        al importe o si la fecha «fecha_base» (generalmente la actual del 
        sistema) es superior a la fecha de vencimiento.
        OJO: Si la fecha de comprobación «fecha_base» es la del sistema, 
        actualizará la cantidad cobrada para ajustarla al importe si además 
        es superior a la de vencimiento (fecha_cobro).
        """
        if fecha_base == datetime.date.today() and fecha_base >= self.fechaCobro:
            self.cobrado = self.cantidad
            self.syncUpdate()
        res = self.cobrado < self.cantidad #or fecha_base < self.fechaCobro 
            # Si se adelanta el confirming, ya no está pendiente.
        return res
    
    def get_cantidad_pendiente(self):
        return self.cantidad - self.cobrado
    
    def set_cantidad_pendiente(self, pendiente):
        """
        Modifica la cantidad cobrada para que quede como pendiente
        la cantidad recibida.
        """
        self.cobrado = self.cantidad - pendiente

    def get_cliente(self):
        """
        Devuelve el objeto cliente relacionado con el pagaré a través de 
        "cobros". Si no tiene, devuelve None.
        """
        res = None
        if len(self.cobros) > 0:
            res = self.cobros[0].cliente
        return res

    def get_fechaCobro(self):
        return self.fechaCobro
    
    def set_fechaCobro(self, fecha):
        self.fechaCobro = fecha
        self.syncUpdate()

    pendiente = property(esta_pendiente, doc = "Valor booleano que devuelve si el pagaré está completamente pagado (False) o no -tiene algo o todo pendiente de cobrar (True)-.")
    cantidad_pendiente = property(get_cantidad_pendiente, set_cantidad_pendiente, doc = "Cantidad pendiente de cobrar del total del pagaré")
    cliente = property(get_cliente, doc = "Devuelve el objeto Cliente relacionado con el pagaré.")
    fechaVencimiento = property(get_fechaCobro, set_fechaCobro) # Por si 
    # alguien se lía con el nombre, que no queda muy claro a qué se refiere.
    
    def actualizar_estado_cobro(clase):
        """
        Marca por defecto como cobrados todos los pagarés vencidos, pero 
        respetando aquellos que ya se marcaron manualmente como pendientes.
        """
        actualizar_estado_cobro_de(clase) 
    
    actualizar_estado_cobro = classmethod(actualizar_estado_cobro)

class TipoDeMaterial(SQLObject, PRPCTOO):
    productosCompra = MultipleJoin('ProductoCompra')
    
    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

class CuentaDestino(SQLObject, PRPCTOO):
    pagos = MultipleJoin('Pago')

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_info(self):
        return ", ".join((self.nombre, self.banco, self.swif, self.iban, self.cuenta, self.nombreBanco, self.proveedor and self.proveedor.nombre or ""))

class CuentaOrigen(SQLObject, PRPCTOO):
    pagos = MultipleJoin('Pago')
    vencimientosCobro = MultipleJoin('VencimientoCobro')
    clientes = MultipleJoin('Cliente')
    recibos = MultipleJoin('Recibo')

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_info(self):
        return ", ".join((self.nombre, self.banco, self.ccc, self.observaciones))

class Proveedor(SQLObject, PRPCTOO):
    pedidosCompra = MultipleJoin('PedidoCompra')
    albaranesEntrada = MultipleJoin('AlbaranEntrada')
    facturasCompra = MultipleJoin('FacturaCompra')
    pagos = MultipleJoin('Pago')
    transportesACuenta = MultipleJoin('TransporteACuenta')
    clientes = MultipleJoin('Cliente')
    cuentasDestino = MultipleJoin('CuentaDestino')
    documentos = MultipleJoin('Documento')

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def es_extranjero(self):
        """
        Devuelve True si el proveedor es extranjero.
        Para ello mira si el país del proveedor es diferente al 
        de la empresa. Si no se encuentran datos de la empresa
        devuelve True si el país no es España.
        """
        cpf = unicode(self.paisfacturacion.strip())
        try:
            de = DatosDeLaEmpresa.select()[0]
            depf = unicode(de.paisfacturacion.strip())
            res = cpf != "" and depf.lower() != cpf.lower()
        except IndexError:
            res = cpf != "" and cpf.lower() != unicode("españa")
        return res

    extranjero = property(es_extranjero)
    
    def get_texto_forma_pago(self):
        """
        Devuelve un texto que representa la forma de pago del proveedor. 
        Por ejemplo:  efectivo, pagaré 90 D.F.F., transferencia banco 1234-23-...
        """
        formapago = ""
        if self.documentodepago != None and self.documentodepago.strip() != "" and self.documentodepago.strip() != "0":
            formapago = "%s, " % (self.documentodepago)
        if self.cuenta != None and self.cuenta.strip() != "" and "ferenc" in self.documentodepago.lower():
            formapago += "(%s) " % (self.cuenta)
        if self.vencimiento != None and self.vencimiento.strip() != "" and self.vencimiento.strip() != "0":
            formapago += "%s " % (self.vencimiento)
        if self.diadepago != None and self.diadepago.strip() != "" and self.diadepago.strip() != "-":
            formapago += "los días %s" % (self.diadepago)
        if len(formapago) > 0:
            formapago += ". "
        return formapago

    textoformapago = property(get_texto_forma_pago)

    def get_albaranes_pendientes_de_facturar(self):
        """
        Devuelve un diccionario de LDCs pendientes de facturar 
        cuyas claves son sus albaranes.
        """
        res = {}
        for albaran in self.albaranesEntrada:
            for ldc in albaran.lineasDeCompra:
                if ldc.facturaCompra == None:
                    if albaran not in res:
                        res[albaran] = [ldc]
                    else:
                        res[albaran].append(ldc)
        return res

    def get_comisiones_pendientes_de_facturar(self):
        """
        Devuelve las comisiones pendientes de facturar del proveedor.
        La estructura en la BD es que un proveedor puede tener uno o 
        varios clientes sobre los que actúa como "representante" en 
        las facturas de compra. Cada uno de esos clientes (por lo general 
        será uno y casi idéntico al registro cliente, solo que en la 
        tabla de proveedores) puede tener una o varias comisiones 
        generadas en albaranes de salida.
        Estas comisiones estarán facturadas sii tienen un registro 
        "servicioTomado" relacionado y éste está a su vez relacionado 
        con una "facturaCompra". No deberían existir registros 
        "servicioTomado" relacionados con una comisión y sin facturas 
        de compra. De ser así, en este método se eliminarán al detectarlos.
        """
        comisiones = []
        #for cliente in self.clientes:
        #    for comision in cliente.comisiones:
        #        # Chequeo coherencia:
        #        for servicio in comision.serviciosTomados:
        #            if servicio.facturaCompra == None:
        #                servicio.destroySelf()
        #        # Ahora miro si de verdad está facturado o no.
        #        if comision.serviciosTomados == []:
        #            comisiones.append(comision)
        return comisiones
    
    def get_transportes_pendientes_de_facturar(self):
        """
        Devuelve las transportes pendientes de facturar del proveedor.
        La estructura en la BD es que un proveedor puede tener uno o 
        varios clientes sobre los que actúa como "representante" en 
        las facturas de compra. Cada uno de esos clientes (por lo general 
        será uno y casi idéntico al registro cliente, solo que en la 
        tabla de proveedores) puede tener una o varias transportes 
        generadas en albaranes de salida.
        Estas transportes estarán facturadas sii tienen un registro 
        "servicioTomado" relacionado y éste está a su vez relacionado 
        con una "facturaCompra". No deberían existir registros 
        "servicioTomado" relacionados con una comisión y sin facturas 
        de compra. De ser así, en este método se eliminarán al detectarlos.
        """
        transportes = []
        for transporte in self.transportesACuenta:
            # Chequeo coherencia:
            for servicio in transporte.serviciosTomados:
                if servicio.facturaCompra == None:
                    servicio.destroySelf()
            # Ahora miro si de verdad está facturado o no.
            if transporte.serviciosTomados == []:
                transportes.append(transporte)
        return transportes

    def get_productos(self):
        """
        Devuelve una lista de objetos producto compra que 
        hayan sido comprados a este proveedor mediante 
        pedidos, albaranes o facturas.
        Como el resultado se convierte a tupla antes de 
        devolverse, este método puede llegar a resultar lento.
        USAR CON CUIDADO.
        """
        productos = ProductoCompra.select(""" id IN (
            SELECT producto_compra_id 
            FROM linea_de_compra 
            WHERE pedido_compra_id IN (
                    SELECT id 
                    FROM pedido_compra
                    WHERE proveedor_id = %d) 
               OR albaran_entrada_id IN (
                    SELECT id
                    FROM albaran_entrada
                    WHERE proveedor_id = %d)
               OR factura_compra_id IN (
                    SELECT id
                    FROM factura_compra 
                    WHERE proveedor_id = %d))
               OR id IN (SELECT producto_compra_id 
                    FROM linea_de_pedido_de_compra 
                    WHERE pedido_compra_id IN (SELECT id
                    FROM pedido_compra 
                    WHERE proveedor_id = %d)) 
            """ % (self.id, self.id, self.id, self.id))
        return tuple(productos)
    
    def get_fechas_vtos_por_defecto(self, fecha):
        """
        Devuelve una lista ordenada de fechas de vencimientos a 
        partir de los vencimientos, día de pago y tomando la 
        fecha recibida como base.
        En caso de que el proveedor no tenga la información necesaria 
        devuelve una lista vacía.
        """
        res = []
        vtos = self.get_vencimientos()
        try:
            diacobro = int(self.diadepago)
        except (TypeError, ValueError):
            diacobro = None
        for incr in vtos:
            res.append(fecha + datetime.timedelta(days = incr))
            if diacobro != None:
                while True:
                    try:
                        res[-1] = datetime.date(day = diacobro, month = res[-1].month, year = res[-1].year)
                        break
                    except:
                        diacobro -= 1
                        if diacobro <= 0:
                            diacobro = 31
                if res[-1] < fecha + datetime.timedelta(days = incr):
                    mes = res[-1].month + 1; anno = res[-1].year
                    if mes > 12:
                        mes = 1; anno += 1
                    res[-1] = datetime.datetime(day = diacobro, month = mes, year = anno)
                while res[-1].weekday() >= 5:
                    res[-1] += datetime.timedelta(days = 1)
        res.sort()
        return res
        
    def get_vencimientos(self):
        """
        Devuelve una lista con los días naturales de los vencimientos
        del cliente. P. ej.:
        - Si el cliente tiene "30", devuelve [30].
        - Si no tiene, devuelve [].
        - Si tiene "30-60", devuelve [30, 60].
        - Si tiene "90 D.F.F." (90 días a partir de fecha factura), devuelve 
          [90].
        - Si tiene "30-120 D.R.F." (30 y 120 días a partir de fecha de 
          recepción de factura) devuelve [30, 120].
        etc.
        En definitiva, filtra todo el texto y devuelve los números que 
        encuentre en cliente.vencimientos.
        """
        res = []
        # Antes había dos campos para "lo mismo", compruebo que no haya 
        # todavía proveedores con algo en "formadepago" y "vencimientos" aún 
        # vacío.
        if ((self.vencimiento == None or self.vencimiento.strip() == '') 
            and (self.formadepago != None and self.formadepago.strip() != '')):
            self.vencimiento = self.formadepago
        if self.vencimiento != None:
            if self.vencimiento.strip() == "":
                res = [0]   # Valor por defecto: a la fecha de factura.
            else:
                import re
                regexpr = re.compile("\d*")
                lista_vtos = regexpr.findall(self.vencimiento)
                try:
                    res = [int(i) for i in lista_vtos if i != '']
                except TypeError, msg:
                    print "ERROR: pclases::cliente.get_vencimientos()-> %s" % (
                        msg)
        return res

    def get_facturas(self, fechaini = None, fechafin = None):
        """
        Devuelve las facturas del proveedor entre las dos 
        fechas recibidas (incluidas). Si ambas son None no 
        aplicará rango de fecha en la búsqueda.
        """
        criterio = (FacturaCompra.q.proveedor == self.id)
        if fechaini != None:
            criterio = AND(criterio, FacturaCompra.q.fecha >= fechaini)
        if fechafin != None:
            criterio = AND(criterio, FacturaCompra.q.fecha <= fechafin)
        return FacturaCompra.select(criterio)

    def calcular_comprado(self, fechaini = None, fechafin = None):
        """
        Devuelve el importe total de compras al proveedor 
        entre las fechas indicadas. Si las fechas son None no 
        impondrá rangos en la búsqueda. No se consideran 
        pedidos ni albaranes, solo compras ya facturadas.
        """
        total = 0
        facturas = self.get_facturas(fechaini, fechafin)
        for f in facturas:
            total += f.calcular_importe_total()
        return total

    def calcular_pagado(self, fechaini = None, fechafin = None):
        """
        Devuelve el importe total de compras pagadas al proveedor 
        entre las fechas indicadas. Si las fechas son None no 
        impondrá rangos en la búsqueda. No se consideran 
        pedidos ni albaranes, solo compras ya facturadas.
        De todas esas facturas, suma el importe de los pagos
        relacionadas con las mismas. _No tiene en cuenta_ las 
        fechas de los pagos, solo las fechas de las facturas 
        a las que corresponden esos pagos (ya que la consulta 
        base es de facturas, lo lógico es saber cuánto de esas 
        facturas está pagado, sea en las fechas que sea).
        """
        total = 0
        facturas = self.get_facturas(fechaini, fechafin)
        for f in facturas:
            for pago in f.pagos:
                total += pago.importe
        return total

    def calcular_pendiente_pago(self, fechaini = None, fechafin = None):
        """
        Devuelve el importe total pendiente de pago. Para ello 
        _ignora los vencimientos_ y simplemente devuelve la diferencia
        entre el importe total facturado y el importe total de los
        cobros relacionados con esas facturas.
        """
        total = self.calcular_comprado(fechaini, fechafin)
        pagado = self.calcular_pagado(fechaini, fechafin)
        pendiente = total - pagado
        return pendiente

class ProductoContratado(SQLObject, PRPCTOO):

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)


class LineaDePedido(SQLObject, PRPCTOO):

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def calcular_precio_unitario_coherente(self, precision = 3):
        """
        Devuelve un precio unitario como cadena con los decimales suficientes 
        (hasta un máximo de 5 y comenzando por «precision») para que al 
        multiplicarlo por la cantidad dé el subtotal con la precisión recibida 
        (por defecto, 3 -por compatibilidad hacia atrás-).
        """
        totlinea = self.get_subtotal()
        cantidad = self.cantidad
        precio = utils.float2str_autoprecision(self.precio, totlinea, cantidad, precision)
        return precio

    def get_subtotal(self, iva = False):
        """
        Devuelve el subtotal de esta línea de pedido.
        """
        subtotal = self.cantidad * self.precio * (1.0 - self.descuento)
        if iva:
            if ldp.pedidoVenta:
                subtotal *= ldp.pedidoVenta.iva
            else:
                raise ValueError, "pclases::LineaDePedido::calcular_subtotal -> La LDP ID %s no tiene pedido del que obtener el IVA."
        return subtotal

    def get_albaraneada(self):
        """
        Devuelve True si la cantidad de la LDP se ha 
        servido por completo en LDVs del pedido con 
        albaranes de salida. Si se ha servido más de 
        lo pedido, también devuelve True.
        """
        servida = self.get_cantidad_servida()
        pedida = self.get_cantidad_pedida()
        return servida >= pedida
    
    def get_cantidad_pedida(self):
        """
        Devuelve la cantidad pedida _del producto_ de la
        LDP en el pedido. OJO: Y al mismo precio -y descuento-. Dos productos
        pedidos a precios distintos, son dos líneas independientes.
        """
        pedida = 0
        for ldp in self.pedidoVenta.lineasDePedido:
            if (ldp.productoCompra == self.productoCompra
                and ldp.precio == self.precio 
                and ldp.descuento == self.descuento):
                pedida += ldp.cantidad
        return pedida

    def get_cantidad_servida(self):
        """
        Devuelve la cantidad servida en LDVs del producto
        de la LDP.
        Postcondición: las LDVs están relacionadas con el 
        pedido y tienen albarán de salida.OJO: Y al mismo precio -y 
        descuento-. 
        Dos productos pedidos a precios distintos, son dos líneas 
        independientes.
        """
        ldvs = self.get_lineas_de_venta()
        servida = 0
        for ldv in ldvs:
            if (ldv.productoCompra == self.productoCompra
                and ldv.precio == self.precio
                and ldv.descuento == self.descuento):
                servida += ldv.cantidad 
        return servida

    def get_lineas_de_venta(self):
        """
        Devuelve las líneas de venta que comparten producto
        con el objeto línea de pedido.
        """
        if self.pedidoVenta != None:
            return [ldv for ldv in self.pedidoVenta.lineasDeVenta 
                    if ldv.productoCompra == self.productoCompra]
        else:
            return []

    def get_albaranes_salida(self):
        """
        Devuelve los albaranes de salida relacionados con la línea
        de pedido atendiendo al producto de venta.
        OJO: Si hay varias LDP del mismo producto, NO DISTINGUE qué 
        LDVs exactamente se corresponde con cada una de ellas.
        """
        return [ldv.albaranSalida for ldv in self.pedidoVenta.lineasDeVenta 
                if ldv.productoCompra == self.productoCompra]

    def get_cantidad_servida_en_esta_LDP(self):
        """
        Devuelve la cantidad servida en la LDP.
        ASSERT: Nunca será superior a la cantidad solicitada en la LDP.
        ASSERT: La suma de get_cantidad_servida_en_esta_LDP para todas las 
                LDP del pedido será igual a la suma de todas las 
                LDV.cantidad = LDP.get_cantidad_servida.
        Hace una estimación para calcular la cantidad servida de la LDP 
        en el caso en que haya varias LDP del mismo producto y varias 
        LDV del mismo producto. Para ello:
          * Si tienen fecha de entrega, las LDP con fecha de entrega menores 
            se supone que han sido las primeras en ser servidas. Lo que exceda 
            será lo pendiente de servir.
          * Si no tienen fecha de entrega, se ordenan por ID y se comienza a 
            repartir la cantidad servida por orden de ID entre las LDP. Lo que 
            exceda debe coincidir con lo pendiente de servir.
        """
        cantidad_a_repartir = self.get_cantidad_servida()
        if cantidad_a_repartir == 0:
            res = 0
        else:
            ldps = [ldp for ldp in self.pedidoVenta.lineasDePedido 
                    if ldp.precio == self.precio 
                        and ldp.descuento == self.descuento 
                        and ldp.productoCompra == self.productoCompra]
            ldps.sort(utils.orden_por_fecha_entrega_o_id)
            for ldp in ldps:
                if cantidad_a_repartir <= 0:    
                    res = 0       # Si no queda nada que repartir, la LDP se 
                    # va a quedar a 0, sea esta o alguna de las siguientes.
                    break
                if ldp == self:    # Soy yo. Me toca.
                    if ldp.cantidad > cantidad_a_repartir:
                        res = cantidad_a_repartir  # Queda menos por repartir 
                        # que lo que se pidió en "mí". Devuelvo lo que queda.
                        break
                    else:
                        res = ldp.cantidad  # De "lo mío" se ha repartido todo. 
                        # (Lo que sobre me da igual, no voy a terminar el 
                        # bucle. Estrategia "cada perrito que se lama su 
                        # pijito", que se llama.)
                        break
                else:
                    cantidad_a_repartir -= ldp.cantidad
        return res

    albaranesSalida = property(get_albaranes_salida)
    albaraneada = property(get_albaraneada)
    cantidadServida = property(get_cantidad_servida)
    cantidadPedida = property(get_cantidad_pedida)
    cantidadServidaPropia = property(get_cantidad_servida_en_esta_LDP)

    def get_producto(self):
        """
        Devuelve el objeto producto relacionado con la línea de venta. None 
        si no hay ningún producto relacionado.
        """
        res = None
        if self.productoCompra != None:
            res = self.productoCompra
        return res

    def set_producto(self, producto):
        """
        Comprueba qué tipo de producto es el del parámetro "producto" 
        recibido e instancia el atributo adecuado poniendo a 
        None el del tipo de producto que no corresponda.
        Si la clase del objeto no es ninguna de las soportadas por 
        la línea de venta, lanzará una excepción TypeError.
        """
        if isinstance(producto, ProductoCompra):
            self.productoCompra = producto
        else:
            raise TypeError

    producto = property(get_producto, set_producto, "Objeto producto de venta o de compra relacionado con la línea de compra.")

class Ticket(SQLObject, PRPCTOO):
    lineasDeVenta = MultipleJoin('LineaDeVenta')

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def calcular_total(self, iva_incluido = True):
        """
        Devuelve el total del ticket basándose en la cantidad y 
        precios de la LDV.
        El total incluye IVA por defecto.
        """
        try:
            subtotal = sqlhub.getConnection().queryOne("""
                SELECT SUM(precio * cantidad * (1 - descuento)) 
                FROM linea_de_venta 
                WHERE ticket_id = %d;""" % self.id)[0]
            #print "  --> He usado consulta."
            if subtotal is None:
                raise TypeError
        except (IndexError, TypeError):
            subtotal = 0
            for ldv in self.lineasDeVenta:
                subtotal += ldv.precio * ldv.cantidad * (1 - ldv.descuento)
            #print "  --> No he usado consulta."
        if iva_incluido:
            iva = 0.18  
            # Las ventas de ticket llevan impepinablemente el 18% de IVA.
        else:
            iva = 0
        total = subtotal * (1 + iva)
        return total

    def get_facturas(self):
        """
        Devuelve las facturas relacionadas con el ticket 
        a través de sus líneas de venta.
        """
        fras = []
        for ldv in self.lineasDeVenta:
            fra = ldv.facturaVenta or ldv.prefactura
            if fra != None and fra not in fras:
                fras.append(fra)
        return fras

class Venta:
    """
    Superclase de líneas de venta y servicios. Define interfaz e implementa 
    métodos comunes.
    """
    def get_comercial(self):
        """
        Devuelve el comercial relacionado con la LDV a través del pedido de 
        venta.
        Devuelve None si el pedido no tiene pedido o comercial relacionado.
        """
        try:
            return self.pedidoVenta.comercial
        except AttributeError:
            return None

    comercial = property(get_comercial)

class LineaDeVenta(SQLObject, PRPCTOO, Venta):

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_cliente(self):
        """
        Devuelve el objeto cliente de la LDV según su pedido, albarán o 
        factura. Por ese orden.
        """
        try:
            return self.pedidoVenta.cliente
        except AttributeError:
            try:
                return self.albaranSalida.cliente
            except AttributeError:
                try:
                    return self.facturaVenta.cliente
                except AttributeError:
                    try:
                        return self.prefactura.cliente
                    except AttributeError:
                        return None

    def calcular_precio_unitario_coherente(self, precision = 3):
        """
        Devuelve un precio unitario como cadena con los decimales suficientes 
        (hasta un máximo de 5 y comenzando por «precision») para que al 
        multiplicarlo por la cantidad dé el subtotal con la precisión recibida 
        (por defecto, 3 -por compatibilidad hacia atrás-).
        """
        totlinea = self.get_subtotal()
        cantidad = self.cantidad
        precio = utils.float2str_autoprecision(self.precio, totlinea, cantidad, precision)
        return precio

    def get_factura_o_prefactura(self):
        """
        Devuelve la factura relacionada, tanto si es facturaVenta
        como prefactura, o None si no tiene ninguna de ellas.
        Como no debería tener ambos valores distintos de nulo a 
        la vez, tiene preferencia facturaVenta sobre prefactura.
        """
        return self.facturaVenta or self.prefactura

    def get_producto(self):
        """
        Devuelve el objeto producto relacionado con la línea de venta.
        None si no hay ningún producto relacionado.
        """
        res = None
        if self.productoCompra != None:
            res = self.productoCompra
        return res

    def set_producto(self, producto):
        """
        Comprueba qué tipo de producto es el del parámetro "producto" 
        recibido e instancia el atributo adecuado poniendo a 
        None el del tipo de producto que no corresponda.
        Si la clase del objeto no es ninguna de las soportadas por 
        la línea de venta, lanzará una excepción TypeError.
        """
        if isinstance(producto, ProductoCompra):
            self.productoCompra = producto
        else:
            raise TypeError

    producto = property(get_producto, set_producto, "Objeto producto de venta o de compra relacionado con la línea de venta.")

    def get_tarifa(self):
        """
        Devuelve la tarifa relacionada con la línea de venta.
        La forma de determinarla es:
        1.- Si pertenece a un pedido y tiene tarifa, comprueba que el precio 
            de la LDV sea el de la tarifa del pedido.
        2.- Si el pedido no tiene tarifa o no coincide con el precio de la LDV 
            para el producto, busca entre todas las tarifas del sistema aquella 
            que tenga el mismo precio para el mismo producto y los periodos de 
            validez a None o dentro de la fecha del pedido o de la fechahora de 
            la LDV, por este orden.
        3.- Si no coincide ninguna o el precio es 0, devuelve None.
        4.- ...
        5.- Profit!
        """
        tarifa = None
        if self.pedidoVenta and \
           self.pedidoVenta.tarifaID != None and \
           abs(self.pedidoVenta.tarifa.obtener_precio(self.producto) - self.precio) < 0.001:   
                # NOTA: Manejamos siempre 3 decimales como mucho en precios. 
                #       No hay que ser más papistas que el papa.
            tarifa = self.pedidoVenta.tarifa
        elif self.precio == 0.0:
            tarifa = None
        else:
            primera = None
            for t in Tarifa.select(orderBy = "-id"):    
                # Empiezo a recorrer partiendo de la última tarifa, ya que 
                # probablemente sea la que esté vigente y seguramente sea la 
                # que interesa obtener en caso de que el pedido no tuviera 
                # tarifa.
                if abs(t.obtener_precio(self.producto) - self.precio) < 0.001:
                    fechaldv = (self.pedidoVenta 
                                and self.pedidoVenta.fecha 
                                or self.fechahora)
                    if ((t.periodoValidezIni == None 
                             or t.periodoValidezIni <= fechaldv) 
                        and (t.periodoValidezFin == None 
                             or t.periodoValidezFin >= fechaldv)):
                        tarifa = t
                        if not primera:
                            primera = tarifa
                        if t.esta_en_tarifa(self.producto):
                            primera = t
                            break
                        # Si no está en la tarifa, aunque coincida el precio, 
                        # sigo buscando. Si al final no estaba en ninguna 
                        # tarifa devolverá la primera con la que coincidió o 
                        # la última de todas.
            if primera:
                tarifa = primera
        return tarifa

    def get_str_bultos(self):
        """
        Devuelve los bultos de la línea de venta como 
        cadena de texto con las unidades del producto.
        Si el producto son balas o bigbags, no se puede
        saber a priori cuántos bultos pertenecen a 
        la línea de venta.
        Si la línea de venta no es de un producto de 
        venta devuelve "?"
        """
        res = "?"
        if self.productoCompraID != None:
            res = "-" 
        return res

    def get_str_cantidad(self):
        """
        Devuelve la cantidad de la línea de venta como 
        cadena de texto con las unidades del producto.
        """
        res = "?"
        if self.productoCompraID != None:
            unidad = self.productoCompra.unidad
            res = "%s %s" % (utils.float2str(self.cantidad), unidad)
        return res

    def get_cantidad_total_solicitada_del_producto(self):
        """
        Devuelve la cantidad total del producto de 
        esta línea de venta solicitada en el pedido completo, 
        SIN TENER EN CUENTA PRECIOS.
        """
        res = 0
        if self.pedidoVentaID != None:
            for ldv in self.pedidoVenta.lineasDeVenta:
                if ldv.producto == self.producto:
                    res += ldv.cantidad
        return res

    def get_cantidad_albaraneada(self):
        """
        Si la LDV pertenece a un albarán, devuelve la 
        cantidad albaraneada de su producto en ese 
        albarán. Si no, devuelve 0.
        """
        res = 0
        if self.albaranSalidaID != None:
            producto = self.producto
            if isinstance(producto, ProductoCompra):  # Si es un producto de 
                # compra, la cantidad albaraneada es la de la propia LDV, 
                res = self.cantidad                     # ya que no tiene 
                # bultos ni nada que se pueda contar aparte de eso.
        return res

    def eliminar(self):
        """
        Intenta eliminar la línea de venta.
        Si tiene relaciones activas con 
        albaranes, pedidos o facturas no la 
        eliminará.
        Devuelve 0 si se elimina de la BD y 
        el número de relaciones en otro caso.
        """
        rels = 0
        if self.pedidoVenta != None:
            rels += 1
        if self.albaranSalida != None:
            rels += 1
        if self.facturaVenta != None:
            rels += 1
        if self.prefactura != None:
            rels += 1
        if rels == 0:
            try:
                self.destroySelf()
            except Exception, msg:  
                # No es buena práctica capturar _cualquier_ excepción 
                # genérica. Esto es eventual para temas de depuración.
                print "ERROR: pclases::LineaDeVenta:eliminar-> No se pudo eliminar la LDV. Excepción disparada: %s" % (msg)
        return rels

    cantidad_albaraneada = property(get_cantidad_albaraneada)
    cantidad_total_solicitada_del_producto = property(get_cantidad_total_solicitada_del_producto)

    def get_subtotal(self, iva = False):
        """
        Devuelve el subtotal con o sin IVA (según se indique) de 
        la línea de compra: precio * cantidad - descuento.
        """
        res = self.cantidad * self.precio * (1 - self.descuento)
        if iva:
            if self.facturaVentaID != None: 
                res *= 1 + self.facturaVenta.iva
            elif self.prefacturaID != None: 
                res *= 1 + self.prefactura.iva
            elif self.pedidoVentaID != None:
                res *= 1 + self.pedidoVenta.iva
            elif (self.albaranSalidaID != None 
                  and self.albaranSalida.clienteID != None):
                res *= 1 + self.albaranSalida.cliente.iva
            elif self.ticketID != None:
                res *= 1.18     # PVP siempre 18% de IVA.
        return res

    calcular_subtotal = get_subtotal

    def calcular_beneficio(self):
        """
        Devuelve el precio de venta sin IVA por el porcentaje de la tarifa 
        aplicada a la línea de venta y por la cantidad.
        Si la tarifa de la LDV no se pudo determinar, el porcentaje 
        corresponde a la diferencia entre el precio por defecto y el precio de 
        venta.
        """
        precio = self.precio
        cantidad = self.cantidad
        producto = self.producto
        tarifa = self.get_tarifa()
        if tarifa != None:
            porcentaje = tarifa.get_porcentaje(producto, fraccion = True)
        else:
            try:
                porcentaje = (self.precio / producto.precioDefecto) - 1.0
            except ZeroDivisionError:
                porcentaje = 1.0
        return producto.precioDefecto * porcentaje * cantidad

    def calcular_precio_costo(self):
        """
        Devuelve el precio de costo del producto de la LDV *en el momento 
        actual* del cálculo.
        Es imposible, con el modelo de datos actual (29/04/2008) saber a 
        qué precio de costo valorar el producto de compra. Se usa 
        precioDefecto. Se podría usar la función de valoración, pero en ese 
        caso se falsearía el método para calcular el beneficio.
        Por tanto, cambiar el precioDefecto (= precio de costo a todos los 
        efectos) cambia la estimación del beneficio y este cálculo del precio 
        de costo en ventas antiguas -esto es, anteriores al cambio-.
        Hago un método en vez de consultar directamente al producto por si 
        en el futuro necesito cambiarlo, usar esta función desde el 
        calcular_beneficio y demás; y así tener centralizado el asunto.
        """
        return self.producto.precioDefecto

class LineaDePedidoDeCompra(SQLObject, PRPCTOO):
    lineasDeCompra = RelatedJoin('LineaDeCompra', 
                joinColumn='linea_de_pedido_de_compra_id', 
                otherColumn='linea_de_compra_id', 
                intermediateTable='linea_de_pedido_de_compra__linea_de_compra')

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_precio_con_descuento(self):
        """
        Precio total de la línea incluyendo descuento, pero sin incluir el IVA.
        """
        return self.precio * (1 - self.descuento)

    precioConDescuento = property(get_precio_con_descuento, doc = get_precio_con_descuento.__doc__)

    def get_cantidad_servida(self):
        """
        Devuelve la cantidad servida del producto solicitado en la línea de 
        pedido de compra. Si el producto se ha pedido en más de una LDPC 
        se estima qué parte de la LDC se ha servido en cada una de ellas 
        para avergiuar la cantidad restante de la LDPC actual.
        """
        producto = self.productoCompra
        pedida = self.cantidad
        servida = 0
        ldpcs = [self]
        ldcs = []
        if self.pedidoCompra == None:
            print "pclases.py::get_cantidad_servida -> ERROR: La línea de pedido de compra ID %d no tiene pedido." % (self.id)
            return 0
        for ldpc in self.pedidoCompra.lineasDePedidoDeCompra: 
                # Hay una relación muchos a muchos entre LDC y LDPC que podría evitarme tirar del pedido de compra, construir 
                # las dos listas, compararlas...
            if ldpc.productoCompra == producto.id and ldpc != self:   # "Yo" ya estoy.
                pedida += ldpc.cantidad
                ldpcs.append(ldpc)
        for ldc in self.pedidoCompra.lineasDeCompra:
            if ldc.productoCompra == producto.id:
                servida += ldc.cantidad
                ldcs.append(ldc)
        if servida >= pedida:
            # Si se ha servido todo, es un derroche de recursos ponerme a buscar nada. De esta LDPC se ha servido toda su cantidad.
            res = self.cantidad
        else:
            try:
                ldpcs.sort(utils.cmp_fecha_id)
            except TypeError, msg:
                print "pclases.py (get_cantidad_servida): Excepción al ordenar líneas de pedido de compra: %s" % (msg)
                print ldpcs
            try:
                ldcs.sort(utils.cmp_fecha_id)
            except TypeError, msg:
                print "pclases.py (get_cantidad_servida): Excepción al ordenar líneas de compra: %s" % (msg)
                print ldcs
            ildpc = 0
            while ildpc < len(ldpcs):
                ldpc = ldpcs[ildpc]
                servida -= ldpc.cantidad
                if ldpc == self:
                    if servida >= 0:
                        res = self.cantidad
                    else:
                        res = self.cantidad + servida
                    break
                ildpc += 1
        return res
        
    cantidadServida = property(get_cantidad_servida, doc = "Cantidad servida correspondiente a la línea de pedido de compra.")
    
    def get_cantidad_pendiente(self):
        """
        Devuelve la cantidad pendiente de servir de la línea de pedido de compra actual.
        """
        return self.cantidad - self.cantidadServida
    
    cantidadPendiente = property(get_cantidad_pendiente, doc = "Cantidad pendiente de servir correspondiente a la línea de pedido de compra.")
        
    def get_subtotal(self, iva = False):
        """
        Devuelve el subtotal con o sin IVA (según se indique) de 
        la línea de compra: precio * cantidad - descuento.
        """
        res = self.cantidad * self.precio * (1 - self.descuento)
        if iva and self.pedidoCompraID: 
            res *= (1 + self.pedidoCompra.iva)
        return res
    
    def es_igual_salvo_cantidad(self, ldpc):
        """
        Compara la LDPC con otra recibida. Devuelve True si los valores 
        son iguales para los campos:
          - pedidoCompraID
          - albaranEntradaID
          - facturaCompraID
          - productoCompraID
          - precio
          - descuento
          - fecha de entrega
          - texto de entrega
        """
        campos = ("pedidoCompraID", 
                  "productoCompraID", 
                  "precio", 
                  "descuento", 
                  "textoEntrega", 
                  "fechaEntrega"
                 )
        for campo in campos:
            if getattr(self, campo) != getattr(ldpc, campo):
                return False
        return True

class PedidoCompra(SQLObject, PRPCTOO):
    lineasDeCompra = MultipleJoin('LineaDeCompra')
    lineasDePedidoDeCompra = MultipleJoin('LineaDePedidoDeCompra')
    documentos = MultipleJoin('Documento')

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def unificar_ldcs(self):
        """
        Combina las líneas de compra del pedido que sólo 
        difieran en la cantidad, en una sola.
        """
        a_borrar = []
        copia_ldcs = self.lineasDeCompra[:]     # Para evitar que se cambien de orden al actualizar cantidades.
        for i in xrange(len(copia_ldcs)):
            ldc1 = copia_ldcs[i]
            for j in xrange(i+1, len(copia_ldcs)):
                ldc2 = copia_ldcs[j]
                if ldc1 not in a_borrar and ldc2 not in a_borrar and ldc1.es_igual_salvo_cantidad(ldc2):
                    ldc1.cantidad += ldc2.cantidad
                    a_borrar.append(ldc2)
        for ldc in a_borrar:
            try:
                ldc.destroySelf()
            except:
                print "pclases.py::unificar_ldcs-> No se pudo eliminar la LDP ID %d. Se asigna 0 a cantidad para evitar descuadres." % (ldc.id)
                ldc.cantidad = 0
    
    def unificar_ldpcs(self):
        """
        Combina las líneas de compra del pedido que sólo 
        difieran en la cantidad, en una sola.
        """
        a_borrar = []
        copia_ldpcs = self.lineasDePedidoDeCompra[:]     # Para evitar que se cambien de orden al actualizar cantidades.
        for i in xrange(len(copia_ldpcs)):
            ldpc1 = copia_ldpcs[i]
            for j in xrange(i+1, len(copia_ldpcs)):
                ldpc2 = copia_ldpcs[j]
                if ldpc1 not in a_borrar and ldpc2 not in a_borrar and ldpc1.es_igual_salvo_cantidad(ldpc2):
                    ldpc1.cantidad += ldpc2.cantidad
                    a_borrar.append(ldpc2)
        for ldpc in a_borrar:
            try:
                ldpc.destroySelf()
            except:
                print "pclases.py::unificar_ldpcs-> No se pudo eliminar la LDP ID %d. Se asigna 0 a cantidad para evitar descuadres." % (ldpc.id)
                ldpc.cantidad = 0

    def get_productos_pendientes_servir(self):
        """
        Devuelve una tupla de tuplas de objetos producto y la cantidad 
        total pendiente de servir del mismo. No se tiene en cuenta si 
        el pedido está o no cerrado y se considera que un resto negativo 
        también es "pendiente". Es decir, sólo filtra y no devuelve 
        aquellos productos cuya cantidad solicitada y cantidad servida 
        coinciden por completo.
        """
        res = []
        productos = {}
        for ldpc in self.lineasDePedidoDeCompra:
            producto = ldpc.productoCompra
            if producto not in productos:
                productos[producto] = {'pedida': ldpc.cantidad, 'servida': 0}
            else:
                productos[producto]['pedida'] += ldpc.cantidad
        for ldc in self.lineasDeCompra:
            producto = ldc.productoCompra
            if producto not in productos:
                productos[producto] = {'pedida': 0, 'servida': ldc.cantidad}
            else:
                productos[producto]['servida'] += ldc.cantidad
        for producto in productos:
            diferencia = productos[producto]['pedida'] - productos[producto]['servida']
            if diferencia != 0:
                res.append((producto, diferencia))
        return tuple(res)

    def get_lineas_sin_albaranear(self):
        """
        Devuelve las LDPC del pedido que no están albaraneadas por completo.
        """
        res = []
        # DONE: Esta función está a punto de quedar obsoleta con la implementación de las nuevas líneas de pedido de compra.
        # return [ldc for ldc in self.lineasDeCompra if ldc.albaranEntrada == None]
        for ldpc in self.lineasDePedidoDeCompra:
            if ldpc.cantidad > ldpc.cantidadServida:
                res.append(ldpc)
        return res

    def get_pendiente(self, producto):
        """
        Devuelve la cantidad pendiente de recibir del 
        producto según el pedido actual y su valoración 
        en precio.
        """
        cantidad, valor = 0, 0
        lineas_pendientes = [l for l in self.get_lineas_sin_albaranear() if l.productoCompra == producto]
        for linea in lineas_pendientes:
            cantidad += linea.cantidadPendiente
            valor += cantidad * linea.precio
        return cantidad, valor

    def get_menor_precio(self, productoCompra):
        """
        Devuelve el menor precio del pedido para el producto 
        de compra recibido.
        Devuelve None si el producto no se solicitó en el pedido.
        """
        menor = None
        for ldpc in self.lineasDePedidoDeCompra:
            if ldpc.productoCompra == productoCompra.id:
                precio = ldpc.precio * (1 - ldpc.descuento)
                if menor == None or precio < menor:
                    menor = precio
        return menor

    def get_cantidad_pedida(self, productoCompra):
        """
        Devuelve la cantidad pedida en total del producto de 
        compra en este pedido.
        """
        cantidad = 0
        for ldpc in self.lineasDePedidoDeCompra:
            if ldpc.productoCompra == productoCompra.id:
                cantidad += ldpc.cantidad
        return cantidad

class Producto:
    """
    Superclase para productos de compra y de venta.
    ... que ya iba siendo hora.
    """
    def es_fibra(self):
        """
        Devuelve True si el producto es un producto de venta y además 
        es fibra (bala, balas de cable o bigbags de fibra de cemento)
        """
        try:
            return (self.es_bala() or self.es_bala_cable() or self.es_bigbag()
                    or self.es_caja())
        except AttributeError:
            return False

    def ajustar_a_fecha_pasada(self, fecha, cantidad = None, bultos = None, 
                               almacen = None):
        """
        Método "virtual" que debe ser implementado por las clases hijas.
        Ajusta las existencias actuales en base a las que se le indiquen en 
        la fecha «fecha».
        Esto se hace sumando y restando producciones, ventas, etc. hasta 
        llegar al día actual.
        «cantidad» es el stock en las unidades del producto (metros, kilos...)
        «bultos» son las existencias en bultos completos (número de artículos 
        si es un producto de venta o la cantidad que sea según la razón 
        bultos/cantidad del producto de compra).
        Los dos parámetros no pueden ser None a la vez. Si alguno de los dos 
        falta, intenta calcular el otro. Si no se puede calcular lanzará una 
        excepción.
        Si no se especifica almacén ajustará las cantidades globales en 
        función del origen/destino de la mercancía en cada albarán tratado.
        Si se especifica un almacén solo se tendrán en cuenta los movimientos 
        de ese almacén y ajustará el global en consecuencia, pero no se 
        hará nada en el resto de almacenes.
        """
        raise NotImplementedError

class Clase(SQLObject, PRPCTOO, Producto):

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def es_privada(self):
        """
        Devuelve True si es una clase privada.
        """
        return self.pax == 1

    def calcular_precio_clase_pax(self, tarifa = None, iva_incluido = True):
        """
        Devuelve el precio por cada clase. Por definición, el precio que 
        guardamos en el producto es precio/persona y mes, 'so' este también 
        es precio por persona.
        OJO: Para usar el precio de alguna tarifa hay que pasar la tarifa 
        en la cabecera.
        """
        if not tarifa:
            precio_completo_mes = self.productoCompra.precioDefecto
        else:
            precio_completo_mes = tarifa.obtener_precio(self.productoCompra)
        # Puede haber varios tipos de clases en un mismo producto. Veamos 
        # cuántas clases al mes hay entre todos, para hacer la media:
        clasesTotales = 0.0
        for clase in self.productoCompra.clases:
            clasesTotales += clase.numClasesTotales
        precio_clase = precio_completo_mes / clasesTotales
        if iva_incluido:
            precio_clase *= 1.18
        return precio_clase

    def calcular_numMeses(self):
        """
        Devuelve el número de meses que durará la clase en función de las 
        clases al mes que tiene y del número de clases totales.
        """
        res = self.numClasesTotales * 1.0
        res /= self.numClasesMes
        return res

    def get_str_dias(self):
        """
        Devuelve los dias como cadena en los que se da esta clase.
        """
        Clase.siglas_to_dias(self.diaSemana)

    def siglas_to_lista_dias(siglas):
        # TODO: Esto debería estar preparado para l10n.
        try:
            siglas = siglas.upper()
        except:     # Es None, no hay nada que convertir
            return ""
        dias = []
        for c in siglas:
            if c == "L":
                dias.append("lunes")
            elif c == "M":
                dias.append("martes")
            elif c == "X":
                dias.append("miércoles")
            elif c == "J":
                dias.append("jueves")
            elif c == "V":
                dias.append("viernes")
            elif c == "S":
                dias.append("sábado")
            elif c == "D":
                dias.append("domingo")
        orden = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", 
                 "domingo"]
        dias.sort(key = lambda x: orden.index(x))
        return dias 

    siglas_to_lista_dias = staticmethod(siglas_to_lista_dias)

    def siglas_to_dias(siglas):
        dias = Clase.siglas_to_lista_dias(siglas)
        return ", ".join(dias)

    siglas_to_dias = staticmethod(siglas_to_dias)
    listadias = ("lunes", "martes", "miercoles", "jueves", "viernes", 
                 "sabado", "domingo")
    listadias_str = ("lunes", "martes", "miércoles", "jueves", "viernes", 
                     "sábado", "domingo")
    listadias_siglas = ("L", "M", "X", "J", "V", "S", "D")

class ProductoCompra(SQLObject, PRPCTOO, Producto):
    lineasDeCompra = MultipleJoin('LineaDeCompra')
    lineasDeVenta = MultipleJoin('LineaDeVenta')
    consumos = MultipleJoin('Consumo')
    pruebasGranza = MultipleJoin('PruebaGranza')
    lineasDePedidoDeCompra = MultipleJoin('LineaDePedidoDeCompra')
    historialesExistenciasCompra = MultipleJoin('HistorialExistenciasCompra')
    precios = MultipleJoin('Precio')
    lineasDePedido = MultipleJoin('LineaDePedido')
    stocksAlmacen = MultipleJoin("StockAlmacen")
    clases = MultipleJoin("Clase")
    productosContratados = MultipleJoin("ProductoContratado")
    actividades = MultipleJoin("Actividad")

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    preciopordefecto = property(lambda o: o.precioDefecto)

    def get_puid(self):
        """
        Devuelve una *cadena* con PV: y el ID del producto.
        puid viene a ser como ProductoUnicoID (un ID único para cada producto 
        cuyo tipo de objeto se diferencia por la cadena que antecede a los :).
        """
        return "PC:%d" % self.id

    def set_existencias(self, cantidad, almacen = None):
        """
        Ajusta las existencias *actuales* del producto a la cantidad recibida.
        Si no se especifica almacén, se ajustará en base al almacén principal
        (según el contrato de add_existencias).
        Anotará en las observaciones del caché de existencias que se ha 
        ajustado programáticamente.
        """
        #self.ajustar_a_fecha_pasada(fecha = mx.DateTime.today(), 
        #                            cantidad = cantidad, almacen = almacen, 
        #    observaciones_historico = "Cacheado por ajuste de existencias", 
        #    check_assert = False)   # No tiene sentido comprobar nada porque 
        #                            # estamos forzando las de HOY sin base 
        #                            # ninguna de entradas y salidas.
        ## Pasando de tirar de un algoritmo que no se pensó justamente para 
        ## el caso contrario.
        self.sync()
        actual = self.existencias
        delta = cantidad - actual
        self.add_existencias(delta, almacen, actualizar_global = True)
        # Cacheo para que quede constancia de que es un ajuste manual:
        for a in Almacen.select():
            try:
                HistorialExistenciasCompra(productoCompra = self, 
                        cantidad = a.get_existencias(self), 
                        observaciones = "Cacheado por ajuste de existencias", 
                        fecha = mx.DateTime.today(), 
                        almacen = a)
            except:     # Integrity error. Ya existía para esa fecha.
                for hec in HistorialExistenciasCompra.select(AND(
                   HistorialExistenciasCompra.q.productoCompraID == self.id, 
                   HistorialExistenciasCompra.q.almacenID == a.id, 
                   HistorialExistenciasCompra.q.fecha == mx.DateTime.today())):
                    hec.destroySelf()
                HistorialExistenciasCompra(productoCompra = self, 
                        cantidad = a.get_existencias(self), 
                        observaciones = "Cacheado por ajuste de existencias", 
                        fecha = mx.DateTime.today(), 
                        almacen = a)

    def ajustar_a_fecha_pasada(self, fecha, cantidad = None, bultos = None, 
                               almacen = None, 
                               observaciones_historico 
                                    = "Cacheado por ajuste de existencias "
                                      "a fecha pasada", 
                               check_assert = True):
        """
        Ajusta las existencias actuales en base a las que se le indiquen en 
        la fecha «fecha».
        Esto se hace sumando y restando producciones, ventas, etc. hasta 
        llegar al día actual.
        «cantidad» es el stock en las unidades del producto (metros, kilos...)
        «bultos» son las existencias en bultos completos según la razón 
        bultos/cantidad del producto de compra.
        Los dos parámetros no pueden ser None a la vez. Si alguno de los dos 
        falta, intenta calcular el otro. Si no se puede calcular lanzará una 
        excepción.
        Si no se especifica almacén ajustarán las cantidades globales tocando 
        solo el almacén principal (no hay otra forma de hacerlo, ya que si 
        las cantidades de los almacenes están mal, lo que tenemos es un 
        sistema de n+1 ecuaciones con n incógnicas donde n = #almacenes).
        Si se especifica un almacén solo se tendrán en cuenta los movimientos 
        de ese almacén y ajustará el global en consecuencia, pero no se 
        hará nada en el resto de almacenes.
        Si check_assert es True comprobará después de ajustar que las 
        existencias siguen siendo coherentes con los históricos, entradas y 
        salidas (a False es útil para llamadas recursivas).
        """
        if cantidad == None:
            raise ValueError, "En productos de compra se debe especificar "\
                              "una cantidad. No es posible la estimación a "\
                              "partir de bultos."
        # 1.- Calcular entradas y salidas
        delta = {}
        if not almacen:
            for a in Almacen.select():
                delta[a] = self.get_entradas_y_salidas_entre(fecha, 
                                                             almacen = a)
        else:
            delta[almacen] = self.get_entradas_y_salidas_entre(fecha, 
                                                            almacen = almacen)
        if DEBUG:
            print "pclases::ajustar_a_fecha_pasada -> delta:"
            for alm in delta:
                print "\t%s: %s" % (alm.nombre, delta[alm])
        # 2.- Eliminar cachés falsear consultas de históricos.
        i = 0
        if not almacen:
            for hec in self.historialesExistenciasCompra:
                hec.destroySelf()
                i += 1
        else:
            for hec in self.historialesExistenciasCompra:
                if hec.almacen == almacen:
                    hec.destroySelf()
                    i += 1
        if DEBUG:
            print "pclases::ajustar_a_fecha_pasada -> "\
                  "%d historiales eliminados." % i
        # 3.- Actualizar existencias del almacén (si es caso) y globales.
        if DEBUG:
            print "pclases::ajustar_a_fecha_pasada -> "\
                  "Existencias actuales antes de tocar: %s" % (
                    utils.float2str(self.existencias))
            for stock_alm in self.stocksAlmacen:
                print "\tAlmacén %s: %s" % (
                    stock_alm.almacen.nombre, 
                    utils.float2str(stock_alm.existencias))
        ppal = Almacen.get_almacen_principal()
        for alm_stock in self.stocksAlmacen:
            if almacen:
                if alm_stock.almacen == almacen:
                    alm_stock.existencias = (cantidad 
                                                + delta[alm_stock.almacen])
                else:
                    pass    # No los toco
            else:   # No se especifica almacén. Ajusto el principal.
                if alm_stock.almacen == ppal:
                    # A la cantidad que debía haber en la fecha indicada, le 
                    # sumo entradas y salidas totales para que me dé la 
                    # cantidad actual. Después, como los demás almacenes no 
                    # los voy a tocar, la diferencia de ambos totales es lo 
                    # que meto en el principal a día de hoy.
                    total = cantidad + sum([delta[sa] for sa in delta]) 
                    #print total
                    total_menos_ppal = sum([sa.existencias 
                                            for sa in self.stocksAlmacen 
                                            if sa.almacen != ppal])
                    #print total_menos_ppal
                    alm_stock.existencias = total - total_menos_ppal
            alm_stock.sync()
        self.existencias = sum([sa.existencias for sa in self.stocksAlmacen])
        self.sync()
        
        if check_assert:
            if not almacen:
                try:
                    ehist = self.get_existencias_historico(fecha = fecha, 
                            observaciones_historico = observaciones_historico)
                    assert ehist == cantidad, "get_existencias_historico: %f;"\
                                              " cantidad: %f" % (ehist,
                                                                 cantidad)
                except AssertionError:
                    # Estará tirando de históricos anteriores erróneos. 
                    # Borro todo.
                    if DEBUG:
                        selfdesc = self.descripcion
                        print "\t... Borrando históricos de %s" % (selfdesc)
                    for hec in self.historialesExistenciasCompra:
                        hec.destroySelf()
                    # Y vuelvo a intentarlo.
                    self.ajustar_a_fecha_pasada(fecha, cantidad, bultos, 
                                                almacen, check_assert = False)
                    ehist = self.get_existencias_historico(fecha = fecha, 
                                                observaciones_historico 
                                                    = observaciones_historico)
                    assert ehist == cantidad, "get_existencias_historico: %f;"\
                                              " cantidad: %f" % (ehist, 
                                                                 cantidad)
            else:
                try:
                    ehist = self.get_existencias_historico(fecha = fecha, 
                            almacen = almacen, 
                            observaciones_historico = observaciones_historico)
                    assert ehist == cantidad, "get_existencias_historico: %f;"\
                                              " cantidad: %f" % (ehist,
                                                                 cantidad)
                except:
                    # Estará tirando de históricos anteriores erróneos. 
                    # Borro todo.
                    if DEBUG:
                        selfdesc = self.descripcion
                        print "\t... Borrando históricos de %s" % selfdesc
                    for hec in self.historialesExistenciasCompra:
                        hec.destroySelf()
                    # Y vuelvo a intentarlo.
                    self.ajustar_a_fecha_pasada(fecha, cantidad, bultos, 
                                                almacen, check_assert = False)
                    ehist = self.get_existencias_historico(fecha = fecha, 
                            almacen = almacen, 
                            observaciones_historico = observaciones_historico)
                    assert ehist == cantidad, "get_existencias_historico: %f;"\
                                              " cantidad: %f" % (ehist, 
                                                                 cantidad)
        if DEBUG:
            print "pclases::ajustar_a_fecha_pasada -> "\
                  "Existencias actualizadas a %s:"  % (
                    utils.float2str(self.existencias))
            for stock_alm in self.stocksAlmacen:
                print "\tAlmacén %s: %s" % (
                    stock_alm.almacen.nombre, 
                    utils.float2str(stock_alm.existencias))

    def get_existencias_historico(self, 
                                  fecha = datetime.datetime.now(), 
                                  forzar = False, 
                                  almacen = None, 
                                  observaciones_historico 
                                    = "Cacheado automáticamente"):
        """
        Devuelve las existencias del producto de compra en 
        la fecha proporcionada. Si no se le pasa ninguna 
        devuelve las existencias -que en teoría- deberían ser 
        las actuales (salvo pequeña desviación de fechas en 
        albaranes, consumos o por CORRECCIONES MANUALES).
        0.- Si fecha es la fecha actual devuelve las existencias en tabla.
        PROTOCOLO DE CACHÉ:
            1.- Buscar la fecha recibida en la tabla HistorialExistenciasCompra
            2.- Si se encuentra:
                2.1.- Si forzar = False:
                    2.1.1.- Devuelve la cantidad de la tabla.
                    2.1.2.- EOA.
                2.2.- Si forzar = True:
                    2.2.1.- Elimina el registro de la caché.
                    2.2.1.- Pasa al paso 3.
            3.- Busca en la tabla historialExistenciasCompra la fecha 
                anterior más cercana a la recibida.
            4.- Si encuentra una fecha: 
                4.1.- A la cantidad en esa fecha resta los consumos y salidas 
                      del producto entre las fechas del histórico y la 
                      recibida.
                4.2.- A la cantidad resultante suma las entradas entre la 
                      fecha del histórico y la fecha recibida.
            (4 1/2.- Aquí cabría la posibilidad de poder hacer la operación 
                     inversa: partir de un registro de caché superior a la 
                     fecha recibida y restar entradas y sumar consumos y 
                     salidas en lugar de hacerlo al contrario como en el 
                     paso 4.)
            5.- Si no encuentra una fecha anterior:
                4.1.- Del total actual de existencias suma los consumos y 
                      salidas del producto DESDE la fecha recibida.
                4.2.- A la cantidad resultante resta las entradas de los 
                      albaranes DESDE la fecha recibida.
            6.- Crea un registro en la tabla histórico con la fecha y 
                cantidad resultante.
        ### ACTUALIZACIÓN ALMACENES
        Si almacen == None, se devuelve el histórico de la suma de todas las 
        almacenes. Si es != None, devuelve el histórico para ese almacén en 
        concreto.
        """
        res = None
        if fecha == datetime.datetime.now():
            if not almacen:
                res = self.existencias
            else:
                res = self.get_existencias(almacen)
        else:
            HEC = HistorialExistenciasCompra
            if almacen:
                regs_cache = HEC.select(AND(HEC.q.productoCompraID == self.id, 
                                            HEC.q.fecha == fecha, 
                                            HEC.q.almacenID == almacen.id))
                if regs_cache.count() > 1:
                    print "WARNING: pclases.py (get_existencias_historico) "\
                          "-> Más de un registro en caché o forzado por "\
                          "parámetro. Los elimino todos y recuento."
                    for reg in regs_cache:
                        reg.destroySelf()
                    res = self.get_existencias_historico(fecha, 
                            almacen = almacen, 
                            observaciones_historico = observaciones_historico)
                elif regs_cache.count() == 1:
                    if not forzar:
                        res = regs_cache[0].cantidad
                    else:
                        regs_cache[0].destroySelf()
                        res = None
            else:       # not almacen
                # Para todos los almacenes necesito sumatorio, pero no a partir 
                # de registros directos de la BD porque puede que un almacén no 
                # esté cacheado en esa fecha y haga falta interpolación.
                caches_almacenes = []
                for a in Almacen.select():
                    cache = self.get_existencias_historico(fecha, almacen = a, 
                            forzar = forzar, 
                            observaciones_historico = observaciones_historico)
                    caches_almacenes.append(cache)
                res = sum(caches_almacenes)
        # --- 
        if res == None:  # Aún no he encontrado las existencias, bien por 
                         # no caché o bien porque hay que forzar.
            if almacen:
                cache_mas_cercano = HEC.select(
                    AND(HEC.q.fecha < fecha, 
                        HEC.q.productoCompra == self.id,
                        HEC.q.almacen == almacen.id), 
                    orderBy = "-fecha")
                if cache_mas_cercano.count() >= 1:
                    cache_mas_cercano = cache_mas_cercano[0]
                    existencias_anteriores = cache_mas_cercano.cantidad
                    entradas_y_salidas = self.get_entradas_y_salidas_entre(
                        cache_mas_cercano.fecha + datetime.timedelta(days = 1), fecha, 
                        almacen = almacen)
                        # Le sumo un día porque en el caché ya están incluídas 
                        # las existencias justo hasta las 23:59:59 de ese mismo 
                        # día.
                    res = existencias_anteriores + entradas_y_salidas
                    if DEBUG:
                        print "pclases::ProductoCompra."\
                              "get_existencias_historico -> Caché más "\
                              "cercano:", \
                              cache_mas_cercano.fecha.strftime("%Y-%m-%d"),\
                              "; existencias_anteriores:", \
                              existencias_anteriores, \
                              "; entradas_y_salidas:", entradas_y_salidas, \
                              "; res:", res
                else:
                    res=(self.get_existencias(almacen)
                         - self.get_entradas_y_salidas_entre(fecha, 
                                                             fechafin = None, 
                                                             almacen=almacen))
                nuevo_cache = HEC(productoCompra = self.id, 
                                  fecha = fecha, 
                                  cantidad = res, 
                                  observaciones = observaciones_historico, 
                                  almacen = almacen)
            else:   # not almacen. Misma movida pero uno por uno. No debería 
                    # entrar aquí porque es un caso que debería cubrir la rama 
                    # else del if anterior... ¿salvo que haya que forzar?
                caches_almacenes = []
                for a in Almacen.select():
                    cache = self.get_existencias_historico(fecha, forzar, a, 
                        observaciones_historico = observaciones_historico)
                    caches_almacenes.append(cache)
                res = sum([caches_almacenes])
        if DEBUG:
            print "get_existencias_historico -> res", res
        return res

    def __get_consultas_entradas_y_salidas_desde(self, sqlfechaini, 
                                                 almacen = None):
        """
        Devuelve tres ResultSelect de entradas, consumos y salidas del 
        producto de compra desde la fecha indicada en formato SQL (%Y-%m-%d).
        Si almacen != None, devuelve lo anterior pero solo para ese almacén.
        Dado que la mayoría de consumos también se contabilizan en un albarán 
        interno de consumo, no se devolverán los consumos que pertenezcan a un 
        parte que tenga albarán interno y éste una línea de venta con el 
        mismo producto y cantidad que el consumo.
        """
        # XXX
        """
        #unittest:
        import pclases, mx
        pclases.DEBUG = True
        pc = pclases.ProductoCompra.select(
            pclases.ProductoCompra.q.descripcion.contains("PLAST"), 
            orderBy = "id")[0]
        fechaini = datetime.datetime(2009,1,1)
        pc.get_entradas_y_salidas_entre(fechaini)
        pc.get_entradas_y_salidas_entre(fechaini, 
            almacen = pclases.Almacen.get_almacen_principal())
        pc.get_entradas_y_salidas_entre(fechaini, 
            almacen = pclases.Almacen.select(orderBy = "-id")[0])
        """

        if not almacen:
            entradas = LineaDeCompra.select(""" 
                producto_compra_id = %d AND 
                albaran_entrada_id IN (SELECT albaran_entrada.id 
                                         FROM albaran_entrada 
                                        WHERE albaran_entrada.fecha >= '%s') 
                """ % (self.id, sqlfechaini))
            # Ahora también pueden entrar productos en albaranes de salida
            # procedentes de otro almacén.
            entradas2 = LineaDeVenta.select("""
                producto_compra_id = %d AND 
                albaran_salida_id IN (SELECT albaran_salida.id 
                                        FROM albaran_salida
                                       WHERE albaran_salida.fecha >= '%s'
                                         AND almacen_destino_id IS NOT NULL)
                """ % (self.id, sqlfechaini))
            if DEBUG:
                print " --> entradas:",entradas.count()," +",entradas2.count()
            entradas = SQLlist(SQLlist(entradas) + SQLlist(entradas2))
        else:
            entradas = LineaDeCompra.select(""" 
                producto_compra_id = %d AND 
                albaran_entrada_id IN (SELECT albaran_entrada.id 
                                         FROM albaran_entrada 
                                        WHERE albaran_entrada.fecha >= '%s'
                                          AND almacen_id = %d) 
                """ % (self.id, sqlfechaini, almacen.id))
            # Ahora también pueden entrar productos en albaranes de salida
            # procedentes de otro almacén.
            entradas2 = LineaDeVenta.select("""
                producto_compra_id = %d AND 
                albaran_salida_id IN (SELECT albaran_salida.id 
                                        FROM albaran_salida
                                       WHERE albaran_salida.fecha >= '%s'
                                         AND almacen_destino_id = %d)
                """ % (self.id, sqlfechaini, almacen.id))
            entradas = SQLlist(SQLlist(entradas) + SQLlist(entradas2))
            if DEBUG:
                print " --> entradas:",entradas.count(), "+", entradas2.count()
        if not almacen:
            salidas_consumos = SQLtuple([])
        else:
            if almacen is Almacen.get_almacen_principal_or_none():
                # Solo se puede consumir del almacén principal.
                salidas_consumos = SQLtuple([])
            else:
                salidas_consumos = SQLtuple([])
        if DEBUG:
            print " <-* consumos(prefilter):", salidas_consumos.count()
        # Ahora filtro para quitar los consumos que se han contado en 
        # albaranes internos. Esto va a ser lento y doloroso, peque...
        _salidas_consumos, salidas_consumos = salidas_consumos[:], []
        for c in _salidas_consumos:
            ldv = c.get_linea_de_venta_albaran_interno()
            if not ldv:
                salidas_consumos.append(c)
        salidas_consumos = SQLtuple(salidas_consumos)
        if DEBUG:
            print " <-- consumos:", salidas_consumos.count()
        if not almacen:
            salidas_albaranes = LineaDeVenta.select(""" 
                producto_compra_id = %d AND 
                albaran_salida_id IN (SELECT albaran_salida.id 
                                      FROM albaran_salida 
                                      WHERE albaran_salida.fecha >= '%s')
                """ % (self.id, sqlfechaini))
        else:
            salidas_albaranes = LineaDeVenta.select(""" 
                producto_compra_id = %d AND 
                albaran_salida_id IN (SELECT albaran_salida.id 
                                      FROM albaran_salida 
                                      WHERE albaran_salida.fecha >= '%s'
                                        AND almacen_origen_id = %d)
                """ % (self.id, sqlfechaini, almacen.id))
        if DEBUG:
            print " <-- salidas:", salidas_albaranes.count()
        return entradas, salidas_consumos, salidas_albaranes

    def __get_consultas_entradas_y_salidas_entre(self, 
                                                 sqlfechaini, 
                                                 sqlfechafin, 
                                                 almacen = None):
        """
        Devuelve tres ResultSelect de entradas, consumos y salidas del 
        producto de compra desde y hasta las fecha indicadas en formato 
        SQL (%Y-%m-%d).
        Si almacen != None, devuelve lo anterior pero solo para ese almacén.
        Dado que la mayoría de consumos también se contabilizan en un albarán 
        interno de consumo, no se devolverán los consumos que pertenezcan a un 
        parte que tenga albarán interno y éste una línea de venta con el 
        mismo producto y cantidad que el consumo.
        """
        if not almacen:
            entradas = LineaDeCompra.select(""" 
                producto_compra_id = %d AND 
                albaran_entrada_id IN (SELECT albaran_entrada.id 
                                       FROM albaran_entrada 
                                       WHERE albaran_entrada.fecha <= '%s'
                                       AND albaran_entrada.fecha >= '%s') 
                """ % (self.id, sqlfechafin, sqlfechaini))
            # Ahora también pueden entrar productos en albaranes de salida
            # procedentes de otro almacén.
            entradas2 = LineaDeVenta.select("""
                producto_compra_id = %d AND 
                albaran_salida_id IN (SELECT albaran_salida.id 
                                        FROM albaran_salida
                                       WHERE albaran_salida.fecha >= '%s'
                                         AND albaran_salida.fecha <= '%s'
                                         AND almacen_destino_id IS NOT NULL)
                """ % (self.id, sqlfechafin, sqlfechaini))
            entradas = SQLlist(SQLlist(entradas) + SQLlist(entradas2))
        else:
            entradas = LineaDeCompra.select(""" 
                producto_compra_id = %d AND 
                albaran_entrada_id IN (SELECT albaran_entrada.id 
                                       FROM albaran_entrada 
                                       WHERE albaran_entrada.fecha <= '%s'
                                       AND albaran_entrada.fecha >= '%s'
                                       AND almacen_id = %d) 
                """ % (self.id, sqlfechafin, sqlfechaini, almacen.id))
            # Ahora también pueden entrar productos en albaranes de salida
            # procedentes de otro almacén.
            entradas2 = LineaDeVenta.select("""
                producto_compra_id = %d AND 
                albaran_salida_id IN (SELECT albaran_salida.id 
                                        FROM albaran_salida
                                       WHERE albaran_salida.fecha >= '%s'
                                         AND albaran_salida.fecha <= '%s'
                                         AND almacen_destino_id = %d)
                """ % (self.id, sqlfechaini, sqlfechafin, almacen.id))
            entradas = SQLlist(SQLlist(entradas) + SQLlist(entradas2))
        if not almacen:
            salidas_consumos = SQLtuple([])
        else:
            if almacen is Almacen.get_almacen_principal_or_none():
                # Solo se puede consumir del almacén principal.
                salidas_consumos = SQLtuple([])
            else:
                salidas_consumos = SQLtuple([])
        # Ahora filtro para quitar los consumos que se han contado en 
        # albaranes internos. Esto va a ser lento y doloroso, peque...
        _salidas_consumos, salidas_consumos = salidas_consumos[:], []
        for c in _salidas_consumos:
            ldv = c.get_linea_de_venta_albaran_interno()
            if not ldv:
                salidas_consumos.append(c)
        salidas_consumos = SQLtuple(salidas_consumos)
        if not almacen:
            salidas_albaranes = LineaDeVenta.select(""" 
                producto_compra_id = %d AND 
                albaran_salida_id IN (SELECT albaran_salida.id 
                                      FROM albaran_salida 
                                      WHERE albaran_salida.fecha <= '%s'
                                      AND albaran_salida.fecha >= '%s')
                """ % (self.id, sqlfechafin, sqlfechaini))
        else:
            salidas_albaranes = LineaDeVenta.select(""" 
                producto_compra_id = %d AND 
                albaran_salida_id IN (SELECT albaran_salida.id 
                                      FROM albaran_salida 
                                      WHERE albaran_salida.fecha <= '%s'
                                      AND albaran_salida.fecha >= '%s' 
                                      AND almacen_origen_id = %d)
                """ % (self.id, sqlfechafin, sqlfechaini, almacen.id))
        return entradas, salidas_consumos, salidas_albaranes

    def get_entradas_y_salidas_entre(self, fechaini, fechafin = None, 
                                     almacen = None):
        """
        Devuelve la cantidad total (entradas - salidas) de entradas y salidas 
        del producto entre las fechas indicadas, AMBAS INCLUIDAS.
        Si la fecha final es None, no establece límite superior en la consulta.
        """
        qin = 0.0     # Quantity in
        qout = 0.0    # Quantity out
        # NOTA: No tiene en cuenta los partes por turno, solo por fecha 
        # "absoluta" (o días naturales, si después de 12 de la noche, es del 
        # día siguiente).
        sqlfechaini = fechaini.strftime("%Y-%m-%d")
        if fechafin != None:
            sqlfechafin = fechafin.strftime("%Y-%m-%d")
            entradas, salidas_consumos, salidas_albaranes \
                = self.__get_consultas_entradas_y_salidas_entre(sqlfechaini, 
                                                                sqlfechafin, 
                                                                almacen)
        else:
            entradas, salidas_consumos, salidas_albaranes \
                = self.__get_consultas_entradas_y_salidas_desde(sqlfechaini, 
                                                                almacen)
        if entradas.count() > 0:
            qin += entradas.sum("cantidad")
            if DEBUG:
                print "get_entradas_y_salidas_desde; qin:", qin
        if salidas_consumos.count() > 0:
            qout += salidas_consumos.sum("cantidad")
            if DEBUG:
                print "get_entradas_y_salidas_desde; qout:", qout
        if salidas_albaranes.count() > 0:
            qout += salidas_albaranes.sum("cantidad")
            if DEBUG:
                print "get_entradas_y_salidas_desde; qout:", qout
        return qin - qout

    def _muestrear_historicos(self):
        """
        Devuelve un diccionario de existencias del producto en los días 1 y 15 
        de los últimos 12 meses y las existencias actuales.
        """
        hoy = datetime.datetime.now()   # Hoy... que no es hoy. Dará las 
                    # existencias a las 00:00 de hoy, no en tiempo real.
        if hoy.day > 15:
            ultima = datetime.datetime(day = 15, 
                                              month = hoy.month, 
                                              year = hoy.year)
        else:
            ultima = datetime.datetime(day = 1, 
                                              month = hoy.month, 
                                              year = hoy.year)
        primera = datetime.datetime(day = ultima.day, 
                                           month = ultima.month, 
                                           year = ultima.year - 1)
        fechas = [primera, ]
        while fechas[-1] != ultima:
            if fechas[-1].month < 12:
                anno = fechas[-1].year
                mes = fechas[-1].month + 1
            else:
                anno = fechas[-1].year + 1
                mes = 1
            fechas.append(datetime.datetime(day = 1, 
                                                   month = mes, 
                                                   year = anno))
            fechas.append(datetime.datetime(day = 15, 
                                                   month = mes, 
                                                   year = anno))
        fechas.append(hoy)
        res = {}
        for fecha in fechas:
            res[fecha] = self.get_existencias_historico(fecha)
#            print "%s -> %s: %s" % (self.descripcion, fecha.strftime("%d/%m/%Y"), utils.float2str(res[fecha]))
#        print "          AHORA, EN TIEMPO REAL: %s" % (utils.float2str(self.existencias))
        return res

    def get_entradas(self, fechaini = None, fechafin = None):
        """
        Devuelve las entradas del producto, agrupadas por fecha y tal.
        El resultado es un diccionario tal que:
            {fecha: {'albaranes': {albaranEntrada: cantidad,... }, 'cantidad': 0}, ...}
        fechaini y fechafin, de recibirse, _deben ser_ fechas mx.DateTime.
        """
        res = {}
        if fechaini == None and fechafin == None:
            entradas = LineaDeCompra.select(""" producto_compra_id = %d AND 
                                                albaran_entrada_id IN (SELECT albaran_entrada.id 
                                                                       FROM albaran_entrada)""" % (self.id))
        elif fechaini == None and fechafin != None:
            sqlfechafin = fechafin.strftime("%Y-%m-%d")
            entradas = LineaDeCompra.select(""" producto_compra_id = %d AND 
                                                albaran_entrada_id IN (SELECT albaran_entrada.id 
                                                                       FROM albaran_entrada 
                                                                       WHERE albaran_entrada.fecha <= '%s') """ % (self.id, sqlfechafin))
        elif fechaini != None and fechafin == None:
            sqlfechaini = fechaini.strftime("%Y-%m-%d")
            entradas = LineaDeCompra.select(""" producto_compra_id = %d AND 
                                                albaran_entrada_id IN (SELECT albaran_entrada.id 
                                                                       FROM albaran_entrada 
                                                                       WHERE albaran_entrada.fecha >= '%s') """ % (self.id, sqlfechaini))
        else:
            sqlfechaini = fechaini.strftime("%Y-%m-%d")
            sqlfechafin = fechafin.strftime("%Y-%m-%d")
            entradas = LineaDeCompra.select(""" producto_compra_id = %d AND 
                                                albaran_entrada_id IN (SELECT albaran_entrada.id 
                                                                       FROM albaran_entrada 
                                                                       WHERE albaran_entrada.fecha >= '%s' 
                                                                        AND albaran_entrada.fecha <= '%s') """ % (self.id, 
                                                                                                                  sqlfechaini, 
                                                                                                                  sqlfechafin))
        for ldc in entradas:
            if ldc.albaranEntrada.fecha not in res:
                res[ldc.albaranEntrada.fecha] = {'albaranes': {ldc.albaranEntrada: ldc.cantidad}, 
                                  'cantidad': ldc.cantidad}
            else:
                if ldc.albaranEntrada not in res[ldc.albaranEntrada.fecha]['albaranes']:
                    res[ldc.albaranEntrada.fecha]['albaranes'][ldc.albaranEntrada] = ldc.cantidad
                else:
                    res[ldc.albaranEntrada.fecha]['albaranes'][ldc.albaranEntrada] += ldc.cantidad
                res[ldc.albaranEntrada.fecha]['cantidad'] += ldc.cantidad
        return res

    def get_salidas(self, fechaini = None, fechafin = None):
        """
        Devuelve las salidas del producto, agrupadas por fecha y tal.
        El resultado es un diccionario tal que:
            {fecha: {'partes': {ParteDeProduccion: cantidad, ... }, 
                     'albaranes': {AlbaranSalida: cantidad, ...}, 
                     'cantidad': 0}, ...}
        fechaini y fechafin, de recibirse, _deben ser_ fechas mx.DateTime.
        """
        res = {}
        if fechaini == None and fechafin == None:
            salidas = LineaDeVenta.select(""" 
                producto_compra_id = %d AND albaran_salida_id IS NOT NULL 
                """ % (self.id))
        elif fechaini == None and fechafin != None:
            sqlfechafin = fechafin.strftime("%Y-%m-%d")
            salidas = LineaDeVenta.select(""" 
                producto_compra_id = %d AND 
                albaran_salida_id IN (
                    SELECT albaran_salida.id 
                    FROM albaran_salida 
                    WHERE albaran_salida.fecha <= '%s')
                """ % (self.id, sqlfechafin))
        elif fechaini != None and fechafin == None:
            sqlfechaini = fechaini.strftime("%Y-%m-%d")
            salidas = LineaDeVenta.select(""" 
                producto_compra_id = %d AND 
                albaran_salida_id IN (
                    SELECT albaran_salida.id 
                    FROM albaran_salida 
                    WHERE albaran_salida.fecha >= '%s')
                """ % (self.id, sqlfechaini))
        else:
            sqlfechaini = fechaini.strftime("%Y-%m-%d")
            sqlfechafin = fechafin.strftime("%Y-%m-%d")
            salidas = LineaDeVenta.select(""" 
                producto_compra_id = %d AND 
                albaran_salida_id IN (SELECT albaran_salida.id 
                                      FROM albaran_salida 
                                      WHERE albaran_salida.fecha >= '%s' 
                                      AND albaran_salida.fecha <= '%s')
                """ % (self.id, sqlfechaini, sqlfechafin))
        for salida in salidas:
            fecha = salida.albaranSalida.fecha
            albaran = salida.albaranSalida
            cantidad = salida.cantidad
            if fecha not in res:
                res[fecha] = {'albaranes': {albaran: cantidad}, 
                              'partes': {}, 
                              'cantidad': cantidad}
            else:
                if albaran not in res[fecha]['albaranes']:
                    res[fecha]['albaranes'][albaran] = cantidad
                else:
                    res[fecha]['albaranes'][albaran] += cantidad
                res[fecha]['cantidad'] += cantidad
        return res

    def get_pendientes(self, fechainicio = None, fechafin = None):
        """
        Devuelve un diccionario de pedidos de compra y cantidad 
        pendiente de recibir del producto entre las fechas indicadas.
        {pedidoCompra: {'cantidad': cantidad_pendiente, 
                        'valor': cantidad_pendiente_valorada_en_euros}, ...}
        """
        if fechainicio == None and fechafin == None:
            pedidos = PedidoCompra.select(PedidoCompra.q.cerrado == False, 
                                          orderBy = "numpedido")
        elif fechainicio != None and fechafin == None:
            pedidos = PedidoCompra.select(
                        AND(PedidoCompra.q.fecha >= fechainicio, 
                            PedidoCompra.q.cerrado == False), 
                        orderBy = "numpedido")
        elif fechainicio == None and fechafin != None:
            pedidos = PedidoCompra.select(AND(PedidoCompra.q.fecha <= fechafin,
                                              PedidoCompra.q.cerrado == False),
                                          orderBy = "numpedido")
        else:
            pedidos=PedidoCompra.select(AND(PedidoCompra.q.fecha>=fechainicio, 
                                            PedidoCompra.q.fecha <= fechafin,
                                            PedidoCompra.q.cerrado == False),
                                          orderBy = "numpedido")
        pendiente = {}
        for pedido in pedidos:
            cantidad_pendiente, valor = pedido.get_pendiente(self)
            if cantidad_pendiente > 0:
                if pedido not in pendiente:
                    pendiente[pedido] = {'cantidad': cantidad_pendiente, 
                                         'valor': valor}
                else:
                    pendiente[pedido]['cantidad'] += cantidad_pendiente
                    pendiente[pedido]['valor'] += valor
        return pendiente

    def get_ultimo_precio(self):
        """
        Devuelve el precio al que se compró el producto 
        en el último pedido. Si el producto no tiene 
        pedidos, devuelve None.
        El precio que se tiene en cuenta es el de la línea 
        de compra en sí, no el de la línea de pedido; ya que 
        un producto se puede pedir a un precio y recibir 
        finalmente a otro. Este último precio es el precio 
        real al que se ha comprado y es el que se usará para
        valorar las existencias.
        """
        ultimo_precio = None
        consulta_ultimo_pedido = PedidoCompra.select(""" 
            id IN (SELECT pedido_compra_id 
                   FROM linea_de_compra 
                   WHERE linea_de_compra.producto_compra_id = %d)
                   ORDER BY fecha DESC """ % (self.id))
        try:
            ultimo_pedido = consulta_ultimo_pedido[0]
        except IndexError:
            ultimo_precio = None
        else:
            ultima_ldc = LineaDeCompra.select(AND(
                          LineaDeCompra.q.pedidoCompra == ultimo_pedido.id, 
                          LineaDeCompra.q.productoCompra == self.id))[0]
            ultimo_precio = ultima_ldc.precio
        return ultimo_precio
    
    def get_ultimo_precio_albaran(self):
        """
        Devuelve el precio al que se compró el producto 
        en el último ALBARÁN. Si el producto no tiene 
        pedidos, devuelve None.
        El precio que se tiene en cuenta es el de la línea 
        de compra en sí, no el de la línea de pedido; ya que 
        un producto se puede pedir a un precio y recibir 
        finalmente a otro. Este último precio es el precio 
        real al que se ha comprado y es el que se usará para
        valorar las existencias.
        """
        ultimo_precio = None
        consulta_ultimo_albaran = AlbaranEntrada.select(""" 
            id IN (SELECT albaran_entrada_id 
                   FROM linea_de_compra 
                   WHERE linea_de_compra.producto_compra_id = %d)
            ORDER BY fecha DESC """ % (self.id))
        try:
            ultimo_albaran = consulta_ultimo_albaran[0]
        except IndexError:
            ultimo_precio = None
        else:
            ultima_ldc = LineaDeCompra.select(AND(
                LineaDeCompra.q.albaranEntrada == ultimo_albaran.id, 
                LineaDeCompra.q.productoCompra == self.id))[0]
            ultimo_precio = ultima_ldc.precio
        return ultimo_precio

    def get_precio_medio(self, fechaini = None, fechafin = None):
        """
        Devuelve el precio medio del producto de compra 
        en función de las entradas del mismo 
        mediante albaranes. Devuelve None si 
        no ha habido entradas.
        Si fechainicio y fechafin son None, devuelve el 
        precio medio de todas las entradas. En otro caso 
        usa las entradas comprendidas entre ambas fechas.
        """
        entradas = self.get_entradas(fechaini, fechafin)
        stock_entradas = 0
        valoracion_entradas = 0
        for fecha in entradas:
            for albaran in entradas[fecha]['albaranes']:
                for ldc in albaran.lineasDeCompra:
                    if ldc.productoCompra == self:
                        stock_entradas += ldc.cantidad
                        valoracion_entradas += ldc.get_subtotal()
        try:
            precio_medio = valoracion_entradas / stock_entradas
        except ZeroDivisionError:
            precio_medio = None
        return precio_medio

    def __get_ldcs_entre(self, fechaini, fechafin):
        """
        Devuelve las LDCs entre las fechas indicadas.
        """
        ldcs = []
        for ldc in self.lineasDeCompra:
            if fechafin == None and fechaini == None:   # Todas las LDCS.
                ldcs.append(ldc)
            else:
                fechaldc = ldc.get_fecha_albaran()
                if fechafin == None and fechaini != None:   
                    # Posteriores a fechaini
                    if fechaini <= fechaldc:
                        ldcs.append(ldc)
                elif fechafin != None and fechaini == None: 
                    # Anteriores a fechafin
                    if fechafin >= fechaldc:
                        ldcs.append(ldc)
                elif fechafin != None and fechaini != None: 
                    # Entre fechaini y fechafin
                    if fechaini <= fechaldc <= fechafin:
                        ldcs.append(ldc)
        return ldcs

    def get_precio_valoracion(self, fechaini = None, fechafin = None):
        """
        Devuelve el precio con el que se valoran las 
        existencias del producto de compra.
        Wrapper al método que realmente lo calcula.
        NOTA: Actualmente se usa el precio medio de las entradas
        entre dos fechas.
        """
        precio = self.precioDefecto
        if (self.fvaloracion == "Función por defecto" 
            or self.fvaloracion == "Precio medio"):
            ldcs = self.__get_ldcs_entre(fechaini, fechafin)
            if ldcs != []:  # Si tiene entradas que evaluar: 
                precio = self.get_precio_medio(fechaini, fechafin)
        elif self.fvaloracion == "Precio último pedido":
            precio = self.get_ultimo_precio()
        elif self.fvaloracion == "Precio última entrada en almacén":
            precio = self.get_ultimo_precio_albaran()
        elif self.fvaloracion == "Usar precio por defecto especificado":
            precio = self.precioDefecto
        else:
            precio = None   
                # precio = None cuando no hay función de valoración 
                # especificada o cuando la misma no ha podido devolver un 
                # precio válido.
                # Acabará tomando un par de líneas más abajo el precio por 
                # defecto.
        if precio == None:
            precio = self.precioDefecto
        return precio

    def get_pedidos(self, proveedor = None):
        """
        Devuelve una tupla de objetos pedido donde se haya 
        pedido el producto del objeto. 
        Si proveedor != None filtra la lista para devolver 
        solo aquellos pedidos que se correspondan con el 
        proveedor recibido.
        NOTA: Tiene en cuenta tanto las LDC (líneas ya albaraneadas
        o facturadas) como las LDPC (líneas de pedido de compra en sí).
        OJO: Ya que convierte un SelectResult a tupla antes de devolver, 
        puede resultar algo lento si la lista de pedidos es grande.
        """
        consulta_sql = """ (id IN (SELECT pedido_compra_id 
                                   FROM linea_de_compra 
                                   WHERE producto_compra_id = %d)
                            OR id IN (SELECT pedido_compra_id
                                      FROM linea_de_pedido_de_compra 
                                      WHERE producto_compra_id = %d)) 
                       """ % (self.id, self.id)
        if proveedor != None:
            consulta_sql += " AND proveedor_id = %d " % (proveedor.id)
        pedidos = PedidoCompra.select(consulta_sql)
        return tuple(pedidos)
        
    def get_albaranes(self, proveedor = None):
        """
        Devuelve los albaranes relacionados con el producto de compra.
        Si proveedor no es None los filtra para devolver solo los de 
        ese proveedor.
        """
        consulta_sql=""" (id IN (SELECT albaran_entrada_id 
                                 FROM linea_de_compra 
                                 WHERE producto_compra_id = %d)) """%(self.id)
        if proveedor != None:
            consulta_sql += " AND proveedor_id = %d " % (proveedor.id)
        albaranes = AlbaranEntrada.select(consulta_sql)
        return tuple(albaranes)
    
    def get_facturas(self, proveedor = None):
        """
        Devuelve las facturas relacionadas con el producto de compra.
        Si el proveedor no es None, los filtra para devolver solo los 
        ese proveedor.
        """
        consulta_sql=""" (id IN (SELECT factura_compra_id 
                                 FROM linea_de_compra 
                                 WHERE producto_compra_id = %d)) """%(self.id)
        if proveedor != None:
            consulta_sql += " AND proveedor_id = %d " % (proveedor.id)
        facturas = FacturaCompra.select(consulta_sql)
        return tuple(facturas)

    def get_proveedores(self):
        """
        Devuelve una lista de proveedores que sirven el 
        producto actual a partir de facturas, albaranes y 
        pedidos sin orden concreto.
        OJO: Puede llegar a resultar MUY lento.
        """
        proveedores = []
        for pedido in self.get_pedidos():
            if (pedido.proveedorID != None 
                and pedido.proveedor not in proveedores):
                proveedores.append(pedido.proveedor)
        for albaran in self.get_albaranes():
            if (albaran.proveedorID != None 
                and albaran.proveedor not in proveedores):
                proveedores.append(albaran.proveedor)
        for factura in self.get_facturas():
            if (factura.proveedorID != None 
                and factura.proveedor not in proveedores):
                proveedores.append(factura.proveedor)
        return proveedores

    proveedores = property(get_proveedores, doc = "Proveedores relacionados "\
          "con el producto de compra mediante pedidos, albaranes o facturas.")

    def get_stock(self):
        """
        Devuelve las existencias.
        """
        return self.existencias

    def get_str_unidad_de_venta(self):
        return self.unidad

    def get_str_stock(self):
        """
        Devuelve las existencias como cadena con su unidad.
        """
        return (utils.float2str(self.get_stock(), autodec = True) 
                + " " + self.get_str_unidad_de_venta())

    def get_existencias(self, almacen = None):
        """
        Devuelve las existencias.
        Si almacen es None, devuelve el total.
        Si no, devuelve las existencias del almacén en concreto.
        OJO: No se asegura aquí que las existencias totales coincidan con 
        la suma de los almacenes.
        """
        # TODO: Para hacerlo compatible con los productos de venta, dejar 
        # que reciba una fecha y llamar a get_existencias_historico.
        if not almacen:
            res = self.existencias
        else:
            try:
                res = [sa.existencias 
                       for sa in self.stocksAlmacen 
                       if sa.almacen == almacen][0]
            except IndexError:
                res = 0
        return res

    def get_str_existencias(self):
        """
        Devuelve las existencias como cadena con su unidad.
        """
        return utils.float2str(self.get_existencias(), autodec = True) + " " + self.unidad

    def calcular_kilos(self):
        """
        Intenta determinar el peso en kg del producto buscando la palabra 
        "kilo", "litro" o "l." "l\0" y devolviendo el número justo a su 
        izquierda.
        Si no se puede determinar, devuelve None.
        OJO: Esta función puede quedar en desuso o ser sustituida por una 
        equivalente con el peso real. Por el momento el peso puede no ser 
        preciso (no hay propiedad en los objetos producto de compra que 
        indique el peso real y además se asume que la densidad de todos los 
        productos es la del agua 1 kg/l).
        """
        s = self.descripcion
        s = s.upper()
        divisor = 1.0
        if "K." in s:
            pos = s.rindex("K.")
        elif "KILO" in s:
            pos = s.rindex("KILO")
        elif "ML." in s:
            pos = s.rindex("ML.")
            divisor = 1000.0
        elif "ML," in s:
            pos = s.rindex("ML,")
            divisor = 1000.0
        elif s.strip().endswith("ML"):
            pos = s.rindex("ML")
            divisor = 1000.0
        elif "ML " in s:
            pos = s.rindex("ML ")
            divisor = 1000.0
        elif "L." in s:
            pos = s.rindex("L.")
        elif "L," in s:
            pos = s.rindex("L,")
        elif s.strip().endswith("L"):
            pos = s.rindex("L")
        elif "GR " in s:
            pos = s.rindex("GR ")
            divisor = 1000.0
        elif s.strip().endswith("GR"):
            pos = s.rindex("GR")
            divisor = 1000.0
        elif "GR." in s:
            pos = s.rindex("GR.")
            divisor = 1000.0
        else:
            pos = None
        res = None
        if pos:
            s = s[pos-1::-1]
            try:
                s = s.split()[0]
            except IndexError:
                pass
            nums = ""
            for l in s:
                if l in ("0123456789.,"):
                    nums += l
            try:
                res = utils._float(nums[::-1])
            except (ValueError, TypeError):
                res = None
            else:
                res /= divisor
        return res

    def add_existencias(self, 
                        cantidad, 
                        almacen = None, 
                        actualizar_global = False):
        """
        Incrementa las existencias del producto en el almacén «almacén» en la 
        cantidad recibida.
        Si no se recibe almacén se usa el almacén principal por defecto.
        Si actualizar_global es True cambia también las existencias totales 
        del producto.
        """
        if almacen == None:
            almacen = Almacen.get_almacen_principal()
        try:
            rstock = StockAlmacen.select(AND(
                StockAlmacen.q.productoCompra == self.id, 
                StockAlmacen.q.almacen == almacen.id))[0]
        except IndexError:
            rstock = StockAlmacen(productoCompra = self, 
                                  almacen = almacen, 
                                  existencias = 0)
        rstock.sync()
        rstock.existencias += cantidad
        rstock.syncUpdate()
        if actualizar_global: 
            self.sync()
            self.existencias += cantidad
            self.syncUpdate()

    def _unificar_historiales(self, d):
        """
        Une los históricos del objeto y d de forma coherente.
        1.- Crear una lista ordenada de fechas de ambos historiales.
        2.- Anotar existencias diferenciales de ambos.
        3.- Sumar las listas en el registro «o»
        4.- Eliminar los historialExistencias de «d».
        """
        fechas = []
        fechas1 = {}
        fechas2 = {}
        for h1 in self.historialesExistenciasCompra:
            fecha = h1.fecha
            if fecha not in fechas:
                fechas.append(fecha)
            try:
                fechas1[fecha][0] += h1.cantidad
                fechas1[fecha][1] += h1.observaciones
            except (KeyError, IndexError):
                fechas1[fecha] = [h1.cantidad, h1.observaciones]
        for h2 in d.historialesExistenciasCompra:
            fecha = h2.fecha
            if fecha not in fechas:
                fechas.append(fecha)
            try:
                fechas2[fecha][0] += h2.cantidad
                fechas2[fecha][1] += h2.observaciones
            except (KeyError, IndexError):
                fechas2[fecha] = [h2.cantidad, h2.observaciones]
        # Guardo las diferencias en lugar de cantidades absolutas.
        for f in (fechas1, fechas2):
            fechasdic = f.keys()
            fechasdic.sort()
            for i in range(1, len(fechasdic)):
                fecha = fechasdic[i]
                base = fechasdic[i-1]
                f[fecha][0] = f[fecha][0] - f[base][0]
        # Unifico en un nuevo diccionario:
        final = {}
        fechas.sort()
        for fecha in fechas:
            try:
                c1, o1 = fechas1[fecha]
            except (KeyError, IndexError):
                c1 = 0
                o1 = ""
            try:
                c2, o2 = fechas2[fecha]
            except (KeyError, IndexError):
                c2 = 0
                o2 = ""
            try:
                fecha_base = fechas[fechas.index(fecha)-1]
                base = final[fecha_base][0]
            except (KeyError, IndexError):
                base = 0
            final[fecha] = [base + c1 + c2, 
                            o1 + " " + o2 + 
                            " Registro unificado por duplicidad de producto."]
        # Elimino los registros existentes y creo los nuevos:
        for h in self.historialesExistenciasCompra + d.historialesExistenciasCompra:
            h.destroySelf()
        for fecha in final:
            h = pclases.HistorialExistenciasCompra(productoCompra = o, 
                                            cantidad = final[fecha][0], 
                                            observaciones = final[fecha][1], 
                                            fecha = fecha)

    def unificar_productos_compra(bueno, malos):
        """
        Unifica dos o más productos de compra. Pasa las existencias totales y 
        por almacén al producto "bueno" sumando las existencias de éste y de 
        todos los de la lista "malos". También combina los históricos de 
        existencias sumándolos.
        Acaba eliminando todos los productos de la lista "malos".
        """
        # Recuento existencias
        existencias = {}
        for a in Almacen.select():
            existencias[a] = 0.0
        for sa in bueno.stocksAlmacen:
            existencias[a] += sa.existencias
            sa.destroySelf()
        for malo in malos:
            for sa in malo.stocksAlmacen:
                if malo.controlExistencias:
                    existencias[a] += sa.existencias
                sa.destroySelf()
        if DEBUG:
            print "DEBUG: pclases.ProductoCompra.unificar_productos_compra ->"\
                  " Existencias:", existencias
        # Unifico historiales y aprovecho para eliminar tarifas de malos. No 
        # quiero que se dupliquen precios en «bueno».
        for malo in malos:
            if DEBUG:
                print "DEBUG: pclases.ProductoCompra.unificar_productos_"\
                      "compra -> Unificando historiales..."
            bueno._unificar_historiales(malo)
            for precio in malo.precios:     # Respeto la tarifa del bueno.
                precio.destroySelf()
        # Unifico resto de registros dependientes (pedidos, etc.)
        unificar(bueno, malos, borrar_despues = True)
        # Actualizo existencias.
        for a in existencias:
            if DEBUG:
                print "DEBUG: pclases.ProductoCompra.unificar_productos_"\
                      "compra ->"\
                      "\n  %d registros stockAlmacen."\
                      "\n  Creando nuevo registro de %s para %s..." % (
                        len(bueno.stocksAlmacen), existencias[a], a.nombre)
            StockAlmacen(productoCompra = bueno, 
                         almacen = a, 
                         existencias = existencias [a])
            if DEBUG: 
                print "\n  %d registros stockAlmacen"%len(bueno.stocksAlmacen)
        bueno.existencias = sum([sa.existencias for sa in bueno.stocksAlmacen])
        bueno.syncUpdate()

    unificar_productos_compra = staticmethod(unificar_productos_compra)

    def calcular_precio_medio_clase(self):
        """
        Calcula el precio MEDIO por clase de todo el producto para las cifras 
        del informe diario.
        """
        precios_clase = []
        for clase in self.clases:
            precio_clase_pax = clase.calcular_precio_clase_pax(
                tarifa = Tarifa.get_tarifa_defecto())
            if clase.numClasesMes:
                precios_clase += [precio_clase_pax] * clase.numClasesMes
            else:
                precios_clase += [precio_clase_pax] * clase.numClasesTotales
        try:
            res = sum(precios_clase) / len(precios_clase)
        except ZeroDivisionError:
            res = 0.0
        return res

class AlbaranEntrada(SQLObject, PRPCTOO):
    lineasDeCompra = MultipleJoin('LineaDeCompra')
    documentos = MultipleJoin('Documento')

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)
        
    def contar_lineas_facturadas(self):
        """
        Devuelve el número de líneas de venta del albarán 
        que ya han sido facturadas.
        """
        lineas_facturadas = [ldc for ldc in self.lineasDeCompra if ldc.facturaCompraID != None]
            # Acceder a ...ID es más rápido que acceder al objeto en sí, aunque sea solo para comparar si no es None.
        return len(lineas_facturadas)

    def get_facturas(self):
        """
        Devuelve una lista de objetos factura relacionados con el albarán.
        """
        facturas = []
        for ldc in self.lineasDeCompra:
            if ldc.facturaCompraID != None and ldc.facturaCompra not in facturas:
                facturas.append(ldc.facturaCompra)
        return facturas

    def get_pedidos(self):
        """
        Devuelve una lista de pedidos de compra relacionados con el albarán.
        """
        pedidos = []
        for ldc in self.lineasDeCompra:
            if ldc.pedidoCompraID != None and ldc.pedidoCompra not in pedidos:
                pedidos.append(ldc.pedidoCompra)
        return pedidos

    facturasCompra = property(get_facturas, doc = "Facturas relacionadas con el albarán de entrda.")
    pedidosCompra = property(get_pedidos, doc = 'Lista de objetos "pedido de compra" servidos en este albarán')


class PedidoVenta(SQLObject, PRPCTOO):
    lineasDeVenta = MultipleJoin('LineaDeVenta')
    lineasDePedido = MultipleJoin('LineaDePedido')
    servicios = MultipleJoin('Servicio')
    documentos = MultipleJoin('Documento')

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_info(self):
        if self.cliente:
            cliente = self.cliente.nombre
        else:
            cliente = "sin cliente"
        if self.cerrado:
            abierto = "Cerrado"
        else:
            abierto = "Abierto"
        if self.bloqueado:
            bloqueado = "bloqueado"
        else:
            bloqueado = "no bloqueado"
        return "Pedido %s (%s) de %s. %s y %s" % (self.numpedido, 
                                                  utils.str_fecha(self.fecha), 
                                                  cliente, 
                                                  abierto, 
                                                  bloqueado)

    def get_nombre_cliente(self):
        """
        Devuelve el nombre del cliente
        o '' si no tiene cliente asociado.
        """
        if self.cliente == None:
            return ''
        else:
            return self.cliente.nombre

    def calcular_importe_total(self, iva = True):
        """
        Devuelve el importe total del pedido (incluyendo IVA y demás).
        """
        total = 0.0
        for ldp in self.lineasDePedido:
            total += ldp.precio * (1 - ldp.descuento) * ldp.cantidad
        for srv in self.servicios:
            total += srv.get_subtotal()
        total -= total * self.descuento
        if iva:
            total *= (1 + self.iva)
        return total
    
    def ultimo_numpedido(clase):
        """
        Devuelve un ENTERO con el último número de albarán sin letras o 0 si 
        no hay ninguno o los que hay tienen caracteres alfanuméricos y no se 
        pueden pasar a entero.
        Para determinar el último número de albarán no se recorre toda la 
        tabla de pedidos intentando convertir a entero. Lo que se hace es 
        ordenar a la inversa por ID y comenzar a buscar el primer número de 
        pedido convertible a entero. 
        """
        # DONE: Además, esto debería ser un método de clase.
        import re
        regexp = re.compile("[0-9]*")
        ultimo = 0
        peds = clase.select(orderBy = '-id')
        for p in peds:
            try:
                numpedido = p.numpedido
                ultimo = [int(item) for item in regexp.findall(numpedido) 
                          if item != ''][0]
                break
            except (IndexError, ValueError), msg:
                print "pclases.py (ultimo_numpedido): Número de último pedido no se pudo determinar: %s" % (msg)
                # No se encontaron números en la cadena de numalbaran o ¿se 
                # encontró un número pero no se pudo parsear (!)?
                ultimo = 0
        return ultimo
    
    def siguiente_numpedido(clase):
        """
        Devuelve el siguiente número de pedido libre partiendo del último encontrado como entero.
        """
        ultimo = PedidoVenta.get_ultimo_numero_numpedido()
        while PedidoVenta.select(PedidoVenta.q.numpedido == str(ultimo + 1)).count() != 0:
            ultimo += 1
        return ultimo + 1

    get_ultimo_numero_numpedido = classmethod(ultimo_numpedido)
    get_siguiente_numero_numpedido = classmethod(siguiente_numpedido)

    def es_de_fibra(self):
        """
        Devuelve True si es un pedido únicamente de fibra. 
        Recalco: u-ni-ca-men-te.
        ¿No ha quedado claro?
        One more time: Debe tener al menos una LDP, y todas las que haya deben 
        tener relacionadas un pedido de venta que cumpla que 
        producto.es_fibra().
        """
        ldps = [ldp for ldp in self.lineasDePedido if ldp.producto.es_fibra()]
        return len(ldps) == len(self.lineasDePedido) >= 1

    def get_pendiente_servir(self):
        """
        Devuelve un diccionario de productos del pedido con la cantidad 
        servida y pedida, una lista de productos pendientes de servir y 
        una lista de servicios pendientes de servir.
        """
        productos = {}
        for ldp in self.lineasDePedido:
            producto = ldp.producto
            if producto not in productos:
                productos[producto] = {'servido': 0, 'pedido': 0}
            productos[producto]['pedido'] += ldp.cantidad
        for ldv in self.lineasDeVenta:
            producto = ldv.producto
            if producto not in productos:
                productos[producto] = {'servido': 0, 'pedido': 0}
            productos[producto]['servido'] += ldv.cantidad
        servicios_pendientes = [s for s in self.servicios 
                                if s.albaranSalida == None]
        productos_pendientes = [p for p in productos 
                        #if productos[p]['pedido'] != productos[p]['servido']]
                        if productos[p]['pedido'] > productos[p]['servido']]
        return productos, productos_pendientes, servicios_pendientes

    def get_pendiente_facturar(self):
        """
        Devuelve una lista de diccionarios de productos y otra de servicios 
        con lo pendiente de facturar del pedido actual, al precio de las 
        líneas de pedido y servicios, pero solo con la cantidad pendiente de 
        facturar.
        """
        # Primero los servicios, que es lo fácil.
        srvs = []
        for srv in self.servicios:
            if not srv.facturaVenta:
                srvs.append(srv)
        # Ahora los productos.
        productos = {}
        for ldp in self.lineasDePedido:
            producto = ldp.producto
            try:
                productos[producto]['pedido'] += ldp.cantidad
                productos[producto]['total_importe_sin_descuento'] +=\
                                            ldp.cantidad * ldp.precio
                productos[producto]['total_importe_con_descuento'] +=\
                                            ldp.cantidad * ldp.precio \
                                                * (1 - ldp.descuento)
                productos[producto]['notas'].append(ldp.notas)
                productos[producto]['textoEntrega'].append(ldp.textoEntrega)
                productos[producto]['fechaEntrega'].append(ldp.fechaEntrega)
            except KeyError:
                productos[producto] = {'pedido': ldp.cantidad, 
                                       'facturado': 0.0, 
                                       'precio': ldp.precio, 
                                       'descuento': ldp.descuento, 
                                       'notas': [ldp.notas], 
                                       'textoEntrega': [ldp.textoEntrega], 
                                       'fechaEntrega': [ldp.fechaEntrega], 
                                       'total_importe_sin_descuento': 
                                            ldp.cantidad * ldp.precio, 
                                       'total_importe_con_descuento': 
                                            ldp.cantidad * ldp.precio 
                                                * (1 - ldp.descuento)}
            # Y ahora cambiamos el precio por el precio medio y el descuento 
            # por el descuento medio que debería aplicarse para conservar el 
            # mismo total. Evidentemente si solo hay una LDP de ese producto, 
            # se quedarán los datos tal cual están.
            if (productos[producto]['pedido'] 
                * productos[producto]['precio'] 
                * productos[producto]['descuento'] 
                != productos[producto]['total_importe_con_descuento']):
                productos[producto]['precio'] = productos[producto]['total_importe_sin_descuento'] / productos[producto]['pedido']
                productos[producto]['descuento'] = 1 - (
                    (productos[producto]['total_importe_con_descuento'] 
                     / productos[producto]['total_importe_sin_descuento']))
        # Ahora actualizo las cantidades facturadas de los productos 
        # recorriendo las facturas del pedido de venta:
        for f in self.get_facturas():
            for ldv in f.lineasDeVenta:
                p = ldv.producto
                if p in productos:
                    productos[p]['facturado'] += ldv.cantidad
        # Aprovecho para limpiar los textos y fechas nulas.
        for p in productos:
            productos[p]['textoEntrega'] = [
                t for t in productos[p]['textoEntrega'] if t]
            productos[p]['fechaEntrega'] = [
                t for t in productos[p]['fechaEntrega'] if t]
        return productos, srvs

    def get_albaranes(self):
        """
        Devuelve los albaranes de salida relacionados con el pedido.
        """
        albaranes = []
        for ldv in self.lineasDeVenta:
            a = ldv.albaranSalida
            if a not in albaranes:
                albaranes.append(a)
        for srv in self.servicios:
            a = srv.albaranSalida
            if a not in albaranes:
                albaranes.append(a)
        return tuple(albaranes)

    def get_facturas(self):
        """
        Devuelve las facturas relacionadas con el pedido actual a través de 
        sus albaranes de salida.
        """
        facturas = []
        for a in self.get_albaranes():
            if not a:
                continue
            for f in a.get_facturas():
                if f not in facturas:
                    facturas.append(f)
        return facturas

class Presupuesto(SQLObject, PRPCTOO):
    lineasDePedido = MultipleJoin('LineaDePedido')
    servicios = MultipleJoin('Servicio')

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_pedidos(self):
        """
        Devuelve los pedidos relacionados con el presupuesto 
        a través de sus líneas de pedido y servicios.
        """
        pedidos = []
        for ldp in self.lineasDePedido:
            ldppedidoVenta = ldp.pedidoVenta
            if ldppedidoVenta != None and ldppedidoVenta not in pedidos:
                pedidos.append(ldppedidoVenta)
        for srv in self.servicios:
            srvpedidoVenta = srv.pedidoVenta
            if srvpedidoVenta != None and srvpedidoVenta not in pedidos:
                pedidos.append(srvpedidoVenta)
        return pedidos

    def calcular_total(self):
        """
        Calcula el total del presupuesto, con IVA y demás incluido.
        Devuelve un FixedPoint (a casi todos los efectos, se comporta como 
        un FLOAT.
        De todas formas, pasa bien por el utils.float2str).
        """
        subtotal = self.calcular_subtotal() 
        tot_iva = self.calcular_total_iva(subtotal)
        irpf = self.calcular_total_irpf(subtotal)
        total = subtotal + tot_iva + irpf
        return total
    
    def calcular_importe_total(self):
        """
        Calcula y devuelve el importe total, incluyendo IVA, de la factura.
        """
        return self.calcular_total()

    importeTotal = property(calcular_importe_total, doc = calcular_importe_total.__doc__)

    def calcular_total_iva(self, subtotal = None):
        """
        Calcula el importe total de IVA del presupuesto.
        """
        if subtotal == None:
            subtotal = self.calcular_subtotal()
        try:
            dde = DatosDeLaEmpresa.select()[0]
            iva = dde.iva
        except IndexError:
            iva = 0.18
        total_iva = utils.ffloat(subtotal) * iva 
        return total_iva
    
    def calcular_total_irpf(self, subtotal = None):
        """
        Calcula el importe total de retención de IRPF (se resta al total)
        del presupuesto.
        """
        if subtotal == None:
            subtotal = self.calcular_subtotal()
        try:
            dde = DatosDeLaEmpresa.select()[0]
            irpf = dde.irpf
        except IndexError:
            irpf = 0.0
        total_irpf = utils.ffloat(subtotal) * irpf
        return total_irpf

    def calcular_subtotal(self, incluir_descuento = True):
        """
        Devuelve el subtotal del presupuesto: líneas 
        de pedido + servicios - descuento.
        No cuenta IVA.
        """
        total_ldvs = sum([utils.ffloat((l.cantidad * l.precio) * (1 - l.descuento)) for l in self.lineasDePedido])
        total_srvs = sum([utils.ffloat((s.precio * s.cantidad) * (1 - s.descuento)) for s in self.servicios])
        subtotal = total_ldvs + total_srvs
        if incluir_descuento:
            subtotal *= 1 - self.descuento
        return subtotal

    def calcular_base_imponible(self):
        """
        Devuelve la suma de conceptos con el descuento global por defecto.
        """
        return self.calcular_subtotal(incluir_descuento = True)

    def calcular_fecha_limite(self):
        """
        Calcula y deuelve la fecha límite de validez del presupuesto.
        El periodo de validez es en meses, de modo que no soy estricto con los 
        días; y si cae en final de mes, por ejemplo, y el mes siguiente no 
        tiene los mismos días, bajo hasta el último día del mes, no lo paso 
        al 1 del siguiente para respetar el "sentido" de la validez en meses.
        """
        fecha_limite = fecha = self.fecha
        mes_fecha = fecha.month
        anno_fecha = fecha.year
        mes_limite = mes_fecha + self.validez
        anno_limite = anno_fecha + ((mes_limite) / 13)
        if mes_limite > 12:
            mes_limite %= 12
        dia = fecha.day
        while dia > 0:
            # Usando «dia» como variable de control evito por un lado el 
            # bucle infinito y por otro que se intente crear fechas con 
            # días negativos (que según qué versión de MX es posible, pero 
            # no me es útil en este caso).
            try:
                fecha_limite = datetime.datetime(day = dia, 
                                                        month = mes_limite, 
                                                        year = anno_limite)
                break
            except ValueError:  # Día fuera de rango
                dia -= 1
        return fecha_limite

    def esta_vigente(self):
        """
        Devuelve True si la validez del presupuesto es 0 o la fecha actual 
        es inferior o igual a la fecha del presupuesto + «validez» meses.
        """
        hoy = datetime.datetime.now()
        fecha_limite = self.calcular_fecha_limite()
        return (not self.validez) or hoy <= fecha_limite

class StockAlmacen(SQLObject, PRPCTOO):

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

class AlbaranSalida(SQLObject, PRPCTOO):
    lineasDeVenta = MultipleJoin('LineaDeVenta')
    servicios = MultipleJoin('Servicio')
    transportesACuenta = MultipleJoin('TransporteACuenta')
    documentos = MultipleJoin('Documento')

    str_tipos = ("Movimiento", "Interno", "Normal", "Repuestos", "Vacío")
    MOVIMIENTO, INTERNO, NORMAL, REPUESTOS, VACIO = range(len(str_tipos))

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)
        # XXX HACK: Terrible chapu.
        self.articulos = []

    def get_pedidos(self):
        """
        Devuelve una lista de pedidos relacionados con el albarán actual.
        """
        res = []
        for ldv in self.lineasDeVenta:
            pedido = ldv.pedidoVenta
            if pedido not in res:
                res.append(pedido)
        for srv in self.servicios:
            pedido = srv.pedidoVenta
            if pedido not in res:
                res.append(pedido)
        return res

    def es_de_repuestos(self):
        """
        Devuelve True si es un albarán de repuestos. 
        Para ello debe cumplir que:
        1.- El cliente sea la propia empresa.
        2.- Contiene en las observaciones el texto "repuestos".
        """
        # TODO: Esto se convertirá en un boolean en la tabla cuando 
        #       se pruebe a fondo.
        res = False
        idPropiaEmpresa = id_propia_empresa_cliente()
        if idPropiaEmpresa != 0:
            res = self.cliente == idPropiaEmpresa
            if res:
                res = "repuestos" in self.observaciones.lower()
        return res

    def es_de_movimiento(self):
        """
        Devuelve True si es un albarán de movimiento de mercancías entre 
        almacenes.
        Para ello debe cumplir que:
        1.- Tenga almacén origen instanciado (por defecto, siempre lo estará).
        2.- Tenga almacén destino instanciado.
        NOTA: Un albarán puede ser interno y de movimiento a la vez. De hecho 
        será lo normal, aunque se verifique las condiciones independientemente.
        """
        return bool(self.almacenOrigen and self.almacenDestino)

    def es_interno(self):
        """
        Devuelve si es un albarán interno de consumo de materiales o de fibra.
        No devuelve True si es un albarán de ajuste aunque el cliente sea la 
        propia empresa.
        Es fundamental que no esté vacío para poder determinar si es interno.
        """
        res = sqlhub.getConnection().queryOne(
            "SELECT es_interno(%d);" % self.id)[0] == 1
        return res

    def comprobar_cantidades(self):
        """
        Devuelve True si las cantidades de las líneas de venta coinciden 
        con las de los artículos del albarán para todos los productos 
        del albarán agrupables en objetos Articulo.
        """
        prods_ldvs = {}
        prods_arts = {}
        # Suma de cantidades de LDVs.
        for ldv in self.lineasDeVenta:
            pv = ldv.productoVenta
            if pv != None and (pv.es_bala() or pv.es_bala_cable() 
                or pv.es_bigbag() or pv.es_rollo() or pv.es_caja()):
                if pv not in prods_ldvs:
                    prods_ldvs[pv] = ldv.cantidad
                else:
                    prods_ldvs[pv] += ldv.cantidad
        # Suma de cantidades de artículos.
        for a in self.articulos + [ldd.articulo for ldd 
                                    in self.lineasDeDevolucion]:
            pv = a.productoVenta
            if a.es_rollo() or a.es_rollo_defectuoso():
                cantidad = a.superficie
            elif (a.es_bala() or a.es_bala_cable() or a.es_bigbag() 
                  or a.es_caja()):
                cantidad = a.peso
            else:
                print "pclases::AlbaranSalida::comprobar_cantidades -> El artículo ID %d no es bala [cable], ni bigbag ni caja ni rollo [defectuoso]." % (a.id)
                cantidad = 0
            if pv not in prods_arts:
                prods_arts[pv] = cantidad
            else:
                prods_arts[pv] += cantidad
        # Comprobación
        res = len(prods_arts) == len(prods_ldvs)
        for pv in prods_ldvs:
            if not res:
                break   # Ahorro iteraciones
            if pv not in prods_arts:
                res = False
            else:
                res = round(prods_arts[pv], 2) == round(prods_ldvs[pv], 2)
        if DEBUG and not res:
            print "prods_arts", prods_arts
            print "prods_ldvs", prods_ldvs
        return res

    def calcular_total(self, iva_incluido = False):
        """
        Devuelve el total del albarán basándose en la cantidad y 
        precios de la LDV.
        El total no incluye IVA a no ser que se indique lo contrario.
        """
        subtotal = 0
        for ldv in self.lineasDeVenta:
            subtotal += ldv.precio * ldv.cantidad * (1 - ldv.descuento)
        for srv in self.servicios:
            subtotal += srv.precio * srv.cantidad * (1 - srv.descuento)
        if iva_incluido:
            iva = self.cliente and self.cliente.get_iva_norm() or 0
        else:
            iva = 0
        total = subtotal * (1 + iva)
        return total

    def _buscar_ldv(self, d, codigo, cantidad):
        """
        Busca en el diccionario d, la clave cuyo valor (que es otro 
        diccionario) contiene el código c en el campo 'codigo' Y la
        cantidad de la LDV sea superior a la cantidad ya añadida (es
        otro campo del diccionario que hace de valor del primer 
        diccionario) más la que se quiere añadir -cant-.
        Si no se encuentra una LDV donde la cantidad sea superior o 
        igual, devolverá cualquiera de las LDV donde coincida el 
        código, aunque después al añadir se sobrepase la cantidad.
        Suena lioso... pero no lo es... ¿o sí? Que va, viendo el 
        código se ve muy claro.
        Devuelve la clave o None si no se encontró.
        """
        # print d
        # print codigo
        # print cantidad
        res = None
        for idldv in d:
            # XXX
            # if idldv == 0: return None
            # XXX
            if d[idldv]['codigo'] == codigo:
                res = idldv
                if d[idldv]['cantidad'] + cantidad <= d[idldv]['ldv'].cantidad:
                    res = idldv
                    break
        return res

    def agrupar_articulos(self):
        """
        Devuelve un diccionario cuyas claves son un ID de línea de venta
        los valores son listas de articulos del producto de la LDV.
        No se permite que un mismo artículo se relacione con dos LDVs
        distintas.
        Si la cantidad de los artículos (en m2, kilos, etc...) supera
        de la LDV donde se quiere añadir, se intentará añadir a otra
        LDV del mismo producto. Si no hay más LDV, se añadirá a la 
        LDV que haya.
        NOTA: Este método es casi calcado al de la ventana de albaranes 
        de salida. El único motivo por el cual se mantienen los dos es 
        porque allí se muestra una ventana de mensaje de error en 
        un caso concreto, que obligatoriamente necesita que la ventana 
        padre esté cargada. En un futuro se modificará para usar 
        únicamente este método y devolver un código de error para 
        poder mostrar el diálogo correspondiente en lugar de hacerlo 
        desde el propio procedimiento.
        NOTA 2: Modificado para que sea determinista (un mismo artículo 
        siempre debe pertenecer a una misma LDV a no ser que cambien 
        las condiciones iniciales). Se ha hecho simplemente ordenando 
        por ID (de otro modo, modificar un simple descuento en una LDV 
        podía moverla al final de la lista y devolver otros artículos 
        en la llamada anterior y posterior a la modificación. 
        """
        if DEBUG:
            import time
            antes = time.time()
            print "Soy agrupar artículos. T0 =", antes 
        # Creo un diccionario con todas las LDVs. Dentro del diccionario irá
        # un campo 'codigo' con el código del producto de la LDV, un 'articulos'
        # con una lista de artículos relacionados a la LDV, un 'cantidad' con 
        # la cantidad añadida y un 'ldv' con el objeto LDV.
        d = {}
        for ldv in self.lineasDeVenta:
            d[ldv.id] = {'codigo': ldv.producto.codigo, 'articulos': [], 
                         'cantidad' : 0.0, 'ldv': ldv, 'idsarticulos': []}
        # for a in self.articulos:    
        # CWT: Hay que contar también con las devoluciones como parte del 
        # albarán. Aunque se hayan devuelto. No importa. Al imprimir el 
        # albarán DEBEN VOLVER A APARECER AHí. Porque sí, porque... porque 
        # sí, y... ¡se sienten coño! 
        # NOTA: OJO: CUIDADÍN: Si no se usa con cuidado es posible que surjan 
        # descuadres si se considera que todos los artículos devueltos en el 
        # diccionario no están en el almacén.
        #articulos = self.articulos[:]
        articulos = []
        devoluciones = [ldd.articulo for ldd in self.lineasDeDevolucion][:]
        #transferencias = [ldm.articulo for ldm in self.lineasDeMovimiento][:]
        transferencias = []
        articulos.sort(lambda x, y: int(x.id - y.id))
        devoluciones.sort(lambda x, y: int(x.id - y.id))
        transferencias.sort(lambda x, y: int(x.id - y.id))
        for a in utils.unificar(articulos + devoluciones + transferencias):
            codigo = a.productoVenta.codigo
            # OJO: NO deberían haber artículos de productos que no se han 
            # pedido. O al menos no deberían haber artículos sin LDV (aunque 
            # la LDV no tenga pedido asignado).
            idldv = self._buscar_ldv(d, codigo, a.get_cantidad())
            if idldv == None:
                print >> sys.stderr, "WARNING(1)::pclases.py::AlbaranSalida: No hay línea de venta para el artículo con id %d." % (a.id)
                print >> sys.stderr, "WARNING(2)::pclases.py::AlbaranSalida: Creando línea de venta sin pedido."
                ldv = LineaDeVenta(pedidoVenta = None, 
                                   facturaVenta = None, 
                                   productoVenta = a.productoVenta, 
                                   albaranSalida = self, 
                                   cantidad = 0)
                idldv = ldv.id
                d[idldv] = {'codigo': ldv.producto.codigo, 'articulos': [], 
                            'cantidad' : 0.0, 'ldv': ldv, 'idsarticulos': []}
                print >> sys.stderr, "WARNING(3)::pclases.py::AlbaranSalida: Línea de venta con id %d creada." % (idldv)
            # idldv NO debería ser None. Si lo es, algo grave pasa; prefiero que salte la excepción.
            d[idldv]['articulos'].append(a)
            d[idldv]['idsarticulos'].append(a.id)
            d[idldv]['cantidad'] += a.get_cantidad()
        if DEBUG:
            import time
            print "Soy agrupar artículos. T1 - T0=", time.time() - antes 
        return d

    def contar_lineas_facturadas(self):
        """
        Devuelve el número de líneas de venta del albarán 
        que ya han sido facturadas.
        """
        lineas_facturadas = [ldv for ldv in self.lineasDeVenta if ldv.facturaVentaID != None or ldv.prefacturaID != None]
            # Acceder a ...ID es más rápido que acceder al objeto en sí, aunque sea solo para comparar si no es None.
        return len(lineas_facturadas)

    def get_facturas(self):
        """
        Devuelve una lista de objetos factura relacionados con el albarán.
        """
        facturas = []
        for ldv in self.lineasDeVenta:
            if ldv.facturaVentaID != None and ldv.facturaVenta not in facturas:
                facturas.append(ldv.facturaVenta)
            elif ldv.prefacturaID != None and ldv.prefactura not in facturas:
                facturas.append(ldv.prefactura)
        for srv in self.servicios:
            if srv.facturaVentaID != None and srv.facturaVenta not in facturas:
                facturas.append(srv.facturaVenta)
            elif srv.prefacturaID != None and srv.prefactura not in facturas:
                facturas.append(srv.prefactura)
        return facturas
    
    def ultimo_numalbaran(clase):
        """
        Devuelve un ENTERO con el último número de albarán sin letras o 0 si 
        no hay ninguno o los que hay tienen caracteres alfanuméricos y no se 
        pueden pasar a entero.
        Para determinar el último número de albarán no se recorre toda la 
        tabla de albaranes intentando convertir a entero. Lo que se hace es 
        ordenar a la inversa por ID y comenzar a buscar el primer número de 
        albarán convertible a entero. Como hay una restricción para crear 
        albaranes, es de suponer que siempre se va a encontrar el número más 
        alto al principio de la lista orderBy="-id".
        OJO: Aquí los números son secuenciales y no se reinicia en cada año 
        (que es como se está haciendo ahora en facturas).
        """
        # DONE: Además, esto debería ser un método de clase.
        import re
        regexp = re.compile("[0-9]*")
        ultimo = 0
        # albs = AlbaranSalida.select(orderBy = '-numalbaran')       # No, porque A_AJUSTE se colocaría el primero a tratar.
        albs = clase.select(orderBy = '-id')
        for a in albs:
            try:
                numalbaran = a.numalbaran
                ultimo = [int(item) for item in regexp.findall(numalbaran) if item != ''][0]
                # ultimo = int(numalbaran)
                break
            except (IndexError, ValueError), msg:
                print "pclases.py (ultimo_numalbaran): Número de último albarán no se pudo determinar: %s" % (msg)
                # No se encontaron números en la cadena de numalbaran o ¿se encontró un número pero no se pudo parsear (!)?
                ultimo = 0
        return ultimo

    def siguiente_numalbaran(clase):
        """
        Devuelve un ENTERO con el siguiente número de albarán sin letras o 0 
        si no hay ninguno o los que hay tienen caracteres alfanuméricos y no 
        se pueden pasar a entero.
        OJO: Aquí los números son secuenciales y no se reinicia en cada año 
        (que es como se está haciendo ahora en facturas).
        """
        return AlbaranSalida.get_ultimo_numero_numalbaran() + 1

    def get_num_numalbaran(self):
        """
        Devuelve el número de albarán como entero.
        Hasta ahora se han usado números solo o año y número, por lo que 
        el número en sí será el último entero encontrado.
        """
        import re
        rexp = re.compile("\d+")
        nums = rexp.findall(self.numalbaran)
        return int(nums[-1])

    def siguiente_numalbaran_str(clase):
        """
        Devuelve el siguiente número de albarán libre como cadena intentando 
        respetar el formato del último numalbaran.
        """
        import re
        regexp = re.compile("[0-9]*")
        ultimo = None
        albs = clase.select(orderBy = '-id')
        for a in albs:
            try:
                numalbaran = a.numalbaran
                ultimo = [int(item) for item in regexp.findall(numalbaran) if item != ''][-1]
                break
            except (IndexError, ValueError), msg:
                print "pclases.py (siguiente_numalbaran_str): Número de último albarán no se pudo determinar: %s" % (msg)
                # No se encontaron números en la cadena de numalbaran o ¿se encontró un número pero no se pudo parsear (!)?
                ultimo = ""
        if ultimo != "" and ultimo != None:
            head = numalbaran[:numalbaran.rindex(str(ultimo))]
            tail = numalbaran[numalbaran.rindex(str(ultimo)) + len(str(ultimo)):]
            str_ultimo = str(ultimo + 1)
            res = head + str_ultimo + tail
            while AlbaranSalida.select(AlbaranSalida.q.numalbaran == res).count() != 0:
                ultimo += 1
                str_ultimo = str(ultimo + 1)
                res = head + str_ultimo + tail
        else:
            res = 0
        if not isinstance(res, str):
            res = str(res)
        return res

    get_ultimo_numero_numalbaran = classmethod(ultimo_numalbaran)
    get_siguiente_numero_numalbaran = classmethod(siguiente_numalbaran)
    get_siguiente_numero_numalbaran_str = classmethod(siguiente_numalbaran_str)

    def get_str_tipo(self):
        """
        Devuelve una cadena en castellano con el tipo de albarán de salida:
            - Movimiento (si es de movimiento de mercancía entre almacenes).
            - Repuestos (si es albarán de repuestos).
            - Interno (si cliente es propia empresa).
            [- Ajuste (PLAN: No sé si incluir los albaranes de ajuste como un 
                       tipo de albarán por derecho propio).]
            - Salida (normal, no movimiento ni interno).
            - Vacío (si no tiene ninguna línea de venta ni nada asociado).
        Las condiciones se chequean en este orden. Esto es importante porque 
        un albarán de movimiento generalmente también será interno.
        """
        if self.esta_vacio():
            return AlbaranSalida.str_tipos[AlbaranSalida.VACIO]
        if self.es_interno():
            return AlbaranSalida.str_tipos[AlbaranSalida.INTERNO]
        if self.es_de_repuestos():
            return AlbaranSalida.str_tipos[AlbaranSalida.REPUESTOS]
        if self.es_de_movimiento():
            return AlbaranSalida.str_tipos[AlbaranSalida.MOVIMIENTO]
        return AlbaranSalida.str_tipos[AlbaranSalida.NORMAL]

    def esta_vacio(self):
        """
        Devuelve True si el albarán no tiene registrado nada. Ni líneas de 
        venta, ni artículos ni servicios. No miro las devoluciones. De todas 
        formas, si tiene devoluciones también tiene LDVs, que sí que se mira.
        """
        return (not self.lineasDeVenta 
                and not self.servicios)

    def get_info(self):
        """
        Muestra número de albarán, fecha, cliente y tipo: interno, 
        movimiento o salida.
        """
        return "Albarán %s. Fecha: %s. Cliente: %s. Tipo: %s" % (
            self.numalbaran, 
            utils.str_fecha(self.fecha), 
            self.clienteID and self.cliente.nombre or "", 
            self.get_str_tipo())

class Cliente(SQLObject, PRPCTOO):
    pedidosVenta = MultipleJoin('PedidoVenta')
    albaranesSalida = MultipleJoin('AlbaranSalida')
    facturasVenta = MultipleJoin('FacturaVenta')
    presupuestos = MultipleJoin('Presupuesto')
    cuentasBancariasCliente = MultipleJoin('CuentaBancariaCliente')
    documentos = MultipleJoin('Documento')
    prefacturas = MultipleJoin('Prefactura')
    padecimientos = MultipleJoin('Padecimiento')
    gruposAlumnos = RelatedJoin('GrupoAlumnos')
    asistencias = MultipleJoin("Asistencia")
    actividades = RelatedJoin('Actividad')
    productosContratados = MultipleJoin("ProductoContratado")
    fotos = MultipleJoin("Foto")
    
    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_info(self):
        cad = "%s (CIF %s)" % (self.nombre, self.cif)
        return cad

    def get_texto_forma_cobro(self):
        """
        Devuelve un texto que representa la forma de cobro del cliente. 
        Por ejemplo:  efectivo, pagaré 90 D.F.F., transferencia banco 1234-23-...
        """
        formapago = ""
        if self.documentodepago != None and self.documentodepago.strip() != "" and self.documentodepago.strip() != "0":
            formapago = "%s, " % (self.documentodepago)
        if self.vencimientos != None and self.vencimientos.strip() != "" and self.vencimientos.strip() != "0":
            formapago += "%s " % (self.vencimientos)
        if self.diadepago != None and self.diadepago.strip() != "" and self.diadepago.strip() != "-":
            formapago += "los días %s" % (self.diadepago)
        if len(formapago) > 0:
            formapago += ". "
        return formapago

    textoformacobro = property(get_texto_forma_cobro)

    def get_iva_norm(self):
        """
        Devuelve el iva normalizado (i.e. como fracción de 1) 
        del cliente.
        NOTAS: Temporal hasta que el IVA de la BD se guarde correctamente 
        y corrija las funciones donde se usa.
        """
        if self.iva == None:
            # Aprovecho para quitar los Nones del IVA de los clientes.
            self.iva = 0.18 
        iva = self.iva
        if iva > 1:
            iva /= 100.0
        return iva

    def get_vencimientos(self, fecha_base = datetime.datetime.now()):
        """
        Devuelve una lista con los días naturales de los vencimientos
        del cliente. P. ej.:
        - Si el cliente tiene "30", devuelve [30].
        - Si no tiene, devuelve [].
        - Si tiene "30-60", devuelve [30, 60].
        - Si tiene "90 D.F.F." (90 días a partir de fecha factura), devuelve 
          [90].
        - Si tiene "30-120 D.R.F." (30 y 120 días a partir de fecha de 
          recepción de factura) devuelve [30, 120].
        etc.
        - ¡NUEVO! Si tiene "120 D.U.D.M.F.F." (120 días a contar a partir del 
          último día del mes de la fecha de factura) devuelve 120 + los días 
          que haya entre la fecha «fecha_base» y el fin de mes, con objeto de 
          que sean sumados a la fecha de factura desde la ventana que me 
          invoca.
        En definitiva, filtra todo el texto y devuelve los números que 
        encuentre en cliente.vencimientos. Si los vencimientos es una cadena 
        vacía devuelve el valor por defecto «[0]» (a la fecha de factura).
        """
        res = []
        if self.vencimientos != None:
            if self.vencimientos.strip() == "":
                res = [0]
            else:
                import re
                regexpcars = re.compile("\w")
                cadena = "".join(regexpcars.findall(self.vencimientos)).upper()
                regexpr = re.compile("\d*")
                lista_vtos = regexpr.findall(self.vencimientos)
                if "UDM" in cadena:
                    try:
                        findemes = datetime.datetime(day = -1, 
                                                     month = fecha_base.month, 
                                                     year = fecha_base.year)
                    except Exception, msg:
                        print "ERROR: pclases::Cliente::get_vencimientos() ->"\
                              " Exception: %s" % (msg)
                        difafindemes = 0
                    else:
                        difafindemes = findemes.day - fecha_base.day
                else:
                    difafindemes = 0
                try:
                    res = [int(i) + difafindemes for i in lista_vtos if i != '']
                except TypeError, msg:
                    print "ERROR: pclases::Cliente::get_vencimientos() -> "\
                          "TypeError: %s" % (msg)
        return res

    def get_dias_de_pago(self):
        """
        Devuelve UNA TUPLA con los días de pago del cliente (vacía si no tiene).
        """
        res = []
        if self.diadepago != None:
            import re
            regexpr = re.compile("\d*")
            lista_dias = regexpr.findall(self.diadepago)
            try:
                res = tuple([int(i) for i in lista_dias if i != ''])
            except TypeError, msg:
                print "ERROR: pclases: cliente.get_dias_de_pago(): %s" % (msg)
        return res

    def es_extranjero(self):
        """
        Devuelve True si el cliente es extranjero.
        Para ello mira si el país del cliente es diferente al 
        de la empresa. Si no se encuentran datos de la empresa
        devuelve True si el país no es España.
        """
        cpf = unicode(self.paisfacturacion.strip())
        try:
            de = DatosDeLaEmpresa.select()[0]
            depf = unicode(de.paisfacturacion.strip())
            res = cpf != "" and depf.lower() != cpf.lower()
        except IndexError:
            res = cpf != "" and cpf.lower() != unicode("españa")
        return res

    extranjero = property(es_extranjero)
    
    def get_facturas(self, fechaini = None, fechafin = None):
        """
        Devuelve las facturas del cliente entre las dos 
        fechas recibidas (incluidas). Si ambas son None no 
        aplicará rango de fecha en la búsqueda.
        """
        criterio = (FacturaVenta.q.cliente == self.id)
        criteriopre = (Prefactura.q.cliente == self.id)
        if fechaini != None:
            criterio = AND(criterio, FacturaVenta.q.fecha >= fechaini)
            criteriopre = AND(criteriopre, Prefactura.q.fecha >= fechaini)
        if fechafin != None:
            criterio = AND(criterio, FacturaVenta.q.fecha <= fechafin)
            criteriopre = AND(criteriopre, Prefactura.q.fecha >= fechaini)
        return [f for f in FacturaVenta.select(criterio)] + [f for f in Prefactura.select(criterio)]

    def calcular_comprado(self, fechaini = None, fechafin = None):
        """
        Devuelve el importe total de ventas al cliente
        entre las fechas indicadas. Si las fechas son None no 
        impondrá rangos en la búsqueda. No se consideran 
        pedidos ni albaranes, solo compras ya facturadas.
        """
        total = 0
        facturas = self.get_facturas(fechaini, fechafin)
        for f in facturas:
            total += f.calcular_importe_total()
        return total

    def calcular_cobrado(self, fechaini = None, fechafin = None):
        """
        Devuelve el importe total de compras cobradas al cliente  
        entre las fechas indicadas. Si las fechas son None no 
        impondrá rangos en la búsqueda. No se consideran 
        pedidos ni albaranes, solo compras ya facturadas.
        De todas esas facturas, suma el importe de los pagos
        relacionadas con las mismas. _No tiene en cuenta_ las 
        fechas de los cobros, solo las fechas de las facturas 
        a las que corresponden esos cobros (ya que la consulta 
        base es de facturas, lo lógico es saber cuánto de esas 
        facturas está pagado, sea en las fechas que sea).
        Si no hay facturas o no hay cobros, devuelve 0.0.
        """
        #import time
        #antes = time.time()
        facturas = self.get_facturas(fechaini, fechafin)
        #total = 0
        #for f in facturas:
        #    for cobro in f.cobros:
        #        total += cobro.importe
        #_total = total
        #print "1.-", time.time() - antes
        #antes = time.time()
        # OPTIMIZACIÓN:
        if facturas:
            csql = """
                SELECT SUM(cobro.importe) 
                  FROM cobro 
                  WHERE factura_venta_id IN (%s);
            """ % (", ".join([str(f.id) for f in facturas]))
            try:
                total = sqlhub.getConnection().queryOne(csql)[0]
            except IndexError:
                total = 0.0
            if total == None:
                total = 0.0
        else:
            total = 0.0
        #print "2.-", time.time() - antes
        #print _total, total
        #assert round(_total, 2) == round(total, 2)
        return total

    def calcular_pendiente_cobro(self, fechaini = None, fechafin = None):
        """
        Devuelve el importe total pendiente de cobro del cliente. Para ello 
        _ignora los vencimientos_ y simplemente devuelve la diferencia
        entre el importe total facturado y el importe total de los
        cobros relacionados con esas facturas.
        """
        total = self.calcular_comprado(fechaini, fechafin)
        cobrado = self.calcular_cobrado(fechaini, fechafin)
        pendiente = total - cobrado
        return pendiente

    def calcular_pendiente_cobro_vencido(self, 
                                         fechaini = None, 
                                         fechafin = None, 
                                         fecha_base = datetime.date.today()):
        """
        Calcula el pendiente de cobro[1] de los vencimientos vencidos en 
        fecha_base de las facturas entre fechaini y fechafin.
        [1] Los cobros también se filtran por fecha_base. Si son posteriores, 
        no se tienen en cuenta.
        Devuelve el pendiente de cobro y un diccionario de facturas, pendiente 
        vencido y cobrado (por ese orden en cada clave del diccionario).
        """
        vencido = 0.0
        cobrado = 0.0
        dicfacturas = {}
        facturas = self.get_facturas(fechaini, fechafin)
        for f in facturas:
            vencf = f.calcular_vencido(fecha_base)
            vencido += vencf
            cobrf = f.calcular_cobrado(fecha_base)
            cobrado += cobrf
            #if vencf - cobrf > 0:
            tot_vtos = sum([v.importe for v in f.vencimientosCobro])
            if (round(tot_vtos - cobrf) != 0):  # No me intersan las 
                                                # diferencias de céntimos
                dicfacturas[f] = (vencf, cobrf)
        return vencido - cobrado, dicfacturas

    def calcular_credito_disponible(self, cache_pdte_cobro = None):
        """
        Riesgo concedido - pendiente de cobro.
        OJO: No usar cache_pdte_cobro si no se está completamente seguro de 
        la certeza de los datos, en cuyo caso es preferible dejar que 
        se calcule dentro de la rutina aunque tarde más.
        Si el 
        """
        if self.riesgoConcedido==-1: # Ignorar. Devuelvo un máximo arbitrario.
            return sys.maxint
        else:
            if cache_pdte_cobro is None:    # Recalculo (agüita, suele tardar)
                pdte_cobro = self.calcular_pendiente_cobro()
            else:
                pdte_cobro = cache_pdte_cobro
            res = self.riesgoConcedido - pdte_cobro
        return res

    def get_facturas_vencidas_impagadas(self):
        """
        Devuelve las facturas vencidas e impagadas (con documento de cobro 
        vencido o directamente sin documento de cobro y sin pagos 
        relacionados).
        """
        if DEBUG:
            print " --> Soy get_facturas_vencidas_impagadas. Toc-toc. Entrando..."
        impagadas = []
        for fra in self.facturasVenta:
            if round(fra.calcular_cobrado(), 2) < round(fra.importeTotal, 2):
                impagadas.append(fra)   # Aunque sea por un céntimo
        if DEBUG:
            print " <-- Soy get_facturas_vencidas_impagadas. Saliendo."
        return impagadas

    def get_facturas_vencidas_sin_documento_de_cobro(self):
        """
        Devuelve las facturas vencidas y sin documento de cobro 
        y sin pagos relacionados.
        """
        if DEBUG:
            print " --> Soy get_facturas_vencidas_sin_documento_de_cobro."\
                  " Toc-toc. Entrando..."
        impagadas = []
        # El criterio es muy fácil. El importe cubierto por los documentos de 
        # cobro o cobros en general (registros cobro) es menor al de los 
        # vencimientos totales.
        # Si la factura no ha vencido (ninguna fecha de vencimiento supera a 
        # la actual) no se tiene en cuenta. Para considerarla vencida, todos 
        # los vencimientos deben haber expirado -esto es para evitar el caso 
        # en que se ha cumplido el primer vencimiento y el segundo cobro 
        # aún no está cubierto por un doc. de pago-.
        for fra in self.facturasVenta:
            if fra.esta_vencida():
                totvencs = sum([v.importe for v in fra.vencimientosCobro])
                totcobrs = sum([c.importe for c in fra.cobros])
                if round(totcobrs, 2) < round(totvencs, 2):
                    impagadas.append(fra)   # Aunque sea por un céntimo
        if DEBUG:
            print " <-- Soy get_facturas_vencidas_sin_documento_de_cobro."\
                  " Saliendo."
        return impagadas

    def get_direccion_completa(self):
        """
        Devuelve una cadena con la dirección completa del cliente:
        dirección, código postal, ciudad, provincia y país.
        """
        res = "%s;" % self.direccion
        if self.cp:
            res += "%s -" % self.cp
        res += " %s" % self.ciudad
        if self.provincia and self.ciudad != self.provincia:
            res += ", %s" % self.provincia
        if self.pais:
            res += " (%s)" % self.pais
        if res.strip() == ";":
            res = ""
        return res.strip()

    def get_grupos(self):
        """
        Devuelve el grupo al que actualmente pertenece el cliente. None si 
        no está en ninguno.
        """
        res = []
        for g in self.gruposAlumnos:
            if not g.en_lista_de_espera(self):
                res.append(g)
        return res

    def calcular_edad(self, fecha = datetime.date.today()):
        """
        Calcula la edad en la fecha dada (por defecto, la edad actual, a día 
        de hoy).
        """ 
        hoy = fecha # Me es más cómodo.
        nac = self.fechaNacimiento
        try:
            annos = (hoy.year - nac.year)
        except (TypeError, AttributeError):   # Fecha de nacimiento es None.
            annos = 0
        else:
            hoy = datetime.date(nac.year, hoy.month, hoy.day)
            if (hoy == nac  # Happy birthday xD
                or hoy > nac):
                annos += 1
        return annos

    edad = property(calcular_edad)


class Padecimiento(SQLObject, PRPCTOO):
    
    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

class Contador(SQLObject, PRPCTOO):
    clientes = MultipleJoin('Cliente')

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_last_factura_creada(self):
        """
        Devuelve la última factura creada según el orden del campo numfactura.
        None si no hay facturas de la serie (ninguna factura coincide en 
        prefijo ni sufijo).
        """
        self.sync()
        fras = self.__get_facturas()
        if fras.count() > 0:
            return fras[0]
        return None

    def get_last_numfactura_creada(self):
        """
        Devuelve la última factura creada de la serie según el orden del 
        campo numfactura, no el de ID ni el de la tabla de la BD.
        Si no hay facturas en la serie, devuelve la cadena vacía.
        """
        ultima_fra = self.get_last_factura_creada()
        if ultima_fra:
            return ultima_fra.numfactura
        return ""
    
    def __get_facturas(self):
        self.sync()
        fras = FacturaVenta.select(AND(
            FacturaVenta.q.numfactura.startswith(self.prefijo), 
            FacturaVenta.q.numfactura.endswith(self.sufijo)), 
            orderBy = "-numfactura")
        return fras

    def get_facturas(self):
        """
        Devuelve las facturas de la serie, ordenadas por numfactura.
        """
        fras = [f for f in self.__get_facturas()]
        fras.reverse()
        return fras

    def get_and_commit_numfactura(self):
        """
        Devuelve y hace efectivo (esto es, aumenta el contador)
        el siguiente número de factura de la serie facturable 
        del contador.
        """
        return self.get_next_numfactura(commit = True)

    def get_next_numfactura(self, commit = False, inc = 1):
        """
        Por defecto devuelve el que sería el siguiente número 
        de factura. Si commit = True entonces sí lo hace 
        efectivo y corre el contador de la serie.
        "inc" es el número en que avanza el contador. Por defecto 1
        """
        self.sync()
        numfactura = "%s%04d%s" % (self.prefijo, 
                                   self.contador - 1 + inc, 
                                   self.sufijo)
        if commit:
            self.contador += inc
            self.syncUpdate()
        return numfactura

    def get_info(self):
        """
        Devuelve el prefijo, número actual y sufijo del contador.
        """
        # return "%s%d%s" % (self.prefijo, self.contador, self.sufijo)
        return self.get_next_numfactura(commit = False)
        
    def get_contador_por_defecto():
        """
        Devuelve un objeto contador por defecto para el año en curso.
        si no existe, lo crea según el formato: AAAA/x. Donde AAAA es el año.
        Para determinar el contador por defecto:
        Si solo hay uno, devuelve ese.
        Si hay varios, devuelve el que tenga el año actual en el prefijo.
        Si no hay ninguno así, el que tenga el año en el prefijo.
        Si tampoco hay, devuelve el último creado en el sistema.
        Y si no hay ninguno, lo crea tal y como dice arriba.
        No hay flor como la amapola, ni cariño como el mío.
        """
        contadores = Contador.select(orderBy = "-id")
        anno = `datetime.date.today().year`
        if contadores.count() == 0:
            res = Contador(prefijo = anno, sufijo = "", contador = 1)
        elif contadores.count() == 1:
            res = contadores[0]
        else:
            res = None
            for c in contadores:
                if anno == c.prefijo:
                    res = c
                    break
            if not res:
                for c in contadores:
                    if anno == c.sufijo:
                        res = c
                        break
            if not res:
                res = contadores[0]
        return res

    get_contador_por_defecto = staticmethod(get_contador_por_defecto)

        
class Nota(SQLObject, PRPCTOO):

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_str_nota(self):
        txtnota = utils.str_fechahora(self.fechahora) + ": "
        if self.texto and self.observaciones:
            if self.texto.strip().endswith("."):
                txtnota += "%s %s" % (self.texto, self.observaciones)
            else:
                txtnota += "%s. %s" % (self.texto, self.observaciones)
        elif self.texto:
            txtnota += self.texto
        else:
            txtnota += self.observaciones
        return txtnota

class SuperFacturaVenta:
    """
    Superclase para las facturas de venta y prefacturas.
    """

    def calcular_vencido(self, fecha_base = datetime.date.today()):
        """
        Devuelve el importe vencido[1] de la factura en la fecha recibida.
        Por defecto se usa la fecha del sistema.

        [1] Cobrado o no, da igual.
        """
        vencido = sum([vto.importe for vto in self.vencimientosCobro 
                       if vto.fecha <= fecha_base])
        return vencido

    def esta_vencida(self):
        """
        Devuelve True si _todos_ los vencimientos de la factura se han pasado.
        """
        vencida = True
        for vto in self.vencimientosCobro:
            if vto.fecha > datetime.datetime.now():
                vencida = False
                break 
                # Tiene un vto. que no ha llegado. Me la salto.
        return vencida

    def get_albaranes(self, incluir_nones = False, incluir_servicios = False):
        """
        Devuelve los objetos albarán que están relacionados 
        con la factura a través de sus líneas de venta.
        """
        albaranes = []
        for ldv in self.lineasDeVenta:
            if not incluir_nones:
                if ldv.albaranSalidaID and ldv.albaranSalida not in albaranes:
                    albaranes.append(ldv.albaranSalida)
            else:
                if ldv.albaranSalida not in albaranes:
                    albaranes.append(ldv.albaranSalida)
        if incluir_servicios:
            for srv in self.servicios:
                if not incluir_nones:
                    if srv.albaranSalidaID and srv.albaranSalida not in albaranes:
                        albaranes.append(srv.albaranSalida)
                else:
                    if srv.albaranSalida not in albaranes:
                        albaranes.append(srv.albaranSalida)
        return albaranes

    def get_pedidos(self, incluir_nones = False):
        """
        Devuelve los objetos PedidoVenta que están relacionados 
        con la factura a través de sus líneas de venta.
        """
        pedidos = []
        for ldv in self.lineasDeVenta:
            if not incluir_nones:
                if ldv.pedidoVentaID and ldv.pedidoVenta not in pedidos:
                    pedidos.append(ldv.pedidoVenta)
            else:
                if ldv.pedidoVenta not in pedidos:
                    pedidos.append(ldv.pedidoVenta)
        return pedidos

    def calcular_total(self):
        """
        Calcula el total de la factura, con descuentos, IVA y demás incluido.
        Devuelve un FixedPoint (a casi todos los efectos, se comporta como 
        un FLOAT.
        De todas formas, pasa bien por el utils.float2str).
        """
        subtotal = self.calcular_subtotal() 
        tot_dto = self.calcular_total_descuento(subtotal) 
        tot_iva = self.calcular_total_iva(subtotal, tot_dto, self.cargo)
        irpf = self.irpf * subtotal
        total = subtotal + float(self.cargo) + tot_dto + tot_iva + irpf
        return total
    
    def calcular_importe_total(self):
        """
        Calcula y devuelve el importe total, incluyendo IVA, de la factura.
        """
        return self.calcular_total()
        # NOTA: Método "duplicado" por error. Funciona mejor el 
        # «calcular_total» porque no comete "errores" de redondeo.

    importeTotal = property(calcular_importe_total, 
                            doc = calcular_importe_total.__doc__)

    def calcular_total_descuento(self, subtotal = None):
        """
        Calcula el total del descuento global.
        """
        if subtotal == None:
            subtotal = self.calcular_subtotal()
        tot_dto = utils.ffloat(-1 * (subtotal + float(self.cargo)) * 
                                self.descuento)
        return tot_dto

    def calcular_total_iva(self, subtotal = None, tot_dto = None, 
                           cargo = None):
        """
        Calcula el importe total de IVA de la factura.
        """
        if subtotal == None:
            subtotal = self.calcular_subtotal()
        if tot_dto == None: 
            tot_dto = self.calcular_total_descuento(subtotal)
        if cargo == None:
            cargo = self.cargo
        total_iva = utils.ffloat(subtotal + tot_dto + float(self.cargo)) 
        total_iva *= self.iva
        return total_iva
    
    def emparejar_vencimientos(self):
        """
        Devuelve un diccionario con los vencimientos y cobros de la factura 
        emparejados.
        El diccionario es de la forma:
        {vencimiento1: [cobro1], 
         vencimiento2: [cobro2], 
         vencimiento3: [], 
         'vtos': [vencimiento1, vencimiento2, vencimiento3...], 
         'cbrs': [cobro1, cobro2]}
        Si tuviese más cobros que vencimientos, entonces se devolvería un diccionario tal que:
        {vencimiento1: [cobro1], 
         vencimiento2: [cobro2],
         None: [cobro3, cobro4...], 
         'vtos': [vencimiento1, vencimiento2], 
         'cbrs': [cobro1, cobro2, cobro3, cobro4...]}
        'vtos' y 'cbrs' son copias ordenadas de las listas de vencimientos y cobros.
        El algoritmo para hacerlo es:
        1.- Construyo el diccionario con todos los vencimientos.
        2.- Construyo una lista auxiliar con los cobros ordenados por fecha.
        3.- Recorro el diccionario de vencimientos por orden de fecha.
            3.1.- Saco y asigno el primer cobro de la lista al vencimiento tratado en la iteración.
            3.2.- Si no quedan vencimientos por asignar, creo una clave None y agrego los cobros restantes.
        """
        res = {}
        cbrs = self.cobros[:]
        cbrs.sort(utils.cmp_fecha_id)
        vtos = self.vencimientosCobro[:]
        vtos.sort(utils.cmp_fecha_id)
        res['vtos'] = vtos[:]
        res['cbrs'] = cbrs[:]
        for vto in vtos:
            try:
                cbr = cbrs.pop()
            except IndexError:
                res[vto] = []
            else:
                res[vto] = [cbr]
        if cbrs != []:
            res[None] = cbrs
        return res

    def calcular_beneficio(self):
        """
        Devuelve la suma de los beneficios por línea de venta.
        El beneficio de un servicio es el precio total del servicio.
        El beneficio de una LDV es el (PVP - IVA) * porcentaje_tarifa * cantidad.
        """
        tot = 0.0
        for srv in self.servicios:
            tot += srv.calcular_beneficio()
        for ldv in self.lineasDeVenta:
            ben = ldv.calcular_beneficio()
            tot += ben
        return tot

    def calcular_pendiente_cobro(self):
        """
        Devuelve el importe pendiente de cobro de la factura.
        Se considera pendiente de cobro a la diferencia entre 
        el total cobrado y el total de los vencimientos, *independientemente
        del importe total de la factura*. Es indispensable, por tanto, 
        que el importe total de la factura coincida con el total 
        de vencimientos.
        Aunque si no fuera así -por un cambio en las LDVs 
        involuntario, error o borrado- no afectaría a la 
        parte financiera si los vencimientos están correctamente 
        creados.
        """
        totvtos = sum([v.importe for v in self.vencimientosCobro])
        totcbrs = self.calcular_cobrado()
        return totvtos - totcbrs

    def calcular_cobrado(self, fecha_base = None):
        """
        Devueve el importe total cobrado de la factura hasta la fecha recibida.
        Si no se pasa una fecha, se devuelve el total cobrado (sumatorio de 
        los importes de todos los cobros relacionados).
        """
        if fecha_base is None:
            # Un cobro cobrado, valga la redundancia, es un cobro que se ha 
            # hecho efectivo, es decir, un pagaré/cheque con fecha no 
            # vencida(*) o con fecha vencida pero marcado como cobrado, 
            # un confirming(*), un pago en efectivo o por transferencia, etc...
            # (*) Una promesa de pago cuenta para mí como un cobro aunque 
            # todavía no tenga las pelas en el bolsillo.
            cobros_cobrados = [c for c in self.cobros 
                                if not c.sync() and c.esta_cobrado()]
            # UGLY HACK: sync() siempre devuelve None, por eso le pongo el 
            # not. Así fuerzo a sincronizar los valores antes de comprobar 
            # si está cobrado.
        else:
            cobros_cobrados = [c for c in self.cobros 
                                if not c.sync() and 
                                   c.fecha <= fecha_base and 
                                   c.esta_cobrado(fecha_base)]
        res = sum([c.importe for c in cobros_cobrados])
        return res

    def calcular_pendiente_de_documento_de_pago(self):
        """
        Devuelve la cantidad de la factura pendiente de cubrir por un 
        documento de pago, vencido o no, o por un cobro.
        OJO: Calcula la diferencia en base al total de los vencimientos, 
        independientemente del total de la factura. Una factura sin 
        vencimientos no sabemos cómo se cobra, por tanto nos da igual si 
        tiene o no documentos de pago, y por tanto aquí devolverá un cero 
        como un castillo como en el que vivo con tu madre.
        Cartón de leche, pijama de lino.
        """
        cobros = sum([c.importe for c in self.cobros])
        total_vencimientos = sum([v.importe for v in self.vencimientosCobro])
        res = total_vencimientos - cobros
        return res

    def __dividir_por_comercial(self, func_a_evaluar_en_lineas_as_str, 
                                *args, **kw):
        """
        Divide el resultado que devuelva la función «func_a_evaluar_en_lineas» 
        aplicada a las líneas de venta, servicio, etc.
        """
        comerciales = {None: 0.0}   # Al menos siempre debe quedar None con 0
                                    # aunque no tenga eledeuves ni servicios.
        totalregladetres = 0.0
        if isinstance(self, (FacturaVenta, Prefactura)):
            lineas = self.lineasDeVenta + self.servicios
        else:
            raise TypeError
        for srv_o_ldv in lineas:
            subtotal = getattr(srv_o_ldv, 
                               func_a_evaluar_en_lineas_as_str)(*args, **kw)
            totalregladetres += subtotal    # Alias cuenta de la vieja.
            try:
                comerciales[srv_o_ldv.comercial] += subtotal 
            except KeyError:
                comerciales[srv_o_ldv.comercial] = subtotal
        totalfactura = self.calcular_total()  # Con IVA, descuentos y de todo.
        res = {}
        for comercial in comerciales:
            try:
                res[comercial] = (comerciales[comercial] / totalregladetres
                                  * totalfactura)
            except ZeroDivisionError:
                res[comercial] = 0.0
        return res
 
    def dividir_total_por_comercial(self):
        """
        Devuelve el total de la factura en euros dividido por comercial en 
        función de los importes de las líneas de venta que componen la factura 
        pertenecientes a cada comercial (relacionados a través del pedido, 
        pero esos detalles van en otra clase. Máxima cohesión, mínima 
        dependencia).
        """
        res = self.__dividir_por_comercial("calcular_subtotal", iva = False)
        return res
   
    def dividir_beneficio_por_comercial(self):
        """
        Hace lo mismo que el método de dividir el total de la factura por 
        comercial, solo que en este caso calcula el beneficio aportado por 
        las ventas del comercial.
        """
        # Esto es un as que me guardo en la manga.
        res = self.__dividir_por_comercial("calcular_beneficio")
        return res

    def get_comerciales(self):
        """
        Devuelve los comerciales de la factura relacionados a través de 
        los pedidos.
        """
        comerciales = []
        for p in self.get_pedidos():
            comercial = p.comercial
            if comercial != None and comercial not in comerciales:
                comerciales.append(comercial)
        return tuple(comerciales)

    def borrar_vencimientos_y_estimaciones(self):
        """
        Borra todos los vencimientos de la factura.
        """
        for vto in self.vencimientosCobro:
            vto.factura = None
            vto.destroySelf()

    def crear_vencimientos_por_defecto(self, formapago = None):
        """
        Intenta crear los vencimientos de la factura con la forma de pago 
        actual del cliente si «formapago» es None. En otro caso debe ser 
        una cadena de texto.
        Devuelve los vencimientos creados o una tupla vacía si no se pudo 
        determinar la forma de pago.
        """
        # TODO: Debería devolver también un código de error con el motivo 
        # por el que no haya podido crear los vencimientos.
        if not formapago:
            formapago = self.cliente and self.cliente.textoformacobro or ""
        res = []
        cliente = self.cliente
        if cliente.vencimientos != None:
            try:
                vtos = cliente.get_vencimientos(self.fecha)
            except:
                pass    # Los vencimientos no son válidos o no tiene.
            else:
                self.borrar_vencimientos_y_estimaciones()
                total = self.calcular_importe_total()
                numvtos = len(vtos)
                try:
                    cantidad = total/numvtos
                except ZeroDivisionError:
                    cantidad = total
                if self.fecha == None:
                    self.fecha = datetime.date.today()
                if cliente.diadepago != None and cliente.diadepago != '':
                    diaest = cliente.get_dias_de_pago()
                else:
                    diaest = False
                for incr in vtos:
                    fechavto = self.fecha + (
                        incr * datetime.timedelta(days = 1))
                    vto = VencimientoCobro(fecha = fechavto,
                            importe = float(cantidad),
                            facturaVenta = self, 
                            observaciones = formapago, 
                            cuentaOrigen = self.cliente 
                                and self.cliente.cuentaOrigen or None)
                    res.append(vto)
                    if diaest:
                        # Esto es más complicado de lo que pueda parecer a 
                        # simple vista. Ante poca inspiración... ¡FUERZA 
                        # BRUTA!
                        fechas_est = []
                        for dia_estimado in diaest:
                            while True:
                                try:
                                    fechaest = datetime.date(
                                                    day = dia_estimado, 
                                                    month = fechavto.month, 
                                                    year = fechavto.year)
                                    break
                                except:
                                    dia_estimado -= 1
                                    if dia_estimado <= 0:
                                        dia_estimado = 31
                            if fechaest < fechavto:     # El día estimado 
                                    # cae ANTES del día del vencimiento. 
                                    # No es lógico, la estimación debe ser 
                                    # posterior. Cae en el mes 
                                    # siguiente, pues.
                                mes = fechaest.month + 1
                                anno = fechaest.year
                                if mes > 12:
                                    mes = 1
                                    anno += 1
                                try:
                                    fechaest = datetime.date(
                                                        day = dia_estimado, 
                                                        month = mes, 
                                                        year = anno)
                                except ValueError:
                                    # La ley de comercio dice que se pasa 
                                    # al último día del mes:
                                    fechaest = utils.last_day_of(mes, anno)
                            fechas_est.append(fechaest)
                        fechas_est.sort(utils.cmp_DateTime)
                        fechaest = fechas_est[0]
                        vto.fecha = fechaest 
        return tuple(res)


class FacturaVenta(SQLObject, PRPCTOO, SuperFacturaVenta):
    servicios = MultipleJoin('Servicio')
    lineasDeVenta = MultipleJoin('LineaDeVenta')
    vencimientosCobro = MultipleJoin('VencimientoCobro')
    cobros = MultipleJoin('Cobro')
    documentos = MultipleJoin('Documento')
    notas = MultipleJoin("Nota")

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_info(self):
        return "Factura %s (%s)[%s]: %s" % (self.numfactura, 
                    self.cliente and self.cliente.nombre or "Sin cliente", 
                    utils.str_fecha(self.fecha), 
                    utils.float2str(self.calcular_total()))

    def get_str_estado(self):
        """
        Devuelve el estado de la factura como cadena: 
        Vacía: No tiene líneas de venta ni servicios.
        Sin vencimientos: No tiene vencimientos creados.
        No vencida: Si alguna fecha de vencimiento < actual.
        Vencida: Si todas las fechas de vencimiento >= actual.
        Cobrada: Si cobros == importe total.
        """
        ESTADOS = ("Vacía", "Sin vencimientos", "No vencida", "Vencida", 
                   "Cobrada")
        if len(self.lineasDeVenta) + len(self.servicios) == 0:
            return ESTADOS[0]
        if len(self.vencimientosCobro) == 0:
            return ESTADOS[1]
        ultima_fecha_vto = self.vencimientosCobro[0].fecha
        for v in self.vencimientosCobro:
            if v.fecha > ultima_fecha_vto:
                ultima_fecha_vto = v.fecha
        vencido = sum([v.importe for v in self.vencimientosCobro])
        cobrado = sum([c.importe for c in self.cobros
                    if c.pagareCobro == None or not c.pagareCobro.pendiente])
        if cobrado and cobrado >= vencido:
            return ESTADOS[4]
        else:
            if ultima_fecha_vto < datetime.date.today():
                return ESTADOS[3]
            else:
                return ESTADOS[2]

    def get_contador(self):
        """
        Devuelve el contador de la factura aunque el cliente ya haya 
        cambiado de contador (por cierre de año, por ejemplo).
        Si no se puede determinar, devuelve None.
        """
        res = None
        numfactura = self.numfactura
        contadores = Contador.select()
        for c in contadores:
            if (numfactura.startswith(c.prefijo) 
               and numfactura.endswith(c.sufijo)):
                tmpnumfactura = numfactura.replace(c.prefijo, "", 1)
                tmpnumfactura=tmpnumfactura[::-1].replace(c.sufijo[::-1], "", 1)
                # Para que solo sustituya el sufijo del final. Útil si el 
                # sufijo es numérico (por ejemplo, un año) y se encuentra por 
                # casualidad también en el propio número.
                if tmpnumfactura.isdigit():
                    res = c
                    break
        return res

    def get_numero_numfactura_contador(self):
        """
        Devuelve el número de la factura como entero sin tener en cuenta 
        el contador del cliente. En lugar de eso, determina el contador de 
        la factura mediante el método «get_contador».
        Si el contador no se puede determinar, intentará usar el del cliente 
        mediante el método «get_numero_numfactura».
        """
        contador = self.get_contador()
        numero = self.numfactura.replace(contador.prefijo, "", 1)
        numero = numero[::-1].replace(contador.prefijo[::-1], "", 1)[::-1]
        try:
            res = int(numero)
        except (ValueError, TypeError):
            res = self.get_numero_numfactura()
        return res

    def get_numero_numfactura(self):
        """
        Devuelve el número de factura sin prefijo ni 
        sufijo y como entero.
        Salta una excepción si no se pudo determinar
        la parte numérica del número de factura.
        """
        ## import re
        ## expresion = re.compile('[0-9]+')
        ## numero = expresion.findall(self.numfactura)
        # NOTA: Esto de arriba está bien, pero no vale cuando tiene prefijos y sufijos numéricos.
        try:
            prefijo = self.cliente.contador.prefijo     # DEBE tener cliente y contador. Es precondición al crear una fra.
            sufijo = self.cliente.contador.sufijo
            # TODO: OJO: Hay un problema. Si se le ha cambiado el contador 
            #            al cliente... la cagaste Burt Lancaster.
        except AttributeError:
            self.cliente.sync()
            try:
                prefijo = self.cliente.contador.prefijo     # DEBE tener cliente y contador. Es precondición al crear una fra.
                sufijo = self.cliente.contador.sufijo
            except Exception, msg:
                txt = "pclases::get_numero_numfactura -> Excepción: %s" % (msg)
                print txt
                prefijo = sufijo = ""
        numero = self.numfactura.replace(prefijo, '')
        numero = numero.replace(sufijo, '')
        # print self.cliente.contador.prefijo, self.cliente.contador.sufijo, numero
        # return int(numero)   # Prefiero que salte la excepción si no se encuentra el número.
        # Ok. El cliente no está, así que voy a intentar primero sacar el número de la factura errónea 
        # (es errónea porque no coincide con el formato del contador de su cliente) y si no puedo, la
        # ignoro.
        try:
            numero = int(numero)
        except ValueError:
            import re
            expr_entero = re.compile('[0-9]+')
            try:
                numero = int(expr_entero.findall(numero)[-1])
            except ValueError:
                numero = 0  # Esto NO debería ocurrir.
            except IndexError:
                numero = 0  # Algo hay que hacer. Y se tiene que devolver un 
                            # número sí o sí, así que...
                            # Como supongo que esto no se usa más que para 
                            # ordenar facturas por número, las facturas 
                            # inválidas (número no encaja en contador) no 
                            # influirán en la actualización del contador.
        return numero

    def calcular_total_irpf(self, subtotal = None, tot_dto = None, 
                            cargo = None):
        """
        Calcula el importe total de retención de IRPF (se resta al total)
        de la factura. Se devuelve en positivo (aunque en realidad sea una 
        cantidad negativa a sumar al total).
        """
        if self.irpf != 0:
            if subtotal == None:
                subtotal = self.calcular_subtotal()
            if tot_dto == None: 
                tot_dto = self.calcular_total_descuento(subtotal)
            if cargo == None:
                cargo = self.cargo
            total_irpf = (utils.ffloat(subtotal + tot_dto + float(self.cargo)) 
                          * self.irpf)
        else:
            total_irpf = 0.0
        return total_irpf

    def enviar_por_correoe_a_comercial_relacionado(self, asunto = None):
        """
        Envia un correo electrónico al (o a los) comercial relacionado con la 
        factura con dos PDF adjuntos: una factura con la marca de agua "copia" 
        y el histórico del CRM.
        También crea una tarea automática para identificar que ya se ha 
        enviado la factura.
        Si no tiene comercial relacionado, envia el correo electrónico a todos 
        los usuarios con permisos sobre la ventana de crm de seguimiento de 
        impagos.
        """
        # No estoy muy seguro de que esta sea el sitio indicado para meter 
        # esta rutina.
        try:
            from geninformes import crm_generar_pdf_detalles_factura
        except ImportError:
            sys.path.append(os.path.join('..', 'informes'))
            from geninformes import crm_generar_pdf_detalles_factura
        try:
            from albaranes_de_salida import imprimir_factura as generar_factura
        except ImportError:
            sys.path.append(os.path.join('..', 'formularios'))
            from albaranes_de_salida import imprimir_factura as generar_factura
        copiafra = generar_factura(self, abrir = False, es_copia = True)
        historial = crm_generar_pdf_detalles_factura(self) 
        comerciales = self.get_comerciales()
        destinatarios = [c.correoe.strip() for c in comerciales 
                         if c.correoe and c.correoe.strip()]
        if not destinatarios:
            # OJO: Ventana HARDCODED.
            try:
                ventana = Ventana.selectBy(
                    fichero = "crm_seguimiento_impagos.py")[0]
            except IndexError:
                pass    # La ventana no existe por lo que sea. 
                        # Weird, but... pasando.
            else:
                for permiso in ventana.permisos:
                    u = permiso.usuario
                    if u.email and u.email.strip():
                        destinatarios.append(u.email.strip())
        if DEBUG:
            destinatarios.append("rodriguez.bogado@gmail.com")
            destinatarios.append("frbogado@novaweb.es")
        if destinatarios:
            # TODO: Datos de cuenta de correo y servidor HARCODED.
            remitente = ("comercialgeotexan@gea21.es", 
                         "comercialgeotexan@gea21.es", "comgeo98")
            if asunto is None:
                asunto = "Factura %s" % self.numfactura
            texto = "Se adjunta copia de la factura en PDF e historial de "\
                    "la misma."
            servidor = "gea21.es"
            ok = utils.enviar_correoe(remitente[0],  
                    destinatarios, 
                    asunto, 
                    texto, 
                    [copiafra, historial], 
                    servidor, 
                    remitente[1], 
                    remitente[2])
            if ok:
                t = Tarea(facturaVenta = self, 
                          categoria = 
                            Categoria.get_categoria_tareas_automaticas(), 
                          texto = "Factura emitida hace más de 45 días."
                                  "No se ha recibido documento de cobro."
                                  "Enviar correo a comercial.", 
                          pendiente = False, 
                          fecha = datetime.date.today(), 
                          observaciones = "Tarea creada automáticamente.", 
                          fechadone = datetime.date.today())

    def calcular_subtotal(self, incluir_descuento = False):
        """
        Devuelve el subtotal de la factura: líneas de venta + servicios.
        No cuenta descuento global ni IVA.
        """
        #import time
        #antes = time.time()
        # OPTIMIZACIÓN:
        try:
            total_ldvs = sqlhub.getConnection().queryOne(""" 
                SELECT SUM(ROUND(
                        CAST(cantidad * precio * (1-descuento) AS NUMERIC), 
                        2))
                  FROM linea_de_venta
                  WHERE factura_venta_id = %d
                ;""" % self.id)[0]
            if total_ldvs == None:
                total_ldvs = 0.0
        except IndexError:
            total_ldvs = 0.0
        try:
            total_srvs = sqlhub.getConnection().queryOne(""" 
                SELECT SUM(ROUND(
                        CAST(cantidad * precio * (1-descuento) AS NUMERIC), 
                        2)) 
                  FROM servicio      
                  WHERE factura_venta_id = %d
                ;""" % self.id)[0]
            if total_srvs == None:
                total_srvs = 0.0
        except IndexError:
            total_srvs = 0.0
        subtotal = float(total_ldvs) + float(total_srvs)
        if incluir_descuento: 
            subtotal += self.calcular_total_descuento(subtotal)
        #_subtotal = subtotal
        #tuno = time.time() - antes
        #print "1.-", tuno 
        #antes = time.time()
        # Código original:
        #total_ldvs = sum([utils.ffloat((l.cantidad * l.precio) * (1 - l.descuento)) for l in self.lineasDeVenta])
        #total_srvs = sum([utils.ffloat((s.precio * s.cantidad) * (1 - s.descuento)) for s in self.servicios])
        #subtotal = total_ldvs + total_srvs
        #if incluir_descuento:
        #    subtotal += self.calcular_total_descuento(subtotal)
        #tdos = time.time() - antes
        #print "2.-", tdos 
        # En las siguientes líneas de venta, la optimización da el resultado 
        # correcto, era el código original el que bailaba un decimal, así que 
        # no comparo
        #if self.id not in (236, 264, 344, 618, 695, 704, 750):
        #    assert _subtotal == subtotal, "\n_subtotal: %s\nsubtotal: %s\nid: %s (%s)" % (_subtotal, subtotal, self.id, self.numfactura)
        #print tuno <= tdos and "                    ---> OK <---" or "                    ---> :( <---"
        return subtotal

    def calcular_base_imponible(self):
        """
        Devuelve la base imponible (subtotal + descuento global) de la factura.
        """
        base_imponible = self.calcular_subtotal(incluir_descuento = True)
        return base_imponible

    def get_last_evento(self):
        """
        Devuelve la última nota (por fecha) relacionada con la factura.
        """
        notas = Nota.select(Nota.q.facturaVenta == self.id, 
                            orderBy = "-fechahora")
        try:
            return notas[0]
        except IndexError:
            return None

    def get_forma_de_pago(self):
        """
        Devuelve la forma de pago de la factura. Si ya tiene vencimientos de 
        cobro, usa la forma de pago del primero de ellos. En otro caso, 
        devuelve la forma de pago del cliente.
        """
        # TODO: No estaría mal dividir el total de la factura entre el número 
        # de vencimientos y devolver el importe correspondiente a cada forma 
        # de pago (si tuviera vencimientos y varias formas de pago, claro).
        try:
            return self.vencimientosCobro[0].observaciones
        except IndexError:
            return self.cliente and self.cliente.textoformacobro or ""
    

class Prefactura(SQLObject, PRPCTOO, SuperFacturaVenta):
    servicios = MultipleJoin('Servicio')
    lineasDeVenta = MultipleJoin('LineaDeVenta')
    vencimientosCobro = MultipleJoin('VencimientoCobro')
    cobros = MultipleJoin('Cobro')
    documentos = MultipleJoin('Documento')

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_str_estado(self):
        """
        Devuelve el estado de la prefactura como cadena: 
        Vacía: No tiene líneas de venta ni servicios.
        Sin vencimientos: No tiene vencimientos creados.
        No vencida: Si alguna fecha de vencimiento < actual.
        Vencida: Si todas las fechas de vencimiento >= actual.
        Cobrada: Si cobros == importe total.
        """
        ESTADOS = ("Vacía", "Sin vencimientos", "No vencida", "Vencida", 
                   "Cobrada")
        if len(self.lineasDeVenta) + len(self.servicios) == 0:
            return ESTADOS[0]
        if len(self.vencimientosCobro) == 0:
            return ESTADOS[1]
        ultima_fecha_vto = self.vencimientosCobro[0].fecha
        for v in self.vencimientosCobro:
            if v.fecha > ultima_fecha_vto:
                ultima_fecha_vto = v.fecha
        vencido = sum([v.importe for v in self.vencimientosCobro])
        cobrado = sum([c.importe for c in self.cobros
                    if c.pagareCobro == None or not c.pagareCobro.pendiente])
        if cobrado and cobrado >= vencido:
            return ESTADOS[4]
        else:
            if ultima_fecha_vto < datetime.date.today():
                return ESTADOS[3]
            else:
                return ESTADOS[2]
    def get_next_numfactura(anno = datetime.datetime.now().year):
        """
        Devuelve el siguiente número de factura del año recibido.
        """
        fras = Prefactura.select(Prefactura.q.fecha >= datetime.datetime(day = 1, month = 1, year = anno))
        numfacturas = [fra.get_numero_numfactura() for fra in fras]
        try:
            next = max(numfacturas) + 1
        except ValueError:
            next = 1
        return "%s/%s" % (anno, next)

    get_next_numfactura = staticmethod(get_next_numfactura)

    def get_numero_numfactura_y_anno_from(numfactura):
        partyear, partnum = numfactura.split("/")
        n = int(partnum)
        a = int(partyear)
        assert n > 0
        assert len(str(a)) == 4
        return n, a
    
    get_numero_numfactura_y_anno_from = staticmethod(get_numero_numfactura_y_anno_from)

    def get_numero_numfactura_from(numfactura):
        return Prefactura.get_numero_numfactura_y_anno_from(numfactura)[0]

    get_numero_numfactura_from = staticmethod(get_numero_numfactura_from)

    def get_numero_numfactura(self):
        """
        Devuelve el número de factura sin prefijo ni 
        sufijo y como entero.
        Salta una excepción si no se pudo determinar
        la parte numérica del número de factura.
        Comprueba también la aserción 
        año de la fecha de factura = año de numfactura
        """
        numfactura, partyear = Prefactura.get_numero_numfactura_y_anno_from(self.numfactura)
        assert partyear == self.fecha.year
        return numfactura

    def calcular_total_irpf(self, subtotal = None, tot_dto = None, 
                            cargo = None):
        """
        Calcula el importe total de retención de IRPF (se resta al total)
        de la factura.
        """
        if subtotal == None:
            subtotal = self.calcular_subtotal()
        if tot_dto == None: 
            tot_dto = self.calcular_total_descuento(subtotal)
        if cargo == None:
            cargo = self.cargo
        total_irpf = (utils.ffloat(subtotal + tot_dto + float(self.cargo)) 
                      * self.irpf)
        return total_irpf

    def calcular_subtotal(self):
        """
        Devuelve el subtotal de la factura: líneas de venta + servicios.
        No cuenta descuento global ni IVA.
        """
        total_ldvs = sum([utils.ffloat((l.cantidad * l.precio) 
                          * (1 - l.descuento)) for l in self.lineasDeVenta])
        total_srvs = sum([utils.ffloat((s.precio * s.cantidad) 
                          * (1 - s.descuento)) for s in self.servicios])
        subtotal = total_ldvs + total_srvs
        return subtotal

class Servicio(SQLObject, PRPCTOO, Venta):
    actividades = MultipleJoin("Actividad")

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_cliente(self):
        """
        Devuelve el objeto cliente de la LDV según su pedido, albarán o 
        factura. Por ese orden.
        """
        try:
            return self.pedidoVenta.cliente
        except AttributeError:
            try:
                return self.albaranSalida.cliente
            except AttributeError:
                try:
                    return self.facturaVenta.cliente
                except AttributeError:
                    try:
                        return self.prefactura.cliente
                    except AttributeError:
                        return None

    def get_factura_o_prefactura(self):
        """
        Devuelve la factura relacionada, tanto si es facturaVenta
        como prefactura, o None si no tiene ninguna de ellas.
        Como no debería tener ambos valores distintos de nulo a 
        la vez, tiene preferencia facturaVenta sobre prefactura.
        """
        return self.facturaVenta or self.prefactura

    def get_subtotal(self, iva = False):
        """
        Devuelve el subtotal del servicio. Con IVA (el IVA de la factura) si se le indica.
        """
        # PLAN: Con un buen diagrama de clases podría haber tenido una clase 
        #       padre común para servicios, líneas de venta y demás con sus 
        #       métodos abstractos get_subtotal y demás. Claro que sin un 
        #       documento de requisitos en condiciones es imposible tener unos 
        #       casos de uso en condiciones para poder hacer un diagrama de 
        #       clases en condiciones. A dios pongo por testigo de que jamás 
        #       volveré a confiar en un cliente que diga "yo creo que ya no 
        #       necesitamos más reuniones de validación de requisitos. 
        #       Eso es todo lo que queremos".
        res = self.cantidad * self.precio * (1 - self.descuento)
        if iva and self.facturaVentaID: 
            res *= (1 + self.facturaVenta.iva)
        elif iva and self.prefacturaID: 
            res *= (1 + self.prefactura.iva)
        return res

    calcular_subtotal = get_subtotal

    def calcular_beneficio(self):
        """
        Devuelve como beneficio el importe total del servicio.
        """
        return self.get_subtotal(iva = False)

class Destino(SQLObject, PRPCTOO):
    albaranesSalida = MultipleJoin('AlbaranSalida')

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_info(self):
        """
        Devuelve información básica acerca del destino.
        """
        return ", ".join((self.nombre, self.direccion, self.cp, self.ciudad, self.pais))

class Transportista(SQLObject, PRPCTOO):
    albaranesEntrada = MultipleJoin('AlbaranEntrada')
    albaranesSalida = MultipleJoin('AlbaranSalida')

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def parse_matricula(self):
        """
        Devuelve una tupla de dos elementos con la matrícula del 
        vehículo tractor en primer lugar y la del semirremolque en segundo.
        Si no se puede parsear o determinar alguna de las dos, devuelve 
        la segunda posición con la cadena vacía.
        """
        # TODO: Con expresiones regulares esto iría mejor.
        if "  " in self.matricula:
            try:
                t, s = [i.strip() for i in self.matricula.split("  ") if i.strip() != ""]
            except Exception, msg:
                if DEBUG: 
                    print "pclases::transportista::parse_matricula -> %s" % msg
                t = self.matricula.split("  ")[0].strip()
                s = "".join(self.matricula.split("  ")[1:]).strip()
        elif " " in self.matricula:
            t = self.matricula.split(" ")[0].strip()
            s = "".join(self.matricula.split(" ")[1:]).strip()
            if len(t) <= 3 or len(s) <= 3:
                t += " "
                t += s
                s = ""
        else:
            t = self.matricula.strip()
            s = ""
        return (t, s)

class Tarifa(SQLObject, PRPCTOO):
    precios = MultipleJoin('Precio')
    clientes = MultipleJoin('Cliente')
    pedidosVenta = MultipleJoin('PedidoVenta')
    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def esta_vigente(self, fecha = datetime.datetime.now()):
        """
        Devuelve True si la tarifa está vigente en la 
        fecha recibida.
        """
        res = True
        res = res and (self.periodoValidezIni == None 
                        or fecha >= self.periodoValidezIni)
        res = res and (self.periodoValidezFin == None 
                        or fecha <= self.periodoValidezFin)
        return res

    vigente = property(esta_vigente, doc = esta_vigente.__doc__)

    def esta_en_tarifa(self, producto):
        """
        Devuelve True si el producto está explícitamente en la tarifa.
        """
        if isinstance(producto, ProductoCompra):
            precios = Precio.select(AND(
                        Precio.q.productoCompra == producto.id, 
                        Precio.q.tarifa == self.id))
            if precios.count() == 1:
                return True
            elif precios.count() > 1:
                print "WARNING: pclases.py: obtener_precio: Más de un precio para una misma tarifa y producto de compra."
                return True
        else:
            raise TypeError, "producto debe ser un ProductoCompra."
        return False

    def obtener_precio(self, 
                       producto, 
                       precio_defecto = None, 
                       tarifa_defecto = None, 
                       sincronizar = True):
        """
        Dado un producto devuelve el precio que tiene en la
        tarifa. Si el producto no está incluido en la tarifa
        devuelve el precio por defecto de dicho producto.
        Si defecto != None, devuelve el precio por defecto recibido 
        en lugar del precio por defecto.
        Si tarifa_defecto != None y precio == None, entonces devuelve 
        el precio para la tarifa_defecto.
        Si sincronizar es False omite el sync antes de consultar el precio, 
        lo cual puede significar que el precio devuelto no sea correcto si 
        ha habido actualizaciones recientes desde otro puesto de trabajo. Se 
        deja la opción de desactivar el sync para consultas masivas de 
        precios al listar tarifas, ya que las tarifas no sueles modificarse 
        tan frecuentemente como para sincronizar en esos casos puntuales 
        (como por ejemplo, en la consulta valor_almacen.py, donde ahorra 
        mucho tiempo -dependiendo, sobre todo, de la red- en la consulta 
        y el riesgo de obtener un valor total erróneo para las valoraciones 
        es mínimo).
        """
        # PLAN: Faltaría un método o algo para saber si el producto 
        # finalmente estaba o no en la tarifa.
        if isinstance(producto, ProductoCompra):
            precios = Precio.select(AND(
                        Precio.q.productoCompra == producto.id, 
                        Precio.q.tarifa == self.id))
            if precios.count() == 1:
                precio = precios[0]
                if sincronizar:
                    precio.sync()
                precio = precio.precio
            elif precios.count() > 1:
                print "WARNING: pclases.py: obtener_precio: " \
                      "Más de un precio para una misma tarifa y producto de " \
                      "compra."
                precio = precios[0]
                if sincronizar:
                    precio.sync()
                precio = precio.precio
            else:
                if precio_defecto != None:
                    precio = precio_defecto
                elif tarifa_defecto != None:
                    precio = tarifa_defecto.obtener_precio(producto)
                else:
                    precio = producto.precioDefecto
        else:
            raise TypeError, "producto debe ser un ProductoCompra."
        return precio

    def get_porcentaje(self, producto, fraccion = False, precio_cache = None):
        """
        Devuelve el porcentaje de la tarifa sobre el precio por defecto del 
        producto.
        """
        if precio_cache == None:
            preciotarifa = self.obtener_precio(producto)
        else:
            preciotarifa = precio_cache
        try:
            porcentaje = 100.0 * ((preciotarifa / producto.precioDefecto) - 1)
        except ZeroDivisionError:
            porcentaje = 0.0
        if fraccion:
            porcentaje /= 100.0
        return porcentaje

    def asignarTarifa(self, producto, precio):
        """
        Si el producto ya tiene un precio asignado a la tarifa
        lo cambia por el precio recibido.
        Si no, crea un registro intermedio y relaciona el 
        producto con la tarifa.
        Devuelve el precio del producto para la tarifa asignado 
        finalmente o un código de error que es:
            -1 si no tenía precio y no se pudo crear.
            -2 si tenía precio pero no se pudo actualizar.
        """
        if isinstance(producto, ProductoCompra):
            criterio = AND(Precio.q.productoCompra == producto.id, 
                           Precio.q.tarifa == self.id)
        else:
            raise TypeError, "El producto debe ser un objeto de ProductoCompra."
        precios = Precio.select(criterio)
        if precios.count() == 0:
            # Crear registro
            if isinstance(producto, ProductoCompra):
                try:
                    reg_precio = Precio(productoCompra = producto, 
                                        tarifa = self,
                                        precio = precio)
                except: # Supongo que por no estar el precio en flotante.
                    return -1
        else:
            # Actualizarlo
            reg_precio = precios[0] 
            # No debería haber más de uno. Si lo hay, me quedo con el primero.
            try:
                reg_precio.precio = precio
            except:
                # ERROR: El precio no se puede convertir a flotante.
                return -2
        reg_precio.syncUpdate()
        return reg_precio.precio

    def get_tarifa_defecto():
        """
        Devuelve la tarifa por defecto (venta público o tarifa1).
        None si no hay tarifa por defecto para PVP.
        """
        try:
            tarifa = Tarifa.select(Tarifa.q.nombre.contains("Tarifa venta"))[0]
        except IndexError:
            try:
                tarifa = Tarifa.select(Tarifa.q.nombre.contains("arifa 1"))[0]
            except IndexError:
                try:
                    tarifa=Tarifa.select(Tarifa.q.nombre.contains("enta p"))[0]
                except IndexError:
                    tarifa = None
        return tarifa

    get_tarifa_defecto = staticmethod(get_tarifa_defecto)

class Precio(SQLObject, PRPCTOO):
    
    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_producto(self):
        """
        Devuelve el producto (de compra o de venta) relacionado 
        con el precio de tarifa actual.
        """
        if self.productoCompraID != None:
            return self.productoCompra
        else:
            return None

    def set_producto(self, producto):
        if isinstance(producto, ProductoCompra): 
            self.productoCompra = producto
        else:
            raise TypeError, 'El parámetro "producto" debe ser del tipo '\
                             'ProductoCompra.'

    producto = property(get_producto, set_producto, "Producto relacionado con el precio de tarifa.")

class CentroTrabajo(SQLObject, PRPCTOO):
    empleados = MultipleJoin('Empleado')
    
    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)


class Empleado(SQLObject, PRPCTOO):
    documentos = MultipleJoin('Documento')
    actividades = MultipleJoin("Actividad")
    fotos = MultipleJoin("Foto")
    gruposAlumnos = MultipleJoin("GrupoAlumnos")
    
    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_nombre_completo(self):
        """
        Devuelve el nombre del empleado en la forma 'apellidos, nombre'
        """
        return "%s, %s" % (self.apellidos, self.nombre)
    
    def es_profesor(self):
        """
        Devuelve True si el empleado es un profesor (su categoría laboral 
        tiene activada la propiedad "da clases").
        """
        return self.categoriaLaboral and self.categoriaLaboral.daClases

    def get_gdk_color_params(self):
        """
        Devuelve los parámetros de un gtk.gdk.Color correspondiente al color 
        RGB de la categoría.
        Las componentes RGB de la categoria van de 0 a 255. Se escalarán al 
        rango del gdk.Color que llega hasta 65535.
        """
        factor_escala = 65535.0 / 255
        r = int(self.colorR * factor_escala)
        g = int(self.colorG * factor_escala)
        b = int(self.colorB * factor_escala)
        pixel = 0   # No sé para qué usa gtk este valor.
        return (r, g, b, pixel)

    def set_gdk_color_params(self, r, g, b):
        """
        Establece los valores R, G, B en la escala 0..255 a partir de los 
        valores recibidos (en escala 0..65535).
        """
        factor_escala = 255.0 / 65535
        r = int(r * factor_escala)
        g = int(g * factor_escala)
        b = int(b * factor_escala)
        self.colorR = r
        self.colorG = g
        self.colorB = b


class Usuario(SQLObject, PRPCTOO):
    permisos = MultipleJoin('Permiso')
    alertas = MultipleJoin('Alerta')
    estadisticas = MultipleJoin('Estadistica')
    listasObjetosRecientes = MultipleJoin("ListaObjetosRecientes")
    empleados = MultipleJoin("Empleado")

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_permiso(self, ventana):
        """
        Devuelve el registro permiso del usuario sobre 
        la ventana "ventana" o None si no se encuentra.
        """
        try:
            # return [p for p in self.permisos if p.ventana == ventana][0]
            query = """
                    SELECT id FROM permiso 
                    WHERE ventana_id = %d AND usuario_id = %d;
                    """ % (ventana.id, self.id)
            id = sqlhub.getConnection().queryOne(query)[0]
            permiso = Permiso.get(id)
            return permiso
        except (IndexError, TypeError):
            return None

    def enviar_mensaje(self, texto, permitir_duplicado = False):
        """
        Envía un nuevo mensaje al usuario creando una 
        alerta pendiente para el mismo.
        Si permitir_duplicado es False, se buscan los mensajes 
        con el mismo texto que se intenta enviar. En caso de 
        que exista, solo se actualizará la hora de la alerta 
        y se pondrá el campo "entregado" a False.
        Si es True, se envía el nuevo mensaje aunque pudiera 
        estar duplicado.
        """
        mensajes = Alerta.select(AND(Alerta.q.mensaje == texto, 
                                     Alerta.q.usuario == self.id))
        if not permitir_duplicado:
            for m in mensajes:
                m.destroySelf()
        a = Alerta(usuario = self, mensaje = texto, entregado = False)

    def cambiar_password(self, nueva):
        """
        Cambia la contraseña por la nueva recibida.
        """
        from hashlib import md5
        self.passwd = md5(nueva).hexdigest()
        self.syncUpdate()

    def get_comerciales(self):
        """
        Devuelve una lista de objetos comerciales relacionados con el 
        usuario a través del registro empleados.
        """
        res = []
        for e in self.empleados:
            for c in e.comerciales:
                if c not in res:
                    res.append(c)
        return res

    # Decoradores de SQLObject:
    _get = lambda cls, id, c, sr: cls.get(cls, id, c, sr)
    def getget(cls, id, connection = None, selectResults = None):
        print "Mira, mamá, sin suerte."
        Usuario._get(Usuario, id, connection, selectResults)
    getget = classmethod(getget)


class Modulo(SQLObject, PRPCTOO):
    ventanas = MultipleJoin('Ventana')

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

class Ventana(SQLObject, PRPCTOO):
    permisos = MultipleJoin('Permiso')
    estadisticas = MultipleJoin('Estadistica')
    listasObjetosRecientes = MultipleJoin("ListaObjetosRecientes")

    class sqlmeta:
        fromDatabase = True
    
    def _init(self, *args, **kw):
        starter(self, *args, **kw)

class Permiso(SQLObject, PRPCTOO):

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

class Alerta(SQLObject, PRPCTOO):

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

class DatosDeLaEmpresa(SQLObject, PRPCTOO):

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_ruta_completa_logo(self):
        """
        Devuelve la ruta completa al logotipo de datos de la empresa.
        Si no tiene logo, devuelve None.
        """
        im = os.path.join("..", "imagenes", self.logo)
        return os.path.abspath(im)

    def get_propia_empresa_como_cliente(clase):
        """
        Devuelve el registro cliente de la BD que se corresponde 
        con la empresa atendiendo a los datos del registro DatosDeLaEmpresa
        o None si no se encuentra.
        """
        nombre_propia_empresa = clase.select()[0].nombre
        clientes = Cliente.select(Cliente.q.nombre == nombre_propia_empresa)
        if clientes.count() == 0:
            cliente = None
        elif clientes.count() == 1:
            cliente = clientes[0]
        else:   # >= 2
            print "pclases.py: DatosDeLaEmpresa::get_propia_empresa_como_cliente: Más de un posible cliente encontrado. Selecciono el primero."
            cliente = clientes[0]
        return cliente

    def get_propia_empresa_como_proveedor(clase):
        """
        Devuelve el registro proveedor que se corresponde con la 
        empresa atendiendo a los datos del registro DatosDeLaEmpresa 
        o None si no se encuentra.
        """
        nombre_propia_empresa = clase.select()[0].nombre
        proveedores = Proveedor.select(Proveedor.q.nombre == nombre_propia_empresa)
        if proveedores.count() == 0:
            proveedor = None
        elif proveedores.count() == 1:
            proveedor = proveedores[0]
        else:   # >= 2
            print "pclases.py: DatosDeLaEmpresa::get_propia_empresa_como_proveedor: Más de un posible proveedor encontrado. Selecciono el primero."
            proveedor = proveedores[0]
        return proveedor
    
    get_cliente = classmethod(get_propia_empresa_como_cliente)
    get_proveedor = classmethod(get_propia_empresa_como_proveedor)

    def str_cif_o_nif(self):
        """
        Devuelve la cadena "N.I.F." o "C.I.F." dependiendo de si el atributo 
        «cif» de la empresa es un N.I.F. (aplicable a personas) o C.I.F. 
        (aplicable a empresas).
        """
        try:
            return self.cif[0].isalpha() and "C.I.F." or "N.I.F."
        except IndexError:
            return ""

class CategoriaLaboral(SQLObject, PRPCTOO):
    empleados = MultipleJoin('Empleado')

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

class FestivoGenerico(SQLObject, PRPCTOO):

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

class TransporteACuenta(SQLObject, PRPCTOO):
    serviciosTomados = MultipleJoin('ServicioTomado')

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        """
        Además de constructor, comprueba la consistencia con 
        las facturas de compra. Si existe un registro (o varios)
        de servicioTomado relacionado con el transporte, éste 
        debe tener facturaCompra != None; en otro caso, se elimina.
        """
        starter(self, *args, **kw)
        self.__comprobar_si_facturado()

    def __comprobar_si_facturado(self):
        """
        Comprueba que si el transporte no está facturado, no tenga 
        registros "serviciosTomados". En caso de que los tenga sin 
        factura, los elimina.
        """
        for servicio in self.serviciosTomados:
            if servicio.facturaCompra == None:
                servicio.destroySelf()
    
    def facturar(self, facturaCompra):
        """
        Factura la transporte en la factura de compra recibida, creando
        el registro intermedio servicioTomado.
        Si "facturaCompra" es None, elimina la relación entre la factura 
        y la transporte.
        Devuelve el servicio recién creado o None si se eliminó.
        PRECONDICIÓN: "facturaCompra" debe ser un objeto de la clase 
                      FacturaCompra válido o None.
        """
        if facturaCompra != None:
            servicio = ServicioTomado(#comision = None, 
                                      transporteACuenta = self, 
                                      facturaCompra = facturaCompra, 
                                      concepto = self.concepto, 
                                      precio = self.precio, 
                                      cantidad = 1, 
                                      descuento = 0)
        else:
            for servicio in self.serviciosTomados:
                servicio.destroySelf()
            servicio = None
        return servicio

class ServicioTomado(SQLObject, PRPCTOO):

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_subtotal(self, iva = False):
        """
        Devuelve el subtotal con o sin IVA (según se indique) de 
        la línea de compra: precio * cantidad - descuento.
        """
        res = self.cantidad * self.precio * (1 - self.descuento)
        if iva:
            res *= 1 + self.iva
        # Ahora el servicio tiene su propio IVA.
        #if iva and self.facturaCompraID: 
        #    res *= (1 + self.facturaCompra.iva)
        return res

    def _get_qconcepto(self):
        """
        Si el registro tiene una comisión relacionada, devuelve el 
        concepto de la comisión.
        Si tiene un transporte a cuenta, devuelve el del transporte 
        a cuenta.
        En otro caso, devuelve el concepto del registro.
        """
        #if self.comision != None:
        #    return self.comision.concepto
        if self.transporteACuenta != None:
            return self.transporteACuenta.concepto
        return self.concepto

    def _set_qconcepto(self, txt):
        """
        Si el registro tiene una comisión relacionada, guarda en su 
        concepto y en del mismo registro el texto recibido.
        Lo mismo con el transporte a cuenta.
        """
        self.concepto = txt
        #if self.comision != None:
        #    self.comision.concepto = self.concepto
        if self.transporteACuenta != None:
            self.transporteACuenta.concepto = self.concepto

    def _get_qcantidad(self):
        """
        Si el registro tiene una comisión relacionada, devuelve el 
        cantidad de la comisión.
        Si tiene un transporte a cuenta, devuelve el del transporte 
        a cuenta.
        En otro caso, devuelve el cantidad del registro.
        """
        #if self.comision != None or self.transporteACuenta != None:
        #    return 1    # Los transportes a cuenta y comisiones no tienen cantidad. 
        return self.cantidad

    def _set_qcantidad(self, txt):
        """
        Como transportes y comisiones no tienen cantidads, este método 
        simplemente ignora la cantidad recibida si existe alguna 
        de estas dos relaciones.
        """
        if not self.transporteACuenta: # and not self.comisionID:
            self.cantidad = txt    # Y si no es un valor válido, que SQLObject se encargue de lanzar la excepción.

    def _get_qprecio(self):
        """
        Si el registro tiene una comisión relacionada, devuelve el 
        precio de la comisión.
        Si tiene un transporte a cuenta, devuelve el del transporte 
        a cuenta.
        En otro caso, devuelve el precio del registro.
        """
        #if self.comision != None:
        #    return self.comision.precio
        if self.transporteACuenta != None:
            return self.transporteACuenta.precio
        return self.precio

    def _set_qprecio(self, txt):
        """
        Si el registro tiene una comisión relacionada, guarda en su 
        precio y en del mismo registro el texto recibido.
        Lo mismo con el transporte a cuenta.
        """
        # Si el precio recibido en txt no es correcto, ya se encargará SQLObject de disparar la 
        # excepción correspondiente.
        self.precio = txt
        #if self.comision != None:
        #    self.comision.precio = self.precio
        if self.transporteACuenta != None:
            self.transporteACuenta.precio = self.precio
    
    def _get_qdescuento(self):
        """
        Si el registro tiene una comisión relacionada, devuelve el 
        descuento de la comisión.
        Si tiene un transporte a cuenta, devuelve el del transporte 
        a cuenta.
        En otro caso, devuelve el descuento del registro.
        """
        #if self.comision != None: # or self.transporteACuenta != None:
        #    return 0    # Los transportes a cuenta y comisiones no tienen descuento. 
        return self.descuento

    def _set_qdescuento(self, txt):
        """
        Como transportes y comisiones no tienen descuentos, este método 
        simplemente ignora la cantidad recibida si existe alguna 
        de estas dos relaciones.
        """
        if not self.transporteACuenta: # and not self.comisionID:
            self.descuento = txt    # Y si no es un valor válido, que SQLObject se encargue de lanzar la excepción.

    qconcepto = property(_get_qconcepto, _set_qconcepto, doc = "Concepto del servicio, o del transporte o comisión relacionada si lo tuviera.")
    qcantidad = property(_get_qcantidad, _set_qcantidad, doc = "Cantidad del servicio, o del transporte o comisión relacionada si lo tuviera.")
    qprecio = property(_get_qprecio, _set_qprecio, doc = "Precio del servicio, o del transporte o comisión relacionada si lo tuviera.")
    qdescuento = property(_get_qdescuento, _set_qdescuento, doc = "Descuento del servicio, o del transporte o comisión relacionada si lo tuviera.")

class HistorialExistenciasCompra(SQLObject, PRPCTOO):

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

class Recibo(SQLObject, PRPCTOO):
    """
    Recibos bancarios para cobros a clientes.
    Incluye un vencimiento que en observaciones (lo que se muestra como 
    "forma de pago" en las facturas) llevará "Recibo bancario nº %d" % (self.numrecibo).
    """

    vencimientosCobro = MultipleJoin('VencimientoCobro')

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_next_numrecibo(clase_recibo, anno):
        """
        Devuelve el siguiente número de recibo disponible para 
        el ano «anno».
        """
        try:
            ultimo_recibo = clase_recibo.select(clase_recibo.q.anno == anno, orderBy = "-numrecibo")[0]
        except IndexError:
            return 1
        else:
            return ultimo_recibo.numrecibo + 1

    get_next_numrecibo = classmethod(get_next_numrecibo)

    def calcular_importe(self):
        """
        Devuelve un float con la suma de los vencimientos relacionados.
        """
        return sum([v.importe for v in self.vencimientosCobro])

    importe = property(calcular_importe, doc = calcular_importe.__doc__)

    def get_cliente(self):
        """
        Devuelve el cliente del recibo (cliente del primer 
        vencimiento relacionado. Todos deberían permanecer 
        al mismo).
        """
        cliente = None
        if self.vencimientosCobro:
            fra = self.vencimientosCobro[0].facturaVenta or self.vencimientosCobro[0].prefactura
            cliente = fra.cliente
        return cliente

    def get_facturas(self):
        """
        Devuelve una lista de facturas relacionadas con el 
        recibo a través de los vencimientos de cobro.
        """
        return [v.facturaVenta or v.prefactura for v in self.vencimientosCobro]

class CuentaBancariaCliente(SQLObject, PRPCTOO):
    """
    Cuenta Bancaria de un cliente.
    """
    recibos = MultipleJoin("Recibo")

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

class Documento(SQLObject, PRPCTOO):

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_ruta_base():
        """
        Devuelve la ruta del directorio que contiene los documentos adjuntos.
        Se asegura cada vez que es consultada que el directorio existe.
        """
        # Siempre se trabaja en un subdirectorio del raíz del programa. 
        # Normalmente formularios o framework.
        # Por tanto lo primero que hago es salir del subdirectorio para buscar 
        # el de documentos adjuntos.
        RUTA_BASE = os.path.join("..", config.get_dir_adjuntos())
        try:
            assert os.path.exists(RUTA_BASE)
        except AssertionError:
            os.mkdir(RUTA_BASE)
        return RUTA_BASE
    
    ruta_base = get_ruta_base = staticmethod(get_ruta_base)

    def get_ruta_completa(self):
        """
        Devuelve la ruta completa al fichero: directorio base + nombre del fichero.
        """
        return os.path.join(Documento.get_ruta_base(), self.nombreFichero)

    def copiar_a(self, ruta):
        """
        Copia el fichero del objeto a la ruta seleccionada.
        """
        import shutil
        try:
            shutil.copy(self.get_ruta_completa(), ruta)
            res = True
        except Exception, msg:
            print "pclases::Documento::copiar_a -> Excepción %s" % msg
            res = False
        return res
    
    def copiar_a_diradjuntos(ruta):
        """
        Copia el fichero de la ruta al directorio de adjuntos.
        """
        import shutil
        try:
            shutil.copy(ruta, Documento.get_ruta_base())
            res = True
        except Exception, msg:
            print "pclases::Documento::copiar_a_diradjuntos -> Excepción %s" % msg
            res = False
        return res

    copiar_a_diradjuntos = staticmethod(copiar_a_diradjuntos)

    def adjuntar(ruta, objeto, nombre = ""):
        """
        Adjunta el fichero del que recibe la ruta con el objeto
        del segundo parámetro.
        Si no puede determinar la clase del objeto o no está 
        soportado en la relación, no crea el registro documento
        y devuelve None.
        En otro caso devuelve el objeto Documento recién creado.
        """
        res = None
        if objeto != None and os.path.exists(ruta):
            pedidoVenta = albaranSalida = facturaVenta = prefactura = \
            pedidoCompra = albaranEntrada = facturaCompra = \
            cliente = proveedor = empleado = \
            pagarePago = pagareCobro = None
            if isinstance(objeto, PedidoVenta):
                pedidoVenta = objeto
            elif isinstance(objeto, AlbaranSalida):
                albaranSalida = objeto
            elif isinstance(objeto, FacturaVenta):
                facturaVenta = objeto
            elif isinstance(objeto, Prefactura):
                prefactura = objeto
            elif isinstance(objeto, PedidoCompra):
                pedidoCompra = objeto
            elif isinstance(objeto, AlbaranEntrada):
                albaranEntrada = objeto
            elif isinstance(objeto, FacturaCompra):
                facturaCompra = objeto
            elif isinstance(objeto, Empleado):
                empleado = objeto
            elif isinstance(objeto, Cliente):
                cliente = objeto
            elif isinstance(objeto, Proveedor):
                proveedor = objeto
            elif isinstance(objeto, PagareCobro):
                pagareCobro = objeto
            elif isinstance(objeto, PagarePago):
                pagarePago = objeto
            else:
                raise TypeError, "pclases::Documento::adjuntar -> %s no es un tipo válido." % type(objeto)
            nombreFichero = os.path.split(ruta)[-1]
            if Documento.copiar_a_diradjuntos(ruta):
                nuevoDoc = Documento(nombre = nombre, 
                                     nombreFichero = nombreFichero, 
                                     pedidoVenta = pedidoVenta, 
                                     albaranSalida = albaranSalida, 
                                     facturaVenta = facturaVenta, 
                                     prefactura = prefactura,
                                     pedidoCompra = pedidoCompra, 
                                     albaranEntrada = albaranEntrada, 
                                     facturaCompra = facturaCompra, 
                                     cliente = cliente, 
                                     proveedor = proveedor, 
                                     empleado = empleado, 
                                     pagareCobro = pagareCobro, 
                                     pagarePago = pagarePago)
                res = nuevoDoc
        return res

    adjuntar = staticmethod(adjuntar)

class Estadistica(SQLObject, PRPCTOO):

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def incrementar(usuario, ventana):
        if isinstance(usuario, int):
            usuario_id = usuario
        else:
            usuario_id = usuario.id
        if isinstance(ventana, int):
            ventana_id = ventana
        elif isinstance(ventana, str):
            try:
                ventana = Ventana.selectBy(fichero = ventana)[0]
                ventana_id = ventana.id
            except Exception, msg:
                print "pclases::Estadistica::incrementar -> Ventana '%s' no encontrada. Excepción: %s" % (ventana, msg)
                return
        else:
            ventana_id = ventana.id
        st = Estadistica.select(AND(Estadistica.q.usuario == usuario_id, Estadistica.q.ventana == ventana_id))
        if not st.count():
            st = Estadistica(usuario = usuario_id, 
                             ventana = ventana_id)
        else:
            if st.count() > 1:
                sts = list(st)
                st = sts[0]
                for s in sts[1:]:
                    st.veces += s.veces
                    s.destroySelf()
            st = st[0]
        st.ultimaVez = datetime.datetime.now()
        st.veces += 1
        st.sync()

    incrementar = staticmethod(incrementar)

class ListaObjetosRecientes(SQLObject, PRPCTOO):
    idsRecientes = MultipleJoin("IdReciente")

    MAX_RECIENTES = 5

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def push(self, id):
        """
        Añade un objeto reciente a la lista de IDs si no estaba ya.
        Mantiene siempre la lista con un máximo de MAX_RECIENTES elementos.
        """
        if id not in [i.objetoID for i in self.idsRecientes]:
            if len(self.idsRecientes) >= self.MAX_RECIENTES:
                self.pop()
        else:
            self.pop(id)
        idr = IdReciente(listaObjetosRecientes = self, objetoID = id)

    def pop(self, id = None):
        """
        Si se recibe un ID y éste está en la lista, lo saca y lo devuelve.
        En otro caso saca de la pila el que tenga ID más bajo (es decir, el 
        más antiguo).
        """
        if id != None:
            if id not in [r.objetoID for r in self.idsRecientes]:
                raise ValueError, "ID %d no está en la lista de ids recientes."
            idr = [r for r in self.idsRecientes if r.objetoID == id][0]
            idr.destroySelf()
            res_id = id
        else:
            if len(self.idsRecientes) == 0:
                raise ValueError, "Lista de ids recientes vacía."
            idrs = [r for r in self.idsRecientes]
            idrs.sort(lambda r1, r2: int(r1.id - r2.id))
            idr = idrs[0]
            res_id = idr.objetoID
            idr.destroySelf()
        return res_id

    def get_lista(self):
        """
        Devuelve una lista de IDs ordenada por id del registro.
        """
        idrs = [r for r in self.idsRecientes]
        idrs.sort(lambda r1, r2: int(r1.id - r2.id))
        return [r.objetoID for r in idrs]

    def buscar(clase, ventana, usuario = None, crear = False):
        """
        Devuelve el registro que coincide con el usuario y ventana recibidos.
        None si no se encontró ninguno.
        El primero de todos si se encontraron varios.
        Si «usuario» es None, se aplica en la búsqueda como None. «ventana» no 
        puede ser None. Sí puede ser una cadena, en cuyo caso se buscará 
        primero si la ventana existe en la BD como registro.
        Si «crear» es True, en lugar de devolver None crea un registro nuevo.
        """
        if isinstance(ventana, str):
            try:
                ventana = Ventana.select(Ventana.q.fichero == ventana)[0]
            except IndexError:
                raise ValueError, "%s no es una ventana válida en la BD" % (
                    ventana)
        if usuario != None:
            uid = usuario.id
        else:
            uid = None
        rs = clase.select(AND(clase.q.usuario == uid, 
                              clase.q.ventana == ventana.id), 
                          orderBy = "id")
        try:
            return rs[0]
        except:
            if not crear:
                res = None
            else:
                nuevo = clase(ventana = ventana, usuario = usuario)
                res = nuevo
        return res

    buscar = classmethod(buscar)

class IdReciente(SQLObject, PRPCTOO):

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

## Clases propias de Universal Pilates
class Asistencia(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

class Maquina(SQLObject, PRPCTOO):
    actividades = RelatedJoin('Actividad')
    class sqlmeta:
        fromDatabase = True
    def _init(self, *args, **kw):
        starter(self, *args, **kw)

class Actividad(SQLObject, PRPCTOO):
    asistencias = MultipleJoin("Asistencia")
    clientes = RelatedJoin('Cliente')
    maquinas = RelatedJoin('Maquina')

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def DEPRECATED_buscar_actividades_de(cliente=None, fechaini=None, 
                                         fechafin=None):
        """
        Busca actividades para donde aparezca el cliente entre las fechas 
        indicadas (si se indica alguno de esos tres parámetros).
        Devuelve un SQLlist.
        """
        A = Actividad
        if fechaini and fechafin:
            acts = A.select(
              NOT(AND(
                A.q.fechahoraFin < fechaini, 
                A.q.fechahoraInicio > fechafin + datetime.timedelta(days = 1))) 
              )
        elif not fechaini and fechafin:
            acts = A.select(
              A.q.fechahoraInicio <= fechafin + datetime.timedelta(days = 1) 
              )
        elif fechaini and not fechafin:
            acts = A.select(
              A.q.fechahoraFin >= fechaini
              )
        else:
            acts = A.select()
        if cliente:
            acts = [a for a in acts if cliente in a.clientes]
        acts = SQLlist(acts)
        return acts

    def buscar_actividades_de(cliente=None, fechaini=None, fechafin=None):
        """
        Busca actividades para donde aparezca el cliente entre las fechas 
        indicadas (si se indica alguno de esos tres parámetros).
        Devuelve un SQLlist.
        """
        sql = """
        SELECT
            actividad.id
        FROM
            actividad, actividad_cliente
        WHERE
            actividad_cliente.actividad_id = actividad.id
        """
        if cliente:
            sql += " AND actividad_cliente.cliente_id = %d " % cliente.id
        if fechaini and fechafin:
            sql += """ AND NOT(actividad.fechahora_fin < '%s' AND 
                               actividad.fechahora_inicio > '%s')
            """ % (utils.fecha2sql(fechaini), 
                   utils.fecha2sql(fechafin + datetime.timedelta(days = 1)))
        elif fechafin:
            sql += " AND actividad.fechahora_inicio <= '%s' " % (
                utils.fecha2sql(fechafin + datetime.timedelta(days = 1)))
        elif fechaini: 
            sql += " AND actividad.fechahora_fin >= '%s' " % (
                utils.fecha2sql(fechaini))
        sql += ";"
        if DEBUG:
            print " >>> pclases::Actividad:buscar_actividades_de -> sql"
            print sql
        acts = SQLlist([Actividad.get(tupla[0]) 
                        for tupla in Actividad._connection.queryAll(sql)])
        if DEBUG:
            print " <<< %d registros." % len(acts)
        return acts
    
    buscar_actividades_de = staticmethod(buscar_actividades_de)
    DEPRECATED_buscar_actividades_de = staticmethod(
                                            DEPRECATED_buscar_actividades_de)

    def get_or_guess_productoCompra(self, cliente = None):
        """
        Devuelve el producto de compra de tipo clase relacionado con la 
        actividad a través del cliente(s).
        Si no tiene aún un producto relacionado, intenta adivinarlo.
        El único criterio para distinguir los productos es sin son clases 
        privadas o no. 
        En el momento en que un cliente contrate más de un producto con clases 
        del mismo tipo, devolverá el primero de ellos.
        """
        # FIXME: Este último párrafo hay que pensarlo mejor. Podría usar 
        # también la fecha de contratación para discernir entre los productos 
        # contratados por el cliente, si ya ha agotado en otras actividades 
        # el sugerido en primer lugar, etc.
        
        if self.productoCompraID:
            return self.productoCompra
        else:
            posibles = []
            es_privada = len(self.clientes) == 1
            for c in self.clientes:
                if cliente and c != cliente:
                    continue
                for p in c.productosContratados:
                    pc = p.productoCompra
                    for c in pc.clases:
                        if es_privada and c.es_privada():
                            return pc   # Ya lo he encontrado.
                        elif not es_privada and not c.es_privada():
                            return pc   # Lo encontré también
            return None

    #productoCompra = property(get_or_guess_productoCompra, 
    #                          doc = 'Producto de tipo clase relacionado '
    #                                'con la actividad.')

    def asistio(self, cliente):
        """
        Devuelve True si el cliente asistió a la clase.
        """
        for a in self.asistencias:
            if a.cliente == cliente:
                return True
        return False

    def get_gruposAlumnos(self, resultado_unico = False):
        """
        Devuelve una lista con los grupos a los que pertenecen (no en lista 
        de espera) los alumnos de esta actividad.
        """
        grupos = {}
        for c in self.clientes:
            for grupo in c.gruposAlumnos:
                if grupo not in grupos and not grupo.en_lista_de_espera(c):
                    try:
                        grupos[grupo] += 1
                    except KeyError:
                        grupos[grupo] = 1
        if not resultado_unico:
            res = grupos.keys()
        else:   # Devuelve el grupo que más gente tiene de todos los que 
                # están implicados en la actividad a través de sus alumnos o 
                # cuyo nombre sea idéntico a la descripción de la actividad. 
            res = None
            for grupo in grupos:
                normalize = lambda x: x.strip().upper()
                if normalize(self.descripcion) == normalize(grupo.nombre):
                    res = grupo
            if not res:
                # Esta ordenación es necesaria para que sea determinista:
                claves = grupos.keys()
                claves.sort(key = lambda x: x.id)
                maximo = 0
                for grupo in claves:
                    if grupos[grupo] >= maximo:
                        res = grupo
                        maximo = grupos[grupo]
        return res

    gruposAlumnos = property(get_gruposAlumnos, doc = get_gruposAlumnos.__doc__)
    grupoAlumnos = property(
        lambda self: self.get_gruposAlumnos(resultado_unico = True))

    def esta_facturado_para(self, cliente):
        """
        Devuelve True si la actividad está facturada para el cliente.
        Lo estará si existe un servicio que los relacione a través de una 
        factura.
        """
        return self.servicioID and self.servicio.get_cliente() == cliente

    def calcular_duracion(self):
        """
        Devuelve la duración en horas de la actividad.
        """
        dif = self.fechahoraFin - self.fechahoraInicio
        horas = dif.seconds / (60.0 * 60)
        horas += dif.days * 24
        return horas

    def get_fecha_hora_y_descripcion(self):
        """
        Devuelve una cadena con la hora y la descripción de la actividad.
        """
        cad = "%s: %s %s" % (utils.str_fecha(self.fechahoraInicio), 
                             self.get_str_horas(), self.descripcion)
        return cad

    def get_hora_y_descripcion(self):
        """
        Devuelve una cadena con la hora y la descripción de la actividad.
        """
        cad = "%s %s" % (self.get_str_horas(), self.descripcion)
        return cad

    def get_str_horas(self):
        """
        Devuelve una cadena con las horas de inicio y fin en el formato 
        [HH:MM - HH:MM].
        """
        return "[%s - %s]" % (utils.str_hora_corta(self.fechahoraInicio), 
                              utils.str_hora_corta(self.fechahoraFin))

    def get_txtinfoactividad(self, incluir_asistentes = True, 
                             tratar_como_grupo_unico = True):
        """
        Devuelve la información de la actividad como texto.
        Si tratar_como_grupo_unico es True devolverá la información haciendo 
        referencia a un único grupo (el más repetido de entre todos los 
        alumnos) aunque haya alumos con más de un grupo.
        """
        txttooltip = "%s. De %s a %s: %s" % (
            utils.str_fecha(self.fechahoraInicio), 
            utils.str_hora_corta(self.fechahoraInicio), 
            utils.str_hora_corta(self.fechahoraFin), 
            self.descripcion)
        mons = self.empleado and self.empleado.get_nombre_completo() or ""
        asistentes = []
        total = 0
        grupos_tratados = []
        for c in self.clientes:
            for grupo in c.get_grupos():
                if grupo and grupo not in grupos_tratados:
                    total += grupo.cupo
                    asistentes.append(" * %s (%s)" % (c.nombre, grupo.nombre))
                    grupos_tratados.append(grupo)
                else:
                    asistentes.append(" * %s" % c.nombre)
        if tratar_como_grupo_unico:
            total = self.grupoAlumnos and self.grupoAlumnos.cupo or 0
        asis = "\n".join(asistentes)
        #if len(asistentes) == 1:
        if len(self.clientes) == 1:
            pax = "priv."
        elif len(self.clientes) == 2:
            pax = "semipriv."
        else:
            #pax = "%d/%d" % (len(asistentes), total)
            pax = "%d/%d" % (len(self.clientes), total)
        if incluir_asistentes:
            txttooltip += "\nMonitor: %s\nAsistentes [%s]:\n%s" % (
                mons, pax, asis)
        else:
            # Ahora los asistentes van en un TV aparte, no van en el texto.
            txttooltip += "\nMonitor: %s\nAsistentes [%s]" % (mons, pax)
        return txttooltip

    def get_precio(self, cliente = None, precio_defecto = 0.0):
        """
        Devuelve el precio al que se factura actualmente la actividad al 
        cliente recibido. Si no se puede determinar el producto de compra para 
        identificar el precio, se usará el proporcionado por defecto. Si no 
        se recibe cliente, se devolverá el precio para la tarifa por 
        defecto.
        """
        if cliente and cliente.tarifa:
            tarifa = cliente.tarifa
        else:
            tarifa = Tarifa.get_tarifa_defecto()
        try:
            if tarifa:
                importe = cliente.tarifa.obtener_precio(
                    self.get_or_guess_productoCompra())
            else:
                importe = self.get_or_guess_productoCompra().precioDefecto
        except AttributeError:  # No se pudo determinar el producto.
            importe = precio_defecto
        return importe

class GrupoAlumnos(SQLObject, PRPCTOO):
    clientes = RelatedJoin("Cliente")
    class sqlmeta:
        fromDatabase = True
    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def en_lista_de_espera(self, cliente):
        """
        Devuelve True si el cliente está en lista de espera para este grupo.
        """
        # ¿Cuál es el criterio? El orden en la lista de clientes.
        return self.clientes.index(cliente) >= self.cupo

    def get_alumnos(self):
        """
        Devuelve una lista de clientes que NO están en lista de espera para 
        el grupo.
        """
        res = [c for c in self.clientes if not self.en_lista_de_espera(c)]
        return res

    def get_gdk_color_params(self):
        """
        Devuelve los parámetros de un gtk.gdk.Color correspondiente al color 
        RGB de la categoría.
        Las componentes RGB de la categoria van de 0 a 255. Se escalarán al 
        rango del gdk.Color que llega hasta 65535.
        """
        factor_escala = 65535.0 / 255
        r = int(self.colorR * factor_escala)
        g = int(self.colorG * factor_escala)
        b = int(self.colorB * factor_escala)
        pixel = 0   # No sé para qué usa gtk este valor.
        return (r, g, b, pixel)

    def set_gdk_color_params(self, r, g, b):
        """
        Establece los valores R, G, B en la escala 0..255 a partir de los 
        valores recibidos (en escala 0..65535).
        """
        factor_escala = 255.0 / 65535
        r = int(r * factor_escala)
        g = int(g * factor_escala)
        b = int(b * factor_escala)
        self.colorR = r
        self.colorG = g
        self.colorB = b

    def get_actividades_pendientes(self):
        """
        Devuelve las actividades del grupo que aún no se han dado.
        """
        ahora = datetime.datetime.now()
        # Las actividades del grupo son aquellas en las que están inscritos 
        # sus alumnos:
        actividades = self.get_actividades()
        pendientes = [a for a in actividades if a.fechahoraInicio > ahora] 
        return pendientes

    def get_actividades(self):
        """
        Devuelve una lista de actividades en las que participa el grupo a 
        través de sus alumnos.
        OJO: O(n^2)
        """
        actividades = []
        for c in self.clientes:
            for a in c.actividades:
                if a not in actividades:
                    actividades.append(a)
        return actividades

class Categoria(SQLObject, PRPCTOO):
    tareas = MultipleJoin("Tarea")
    memos = MultipleJoin("Memo")
    class sqlmeta:
        fromDatabase = True
    def _init(self, *args, **kw):
        starter(self, *args, **kw)
    def get_gdk_color_params(self):
        """
        Devuelve los parámetros de un gtk.gdk.Color correspondiente al color 
        RGB de la categoría.
        Las componentes RGB de la categoria van de 0 a 255. Se escalarán al 
        rango del gdk.Color que llega hasta 65535.
        """
        factor_escala = 65535.0 / 255
        r = int(self.colorR * factor_escala)
        g = int(self.colorG * factor_escala)
        b = int(self.colorB * factor_escala)
        pixel = 0   # No sé para qué usa gtk este valor.
        return (r, g, b, pixel)
    
    def set_gdk_color_params(self, r, g, b):
        """
        Establece los valores R, G, B en la escala 0..255 a partir de los 
        valores recibidos (en escala 0..65535).
        """
        factor_escala = 255.0 / 65535
        r = int(r * factor_escala)
        g = int(g * factor_escala)
        b = int(b * factor_escala)
        self.colorR = r
        self.colorG = g
        self.colorB = b

class Evento(SQLObject, PRPCTOO):
    actividades = MultipleJoin("Actividad")
    class sqlmeta:
        fromDatabase = True
    def _init(self, *args, **kw):
        starter(self, *args, **kw)
    def get_gdk_color_params(self):
        """
        Devuelve los parámetros de un gtk.gdk.Color correspondiente al color 
        RGB de la categoría.
        Las componentes RGB de la categoria van de 0 a 255. Se escalarán al 
        rango del gdk.Color que llega hasta 65535.
        """
        factor_escala = 65535.0 / 255
        r = int(self.colorR * factor_escala)
        g = int(self.colorG * factor_escala)
        b = int(self.colorB * factor_escala)
        pixel = 0   # No sé para qué usa gtk este valor.
        return (r, g, b, pixel)
    
    def set_gdk_color_params(self, r, g, b):
        """
        Establece los valores R, G, B en la escala 0..255 a partir de los 
        valores recibidos (en escala 0..65535).
        """
        factor_escala = 255.0 / 65535
        r = int(r * factor_escala)
        g = int(g * factor_escala)
        b = int(b * factor_escala)
        self.colorR = r
        self.colorG = g
        self.colorB = b

class Tarea(SQLObject, PRPCTOO):

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

class Memo(SQLObject, PRPCTOO):

    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)


class Foto(SQLObject): #, PRPCTOO):
    class sqlmeta:
        fromDatabase = True

    #def _init(self, *args, **kw):
    #    starter(self, *args, **kw)

    def _set_data(self, value):
        self._SO_set_data(value.encode('base64'))

    def _get_data(self):
        return self._SO_get_data().decode('base64')

    def save_to_temp(self):
        """
        Guarda la imagen en un temporal y devuelve la ruta a la misma.
        """
        # OJO: 1.- No chequea que no haya imagen almacenada.
        #      2.- No chequea que no exista una imagen con el mismo nombre o 
        #          que no pueda escribir a disco por falta de espacio, etc.
        from tempfile import gettempdir
        from random import randint 
        dir = gettempdir()
        nombre = "%d" % randint(10**9, 10**10 - 1) #+ self.extension
        #if self.extension:
        #    nombre = ".".join((nombre, self.extension))  # Para el PIL en Win
        ruta = os.path.join(dir, nombre)
        f = open(ruta, "wb")
        f.write(self.data)
        f.close()
        return ruta

    def to_pil(self):
        """
        Devuelve una imagen PIL a partir del BLOB guardado.
        """
        from PIL import Image
        #im = Image.new(self.modo, (self.ancho, self.alto))
        #im.fromstring(self.imagen)
        path_tmp_im = self.save_to_temp()
        im = Image.open(path_tmp_im)
        return im

    def store_from_file(self, ruta):
        """
        Guarda la imagen especificada por la ruta en la base de datos.
        """
        self.data = ""
        f = open(ruta, "rb")
        binchunk = f.read()
        while binchunk:
            self.data += binchunk
            binchunk = f.read()
        f.close()

    def store_from_pil(self, imagen):
        """
        Guarda la imagen del objeto PIL en la base de datos.
        """
        import Image
        # PLAN
        raise NotImplementedError


## XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX

def getObjetoPUID(puid):
    """
    Intenta determinar la clase del objeto a partir de la primera parte del 
    PUID y devuelve el objeto en sí o lanzará una excepción.
    """
    dict_clases = {"PC": ProductoCompra, 
                   "PAGC": PagareCobro, 
                   "PAGP": PagarePago, 
                   "CONF": Confirming, 
                   "COB": Cobro, 
                   "PAG": Pago, 
                  }
    tipo, id = puid.split(":")
    if tipo not in dict_clases:
        try:
            clase = eval(tipo)
        except:
            raise ValueError, "La primera parte del PUID debe ser: %s" % (
                ", ".join(dict_clases.keys()))
    else:
        clase = dict_clases[tipo]
    id = int(id)
    objeto = clase.get(id)
    return objeto

def func_orden_cargas_fecha(c1, c2):
    """
    Compara dos fechas entre dos cargas de silo.
    """
    if c1.fechaCarga < c2.fechaCarga:
        return -1
    if c1.fechaCarga > c2.fechaCarga:
        return 1
    return 0

def unificar(bueno, malos, borrar_despues = True):
    """
    Pasa todos los registros dependientes de cada objeto de «malos» a «bueno».
    Si borrar_despues es Verdadero, elimina los malos después de haber 
    unificado.
    Se comprueba que todos los objetos sean de la misma clase de pclases.
    """
    for malo in malos:
        assert malo.__class__ == bueno.__class__
    assert bueno not in malos
    nombreclase=str(bueno.__class__).split(".")[-1].split()[0]
    from string import letters
    nombreclase = [l for l in nombreclase 
                   if l in letters or l in "12344567890" or l in "_"]
    nombreclase = "".join(nombreclase)
    for malo in malos:
        for join in malo.sqlmeta.joins:
            lista = join.joinMethodName
            for dependiente in getattr(malo, lista):
                for col in dependiente.sqlmeta.columns:
                    if (isinstance(col, SOForeignKey) 
                        and col.foreignKey == nombreclase):
                        clave_ajena = col.name
                setattr(dependiente, clave_ajena, bueno.id)
                dependiente.syncUpdate()
    if borrar_despues:
        for malo in malos:
            malo.destroySelf()

def el_anecdoton(fecha):
    """
    Devuelve una lista de puids de objetos cuya fecha coincida con la 
    recibida.
    """
    res = []
    this_mod = __import__(__name__)
    clases_y_mas = [val.replace(__name__ + ".", "") for val in dir(this_mod)]
    for nombreitem in clases_y_mas:
        clase = eval(nombreitem)
        if DEBUG:
            print "clase", clase
        try:
            padres = clase.__bases__
            if DEBUG:
                print "padres", padres
        except AttributeError:
            padres = []
        if SQLObject in padres:
            dict_cols = clase.sqlmeta.columns
            for namecol in dict_cols:
                col = dict_cols[namecol]
                if isinstance(col, SODateCol):
                    res += buscar_puids_en_fecha(fecha, nombreitem, namecol)
                elif isinstance(col, SODateTimeCol):
                    res += buscar_puids_sobre_fecha(fecha, nombreitem, namecol)
    return res

def buscar_puids_en_fecha(fecha, nameclase, namecol):
    """
    Recibe una clase y un nombre de columna por el que buscar la fecha "fecha".
    Devuelve una lista de PUIDs coincidentes.
    """
    colbusqueda = nameclase + ".q." + namecol
    consulta = nameclase + ".select(%s == fecha)" % colbusqueda
    if DEBUG:
        print "consulta (buscar_puids_sobre_fecha)", consulta
    consulta = eval(consulta)
    puids = [o.get_puid() for o in consulta]
    return puids

def buscar_puids_sobre_fecha(fecha, nameclase, namecol):
    """
    Recibe una clase y un nombre de columna por el que buscar la fecha "fecha".
    Devuelve una lista de PUIDs coincidentes.
    """
    colbusqueda = nameclase + ".q." + namecol
    diasiguiente = fecha + datetime.timedelta(days = 1)
    consulta = nameclase + ".select(AND(%s >= fecha, %s < diasiguiente))" % (
        colbusqueda)
    if DEBUG:
        print "consulta (buscar_puids_sobre_fecha)", consulta
    consulta = eval(consulta)
    puids = [o.get_puid() for o in consulta]
    return puids

def get_formas_de_pago():
    """
    Devuelve una lista de cadenas con todas las formas de pago usadas 
    más algunas preconfiguradas (en realidad son documentos de pago, la 
    forma de pago establece los periodos, el documento el modo usado 
    para formalizar el pago).
    """
    res = ["EFECTIVO",  # = "CONTADO"
           "TARJETA", 
           "RECIBO", 
           "PAGARÉ", 
           "CONFIRMING", 
           "CHEQUE"]
    for cliente in Cliente.select():
        formadepago = cliente.documentodepago
        if formadepago and formadepago.upper().strip() not in res:
            res.append(formadepago)
    return tuple(res)


class ProductoVenta:
    """
    Es por compatibilidad con las facturas de venta. Cuando lo arregle allí, 
    se eliminará de aquí.
    """
    pass


if __name__ == '__main__':
    # Pruebas unitarias
    for clase in (
                  'FacturaCompra', 
                  'LineaDeCompra', 'VencimientoPago', 'Pago',  
                  'VencimientoCobro', 'PagarePago', 'Cobro', 'PagareCobro', 
                  'TipoDeMaterial', 'Proveedor', 
                  'LineaDeVenta', 'PedidoCompra', 'ProductoCompra', 
                  'AlbaranEntrada', 
                  'PedidoVenta', 
                  'AlbaranSalida', 
                  'Cliente', 'Contador', 
                  'FacturaVenta', 'Servicio', 'Transportista', 
                  'Tarifa', 'Precio', 'CentroTrabajo', 
                  'Empleado', 
                  'Usuario', 'Modulo', 
                  'Ventana', 'Permiso', 'Alerta', 'DatosDeLaEmpresa', 
                  'CategoriaLaboral', 
                  'FestivoGenerico', 
                  'TransporteACuenta', 'ServicioTomado', 
                  ):
        try:
            c = eval(clase)
            print "Buscando primer registro de %s... " % (clase),
            reg = c.select(orderBy="id")[0]
            print "[OK]"
        except IndexError:
            print "[KO] - La clase %s no tiene registros" % (clase)


