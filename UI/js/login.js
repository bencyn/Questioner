import { serialize, base_url,parseJwt} from './helper.js';

let login_url = base_url + '/auth/login';
var notification = document.getElementById('notification');

window.onload = function () {
 
    // notification.style.display = 'none';

   // get the button to submit the query 
    var form = document.getElementById("login-form")
    //  add eventListener on the button
    form.addEventListener('submit', loginUser)
    
}

function loginUser(e){
    e.preventDefault()

    var form = document.querySelector('#login-form');
    var formData = serialize(form);
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

    fetch(login_url, {
        method: 'POST',
        headers: {
            "Content-type":"application/json",
        },
        body: JSON.stringify(data)
    })
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
            notification.innerHTML = `${response.msg}`;
            submit.innerHTML = "Sign In";
            submit.removeAttribute("disabled", "disabled");
		// 	setTimeout(()=> {
		// 		const message = "";
		// 		notification.innerHTML = message;
		// 	}, 3000)
		}

    })
}