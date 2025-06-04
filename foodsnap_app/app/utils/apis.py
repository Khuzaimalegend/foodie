import os
import requests
from config import NUTRITIONIX_APP_ID, NUTRITIONIX_APP_KEY, EDAMAM_APP_ID, EDAMAM_APP_KEY

def get_nutrition(query_food: str):
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": NUTRITIONIX_APP_ID,
        "x-app-key": NUTRITIONIX_APP_KEY,
        "Content-Type": "application/json",
    }
    data = {"query": query_food, "timezone": "UTC"}
    try:
        resp = requests.post(url, json=data, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"[Nutritionix Error] {e}")
        return None

def get_recipe(query_food: str, max_results: int = 3):
    url = "https://api.edamam.com/search"
    params = {
        "q": query_food,
        "app_id": EDAMAM_APP_ID,
        "app_key": EDAMAM_APP_KEY,
        "from": 0,
        "to": max_results,
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        recipes = []
        for hit in data.get("hits", []):
            recipe = hit.get("recipe", {})
            recipes.append({
                "label": recipe.get("label"),
                "url": recipe.get("url"),
                "ingredients": recipe.get("ingredientLines"),
                "calories": int(recipe.get("calories", 0)),
            })
        return recipes
    except Exception as e:
        print(f"[Edamam Error] {e}")
        return []
