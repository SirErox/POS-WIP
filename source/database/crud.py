import os
from datetime import datetime
from sqlalchemy.orm import Session
from source.database.database import SessionLocal
from source.Utils.auditoria import registrar_accion
from source.Utils.helpers import calcular_antiguedad

from .models import (
    ProductoProveedor,
    Proveedor,
    Usuarios,
    Inventario,
    MovimientoInventario,
    Ventas,
    DetalleVenta,
)
from .security import hashear_contra
class CRUDUsuarios:
    """Manejo de usuarios"""

    @staticmethod
    def agregar_usuario(
        nombre_completo,
        username,
        password,
        rol,
        curp,
        foto=None,
        fecha_nacimiento=None,
        fecha_inicio=None,
        ultimo_editor=None,
    ):
        antiguedad = calcular_antiguedad(fecha_inicio)
        with SessionLocal() as sesion:
            try:
                nuevo_usuario = Usuarios(
                    nombre_completo=nombre_completo,
                    username=username,
                    password=hashear_contra(password),
                    rol=rol,
                    foto_perfil=foto,
                    curp=curp,
                    fecha_nacimiento=fecha_nacimiento,
                    fecha_inicio=fecha_inicio,
                    antiguedad=antiguedad,
                    ultimo_editor=ultimo_editor,
                )
                sesion.add(nuevo_usuario)
                sesion.commit()
            except Exception as e:
                sesion.rollback()
                raise e

    @staticmethod
    def listar_usuarios():
        with SessionLocal() as sesion:
            return sesion.query(Usuarios).all()

    @staticmethod
    def registrar_actividad(usuario_id, accion):
        with SessionLocal() as sesion:
            try:
                nueva_actividad = {
                    'usuario_id': usuario_id,
                    'accion': accion,
                    'fecha': datetime.now()
                }
                sesion.execute(
                    "INSERT INTO logs (usuario_id, accion, fecha) VALUES (:usuario_id, :accion, :fecha)",
                    nueva_actividad
                )
                sesion.commit()
            except Exception as e:
                sesion.rollback()
                raise e

    @staticmethod
    def editar_usuario(user_data):
        with SessionLocal() as session:
            try:
                usuario = session.query(Usuarios).filter_by(id=user_data["id"]).first()
                if not usuario:
                    raise Exception("Usuario no encontrado.")
                usuario.nombre_completo = user_data["nombre_completo"]
                usuario.username = user_data["username"]
                usuario.rol = user_data["rol"]
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    @staticmethod
    def eliminar_usuario(user_id):
        with SessionLocal() as session:
            try:
                usuario = session.query(Usuarios).filter_by(id=user_id).first()
                if not usuario:
                    raise Exception("Usuario no encontrado.")
                session.delete(usuario)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

