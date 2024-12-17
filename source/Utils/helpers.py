from datetime import datetime

def calcular_edad(fecha_nacimiento):
    """Calcula la edad en años a partir de la fecha de nacimiento."""
    if isinstance(fecha_nacimiento, str):
        # Convierte el texto a un objeto datetime.date
        fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()
    hoy = datetime.today().date()
    return hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

def calcular_antiguedad(fecha_inicio):
    if isinstance(fecha_inicio, str):  # Si es una cadena, conviértela a una fecha
        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
    hoy = datetime.now().date()
    return hoy.year - fecha_inicio.year - ((hoy.month, hoy.day) < (fecha_inicio.month, fecha_inicio.day))