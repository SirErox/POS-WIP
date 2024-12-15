from datetime import date

def calcular_edad(fecha_nacimiento):
    """Calcula la edad en años a partir de la fecha de nacimiento."""
    hoy = date.today()
    return hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

def calcular_antiguedad(fecha_inicio):
    """Calcula la antigüedad en años a partir de la fecha de inicio."""
    hoy = date.today()
    return hoy.year - fecha_inicio.year - ((hoy.month, hoy.day) < (fecha_inicio.month, fecha_inicio.day))