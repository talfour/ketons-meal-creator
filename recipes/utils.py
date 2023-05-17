from collections import Counter


def sum_up_nutritien(ingredient_or_kcal, quantity):
    """
        Returns the float nutritional value.
    """

    return round(ingredient_or_kcal*quantity/100, 2)


def sum_up_nutritien_based_by_portions(ingredient_or_kcal, quantity, meal_portions, choosen_portions):
    return round(ingredient_or_kcal*quantity/100/meal_portions*choosen_portions, 2)


def sum_values_from_dictionary(ingr):
    total = sum((Counter(dict(x)) for x in ingr), Counter())
    # tutaj zmieniony counter na dict może w czymś zaszkodzić ?
    total = dict(total)
    return total


def calculation_based_by_quantity(ingr, quantity, gram=1):
    for key in ingr:
        ingr[key] *= quantity/100*gram
    return ingr


def calculation_based_by_portions(ingr, quantity, gram, choosen_portions,max_portions):
    for key in ingr:
        ingr[key] *= quantity/100*gram/max_portions*choosen_portions
    return ingr