// const menuBtn = document.querySelector(".menu-icon span");
// const searchBtn = document.querySelector(".search-icon");
// const cancelBtn = document.querySelector(".cancel-icon");
// const items = document.querySelector(".nav-items");
// const form = document.querySelector("form");

// const commentReplyBtn = document.querySelectorAll(".comment-reply-btn");
const navIcon = document.querySelector('.menu__icon');
const menuList = document.querySelector('.menu__list')
const menuListWrapper = document.querySelector('.menu-wrapper')

navIcon.onclick = function() {
  this.classList.toggle("menu__icon--active");
  menuListWrapper.classList.toggle('menu-wrapper--active')
  menuList.classList.toggle("menu__list--active");

}

// menuBtn.onclick = () => {
//   items.classList.add("active");
//   menuBtn.classList.add("hide");
//   searchBtn.classList.add("hide");
//   cancelBtn.classList.add("show");
//   cancelBtn.style.color = "#d08770";
// // };
// cancelBtn.onclick = () => {
//   items.classList.remove("active");
//   menuBtn.classList.remove("hide");
//   searchBtn.classList.remove("hide");
//   cancelBtn.classList.remove("show");
//   form.classList.remove("active");
//   cancelBtn.style.color = "#d08770";
// };
// searchBtn.onclick = () => {
//   form.classList.add("active");
//   searchBtn.classList.add("hide");
//   cancelBtn.classList.add("show");
//   cancelBtn.style.color = "#d08770";
// };

// commentReplyBtn.forEach(function (el) {
//   el.addEventListener("click", function (e) {
//     let element = e.target.parentElement.nextElementSibling;
//     if (element) {
//       if (element.classList.contains("fade-out")) {
//         element.classList.remove("fade-out");
//         element.classList.add("fade-in");
//         el.innerHTML = "Hide";
//       } else {
//         element.classList.remove("fade-in");
//         element.classList.add("fade-out");
//         el.innerHTML = "Reply";
//       }
//     }
//   });
// });


