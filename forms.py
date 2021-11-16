# Importamos librerias
import os
from babel.numbers import parse_number
from flask import Flask, render_template,redirect,url_for, flash,request,session
from flask import jsonify
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import mysql.connector
import wtforms
from controlador_usu import insertar_usu
from flask import send_from_directory

from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,IntegerField,DecimalField
from wtforms.validators import DataRequired

from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash, check_password_hash

from bd import db_connection
from flask_mail import Mail,Message
import smtplib
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField,IntegerField,DateField,HiddenField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField


# Funciones

def llenarProveedor():
    conexion=db_connection()
    cursor = conexion.cursor()
    cursor.execute("SELECT DISTINCT proveedor FROM productos GROUP BY proveedor")
    _productos=cursor.fetchall()
    conexion.commit()
    _Proveedor=[]
    for producto in _productos:
        _Proveedor.append(producto)
    return _Proveedor

def llenarProductos():
    conexion=db_connection()
    cursor = conexion.cursor()
    cursor.execute("SELECT DISTINCT producto FROM productos GROUP BY producto")
    _productos=cursor.fetchall()
    conexion.commit()
    _Producto=[]
    for producto in _productos:
        _Producto.append(producto)
    return _Producto




#Creamos los Form Class
class SalidasForm(FlaskForm):
    #Select Choices
    my_choices = [('1', 'Clientes'), ('2', 'belnu'), ('3', 'buenos aires'), ('4', 'cordoba'),('5', 'rosario')]
    
    proveedores=llenarProveedor()
    my_proveedores=[]
    indice=1
    my_proveedores.append((str(indice),"Provedoores ...."))    
    for proveedores in proveedores:
        indice = indice + 1
        my_proveedores.append((str(indice),proveedores[0]))
    print(my_proveedores)
    print(my_choices)
    print(type(my_choices))
    print(type(proveedores))
    
    productos=llenarProductos()
    my_productos=[]
    indice=1
    my_productos.append((str(indice),"Productos ...."))
    for producto in productos:
        indice = indice + 1
        my_productos.append((str(indice),producto[0]))
    print(my_productos)
    print(type(productos))
    
    
    
    fecha=DateField("Fecha salida:")
    proveedor=SelectField("Proveedor:",choices=my_proveedores, render_kw={"placeholder": "Proveedores ...."})
    cliente=SelectField("Cliente:",choices=my_choices, render_kw={"placeholder": "Clientes ...."})
    producto=SelectField("Producto:",choices=my_productos, render_kw={"placeholder": "Productos ...."})
    cantidad=IntegerField("Cantidad:")
    precio_costo=DecimalField("Precio Costo:")
    factura_costo=HiddenField("Factura Costo")
    precio_venta=DecimalField("Precio Venta:")
    factura_venta=HiddenField("Factura Venta")
    utilidad_unidad=HiddenField("Utilidad x U.:")
    utilidad_total=HiddenField("Utilidad Total")
    cantidad_vendida=HiddenField("Cantidad Vendida:")
    stock=HiddenField("Stock:")
    saldo=HiddenField("Saldo:")
    liquidado=HiddenField("Liquidado:")
    submit=SubmitField("Guardar")



