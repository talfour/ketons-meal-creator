document.addEventListener("DOMContentLoaded", function () {
    const csrftoken = getCookie("csrftoken");
    const followBtn = document.querySelector("#follow");
    const user_id = document.querySelector("#follow").getAttribute("data-id");
    let total_followers = document.querySelector('.profile-overview__profile-followers__number')
    number = parseInt(total_followers.innerHTML)

  
    if(followBtn){
      followBtn.addEventListener("click", (e) => {
        e.preventDefault();

        
        fetch(`/profiles/profile/follow_user/`, {
          credentials: "include",
          method: "POST",
          mode: "same-origin",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
          body: JSON.stringify({
            following_user: user_id,
          }),
        })
          .then((response) => response.json())
          .then((follow) => {
            if(followBtn.innerText == "FOLLOW"){
              number++
              if(number == 1){
                total_followers.innerHTML = `${number} obserwujący`
              }else{
                total_followers.innerHTML = `${number} obserwujących`
              }
              followBtn.innerText = "UNFOLLOW"
            }
            else{
              number--
              if(number == 1){
                total_followers.innerHTML = `${number} obserwujący`
              }else{
                total_followers.innerHTML = `${number} obserwujących`
              }
              followBtn.innerText = "FOLLOW"
              
            }
          });
      });
    }
    
    
    
  });