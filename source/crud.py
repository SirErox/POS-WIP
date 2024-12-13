from sqlalchemy.orm import sessionmaker
from .models import Table_usuario
from .config_db import engine
from .security import hashear_contra

#creamos sesion
Sesion=sessionmaker(bind=engine)
sesion=Sesion()

#para agregar usuarios a la tabla usuarios
def agregar_usuario(nombre, username, password,rol):
    hashed_password=hashear_contra(password)
    nuevo_usuario=Table_usuario(nombre=nombre,username=username,password=hashed_password,rol=rol)
    sesion.add(nuevo_usuario)
    sesion.commit()

    return f"usuario {nuevo_usuario} añadido correctamente"
#para listar usuarios de la tabla usuarios
def listar_usuarios():
    usuarios=sesion.query(Table_usuario).all()
    return usuarios
#para editar usuarios de la tabla usuarios
def editar_usuario(usuario_id, nuevo_nombre=None, nuevo_username=None, nuevo_rol=None):
    usuario = sesion.query(Table_usuario).get(usuario_id)
    if usuario:
        if nuevo_nombre:
            usuario.nombre = nuevo_nombre
        if nuevo_username:
            usuario.username = nuevo_username
        if nuevo_rol:
            usuario.rol = nuevo_rol
        sesion.commit()
        return f"Usuario ID {usuario_id} actualizado correctamente."
    return "Usuario no encontrado."
#eliminar un usuario de la tabla usuarios
def eliminar_usuario(usuario_id):
    usuario = sesion.query(Table_usuario).get(usuario_id)
    if usuario:
        sesion.delete(usuario)
        sesion.commit()
        return f"Usuario ID {usuario_id} eliminado correctamente."
    return "Usuario no encontrado."