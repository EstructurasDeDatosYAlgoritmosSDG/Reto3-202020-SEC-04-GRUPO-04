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
from math import radians, cos, sin, asin, sqrt

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria


"""

# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------

def newAnalyzer():

    analyzer = {'accidentes': None,
                'dateIndex': None,
                'hourIndex': None
                }
    
    analyzer['accidentes'] = lt.newList('SINGLE_LINKED', compareIds)
    analyzer['dateIndex'] = om.newMap(omaptype='RBT', comparefunction= compareDates)
    analyzer['hourIndex'] = om.newMap(omaptype='RBT', comparefunction= compareHours)

    return analyzer


# Funciones para agregar informacion al catalogo

# Mapa fechas
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

# Mapa horas

def addAccidentHour(analyzer, accidente):
    """
    """
    updateHourIndex(analyzer['hourIndex'], accidente)
    return analyzer

def updateHourIndex(map, accidente):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    occurredhour = accidente['Start_Time'][11:]
    hora = int(occurredhour[:2])
    minutos = int(occurredhour[3:5])
    o = str(hora), str(minutos)
    if minutos <= 30:
        minutos = 30
    elif minutos < 60:
        if hora == 23:
            hora = int('23')
            minutos = 59
        else:
            hora += 1
            minutos = int('00')
    segundos = int('00')
    accidenthour = datetime.time(hora,minutos,segundos)
    print(accidenthour, o)
    entry = om.get(map, accidenthour)
    if entry is None:
        datentry = newDataEntryHour(accidente)
        om.put(map, accidenthour, datentry)
    else:
        datentry = me.getValue(entry)
    addHourIndex(datentry, accidente)
    return map

def addHourIndex(hourentry, accidente):
    """
    Actualiza un indice de tipo de accidentes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = hourentry['lstaccidents']
    lt.addLast(lst, accidente)
    severityIndex = hourentry['severityIndex']
    severidad = m.get(severityIndex, accidente['Severity'])
    if (severidad is None):
        entry = newSeverityEntry(accidente['Severity'], accidente)
        lt.addLast(entry['lstofseverities'], accidente)
        m.put(severityIndex, accidente['Severity'], entry)
    else:
        entry = me.getValue(severidad)
        lt.addLast(entry['lstofseverities'], accidente)
    return hourentry

def newDataEntryHour(accidente):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'severityIndex': None, 'lstaccidents': None}
    entry['severityIndex'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareSeverities)
    entry['lstaccidents'] = lt.newList('SINGLE_LINKED', compareHours)
    return entry

# Para los dos

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

# Mapa fechas

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

# Mapa horas
def indexHeightHour(analyzer):
    """Numero de autores leido
    """
    return om.height(analyzer['hourIndex'])


def indexSizeHour(analyzer):
    """Numero de autores leido
    """
    return om.size(analyzer['hourIndex'])


def minKeyHour(analyzer):
    """Numero de autores leido
    """
    return om.minKey(analyzer['hourIndex'])


def maxKeyHour(analyzer):
    """Numero de autores leido
    """
    return om.maxKey(analyzer['hourIndex'])

# siguiente

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

def getAccidentsByHourRange(analizer, initial_hour, final_hour):
    fechas = om.keys(analizer['hourIndex'], initial_hour, final_hour)
    cant_fechas = lt.size(fechas)
    categorias = m.newMap(numelements=0,maptype='CHAINING',loadfactor=0.5,comparefunction=comparar_categorias)
    cant_accidentes = 0 
    i = 1
    while i <= cant_fechas:
        llave = lt.getElement(fechas, i)
        arbol = om.get(analizer['hourIndex'], llave)
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
    return cant_accidentes, categorias

# Formula de haversine

def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def calcular_dia(dia, mes, year):
    a = (14 - mes) // 12
    m = mes + 12 * a - 2
    d = (dia + year + (year//4) - (year//100) + (year//400) + ((31 * m)//12)) % 7
    if d == 0:
        diaSemana = 'Domingo'
    elif d == 1:
        diaSemana = 'Lunes'
    elif d == 2:
        diaSemana = 'Martes'
    elif d == 3:
        diaSemana = 'Miercoles'
    elif d == 4:
        diaSemana = 'Jueves'
    elif d == 5:
        diaSemana = 'Viernes'
    else:
        diaSemana = 'Sabado'
    return diaSemana


def getAccidentsByGeographicZone(analyzer, longitud, latitud, radio):
    cant_accidentes = om.size(analyzer['dateIndex'])
    llaves = om.keys(analyzer['dateIndex'],om.minKey(analyzer['dateIndex']),om.maxKey(analyzer['dateIndex']))
    accidentes = m.newMap(numelements=17, prime=109345121, maptype='CHAINING', loadfactor=0.5, comparefunction=compararDias)
    accidentes_reportados = 0
    i = 1
    while i <= cant_accidentes:
        fecha = om.get(analyzer['dateIndex'], lt.getElement(llaves, i))
        lista_accidentes = fecha['value']['lstaccidents']
        j = 1
        while j <= lt.size(lista_accidentes):
            accidente = lt.getElement(lista_accidentes, j)
            long = float(accidente['Start_Lng'])
            lat = float(accidente['Start_Lat'])
            distancia = haversine(longitud, latitud, long, lat)
            if distancia <= radio:
                fecha = accidente['Start_Time']
                anio = fecha[:4]
                mes = fecha[5:7]
                dia = fecha[8:10]
                dia_semana = calcular_dia(int(dia),int(mes),int(anio))
                esta_dia = m.contains(accidentes, dia_semana)
                if not esta_dia:
                    lista = lt.newList(datastructure='SINGLE_LINKED', cmpfunction=None)
                    m.put(accidentes,dia_semana,lista)
                lis = m.get(accidentes, dia_semana)
                lis = lis['value']
                lt.addLast(lis,accidente)
                m.put(accidentes, dia_semana,lis)
                accidentes_reportados += 1
            j += 1
        i += 1
    return accidentes_reportados, accidentes

def getAccidentsByRangeDate(analyzer, initialDate,finalDate):

    """
    Retornal el número de accidentes ocurridos en un rango de fechas
    """

    lst = om.values(analyzer['dateIndex'], initialDate,finalDate)
    
    return lst

def getAccidentsBySeverity(analyzer, initialDate, finalDate, severity):

    accidentDate = om.get(analyzer['dateIndex'], initialDate, finalDate)
    if accidentDate['key'] is not None:
        severityMap = me.getValue(accidentDate)['severityIndex']
        numSeverity = m.get(severityMap, severity)
        if(numSeverity is not None):
            return m.size(me.getValue(numSeverity)['lstofseverities'])
        return 0

def getMostSeverity(analyzer, initialDate, finalDate):

    s1= getAccidentsBySeverity(analyzer,initialDate,finalDate,1)
    s2 = getAccidentsBySeverity(analyzer,initialDate,finalDate,2)
    s3 = getAccidentsBySeverity(analyzer,initialDate,finalDate,3)
    s4 = getAccidentsBySeverity(analyzer,initialDate,finalDate,4)

    mayor = s1
    
    if(mayor < s2):
        mayor = s2
    elif(mayor < s3):
        mayor = s3
    elif(mayor < s4):
        mayor = s4
    else:
        return 1

    if(mayor == s2):
        return 2
    elif(mayor == s3):
        return 3
    elif(mayor == s4):
        return 4



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

def compararDias(date1, date2):
    date = me.getKey(date2)
    if (date1 == date):
        return 0
    elif (date1 > date):
        return 1
    else:
        return -1

def compareHours(date1, date2):
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
