from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room, random_event


def show_inventory(game_state):
    inventory = game_state['player_inventory']
    if inventory:
        print("Инвентарь: ", ", ".join(inventory))
    else:
        print("Инвентарь пуст")

def move_player(game_state, direction):
    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]

    if direction in room['exits']:
        next_room = room['exits'][direction]
        if next_room == 'treasure_room' and 'rusty_key' not in game_state['player_inventory']:
            print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
            return False
        if next_room == 'treasure_room' and 'rusty_key' in game_state['player_inventory']:
            game_state['player_inventory'].remove('rusty_key')
            print("Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.")
        game_state['current_room'] = room['exits'][direction]
        game_state['steps_taken']+=1
        describe_current_room(game_state)
        random_event(game_state)
    else:
        print("Нельзя пойти в этом направлении.")

def take_item(game_state, item_name):
    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]

    if item_name == 'treasure_chest':
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return False

    if room['puzzle'] is not None:
        print("Вы не можете взять предметы здесь, пока не решите загадку.")
        return False

    if item_name in room['items']:
        game_state['player_inventory'].append(item_name)
        room['items'].remove(item_name)
        print("Вы подняли: ", item_name)
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state, item_name):
    if item_name == 'treasure_key' and game_state['current_room'] == 'treasure_room':
        from utils import attempt_open_treasure
        attempt_open_treasure(game_state)
        return True
    inventory = game_state['player_inventory']
    if item_name in inventory:
        match item_name:
            case 'torch':
                print("стало светлее")
            case 'sword':
                print("вы чувствуете себя увереннее")
            case 'bronze_box':
                print("вы открыли шкатулку")
                if 'rusty_key' in inventory:
                    pass
                else:
                    inventory.append('rusty_key')
                    print("подобран rusty_key")
                    inventory.remove('bronze_box')
            case _:
                print("вы не знаете как это использовать")
    else:
        print("У вас нет такого предмета")
