import re
import torch
from transformers import BertTokenizer, BertModel

# Завантажуємо модель BERT та токенізатор
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Вхідний текст
text = """
Resistors have a temperature range from -55 to 155 degrees Celsius, pressure from 50 to 105 kPa, and humidity from 20 to 80 percent.
Capacitors have a temperature range from -40 to 125 degrees Celsius and pressure from 20 to 100 kPa.
"""

# Компоненти для пошуку
components = ["resistors", "capacitors", "diodes", "transistors"]

# Створюємо порожній словник для зберігання компонентів та їх характеристик
components_data = {}

# Проходимо по кожному компоненту
for component in components:
    # Шукаємо блок тексту, де згадується компонент
    component_block = re.search(rf"({component}.*?)(?:\n|$)", text.lower(), re.DOTALL)
    if component_block:
        component_data = {}

        # Знаходимо температуру, тиск та вологість в блоці компоненту
        temp_match = re.search(r"temperature.*?([-]?\d+).*?([-]?\d+)?\s*degrees\s*celsius", component_block.group(1))
        pressure_match = re.search(r"pressure.*?([-]?\d+).*?([-]?\d+)?\s*kpa", component_block.group(1))
        humidity_match = re.search(r"humidity.*?([-]?\d+).*?([-]?\d+)?\s*percent", component_block.group(1))

        # Додаємо знайдені значення до даних компоненту
        if temp_match:
            component_data["temperature"] = f"{temp_match.group(1)} to {temp_match.group(2)} degrees Celsius" if temp_match.group(2) else f"{temp_match.group(1)} degrees Celsius"
        if pressure_match:
            component_data["pressure"] = f"{pressure_match.group(1)} to {pressure_match.group(2)} kPa" if pressure_match.group(2) else f"{pressure_match.group(1)} kPa"
        if humidity_match:
            component_data["humidity"] = f"{humidity_match.group(1)} to {humidity_match.group(2)} percent" if humidity_match.group(2) else f"{humidity_match.group(1)} percent"

        # Додаємо компонент з характеристиками в словник
        components_data[component] = component_data

# Виводимо знайдені компоненти та їх характеристики
print("Знайдені компоненти та їх характеристики:")
for component, characteristics in components_data.items():
    print(f"{component.capitalize()}:")
    for key, value in characteristics.items():
        print(f"  {key.capitalize()}: {value}")
