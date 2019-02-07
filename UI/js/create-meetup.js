import { logout,append_logout,notify } from './helper.js';

import base from './base.js';

let url = '/auth/meetups';
var notification = document.getElementById('notification');

window.onload = function () {
    append_logout()
    var logout_link = document.querySelector('.logout');
    if(logout_link){
        logout_link.addEventListener('click', logout)
    }
    var form = document.getElementById("meetup-form")
    form.addEventListener('submit',createMeetup)

}

function createMeetup(e){
    e.preventDefault();
    const data = {
        topic:document.getElementById('title').value,
        happening_on:document.getElementById('date').value,
        location:document.getElementById('venue').value,
        body:document.getElementById('body').value,
    };
    
    var submit = document.getElementById("submit")
    submit.innerHTML = "Saving...";
    submit.setAttribute("disabled", "disabled");
    console.log(data);
    let token = localStorage.getItem("token");
    if(token){
        base
        .post(url,data,token)
        .then(function(response){return response.json()})
        .then(function(response){
            console.log(response)
            if(response.msg === "Token has expired"){
                alert("session expired!!")
                window.location.href = '../UI/login.html'
            }else if (response.status === 201){
                alert(response.message)
                sessionStorage.setItem('success',"meetup successfully created!!")
                window.location.href = '../UI/admin.html'
            
            }else{
                
                notify(response.error,status="error")
                submit.innerHTML = "Save";
                submit.removeAttribute("disabled", "disabled");
            }
    
        })
    }
   
}