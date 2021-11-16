// VALIDACION DE FORM registrate - registrate.html //

const formulario = document.getElementById("registrate");
const pass = document.getElementById("pass");
const email = document.getElementById("email");
const nombre = document.getElementById("nombre");
const boton_reg = document.getElementById("btn-reg")


formulario.addEventListener('submit',function(e){
    if(pass.value==""){
        e.preventDefault();
        console.log("Campo password esta vacio!")
        pass.style.borderColor="orange";
        pass.focus();
        }
        else{
            pass.style.borderColor="#3742fa";
        }
    if(email.value == ""){
        e.preventDefault();
        console.log("Campo email esta vacio!")
        email.style.borderColor="orange";
        email.focus();
        }
        else{
            email.style.borderColor="#3742fa";
        }
    if(nombre.value == ""){
        e.preventDefault();
        console.log("Campo nombre esta vacio!")
        nombre.style.borderColor="orange";
        nombre.focus();
        }
        else{
            nombre.style.borderColor="#3742fa";
        }
//    if (nombre.value != "" && email.value!="" && usu.value!="" && pass.value!=""){
//        e.stopPropagation();
//    }
});

function LimpiarCampos(){
    nombre.value=""
    email.value=""
    pass.value=""
}
