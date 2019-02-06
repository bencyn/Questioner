import { logout, append_logout } from './helper.js';

window.onload = function () {
    append_logout
    var logout_link = document.querySelector('.logout');
    if(logout_link){
        logout_link.addEventListener('click', logout)
    }

}





