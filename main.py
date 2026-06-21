# ============================================================
# SISTEMA DE AGENDA DE TURNOS DE PACIENTES - CLÍNICA
# Asignatura: Estructura de Datos - UEA 2026
# Autores
# Leonardo Benjamin Córdova Jaramillo
# Mayra Del Rocio Carrion Rodriguez
# Jefferson Jasmani Galeas Salazar
# Jeremy Xavier Guevara Barrera
# ============================================================

from dataclasses import dataclass

# ============================================================
# REGISTROS / ESTRUCTURAS (dataclass)
# ============================================================

@dataclass
class Especialidad:
    codigo: int
    nombre: str

@dataclass
class Paciente:
    id_paciente: str
    nombre: str
    edad: int
    contacto: str

# ============================================================
# CLASE TURNO - POO
# ============================================================

class Turno:
    def __init__(self, id_turno: int, paciente: Paciente,
                 especialidad: Especialidad, fecha: str,
                 hora: str, medico: str):
        self.id_turno     = id_turno
        self.paciente     = paciente
        self.especialidad = especialidad
        self.fecha        = fecha
        self.hora         = hora
        self.medico       = medico
        self.activo       = True  # booleano: estado del turno

    def cancelar(self):
        self.activo = False

    def __str__(self):
        estado = "Activo" if self.activo else "Cancelado"
        return (f"Turno N°{self.id_turno} | "
                f"Paciente: {self.paciente.nombre} | "
                f"Especialidad: {self.especialidad.nombre} | "
                f"Fecha: {self.fecha} {self.hora} | "
                f"Médico: {self.medico} | "
                f"Estado: {estado}")

# ============================================================
# CLASE PRINCIPAL DEL SISTEMA - POO
# ============================================================

