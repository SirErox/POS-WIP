from .models import Table_usuario
from database import SessionLocal
from .security import hashear_contra
from datetime import datetime

#creamos sesion
db=SessionLocal()

#para agregar usuarios a la tabla usuarios
def agregar_usuario(nombre, username, password,rol):
    hashed_password=hashear_contra(password)
    nuevo_usuario=Table_usuario(nombre=nombre,username=username,password=hashed_password,rol=rol)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh()
    return nuevo_usuario
#para listar usuarios de la tabla usuarios
def listar_usuarios():
    usuarios=db.query(Table_usuario).all()
    return usuarios

def registrar_actividad(usuario_id, accion):
    nueva_actividad = {
        'usuario_id': usuario_id,
        'accion': accion,
        'fecha': datetime.now()
    }
    db.execute("INSERT INTO logs (usuario_id, accion, fecha) VALUES (:usuario_id, :accion, :fecha)", nueva_actividad)
    db.commit()

#para editar usuarios de la tabla usuarios
def editar_usuario(usuario_id, nuevo_nombre=None, nuevo_username=None, nuevo_rol=None):
    usuario = db.query(Table_usuario).get(usuario_id)
    if usuario:
        if nuevo_nombre:
            usuario.nombre = nuevo_nombre
        if nuevo_username:
            usuario.username = nuevo_username
        if nuevo_rol:
            usuario.rol = nuevo_rol
        db.commit()
        return f"Usuario ID {usuario_id} actualizado correctamente."
    return "Usuario no encontrado."
#eliminar un usuario de la tabla usuarios
def eliminar_usuario(usuario_id):
    usuario = db.query(Table_usuario).get(usuario_id)
    if usuario:
        db.delete(usuario)
        db.commit()
        return f"Usuario ID {usuario_id} eliminado correctamente."
    return "Usuario no encontrado."