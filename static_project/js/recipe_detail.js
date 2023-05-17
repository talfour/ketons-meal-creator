document.addEventListener("DOMContentLoaded", function () {
    const csrftoken = getCookie("csrftoken");
    let show_additiona_info = document.querySelector('.meal-details__nutritions__nutrition__show-additional')
    let close_message = document.querySelector('.message__close')
    let answer_comment = document.querySelectorAll('.comment__reply-btn')
    let new_comment = document.querySelector('.comments__add-new-comment');
    
    show_additiona_info.addEventListener('click', () =>{
      let additional_info = document.querySelectorAll('.meal-details__nutritions__nutrition__additional')
      if(show_additiona_info.value == "Więcej"){
        show_additiona_info.value = "Ukryj"
        additional_info.forEach(e => {
          e.classList.add('meal-details__nutritions__nutrition__additional--active')
        });
      }else{
        show_additiona_info.value = "Więcej";
        additional_info.forEach(e => {
          e.classList.remove('meal-details__nutritions__nutrition__additional--active')

        })
      }
      
    })

    new_comment.addEventListener('click', () =>{
      const form = document.querySelector('.comments__new-comment');
      if(new_comment.value == "Dodaj nowy komentarz"){
        
        form.classList.add('comments__new-comment--active');
        new_comment.value = "Zamknij";
      }else{
        form.classList.remove('comments__new-comment--active');
        new_comment.value = "Dodaj nowy komentarz";
      }
      
    });

    answer_comment.forEach((element) =>{
        element.addEventListener('click', () =>{
          if(element.value == "Odpowiedz"){
            element.parentElement.nextElementSibling.lastElementChild.classList.add('comment__reply-form--active');
            element.value = "Zamknij";
          }else{
            element.parentElement.nextElementSibling.lastElementChild.classList.remove('comment__reply-form--active');
            element.value = "Odpowiedz";
          }
        })
      
      
    })
   

    function close_messages(){
      close_message.addEventListener('click', () =>{
        message.classList.remove('message--active-danger')
        message.classList.remove('message--active')
      })
    }
    try{
    let like_btn = document.querySelector('#like-recipe');
    let recipe_id = like_btn.getAttribute("data-id");
    let add_to_book = document.querySelector('.btn.btn-add-to-book')
    let recipe_id_atb = add_to_book.getAttribute("data-id");
    let message = document.querySelector('.message');
    let mess = document.querySelector('.message__mess');
    let total_likes = document.querySelector("#total_likes");
    

    

    

    

    if(add_to_book){
      add_to_book.addEventListener('click', () =>{
        fetch("/recipes/add_to_book/", {
          credentials: "include",
          method: "POST",
          mode: "same-origin",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body:JSON.stringify({
          recipe_id: recipe_id_atb,
        })
      })
      .then((response) => response.json())
      .then((saveresponse) =>{
        mess.innerHTML = `${saveresponse.message}`;
        if(add_to_book.innerHTML == `<i class=\"fas fa-book-medical\" aria-hidden=\"true\">Dodaj do książki</i>`){
          message.classList.remove('message--active-danger')
          message.classList.add('message--active')
          close_messages()
          add_to_book.innerHTML = `<i class="fas fa-book-dead">Usuń z książki</i>`;
        }
        else{
          message.classList.add('message--active-danger')
          add_to_book.innerHTML = `<i class="fas fa-book-medical">Dodaj do książki</i>`;
          close_messages()
        }
      })
      })
    }



    if(like_btn){
      like_btn.addEventListener('click', () =>{
        fetch("/recipes/recipe_liked/", {
          credentials: "include",
          method: "POST",
          mode: "same-origin",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body:JSON.stringify({
          recipe_id: recipe_id,
        })
      })
      .then((response) => response.json())
      .then((likeresponse) =>{
        mess.innerHTML = `${likeresponse.message}`
        if(like_btn.innerHTML == `<i class=\"fas fa-thumbs-up\" aria-hidden=\"true\">Like</i>`){
          message.classList.remove('message--active-danger')
          message.classList.add('message--active')
          close_messages()
          let likes_count = parseInt(total_likes.innerHTML) + 1
          total_likes.innerHTML = ` ${likes_count}`
          like_btn.innerHTML = `<i class="fas fa-thumbs-down">Unlike</i>`;
        }
        else{
          message.classList.add('message--active-danger')
          let likes_count = parseInt(total_likes.innerHTML) - 1
          total_likes.innerHTML = ` ${likes_count}`
          like_btn.innerHTML = `<i class="fas fa-thumbs-up">Like</i>`;
          close_messages()
        }
      })
      })
    }
    }
    catch (e){
      if(e instanceof ReferenceError){

      }
    }
    
    
    
    

});
