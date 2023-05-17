function loadUnit(){
    //function load unit when dom is loaded and any ingredient is choosen
    let container = document.querySelector("#form-container")
    const url = container.getAttribute('data-unit-url')
    const csrftoken = getCookie("csrftoken");

    let iff = document.querySelectorAll(".recipe-create__ingredients") 
    lista = Array.from(iff)
    lista.map(function (element) {
        let ingredient = element.firstElementChild.nextSibling.nextElementSibling
        // console.log(element)
        if(ingredient.value != ""){
            fetch(url, {
                credentials: 'include',
                method: 'POST',
                mode: 'same-origin',
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken,
                },
                body: JSON.stringify({
                    ingredient: ingredient.value,
                })
                })
                .then((response) => response.text())
                .then((response) =>{
                    element.childNodes[8].innerHTML = response
                })
                .catch((error) => {
                    // console.clear();
                    console.log(error)
                })
        }
        
    });
}

window.addEventListener('DOMContentLoaded', () =>{
    let container = document.querySelector("#form-container")
    let birdForm = document.querySelectorAll(".recipe-create__ingredients")
    let addButton = document.querySelector("#add-form")
    let totalForms = document.querySelector("#id_recipeingredients_set-TOTAL_FORMS")    
    let iff = document.querySelectorAll(".recipe-create__ingredients") 
    let formNum = birdForm.length-1 
    const csrftoken = getCookie("csrftoken");
    const url = container.getAttribute('data-unit-url')
    
    loadUnit();
    
    addButton.addEventListener('click', addForm)
    handleDatalist();
    
    function addForm(e){
        // function which is adding new ingredient form
        e.preventDefault()
        
        
        let newForm = birdForm[0].cloneNode(true)
        let formRegex = RegExp(`recipeingredients_set-(\\d){1}-`,'g')
        formNum++
        newForm.innerHTML = newForm.innerHTML.replace(formRegex, `recipeingredients_set-${formNum}-`)
        let deleteButton = document.createElement('input')
        deleteButton.type = "button"
        deleteButton.value = "Usuń"
        deleteButton.className = "delete-btn"
        newForm.lastChild.previousElementSibling.previousElementSibling.previousElementSibling.innerHTML = "";
        newForm.appendChild(deleteButton)
        deleteButton.addEventListener('click', deleteForm)
        container.insertBefore(newForm, addButton)
        totalForms.setAttribute('value', `${formNum+1}`)
        iff = document.querySelectorAll(".recipe-create__ingredients")  
        ingredients = document.querySelectorAll("[id$='ingredient']")
        
        handleDatalist()
        return iff
    }
    
    function deleteForm(e){
        // function which is deleteing ingredient form
        e.preventDefault()
        formNum--
        e.target.parentNode.remove()
        totalForms.setAttribute('value', `${formNum+1}`)
        iff = document.querySelectorAll(".recipe-create__ingredients")  
        return iff
    }

    function handleDatalist(){
        // function which is handling datalist
        let chosenIngredient = document.querySelectorAll('.recipe-create__choosen_ingredient');
        let container = document.querySelector("#form-container")
        const url = container.getAttribute('data-unit-url')
        const csrftoken = getCookie("csrftoken");
            chosenIngredient.forEach((element) => {
                element.addEventListener('input', () =>{
                    try{
                        const ingredient = document.querySelector('option[value="' + element.value + '"]').getAttribute('data-value');
                        if(ingredient){
                            //jeśli znalazło ingredient
                            element.nextElementSibling.value = ingredient;
                        }
                    }catch(error){
                        // console.log(error)
                    }
                    
                
                })
                element.addEventListener('focusout', () =>{
                    const ingredient = document.querySelector('option[value="' + element.value + '"]').getAttribute('data-value');
                    fetch(url, {
                    credentials: 'include',
                    method: 'POST',
                    mode: 'same-origin',
                    headers: {
                        Accept: "application/json",
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrftoken,
                    },
                    body: JSON.stringify({
                        ingredient: ingredient,
                    })
                    })
                    .then((response) => response.text())
                    .then((response) =>{
                        element.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.innerHTML = ""
                        element.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.innerHTML = response
                    })
                })            
            });
    }
})




