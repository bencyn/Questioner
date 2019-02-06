import { parseJwt} from './helper.js';
import base from './base.js';

let upcoming_url = '/meetups/upcoming/';
var notification = document.getElementById('notification');

window.onload = function () {
    upcomingMeetups()
    let message = sessionStorage.getItem('success');

    if(message){
        notification.style.display='block';
        notification.setAttribute('class','alert alert-success');
        notification.innerHTML = `${message}`;
        sessionStorage.clear();
    }
}

function upcomingMeetups(){
   
    base
    .get(upcoming_url)
    .then(function(response){return response.json()})
    .then(data => {
        if(data.status === 200){
            let result = ''
            for(var count=0; count < data.meetup.length; count++){
                let meetup = data.meetup[count]
                var image
                let is_admin =localStorage.getItem("is_admin");
                if(is_admin ===1){
                    result +=  
                    `<div class="meetup-item" id=${meetup.id}>
                        <a class="meetup-link" href="#">
                            <div class="m-img">
                                <img src="${meetup.images}">
                            </div>
                            <div class="m-detail">
                                <div class="m-time">${meetup.happening_on}</div>
                                <div class="m-content">
                                    <h4>${meetup.topic}</h4>
                                </div>
                                <div class="m-location"><strong>Venue:</strong>${meetup.location}</div>
                                <div class="m-admin">
                                    <a href="" class="m-admin-btn delete">Delete</a>
                                </div>
                            </div>
                        </a>
                    </div>`;
                }else{
                    result +=  
                    `<div class="meetup-item" id=${meetup.id}>
                        <a class="meetup-link" href="#">
                            <div class="m-img">
                                <img src="${meetup.images}">
                            </div>
                            <div class="m-detail">
                                <div class="m-time">${meetup.happening_on}</div>
                                <div class="m-content">
                                    <h4>${meetup.topic}</h4>
                                </div>
                                <div class="m-location"><strong>Venue:</strong>${meetup.location}</div>
                            </div>
                        </a>
                    </div>`;
                }
                
            }
            document.getElementById('meetups').innerHTML=result
            for(var count=0; count < data.meetup.length; count++){
                let meetup = data.meetup[count]
                document.getElementById(meetup.id).addEventListener('click', viewMeetup);
            }
        }else{
            let el =document.querySelector('#meetups');
            el.innerHTML=`<div id="notification" class="alert alert-danger" role="alert">${data.error}</div>`;
        }
    })
}

function viewMeetup(e){
    e.preventDefault();
    localStorage.setItem('meetup-id',this.id);
    window.location.href = '../UI/view-meetup.html'
}
