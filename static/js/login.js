// VALIDACION DE FORM LOGIN - INDEX.HTML //

const formulario = document.getElementById("formulario");
const email = document.getElementById("email");
const passw = document.getElementById("passw");
var texto =  document.querySelectorAll('input[type=email], input[type=password]');
const btn_login = document.getElementById("btn-login")


function login(){
   console.log(email.value);
   console.log(passw.value);
   const user = { id: 1, name: email.value };
   window.localStorage.setItem('current_user', JSON.stringify(user));
   console.log("se esta grabando el usuario!!!!" + user)
}

formulario.addEventListener('submit',function(e){
    
    if(passw.value == ""){
        e.preventDefault();
        console.log("Campo password esta vacio!")
        passw.style.borderColor="orange";
        passw.focus();
        }
    else{
        passw.style.borderColor="#3742fa";
        }
    if (email.value == ""){
        e.preventDefault();
        console.log("Campo usuario esta vacio!")
        email.style.borderColor="orange";
        email.focus();
        }
    else{
        email.style.borderColor="#3742fa";
    }
    if (passw.value !="" && email.value !="") {
        e.stopPropagation();
    }
});

$(document).ready(function(){
    $(".alert_message").delay(5000).slideUp(300);
});
