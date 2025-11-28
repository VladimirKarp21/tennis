import sqlite3
import hashlib
from datetime import datetime


# === КЛАСС БАЗЫ ДАННЫХ ===
class TennisDatabase:
    def __init__(self, db_name='tennis.db'):
        self.db_name = db_name
        self.init_database()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def init_database(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    player_hash TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INTEGER,
                    country TEXT,
                    ranking INTEGER,
                    ranking_points INTEGER,
                    preferred_hand TEXT,
                    last_updated TEXT
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ranking_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_hash TEXT,
                    ranking INTEGER,
                    ranking_points INTEGER,
                    date TEXT,
                    FOREIGN KEY (player_hash) REFERENCES players (player_hash)
                )
            ''')

            conn.commit()

    def generate_player_hash(self, name, country, birth_year=None):
        base_string = f"{name}_{country}_{birth_year if birth_year else ''}"
        return hashlib.md5(base_string.encode()).hexdigest()

    def player_exists(self, player_hash):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 1 FROM players WHERE player_hash = ?', (player_hash,))
            return cursor.fetchone() is not None

    def add_player(self, player_data):
        player_hash = self.generate_player_hash(
            player_data['name'],
            player_data['country'],
            player_data.get('birth_year')
        )

        if self.player_exists(player_hash):
            return False

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO players 
                (player_hash, name, age, country, ranking, ranking_points, preferred_hand, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                player_hash,
                player_data['name'],
                player_data.get('age'),
                player_data['country'],
                player_data.get('ranking'),
                player_data.get('ranking_points', 0),
                player_data.get('preferred_hand', 'right'),
                datetime.now().strftime("%Y-%m-%d")
            ))
            conn.commit()
            return True

    def get_all_players(self, limit=None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if limit:
                cursor.execute('SELECT * FROM players ORDER BY ranking LIMIT ?', (limit,))
            else:
                cursor.execute('SELECT * FROM players ORDER BY ranking')
            return cursor.fetchall()

    def get_players_count(self):
        """Получить общее количество игроков в базе"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM players')
            return cursor.fetchone()[0]

    def search_players_by_name(self, name):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM players 
                WHERE name LIKE ? 
                ORDER BY ranking
            ''', (f'%{name}%',))
            return cursor.fetchall()

    def get_players_by_country(self, country):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM players 
                WHERE country = ? 
                ORDER BY ranking
            ''', (country,))
            return cursor.fetchall()

    def get_country_stats(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT country, COUNT(*) as players_count, 
                       AVG(ranking_points) as avg_points,
                       MIN(ranking) as best_ranking
                FROM players 
                WHERE ranking IS NOT NULL
                GROUP BY country
                ORDER BY players_count DESC, avg_points DESC
            ''')
            return cursor.fetchall()


