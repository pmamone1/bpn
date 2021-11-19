# Importamos librerias
import decimal
import os
from typing import cast
from babel.numbers import parse_decimal, parse_number
from flask import Flask, render_template,redirect,url_for, flash,request,session,make_response
from flask import jsonify
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import mysql.connector
#from pymysql import NULL
from controlador_usu import insertar_usu
from flask import send_from_directory

from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,BooleanField,PasswordField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField

from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash, check_password_hash

from bd import db_connection
from flask_mail import Mail,Message
import smtplib

from forms import SalidasForm
from datetime import date


#  creamos instancia de flask
app = Flask(__name__)
#app.debug = True
#IS_DEV = app.env == 'development'  # FLASK_ENV env. variable

# secret key
app.config['SECRET_KEY']= "Pablo Mamone ultra secreta clave que en ingles quiere decir secret key"

#Configuramos MySQL 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pablo1612@localhost/bpn'
db = SQLAlchemy(app)
    
#configuramos carpeta de fotos de productos
CARPETA = os.path.join('uploads')
app.config['CARPETA'] = CARPETA

#Variable global nombre de usuario
USUARIO ='usuario'


# Configuramos Variables para enviar mails
mail1 = Mail()
mail1.init_app(app)

# Inicializamos el MAIN #
#if __name__ == '__main__':
    # guaranteed to not be run on a production server
#    assert os.path.exists('.env')  # for other environment variables...
#    os.environ['FLASK_ENV'] = 'development'  # HARD CODE since default is production
#    os.environ['FLASK_APP'] = 'app.py'
#    app.run(debug=True, port =8000)    

    
####################################################################################################################
####################################################################################################################
########      FUNCIONES    #########################################################################################
####################################################################################################################

#funcion buscar si existe el mail        
def buscaUsuario(email):
    conexion=db_connection()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM usuarios WHERE email= %s",(email))
        existe = cursor.fetchone()
   #     print(existe)
        USUARIO=existe[1]
   #     print("Se acaba de asiganr el usuario a la vatriable usuario : {}".format(USUARIO))
        conexion.close()
        if existe:
    #        print("encontro el usuario") 
            return True
        else:
    #        print("no existe")
            return False 
        
# funcion chequear si el password es correcto
def check_password(email,password):
    conexion=db_connection()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM usuarios WHERE email= %s",(email))
        existe = cursor.fetchone()
        conexion.close()
        if check_password_hash(existe[3] ,password):
    #        print("existe el email y la contraseña")
            return True
        else:
    #        print("esta mal la contraseña")
            return False
app.config.update(
# Configuración del email
MAIL_SERVER = 'smtp.gmail.com',
MAIL_PORT = 587,
MAIL_USE_TLS = True,
MAIL_USERNAME = 'pmamone1@gmail.com',
MAIL_PASSWORD = 'lwmpmzlhglqbdpcx',
MAIL_USE_SSL = False,
)

# funcion envio del mail de alta de usuario
def enviar_mail_alta(email,password):
    conexion=db_connection()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM usuarios WHERE email= %s",(email))
        existe = cursor.fetchone()
        conexion.close()
        nombre= existe[1]
        mail = existe[2]
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login("pmamone1@gmail.com","lwmpmzlhglqbdpcx")
        msg ="Felicitaciones!!!!!    " + nombre + ", has creado una cuenta... Bienvenido a Bpn !!!!"
        server.sendmail("pmamone1@gmail.com",mail,msg)
        

####################################################################################################################
####################################################################################################################
########      RUTAS    #############################################################################################
####################################################################################################################

#ruta de la carpeta de fotos de productos
@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config["CARPETA"],nombreFoto)

# creamos una ruta o decorador inicial para login
@app.route('/')
@app.route('/login')
def index():
    return render_template('index.html')

# ruta para registrarse
@app.route('/registracion')
def registracion():
    return render_template('registracion.html')
        
