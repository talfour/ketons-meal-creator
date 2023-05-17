let close_message = document.querySelector('.message__close')
let message = document.querySelector('.message--active-danger');
try{

close_messages()
}catch(e){
    console.log(e)
}


function close_messages(){
    close_message.addEventListener('click', () =>{
      message.classList.remove('message--active-danger')
      message.classList.remove('message--active')
    })
  }