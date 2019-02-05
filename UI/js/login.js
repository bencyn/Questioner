import { parseJwt} from './helper.js';
import base from './base.js';

let login_url = '/auth/login';
var notification = document.getElementById('notification');

window.onload = function () {
    var form = document.getElementById("login-form")
    form.addEventListener('submit', loginUser)
    let message = sessionStorage.getItem('success');

    if(message){
        notification.style.display='block';
        notification.setAttribute('class','alert alert-success');
        notification.innerHTML = `${message}`;
        sessionStorage.clear();
    }
}

function loginUser(e){
    e.preventDefault()

    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;

    const data = {
        username:username,
        password:password,
        };
    var submit = document.getElementById("submit")
    submit.innerHTML = "Signing in...";
    submit.setAttribute("disabled", "disabled");
    console.log(data);
    base
    .post(login_url,data)
    .then(function(response){return response.json()})
	.then(function(response){
        console.log(response)
		
		if (response.status === 201){
            let token =response.data[0]["token"]
            let decode=parseJwt(token)
            let is_admin=decode.identity.is_admin

            localStorage.setItem('token',token)
		    localStorage.setItem('is_logged_in','true')
            localStorage.setItem('username',decode.identity.username)
            localStorage.setItem('is_admin',is_admin)
            
            alert(response.message)
            
            if(is_admin === "1"){
                window.location.href = '../UI/admin.html'
            }else{
                window.location.href = '../UI/index.html'
            }
			
		}
		else{
            notification.style.display='block';
            notification.innerHTML = `${response.error}`;
            submit.innerHTML = "Sign In";
            submit.removeAttribute("disabled", "disabled");
            
		}

    })
}