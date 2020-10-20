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
    analyzer['dateIndex'] = om.newMap(omaptype='RBT', comparefunction= compareDates)

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
    Actualiza un indice de tipo de accidentes.  Este indice tiene una lista
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

def getAccidentsByRange(analizer, initial_date, final_date):
    fechas = om.keys(analizer['dateIndex'], initial_date, final_date)
    cant_fechas = lt.size(fechas)
    categorias = m.newMap(numelements=0,maptype='CHAINING',loadfactor=0.5,comparefunction=comparar_categorias)
    cant_accidentes = 0 
    i = 1
    while i <= cant_fechas:
        llave = lt.getElement(fechas, i)
        arbol = om.get(analizer['dateIndex'], llave)
        severityIndex = arbol['value']['severityIndex']
        llaves_severityIndex = m.keySet(severityIndex)
        j = 1
        while j <= lt.size(llaves_severityIndex):
            categoria = lt.getElement(llaves_severityIndex, j)
            cat = m.get(severityIndex,categoria)
            accidentes = lt.size(cat['value']['lstofseverities'])
            cant_accidentes += accidentes
            esta_categoria = m.contains(categorias, categoria)
            if not esta_categoria:
                m.put(categorias,categoria,0)
            cant = m.get(categorias,categoria)
            cant = cant['value']
            cant += accidentes
            m.put(categorias,categoria,cant)
            j += 1
        i += 1
    i = 1
    mayor = 0
    cat = -10
    llaves_categorias = m.keySet(categorias)
    while i <= lt.size(llaves_categorias):
        categoria2 = lt.getElement(llaves_categorias, i)
        valor = m.get(categorias, categoria2)
        valor = valor['value']
        if valor > mayor:
            mayor = valor
            cat = categoria2
        i += 1
    return cant_accidentes, cat

def getAccidentsBeforeDate(analyzer, date):
    existe_fecha = om.contains(analyzer['dateIndex'], date)
    if existe_fecha == False:
        return('Esta fecha no existe dentro de la documentación.')
    else:
        first_date = om.minKey(analyzer['dateIndex'])
        fechas = om.keys(analyzer['dateIndex'], first_date, date)
        lt.removeLast(fechas)
        cant_fechas = lt.size(fechas)
        cant_accidentes = 0
        i = 1
        mayor = 0
        fecha_final = -10
        while i <= cant_fechas:
            llave = lt.getElement(fechas, i)
            arbol = om.get(analyzer['dateIndex'], llave)
            valor = lt.size(arbol['value']['lstaccidents'])        
            cant_accidentes += valor
            if valor > mayor:
                mayor = valor
                fecha_final = llave
            i += 1
    return cant_accidentes, fecha_final
    

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

def comparar_categorias(keyname, author):
    """
    Compara dos productoras. El primero es una cadena
    y el segundo un entry de un map
    """
    authentry = me.getKey(author)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1
