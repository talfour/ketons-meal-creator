const button_show = document.querySelectorAll(".calendar-detail__meal__show-all")


button_show.forEach((element) => {
    element.addEventListener('click', () => {
        if(element.previousElementSibling.classList.contains('calendar-detail__meal__meal-ingredients__ingredient--visible')){
            element.previousElementSibling.style.transition = 'none 0s'
            element.previousElementSibling.classList.remove('calendar-detail__meal__meal-ingredients__ingredient--visible')
            element.value = "Pokaż wszystkie składniki żywieniowe"
        }else{
            element.previousElementSibling.style.transition = 'all .7s ease'
            element.previousElementSibling.classList.add('calendar-detail__meal__meal-ingredients__ingredient--visible')
            element.value = "Ukryj"
        }
    })
});