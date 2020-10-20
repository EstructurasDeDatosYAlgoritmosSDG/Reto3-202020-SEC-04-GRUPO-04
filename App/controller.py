"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
from App import model
import datetime
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion del modelo.
    """
    analyzer = model.newAnalyzer()

    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadData(analyzer, accidentsfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    accidentsfile = cf.data_dir + accidentsfile
    input_file = csv.DictReader(open(accidentsfile, encoding="utf-8"),
                                delimiter=",")
    for accidente in input_file:
        model.addAccident(analyzer, accidente)
        model.addAccidentHour(analyzer, accidente)
    return analyzer

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

# Mapa fechas

def accidentsSize(analyzer):
    """
    Numero de crimenes leidos
    """
    return model.accidentsSize(analyzer)

def indexHeight(analyzer):
    """
    Altura del indice (arbol)
    """
    return model.indexHeight(analyzer)

def indexSize(analyzer):
    """
    Numero de nodos en el arbol
    """
    return model.indexSize(analyzer)

def minKey(analyzer):
    """
    La menor llave del arbol
    """
    return model.minKey(analyzer)


def maxKey(analyzer):
    """
    La mayor llave del arbol
    """
    return model.maxKey(analyzer)

# Mapa horas
def indexHeightHour(analyzer):
    """
    Altura del indice (arbol)
    """
    return model.indexHeightHour(analyzer)

def indexSizeHour(analyzer):
    """
    Numero de nodos en el arbol
    """
    return model.indexSizeHour(analyzer)

def minKeyHour(analyzer):
    """
    La menor llave del arbol
    """
    return model.minKeyHour(analyzer)


def maxKeyHour(analyzer):
    """
    La mayor llave del arbol
    """
    return model.maxKeyHour(analyzer)

# Siguiente

def getAccidentsByDate(analyzer, date):
    """
    Retorna el total de accidentes en una fecha
    """
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    return model.getAccidentsByDate(analyzer, date.date())

def getAccidentesByRange(analizer, initial_date, final_date):
    initial_date = datetime.datetime.strptime(initial_date, '%Y-%m-%d')
    final_date = datetime.datetime.strptime(final_date, '%Y-%m-%d')
    return model.getAccidentsByRange(analizer, initial_date.date(), final_date.date())

def getAccidentsByGeographicZone(analyzer, longitud, latitud, radio):
    return model.getAccidentsByGeographicZone(analyzer, longitud, latitud, radio)

def getAccidentsByHourRange(analizer, initial_hour, final_hour):
    hora1 = int(initial_hour[:2])
    minutos1 = int(initial_hour[3:5])
    segundos1 = int(initial_hour[6:8])
    initial_hour1 = datetime.time(hora1,minutos1,segundos1)

    hora2 = int(final_hour[:2])
    minutos2 = int(final_hour[3:5])
    segundos2 = int(final_hour[6:8])
    final_hour2 = datetime.time(hora2,minutos2,segundos2)
    return model.getAccidentsByHourRange(analizer, initial_hour1, final_hour2)
