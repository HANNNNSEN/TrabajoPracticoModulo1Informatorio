"""Desafío 2: Sistema de Gestión de Ventas

Objetivo: Desarrollar un sistema para registrar y gestionar ventas de productos.

Requisitos:

Crear una clase base Venta con atributos como fecha, cliente, productos vendidos, etc.

Definir al menos 2 clases derivadas para diferentes tipos de ventas (por ejemplo, VentaOnline, VentaLocal) con atributos y métodos específicos.

Implementar operaciones CRUD para gestionar las ventas.

Manejar errores con bloques try-except para validar entradas y gestionar excepciones.

Persistir los datos en archivo JSON.

##############################"""

import json

#se crea la clase principal Venta con su constructor y los metodos de lectura y escritura
class Venta:
    def __init__(self, producto, cantidad, precio, nombre_cliente,apellido_cliente, vendedor, local):        
        self.__producto = producto
        self.__cantidad = cantidad
        self.__precio = precio
        self.__nombre_cliente = nombre_cliente
        self.__apellido_cliente = apellido_cliente
        self.__local = local
        self.__vendedor = vendedor       
        self.__n_venta = int(0)
   
    @property
    def n_venta(self):
        return self.__n_venta
    
    @property
    def producto(self):
        return self.__producto
    @property
    def cantidad(self):
        return self.__cantidad
    @property
    def precio(self):
        return self.__precio
    
    @property
    def apellido_cliente(self):
        return self.__apellido_cliente.capitalize()
    
    @property
    def nombre_cliente(self):
        return self.__nombre_cliente.capitalize()
    
    @property
    def vendedor(self):
        return self.__vendedor
    
    @property
    def local(self):
        return self.__local
    
    @precio.setter
    def precio(self, nuevo_precio):
        self.__precio = self.validar_positivo(nuevo_precio) 

    @cantidad.setter
    def cantidad(self, nueva_cantidad):
        self.__cantidad = self.validar_positivo(nueva_cantidad)

    @n_venta.setter
    def n_venta(self, n_venta):
        self.__n_venta = n_venta

    def validar_positivo(self, valor):
        try:
            valor = float(valor)
            if valor <= 0:
                raise ValueError(f"debe ser numérico positivo. ({valor}: valor incorrecto)")
            return valor
        except ValueError:
            raise ValueError("debe ser un número válido.")

    def to_dict(self):
        return {
            "n_venta": int(self.n_venta),
            "producto": self.producto,
            "cantidad": self.cantidad,
            "precio": self.precio,
            "apellido_cliente": self.apellido_cliente,
            "nombre_cliente": self.apellido_cliente,
            "vendedor": self.apellido_cliente,
            "local": self.apellido_cliente

        }

    def __str__(self):
        return f"Número de venta: {self.n_venta} producto: {self.producto} vendedor: {self.vendedor}"
    
#se crea la clase VentaTarjetaCredito que hereda de la principal "Venta" 
# con su constructor y los metodos de lectura y escritura
#en esta clase se agrega la marca de la tarjeta de crédito y en cuantas cuotas se vendio el producto
class VentaTarjetaCredito(Venta):

    def __init__(self, producto, cantidad, precio, nombre_cliente,apellido_cliente, vendedor, local,marca_tarjeta,n_cuotas):
            super().__init__(producto, cantidad, precio, nombre_cliente,apellido_cliente, vendedor, local)            
            self.__marca_tarjeta = marca_tarjeta
            self.__n_cuotas = n_cuotas

    @property
    def marca_tarjeta(self):
        return self.__marca_tarjeta
        
    @property
    def n_cuotas(self):
        return self.__n_cuotas

    def to_dict(self):
        data = super().to_dict()
        data["marca_tarjeta"] = self.marca_tarjeta
        data["n_cuotas"] = self.n_cuotas
        return data

    def __str__(self):
        return f"{super().__str__()} - En cuotas con tarjeta de crédito: {self.n_cuotas} "  
    

#se crea la clase VentaCreditoCasa que hereda de la principal "Venta" 
# con su constructor y los metodos de lectura y escritura
#en esta clase se agrega en cuantas cuotas se vendio el producto con el credito de la casa                       
class VentaCreditoCasa(Venta):

    def __init__(self, producto, cantidad, precio, nombre_cliente,apellido_cliente, vendedor, local,n_cuotas):
            super().__init__(producto, cantidad, precio, nombre_cliente,apellido_cliente, vendedor, local)            
            self.__n_cuotas = n_cuotas           
        
    @property
    def n_cuotas(self):
        return self.__n_cuotas

    def to_dict(self):
        data = super().to_dict()
        data["n_cuotas"] = self.n_cuotas
        return data

    def __str__(self):
        return f"{super().__str__()} - En cuotas con crédito de la casa: {self.n_cuotas} "

