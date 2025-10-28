#!/usr/bin/env python3
from labyrinth_game.constants import COMMANDS
from labyrinth_game.player_actions import move_player, show_inventory, take_item, use_item
from labyrinth_game.utils import attempt_open_treasure, describe_current_room, get_input, show_help, solve_puzzle

game_state = {
    'player_inventory': [], # Инвентарь игрока
    'current_room': 'entrance', # Текущая комната
    'game_over': False, # Значения окончания игры
    'steps_taken': 0 # Количество шагов
}

def process_command(game_state, command):
        match command:
            case 'выход' | 'exit' | 'quit':
                print("Game over!")
                game_state['game_over'] = True
            case 'инвентарь' | 'inventory' | 'i':
                show_inventory(game_state)
            
            case 'осмотреться' | 'look':
                describe_current_room(game_state)

            case 'решить' | 'solve':
                if game_state['current_room'] == 'treasure_room':
                    attempt_open_treasure(game_state)
                else:
                    solve_puzzle(game_state)
            
            case cmd if cmd.startswith('идти ') or cmd.startswith('move ') or cmd.startswith('go '):
                direction = command.split()[1] if len(command.split()) > 1 else ''
                move_player(game_state, direction)

            case 'north' | 'south' | 'east' | 'west' as direction:
                move_player(game_state, direction)

            case cmd if cmd.startswith('поднять ') or cmd.startswith('take '):
                item = command.split()[1] if len(command.split()) > 1 else ''
                take_item(game_state, item)
            
            case cmd if cmd.startswith('использовать ') or cmd.startswith('use '):
                item = command.split()[1] if len(command.split()) > 1 else ''
                use_item(game_state, item)

            case 'помощь' | 'help':
                show_help(COMMANDS)
            
            case _:
                print("Неизвестная команда")

def main():
    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)

    while not game_state['game_over']:
        command = get_input("Введите команду: ").lower()
        process_command(game_state, command)
        



if __name__ == "__main__":
    # Этот код выполнится только при прямом запуске модуля
    main()