from .models import Table_usuario
from database import SessionLocal
from .security import hashear_contra
from datetime import datetime, date
# Crear una sesión global para la base de datos
db = SessionLocal()

# Función para calcular la edad a partir de la fecha de nacimiento
def calcular_edad(fecha_nacimiento):
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return edad

# Para agregar usuarios a la tabla usuarios
def agregar_usuario(Nombre_completo, username, password, rol, foto=None, fecha_nacimiento=None, fecha_inicio=None, ultimo_editor=None):
    sesion = SessionLocal()
    try:
        nuevo_usuario = Table_usuario(
            nombre=Nombre_completo,
            username=username,
            password=hashear_contra(password),
            rol=rol,
            foto=foto,
            fecha_nacimiento=fecha_nacimiento,
            fecha_inicio=fecha_inicio,
            antiguedad=calcular_antiguedad(fecha_inicio),
            ultimo_editor=ultimo_editor
        )
        sesion.add(nuevo_usuario)
        sesion.commit()
    except Exception as e:
        sesion.rollback()
        raise e
    finally:
        sesion.close()

# Para listar usuarios de la tabla usuarios
def listar_usuarios():
    with SessionLocal() as db:
        usuarios = db.query(Table_usuario).all()
    return usuarios

# Para registrar actividades en la tabla de logs
def registrar_actividad(usuario_id, accion):
    with SessionLocal() as db:
        nueva_actividad = {
            'usuario_id': usuario_id,
            'accion': accion,
            'fecha': datetime.now()
        }
        db.execute(
            "INSERT INTO logs (usuario_id, accion, fecha) VALUES (:usuario_id, :accion, :fecha)",
            nueva_actividad
        )
        db.commit()

# Para editar usuarios de la tabla usuarios
def editar_usuario(usuario_id, **kwargs):
    with SessionLocal() as db:
        usuario = db.query(Table_usuario).get(usuario_id)
        if usuario:
            for campo, valor in kwargs.items():
                if campo == "password" and valor:  # Hashear la contraseña si se va a cambiar
                    setattr(usuario, campo, hashear_contra(valor))
                elif campo == "fecha_nacimiento" and valor:  # Calcular edad si cambia la fecha de nacimiento
                    setattr(usuario, campo, valor)
                    usuario.edad = calcular_edad(valor)
                else:
                    setattr(usuario, campo, valor)
            db.commit()
            return f"Usuario ID {usuario_id} actualizado correctamente."
        return "Usuario no encontrado."

# Eliminar un usuario de la tabla usuarios
def eliminar_usuario(usuario_id):
    with SessionLocal() as db:
        usuario = db.query(Table_usuario).get(usuario_id)
        if usuario:
            db.delete(usuario)
            db.commit()
            return f"Usuario ID {usuario_id} eliminado correctamente."
        return "Usuario no encontrado."

# Calcular antigüedad a partir de la fecha de inicio
def calcular_antiguedad(fecha_inicio):
    if fecha_inicio:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        antiguedad = (datetime.now() - fecha_inicio_dt).days // 365  # Convertir a años
        return antiguedad
    return 0