class CRUDInventario:
    # Metodos relacionados a manejo de inventario
    @staticmethod
    def agregar_producto(
        session,
        nombre_producto,
        descripcion,
        categoria,
        tipo,
        unidad_medida,
        precio,
        codigo_barras,
        cantidad_stock,
        activo,
        foto=None,
    ):
        if foto and os.path.exists(foto):
            _, extension = os.path.splitext(foto)
            nueva_foto_path = f"source/imagenes/productos/{nombre_producto}_item{extension}"
            os.makedirs(os.path.dirname(nueva_foto_path), exist_ok=True)
            if os.path.exists(nueva_foto_path):
                os.remove(nueva_foto_path)
            os.rename(foto, nueva_foto_path)
            foto = nueva_foto_path

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
            foto=foto,
        )
        session.add(nuevo_producto)
        session.commit()

        CRUDInventario.registrar_movimiento(
            session,
            nuevo_producto.id,
            "entrada",
            cantidad_stock,
            "Inventario inicial",
        )
        session.refresh(nuevo_producto)
        return nuevo_producto.id

    @staticmethod
    def listar_usuarios():
        with SessionLocal() as sesion:
            return sesion.query(Usuarios).all()
    
    @staticmethod
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
        CRUDInventario.registrar_movimiento(session, producto.id, "actualizacion", cantidad_stock, "Inventario inicial")
        session.refresh(producto)
        return producto.id
    
    @staticmethod
    def buscar_producto(session: Session, producto_id):
        return session.query(Inventario).filter(Inventario.id == producto_id).first()
    
    @staticmethod
    def eliminar_producto(session: Session, usuario_id, producto_id):
        producto = session.query(Inventario).filter(Inventario.id == producto_id).first()
        if producto:
            producto.activo = False  # Marcar el producto como inactivo
            session.commit()
        
        # Registrar acción en auditoría
            registrar_accion(usuario_id, "Eliminar Producto", f"Producto {producto.nombre_producto} marcado como inactivo.")

    @staticmethod
    def registrar_movimiento(
        session: Session, producto_id, tipo_movimiento, cantidad, descripcion=None
    ):
        movimiento = MovimientoInventario(
            producto_id=producto_id,
            tipo_movimiento=tipo_movimiento,
            cantidad=cantidad,
            descripcion=descripcion,
        )
        session.add(movimiento)
        session.commit()
        session.refresh(movimiento)
        return movimiento.id

    @staticmethod
    def obtener_movimientos(session: Session, producto_id=None):
        query = session.query(MovimientoInventario)
        if producto_id:
            query = query.filter(MovimientoInventario.producto_id == producto_id)
        return query.all()

    @staticmethod
    def registrar_venta(session: Session, usuario_id, productos, metodo_pago, cambio, recibo_generado):
        """
        Registra una venta y actualiza el stock de los productos involucrados.
    
        :param session: Sesión SQLAlchemy.
        :param usuario_id: ID del usuario que realiza la venta.
        :param productos: Lista de productos a vender. Cada producto es un diccionario con 'id', 'cantidad', y 'precio_unitario'.
        :param metodo_pago: Método de pago utilizado (efectivo, tarjeta, etc.).
        :param cambio: Cambio entregado al cliente.
        :param recibo_generado: Tipo de recibo generado (digital, impreso, ninguno).
        :return: ID de la venta registrada.
        """
        try:
            # Validar el stock de todos los productos antes de registrar la venta
            for producto in productos:
                item_inventario = session.query(Inventario).filter_by(id=producto['id']).first()
                if not item_inventario:
                    raise ValueError(f"Producto con ID {producto['id']} no encontrado")
            
                if item_inventario.tipo == 'producto' and item_inventario.cantidad_stock < producto['cantidad']:
                    raise ValueError(
                        f"Stock insuficiente para el producto '{item_inventario.nombre_producto}'. "
                        f"Disponible: {item_inventario.cantidad_stock}, Requerido: {producto['cantidad']}"
                    )

            # Calcular el total de la venta
            total = sum(p['cantidad'] * p['precio_unitario'] for p in productos)

            # Crear la venta
            nueva_venta = Ventas(
                usuario_id=usuario_id,
                fecha=datetime.now(),
                metodo_pago=metodo_pago,
                total=total,
                cambio=cambio,
                recibo_generado=recibo_generado
            )
            session.add(nueva_venta)
            session.commit()  # Confirmar la venta antes de registrar detalles

            # Registrar los detalles de la venta y actualizar stock
            for producto in productos:
                detalle = DetalleVenta(
                    venta_id=nueva_venta.id,
                    producto_id=producto['id'],
                    cantidad=producto['cantidad'],
                    precio_unitario=producto['precio_unitario']
                )
                session.add(detalle)

                # Reducir el stock del producto
                item_inventario = session.query(Inventario).filter_by(id=producto['id']).first()
                if item_inventario.tipo == 'producto':  # Solo reducir stock si es un producto
                    item_inventario.cantidad_stock -= producto['cantidad']

            # Confirmar todos los cambios
            session.commit()
            return nueva_venta.id
        except Exception as e:
            session.rollback()
            raise e
    
    """Proovedores CRUD"""
