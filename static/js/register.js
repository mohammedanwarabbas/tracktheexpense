const registerField = document.querySelector('#userNameField');
const usernameFeedbackField = document.querySelector('.usernameFeedback')
const usernameSuccessOutput = document.querySelector('.usernameSuccessOutput')
registerField.addEventListener('keyup',(e)=>{console.log({'12':12});
const usernameVal = e.target.value;
usernameSuccessOutput.textContent=`checking ${usernameVal}`;
usernameSuccessOutput.style.display='block';

registerField.classList.remove('is-invalid');
usernameFeedbackField.style.display = 'none';
usernameFeedbackField.innerHTML='';

const submitBtn = document.querySelector('.submit-btn');
if (usernameVal.length>0){
  
    fetch("/authentication/validate-username/",{
        method : 'POST',
        body : JSON.stringify({'username':usernameVal}) 
    })  
    .then((res) => res.json())
    .then((data)=>{
        //console.log('data',data);//testin
        usernameSuccessOutput.style.display='none';
        if(data.username_error){
            registerField.classList.add('is-invalid');
            usernameFeedbackField.style.display = 'block';
            usernameFeedbackField.innerHTML=`<p>${data.username_error}</p>`;
            //feedbackField.innerHTML='<p>'+  data['username_error'] +'</p>';
            //submitBtn.setAttribute("disabled","disabled"); //same as
            submitBtn.disabled =true;
        }else{
            //if no error 
            submitBtn.removeAttribute("disabled");
        }
    });


}

});


const emailField = document.querySelector('#emailField');
const emailFeedbackField = document.querySelector('.emailfeedback')
const emailSuccessOutput = document.querySelector('.emailSuccessOutput')

emailField.addEventListener('keyup',(e)=>{console.log({'12':12});
const emailVal = e.target.value;
emailSuccessOutput.textContent=`checking ${emailVal}`;
emailSuccessOutput.style.display='block';

emailField.classList.remove('is-invalid');
emailFeedbackField.style.display = 'none';
emailFeedbackField.innerHTML='';

const submitBtn = document.querySelector('.submit-btn');
if (emailVal.length>0){
  
    fetch("/authentication/validate-email/",{
        method : 'POST',
        body : JSON.stringify({'email':emailVal}) 
    })  
    .then((res) => res.json())
    .then((data)=>{
        //console.log('data',data);//testin
        emailSuccessOutput.style.display='none';
        if(data.email_error){
            emailField.classList.add('is-invalid');
            emailFeedbackField.style.display = 'block';
            emailFeedbackField.innerHTML=`<p>${data.email_error}</p>`;
            //feedbackField.innerHTML='<p>'+  data['username_error'] +'</p>';
            submitBtn.disabled =true;
        }else{
            submitBtn.removeAttribute("disabled");
        }
    });


}

});



const showPasswordToggle = document.querySelector('.showPasswordToggle');
const passwordField = document.querySelector('#passwordField');
const handleToggleInput=(e)=>{
    if (showPasswordToggle.textContent=='show'){
        showPasswordToggle.textContent='hide';
        passwordField.setAttribute("type", "text");
    }else{
        showPasswordToggle.textContent='show';
        passwordField.setAttribute("type", "password");
    }
};

showPasswordToggle.addEventListener("click", handleToggleInput);

