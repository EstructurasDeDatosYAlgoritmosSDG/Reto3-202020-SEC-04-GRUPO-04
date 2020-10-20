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

import sys
import config
from DISClib.ADT import list as lt
from App import controller
assert config
from DISClib.ADT import map as m

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________

accidentsfilesmall = 'us_accidents_small.csv'
accidentsfile2016 = 'us_accidents_dis_2016.csv'
accidentsfile2017 = 'us_accidents_dis_2017.csv'
accidentsfile2018 = 'us_accidents_dis_2018.csv'
accidentsfile2019 = 'us_accidents_dis_2019.csv'
accidentsfileDec19 = 'us_accidents_Dec19.csv'


# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de accidentes")
    print("3- Conocer los accidentes en una fecha")
    print("4- Conocer los accidentes anteriores a una fecha ")
    print("5- Conocer los accidentes en un rango de fechas ")
    print("6- Conocer el estado con más accidentes ")
    print("7- Conocer los accidentes por rango de horas ")
    print("8- Conocer la zona geográfica más accidentada ")
    print("9- Usar el conjunto completo de datos ")
    print("0- Salir")
    print("*******************************************")


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()
        

    elif int(inputs[0]) == 2:
        print("\nCargando información de accidentes ....")
        controller.loadData(cont, accidentsfilesmall)
        print('Accidentes cargados: ' + str(controller.accidentsSize(cont)))
        print('Altura del arbol: ' + str(controller.indexHeight(cont)))
        print('Elementos en el arbol: ' + str(controller.indexSize(cont)))
        print('Menor Llave: ' + str(controller.minKey(cont)))
        print('Mayor Llave: ' + str(controller.maxKey(cont)))
        print('Menor Llave dos: ' + str(controller.minKeyHour(cont)))
        print('Mayor Llave dos: ' + str(controller.maxKeyHour(cont)))


    elif int(inputs[0]) == 3:
        print("\nBuscando accidentes en una fecha en específico: ")
        date = input("Fecha (YYYY-MM-DD): ")
        lista = controller.getAccidentsByDate(cont, date)
        print("\nTotal de accidentes en la fecha: " + str(lt.size(lista)))


    elif int(inputs[0]) == 4:
        print("\nBuscando accidentes anteriores a una fecha en específico: ")
        date = input("Ingrese la fecha (YYYY-MM-DD): ")
        valores = controller.getAccidentsBeforeDate(cont, date)
        print('\nEl total de accidentes ocurridos antes de la fecha indicada es de:', valores[0])
        print('\nLa fecha en la que más accidentes se reportaron fue:', valores[1] )
        

    elif int(inputs[0]) == 5:
        fecha_inicio = input("\nIngrese la fecha de inicio (YYYY-MM-DD): ")
        fecha_final = input("\nIngrese la fecha final (YYYY-MM-DD): ")
        if len(fecha_inicio) == 10 and len(fecha_final) == 10:
            valores = controller.getAccidentesByRange(cont, fecha_inicio,fecha_final)
            if valores[0] != 0 and valores[1] != 0:
                print("\nEl número total de accidentes en el rango de fechas es de:",valores[0])
                print("La categoría de accidentes más reportadas en el rango de fechas es:", valores[1])
            else:
                print('El rango de fechas no se ha ingresado correctamente')
        else:
            print("\nFormato de fecha incorrecto")
    elif int(inputs[0]) == 6:
        print("\nRequerimiento No 1 del reto 3: ")

    elif int(inputs[0]) == 7:
        hora_inicio = input("\nIngrese la hora de inicio (HH:MM): ")
        hora_inicio = hora_inicio + ':00'
        hora_final = input("\nIngrese la hora final (HH:MM): ")
        hora_final = hora_final + ':00'
        if len(hora_inicio) == 8 and len(hora_final) == 8:
            valores = controller.getAccidentsByHourRange(cont, hora_inicio,hora_final)
            if valores[0] != 0 and valores[1] != 0:
                print("\nEl número total de accidentes en el rango de fechas es de:",valores[0])
                llaves_severidad = m.keySet(valores[1])
                i = 1
                while i <= lt.size(llaves_severidad):
                    llave = m.get(valores[1],lt.getElement(llaves_severidad,i))
                    print('Los accidentes reportados por la severidad',lt.getElement(llaves_severidad,i),'son:',llave['value'])
                    i += 1
            else:
                print('El rango de fechas no se ha ingresado correctamente')
        else:
            print("\nFormato de fecha incorrecto")

    elif int(inputs[0]) == 8:
        longitud = float(input('\nIngrese la longitud en formato decimal: '))
        latitud = float(input('\nIngrese la latitud en formato decimal: '))
        radio = float(input('\nIngrese el radio en kilometros: '))
        print('')
        resultado = controller.getAccidentsByGeographicZone(cont, longitud, latitud, radio)
        llaves = m.keySet(resultado[1])
        i = 1
        while i <= lt.size(llaves):
            llave = lt.getElement(llaves, i)
            valor = m.get(resultado[1], llave)
            valor = valor['value']
            accidentes_dia = lt.size(valor)
            print('El día', llave, 'se reportó un total de',accidentes_dia,'accidentes')
            i += 1
        print('\nEl total de accidentes reportados en ese radio es de:',resultado[0])


    elif int(inputs[0]) == 9:
        print("\nRequerimiento No 1 del reto 3: ")
    else:
        sys.exit(0)
sys.exit(0)
