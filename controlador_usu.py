#from pymysql.cursors import Cursor
from bd import db_connection
import os
from flask import Flask, render_template,redirect, flash,request,session
from sqlalchemy.sql import exists



def insertar_usu(nombre,email,password):
    conexion = db_connection()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO usuarios(nombre,email,password) VALUES (%s,%s,%s)",(nombre,email,password))
        conexion.commit()
        conexion.close()
     
        
def buscaUsuario(email):
    conexion=db_connection()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM usuarios WHERE email= %s",(email))
        conexion.commit()
        usuario = cursor.fetchone()
        conexion.close()
        existe = usuario.query.filter_by(email=email).first()
      #  if existe:
       #     print("encontro el usuario") 
      #  else:
        #    print("no existe")

