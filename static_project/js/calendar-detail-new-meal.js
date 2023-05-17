const csrftoken = getCookie("csrftoken");
const meal_form = document.querySelector("#meal_form")
const url = meal_form.getAttribute('data-unit-url')
const recipe_url = meal_form.getAttribute('data-recipe-url')
const recipe = document.querySelector("#id_recipe")
let recipe_info = document.querySelector('.calendar-new-meal__recipe-info')
let portions = document.querySelector('#id_portions')
const check_recipe_btn = document.querySelector('#check_recipe')

window.addEventListener("DOMContentLoaded", () => {
    check_recipe_btn.addEventListener('click', () =>{
        recipe_info.innerHTML = ""
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
                recipe_id: recipe.value,
                portions: portions.value
            })
            })
            .then((response) => response.json())
            .then((response) =>{
                let kcal = check_value(response.meal_info['Kalorie'])
                let białko = check_value(response.meal_info['Białko'])
                let tłuszcze = check_value(response.meal_info['Tłuszcze'])
                let węglowodany = check_value(response.meal_info['Węglowodany'])
                let węglowodany_netto = check_value(response.meal_info['Węglowodany netto'])
                let błonnik = check_value(response.meal_info['Błonnik'])
                recipe_info.classList.add('calendar-new-meal__recipe-info--active')
                response.meal_info['Błonnik']
                recipe_info.innerHTML += `<div class="recipe__info">
                <h1 class="recipe-info__header">Wartości odżywcze z przepisu uzwględniając wybraną ilość porcji: <span class="bold">${portions.value}</span></h1>
                <div class="recipe-info__nutritions">
                    <div class="recipe-info__nutritions__nutri"><span class="bold">Kalorie:</span> ${kcal} kcal</div>
                    <div class="recipe-info__nutritions__nutri"><span class="bold">Białko:</span> ${białko} g</div>
                    <div class="recipe-info__nutritions__nutri"><span class="bold">Tłuszcze:</span> ${tłuszcze} g</div>
                    <div class="recipe-info__nutritions__nutri"><span class="bold">Węglowodany:</span> ${węglowodany} g</div>
                    <div class="recipe-info__nutritions__nutri"><span class="bold">Węlgowodany netto:</span> ${węglowodany_netto} g</div>
                    <div class="recipe-info__nutritions__nutri"><span class="bold">Błonnik:</span> ${błonnik} g</div>         
                    </div>
                </div>`;
                
                for(var key in response.ingredients) {
                    var value = response.ingredients[key]
                    if(value['unit'] != 'gram'){
                        recipe_info.innerHTML += `<div class="recipe-info__ingredient">
                                                    <span class="bold">Produkt:</span> ${value['ingredient']}
                                                    <span class="bold">Ilość:</span> ${value['quantity']} ${value['unit']} 
                                                    <span class="bold">Około:</span> ${value['gram']}gram
                                                  </div>`
                    
                    }else{
                        recipe_info.innerHTML += `<div class="recipe-info__ingredient"><span class="bold">Produkt:</span> ${value['ingredient']} <span class="bold">Ilość:</span> ${value['quantity']} ${value['unit']}</div>`   
                    }
            }
                
            })
    });

function check_value(value){
    if(value != undefined){
        return Math.round(value * 100 / 100)
    }else{
        return value = 0
    }
}












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
            recipe: recipe.value
        })
        })
        .then((response) => response.json())
        .then((response) =>{
            portions.setAttribute("min", "1");
            portions.setAttribute("max", `${response.portions}`);
            
        })
})

function load_portions(){
    recipe.addEventListener('change', (e) =>{
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
                recipe: recipe.value
            })
            })
            .then((response) => response.json())
            .then((response) =>{
                portions.setAttribute("max", `${response.portions}`);
            });
        });
}


