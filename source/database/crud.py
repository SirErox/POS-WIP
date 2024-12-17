from .models import Table_usuario
from source.database.database import SessionLocal
from .security import hashear_contra
from datetime import datetime
# Crear una sesión global para la base de datos
db = SessionLocal()

# Función para calcular la edad a partir de la fecha de nacimiento
def calcular_edad(fecha_nacimiento):
    if isinstance(fecha_nacimiento, str):
        # Convierte el texto a un objeto datetime.date
        fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()
    hoy = datetime.today().date()
    return hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

# Para agregar usuarios a la tabla usuarios
def agregar_usuario(nombre_completo, username, password, rol,curp, foto=None, fecha_nacimiento=None, fecha_inicio=None, ultimo_editor=None):
    sesion = SessionLocal()
    try:
        nuevo_usuario = Table_usuario(
            nombre_completo=nombre_completo,
            username=username,
            password=hashear_contra(password),
            rol=rol,
            foto_perfil=foto,
            curp=curp,
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
def editar_usuario(user_data):
    """Editar un usuario en la base de datos."""
    session = SessionLocal()
    try:
        usuario = session.query(Table_usuario).filter_by(id=user_data["id"]).first()
        if not usuario:
            raise Exception("Usuario no encontrado.")

        usuario.nombre_completo = user_data["nombre_completo"]
        usuario.username = user_data["username"]
        usuario.rol = user_data["rol"]

        session.commit()  # Guardar los cambios
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

    # Eliminar un usuario de la tabla usuarios
def eliminar_usuario(user_id):
    """Eliminar un usuario en la base de datos."""
    session = SessionLocal()
    try:
        usuario = session.query(Table_usuario).filter_by(id=user_id).first()
        if not usuario:
            raise Exception("Usuario no encontrado.")

        session.delete(usuario)
        session.commit()  # Guardar los cambios
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

# Calcular antigüedad a partir de la fecha de inicio
def calcular_antiguedad(fecha_inicio):
    if fecha_inicio:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        antiguedad = (datetime.now() - fecha_inicio_dt).days // 365  # Convertir a años
        return antiguedad
    return 0
