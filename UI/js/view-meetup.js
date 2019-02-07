import { append_logout,logout} from './helper.js';
import base from './base.js';

var url = '/meetups/';
var view_url
// var notification = document.getElementById('notification');
var question_url
var topic;
window.onload = function () {
    append_logout()
    var logout_link = document.querySelector('.logout');
    if(logout_link){
        logout_link.addEventListener('click', logout)
    }
    let id = localStorage.getItem("meetup-id");
    if(id){
        view_url=url+id;
        question_url=view_url+'/questions'
        viewMeetup(view_url);
    } 
    var form = document.getElementById("question-form")
    form.addEventListener('submit', postQuestion)
}

function viewMeetup(url){
   
    base
    .get(url)
    .then(function(response){return response.json()})
    .then(data => {
        // console.log(data)
        if(data.status ===200){
            let meetup = data.meetup[0]
            let questions =data.questions
            // console.log(data.questions)
            // document.getElementsByClassName('meetup-title')
            topic=meetup.topic
          document.querySelector('.meetup-title').innerHTML=meetup.topic;
            document.querySelector('.m-img').innerHTML=`<img src="${meetup.images}"/>`;
            document.querySelector('.m-time').innerHTML=`${meetup.happening_on}`;
            document.querySelector('.m-content').innerHTML=`<p>${meetup.body}</p>`;
            document.querySelector('.m-location').innerHTML=`<strong>Venue:</strong> ${meetup.location}`;
            if(questions){
                document.querySelector('#questions-title').style.display="block"
                var i = 0;
                let result = ''
                // console.log(questions)
                for(var count=0; count < data.questions.length; count++){
                    let question = questions[count]
                    console.log(question)
                    // getComments(question.id)
                    result += 
                    `<div class="question">
                        <div class="meetup-item">  
                            <div class="m-detail">
                                <div class="m-time">
                                    <img src="images/user-avatar.jpg" alt="Avatar">
                                    <span class="q-name">${question.username}</span>
                                    <span class="q-time"></span>
                                </div>
                                <div class="m-content">
                                    <p>${question.body}</p>
                                    <div class="q-reaction">
                                        <span><a href=""><i class="fa fa-thumbs-up"></i> upvote <small>(20)</small></a></span>
                                        <span><a href=""><i class="fa fa-thumbs-down"></i> downvote <small>(1)</small></a></span>
                                    </div>
                                    <br>
                                    <div id="comment-${question.questions_id}">
                                    </div>
                                    <div class="question post-question post-comment">
                                        <div class="meetup-item">  
                                            <div class="m-detail">
                                                <div class="m-content">
                                                    <form>
                                                    <textarea name="description" placeholder="Enter Comment..."></textarea>
        
                                                    <div class="form-btn">
                                                            <button class="submit" type="submit">Post Comment</button>
                                                    </div>
                                                </form>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>`
                }
                document.getElementById('questions').innerHTML=result
                
                for(var count=0; count < data.questions.length; count++){
                    let question = questions[count]
                    // console.log(question)
                    getComments(question.questions_id)
                }
                // append comments
            }
        }else{
            // alert(data.error)
            let el =document.querySelector('.meetup-details');
            el.innerHTML=`<div id="notification" class="alert alert-danger" role="alert">${data.error}</div>`;
        }

    })
}

function getComments(id){
    let url ='/questions/'+id;
    base
    .get(url)
    .then(function(response){return response.json()})
    .then(data => {
        // console.log(data)
        if(data.status ===200){
            // console.log(data.comments.length)
            let result = ''
            for(var count=0; count < data.comments.length; count++){
                let comment = data.comments[count]
                result +=
                `<div class="question comment">
                    <div class="meetup-item">  
                        <div class="m-detail">
                            <div class="m-time">
                                <img src="images/comment-1.jpg" alt="Avatar">
                                <span class="q-name">${comment.username}</span>
                                <span class="q-time"></span>
                            </div>
                            <div class="m-content">
                                <p>${comment.comment}</p>
                            </div>
                        </div>
                    </div>
                </div>`
            }
            document.getElementById('comment-'+id).innerHTML=result
        }
    })

}

function postQuestion(e){
    e.preventDefault();
    const data = {
        title:document.querySelector('.meetup-title').innerHTML,
        body:document.getElementById('body').value,
    };
    
    var submit = document.getElementById("submit")
  
    console.log(data);
    let token = localStorage.getItem("token");
    if(token){
        submit.innerHTML = "Posting Question....";
        submit.setAttribute("disabled", "disabled");
        base
        .post(question_url,data,token)
        .then(function(response){return response.json()})
        .then(function(response){
            // console.log(response)
            if(response.msg === "Token has expired"){
                alert("session expired!!")
                window.location.href = '../UI/login.html'
            }
            if (response.status === 201){
                alert(response.message)
                // sessionStorage.setItem('success',"question successfully posted!!")
                // window.location.href = '../UI/admin.html'
                viewMeetup(view_url);
                notify(response.message);
                document.getElementById("question-form").reset();
                submit.innerHTML = "Post Question";
                submit.removeAttribute("disabled", "disabled");
            }
            else{
                alert(response.error)
                notification.style.display='block';
                notification.innerHTML = `${response.error}`;
            }

    
        })
    }else{
        alert("You have to be logged in user in order to post a question")
    }
  
}

function notify(message){
    // let message = sessionStorage.getItem('success');

    if(message){
        notification.style.display='block';
        notification.setAttribute('class','alert alert-success');
        notification.innerHTML = `${message}`;
        // sessionStorage.clear();
    }
}