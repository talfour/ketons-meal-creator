const showFollowers = document.querySelector(".my-profile__overview__followers__button");
const showFollowing = document.querySelector(".my-profile__overview__following__button");
const followersList = document.querySelector(".followers-list");
const followingList = document.querySelector(".following-list");
const updateProfile = document.querySelector(".my-profile__overview__update-button");
const formUpdate = document.querySelector("#form-update");
const modal_body = document.querySelector(".modal__body");
const modal = document.querySelector(".modal");
const checkbox = document.querySelector('input[type="checkbox"]');
let message = document.querySelector('.message--active');
let close_message = document.querySelector('.message__close')
let userWantToTypeNutritiens = document.querySelector('#id_want_to_type_nutritiens')
let hidden = document.querySelectorAll('.profile-update-form__form--hidden')
const kcal = document.querySelector('#id_total_kcal')
const proteins = document.querySelector('#id_proteins')
const carbs = document.querySelector('#id_carbs')
const fats = document.querySelector('#id_fats')
// document.addEventListener("DOMContentLoaded", () =>{
//     const checkboxStyle = document.createElement("span")
//     checkboxStyle.classList.add("checkbox")
//     checkbox.append(checkboxStyle)
// })
try{
    close_messages()
}catch{

}


function close_messages(){
    close_message.addEventListener('click', () =>{
      message.classList.remove('message--active-danger')
      message.classList.remove('message--active')
    })
  }

if (showFollowing){
    showFollowing.onclick = () =>{
        followingList.style.display = "block";
        modal.classList.add("open");
        modal_body.appendChild(followingList)
    }
}

if (showFollowers){
    showFollowers.onclick = () =>{
        followersList.style.display = "block";
        modal.classList.add("open");
        modal_body.appendChild(followersList);
    }
}



updateProfile.onclick = () => {
    if(updateProfile.value == "Zaktualizuj profil"){
        formUpdate.style.opacity = 100;
        formUpdate.style.height = 'auto';
        formUpdate.style.pointerEvents = 'auto';
        updateProfile.value = "Zamknij";
    }else{
        formUpdate.style.opacity = 0;
        formUpdate.style.height = 0;
        formUpdate.style.pointerEvents = 'none';
        updateProfile.value = "Zaktualizuj profil"
    }
    

}

modal.addEventListener("click", (e) =>{
    if(e.target.classList.contains("modal")) {
        modal_body.innerHTML = '';
        modal.classList.remove("open");

    }
});

if(userWantToTypeNutritiens.checked){
    hidden.forEach((element) => {
        element.firstElementChild.style.display = "block";
        element.classList.add("profile-update-form__form--displayed")
    }); 
}

userWantToTypeNutritiens.addEventListener('change', function(){
    if(userWantToTypeNutritiens.checked){
        hidden.forEach((element) => {
            element.firstElementChild.style.display = "block";
            element.classList.add("profile-update-form__form--displayed")
        }); 
    }else{
        hidden.forEach((element) => {
            element.firstElementChild.style.display = "none";
            element.classList.remove("profile-update-form__form--displayed")
        });
    }
})

