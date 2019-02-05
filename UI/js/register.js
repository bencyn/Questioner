import { parseJwt} from './helper.js';
import base from './base.js';

let register_url = '/auth/signup';
var notification = document.getElementById('notification');

window.onload = function () {
    var form = document.getElementById("register-form")
    form.addEventListener('submit', registerUser)
}

function registerUser(e){
    e.preventDefault()

    const data = {
        firstname:document.getElementById('firstname').value,
        lastname:document.getElementById('lastname').value,
        othername:document.getElementById('othername').value,
        phone_number:document.getElementById('phone_number').value,
        username:document.getElementById('username').value,
        email:document.getElementById('email').value,
        password:document.getElementById('password').value,
        confirm_password:document.getElementById('confirm_password').value,
    };
    
    var submit = document.getElementById("submit")
    submit.innerHTML = "Registering...";
    submit.setAttribute("disabled", "disabled");
    console.log(data);
    base
    .post(register_url,data)
    .then(function(response){return response.json()})
	.then(function(response){
        console.log(response)
		
		if (response.status === 201){
            alert(response.message)
            sessionStorage.setItem('success',"!! you have successfully created an account, login to continue !!")
            window.location.href = '../UI/login.html'
        
		}
		else{
            // alert(response.error)
            notification.style.display='block';
            notification.innerHTML = `${response.error}`;
            submit.innerHTML = "Register";
            submit.removeAttribute("disabled", "disabled");
		}

    })
}