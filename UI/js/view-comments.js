import { append_logout,logout,notify,avatar_image} from './helper.js';
import base from './base.js';

var notification = document.getElementById('notification');
var question_notification = document.getElementsByClassName('question-notification');
console.log(question_notification)
var question_url
var post_url
var topic;
window.onload = function () {
    append_logout()
    var logout_link = document.querySelector('.logout');
    if(logout_link){
        logout_link.addEventListener('click', logout)
    }
    let id = localStorage.getItem("question-id");
    console.log(id);
    if(id){
        question_url='/questions/'+id;
        post_url=question_url+'/comments';
        viewQuestion(question_url);
    } 
  

}

function viewQuestion(url){
   
    base
    .get(url)
    .then(function(response){return response.json()})
    .then(data => {
        console.log(data)
        console.log(data.question[0])
        if(data.status ===200){
            let question =data.question[0]
            let comments =data.comments
            let result = 
                `<div class="question">
                    <div class="meetup-item">  
                        <div class="m-detail">
                            <div class="m-time">
                                <img src="${avatar_image}" alt="Avatar">
                                <span class="q-name">${question.username}</span>
                                <span class="q-time"></span>
                            </div>
                            <div class="m-content">
                                <p>${question.body}</p>
                                <div class="q-reaction">
                                    <span><a class="upvote-${question.questions_id}" id="${question.questions_id}" href="#"><i class="fa fa-thumbs-up"></i> upvote <small>(${question.upvotes})</small></a></span>
                                    <span><a class="downvote-${question.questions_id}" id="${question.questions_id}" href=""><i class="fa fa-thumbs-down"></i> downvote <small>(${question.downvotes})</small></a></span>
                                    <span><a id="view-meetup" href=""><i class="fa fa-question-circle"></i> view meetup</a></span>
                                </div>
                                <br>
                                <div id="notification" class="alert alert-danger" role="alert"></div>
                                <div id="comments"></div>
                                <div class="question post-question post-comment">
                                    <div class="meetup-item">  
                                        <div class="m-detail">
                                            <div class="m-content">
                                                <form data-id="comment-form">
                                                    <textarea name="description" data-id="comment" placeholder="Enter Comment..." required=""></textarea>
        
                                                    <div class="form-btn">
                                                        <button class="submit" data-id="submit" type="submit">Post Comment</button>
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
            document.getElementById('questions').innerHTML=result
            document.querySelector('.upvote-'+question.questions_id).addEventListener('click',upvoteQuestion);
            document.querySelector('.downvote-'+question.questions_id).addEventListener('click',downvoteQuestion);
            document.querySelector('[data-id="comment-form"]').addEventListener('submit',postComment)
            document.querySelector("#view-meetup").addEventListener('click',viewMeetup);
        
            if(comments){
                let result = ''
                for(var count=0; count < data.comments.length; count++){
                    let comment = data.comments[count]
                    console.log(comment) 
                    result +=
                    `<div class="question comment">
                        <div class="meetup-item">  
                            <div class="m-detail">
                                <div class="m-time">
                                    <img src="${avatar_image}" alt="Avatar">
                                    <span class="q-name">${comment.username}</span>
                                    <span class="q-time"></span>
                                </div>
                                <div class="m-content">
                                    <p>${comment.comment}</p>
                                </div>
                                
                            </div>
                        </div>
                    </div>`                   
                    // getComments(question.questions_id)
                }
                document.getElementById('comments').innerHTML=result
            }
        }else{
            let el =document.querySelector('.meetup-details');
            el.innerHTML=`<div id="notification" class="alert alert-danger" role="alert">${data.error}</div>`;
        }
    })
}
function viewMeetup(e){
    e.preventDefault();
    window.location.href = '../UI/view-meetup.html'
}

function upvoteQuestion(e){
    e.preventDefault();
    let url ='/questions/'+this.id+'/upvote';
    console.log(url);
    let token = localStorage.getItem("token");
    if(token){
        let data;
        base
        .patch(url,token)
        .then(function(response){return response.json()})
        .then(function(response){
            // console.log(response)
            if(response.msg === "Token has expired"){
                alert("session expired!!")
                window.location.href = '../UI/login.html'
            }else if (response.status === 201){
                // alert(response.message)
                console.log(response.data)
                viewQuestion(question_url)
            }
            else{
                alert(response.error)
                notify(response.error,status="error");
                // hideNotification();
            }
        })
    }else{
        alert("You have to be logged in user in order to post a question")
    }
}

function downvoteQuestion(e){
    e.preventDefault();
    let url ='/questions/'+this.id+'/downvote';
    console.log(url);
    let token = localStorage.getItem("token");
    if(token){
        let data;
        base
        .patch(url,token)
        .then(function(response){return response.json()})
        .then(function(response){
            // console.log(response)
            if(response.msg === "Token has expired"){
                alert("session expired!!")
                window.location.href = '../UI/login.html'
            }else if (response.status === 201){
                console.log(response.data)
                viewQuestion(question_url)
            }else{
                alert(response.error)
                notify(response.error,status="error");
            }
        })
    }else{
        alert("You have to be logged in user in order to post a question")
    }
}
function postComment(e,id){
    e.preventDefault();

    var comment_url ='/questions/'+id+'/comments';
   
    const data = {
        comment:document.querySelector('[data-id="comment"]').value
    };
    
    var submit = document.querySelector('[data-id="submit"]')
  
    console.log(data);
    let token = localStorage.getItem("token");
    if(token){
        submit.innerHTML = "Posting Comment....";
        submit.setAttribute("disabled", "disabled");
        base
        .post(post_url,data,token)
        .then(function(response){return response.json()})
        .then(function(response){
            // console.log(response)
            if(response.msg === "Token has expired"){
                alert("session expired!!")
                window.location.href = '../UI/login.html'
            }else if (response.status === 201){
                alert(response.message)
                viewQuestion(question_url)
                notify(response.message,status="success");
                document.querySelector('[data-id="comment-form"]').reset();
                submit.innerHTML = "Post Comment";
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

