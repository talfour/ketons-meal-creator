try{
    const searchBtn = document.querySelector('.menu__search');
    const backBtn = document.querySelector('.menu__back');
    searchBtn.addEventListener('click', toggleSearchBox);
    backBtn.addEventListener('click', toggleSearchBox);
}catch(e){

}


    const nav = document.querySelector('.menu');
    const menuBtn = document.querySelector('.menu__button');
    const sideBar = document.querySelector('.sidebar');
    
    

    menuBtn.addEventListener('click', toggleSideBar);



function toggleSideBar(){
    if(sideBar.classList.contains('sidebar--active')){
        sideBar.classList.remove('sidebar--active')
        menuBtn.innerHTML = '<i class="fas fa-bars"></i>'
    }else{
        sideBar.classList.add('sidebar--active')
        menuBtn.innerHTML = '<i class="fas fa-times"></i>'
    }
}

function toggleSearchBox(){
    if(nav.classList.contains('search_active')){
        nav.classList.remove('search_active');
    }else{
        nav.classList.add('search_active');
    }
}