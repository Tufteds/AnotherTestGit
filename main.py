# Импорт модулей
import random
import matplotlib.pyplot as plt # Перед запуском скачать модуль или удалить его!

# Начальные параметры
population_size = int(input("Введите размер популяции: "))
initial_infected = round(population_size * 0.05)
infection_probability = 0.1
base_duration = random.randint(5, 6)
power_immunity = ['low', 'medium', 'strong']
immunity_effects = {'low': 1, 'medium': 0, 'strong': -1}
time_incubation = 2

# Запрос популяции
while population_size <= 0:
    print("Размер популяции должен быть положительным числом.")
    population_size = int(input("Введите размер популяции: "))

# Инициализация популяции
def initialize_population(size, infected_count):
    population = [{'status': 'healthy', 'days_infected': 0,
                   'incubation': 0, 'immunity': random.choice(power_immunity)} for _ in range(size)]
    for i in range(infected_count):
        population[i]['status'] = 'exposed'
    return population

# Обновление статуса инфицированных и заражённых
def update_infections(population):
    # Получение статуса инфицированного или заражённого
    new_infections = 0
    for person in population:
        if person['status'] == 'infected':
            person['days_infected'] += 1
            if person['days_infected'] >= base_duration + immunity_effects[person['immunity']]:
                person['status'] = 'cured'
        elif person['status'] == 'exposed':
            person['incubation'] += 1
            if person['incubation'] >= time_incubation:
                person['status'] = 'infected'
    # Заражение
    infected_people = [p for p in population if p['status'] == 'infected']
    for infected_person in infected_people:
        healthy_people = [p for p in population if p['status'] == 'healthy']
        contacts_count = min(2, len(healthy_people))  # Число контактов в день
        if contacts_count > 0:
            contacts = random.sample(healthy_people, contacts_count)
            for other_person in contacts:
                adjusted_probability = infection_probability + \
                    (0.03 if infected_person['immunity'] == 'low' else -0.03 if infected_person['immunity'] == 'strong' else 0)
                if random.random() < adjusted_probability:
                    other_person['status'] = 'exposed'
                    other_person['incubation'] = 0
                    new_infections += 1
    return new_infections

# Основная логика симуляции
def simulate(days):
    population = initialize_population(population_size, initial_infected)
    history = {'healthy': [], 'exposed': [], 'infected': [], 'cured': []}

    for day in range(days):
        healthy_count = sum(1 for p in population if p['status'] == 'healthy')
        exposed_count = sum(1 for p in population if p['status'] == 'exposed')
        infected_count = sum(1 for p in population if p['status'] == 'infected')
        cured_count = sum(1 for p in population if p['status'] == 'cured')

        history['healthy'].append(healthy_count)
        history['exposed'].append(exposed_count)
        history['infected'].append(infected_count)
        history['cured'].append(cured_count)

        print(f"--------День {day + 1}-----------")
        print(f"Здоровые: {healthy_count}, Подверженные: {exposed_count}, Заражённые: {infected_count}, Вылеченные: {cured_count}")

        if (infected_count == 0 and exposed_count == 0) or healthy_count == 0:
            print("Симуляция завершена.")
            break

        new_infections = update_infections(population)
        print(f"Новые заражённые: {new_infections}")

    # Визуализация результатов (matplotlib)
    plt.plot(history['healthy'], label='Здоровые')
    plt.plot(history['exposed'], label='Подверженные')
    plt.plot(history['infected'], label='Заражённые')
    plt.plot(history['cured'], label='Вылеченные')
    plt.xlabel('Дни')
    plt.ylabel('Количество людей')
    plt.title('Моделирование распространения ОРВИ')
    plt.legend()
    plt.show()

# Запуск симуляции
days = int(input("Введите количество дней симуляции: "))
while days <= 0:
    print("Количество дней должно быть положительным числом.")
    days = int(input("Введите количество дней симуляции: "))
simulate(days)
