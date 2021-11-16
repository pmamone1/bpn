campo = document.querySelector('.numero');
form=document.getElementById("formulario_alta_producto")
form2=document.getElementById('imagen');
inputs = document.getElementsByClassName("texto")
formulario= document.getElementById("formulario_alta_producto")
_usu=document.querySelector("#lblusu")

window.setTimeout("document.getElementById('mensaje').style.display='none';", 2000);

function Volver(e){
	e = e || window.event;
	e.preventDefault();
    location.href ="/home.html";
}

const selectElement = document.querySelectorAll('.cuenta');

    for (i = 0; i < selectElement.length; i++) {
        selectElement[i].addEventListener('blur', (event) => {
            const result1 = document.querySelector('#utilidad');
            const result2 = document.querySelector('#porcutilidad');
            porcutilidad
            _utilidad= parseFloat(utilidad())
            _porc_utilidad=parseFloat(porc_utilidad())
            console.log("La utilidad es "+_utilidad)
            console.log("el % de utilidad es "+_porc_utilidad)
            console.log(result1)
            result1.value = _utilidad.toFixed(2);
            result2.value = _porc_utilidad.toFixed(2);
        })
    };    

    var inputs = document.querySelectorAll("input");
    for (var i = 0 ; i < inputs.length; i++) {
       inputs[i].addEventListener("keypress", function(e){
          if (e.which == 13) {
             e.preventDefault();
             var nextInput = document.querySelectorAll('[tabIndex="' + (this.tabIndex + 1) + '"]');
             if (nextInput.length === 0) {
                nextInput = document.querySelectorAll('[tabIndex="1"]');
             }
             nextInput[0].focus();
          } 
        }
       )};
    
function utilidad(){
    num1=parseFloat(selectElement[0].value);
    num2=parseFloat(selectElement[1].value);
    return num2-num1
}
function porc_utilidad(){
    resultado = ((parseFloat(selectElement[1].value)/parseFloat(selectElement[0].value))-1)*100
    return resultado
}


function limpiarcampos(){
    for (input in inputs)
    {
        input.value = "";
    }
};


