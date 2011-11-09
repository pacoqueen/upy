#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005, 2006 Francisco José Rodríguez Bogado,                   #
#                          (pacoqueen@users.sourceforge.net)                  #
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

import sys
import sqlobject, gtk
from utils import combo_set_from_db, \
                  str_fecha, \
                  str_fechahoralarga, \
                  str_hora, \
                  float2str, \
                  rellenar_lista
import datetime

DEBUG = False
NOMBRES_COLUMNAS_PORCENTAJE = ("iva", "descuento", "comision")

def setter_entry(objeto, col, w):
    """
    Muestra el valor del atributo "col" del objeto
    "objeto" en el entry "w".
    """
    valor = getattr(objeto, col.name)
    if isinstance(col, sqlobject.col.SODateCol):
        valor = str_fecha(valor)
    elif isinstance(col, sqlobject.col.SODateTimeCol):
        valor = str_fechahoralarga(valor)
    elif isinstance(col, sqlobject.col.SOTimeCol):
        valor = str_hora(valor)
    elif isinstance(col, sqlobject.col.SOFloatCol):
        # XXX
        # HACK: Workaround. Los valores que son porcentaje (descuentos e IVA) 
        # se deben mostrar con el símbolo "%", pero la única manera de 
        # distinguir esas columnas es mirar el nombre.
        if col.name in NOMBRES_COLUMNAS_PORCENTAJE:
            valor = "%s %%" % float2str(valor * 100,    
                                        precision = 5, 
                                        autodec = True)
        # XXX
        else:
            valor = float2str(valor, autodec = False)
            # Si autodec=True y es número redondo > 1000 escribe 1.000 y el 
            # getter lo interpreta como flotante.
    if not isinstance(valor, str):
        valor = str(valor)
    w.set_text(valor)

def setter_spinbutton(objeto, col, w):
    """
    Muestra el valor del atributo "col" del objeto
    "objeto" en el spinbutton "w".
    """
    valor = getattr(objeto, col.name)
    w.set_value(valor)

def setter_textview(objeto, col, w):
    """
    Muestra el valor del atributo "col" del objeto
    "objeto" en el textview "w".
    """
    valor = getattr(objeto, col.name)
    if isinstance(col, sqlobject.col.SODateCol):
        valor = str_fecha(valor)
    elif isinstance(col, sqlobject.col.SODateTimeCol):
        valor = str_fechahoralarga(valor)
    elif isinstance(col, sqlobject.col.SOTimeCol):
        valor = str_hora(valor)
    elif isinstance(col, sqlobject.col.SOFloatCol):
        # XXX
        # HACK: Workaround. Los valores que son porcentaje (descuentos e IVA) 
        # se deben mostrar con el símbolo "%", pero la única manera de 
        # distinguir esas columnas es mirar el nombre.
        if col.name in NOMBRES_COLUMNAS_PORCENTAJE:
            valor = "%s %%" % float2str(valor * 100, 
                                        precision = 5, 
                                        autodec = True)
        # XXX
        else:
            valor = float2str(valor, autodec = False)
            # Si autodec=True y es número redondo > 1000 escribe 1.000 y el 
            # getter lo interpreta como flotante.
    if not isinstance(valor, str):
        valor = str(valor)
    buf = w.get_buffer()
    buf.set_text(valor)

def setter_comboboxentry(objeto, col, w):
    """
    Muestra el valor del atributo "col" del objeto
    "objeto" en el entry hijo del combobox "w".
    """
    valor = getattr(objeto, col.name)
    # TODO: Comprobar qué tipo de SOCol es y convertir el valor si 
    #       es una fecha, un float, etc.
    combo_set_from_db(w, valor)

def setter_combobox(objeto, col, w):
    """
    Muestra el valor del atributo "col" del objeto
    "objeto" en el entry hijo del combobox "w".
    """
    valor = getattr(objeto, col.name)
    # TODO: Comprobar qué tipo de SOCol es y convertir el valor si 
    #       es una fecha, un float, etc.
    combo_set_from_db(w, valor)

def setter_checkbutton(objeto, col, w):
    """
    Muestra el valor de "col" del objeto como True/False en 
    el checkbutton recibido.
    """
    valor = getattr(objeto, col.name)
    w.set_inconsistent(False)
    try:
        w.set_active(valor)
    except (TypeError, ValueError), msg:
        sys.stderr.write('adapter.py::setter_checkbutton: "%s" no es un valor correcto para "%s". Excepción: %s'
            % (valor, w, msg))
        w.set_inconsistent(True)

