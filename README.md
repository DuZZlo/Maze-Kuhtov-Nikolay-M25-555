# Maze-Kuhtov-Nikolay-M25-555

"Лабиринт Сокровищ" - это классическая текстовая RPG-игра, написанная на Python, где игрок исследует таинственный лабиринт в поисках легендарных сокровищ. Проект демонстрирует лучшие практики программирования, включая модульную архитектуру, обработку состояний и детерминированную случайность.

Требования:
Python 3.8+
Poetry

Установка:
# Клонирование репозитория
git clone <git@github.com:DuZZlo/Maze-Kuhtov-Nikolay-M25-555.git>
cd labyrinth-game

# Установка зависимостей
poetry install
или
make install

# Запуск игры
poetry run project
или 
make project

### Основные команды:
go <direction>    # Движение (north/south/east/west)
look              # Осмотреть комнату
take <item>       # Поднять предмет
use <item>        # Использовать предмет
inventory         # Показать инвентарь
solve             # Решить загадку
help              # Справка по командам
quit              # Выйти из игры

## 🎥 Демонстрация игры

### Сценарий 1: Успешное прохождение
```bash
# Для просмотра локально
asciinema play gamedemo.cast
```

### Сценарий 2: Cхватка с гоблином  
```bash
asciinema play goblindemo.cast
```