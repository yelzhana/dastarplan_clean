import requests
import json

URL = "http://localhost:8000/api/recipes/"

recipe_data = {
    "title": "Курица по-средиземноморски",
    "description": "Нежная куриная грудка с овощами и травами, запеченная в духовке.",
    "difficulty": "Easy",
    "cook_time": 30,
    "ingredients": [
        {"product": 1, "amount": 500, "unit": "г", "name": "Куриное филе"},
        {"product": 2, "amount": 200, "unit": "г", "name": "Помидоры черри"},
        {"product": 3, "amount": 100, "unit": "г", "name": "Маслины"},
        {"product": 4, "amount": 20, "unit": "мл", "name": "Оливковое масло"}
    ],
    "nutrition_json": {
        "calories": 350,
        "protein": 40,
        "fat": 15,
        "carbs": 10
    }
}

def send_recipe(data):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(URL, data=json.dumps(data), headers=headers)
    
    if response.status_code == 201:
        print("✅ Рецепт успешно добавлен!")
    else:
        print(f"❌ Ошибка {response.status_code}: {response.json()}")

if __name__ == "__main__":
    send_recipe(recipe_data)
