import { logout } from './helper.js';

window.onload = function () {
    append_logout()
    var logout_link = document.querySelector('.logout');
    if(logout_link){
        logout_link.addEventListener('click', logout)
    }
    
    
}
function append_logout(){
    // disable login link
    // let notification = document.getElementById('notification');


    // var el = document.querySelector('.navigation');
    // el.innerHTML += '<a  href="logout.html">Logout/a>';
    // var newEl = document.createElement('p');
    // newEl.setAttribute('class', 'signature');
    // newEl.setAttribute('href', 'logout.html');
    // newEl.appendChild(document.createTextNode('Logout'));
    let token = localStorage.getItem("token");
    let username =localStorage.getItem("username");
    console.log(token);
    if (token) {
        // alert("yes");
        var el = document.querySelector('.nav-link');
        el.removeAttribute('href','index.html');
        el.setAttribute('href','logout.html');
        el.setAttribute('class','logout nav-link');
        el.innerHTML= 'Logout';
      
    }
}