# === ЗАГРУЗКА ДАННЫХ ===
def load_initial_data(db):
    all_players = [
        {"ranking": 1, "country": "Испания", "name": "Карлос Алькарас", "ranking_points": 12050, "age": 21},
        {"ranking": 2, "country": "Италия", "name": "Янник Синнер", "ranking_points": 11500, "age": 23},
        {"ranking": 3, "country": "Германия", "name": "Александр Зверев", "ranking_points": 5160, "age": 27},
        {"ranking": 4, "country": "Сербия", "name": "Новак Джокович", "ranking_points": 4830, "age": 37},
        {"ranking": 5, "country": "Канада", "name": "Феликс Оже-Альяссим", "ranking_points": 4245, "age": 24},
        {"ranking": 6, "country": "США", "name": "Тейлор Фриц", "ranking_points": 4135, "age": 26},
        {"ranking": 7, "country": "Австралия", "name": "Алекс де Минор", "ranking_points": 4135, "age": 25},
        {"ranking": 8, "country": "Италия", "name": "Лоренцо Музетти", "ranking_points": 4040, "age": 23},
        {"ranking": 9, "country": "США", "name": "Бен Шелтон", "ranking_points": 3970, "age": 22,
         "preferred_hand": "left"},
        {"ranking": 10, "country": "Великобритания", "name": "Джек Дрейпер", "ranking_points": 2990, "age": 22,
         "preferred_hand": "left"},
        {"ranking": 11, "country": "Казахстан", "name": "Александр Бублик", "ranking_points": 2870, "age": 27},
        {"ranking": 12, "country": "Норвегия", "name": "Каспер Рууд", "ranking_points": 2835, "age": 25},
        {"ranking": 13, "country": "Россия", "name": "Даниил Медведев", "ranking_points": 2760, "age": 28},
        {"ranking": 14, "country": "Испания", "name": "Алехандро Давидович-Фокина", "ranking_points": 2635, "age": 25},
        {"ranking": 15, "country": "Дания", "name": "Хольгер Руне", "ranking_points": 2590, "age": 21},
        {"ranking": 16, "country": "Россия", "name": "Андрей Рублёв", "ranking_points": 2520, "age": 26},
        {"ranking": 17, "country": "Чехия", "name": "Иржи Легечка", "ranking_points": 2325, "age": 24},
        {"ranking": 18, "country": "Россия", "name": "Карен Хачанов", "ranking_points": 2320, "age": 28},
        {"ranking": 19, "country": "Чехия", "name": "Якуб Меншик", "ranking_points": 2180, "age": 19},
        {"ranking": 20, "country": "США", "name": "Томми Пол", "ranking_points": 2100, "age": 26},
        {"ranking": 21, "country": "Аргентина", "name": "Франсиско Серундоло", "ranking_points": 2085, "age": 25},
        {"ranking": 22, "country": "Италия", "name": "Флавио Коболли", "ranking_points": 2025, "age": 22},
        {"ranking": 23, "country": "Канада", "name": "Денис Шаповалов", "ranking_points": 1675, "age": 25},
        {"ranking": 24, "country": "Бразилия", "name": "Жоао Фонсека", "ranking_points": 1635, "age": 19},
        {"ranking": 25, "country": "Нидерланды", "name": "Таллон Грикспор", "ranking_points": 1615, "age": 23},
        {"ranking": 26, "country": "Италия", "name": "Лучано Дардери", "ranking_points": 1609, "age": 21},
        {"ranking": 27, "country": "Великобритания", "name": "Кэмерон Норри", "ranking_points": 1573, "age": 28},
        {"ranking": 28, "country": "США", "name": "Лёнер Тьен", "ranking_points": 1550, "age": 21},
        {"ranking": 29, "country": "Франция", "name": "Артур Риндеркнеш", "ranking_points": 1540, "age": 23},
        {"ranking": 30, "country": "США", "name": "Фрэнсис Тиафо", "ranking_points": 1510, "age": 26},
        {"ranking": 31, "country": "Монако", "name": "Валантен Вашеро", "ranking_points": 1483, "age": 22},
        {"ranking": 32, "country": "Чехия", "name": "Томаш Махач", "ranking_points": 1445, "age": 28},
        {"ranking": 33, "country": "США", "name": "Брэндон Накашима", "ranking_points": 1430, "age": 22},
        {"ranking": 34, "country": "Греция", "name": "Стефанос Циципас", "ranking_points": 1425, "age": 25},
        {"ranking": 35, "country": "Франция", "name": "Корентен Муте", "ranking_points": 1408, "age": 27},
        {"ranking": 36, "country": "Испания", "name": "Хауме Мунар", "ranking_points": 1395, "age": 27},
        {"ranking": 37, "country": "Франция", "name": "Уго Умбер", "ranking_points": 1380, "age": 25},
        {"ranking": 38, "country": "США", "name": "Алекс Михельсен", "ranking_points": 1325, "age": 20},
        {"ranking": 39, "country": "Италия", "name": "Лоренцо Сонего", "ranking_points": 1265, "age": 28},
        {"ranking": 40, "country": "Франция", "name": "Артюр Фис", "ranking_points": 1250, "age": 22}
    ]

    added_count = 0
    for player_data in all_players:
        if db.add_player(player_data):
            added_count += 1

    return added_count