def get_raw_value(w):
    if isinstance(w, gtk.Entry):
        res = w.get_text()
    elif isinstance(w, gtk.TextView):
        buf = w.get_buffer()
        res = buf.get_text(*buf.get_bounds())
    elif isinstance(w, (gtk.CheckButton, gtk.ToggleButton)):
        res = w.get_active()
    elif isinstance(w, (gtk.ComboBoxEntry, gtk.ComboBox)):
        pos = w.get_active()
        if pos > -1:
            res = w.get_model()[pos][0]
        else:
            res = ""
    else:
        raise TypeError, "adapter.py::get_raw_value: Widget %s no soportado."%w
    return res

def generic_getter(func_tratamiento, w):
    """
    Obtiene el valor bruto y una función de tratamiento.
    Devuelve una función que devuelve el valor después 
    de ser procesado.
    """
    valor_bruto = get_raw_value(w)
    return func_tratamiento(valor_bruto)

def convertir_a_entero(valor):
    """
    Convierte un valor a entero.
    Si es flotante, trunca.
    Si valor no es un texto o un número, devuelve 0 -especialmente 
    para None-.
    Si contiene texto, lo filtra y se queda con el primer
    entero que pueda formar.
    Si es una cadena vacía, también devuelve 0.
    En otro caso lanza una excepción de ValueError.
    """
    try:
        res = int(valor)
    except ValueError:
        if isinstance(valor, str) and valor.strip() == "":
            return 0
        import re
        reint = re.compile("[0-9]+")
        try:
            res = reint.findall(valor)[0]
        except (IndexError):
            raise TypeError
    except TypeError:
        res = 0
    return res

def convertir_a_flotante(valor, vdefecto = 0.0, col = None):
    """
    Devuelve el valor por defecto "vdefecto" en caso de excepción.
    Antes de lanzarla, prueba como número flotante y como flotante con 
    símbolo de porcentaje.
    Fuerza la comprobación de porcentaje si col es distinto de None y 
    está entre las columnas a tratar así.
    """
    from utils import _float, parse_porcentaje
    try:
        if col != None and col.name in NOMBRES_COLUMNAS_PORCENTAJE:
            raise Exception, "Forzando comprobación de porcentaje."
        return _float(valor)
    except:
        try:
            # 5 decimales de precisión es bastante para un porcentaje. Es lo 
            # que uso también para mostrar en pantalla (ver el getter arriba).
            return round(parse_porcentaje(valor, fraccion = True), 5)
        except:
            return vdefecto

def convertir_a_booleano(valor, vdefecto = False):
    try:
        return bool(valor)
    except:
        return vdefecto

def convertir_a_fechahora(valor, vdefecto = datetime.date.today()):
    from utils import parse_fechahora
    try:
        return parse_fechahora(valor)
    except:
        return vdefecto

def convertir_a_fecha(valor, vdefecto = datetime.date.today()):
    from utils import parse_fecha
    try:
        return parse_fecha(valor)
    except:
        return vdefecto

def convertir_a_hora(valor, vdefecto = datetime.date.today()):
    from utils import parse_hora
    try:
        return parse_hora(valor)
    except:
        return vdefecto