# ruta que guarda el nuevo usuario
@app.route('/reg_guardado', methods=['get','post'])
def reg_guardado():
    nombre=request.form["nombre"]
    email=request.form['email'] 
    passw=request.form['pass']
    user =generate_password_hash(passw)
    if nombre=="" or email=="" or passw=="":
        flash("Faltan completar Campos!")
        return ('')
    else:
    #    print(email)
    #    print(passw)
        insertar_usu(nombre,email,user)
        enviar_mail_alta(email,passw)
        flash("{}, has creado un nuevo Usuario !!!".format(nombre))
        return redirect("/login")


# ruta principal vacia una vez logueado
@app.route('/home',methods=['get','post'])
def home():
    # esto va a haber que cambiarlo esta forma de pasar el usuario entre paginas
    email=request.args.get("email")
    passwd=request.args.get("passw")
    if buscaUsuario(email):
        if check_password(email,passwd):    
            resp=make_response(render_template('home.html',usu=email))
            resp.set_cookie("username",email)
            return resp
            #return render_template("home.html",usu=email)
        else:
            flash(("La contraseña es incorrecta!"))
            return redirect(('/login'))
    else:
        flash("El usuario no existe!")
        return redirect('/login')     


#ruta de consulta de la base de datos
@app.route('/consultaProductos', methods=['GET', 'POST'])
def consultaProductos():
    sql="SELECT * FROM productos"
    conexion=db_connection()
    cursor = conexion.cursor()
    cursor.execute(sql)
    _productos=cursor.fetchall()
   # print(_productos)
    conexion.commit()
    return render_template("consulta_productos.html",productos=_productos)

@app.route('/buscar',methods=['post'])
def buscar():
    proveedor=request.form["proveedor"]
 #   print(f"El proveedor es {proveedor}")
    conexion=db_connection()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos where proveedor like '%"+proveedor+"%' or producto like '%"+proveedor+"%'")
    _productos=cursor.fetchall()
  #  print(_productos)
    conexion.commit()
    return render_template("consulta_productos.html",productos=_productos)

#ruta de eliminacion de productos    
@app.route('/eliminarProducto/<int:id>')
def eliminarProducto(id):
    conexion=db_connection()
    cursor = conexion.cursor()
    cursor.execute("SELECT imagen FROM productos WHERE id_producto=%s",id)
    fila=cursor.fetchall()
    os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))
    cursor.execute("DELETE FROM productos WHERE id_producto=%s",(id))
    conexion.commit()
    conexion.close()
    return redirect("/consultaProductos")

#ruta de edicion de productos
@app.route('/editarProducto/<int:id>')
def editarProducto(id):
    conexion=db_connection()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos where id_producto=%s",(id))
    _producto=cursor.fetchall()
   # print(_producto)
    conexion.commit()
    return render_template("/editarProducto.html",producto=_producto)

#guarda los cambios de la edicion de productos
@app.route('/graba_editar_Producto', methods=['POST'])
def graba_editar_Producto():
    producto=request.form["producto"]
    proveedor=request.form["proveedor"]
    costo=request.form["costo"]
    precio_venta=request.form["preciovta"]
    precio_sugerido=request.form["pvpsug"]
    utilidad=request.form["utilidad"]
    porc_utilidad=request.form["porcutilidad"]
    imagen=request.files["imagen"]
    id=request.form['id']
    
        
    sql="UPDATE productos SET producto=%s, costo=%s, precio_venta=%s, precio_sugerido=%s, utilidad=%s, porc_utilidad=%s, proveedor=%s WHERE id_producto=%s"
            
    datos=(producto,costo,precio_venta,precio_sugerido,utilidad,porc_utilidad,proveedor,id)
    conexion=db_connection()
    cursor = conexion.cursor()
    
    now = datetime.now()
    tiempo=now.strftime("%Y%H%M%S")
    
    if imagen.filename !="":
        foto = tiempo+imagen.filename
        imagen.save("uploads/"+foto)
        #buscamos la foto vieja para remover
        cursor.execute("SELECT imagen FROM productos WHERE id_producto=%s",id)
        fila=cursor.fetchall()
      #  print("la dire de la foro vieja"+ fila[0][0])
        os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))
        cursor.execute("UPDATE productos SET imagen=%s WHERE id_producto=%s",(foto,id))
        conexion.commit()
    
    cursor.execute(sql,datos)
    conexion.commit()  
 #   print("Se Guardo el registro de producto!!!!")
    return redirect("/consultaProductos")


