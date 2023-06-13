# imports

import requests
import json
import plotly.express as px
import pandas as pd
import streamlit as st

# api connection

base_url = "https://api.nal.usda.gov/fdc/v1"
api_key = "xxx"

def search_foods(query, data_type=None):
    search_endpoint = f"{base_url}/foods/search"
    params = {
        "api_key": api_key,
        "query": query
    }

    if data_type:
        params["dataType"] = data_type

# verify response

    response = requests.get(search_endpoint, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

# define average protein function

def display_average_protein(results, title):
    if not results:
        print(f"{title}: No results found.")
        return

    total_protein = 0
    count = 0

    for food in results["foods"]:
        protein_amount = get_protein_amount(food)
        total_protein += protein_amount
        count += 1

    average_protein = total_protein / count
    print(f"{title}: Average protein content: {average_protein:.2f} g")

# define amount of protein in the food in grams per a 100 gram serving

def get_protein_amount(food, serving_size=100):
    protein_amount = 0
    for nutrient in food['foodNutrients']:
        if nutrient['nutrientName'] == 'Protein':
            protein_amount = nutrient['value']
            break

    if protein_amount > 0:
        # adjust protein amount based on serving size
        protein_amount = protein_amount * (serving_size / 100)

    return protein_amount

# Define searches for particular foods

# meats
grilled_chicken_results = search_foods("grilled chicken")
ground_beef_results = search_foods("ground beef")
salmon = search_foods("salmon")
tuna = search_foods("tuna")

# dairy
yogurt_results = search_foods("yogurt")
milk = search_foods("milk")
cheese = search_foods("cheese")
cottage_cheese = search_foods("cottage cheese")

# legunes
peas = search_foods("peas")
lentils = search_foods("lentils")
chickpeas = search_foods("chickpeas")
soybeans = search_foods("soybeans")

# nuts & seeds
almonds = search_foods("almonds")
peanuts = search_foods("peanuts")
pistachios = search_foods("pistachios")
walnuts = search_foods("walnuts")
sunflower_seeds = search_foods("sunflower seeds")

# whole grains
quinoa = search_foods("quinoa")
brown_rice = search_foods("brown rice")
oatmeal = search_foods("oatmeal")

# other
eggs = search_foods("eggs")

# display the description of each food listed above

def display_foods(results, title):
    if not results:
        print(f"{title}: No results found.")
        return

    for food in results["foods"]:
        protein_amount = get_protein_amount(food)
        print(f"{food['description']} ({food['dataType']}): {protein_amount} g")

    print()

# Displaying protein results for the foods

def display_food_results():
    print("Average protein content in foods by type of food\n")
    print("\nMeats:")
    display_average_protein(grilled_chicken_results, "Grilled chicken")
    display_average_protein(ground_beef_results, "Ground beef")
    display_average_protein(salmon, "Salmon")
    display_average_protein(tuna, "Tuna")
    print("\nDairy:")
    display_average_protein(yogurt_results, "Yogurt")
    display_average_protein(milk, "Milk")
    display_average_protein(cheese, "Cheese")
    display_average_protein(cottage_cheese, "Cottage cheese")
    print("\nLegumes:")
    display_average_protein(peas, "Peas")
    display_average_protein(lentils, "Lentils")
    display_average_protein(chickpeas, "Chickpeas")
    print("\nNuts & Seeds:")
    display_average_protein(almonds, "Almonds")
    display_average_protein(peanuts, "Peanuts")
    display_average_protein(pistachios, "Pistachios")
    display_average_protein(walnuts, "Walnuts")
    display_average_protein(sunflower_seeds, "Sunflower seeds")
    print("\nWhole Grains:")
    display_average_protein(quinoa, "Quinoa")
    display_average_protein(brown_rice, "Brown rice")
    display_average_protein(oatmeal, "Oatmeal")
    print("\nOther:")
    display_average_protein(eggs, "Eggs")

# Display results for average amount of protein in foods (g) per 100 grams

display_food_results()

#Create new environment: python -m venv myenv
#Activate the environment: myenv\Scripts\activate | C:\Users\kevin>myenv\Scripts\activate
#Run streamlit: python -m streamlit run "c:/Users/kevin/OneDrive/Desktop/Coding Temple/Week 6 (Tableau) + Pipeline/weekend_project/Food_analysis.py"

# Create a DataFrame

columns = ["Food", "Category", "Average Protein (g/100g)"]

protein_data = pd.DataFrame(columns=columns)

# Populate the DataFrame

def populate_dataframe(results, category):
    global protein_data # not a local variable within the function
    if not results:
        return
    
    total_protein = 0
    count = 0

    for food in results["foods"]:
        protein_amount = get_protein_amount(food)
        total_protein += protein_amount
        count += 1

    average_protein = total_protein / count
    protein_data = protein_data.append({"Food": results["foods"][0]["description"],
                                        "Category": category,
                                        "Average Protein (g/100g)": average_protein},
                                        ignore_index = True)

# Populate the DataFrame with the data
populate_dataframe(grilled_chicken_results, "Meats")
populate_dataframe(ground_beef_results, "Meats")
populate_dataframe(salmon, "Meats")
populate_dataframe(tuna, "Meats")
populate_dataframe(yogurt_results, "Dairy")
populate_dataframe(milk, "Dairy")
populate_dataframe(cheese, "Dairy")
populate_dataframe(cottage_cheese, "Dairy")
populate_dataframe(peas, "Legumes")
populate_dataframe(lentils, "Legumes")
populate_dataframe(chickpeas, "Legumes")
populate_dataframe(almonds, "Nuts & Seeds")
populate_dataframe(peanuts, "Nuts & Seeds")
populate_dataframe(pistachios, "Nuts & Seeds")
populate_dataframe(walnuts, "Nuts & Seeds")
populate_dataframe(sunflower_seeds, "Nuts & Seeds")
populate_dataframe(quinoa, "Whole Grains")
populate_dataframe(brown_rice, "Whole Grains")
populate_dataframe(oatmeal, "Whole Grains")
populate_dataframe(eggs, "Other")


# Display the DataFrame in Streamlit
st.title("Average Protein Content by Foods")
st.write(protein_data)

# Create a bar chart of the food categories
fig = px.bar(protein_data, x="Food", y="Average Protein (g/100g)", color="Category")

# Display the chart in Streamlit
st.plotly_chart(fig)

'''Data derived from
U.S. DEPARTMENT OF AGRICULTURE
FoodData Central API'''