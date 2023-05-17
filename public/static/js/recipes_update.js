

try{
  let close_message = document.querySelector('.message__close')
  let message = document.querySelector('.message--active-danger')
  let message_text = document.querySelector('message__mess')
  function close_messages(){
    close_message.addEventListener('click', () =>{
      message.classList.add('hidden')
    })
  }
  close_messages()
}catch(e){

}
let birdForm = document.querySelectorAll(".recipe-create__ingredients")
let container = document.querySelector("#form-container")
let addButton = document.querySelector("#add-form")
let totalForms = document.querySelector("#id_recipeingredients_set-TOTAL_FORMS")
const csrftoken = getCookie("csrftoken");
const url = container.getAttribute('data-unit-url')
const recipe_id = container.getAttribute('recipe-id')
let ingredient_form = document.querySelectorAll(".recipe-create__ingredients")  
let ingredients = document.querySelectorAll("[id$='ingredient']")
const recipe_url = container.getAttribute('data-recipe-url')

function close_messages(){
  close_message.addEventListener('click', () =>{
    message.classList.remove('message--active-danger')
    message.classList.remove('message--active')
  })
}



window.addEventListener('DOMContentLoaded', () => {
  // handleDatalist()
  // to zwraca mi możliwe values do wyboru i ładuje je na start
  ingredients.forEach(element => {
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
        ingredient: element.value
      })
    })
    .then((response) => response.text())
    .then((response) =>{
      // // console.log(element.nextElementSibling.nextElementSibling.nextElementSibling)
      // console.log(response)
      // console.log(element.nextElementSibling.nextElementSibling.nextElementSibling)
      element.nextElementSibling.nextElementSibling.nextElementSibling.innerHTML = response
      
    })
});

function getUnitForIngredient(){
  //function which is getting choosen value "rodzaj" for specific ingredient
  fetch(recipe_url, {
      credentials: 'include',
        method: 'POST',
        mode: 'same-origin',
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
    },
      body: JSON.stringify({
        recipe: recipe_id
      })
    })
    .then((response) => response.json())
    .then((response) =>{
      ingredients.forEach(element => {
        const ingredient = document.querySelector('option[data-value="' + element.value + '"]');
        //change input value
        element.previousElementSibling.value = ingredient.value
        if(Object.keys(response.ingredients).includes(element.value)){
          // console.log(response.ingredients[element.value][1])
          
          element.nextElementSibling.nextElementSibling.nextElementSibling.value = response.ingredients[element.value][1]
          // console.log(element.nextElementSibling.nextElementSibling.nextElementSibling)
        }
      })
      
    })
}
handleDatalist()
getUnitForIngredient()

});
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



// Handle adding and deleting ingredient forms
let formNum = birdForm.length-1
addButton.addEventListener('click', addForm)

function addForm(e){
    e.preventDefault()
    
    
    let newForm = birdForm[0].cloneNode(true)
    let formRegex = RegExp(`recipeingredients_set-(\\d){1}-`,'g')
    formNum++
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `recipeingredients_set-${formNum}-`)
    let deleteButton = document.createElement('input')
    deleteButton.type = "button"
    deleteButton.value = "Usuń"
    deleteButton.className = "delete-btn"
    newForm.appendChild(deleteButton)
    // console.log(newForm)
    newForm.removeChild(newForm.childNodes[12])
    newForm.removeChild(newForm.childNodes[11])
    
    deleteButton.addEventListener('click', deleteForm)
    container.insertBefore(newForm, addButton)
    
    totalForms.setAttribute('value', `${formNum+1}`)
    ingredient_form = document.querySelectorAll(".recipe-create__ingredients")  
    ingredients = document.querySelectorAll("[id$='ingredient']")
    handleDatalist()
    return ingredient_form
}

function deleteForm(e){
    e.preventDefault()
    formNum--
    e.target.parentNode.remove()
    totalForms.setAttribute('value', `${formNum+1}`)
    ingredient_form = document.querySelectorAll(".recipe-create__ingredients")  
    return ingredient_form
}


