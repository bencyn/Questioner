import { parseJwt,notify} from './helper.js';
import base from './base.js';

let upcoming_url = '/meetups/upcoming/';
var notification = document.getElementById('notification');
var loader =  document.querySelector('.loader');
var is_admin =localStorage.getItem("is_admin");
var username =localStorage.getItem("username");
window.onload = function () {
    loader.style.display='block';
    upcomingMeetups()

    let message = sessionStorage.getItem('success');

    if(message){
        notify(message,status="success")
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
                console.log(meetup.id)
                if((count % 2) ==0){
                    image="https://s3.envato.com/files/188307997/1.jpg"
                }else{
                    image="https://cdn.dribbble.com/users/1807056/screenshots/4666838/dribbble_404.png"
                }
                if(is_admin === "1" && username==="admin"){
                    result +=  
                    `<div class="meetup-item">
                        <a class="meetup-link" id=${meetup.id} data-image=${image} href="#">
                            <div class="m-img">
                                <img src="${image}">
                            </div>
                            <div class="m-detail">
                                <div class="m-time">${meetup.happening_on}</div>
                                <div class="m-content">
                                    <h4>${meetup.topic}</h4>
                                </div>
                                <div class="m-location"><strong>Venue:</strong>${meetup.location}</div>
                            </div>
                        </a>
                        <div class="m-admin">
                            <a href="" data-id="${meetup.id}" class="m-admin-btn delete">Delete</a>
                        </div>
                    </div>`;
                }else{
                    result +=  
                    `<div class="meetup-item">
                        <a class="meetup-link" id=${meetup.id} href="#" data-image=${image}>
                            <div class="m-img">
                                <img src="${image}">
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

            loader.style.display='none';
            for(var count=0; count < data.meetup.length; count++){
                let meetup = data.meetup[count]
                document.getElementById(meetup.id).addEventListener('click', viewMeetup);
                if(is_admin === "1" && username==="admin"){
                    document.querySelector('[data-id="'+meetup.id+'"]').addEventListener('click', deleteMeetup)
                }
            }
        }else{
            let el =document.querySelector('#meetups');
            el.innerHTML=`<div id="notification" class="alert alert-danger" role="alert">${data.error}</div>`;
        }
    })
}
function deleteMeetup(e){
    e.preventDefault();

    let id =e.target.attributes.getNamedItem("data-id").value;
    let url = '/meetups/'+id
    let token = localStorage.getItem("token");
    var result = confirm("Are sure you want to delete this record?");
	if (result) {
        if(token){
            base
            .delete(url,token)
            .then(function(response){return response.json()})
            .then(function(response){
                // console.log(response)
                if(response.msg === "Token has expired"){
                    alert("session expired!!")
                    window.location.href = '../UI/login.html'
                }else if (response.status === 200){
                    notify(response.message,status="success")
                    upcomingMeetups()
                }else{
                    alert(response.error)
                    notify(response.error,status="error");
                    // hideNotification();
                }
            })
        }else{
            alert("You have to be logged in user in order to post a question")
        }
	}
   
}
function viewMeetup(e){
    e.preventDefault();
    // a.attributes.getNamedItem
    let image =this.attributes.getNamedItem("data-image").value;
    localStorage.setItem('meetup-id',this.id);
    localStorage.setItem('image',image);
    window.location.href = '../UI/view-meetup.html'
}