class Adaptador:
    """
    Pegamento para el MVC.
    Adapta y mantiene un diccionario de los adaptadores 
    entre el modelo y la vista. Cada campo sabrá cómo 
    debe mostrarse en pantalla y con qué widget, así como 
    la manera de leer su valor de la vista y guardarlo 
    en el modelo.
    """
    TUPLATEXTO = (gtk.Entry, gtk.TextView, gtk.ComboBoxEntry, gtk.ComboBox)
    TUPLABOOL = (gtk.CheckButton, gtk.ToggleButton)
    TUPLANUM = tuple(list(TUPLATEXTO) + [gtk.SpinButton])
    TUPLAFECHA = TUPLATEXTO
    TUPLACOMBO = (gtk.ComboBoxEntry, gtk.ComboBox)
    TIPOS = {sqlobject.col.SOStringCol: TUPLATEXTO, 
             sqlobject.col.SOUnicodeCol: TUPLATEXTO, 
             sqlobject.col.SOIntCol: TUPLANUM, 
             sqlobject.col.SOTinyIntCol: TUPLANUM, 
             sqlobject.col.SOSmallIntCol: TUPLANUM, 
             sqlobject.col.SOMediumIntCol: TUPLANUM, 
             sqlobject.col.SOBigIntCol: TUPLANUM, 
             sqlobject.col.SOBoolCol: TUPLABOOL, 
             sqlobject.col.SOFloatCol: TUPLANUM, 
             sqlobject.col.SOEnumCol: (gtk.ComboBox, ), 
             sqlobject.col.SODateTimeCol: TUPLATEXTO, 
             sqlobject.col.SODateCol: TUPLATEXTO,
                # En un futuro cambiar por un pack (gtk.Entry + gtk.Button 
                # para elegir fecha).
             sqlobject.col.SOTimeCol: TUPLATEXTO, 
             sqlobject.col.SOTimestampCol: TUPLATEXTO, 
             sqlobject.col.SODecimalCol: TUPLANUM, 
             sqlobject.col.SOForeignKey: TUPLACOMBO}

    def __init__(self):
        self.__adaptadores = {}

    def adaptar(self, col, widget = None):
        """
        Crea o modifica el adaptador registrado para la columna recibida.
        Si widget != None, relaciona el campo con el widget.
        """
        self.__adaptadores[col] = self.build_adapter(col, widget)

    def get_adaptadores(self):
        """
        Devuelve el diccionario de adaptadores.
        """
        return self.__adaptadores

    def build_adapter(self, col, widget = None):
        """
        Crea y devuelve un diccionario con cuatro elementos:
            - Un widget de pygtk con el que el atributo de la 
              columna se mostrará en pantalla.
            - Una función para volcar el valor de la columna 
              en el widget.
            - Una función para traducir y guardar el valor del 
              widget en el campo.
            - Una función para comparar el valor del modelo y 
              de la vista.
        """
        res = {'widget': self._inferir_widget(col, widget)}
        res['mostrar'] = self._inferir_setter(col, res['widget']) 
        res['leer'] = self._inferir_getter(col, res['widget'])
        res['comparar'] = self._inferir_comparator(col, res['leer'])
        return res

    def _inferir_comparator(self, col, func_get_value):
        """
        Devuelve una función que a su vez devolverá True o False 
        cuando sea llamada en función de si el atributo del campo 
        "col" del objeto es igual o no al contenido del widget "w".
        """
        return lambda o: getattr(o, col.name) == func_get_value()

    def _inferir_getter(self, col, w):
        """
        Devuelve una función para obtener el 
        valor del widget en el tipo adecuado
        para la columna col.
        """
        if isinstance(col, (sqlobject.col.SOStringCol, 
                            sqlobject.col.SOUnicodeCol)):
            f = lambda v: v
        elif isinstance(col, (sqlobject.col.SOIntCol, 
                              sqlobject.col.SOTinyIntCol, 
                              sqlobject.col.SOSmallIntCol, 
                              sqlobject.col.SOMediumIntCol, 
                              sqlobject.col.SOBigIntCol, 
                              sqlobject.col.SODecimalCol)):
            f = lambda v: convertir_a_entero(v)
        elif isinstance(col, sqlobject.col.SOBoolCol):
            f = lambda v: convertir_a_booleano(v)
        elif isinstance(col, sqlobject.col.SOFloatCol):
            f = lambda v: convertir_a_flotante(v, col = col)
        elif isinstance(col, sqlobject.col.SOEnumCol):
            f = lambda v: v # No sé muy bien qué hacer en este caso, tal 
                            # vez se trate del índice del elemento en el 
                            # combobox/enumerado, y por tanto un entero.
        elif isinstance(col, (sqlobject.col.SODateTimeCol, 
                              sqlobject.col.SOTimestampCol)):
            f = lambda v: convertir_a_fechahora(v)
        elif isinstance(col, sqlobject.col.SODateCol):
            f = lambda v: convertir_a_fecha(v)
        elif isinstance(col, sqlobject.col.SOTimeCol):
            f = lambda v: convertir_a_hora(v)
        elif isinstance(col, sqlobject.col.SOForeignKey):
            def get_id_or_none(v):
                if not v:
                    res = None
                try:
                    res = int(v)
                except:
                    res = None
                return res
            f = get_id_or_none
        else:
            f = lambda v: v
        return lambda : generic_getter(f, w)

    def _inferir_setter(self, col, w):
        """
        Devuelve la función que muestra el 
        valor de la columna en el widget w.
        """
        if DEBUG:
            print w, w.name
        if isinstance(w, gtk.SpinButton):
            func = lambda o: setter_spinbutton(o, col, w)
        elif isinstance(w, gtk.Entry):
            func = lambda o: setter_entry(o, col, w)
        elif isinstance(w, gtk.TextView):
            func = lambda o: setter_textview(o, col, w)
        elif isinstance(w, gtk.ComboBoxEntry):
            func = lambda o: setter_comboboxentry(o, col, w)
        elif isinstance(w, gtk.ComboBox):
            func = lambda o: setter_combobox(o, col, w)
        elif isinstance(w, (gtk.CheckButton, gtk.ToggleButton)):
            func = lambda o: setter_checkbutton(o, col, w)
        else:
            txterr = 'adapter.py::_inferir_setter: Widget "%s" no soportado' % w
            sys.stderr.write(txterr)
            raise TypeError, txterr
        return func

    def _inferir_widget(self, col, widget = None):
        """
        Si widget != None, comprueba que el tipo es correcto
        para la columna y lo asigna. Si no es correcto o es None, 
        crea y devuelve un widget apropiado, eliminando si hiciera 
        falta el widget recibido y llamando al nuevo con el mismo
        nombre.
        """
        ws_soportados = None
        for tipo in Adaptador.TIPOS:
            if isinstance(col, tipo):
                ws_soportados = self.TIPOS[tipo]
                break
        if not ws_soportados:
            raise TypeError, "adapter::_inferir_widget -> Tipo no soportado: %s" % (col)
        if widget == None:
            widget = self._crear_widget(ws_soportados[0], col)
        if DEBUG:
            print widget.name, type(widget), ws_soportados
        if type(widget) not in ws_soportados:
            widget = self._reemplazar_widget(widget, ws_soportados[0], col)
        if isinstance(widget, gtk.ComboBox):    
            # ComboBoxEntry deriva de ComboBox, entra también.
            if widget.get_model() == None:
                self._construir_model_a(widget, col)
        return widget

    def _construir_model_a(self, widget, col):
        """
        Averigua la fuente del widget según el nombre de la columna 
        recibida y asocia un model sencillo al widget, que debe ser 
        un ComboBox[Entry].
        """
        import pclases
        nomclase = col.name.replace("ID", "")
        nomclase = nomclase[0].upper() + nomclase[1:]
        clase = getattr(pclases, nomclase)
        primera_col = clase.sqlmeta.columnList[0].name
        filas = [(r.id, getattr(r, primera_col))
                 for r in clase.select(orderBy = primera_col)]
        rellenar_lista(widget, filas)

    def _crear_widget(self, tipo, col, nombre = None):
        """
        Crea y devuelve un widget del tipo recibido y con 
        el nombre de la columna recibido.
        """
        if not nombre:
            nombre = col.name
        w = tipo()
        w.set_property("name", nombre)
        if (isinstance(w, self.TUPLACOMBO) 
           and isinstance(col, sqlobject.SOForeignKey)):
            import pclases
            tablajena = getattr(pclases, col.foreignKey)
            texto = tablajena.sqlmeta.columnList[0]
            ops = []
            for i in tablajena.select(orderBy = texto.name):
                id = i.id
                txt = getattr(i, texto.name)
                ops.append((id, txt))
            rellenar_lista(w, ops)
        return w

    def _reemplazar_widget(self, w, tipo, col):
        """
        Crea un widget y "reemplaza" el recibido por 
        el nuevo, asignándole el mismo nombre y 
        devolviéndolo.
        """
        nombre = w.name
        del(w)
        w = self._crear_widget(tipo, col, nombre)
        return w

