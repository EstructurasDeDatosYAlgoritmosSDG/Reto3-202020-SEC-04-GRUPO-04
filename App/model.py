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
import config
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
import datetime
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria


"""

# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------

def newAnalyzer():

    analyzer = {'accidentes': None,
                'dateIndex': None
                }
    
    analyzer['accidentes'] = lt.newList('SINGLE_LINKED', compareIds)
    analyzer['dateIndex'] = om.newMap(omaptype='BST', comparefunction= compareDates)

    return analyzer


# Funciones para agregar informacion al catalogo

def addAccident(analyzer, accidente):
    """
    """
    lt.addLast(analyzer['accidentes'], accidente)
    updateDateIndex(analyzer['dateIndex'], accidente)
    return analyzer

def updateDateIndex(map, accidente):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    occurreddate = accidente['Start_Time']
    accidentdate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, accidentdate.date())
    if entry is None:
        datentry = newDataEntry(accidente)
        om.put(map, accidentdate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, accidente)
    return map

def addDateIndex(datentry, accidente):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstaccidents']
    lt.addLast(lst, accidente)
    severityIndex = datentry['severityIndex']
    severidad = m.get(severityIndex, accidente['Severity'])
    if (severidad is None):
        entry = newSeverityEntry(accidente['Severity'], accidente)
        lt.addLast(entry['lstofseverities'], accidente)
        m.put(severityIndex, accidente['Severity'], entry)
    else:
        entry = me.getValue(severidad)
        lt.addLast(entry['lstofseverities'], accidente)
    return datentry

def newDataEntry(accidente):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'severityIndex': None, 'lstaccidents': None}
    entry['severityIndex'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareSeverities)
    entry['lstaccidents'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry


def newSeverityEntry(Severity, accidente):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'severidad': None, 'lstofseverities': None}
    ofentry['severidad'] = Severity
    ofentry['lstofseverities'] = lt.newList('SINGLELINKED', compareSeverities)
    return ofentry


# ==============================
# Funciones de consulta
# ==============================
def accidentsSize(analyzer):
    """
    Número de libros en el catago
    """
    return lt.size(analyzer['accidentes'])


def indexHeight(analyzer):
    """Numero de autores leido
    """
    return om.height(analyzer['dateIndex'])


def indexSize(analyzer):
    """Numero de autores leido
    """
    return om.size(analyzer['dateIndex'])


def minKey(analyzer):
    """Numero de autores leido
    """
    return om.minKey(analyzer['dateIndex'])


def maxKey(analyzer):
    """Numero de autores leido
    """
    return om.maxKey(analyzer['dateIndex'])

def getAccidentsByDate(analyzer, date):
    """
    Retorna el numero de accidentes en una fecha.
    """
    lst = om.get(analyzer['dateIndex'], date)
    data = lst['value']['lstaccidents']
    return data


# ==============================
# Funciones de Comparacion
# ==============================

def compareIds(id1, id2):

    if(id1 == id2):
        return 0
    elif(id1 > id2):
        return 1 
    else:
        return -1

def compareDates(date1, date2):

    if (date1 == date2):
        return 0 
    elif (date1 > date2):
        return 1
    else: 
        return -1

def compareSeverities(severidad1, severidad2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    severidad = me.getKey(severidad2)
    if (severidad1 == severidad):
        return 0
    elif (severidad1 > severidad):
        return 1
    else:
        return -1
