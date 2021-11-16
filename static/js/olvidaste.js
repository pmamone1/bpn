const form = document.getElementById("olvidaste");
const email = document.getElementById("email");

form.addEventListener('submit',function(e){
    e.preventDefault();
    if(email.value == ""){
        console.log("Campo email esta vacio!");
        email.style.borderColor="orange";
        email.focus();
        }
        else{
            email.style.borderColor="#3742fa";
        }
    });
