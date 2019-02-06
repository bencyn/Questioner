import { logout,append_logout } from './helper.js';

append_logout()
var logout_link = document.querySelector('.logout');
if(logout_link){
    logout_link.addEventListener('click', logout)
}




