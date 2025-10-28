import math

from labyrinth_game.constants import ROOMS

random = 0

def get_input(prompt="> "):

    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def describe_current_room(game_state):
    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]
    
    # Вывод названия комнаты
    print(f"\n== {current_room_name.upper()} ==")
    
    # Вывод описания комнаты
    print(room['description'])
    
    # Вывод предметов, если они есть
    if room['items']:
        print("\nЗаметные предметы:", ", ".join(room['items']))
    
    # Вывод доступных выходов
    exits = room['exits']
    exit_directions = list(exits.keys())
    print("\nВыходы:", ", ".join(exit_directions))
    
    # Сообщение о загадке, если она есть
    if room['puzzle'] is not None:
        print("\nКажется, здесь есть загадка (используйте команду solve).")

def solve_puzzle(game_state):
    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]
    if current_room_name == 'treasure_room':
        return attempt_open_treasure(game_state)

    if room['puzzle'] is None:
        print("Загадок нет")
        return False
        
    question, answer = room['puzzle']
    print(question)
    user_answer = get_input("Ваш ответ: ")

    if answer_check(user_answer, answer, current_room_name):
        print("Верно!")
        room['puzzle'] = None
        if room['items']:
            reward_item = room['items'][0]
            game_state['player_inventory'].append(reward_item)
            print(f"Вы получили: {reward_item}")
            room['items'].remove(reward_item)

    elif current_room_name == 'trap_room':
        print("Неверно!")
        trigger_trap(game_state)
    else:
        print("Неверно!")

def answer_check(user_answer, correct_answer, room_name):
    user_answer = user_answer.lower().strip()
    correct_answer = correct_answer.lower().strip()
    if user_answer == correct_answer:
        return True
    
    alternative_answers = {
        'treasure_room': ['десять', 'ten'],
        'hall': ['десять', 'ten'],
        'library': ['resonance'], 
        'artifact_room': ['insert sword'], 
        'goblin_room': ['hit dodge hit'],
        'trap_room': ['step step step'], 
    }

    if user_answer in alternative_answers[room_name]:
        return True

def attempt_open_treasure(game_state):
    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]
    inventory = game_state['player_inventory']
    if 'treasure_key' in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        if 'treasure_chest' in room['items']:
            room['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return True
    
    print("Сундук заперт. На замке есть клавиатура для ввода кода.")
    answer = get_input("Ввести код? (да/нет): ").strip().lower()
    
    if answer in ('да', 'yes', 'y'):
        code = get_input("Введите код: ").strip()
        correct_code = '10'
        
        if code == correct_code:
            print("Замок щёлкает! Сундук открыт!")
            room['items'].remove('treasure_chest')
            print("В сундуке сокровище! Вы победили!")
            game_state['game_over'] = True

        else:
            print("Неверный код. Замок не открывается.")

    else:
        print("Вы отступаете от сундука.")

def pseudo_random(seed, modulo):
    x = math.sin(seed * 12.9898) * 43758.5453
    fractional_part = x - math.floor(x)
    return math.floor(fractional_part * modulo)

def trigger_trap(game_state):
    print("Ловушка активирована! Пол стал дрожать...")
    inventory = game_state['player_inventory']
    steps = game_state.get('steps_taken', 0)
    
    if inventory:
        item_index = pseudo_random(steps, len(inventory))
        lost_item = inventory[item_index]
        inventory.pop(item_index)
        print(f"В суматохе вы потеряли: {lost_item}")
        
    else:
        global random #random позволит изменять шанс для ловушки, не делая шагов 
        damage_chance = pseudo_random(steps + random, 10)
        random += 1
        if damage_chance < 3:
            print("Вы не успели увернуться! Ловушка нанесла смертельный урон.")
            print("Игра окончена.")
            game_state['game_over'] = True
        else:
            print("Вам повезло! Вы успели увернуться от ловушки.")

def random_event(game_state):

    steps = game_state.get('steps_taken', 0)
    current_room = game_state['current_room']
    inventory = game_state['player_inventory']
    event_chance = pseudo_random(steps, 10)
    if event_chance != 0:
        return  # Событие не происходит

    event_type = pseudo_random(steps + 1, 3)  # +1 чтобы получить другое значение
    match event_type:
        case 0:
            print("Вы заметили что-то блестящее на полу...")
            print("Это монетка! Вы подобрали её.")
            if 'coin' not in inventory:
                game_state['player_inventory'].append('coin')
        
        case 1:
            print("Вы слышите подозрительный шорох из темноты...")
            if 'sword' in inventory:
                print("Вы достаёте меч, и существо быстро ретируется!")
            else:
                print("Вы замираете от страха, но вскоре шорох стихает.")
        
        case 2:
            print("Вы чувствуете, что наступили на подозрительную плиту...")
            if current_room == 'trap_room' and 'torch' not in inventory:
                print("Без факела вы не заметили ловушку вовремя!")
                trigger_trap(game_state)
            else:
                print("К счастью, ловушка оказалась неактивной или вы её заметили.")

# labyrinth_game/utils.py
def show_help(COMMANDS):
    print("Доступные команды:")
    for command, description in COMMANDS.items():
        formatted_command = f"  {command:<16}"
        print(f"{formatted_command}- {description}")