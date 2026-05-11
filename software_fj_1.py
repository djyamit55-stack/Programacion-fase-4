import tkinter as tk # Importa la biblioteca base para la interfaz gráfica
from tkinter import messagebox, ttk # Importa diálogos de alerta y widgets modernos
from abc import ABC, abstractmethod # Importa herramientas para clases abstractas
import logging # Importa el sistema de registro de eventos y errores


# --- CONFIGURACIÓN DE LOGS ---
LOG_FILE = "software_fj_debug.log" # Define el nombre del archivo donde se guardarán los errores
logging.basicConfig(filename=LOG_FILE, level=logging.ERROR, 
                    format="%(asctime)s - %(levelname)s - %(message)s") # Configura el formato del log

# --- EXCEPCIONES PERSONALIZADAS ---
class GestionError(Exception): """Excepción base para errores generales del sistema.""" 
class DatosInvalidosErrorNo(GestionError): """Excepción para datos de entrada erróneos o faltantes Nombre.""" 
class DatosInvalidosErrorCe(GestionError): """Excepción para datos de entrada erróneos o faltantes Cedula.""" 
class DatosInvalidosErrorCo(GestionError): """Excepción para datos de entrada erróneos o faltantes Correo.""" 
class DatosInvalidosErrorCa(GestionError): """Excepción para datos de entrada erróneos o faltantes Cantidad.""" 
class DatosReservaNoSeleccionada(GestionError): """Excepción específica cuando no se elige una reserva.""" 
class ServicioNoSeleccionadoError(GestionError): """1. Excepción específica cuando no se elige un servicio válido.""" 
class ServicioNoDisponible(GestionError): """1. Excepción cuando el servicio no esta disponible.""" 

# --- CLASES BASE Y MODELOS ---

class EntidadSistema(ABC):
    """Clase abstracta raíz para todas las entidades del software."""
    @abstractmethod
    def obtener_detalles(self): # Método obligatorio para describir la entidad
        pass

class Cliente(EntidadSistema):
    """Clase que representa al cliente con encapsulamiento estricto."""
    def __init__(self, id_cliente, nombre, correo):
        self.__id = id_cliente # Identificador privado
        self.__nombre = nombre
        self.__correo = correo # Correo electrónico privado

    def obtener_detalles(self): # Implementación del detalle del cliente
        return f"Cliente: {self.__nombre} (ID: {self.__id})"

class Servicio(EntidadSistema, ABC):
    """Clase abstracta para servicios con campos técnicos base."""
    def __init__(self, codigo, duracion):
        self.codigo = str(codigo) # Código único del servicio
        self.estado = True # Estado de disponibilidad (Booleano)
        self.duracion = int(duracion) # Duración en horas o días (Entero)

    @abstractmethod
    def calcular_costo(self, descuento=0, impuesto=0.19): # Método para polimorfismo
        pass

# --- CLASES DERIVADAS (PRODUCTOS ESPECÍFICOS) ---

class ReservaSala(Servicio):
    """Servicio específico para reserva de espacios físicos."""
    def calcular_costo(self, descuento=0, impuesto=0.19): # Sobrecarga de parámetros
        base = self.duracion * 45000 # Cálculo basado en precio por hora
        return (base - descuento) * (1 + impuesto) # Aplica lógica comercial

    def obtener_detalles(self): # Detalle técnico de la sala
        return f"Sala [{self.codigo}] por {self.duracion}h"

class AlquilerEquipo(Servicio):
    """Servicio específico para préstamo de hardware."""
    def calcular_costo(self, descuento=0, impuesto=0.19):
        base = self.duracion * 25000 # Cálculo basado en días de uso
        return (base - descuento) * (1 + impuesto)

    def obtener_detalles(self):
        return f"Equipo [{self.codigo}] por {self.duracion} días"

