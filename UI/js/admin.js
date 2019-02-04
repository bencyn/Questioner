import { logout } from './helper.js';

window.onload = function () {
    // append_logout()
    var logout_link = document.querySelector('.logout');
    logout_link.addEventListener('click', logout)
    
}