class SistemaClinica:

    # DÍAS Y HORAS para la matriz de agenda semanal
    DIAS  = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    HORAS = ["08:00", "09:00", "10:00", "11:00", "14:00",
             "15:00", "16:00"]

    def __init__(self):
        # VECTORES (listas)
        self.pacientes:      list[Paciente]     = []
        self.turnos:         list[Turno]        = []
        self.especialidades: list[Especialidad] = []
        self.contador_turnos: int = 1

        # MATRIZ de agenda semanal (filas=horas, columnas=días)
        # Cada celda guarda "Libre" o el nombre del paciente
        self.agenda: list[list[str]] = [
            ["Libre"] * len(self.DIAS)
            for _ in range(len(self.HORAS))
        ]

        # Cargar especialidades iniciales
        self._cargar_especialidades()

    # ----------------------------------------------------------
    # DATOS INICIALES
    # ----------------------------------------------------------

    def _cargar_especialidades(self):
        datos = [
            (1, "Medicina General"),
            (2, "Pediatría"),
            (3, "Cardiología"),
            (4, "Traumatología"),
            (5, "Ginecología"),
        ]
        for cod, nom in datos:
            self.especialidades.append(Especialidad(cod, nom))

    # ----------------------------------------------------------
    # REGISTRAR PACIENTE
    # ----------------------------------------------------------

    def registrar_paciente(self):
        print("\n--- REGISTRAR PACIENTE ---")
        id_pac   = input("Identificación: ").strip()

        # Verificar que no exista
        for p in self.pacientes:
            if p.id_paciente == id_pac:
                print("⚠ Ya existe un paciente con esa identificación.")
                return

        nombre   = input("Nombre completo: ").strip()
        edad     = int(input("Edad: "))
        contacto = input("Número de contacto: ").strip()

        nuevo = Paciente(id_pac, nombre, edad, contacto)
        self.pacientes.append(nuevo)
        print(f"✔ Paciente '{nombre}' registrado correctamente.")

    # ----------------------------------------------------------
    # MOSTRAR PACIENTES
    # ----------------------------------------------------------

    def mostrar_pacientes(self):
        print("\n--- LISTA DE PACIENTES ---")
        if not self.pacientes:
            print("No hay pacientes registrados.")
            return
        for p in self.pacientes:
            print(f"  ID: {p.id_paciente} | "
                  f"Nombre: {p.nombre} | "
                  f"Edad: {p.edad} | "
                  f"Contacto: {p.contacto}")

    # ----------------------------------------------------------
    # MOSTRAR ESPECIALIDADES
    # ----------------------------------------------------------

    def mostrar_especialidades(self):
        print("\n--- ESPECIALIDADES DISPONIBLES ---")
        for e in self.especialidades:
            print(f"  [{e.codigo}] {e.nombre}")

    # ----------------------------------------------------------
    # ASIGNAR TURNO
    # ----------------------------------------------------------

    def asignar_turno(self):
        print("\n--- ASIGNAR TURNO ---")

        if not self.pacientes:
            print("⚠ No hay pacientes registrados.")
            return

        # Buscar paciente
        self.mostrar_pacientes()
        id_pac = input("\nIngrese ID del paciente: ").strip()
        paciente_sel = None
        for p in self.pacientes:
            if p.id_paciente == id_pac:
                paciente_sel = p
                break
        if not paciente_sel:
            print("⚠ Paciente no encontrado.")
            return

        # Seleccionar especialidad
        self.mostrar_especialidades()
        try:
            cod_esp = int(input("Ingrese código de especialidad: "))
        except ValueError:
            print("⚠ Código inválido.")
            return
        esp_sel = None
        for e in self.especialidades:
            if e.codigo == cod_esp:
                esp_sel = e
                break
        if not esp_sel:
            print("⚠ Especialidad no encontrada.")
            return

        # Seleccionar día y hora de la matriz
        print("\n--- AGENDA SEMANAL ---")
        self.mostrar_agenda()

        print("\nDías disponibles:")
        for i, dia in enumerate(self.DIAS):
            print(f"  [{i}] {dia}")
        try:
            idx_dia = int(input("Seleccione número de día: "))
        except ValueError:
            print("⚠ Opción inválida.")
            return

        print("\nHoras disponibles:")
        for i, hora in enumerate(self.HORAS):
            print(f"  [{i}] {hora}")
        try:
            idx_hora = int(input("Seleccione número de hora: "))
        except ValueError:
            print("⚠ Opción inválida.")
            return

        if not (0 <= idx_dia < len(self.DIAS) and
                0 <= idx_hora < len(self.HORAS)):
            print("⚠ Selección fuera de rango.")
            return

        if self.agenda[idx_hora][idx_dia] != "Libre":
            print("⚠ Ese horario ya está ocupado. Elija otro.")
            return

        fecha  = input("Ingrese fecha (DD/MM/AAAA): ").strip()
        medico = input("Ingrese nombre del médico: ").strip()
        hora   = self.HORAS[idx_hora]

        # Crear turno
        nuevo_turno = Turno(
            self.contador_turnos,
            paciente_sel,
            esp_sel,
            fecha,
            hora,
            medico
        )
        self.turnos.append(nuevo_turno)

        # Actualizar MATRIZ de agenda
        self.agenda[idx_hora][idx_dia] = paciente_sel.nombre

        self.contador_turnos += 1
        print(f"✔ Turno N°{nuevo_turno.id_turno} asignado correctamente.")

    # ----------------------------------------------------------
    # CONSULTAR TODOS LOS TURNOS
    # ----------------------------------------------------------

    def consultar_turnos(self):
        print("\n--- LISTA DE TURNOS ---")
        if not self.turnos:
            print("No hay turnos registrados.")
            return
        for t in self.turnos:
            print(f"  {t}")

    # ----------------------------------------------------------
    # CONSULTAR TURNO POR PACIENTE
    # ----------------------------------------------------------

    def consultar_por_paciente(self):
        print("\n--- CONSULTAR TURNOS POR PACIENTE ---")
        id_pac = input("Ingrese ID del paciente: ").strip()
        encontrados = [t for t in self.turnos
                       if t.paciente.id_paciente == id_pac]
        if not encontrados:
            print("No se encontraron turnos para ese paciente.")
            return
        for t in encontrados:
            print(f"  {t}")

    # ----------------------------------------------------------
    # CANCELAR TURNO
    # ----------------------------------------------------------

    def cancelar_turno(self):
        print("\n--- CANCELAR TURNO ---")
        self.consultar_turnos()
        if not self.turnos:
            return
        try:
            id_turno = int(input("\nIngrese N° de turno a cancelar: "))
        except ValueError:
            print("⚠ Número inválido.")
            return
        for t in self.turnos:
            if t.id_turno == id_turno and t.activo:
                t.cancelar()
                print(f"✔ Turno N°{id_turno} cancelado correctamente.")
                return
        print("⚠ Turno no encontrado o ya estaba cancelado.")

    # ----------------------------------------------------------
    # MOSTRAR MATRIZ DE AGENDA SEMANAL
    # ----------------------------------------------------------

    def mostrar_agenda(self):
        print("\n--- AGENDA SEMANAL (MATRIZ) ---")
        # Encabezado
        encabezado = f"{'Hora':<10}" + "".join(
            f"{dia:<15}" for dia in self.DIAS
        )
        print(encabezado)
        print("-" * (10 + 15 * len(self.DIAS)))
        # Filas de la matriz
        for i, hora in enumerate(self.HORAS):
            fila = f"{hora:<10}"
            for j in range(len(self.DIAS)):
                celda = self.agenda[i][j]
                fila += f"{celda:<15}"
            print(fila)

    # ----------------------------------------------------------
    # MENÚ PRINCIPAL
    # ----------------------------------------------------------

    def menu(self):
        while True:
            print("\n" + "=" * 45)
            print("   AGENDA DE TURNOS - CLÍNICA UEA")
            print("=" * 45)
            print("  1. Registrar paciente")
            print("  2. Asignar turno")
            print("  3. Consultar todos los turnos")
            print("  4. Consultar turnos por paciente")
            print("  5. Cancelar turno")
            print("  6. Ver agenda semanal (Matriz)")
            print("  7. Ver lista de pacientes")
            print("  8. Salir")
            print("=" * 45)

            opcion = input("  Seleccione una opción: ").strip()

            if   opcion == "1": self.registrar_paciente()
            elif opcion == "2": self.asignar_turno()
            elif opcion == "3": self.consultar_turnos()
            elif opcion == "4": self.consultar_por_paciente()
            elif opcion == "5": self.cancelar_turno()
            elif opcion == "6": self.mostrar_agenda()
            elif opcion == "7": self.mostrar_pacientes()
            elif opcion == "8":
                print("\n✔ Saliendo del sistema. ¡Hasta pronto!\n")
                break
            else:
                print("⚠ Opción no válida. Intente de nuevo.")

# ============================================================
# PUNTO DE ENTRADA
# ============================================================

if __name__ == "__main__":
    sistema = SistemaClinica()
    sistema.menu()