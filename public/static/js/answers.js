document.addEventListener('DOMContentLoaded', function(){
    const bestAnswer = document.querySelectorAll('.btn.question__answers__details__mark-as-best-btn');
    const csrftoken = getCookie("csrftoken");
    // const answerId = bestAnswer.getAttribute("data-id"); //this one need to go inside foreach loop
    const replyBtn = document.querySelectorAll('.question__answers__details__reply-btn');
    let mainReply = document.querySelector('.btn.question__answer-form__button')
    let close_message = document.querySelector('.message__close')
    const messageText = document.querySelector('.message--success')
    const message = document.querySelector('.message')
    let voted_value = document.querySelector('.question__vote-value').value
    
    let score = document.querySelector('.bold.question__score');

    try{
      const like = document.querySelector('.btn.btn-like.question-up')
      like.addEventListener('click', () => {
        question_id = like.getAttribute("data-id")
        question_value = like.getAttribute("data-value")
        fetch('/questions/vote-system', {
          credentials: 'include',
          method: 'POST',
          mode: 'same-origin',
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
          body: JSON.stringify({
            question_id: question_id,
            value: question_value
          })
        })
        .then((response) => response.json())
        .then((response) => {
          let current_score = parseInt(score.innerText)
          current_score + 1
          if(voted_value == 'unlike'){
            score.innerText = current_score + 2
          }else{
            score.innerText = current_score +1
          }
          
          like.style.display = 'none';
        })
      })
    }catch{

    }

    try{
      const unlike = document.querySelector('.btn.btn-like.question-down')
      unlike.addEventListener('click', () => {
        question_id = unlike.getAttribute("data-id")
        question_value = unlike.getAttribute("data-value")
        fetch('/questions/vote-system', {
          credentials: 'include',
          method: 'POST',
          mode: 'same-origin',
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
          body: JSON.stringify({
            question_id: question_id,
            value: question_value
          })
        })
        .then((response) => response.json())
        .then((response) => {
          let current_score = parseInt(score.innerText)
          current_score - 1
          if(voted_value == 'like'){
            score.innerText = current_score - 2
          }else{
            score.innerText = current_score - 1
          }
          
          unlike.style.display = 'none';
        })
      })
  
    }catch{

    }


    

    try{
      mainReply.addEventListener('click', () =>{
        let form = document.querySelector('.question__answer-form');
        if(form.classList.contains('question__answer-form--active')){
          form.classList.remove('question__answer-form--active');
          mainReply.value = "Odpowiedz na pytanie";
        }else{
          
          form.classList.add('question__answer-form--active');
          mainReply.value = "Zamknij";
        }
      })
    }catch{

    }


    replyBtn.forEach(function (el){
      el.addEventListener('click', function(e){
        e.preventDefault();
        // question__answers__answer__reply__form--active
        let element = e.target.parentNode.nextElementSibling.lastElementChild;
        if(element.classList.contains('question__answers__answer__reply__form--active')){
          element.classList.remove('question__answers__answer__reply__form--active');
          el.innerText = "Odpowiedz";
        }else{
          element.classList.add('question__answers__answer__reply__form--active')
          el.innerText = "Zamknij";
        }     
      })
    })
    function close_messages(){
      close_message.addEventListener('click', () =>{
        message.classList.remove('message--active-danger')
        message.classList.remove('message--active')
      })
    }

    bestAnswer.forEach(element => {
      element.addEventListener('click', (e) =>{
        e.preventDefault();
        let dataId = e.target.getAttribute("data-id")
        fetch('/questions/marked/', {
          credentials: 'include',
          method: 'POST',
          mode: 'same-origin',
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
          body: JSON.stringify({
            answer_id: dataId,
          })
        })
        .then((response) => response.json())
        .then((response) =>{
          
          messageText.innerText = response.message;
          message.classList.add('message--active')
          close_messages()
          element.remove()
          mainReply.remove()
          let form = document.querySelector('.question__answer-form')
          form.remove()
          replyBtn.remove()
          let form_reply = document.querySelector('.question__answers__answer__reply__form__form')
          form_reply.remove()
        });
      });
    });
});