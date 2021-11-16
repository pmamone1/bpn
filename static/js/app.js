//console.log("js funciona ok!")

//       ***   FUNCIONES GENERALES  ***
function Minusculas(e) {
    e.value = e.value.toLowerCase();
}
function SinFoco(texto){    
    if(texto.value != "")
    texto.style.borderColor="#3742fa";
}


// Para obtenerlo
// const currentUser = JSON.parse(window.localStorage.getItem('current_user'));
function ponerUsuario(){
    const currentUser = JSON.parse(window.localStorage.getItem('current_user'));
    _usu=document.getElementById("lblusu").innerHTML=currentUser["name"];
    console.log(currentUser["name"])
    
}

function ExportToExcelSalidas(type, fn, dl) {
    
    var elt = document.getElementById('tablaProductosSalidas');
    var wb = XLSX.utils.table_to_book(elt, { sheet: "sheet1" });
    return dl ?
      XLSX.write(wb, { bookType: type, bookSST: true, type: 'base64' }):
      XLSX.writeFile(wb, fn || ('bpn_salidas_.' + (type || 'xlsx')));
 }
 
_excel=document.querySelector("#excel");

_excel.addEventListener('click', (event) => {
    ExportToExcelPagos("xlsx");
})


function ExportToExcelPagos(type, fn, dl) {
  
    console.log("estoy aca!")
    var elt = document.getElementById('tablaProducto');
    var wb = XLSX.utils.table_to_book(elt, { sheet: "sheet1" });
    return dl ?
      XLSX.write(wb, { bookType: type, bookSST: true, type: 'base64' }):
      XLSX.writeFile(wb, fn || ('bpn_pagos_.' + (type || 'xlsx')));
 }

function load(){
    //   form2.style.color="white";
       //Para obtenerlo
       ponerUsuario()
    
    };

function obtenerUsu(){
    //Accedemos a los valores
   
    console.log(usu)
}

const pago = document.querySelector("#pago")
if (pago.value==""){
    pago.value="0";
}
function control(){
const pago = document.querySelector("#pago")
if(pago.value==""){
    pago.value="0";
    console.log("puso pago en 0")
}
}
/*
const mysql = require("mysql")

const conexion = mysql.createConnection({
    host:'localhost',
    user:'root',
    password:'pablo1612',
    database:'bpn'
})

conexion.connect((err)=>{
    if (err) throw err
    console.log("la conexion funciona!!!!")
})

conexion.query("select * from salidas",(err,rows)=>{
    if (err) throw err
    console.log("los datos de la tabla salida son")
    console.log(rows)
})
conexion.end()

$(document).ready(function(){
    $('#tablaProductosSalidas').dataTable();
})
*/