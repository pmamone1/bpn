const alta = document.getElementById("alta");
const  p= document.getElementById("passw");
const email = document.getElementById("email")
const usu = document.getElementById("usu");


function UserValue(){
    const valores = window.location.search;
    //Mostramos los valores en consola:
    console.log(valores);
    //Creamos la instancia
    const urlParams = new URLSearchParams(valores);

    //Accedemos a los valores
    var producto = urlParams.get('email');
    //Verificar si existe el parámetro
    console.log(urlParams.has('email'));

//Puedes recorrer los valores, claves y pares completos.
const
  keys = urlParams.keys(),
  values = urlParams.values(),
  entries = urlParams.entries();

for (const value of values) console.log(value);

}

// windows.onLoad=UserValue();