# ruta para dar de alta productos
@app.route('/altaproducto')
def altaproducto():
    return render_template('altaproducto.html')

# ruta que guarda el producto nuevo
@app.route('/guardaproducto', methods=["post"])
def guardaproducto():
        if request.method == 'POST':
            producto=request.form["producto"]
            proveedor=request.form["proveedor"]
            costo=request.form["costo"]
            precio_venta=request.form["preciovta"]
            precio_sugerido=request.form["pvpsug"]
            utilidad=request.form["utilidad"]
            porc_utilidad=request.form["porcutilidad"]
            
            imagen=request.files["imagen"]
    
            now = datetime.now()
            tiempo=now.strftime("%Y%H%M%S")
            if imagen.filename !="":
                foto = tiempo+imagen.filename
                imagen.save("uploads/"+foto)
                
            sql="INSERT INTO productos (producto,costo,precio_venta,precio_sugerido,utilidad,porc_utilidad,proveedor,imagen) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)" #%(producto,costo,precio_venta,precio_sugerido,utilidad,porc_utilidad,proveedor,imagen)
            
            datos=(producto,costo,precio_venta,precio_sugerido,utilidad,porc_utilidad,proveedor,foto)
    
            conexion=db_connection()
            cursor = conexion.cursor()
            cursor.execute(sql,datos)
            conexion.commit()
    
          #  print("Se Guardo el registro de producto!!!!")
            flash("Has creado un nuevo producto !!!")
            return redirect('/altaproducto')
        else:
            return render_template("altaproducto.html")
        
        
# Ruta de Salidas de Productos
@app.route('/salidas',methods=['get','post'])
def salidas():
    
    return render_template("salidas.html")


#guarda el formulario salidas
@app.route('/graba_salidas',methods=['get','post'])
def graba_salidas():        
    fecha=date.today()
    proveedor=None
    cliente=None
    producto=None
    cantidad=None
    precio_costo=None
    factura_costo=None
    precio_venta=None
    factura_venta=None
    utilidad_unidad=None
    utilidad_total=None
    cantidad_vendida=None
    stock=None
    saldo=None
    liquidado=None 
    pago=None
    usuario=None
    _form=SalidasForm()
    
    
    
    if _form.validate_on_submit():
        fecha=_form.fecha.data 
        index = int(_form.proveedor.data)-1
        proveedor=_form.proveedor.choices[index][1]
        index = int(_form.cliente.data)-1
        cliente=_form.cliente.choices[index][1]
        index = int(_form.producto.data)-1
        producto=_form.producto.choices[index][1]
        cantidad=_form.cantidad.data
        precio_costo=_form.precio_costo.data
        precio_venta=_form.precio_venta.data
        
        #cant vendida ya esta
        cantidad_vendida=0
        pago=0
        #stock ya esta
        stock=_form.cantidad.data
        
        #liquidado ya esta
        liquidado="NO"
        username=request.cookies.get("username","none")
    
        fact_costo=cantidad * precio_costo
     #   print(f"La factura del costo es : {fact_costo}")
        
        fact_vta=cantidad * precio_venta
      #  print(f"La factura del costo es : {fact_vta}")
        
        utilidadXu=precio_venta-precio_costo
        utilidadXT=cantidad*utilidadXu
        
        factura_costo=fact_costo
        factura_venta=fact_vta
        utilidad_unidad=utilidadXu
        utilidad_total=utilidadXT
        #saldo ya esta
        saldo=fact_vta
        
        # ya estan todos los campos con su valor asigando 
        # ahora vamos a grabarlos en la base de datos
        sql="INSERT INTO salidas (fecha_salida,proveedor,cliente,producto,cantidad,precio_costo,factura_costo,precio_vta,factura_vta,utilidad_unidad,utilidad_total,cantidad_vendida,stock,saldo,liquidado,pago,usuario) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            
        datos=(fecha,proveedor,cliente,producto,cantidad,precio_costo,factura_costo,precio_venta,factura_venta,utilidad_unidad,utilidad_total,cantidad_vendida,stock,saldo,liquidado,pago,username)
    
        conexion=db_connection()
        cursor = conexion.cursor()
        cursor.execute(sql,datos)
        conexion.commit()
    
    #    print("Se Guardo el registro de producto!!!!")
        flash("Has creado un nuevo producto !!!")
        return redirect('/graba_salidas') 
    else:
                
        #limpio campos
        fecha=date.today()
        proveedor=None
        cliente=None
        producto=None
        cantidad=None
        precio_costo=None
        factura_costo=None
        precio_venta=None
        factura_venta=None
        utilidad_unidad=None
        utilidad_total=None
        cantidad_vendida=None
        stock=None
        saldo=None
        liquidado=None 
        pago=None
        usuario=None
        _form=SalidasForm()
        return render_template('salidas.html',form =_form, fecha=fecha,proveedor=proveedor,producto=producto,cliente=cliente,cantidad=cantidad,precio_costo=precio_costo,precio_venta=precio_venta,factura_costo=factura_costo,factura_venta=factura_venta,utilidad_unidad=utilidad_unidad,utilidad_total=utilidad_total,cantidad_vendida=cantidad_vendida,stock=stock,saldo=saldo,liquidado=liquidado)    

