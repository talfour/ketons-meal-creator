const news = document.querySelector('.btn.actions__header');

news.addEventListener('click', () =>{
    let actions = document.querySelector('.actions');

    if(actions.classList.contains('expanded-actions')){
        actions.classList.remove('expanded-actions');
        news.value = "Nowości"
        actions.classList.add('collapsed-actions');
    }else{
        actions.classList.remove('collapsed-actions')
        news.value = "Schowaj"
        actions.classList.add('expanded-actions');
    }
})