# === ИНТЕРФЕЙС ===
class TennisInterface:
    def __init__(self):
        self.db = TennisDatabase()
        self.init_data()

    def init_data(self):
        players_count = self.db.get_players_count()
        if players_count == 0:
            count = load_initial_data(self.db)
            print(f"Загружено {count} игроков в базу данных")
        else:
            print(f"В базе данных уже есть {players_count} игроков")

    def display_ranking(self):
        """Показать рейтинг с выбором количества игроков"""
        players_count = self.db.get_players_count()
        print(f"\nВ базе данных: {players_count} игроков")

        limit_input = input("Сколько игроков показать (по умолчанию все): ")
        if limit_input.isdigit():
            limit = int(limit_input)
        else:
            limit = None  # Показать всех

        players = self.db.get_all_players(limit=limit)

        print(f"\n{'=' * 70}")
        print(f"АТР РЕЙТИНГ 2025 - {datetime.now().strftime('%d.%m.%Y')}")
        print(f"Показано игроков: {len(players)} из {players_count}")
        print(f"{'=' * 70}")
        print(f"{'Поз.':<4} {'Игрок':<25} {'Страна':<15} {'Возр.':<5} {'Очки':<10}")
        print(f"{'-' * 70}")

        for player in players:
            player_hash, name, age, country, ranking, points, hand, updated = player
            print(f"{ranking:<4} {name:<25} {country:<15} {age:<5} {points:<10}")

    def display_full_ranking(self):
        """Показать полный рейтинг (всех игроков)"""
        players = self.db.get_all_players()  # Без лимита - все игроки
        players_count = len(players)

        print(f"\n{'=' * 70}")
        print(f"ПОЛНЫЙ АТР РЕЙТИНГ 2025 - {datetime.now().strftime('%d.%m.%Y')}")
        print(f"Всего игроков: {players_count}")
        print(f"{'=' * 70}")
        print(f"{'Поз.':<4} {'Игрок':<25} {'Страна':<15} {'Возр.':<5} {'Очки':<10}")
        print(f"{'-' * 70}")

        for player in players:
            player_hash, name, age, country, ranking, points, hand, updated = player
            print(f"{ranking:<4} {name:<25} {country:<15} {age:<5} {points:<10}")

    def display_top_ranking(self):
        """Показать топ игроков"""
        limit_input = input("Показать топ-N игроков (по умолчанию 20): ")
        limit = int(limit_input) if limit_input.isdigit() else 20

        players = self.db.get_all_players(limit=limit)

        print(f"\n{'=' * 70}")
        print(f"ТОП-{limit} АТР РЕЙТИНГ 2025 - {datetime.now().strftime('%d.%m.%Y')}")
        print(f"{'=' * 70}")
        print(f"{'Поз.':<4} {'Игрок':<25} {'Страна':<15} {'Возр.':<5} {'Очки':<10}")
        print(f"{'-' * 70}")

        for player in players:
            player_hash, name, age, country, ranking, points, hand, updated = player
            print(f"{ranking:<4} {name:<25} {country:<15} {age:<5} {points:<10}")

    def search_player(self):
        name = input("Введите имя игрока для поиска: ")
        players = self.db.search_players_by_name(name)

        if players:
            print(f"\nНайдено {len(players)} игроков:")
            print(f"{'Поз.':<4} {'Игрок':<25} {'Страна':<15} {'Очки':<8}")
            print(f"{'-' * 60}")
            for player in players:
                player_hash, name, age, country, ranking, points, hand, updated = player
                print(f"{ranking:<4} {name:<25} {country:<15} {points:<8}")
        else:
            print("Игроки не найдены")

    def show_country_players(self):
        country = input("Введите страну: ")
        players = self.db.get_players_by_country(country)

        if players:
            print(f"\nИгроки из {country} (всего {len(players)}):")
            print(f"{'Поз.':<4} {'Игрок':<25} {'Возр.':<5} {'Очки':<8}")
            print(f"{'-' * 50}")
            for player in players:
                player_hash, name, age, country, ranking, points, hand, updated = player
                print(f"{ranking:<4} {name:<25} {age:<5} {points:<8}")
        else:
            print(f"Игроки из {country} не найдены")

    def show_country_stats(self):
        stats = self.db.get_country_stats()

        print(f"\n{'=' * 50}")
        print("СТАТИСТИКА ПО СТРАНАМ")
        print(f"{'=' * 50}")
        print(f"{'Страна':<15} {'Игроков':<8} {'Ср. очки':<10} {'Лучший':<8}")
        print(f"{'-' * 50}")
        for stat in stats:
            country, count, avg_points, best_ranking = stat
            avg_points = int(avg_points) if avg_points else 0
            print(f"{country:<15} {count:<8} {avg_points:<10} {best_ranking:<8}")

    def run(self):
        menu_items = {
            '1': {'name': 'Показать рейтинг (выбрать количество)', 'func': self.display_ranking},
            '2': {'name': 'Показать полный рейтинг (все игроки)', 'func': self.display_full_ranking},
            '3': {'name': 'Показать топ-N игроков', 'func': self.display_top_ranking},
            '4': {'name': 'Поиск игрока по имени', 'func': self.search_player},
            '5': {'name': 'Игроки по стране', 'func': self.show_country_players},
            '6': {'name': 'Статистика по странам', 'func': self.show_country_stats},
            '7': {'name': 'Выход', 'func': None}
        }

        while True:
            print(f"\n{'=' * 50}")
            print("ИНФОРМАЦИОННО-АНАЛИТИЧЕСКАЯ СИСТЕМА ПО ТЕННИСУ")
            print(f"{'=' * 50}")

            for key, item in menu_items.items():
                print(f"{key}. {item['name']}")

            choice = input("\nВыберите опцию: ")

            if choice == '7':
                print("Выход из системы...")
                break
            elif choice in menu_items and menu_items[choice]['func']:
                menu_items[choice]['func']()
            else:
                print("Неверный выбор. Попробуйте снова.")


# === ЗАПУСК ПРОГРАММЫ ===
if __name__ == "__main__":
    app = TennisInterface()
    app.run()