#se crea la clase GestionVentas la cual estará encargada de hacer las operaciones de lectura,escritura,busqueda,modificaciones del archivo    
class GestionVentas:
    def __init__(self, archivo):
        self.archivo = archivo
    #leer los datos y algunas excepciones
    def leer_datos(self):
        try:
            with open(self.archivo, 'r') as file:
                datos = json.load(file)
        except FileNotFoundError:
            return {}
        except PermissionError:
            print(f"Error: No tienes permiso para acceder al archivo '{file}'.")
        except Exception as error:
            raise Exception(f'Error: al leer datos del archivo: {error}')
        else:
            return datos
    #guardar los datos y algunas excepciones
    def guardar_datos(self, datos):
        try:
            with open(self.archivo, 'w') as file:
                json.dump(datos, file, indent=4)
        except PermissionError:
            print(f"Error: No tienes permiso para acceder al archivo '{file}'.")
        except IOError as error:
            print(f'Error al intentar guardar los datos en {self.archivo}: {error}')
        except Exception as error:
            print(f'Error inesperado: {error}')
    #crear ventas:
    #para crear la venta, se recorre el archivo si es que existe
    # luego se saca el ultimo valor de n_ventas, este se usa como variable acumulativa  
    # n_ventas tambien será la key de acceso al diccionario.
    def crear_venta(self, venta):
        try:
            datos = self.leer_datos()
            if datos:
                n_ventas_max = max(int(venta_data['n_venta']) for venta_data in datos.values())
            else: 
                n_ventas_max=0                
            
            nuevo_n_venta = int(n_ventas_max + 1)
            venta.n_venta=int(nuevo_n_venta)

            datos[nuevo_n_venta] = venta.to_dict()
            self.guardar_datos(datos)
            print(f"Venta N°: { nuevo_n_venta} creada correctamente.")

        except Exception as error:
            print(f'Error inesperado al crear venta N°: { nuevo_n_venta} error: {error}')
    #leer ventas
    #se realiza un if para imprimir según la clase que se esta mostrando
    def leer_venta(self, n_venta):
        try:
            datos = self.leer_datos()
            if str(n_venta) in datos:
                
                venta_data = datos[str(n_venta)]
                
                
                if 'marca_tarjeta' in venta_data:
                    print(f"Venta n° {venta_data['n_venta']} - producto: {venta_data['producto']}  - cantidad: {venta_data['cantidad']} - precio: {venta_data['precio']}- compra con tarjeta de credito: {venta_data['marca_tarjeta']} en: {venta_data['n_cuotas']} cuotas ")
                    
                elif 'n_cuotas' in venta_data:
                    print(f"Venta n° {venta_data['n_venta']} - producto: {venta_data['producto']}  - cantidad: {venta_data['cantidad']} - precio: {venta_data['precio']}- compra con credito de la casa en: {venta_data['n_cuotas']} cuotas ")
                    
                else:
                    print(f"Venta n° {venta_data['n_venta']} - producto: {venta_data['producto']}  - cantidad: {venta_data['cantidad']} - precio: {venta_data['precio']}- compra al contado")
                                   
                               
            else:
                print(f'No se encontró venta {n_venta}')

        except Exception as e:
            print(f'Error al leer la venta: {e}')
    #modificar ventas
    #se lee el archivo luego se busca según el número de venta y se modifica
    def modificar_venta(self, n_venta, nuevo_precio):
        try:
            datos = self.leer_datos()
            if str(n_venta) in datos.keys():
                 datos[n_venta]['precio'] = nuevo_precio
                 self.guardar_datos(datos)
                 print(f'se modificó precio de venta:{nuevo_precio}')
            else:
                print(f'No se modificó precio de venta: {nuevo_precio}')
        except Exception as e:
            print(f'Error al actualizar la venta: {e}')
    #eliminar alguna venta
    #se lee el archivo luego se busca según el número de venta y se elimina
    def eliminar_venta(self, n_venta):
        try:
            datos = self.leer_datos()
            if str(n_venta) in datos.keys():
                 del datos[n_venta]
                 self.guardar_datos(datos)
                 print(f'La venta N°:{n_venta} se eliminó correctamente')
            else:
                print(f'No se encontró la venta N°:{n_venta}')
        except Exception as e:
            print(f'Error al eliminar la venta: {e}')