@app.route('/buscaProducto',methods=['get','post'])
def busca_producto():
   # print("Buscando producto!!!!!")
    fecha=request.form["fecha"]
    proveedor=request.form["proveedor"]
    cliente=request.form["cliente"]
    producto=request.form["producto"]
    cantidad=request.form["cantidad"]
    sql="SELECT precio_costo,precio_venta FROM productos WHERE producto ==%S",producto
    conexion=db_connection()
    cursor = conexion.cursor()
    cursor.execute(sql)
    conexion.commit()
    _producto=cursor.fetchone()
    precio_costo=_producto[0]
    factura_costo=None
    precio_venta=_producto[1]
    factura_venta=None
    utilidad_unidad=None
    utilidad_total=None
    cantidad_vendida=None
    stock=None
    saldo=None
    liquidado=None 
    _form=SalidasForm()
  #  print("mando a la pagina la info del producto!!!")
    return redirect('/graba_salidas',form=_form,fecha=fecha,proveedor=proveedor,cliente=cliente,producto=producto,cantidad=cantidad,precio_costo=precio_costo,factura_costo=factura_costo,precio_venta=precio_venta,factura_venta=factura_venta,utilidad_unidad=utilidad_unidad,utilidad_total=utilidad_total,cantidad_vendida=cantidad_vendida,stock=stock,saldo=saldo,liquidado=liquidado)


# Rutas de Error Handlers
@app.errorhandler(404)
def page_not_found(error):
 return render_template("home.html"), 404

@app.errorhandler(500)
def page_not_found(error):
 return render_template("home.html"), 500



#############################################################################
########      Consultas edicion y borrado de Salidas
#############################################################################

#ruta de consulta de la base de datos
@app.route('/consultaSalidas', methods=['GET', 'POST'])
def consultaSalidas():
    sql="SELECT * FROM salidas"
    conexion=db_connection()
    cursor = conexion.cursor()
    cursor.execute(sql)
    _productos=cursor.fetchall()
  #  print(_productos)
    conexion.commit()
    return render_template("consulta_salidas.html",productos=_productos)

#buscar salidas
@app.route('/buscar_salidas',methods=['post'])
def buscar_salidas():
    #proveedor es el nombre del campo de busqueda OJO!!!!!! en el request form
    proveedor=request.form["proveedor"]
 #   print(f"El proveedor es {proveedor}")
    conexion=db_connection()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM salidas where proveedor like '%"+proveedor+"%' or producto like '%"+proveedor+"%' or fecha_salida ='"+proveedor+"' or liquidado ='"+proveedor+"' or cliente ='"+proveedor+"' or id ='"+proveedor+"'")
    _productos=cursor.fetchall()
  #  print(_productos)
    conexion.commit()
    return render_template("consulta_salidas.html",productos=_productos)

