import { append_logout,logout,notify,parseJwt,avatar_image} from './helper.js';
import base from './base.js';

var profile_url
var identity
var name
window.onload = function () {
    append_logout()
    var logout_link = document.querySelector('.logout');
    if(logout_link){
        logout_link.addEventListener('click', logout)
    }
    var token = localStorage.getItem("token");
    var decode=parseJwt(token)
    console.log(decode)
    identity=decode.identity
    
    let id =decode.identity.id
    name=identity.firstname+' '+identity.othername+' '+identity.lastname
    console.log(id)
    if(id){
        profile_url='/auth/'+id
        viewProfile(profile_url)
    }
   
}

function viewProfile(url){
   
    base
    .get(url)
    .then(function(response){return response.json()})
    .then(data => {
        console.log(data)
        if(data.status ===200){
            let questions_commented=data.questions_commented[0].count
            let questions_posted=data.questions_posted[0].count
            let questions= data.feeds
            // let meetup = data.meetup[0]
            // let questions =data.questions
            // topic=meetup.topic
            // let image=localStorage.getItem("image");
           
            document.querySelector('.t-name').innerHTML=`: ${name} `;
            document.querySelector('.t-questions').innerHTML=`: (${questions_posted})`;
            document.querySelector('.t-comments').innerHTML=`: (${questions_commented})`;
            if(questions){
                document.querySelector('#questions-title').style.display="block"
                var i = 0;
                let result = ''
                console.log(questions)
                for(var count=0; count < questions.length; count++){
                    let question = questions[count]
                    console.log(question)
                    // getComments(question.id)
                    result += 
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
                                        <span><a class="comment-${question.questions_id}" id="${question.questions_id}" href="#"><i class="far fa-comment"></i> view comments</a></span>
                                    </div>
                                    <div id="comments">
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>`
                }
                document.getElementById('questions').innerHTML=result
                
                for(var count=0; count < questions.length; count++){
                    let question = questions[count]
                    document.querySelector('.upvote-'+question.questions_id).addEventListener('click',upvote);
                    document.querySelector('.downvote-'+question.questions_id).addEventListener('click',downvote);
                    document.querySelector('.comment-'+question.questions_id).addEventListener('click',viewComment);
                }
            }
        
        }else{
            // alert(data.error)
            let el =document.querySelector('.meetup-details');
            el.innerHTML=`<div id="notification" class="alert alert-danger" role="alert">${data.error}</div>`;
        }

    })
}

function viewComment(e){
    e.preventDefault();
    console.log(this.id)
    localStorage.setItem('question-id',this.id);
    window.location.href = '../UI/view-comment.html'
}
function upvote(e){
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
                viewProfile(profile_url)
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

function downvote(e){
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
                viewProfile(profile_url)
            }else{
                alert(response.error)
                notify(response.error,status="error");
            }
        })
    }else{
        alert("You have to be logged in user in order to post a question")
    }
}



