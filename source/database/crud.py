import os
from .models import Table_usuario,Inventario,MovimientoInventario
from sqlalchemy.orm import Session
from source.database.database import SessionLocal
from .security import hashear_contra
from datetime import datetime
from source.Utils.auditoria import registrar_accion

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

def agregar_producto(session: Session, nombre_producto, descripcion, categoria, tipo, unidad_medida, precio, codigo_barras, cantidad_stock, activo, foto=None):
    if foto and os.path.exists(foto):
        _, extension = os.path.splitext(foto)
        nueva_foto_path = f"source/imagenes/productos/{nombre_producto}_item{extension}"
        os.makedirs(os.path.dirname(nueva_foto_path), exist_ok=True)
        if os.path.exists(nueva_foto_path):
            os.remove(nueva_foto_path)
        os.rename(foto, nueva_foto_path)
        foto = nueva_foto_path
    else:
        foto = None  # Asegúrate de que foto es None si no existe el archivo

    nuevo_producto = Inventario(
        nombre_producto=nombre_producto,
        descripcion=descripcion,
        categoria=categoria,
        tipo=tipo,
        unidad_medida=unidad_medida,
        precio=precio,
        codigo_barras=codigo_barras,
        cantidad_stock=cantidad_stock,
        activo=activo,
        foto=foto
    )
    session.add(nuevo_producto)
    session.commit()
    registrar_movimiento(session, nuevo_producto.id, "entrada", cantidad_stock, "Inventario inicial")
    session.refresh(nuevo_producto)
    return nuevo_producto.id

def listar_inventario(db, activo=None):
    query = "SELECT * FROM inventario"
    if (activo is not None):
        query += " WHERE activo = %s"
        values = (int(activo),)
    else:
        values = ()
    
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, values)
    return cursor.fetchall()

def actualizar_producto(session: Session, producto_id, nombre_producto=None, descripcion=None, categoria=None, tipo=None, unidad_medida=None, precio=None, codigo_barras=None, cantidad_stock=None, activo=None, foto=None):
    producto = session.query(Inventario).filter(Inventario.id == producto_id).first()
    if not producto:
        raise ValueError("Producto no encontrado")

    if nombre_producto is not None:
        producto.nombre_producto = nombre_producto
    if descripcion is not None:
        producto.descripcion = descripcion
    if categoria is not None:
        producto.categoria = categoria
    if tipo is not None:
        producto.tipo = tipo
    if unidad_medida is not None:
        producto.unidad_medida = unidad_medida
    if precio is not None:
        producto.precio = precio
    if codigo_barras is not None:
        producto.codigo_barras = codigo_barras
    if cantidad_stock is not None:
        producto.cantidad_stock = cantidad_stock
    if activo is not None:
        producto.activo = activo
    if foto and os.path.exists(foto):
        _, extension = os.path.splitext(foto)
        nueva_foto_path = f"source/imagenes/productos/{nombre_producto}_item{extension}"
        os.makedirs(os.path.dirname(nueva_foto_path), exist_ok=True)
        if os.path.exists(nueva_foto_path):
            os.remove(nueva_foto_path)
        os.rename(foto, nueva_foto_path)
        producto.foto = nueva_foto_path

    session.commit()
    registrar_movimiento(session, producto.id, "actualizacion", cantidad_stock, "Inventario inicial")
    session.refresh(producto)
    return producto.id

def buscar_producto(session: Session, producto_id):
    return session.query(Inventario).filter(Inventario.id == producto_id).first()

def eliminar_producto(session: Session, usuario_id, producto_id):
    producto = session.query(Inventario).filter(Inventario.id == producto_id).first()
    if producto:
        producto.activo = False  # Marcar el producto como inactivo
        session.commit()
        
        # Registrar acción en auditoría
        registrar_accion(usuario_id, "Eliminar Producto", f"Producto {producto.nombre_producto} marcado como inactivo.")

def registrar_movimiento(session: Session, producto_id, tipo_movimiento, cantidad, descripcion=None):
    movimiento = MovimientoInventario(
        producto_id=producto_id,
        tipo_movimiento=tipo_movimiento,
        cantidad=cantidad,
        descripcion=descripcion
    )
    session.add(movimiento)
    session.commit()
    session.refresh(movimiento)
    return movimiento.id

def obtener_movimientos(session: Session, producto_id=None):
    query = session.query(MovimientoInventario)
    if producto_id:
        query = query.filter(MovimientoInventario.producto_id == producto_id)
    return query.all()