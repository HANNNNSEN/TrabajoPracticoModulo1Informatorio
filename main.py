import os
import platform

#se importan las clases
from ventas import (
    Venta,
    VentaTarjetaCredito,
    VentaCreditoCasa,
    GestionVentas,
)


#una función para limpiar pantalla
def limpiar_pantalla():
    ''' Limpiar la pantalla según el sistema operativo'''
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear') # Para Linux/Unix/MacOs


#una función para mostrar menú
def mostrar_menu():
    print("========== Menú de Gestión de Ventas ==========")
    print('1. Agregar Venta Contado')
    print('2. Agregar Venta con tarjeta de credito')
    print('3. Agregar Venta con credito de la casa')
    print('4. Buscar venta por n_venta')
    print('5. Modificar precio de una venta')
    print('6. Eliminar una venta ')
    print('7. Mostrar Todos las ventas')
    print('8. Mostrar mejor vendedor') #el mejor vendedor es el que vendio mas dinero
    print('9. Salir')
    print('================================================')


#función para agregar venta
#en esta se pide que ingrese cada valor para la creación de las clases
def agregar_venta(gestion,opcion):
    try:
        producto = input('Ingrese el nombre del producto ')
        cantidad = input('Ingrese la cantidad: ')
        precio = float(input('Ingrese el precio: '))
        nombre = input('Ingrese el nombre del cliente: ')
        apellido = input('Ingrese apellido del cliente: ')
        vendedor = int(input('Ingrese el número id del vendedor: '))
        local = input('Ingrese el local de la venta: ')

        if opcion == '1':
            
            venta = Venta(producto,cantidad, precio,nombre, apellido, vendedor,local)

        elif opcion == '2':

            marca_tarjeta = input('Ingrese la marca de la tarjeta: ')
            n_cuotas = int(input('Ingrese cantidad de cuotas: '))
            venta = VentaTarjetaCredito(producto,cantidad, precio,nombre, apellido, vendedor,local,marca_tarjeta,n_cuotas)

        elif opcion == '3':

            n_cuotas = int(input('Ingrese cantidad de cuotas: '))
            venta = VentaCreditoCasa(producto,cantidad, precio,nombre, apellido, vendedor,local,n_cuotas)         
        else:
            print('Opción inválida')
            return

        gestion.crear_venta(venta)
        input('Presione enter para continuar...')

    except ValueError as e:
        print(f'Error: {e}')
    except Exception as e:
        print(f'Error inesperado: {e}')

#función para buscar venta
def buscar_venta(gestion):
    n_venta = input('Ingrese el número de venta a buscar: ')
    gestion.leer_venta(n_venta)   
    input('Presione enter para continuar...')

#función para modificar venta
def modificar_precio_venta(gestion):
    n_venta = input('Ingrese el número de venta a modificar el precio: ')
    precio = float(input('Ingrese el nuevo precio'))
    gestion.modificar_venta(n_venta, precio)
    input('Presione enter para continuar...')

#función para eliminar venta
def eliminar_venta(gestion):
    n_venta = input('Ingrese el número de venta a eliminar: ')
    gestion.eliminar_venta(n_venta)
    input('Presione enter para continuar...')

#función para mostrar venta
def mostrar_ventas(gestion):
    print('=============== Listado completo de Ventas ==============')
    for venta in gestion.leer_datos().values():
        if 'marca_tarjeta' in venta:
            print(f"Venta n° {venta['n_venta']} - producto: {venta['producto']}  - cantidad: {venta['cantidad']} - precio: {venta['precio']}- compra con tarjeta de credito: {venta['marca_tarjeta']} en: {venta['n_cuotas']} cuotas ")
        elif 'n_cuotas' in venta:
             print(f"Venta n° {venta['n_venta']} - producto: {venta['producto']}  - cantidad: {venta['cantidad']} - precio: {venta['precio']}- compra con credito de la casa en: {venta['n_cuotas']} cuotas ")
        else:
             print(f"Venta n° {venta['n_venta']} - producto: {venta['producto']}  - cantidad: {venta['cantidad']} - precio: {venta['precio']}- compra al contado")
          
    print('=====================================================================')
    input('Presione enter para continuar...')
    
#función para buscar mejor vendedor, se crea un diccionario con los vendedores reccoriendo el archivo 
#luego se recorre el archivo para ir multiplicando precio por cantidad y agregar al vendedor correspondiente
# y por ulitmo se busca el valor máximo 
def mejor_vendedor(gestion):
    try:        
        ventas = gestion.leer_datos()
        ventas_por_vendedor = {}
        if(ventas):
            # Calcular el total de ventas por vendedor
            for venta in ventas.values():
                vendedor = venta['vendedor']
                total_venta = venta['precio'] * venta['cantidad']
                
                if vendedor in ventas_por_vendedor:
                    ventas_por_vendedor[vendedor] += total_venta
                else:
                    ventas_por_vendedor[vendedor] = total_venta
            # Encontrar el vendedor con la máxima venta
            if ventas_por_vendedor:
                mejor_vendedor = max(ventas_por_vendedor, key=ventas_por_vendedor.get)                
                max_venta = ventas_por_vendedor[mejor_vendedor]
                print(f'El vendedor que más vendió es {mejor_vendedor} con un total de {max_venta}.')
            else:
                print('No se encontraron ventas para calcular.')
        else:
            print('No hay ventas registradas para determinar el mejor vendedor.')
    except Exception as e:
        print(f'Error inesperado: {e}')
    input('Presione enter para continuar...')


if __name__ == "__main__":
    archivo_ventas = 'ventas_db.json'
    gestion = GestionVentas(archivo_ventas)

    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input('Seleccione una opción: ')

        if opcion == '1' or opcion == '2'or opcion == '3':

            agregar_venta(gestion, opcion)
        
        elif opcion == '4':
            buscar_venta(gestion)

        elif opcion == '5':
            modificar_precio_venta(gestion)

        elif opcion == '6':
            eliminar_venta(gestion)

        elif opcion == '7':
            mostrar_ventas(gestion)

        elif opcion == '8':
            mejor_vendedor(gestion)            

        elif opcion == '9':
            print('Saliendo del programa...')
            break
        else:
            print('Opción no válida. Por favor, seleccione una opción válida (1-9)')