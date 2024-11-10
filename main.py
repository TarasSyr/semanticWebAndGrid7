import spacy
from spacy.matcher import Matcher

# Завантажуємо модель spaCy для української мови
nlp = spacy.load("uk_core_news_sm")

# Текст для аналізу
text = """
Резистори мають робочу температуру 155 градусів Цельсія, робочий тиск 105 кПа і працюють при вологості 80 відсотків.
Конденсатори мають робочу температуру 125 градусів Цельсія, робочий тиск 100 кПа і працюють при вологості 90 відсотків.
Діоди мають робочу температуру 150 градусів Цельсія, робочий тиск 110 кПа і працюють при вологості 85 відсотків.
Транзистори мають робочу температуру 70 градусів Цельсія, робочий тиск 85 кПа і працюють при вологості 60 відсотків.
"""

# Обробляємо текст
doc = nlp(text)

# Створюємо об'єкт Matcher
matcher = Matcher(nlp.vocab)

# Паттерни для компонентів
component_pattern = [{"LOWER": {"in": ["резистори", "конденсатори", "діоди", "транзистори"]}}]

# Паттерни для характеристик
temperature_pattern = [{"IS_DIGIT": True}, {"ORTH": "градусів"}, {"ORTH": "Цельсія"}]
pressure_pattern = [{"IS_DIGIT": True}, {"ORTH": "кПа"}]
humidity_pattern = [{"IS_DIGIT": True}, {"ORTH": "відсотків"}]

# Додаємо паттерни до Matcher
matcher.add("ELECTRONIC_COMPONENT", [component_pattern])
matcher.add("TEMPERATURE", [temperature_pattern])
matcher.add("PRESSURE", [pressure_pattern])
matcher.add("HUMIDITY", [humidity_pattern])

# Шукаємо паттерни
matches = matcher(doc)

# Створюємо словник для зберігання знайдених компонентів і характеристик
components = {}
current_component = None
current_characteristics = {"temperature": [], "pressure": [], "humidity": []}

# Обробляємо знайдені паттерни для зв'язування компонентів з їх характеристиками
for match_id, start, end in matches:
    match_name = nlp.vocab.strings[match_id]  # Отримуємо назву паттерну
    span = doc[start:end]  # Виділяємо текст для паттерну

    print(f"Обробляємо: {match_name} - {span.text}")

    # Перевіряємо на знайдений компонент
    if match_name == "ELECTRONIC_COMPONENT":
        # Якщо компонент вже знайдений, зберігаємо його характеристики
        if current_component:
            components[current_component] = current_characteristics
        # Оновлюємо поточний компонент
        current_component = span.text
        current_characteristics = {"temperature": [], "pressure": [], "humidity": []}
        print(f"Знайдено компонент: {current_component}")
    elif match_name == "TEMPERATURE" and current_component:
        current_characteristics["temperature"].append(span.text)
        print(f"Додано температура: {span.text}")
    elif match_name == "PRESSURE" and current_component:
        current_characteristics["pressure"].append(span.text)
        print(f"Додано тиск: {span.text}")
    elif match_name == "HUMIDITY" and current_component:
        current_characteristics["humidity"].append(span.text)
        print(f"Додано вологість: {span.text}")

# Зберігаємо останній компонент
if current_component:
    components[current_component] = current_characteristics

# Виводимо результат
print("\nЗнайдені компоненти та їх характеристики:")
for component, characteristics in components.items():
    print(f"{component}:")
    print(f"  Температура: {', '.join(characteristics['temperature'])}")
    print(f"  Тиск: {', '.join(characteristics['pressure'])}")
    print(f"  Вологість: {', '.join(characteristics['humidity'])}")