class CRUDProveedores:
    # Metodos relacionados a manejo de proveedores
    @staticmethod
    def agregar_proveedor(
        session,
        nombre,
        rfc=None,
        tipo_proveedor="local",
        contacto=None,
        telefono=None,
        correo=None,
        direccion=None,
        notas=None,
        activo=True,
    ):
        nuevo_proveedor = Proveedor(
            nombre=nombre,
            rfc=rfc,
            tipo_proveedor=tipo_proveedor,
            contacto=contacto,
            telefono=telefono,
            correo=correo,
            direccion=direccion,
            notas=notas,
            activo=activo,
        )
        session.add(nuevo_proveedor)
        session.commit()
        return nuevo_proveedor.id

    @staticmethod
    def editar_proveedor(session, proveedor_id, rfc=None, **kwargs):
        proveedor = session.query(Proveedor).filter_by(id=proveedor_id).first()
        if not proveedor:
            raise ValueError("Proveedor no encontrado")

        # Actualiza los campos necesarios
        if rfc is not None:
            proveedor.rfc = rfc
        for key, value in kwargs.items():
            if hasattr(proveedor, key):
                setattr(proveedor, key, value)

        session.commit()

    @staticmethod
    def listar_proveedores(session, activo=True):
        proveedores = session.query(Proveedor).filter_by(activo=activo).all()
        return [
            {
                "id": p.id,
                "nombre": p.nombre,
                "rfc": p.rfc or "N/A",
                "tipo_proveedor": p.tipo_proveedor,
                "contacto": p.contacto,
                "telefono": p.telefono,
                "correo": p.correo,
                "direccion": p.direccion,
                "notas": p.notas,
                "activo": p.activo
            }
            for p in proveedores
        ]

    @staticmethod
    def agregar_relacion_producto_proveedor(session, producto_id, proveedor_id, precio_compra, tiempo_entrega=None, cantidad_minima=0):
        relacion = ProductoProveedor(
            producto_id=producto_id,
            proveedor_id=proveedor_id,
            precio_compra=precio_compra,
            tiempo_entrega=tiempo_entrega,
            cantidad_minima=cantidad_minima
        )
        session.add(relacion)
        session.commit()
        return relacion.id

    @staticmethod
    def listar_proveedores_por_producto(session, producto_id):
        relaciones = session.query(ProductoProveedor).filter_by(producto_id=producto_id).all()
        return [
            {
                "proveedor_id": r.proveedor_id,
                "nombre_proveedor": r.proveedor.nombre,
                "precio_compra": r.precio_compra,
                "tiempo_entrega": r.tiempo_entrega,
                "cantidad_minima": r.cantidad_minima
            }
            for r in relaciones
        ]

    @staticmethod
    def editar_relacion_producto_proveedor(session, relacion_id, **kwargs):
        relacion = session.query(ProductoProveedor).filter_by(id=relacion_id).first()
        if not relacion:
            raise ValueError("Relación no encontrada")

        for key, value in kwargs.items():
            if hasattr(relacion, key):
                setattr(relacion, key, value)
        session.commit()

    @staticmethod
    def agregar_proveedor_producto(session, producto_id, proveedor_id, precio_compra, tiempo_entrega=None, cantidad_minima=0):
        """
        Crea una relación entre un producto y un proveedor.

        :param session: Sesión de SQLAlchemy.
        :param producto_id: ID del producto.
        :param proveedor_id: ID del proveedor.
        :param precio_compra: Precio de compra del producto al proveedor.
        :param tiempo_entrega: Tiempo de entrega estimado (opcional).
        :param cantidad_minima: Cantidad mínima de pedido (opcional).
        :return: ID de la relación creada.
        """
        try:
            nueva_relacion = ProductoProveedor(
                producto_id=producto_id,
                proveedor_id=proveedor_id,
                precio_compra=precio_compra,
                tiempo_entrega=tiempo_entrega,
                cantidad_minima=cantidad_minima
            )
            session.add(nueva_relacion)
            session.commit()
            session.refresh(nueva_relacion)
            return nueva_relacion.id
        except Exception as e:
            session.rollback()
            raise e