#ruta de eliminacion de salidas    
@app.route('/eliminar_salidas/<int:id>')
def eliminar_salidas(id):
    conexion=db_connection()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM salidas WHERE id=%s",(id))
    conexion.commit()
    conexion.close()
    return redirect("/consultaSalidas")

#ruta de edicion de salidas
@app.route('/editar_salidas/<int:id>')
def editar_salidas(id):
    conexion=db_connection()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM salidas where id=%s",(id))
    _producto=cursor.fetchall()
  #  print(_producto)
    conexion.commit()
    return render_template("/editar_salidas.html",producto=_producto)

#guarda los cambios de la edicion de salidas
@app.route('/graba_editar_salidas', methods=['POST'])
def graba_editar_salidas():
    id=request.form["id"]
    fecha_salida=request.form["fecha_salida"]
    proveedor=request.form["proveedor"]
    cliente=request.form["cliente"]
    producto=request.form["producto"]
    cantidad=request.form["cantidad"]
    precio_costo=request.form["precio_costo"]
    precio_venta=request.form["precio_venta"]
    facturacion_costo=request.form["facturacion_costo"]
    facturacion_venta=request.form["facturacion_venta"]
    utilidad_unidad=request.form["utilidad_unidad"]
    utilidad_total=request.form["utilidad_total"]
    venta=request.form["venta"]
    stock=request.form["stock"]
    saldo=request.form["saldo"]
    liquidado=request.form["liquidado"]
    username=request.cookies.get("username","none")
    
    sql="UPDATE salidas SET fecha_salida=%s,proveedor=%s,cliente=%s,producto=%s,cantidad=%s, precio_costo=%s, precio_vta=%s, factura_costo=%s, factura_vta=%s, utilidad_unidad=%s, utilidad_total=%s,cantidad_vendida=%s,stock=%s,saldo=%s,liquidado=%s,usuario=%s WHERE id=%s"
  #  print("el id es {} y el precio venta es {}".format(id,precio_venta))            
    datos=(fecha_salida,proveedor,cliente,producto,cantidad, precio_costo, precio_venta, facturacion_costo, facturacion_venta, utilidad_unidad, utilidad_total,venta,stock,saldo,liquidado,username,id)
    conexion=db_connection()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()  
   # print("Se Guardo el registro de salidas!!!!")
    return redirect("/consultaSalidas")

#ruta de pagar salidas
@app.route('/pagar_salidas/<int:id>')
def pagar_salidas(id):
    conexion=db_connection()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM salidas where id=%s",(id))
    _salidas=cursor.fetchall()
    #print(_salidas)
    conexion.commit()
    return render_template("pagar_salidas.html",producto=_salidas)

#guarda los cambios de la edicion de salidas
@app.route('/graba_pagar_salidas', methods=['POST'])
def graba_pagar_salidas():
    id=request.form["id"]
    saldo=int(float(request.form["saldo"]))
    factura_venta=int(float(request.form["factura_venta"]))
    pago= int(float(request.form["pago"]))
   # print("El id es {} y el saldo {} y el pago {}".format(id,saldo,pago))    
    nuevoSaldo=factura_venta-pago
   # print("nuevo saldo{}".format(nuevoSaldo))
    username=request.cookies.get("username","none")
    
    
    if nuevoSaldo <=0:
        nuevoLiquidado="SI"
    else:
        nuevoLiquidado="NO"
    
    sql="UPDATE salidas SET pago=%s,saldo=%s,liquidado=%s, usuario=%s WHERE id=%s"
    datos=(pago,nuevoSaldo,nuevoLiquidado, username, id)
    conexion=db_connection()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()  
    
   # print("Se Guardo el pago de la salida!!!!")
    return redirect("/consultaSalidas")


@app.route('/pago_salidas')
def pago_salidas():
    return render_template('/pagos.html')
