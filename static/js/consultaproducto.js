
const selectElement = document.querySelectorAll('.cuenta');
print(str(selectElement[0].value))
for (i = 0; i < selectElement.length; i++) {
    selectElement[i].addEventListener('blur', (event) => {
        const result1 = document.querySelector('#utilidad');
        const result2 = document.querySelector('#porcutilidad');
        print("el objeto es " + str(selectElement[i].value))
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

  
function utilidad(){
    num1=parseFloat(selectElement[0].value);
    num2=parseFloat(selectElement[1].value);
    return num2-num1
}
function porc_utilidad(){
    resultado = ((parseFloat(selectElement[1].value)/parseFloat(selectElement[0].value))-1)*100
    return resultado
}

 