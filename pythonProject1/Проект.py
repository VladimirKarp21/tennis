import sqlite3
from datetime import datetime


class TennisDatabase:
    def __init__(self, db_name='tennis.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.initialize_actual_ranking()

    def create_tables(self):
        """Создание таблиц базы данных"""
        self.cursor.execute('DROP TABLE IF EXISTS ranking_history')
        self.cursor.execute('DROP TABLE IF EXISTS matches')
        self.cursor.execute('DROP TABLE IF EXISTS tournaments')
        self.cursor.execute('DROP TABLE IF EXISTS players')

        self.cursor.execute('''
            CREATE TABLE players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                country TEXT,
                ranking INTEGER,
                ranking_points INTEGER,
                preferred_hand TEXT CHECK(preferred_hand IN ('right', 'left', 'both')),
                last_updated TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE tournaments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                surface TEXT CHECK(surface IN ('hard', 'clay', 'grass', 'carpet')),
                level TEXT CHECK(level IN ('Grand Slam', 'Masters 1000', 'ATP 500', 'ATP 250')),
                date TEXT,
                points INTEGER
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE matches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tournament_id INTEGER,
                player1_id INTEGER,
                player2_id INTEGER,
                score TEXT,
                winner_id INTEGER,
                round TEXT,
                match_date TEXT,
                FOREIGN KEY (tournament_id) REFERENCES tournaments (id),
                FOREIGN KEY (player1_id) REFERENCES players (id),
                FOREIGN KEY (player2_id) REFERENCES players (id),
                FOREIGN KEY (winner_id) REFERENCES players (id)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE ranking_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER,
                ranking INTEGER,
                ranking_points INTEGER,
                date TEXT,
                FOREIGN KEY (player_id) REFERENCES players (id)
            )
        ''')
        self.conn.commit()

    def initialize_actual_ranking(self):
        """Инициализация актуального рейтинга ATP 2025"""
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Актуальный рейтинг ATP 2025
        actual_players = [
            (1, "Испания", "Карлос Алькарас", 12050, 21, "right", current_date),
            (2, "Италия", "Янник Синнер", 11500, 23, "right", current_date),
            (3, "Германия", "Александр Зверев", 5160, 27, "right", current_date),
            (4, "Сербия", "Новак Джокович", 4830, 37, "right", current_date),
            (5, "Канада", "Феликс Оже-Альяссим", 4245, 24, "right", current_date),
            (6, "США", "Тейлор Фриц", 4135, 26, "right", current_date),
            (7, "Австралия", "Алекс де Минор", 4135, 25, "right", current_date),
            (8, "Италия", "Лоренцо Музетти", 4040, 23, "right", current_date),
            (9, "США", "Бен Шелтон", 3970, 22, "left", current_date),
            (10, "Великобритания", "Джек Дрейпер", 2990, 22, "left", current_date),
            (11, "Казахстан", "Александр Бублик", 2870, 27, "right", current_date),
            (12, "Норвегия", "Каспер Рууд", 2835, 25, "right", current_date),
            (13, "Россия", "Даниил Медведев", 2760, 28, "right", current_date),
            (14, "Испания", "Алехандро Давидович-Фокина", 2635, 25, "right", current_date),
            (15, "Дания", "Хольгер Руне", 2590, 21, "right", current_date),
            (16, "Россия", "Андрей Рублёв", 2520, 26, "right", current_date),
            (17, "Чехия", "Иржи Легечка", 2325, 24, "right", current_date),
            (18, "Россия", "Карен Хачанов", 2320, 28, "right", current_date),
            (19, "Чехия", "Якуб Меншик", 2180, 19, "right", current_date),
            (20, "США", "Томми Пол", 2100, 26, "right", current_date)
        ]

        # Добавляем игроков в базу
        for player in actual_players:
            ranking, country, name, points, age, hand, date = player
            self.cursor.execute('''
                INSERT INTO players (ranking, country, name, ranking_points, age, preferred_hand, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (ranking, country, name, points, age, hand, date))

        self.conn.commit()
        print("Актуальный рейтинг ATP 2025 успешно загружен!")

    def display_current_ranking(self, limit=20):
        """Отображение текущего рейтинга игроков"""
        print(f"\n{'=' * 70}")
        print(f"АТР РЕЙТИНГ 2025 - {datetime.now().strftime('%d.%m.%Y')}")
        print(f"{'=' * 70}")
        print(f"{'Поз.':<4} {'Игрок':<25} {'Страна':<15} {'Возр.':<5} {'Очки':<10} {'ID':<3}")
        print(f"{'-' * 70}")

        self.cursor.execute('''
            SELECT ranking, name, country, age, ranking_points, id 
            FROM players 
            WHERE ranking IS NOT NULL 
            ORDER BY ranking 
            LIMIT ?
        ''', (limit,))

        players = self.cursor.fetchall()
        for player in players:
            ranking, name, country, age, points, player_id = player
            print(f"{ranking:<4} {name:<25} {country:<15} {age:<5} {points:<10} {player_id:<3}")

    def search_player_by_name(self, name):
        """Поиск игрока по имени"""
        self.cursor.execute('''
            SELECT id, ranking, name, country, age, ranking_points, preferred_hand
            FROM players 
            WHERE name LIKE ? 
            ORDER BY ranking
        ''', (f'%{name}%',))

        players = self.cursor.fetchall()
        if players:
            print(f"\nРезультаты поиска по запросу '{name}':")
            print(f"{'ID':<3} {'Поз.':<4} {'Игрок':<25} {'Страна':<15} {'Очки':<8}")
            print(f"{'-' * 60}")
            for player in players:
                player_id, ranking, name, country, age, points, hand = player
                print(f"{player_id:<3} {ranking:<4} {name:<25} {country:<15} {points:<8}")
        else:
            print(f"Игроки по запросу '{name}' не найдены.")
        return players

    def get_players_by_country(self, country):
        """Получение игроков по стране"""
        self.cursor.execute('''
            SELECT ranking, name, age, ranking_points, id
            FROM players 
            WHERE country = ? AND ranking IS NOT NULL
            ORDER BY ranking
        ''', (country,))

        players = self.cursor.fetchall()
        if players:
            print(f"\nИгроки из {country}:")
            print(f"{'Поз.':<4} {'Игрок':<25} {'Возр.':<5} {'Очки':<8} {'ID':<3}")
            print(f"{'-' * 50}")
            for player in players:
                ranking, name, age, points, player_id = player
                print(f"{ranking:<4} {name:<25} {age:<5} {points:<8} {player_id:<3}")
        else:
            print(f"Игроки из {country} не найдены в рейтинге.")
        return players

    def get_country_stats(self):
        """Статистика по странам"""
        self.cursor.execute('''
            SELECT country, COUNT(*) as players_count, 
                   AVG(ranking_points) as avg_points,
                   MIN(ranking) as best_ranking
            FROM players 
            WHERE ranking IS NOT NULL
            GROUP BY country
            ORDER BY players_count DESC, avg_points DESC
        ''')

        stats = self.cursor.fetchall()
        print(f"\n{'=' * 50}")
        print("СТАТИСТИКА ПО СТРАНАМ")
        print(f"{'=' * 50}")
        print(f"{'Страна':<15} {'Игроков':<8} {'Ср. очки':<10} {'Лучший':<8}")
        print(f"{'-' * 50}")
        for stat in stats:
            country, count, avg_points, best_ranking = stat
            avg_points = int(avg_points) if avg_points else 0
            print(f"{country:<15} {count:<8} {avg_points:<10} {best_ranking:<8}")

    def update_player_ranking(self, player_id, new_ranking, new_points):
        """Обновление рейтинга игрока"""
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Сохраняем историю рейтинга
        self.cursor.execute('''
            INSERT INTO ranking_history (player_id, ranking, ranking_points, date)
            SELECT id, ranking, ranking_points, ? FROM players WHERE id = ?
        ''', (current_date, player_id))

        # Обновляем текущий рейтинг
        self.cursor.execute('''
            UPDATE players 
            SET ranking = ?, ranking_points = ?, last_updated = ?
            WHERE id = ?
        ''', (new_ranking, new_points, current_date, player_id))

        self.conn.commit()
        print(f"Рейтинг игрока обновлен.")

    def add_new_player(self, name, age, country, points=0, preferred_hand='right'):
        """Добавление нового игрока"""
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Определяем следующий доступный рейтинг
        self.cursor.execute('SELECT MAX(ranking) FROM players WHERE ranking IS NOT NULL')
        max_ranking = self.cursor.fetchone()[0]
        new_ranking = max_ranking + 1 if max_ranking else 21

        self.cursor.execute('''
            INSERT INTO players (name, age, country, ranking, ranking_points, preferred_hand, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, age, country, new_ranking, points, preferred_hand, current_date))

        self.conn.commit()
        print(f"Игрок {name} добавлен в базу с рейтингом {new_ranking}.")

    def get_ranking_history(self, player_id):
        """Получение истории рейтинга игрока"""
        self.cursor.execute('''
            SELECT date, ranking, ranking_points 
            FROM ranking_history 
            WHERE player_id = ? 
            ORDER BY date DESC
        ''', (player_id,))

        history = self.cursor.fetchall()
        if history:
            player_name = self.cursor.execute('SELECT name FROM players WHERE id = ?', (player_id,)).fetchone()[0]
            print(f"\nИстория рейтинга: {player_name}")
            print(f"{'Дата':<12} {'Поз.':<4} {'Очки':<8}")
            print(f"{'-' * 30}")
            for record in history:
                date, ranking, points = record
                print(f"{date:<12} {ranking:<4} {points:<8}")
        else:
            print("История рейтинга не найдена.")
        return history

    def get_top_players_by_points(self, limit=5):
        """Топ игроков по количеству очков"""
        self.cursor.execute('''
            SELECT name, country, ranking_points, ranking
            FROM players 
            ORDER BY ranking_points DESC 
            LIMIT ?
        ''', (limit,))

        players = self.cursor.fetchall()
        print(f"\nТОП-{limit} ИГРОКОВ ПО ОЧКАМ:")
        print(f"{'Игрок':<25} {'Страна':<15} {'Очки':<8} {'Поз.':<4}")
        print(f"{'-' * 55}")
        for player in players:
            name, country, points, ranking = player
            print(f"{name:<25} {country:<15} {points:<8} {ranking:<4}")

    def __del__(self):
        """Закрытие соединения с базой данных"""
        self.conn.close()


# Пример использования
def main():
    try:
        db = TennisDatabase()

        while True:
            print(f"\n{'=' * 50}")
            print("ИНФОРМАЦИОННО-АНАЛИТИЧЕСКАЯ СИСТЕМА ПО ТЕННИСУ")
            print("           АКТУАЛЬНЫЙ РЕЙТИНГ ATP 2025")
            print(f"{'=' * 50}")
            print("1. Показать текущий рейтинг ATP")
            print("2. Поиск игрока по имени")
            print("3. Игроки по стране")
            print("4. Статистика по странам")
            print("5. Топ игроков по очкам")
            print("6. Добавить нового игрока")
            print("7. История рейтинга игрока")
            print("8. Обновить рейтинг игрока")
            print("9. Выход")

            choice = input("\nВыберите опцию (1-9): ")

            if choice == '1':
                limit = input("Сколько игроков показать (по умолчанию 20): ")
                limit = int(limit) if limit.isdigit() else 20
                db.display_current_ranking(limit)

            elif choice == '2':
                name = input("Введите имя игрока для поиска: ")
                db.search_player_by_name(name)

            elif choice == '3':
                country = input("Введите страну: ")
                db.get_players_by_country(country)

            elif choice == '4':
                db.get_country_stats()

            elif choice == '5':
                limit = input("Сколько игроков показать (по умолчанию 5): ")
                limit = int(limit) if limit.isdigit() else 5
                db.get_top_players_by_points(limit)

            elif choice == '6':
                name = input("Имя: ")
                age = input("Возраст: ")
                country = input("Страна: ")
                points = input("Очки рейтинга (по умолчанию 0): ")
                points = int(points) if points.isdigit() else 0
                hand = input("Ведущая рука (right/left/both, по умолчанию right): ") or "right"
                db.add_new_player(name, int(age), country, points, hand)

            elif choice == '7':
                name = input("Введите имя игрока: ")
                players = db.search_player_by_name(name)
                if players:
                    player_id = input("Введите ID игрока для просмотра истории: ")
                    if player_id.isdigit():
                        db.get_ranking_history(int(player_id))

            elif choice == '8':
                player_id = input("Введите ID игрока: ")
                new_ranking = input("Новый рейтинг: ")
                new_points = input("Новые очки: ")
                if player_id.isdigit() and new_ranking.isdigit() and new_points.isdigit():
                    db.update_player_ranking(int(player_id), int(new_ranking), int(new_points))
                else:
                    print("Ошибка: введите корректные числовые значения.")

            elif choice == '9':
                print("Выход из системы...")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()