#ruta de Pagos Cta. Cte.
@app.route('/cta_pagar_salidas', methods=['POST'])
def cta_pagar_salidas():
   # print("aca llega - entro en la funcion")
   # print("aca llega - entro en la funcion entro al post")
    #### Vamos a Grababr a la tabla de Pagos en si
    fecha_pago= request.form["fecha_pago"]
    obs= request.form["obs"]
    username=request.cookies.get("username","none")
    pago= int(float(request.form["pago"]))
    if pago>0:    
        sql="INSERT INTO pagos (fecha, importe, destino, usuario) VALUES(%s, %s, %s, %s)"
        datos=(fecha_pago, pago, obs, username)
        conexion=db_connection()
        cursor = conexion.cursor()
        cursor.execute(sql,datos)
        conexion.commit()
    #    print("Se guardo en la tabla de pagos el pago!!!!")
    else:
     #   print("no se grabo pago porque no hubo pago!")
        return render_template("/consulta_pagos.html")
    return redirect("/pagos.html")

#ruta de ventas salidas
@app.route('/ventas_salidas/<int:id>')
def ventas_salidas(id):
    conexion=db_connection()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM salidas where id=%s",(id))
    _salidas=cursor.fetchall()
  #  print(_salidas)
    conexion.commit()
    return render_template("ventas_salidas.html",producto=_salidas)


#guarda los cambios de la venta de las salidas
@app.route('/graba_ventas_salidas/', methods=['POST'])
def graba_ventas_salidas():
    id=request.form["id"]
    stock=int(request.form["stock"])
    venta=int(request.form["venta"])
    cantidad= int(request.form["carga"])
   # print("******************** {}".format(USUARIO))
    nuevoStock = cantidad - venta
    username=request.cookies.get("username","none")
        
    sql="UPDATE salidas SET cantidad_vendida=%s,stock=%s,usuario=%s WHERE id=%s"
    datos=(venta,nuevoStock,username,id)
    
    conexion=db_connection()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()  

 #   print("Se Guardo la venta !!!!")
    return redirect("/consultaSalidas")


#Consulta de Pagos
@app.route('/consulta_pagos',methods=["get","post"])
def consulta_pagos():
 #   print("fdfdfdfdfdfdfdfdfdfdfdfdfdfdfdfdfdfdfd")
    proveedor=request.form["proveedor"]
 #   print(proveedor)
    if proveedor=="":    
        sql="SELECT * FROM pagos"
    else:
        sql="SELECT * FROM pagos WHERE id='"+proveedor+"' or fecha='"+proveedor+"' or importe like '%"+proveedor+"%' or destino like '%"+proveedor+"%' or usuario like'%"+proveedor+"%'"
    conexion=db_connection()
    cursor = conexion.cursor()
    cursor.execute(sql)
    _productos=cursor.fetchall()
 #   print(_productos)
    conexion.commit()
    return render_template("/consulta_pagos.html",productos=_productos)


#ruta de eliminacion de salidas    
@app.route('/eliminar_pago/<int:id>')
def eliminar_pago(id):
    conexion=db_connection()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM pagos WHERE id=%s",(id))
    conexion.commit()
    conexion.close()
    return redirect("/consulta_pagos.html")


#guarda los cambios de la edicion de pagos
@app.route('/grabar_editar_pago', methods=['POST'])
def grabar_editar_pago():
    id=request.form["id"]
    fecha_pago=request.form["fecha_pago"]
    pago=request.form["pago"]
    obs=request.form["obs"]
    username=request.cookies.get("username","none")
    
    sql="UPDATE pagos SET fecha=%s, importe=%s, destino=%s, usuario=%s WHERE id=%s"
    datos=(fecha_pago, pago, obs, username, id)
    conexion=db_connection()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()  
#    print("Se Guardo la edicion del Pago !!!!")
    return redirect("/consulta_pagos.html")
    
#ruta de ventas salidas
@app.route('/editar_pago/<int:id>')
def editar_pago(id):
#    print("edito el pagooooooooo")
    conexion=db_connection()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM pagos where id=%s",(id))
    _salidas=cursor.fetchall()
#    print(_salidas)
    conexion.commit()
    return render_template("/editar_pago.html",producto=_salidas)
    