class AsesoriaEspecializada(Servicio):
    """Servicio de consultoría profesional."""
    def calcular_costo(self, descuento=0, impuesto=0.19):
        base = self.duracion * 80000 # Costo elevado por especialidad
        return (base - descuento) * (1 + impuesto)

    def obtener_detalles(self):
        return f"Asesoría [{self.codigo}] por {self.duracion}h"

class Reserva:
    """Clase mediadora que vincula un Cliente con un Servicio."""
    def __init__(self, cliente, servicio):
        self.cliente = cliente # Objeto de tipo Cliente
        self.servicio = servicio # Objeto de tipo Servicio
        self.confirmada = False # Estado inicial de la reserva

    def procesar(self): # Ejecuta la lógica de confirmación
        try:
            if not self.servicio.estado: # Verifica disponibilidad
                raise GestionError("Servicio no disponible.")
            self.confirmada = True # Cambia estado a éxito
            return f"Reserva procesada para: {self.cliente.obtener_detalles()}"
        except Exception as e:
            logging.error(f"Fallo en procesamiento de reserva: {e}") # Registra el error
            raise # Lanza el error para ser capturado en la UI

# --- INTERFAZ GRÁFICA ---

class VentanaSoftwareFJ:
    
    numeros_de_salas = 4
    numero_de_equipos = 6
    numero_de_asesores = 3
    s = "salas disponibles: " + str(numeros_de_salas) + "  equipos disponibles: " + str(numero_de_equipos) + "  asesores disponibles: " + str(numero_de_asesores)
    
    
    def __init__(self, master):
        self.master = master # Referencia a la ventana principal
        self.master.title("Software FJ - Gestión de Reservas") # Título de la ventana
        self.master.geometry("750x400") # Dimensiones de la ventana
        
        frame_entrada = tk.Frame(self.master) # Crea un marco para organizar elementos
        frame_entrada.pack(pady=20, fill="x", padx=15) # Empaqueta el marco arriba
        
        # Contenedor superior
        frame_superior = tk.Frame(frame_entrada, bg="grey") 
        frame_superior.pack(side="top", fill="x", expand=True)
        
        tk.Label(frame_superior, text="Nombre Cliente:").grid(row=0, column=0, padx=5) # Etiqueta cliente
        self.nom_cliente = tk.Entry(frame_superior) # Campo de texto para nombre
        self.nom_cliente.grid(row=0, column=1, padx=5)
        
        tk.Label(frame_superior, text="Cedula:").grid(row=0, column=2, padx=5) # Etiqueta cliente
        self.ced_cliente = tk.Entry(frame_superior) # Campo de texto para nombre
        self.ced_cliente.grid(row=0, column=3, padx=5)
        
        tk.Label(frame_superior, text="Correo Cliente:").grid(row=0, column=4, padx=5) # Etiqueta cliente
        self.cor_cliente = tk.Entry(frame_superior) # Campo de texto para nombre
        self.cor_cliente.grid(row=0, column=5, padx=5)
       
        # --- CONTENEDOR HORIZONTAL PARA ENTRADA ---
        frame_inferior = tk.Frame(frame_entrada, bg="grey") 
        frame_inferior.pack(side="top", fill="x", expand=True)

        tk.Label(frame_inferior, text="Servicio:").grid(row=0, column=2, padx=5) # Etiqueta servicio
        self.combo_tipo = ttk.Combobox(frame_inferior, values=["Salas", "Equipos", "Asesores"], width=20) # Combo de opciones
        self.combo_tipo.config(state="readonly")
        self.combo_tipo.grid(row=0, column=3, padx=5)

        tk.Label(frame_inferior, text="Cantidad horas/dias:").grid(row=0, column=4, padx=5) # Etiqueta cantidad
        self.ent_cant = tk.Entry(frame_inferior, width=8) # Campo de texto para cantidad
        self.ent_cant.grid(row=0, column=5, padx=5)

        self.btn_reg = tk.Button(frame_inferior, text="Registrar", command=self.ejecutar_registro, bg="#3498db", fg="white") # Botón registro
        self.btn_reg.grid(row=0, column=6, padx=10)

        # ÁREA DE RESULTADOS
        self.label = tk.Label(self.master, text=str(self.s))
        self.label.pack(anchor="w", padx=15) # Título del historial

        tk.Label(self.master, text="Lista de Servicios Reservados:").pack(anchor="w", padx=15) # Título del historial
        self.txt_display = tk.Listbox(self.master, height=12) # Caja de texto multilínea
        self.txt_display.pack(fill="both", padx=15, pady=5, expand=True)
        
        self.btn_eli = tk.Button(self.master, text="Eliminar Reserva", command=self.eliminar_registro, bg="#3498db", fg="white") # Botón registro
        self.btn_eli.pack(pady=20)

    def eliminar_registro(self):
        try:
            
            # Obtener el índice del elemento seleccionado
            seleccion = self.txt_display.curselection()
        
            # Si hay algo seleccionado
            if seleccion:
                simboloi = "¡"
                simbolof = "!"
                texto = self.txt_display.get(seleccion)
                inicio = texto.find(simboloi) + 1
                fin = texto.find(simbolof)
                resultado = texto[inicio:fin]
                if resultado == "S-1":
                    self.numeros_de_salas = self.numeros_de_salas + 1
                elif resultado == "E-1":
                    self.numero_de_equipos = self.numero_de_equipos + 1
                elif resultado == "A-1":
                    self.numero_de_asesores = self.numero_de_asesores + 1
                self.txt_display.delete(seleccion[0])
            else: raise DatosReservaNoSeleccionada("seleccione un registro.")
            self.s = "salas disponibles: " + str(self.numeros_de_salas) + "  equipos disponibles: " + str(self.numero_de_equipos) + "  asesores disponibles: " + str(self.numero_de_asesores)
            self.label.config(text=str(self.s))
        except DatosReservaNoSeleccionada as so: # Captura falta de selección
            messagebox.showwarning("seleccione un registro", str(so))
            logging.warning(f"Reserva no seleccionada {so}")     
            
    def ejecutar_registro(self):
        """Método principal con manejo robusto de excepciones."""
        try:
            # Captura de datos de la interfaz
            nombre = self.nom_cliente.get()
            cedula = self.ced_cliente.get()
            correo = self.cor_cliente.get()
            tipo = self.combo_tipo.get()
            valor_cant = self.ent_cant.get()

            # 1. VALIDACIÓN DE SELECCIÓN DE SERVICIO
            if len(nombre) < 4: # Si la cantidad está vacía
                raise DatosInvalidosErrorNo("el nombre debe tener mas de 4 caracteres")
            
            if not cedula.isdigit(): # Si la cantidad está vacía
                raise DatosInvalidosErrorCe("Debe ingresar un numero de cedula válida.")
            
            if not "@" in correo:
                raise DatosInvalidosErrorCo("Debe ingresar un correo válido.")
             
            if not tipo: # Si el combo está vacío
                raise ServicioNoSeleccionadoError("Debe seleccionar un tipo de servicio de la lista.")

            if not valor_cant: # Si la cantidad está vacía
                raise DatosInvalidosErrorCa("Debe ingresar una numero entero")

            cantidad = int(valor_cant) # Intento de conversión a entero
            print("cantidad")
            # Creación de objetos de negocio
            cliente_obj = Cliente(cedula, nombre, correo)
            print("cliente creado")
            # Lógica polimórfica según el tipo de servicio
            if tipo == "Salas":
                serv_obj = ReservaSala("¡S-1!", cantidad)
                self.var = 0
            elif tipo == "Equipos":
                serv_obj = AlquilerEquipo("¡E-1!", cantidad)
                self.var = 1
            elif tipo == "Asesores":
                serv_obj = AsesoriaEspecializada("¡A-1!", cantidad)
                self.var = 2

            print(str(self.var))
            # Procesamiento de la reserva
            if self.var == 0:
                if self.numeros_de_salas == 0:
                    raise ServicioNoDisponible("Servicio no disponible.")
            
            if self.var == 1:
                if self.numero_de_equipos == 0:
                    raise ServicioNoDisponible("Servicio no disponible.")
                
            if self.var == 2:
                if self.numero_de_asesores == 0:
                    raise ServicioNoDisponible("Servicio no disponible.")

            reserva_obj = Reserva(cliente_obj, serv_obj)
            mensaje_exito = reserva_obj.procesar()
            print("3")
            if self.var == 0:
                self.numeros_de_salas = self.numeros_de_salas - 1
        
            if self.var == 1:
                self.numero_de_equipos = self.numero_de_equipos - 1

            if self.var == 2:
                self.numero_de_asesores = self.numero_de_asesores - 1
            total_cobro = serv_obj.calcular_costo() # Polimorfismo en el cálculo

            # Salida de información exitosa
            
            self.s = "salas disponibles: " + str(self.numeros_de_salas) + "  equipos disponibles: " + str(self.numero_de_equipos) + "  asesores disponibles: " + str(self.numero_de_asesores)
            self.label.config(text=str(self.s))
            self.txt_display.insert(tk.END, f"{mensaje_exito} | {serv_obj.obtener_detalles()} | Total: ${total_cobro:,.0f}\n")

        except DatosInvalidosErrorNo as se: # Captura falta de selección
            messagebox.showwarning("el nombre debe tener mas de 4 caracteres", str(se))
            logging.warning(f"Ingreso de dato invalido: {se}")
        except DatosInvalidosErrorCe as se1: # Captura falta de selección
            messagebox.showwarning("Debe ingresar un numero de cedula válida", str(se1))
            logging.warning(f"Ingreso de dato invalido: {se1}")
        except DatosInvalidosErrorCo as se2: # Captura falta de selección
            messagebox.showwarning("Debe ingresar un correo válido.", str(se2))
            logging.warning(f"Ingreso de dato invalido: {se2}")
        except DatosInvalidosErrorCa as se3: # Captura falta de selección
            messagebox.showwarning("Debe ingresar una numero entero en cantidad", str(se3))
            logging.warning(f"Ingreso de dato invalido: {se3}")
        except ServicioNoSeleccionadoError as sne: # Captura falta de selección
            messagebox.showwarning("Campo Faltante o no valido", str(sne))
            logging.warning(f"Intento de registro sin servicio: {sne}")
        except ValueError: # Captura error de letras en campos numéricos
            messagebox.showerror("Error de Formato", "La cantidad debe ser un número entero.")
            logging.error("Error de conversión: El usuario ingresó texto en cantidad.")
        except GestionError as ge: # Captura errores lógicos definidos por nosotros
            messagebox.showerror("Error de Negocio", str(ge))
            logging.error(f"Error controlado: {ge}")
        except ServicioNoDisponible as gi: # Captura errores lógicos definidos por nosotros
            messagebox.showerror("el servicio no se encuentra disponible", str(gi))
            logging.error(f"Servicio no esta disponible en el momento: {gi}")
        except Exception as e: # Captura cualquier fallo inesperado del sistema
            messagebox.showerror("Fallo Crítico", "Ocurrió un error inesperado. Revise el archivo de log.")
            logging.critical(f"Error sistémico: {e}", exc_info=True)
        else: # Si todo fue bien, limpia los campos
            self.ent_cliente.delete(0, tk.END)
            self.ent_cant.delete(0, tk.END)
            self.combo_tipo.set('')
        finally: # Siempre se ejecuta para asegurar cierre de procesos
            print("Intento de registro finalizado.")

# --- INICIO DE LA APLICACIÓN ---
if __name__ == "__main__":
    root = tk.Tk() # Inicializa el motor de Tkinter
    app = VentanaSoftwareFJ(root) # Crea la instancia de nuestra ventana
    root.mainloop() # Mantiene la ventana abierta y escuchando eventos