def adaptar_clase(clase_pclases, widgets = {}):
    """
    Adapta una clase completa de pclases.
    Si widgets no está vacío, deberá contener un diccionario 
    cuyas claves son el nombre de las columnas de la clase o 
    la columna en sí, y el valor de cada una es el widget al 
    que se adaptará.
    Devuelve el objeto Adaptador que guarda los adaptadores 
    de las columnas.
    """
    adaptador = Adaptador()
    columns_dict = clase_pclases.sqlmeta.columns
    for nombre_col in columns_dict:
        col = columns_dict[nombre_col]
        if col in widgets:
            adaptador.adaptar(col, widgets[col])
        elif nombre_col in widgets:
            adaptador.adaptar(col, widgets[nombre_col])
        else:
            adaptador.adaptar(col)
    return adaptador

if __name__ == "__main__":
    import pclases
    c = pclases.Cliente.select()[0]
    a = Adaptador()
    a.adaptar(pclases.Cliente.sqlmeta.columnList[0])
    a._Adaptador__adaptadores[a._Adaptador__adaptadores.keys()[0]]['widget'].set_text("Tal")
    a._Adaptador__adaptadores[a._Adaptador__adaptadores.keys()[0]]['comparar'](c)
    c.nombre = a._Adaptador__adaptadores[a._Adaptador__adaptadores.keys()[0]]['leer']()
    assert a._Adaptador__adaptadores[a._Adaptador__adaptadores.keys()[0]]['comparar'](c)

