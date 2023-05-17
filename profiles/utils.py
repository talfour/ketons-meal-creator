import uuid


def get_random_code():
    code = str(uuid.uuid4())[:8].replace('-', '').lower()
    return code


def count_calories(weight, height, age, gender, activity, target):
    kcal = 0
    if gender == "female":
        kcal = 665.09 + (9.56 * weight) + (1.85 * height) - (4.67 * age)
        if activity == 'sedentary behaviour':
            kcal *= 1.2
        elif activity == 'light physical activity':
            kcal *= 1.3
        elif activity == 'moderate physical activity':
            kcal *= 1.45
        elif activity == 'vigorous physical activity':
            kcal *= 1.6
        total_kcal = (kcal) -300 if target == 'redukcja' else (kcal + 300) if target == 'masa' else kcal
        return int(total_kcal)
        

    elif gender == "male":
        kcal = 66.47 + (13.75 * weight) + (5 * height) - (6.75 * age)
        if activity == 'sedentary behaviour':
            kcal *= 1.2
        elif activity == 'light physical activity':
            kcal *= 1.3
        elif activity == 'moderate physical activity':
            kcal *= 1.45
        elif activity == 'vigorous physical activity':
            kcal *= 1.6
        total_kcal = (kcal) -300 if target == 'redukcja' else (kcal + 300) if target == 'masa' else kcal
        return int(total_kcal)
    

def count_micronutrient_keto(total_kcal, diet, is_on_adaptation):
    if diet == "keto" and is_on_adaptation:
        carbs = 30
        carbs_kcal = carbs*4
        total_kcal -= carbs_kcal
        proteins_kcal = total_kcal*0.16
        fats_kcal = total_kcal*0.84
        proteins = proteins_kcal/4
        fats = fats_kcal/9
        return int(carbs), int(proteins), int(fats)

    elif diet == "keto" and is_on_adaptation == False:
        proteins_kcal = total_kcal*0.15
        fats_kcal = total_kcal*0.78
        carbs_kcal = total_kcal*0.07
        carbs = carbs_kcal/4
        proteins = proteins_kcal/4
        fats = fats_kcal/9
        return int(carbs), int(proteins), int(fats)


def count_micronutrient_optimal(weight):
    carbs = 0.8*weight
    proteins = 1.2*weight
    fats = 2.5*weight
    return int(carbs), int(proteins), int(fats)