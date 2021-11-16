function Totales(){
    let totalCarga=0;
    let totalVenta=0;
    let totalStock=0;
    let totalFilas=0;
    
    sumaCarga=document.querySelectorAll('#carga');
    sumaVenta=document.querySelectorAll('#venta');
    sumaStock=document.querySelectorAll('#stock');
    
    for(let i=0; i<sumaCarga.length;++i){
        totalCarga +=parseFloat(sumaCarga[i].firstChild.data);
        console.log(sumaCarga[i].firstChild.data)
        totalFilas=sumaCarga.length;
        console.log("la cantidad de filas es"+totalFilas)
    }
    for(let i=0; i<sumaVenta.length;++i){
        totalVenta +=parseFloat(sumaVenta[i].firstChild.data);
        console.log(sumaVenta[i].firstChild.data)
    }
    for(let i=0; i<sumaStock.length;++i){
        totalStock +=parseFloat(sumaStock[i].firstChild.data);
        console.log(sumaStock[i].firstChild.data)
    }

    _campo_carga=document.querySelector('#cargaModal');
    _campo_venta=document.querySelector('#ventaModal');
    _campo_stock=document.querySelector('#stockModal');
    _campo_filas=document.querySelector("#filas");

    _campo_carga.innerHTML=Number((totalCarga).toFixed(0)).toLocaleString();
    _campo_venta.innerHTML=Number((totalVenta).toFixed(0)).toLocaleString();
    _campo_stock.innerHTML=Number((totalStock).toFixed(0)).toLocaleString();
    _campo_filas.innerHTML=Number((totalFilas).toFixed(0)).toLocaleString();

    let totalCosto=0;
    let totalUtilidad=0;
    let totalPago=0;
    let totalSaldo=0;
    let SaldoAlDia=0;
    let totalFacturacion=0;

    sumaCosto=document.querySelectorAll('#costo');
    sumaUtilidad=document.querySelectorAll('#util');
    sumaPago=document.querySelectorAll('#pago');
    sumaSaldo=document.querySelectorAll('#saldo');
    sumaSaldoAlDia=document.querySelectorAll('#saldoAlDiaModal');
    sumaPrecioVenta=document.querySelectorAll('#precioVenta')
    sumaFacturacion=document.querySelectorAll('#facturacion')

    for(let i=0; i<sumaFacturacion.length;++i){
        totalFacturacion +=parseFloat(sumaFacturacion[i].firstChild.data);
        console.log(sumaFacturacion[i].firstChild.data)
    }
    for(let i=0; i<sumaCosto.length;++i){
        totalCosto +=parseFloat(sumaCosto[i].firstChild.data);
        console.log(sumaCosto[i].firstChild.data)
    }
    for(let i=0; i<sumaUtilidad.length;++i){
        totalUtilidad +=parseFloat(sumaUtilidad[i].firstChild.data);
        console.log(sumaUtilidad[i].firstChild.data)
    }
    for(let i=0; i<sumaPago.length;++i){
        totalPago +=parseFloat(sumaPago[i].firstChild.data);
        console.log(sumaPago[i].firstChild.data)
    }
    for(let i=0; i<sumaSaldo.length;++i){
        totalSaldo +=parseFloat(sumaSaldo[i].firstChild.data);
        console.log(sumaSaldo[i].firstChild.data)
    }
    for(let i=0; i<sumaVenta.length;++i){
        SaldoAlDia += (parseFloat(sumaVenta[i].firstChild.data) * parseFloat(sumaPrecioVenta[i].firstChild.data) )- parseFloat(sumaPago[i].firstChild.data);
        
    }
    
    console.log("La facturacion total es "+ totalFacturacion)
    _sumaCosto=document.querySelector('#costoModal');
    _sumaFacturacion=document.querySelector("#facturacionModal")
    _sumaUtilidad=document.querySelector('#utilidadModal');
    _sumaPago=document.querySelector('#pagoModal');
    _sumaSaldo=document.querySelector('#saldoModal');
    _sumaSaldoAlDia=document.querySelector('#saldoAlDiaModal');

    _sumaCosto.innerHTML=Number(totalCosto).toFixed(2).toLocaleString()
    _sumaFacturacion.innerHTML=Number(totalFacturacion).toFixed(2).toLocaleString()
    _sumaUtilidad.innerHTML=Number(totalUtilidad).toFixed(2).toLocaleString()
    _sumaPago.innerHTML=Number(totalPago).toFixed(2).toLocaleString()
    _sumaSaldo.innerHTML=Number(totalSaldo).toFixed(2).toLocaleString()
    _sumaSaldoAlDia.innerHTML=Number(SaldoAlDia).toFixed(2).toLocaleString()
}

_Ch=document.querySelector('#checkConsulta');

_Ch.addEventListener('click', (event) => {
        tabla=document.querySelectorAll('#liquidado');
        // recorro toda la tabla y busco la columna liquidado
        console.log("entro en este evento!")
        var table = document.getElementById('tablaProductosSalidas');
        var rowCount = table.rows.length;
        for(let i=0; i<tabla.length;++i){
            if (tabla[i].firstChild.data =="SI"){
                console.log("se encontro un liquidado!!!!")
                table.deleteRow(i+1);
             };
  }})
