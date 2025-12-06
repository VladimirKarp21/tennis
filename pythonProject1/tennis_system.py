import sqlite3
import hashlib
from datetime import datetime
import random

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
            
            # Таблица игроков
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    player_hash TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INTEGER,
                    country TEXT,
                    ranking INTEGER,
                    ranking_points INTEGER,
                    height_cm INTEGER,
                    weight_kg INTEGER,
                    preferred_hand TEXT,
                    play_style TEXT,
                    last_updated TEXT
                )
            ''')
            
            # Таблица покрытий
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS surface_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_hash TEXT,
                    surface_type TEXT CHECK(surface_type IN ('hard', 'clay', 'grass', 'carpet')),
                    win_rate REAL,
                    matches_played INTEGER,
                    points_won_percentage REAL,
                    FOREIGN KEY (player_hash) REFERENCES players (player_hash)
                )
            ''')
            
            # Таблица погодных условий
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS weather_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_hash TEXT,
                    weather_type TEXT CHECK(weather_type IN ('sunny', 'rainy', 'windy', 'indoor', 'hot', 'cold')),
                    win_rate REAL,
                    matches_played INTEGER,
                    FOREIGN KEY (player_hash) REFERENCES players (player_hash)
                )
            ''')
            
            # Таблица матчей
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS matches (
                    match_id TEXT PRIMARY KEY,
                    player1_hash TEXT,
                    player2_hash TEXT,
                    surface TEXT,
                    weather TEXT,
                    temperature INTEGER,
                    humidity INTEGER,
                    winner_hash TEXT,
                    score TEXT,
                    match_date TEXT,
                    tournament TEXT
                )
            ''')
            
            conn.commit()

    # === МЕТОДЫ ДЛЯ ИГРОКОВ ===
    def generate_player_hash(self, name, country, age=None):
        base_string = f"{name}_{country}_{age if age else ''}"
        return hashlib.md5(base_string.encode()).hexdigest()

    def add_player_with_stats(self, player_data):
        """Добавление игрока со статистикой по покрытиям и погоде"""
        player_hash = self.generate_player_hash(
            player_data['name'], 
            player_data['country'],
            player_data.get('age')
        )
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Добавляем игрока
                cursor.execute('''
                    INSERT OR REPLACE INTO players 
                    (player_hash, name, age, country, ranking, ranking_points, 
                     height_cm, weight_kg, preferred_hand, play_style, last_updated)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    player_hash,
                    player_data['name'],
                    player_data.get('age'),
                    player_data['country'],
                    player_data.get('ranking'),
                    player_data.get('ranking_points', 0),
                    player_data.get('height_cm'),
                    player_data.get('weight_kg'),
                    player_data.get('preferred_hand', 'right'),
                    player_data.get('play_style', 'all_court'),
                    datetime.now().strftime("%Y-%m-%d")
                ))
                
                # Генерируем статистику по покрытиям
                surfaces = ['hard', 'clay', 'grass']
                for surface in surfaces:
                    win_rate = random.uniform(0.4, 0.8)
                    matches = random.randint(10, 50)
                    points_won = random.uniform(0.45, 0.55)
                    
                    cursor.execute('''
                        INSERT INTO surface_stats 
                        (player_hash, surface_type, win_rate, matches_played, points_won_percentage)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (player_hash, surface, win_rate, matches, points_won))
                
                # Генерируем статистику по погоде
                weather_types = ['sunny', 'rainy', 'windy', 'indoor']
                for weather in weather_types:
                    win_rate = random.uniform(0.4, 0.8)
                    matches = random.randint(5, 30)
                    
                    cursor.execute('''
                        INSERT INTO weather_stats 
                        (player_hash, weather_type, win_rate, matches_played)
                        VALUES (?, ?, ?, ?)
                    ''', (player_hash, weather, win_rate, matches))
                
                conn.commit()
                return True
        except Exception as e:
            print(f"Ошибка: {e}")
            return False

    # === МЕТОДЫ ДЛЯ ПОКРЫТИЙ ===
    def get_surface_stats(self, player_hash):
        """Получить статистику по покрытиям для игрока"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT surface_type, win_rate, matches_played, points_won_percentage
                FROM surface_stats 
                WHERE player_hash = ?
                ORDER BY win_rate DESC
            ''', (player_hash,))
            return cursor.fetchall()

    def get_best_surface(self, player_hash):
        """Получить лучшее покрытие для игрока"""
        stats = self.get_surface_stats(player_hash)
        if stats:
            return max(stats, key=lambda x: x[1])
        return None

    def compare_players_on_surface(self, player1_hash, player2_hash, surface):
        """Сравнить двух игроков на конкретном покрытии"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT win_rate FROM surface_stats 
                WHERE player_hash = ? AND surface_type = ?
            ''', (player1_hash, surface))
            player1 = cursor.fetchone()
            
            cursor.execute('''
                SELECT win_rate FROM surface_stats 
                WHERE player_hash = ? AND surface_type = ?
            ''', (player2_hash, surface))
            player2 = cursor.fetchone()
            
            if player1 and player2:
                return {
                    'player1_win_rate': player1[0],
                    'player2_win_rate': player2[0],
                    'advantage': player1[0] - player2[0]
                }
            return None

    # === МЕТОДЫ ДЛЯ ПОГОДЫ ===
    def get_weather_stats(self, player_hash):
        """Получить статистику по погоде для игрока"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT weather_type, win_rate, matches_played
                FROM weather_stats 
                WHERE player_hash = ?
                ORDER BY win_rate DESC
            ''', (player_hash,))
            return cursor.fetchall()

    def get_best_weather(self, player_hash):
        """Получить лучшие погодные условия для игрока"""
        stats = self.get_weather_stats(player_hash)
        if stats:
            return max(stats, key=lambda x: x[1])
        return None

    def compare_players_in_weather(self, player1_hash, player2_hash, weather):
        """Сравнить двух игроков в конкретных погодных условиях"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT win_rate FROM weather_stats 
                WHERE player_hash = ? AND weather_type = ?
            ''', (player1_hash, weather))
            player1 = cursor.fetchone()
            
            cursor.execute('''
                SELECT win_rate FROM weather_stats 
                WHERE player_hash = ? AND weather_type = ?
            ''', (player2_hash, weather))
            player2 = cursor.fetchone()
            
            if player1 and player2:
                return {
                    'player1_win_rate': player1[0],
                    'player2_win_rate': player2[0],
                    'advantage': player1[0] - player2[0]
                }
            return None

    # === МЕТОДЫ ДЛЯ МАТЧЕЙ ===
    def add_match_result(self, match_data):
        """Добавить результат матча"""
        match_id = hashlib.md5(
            f"{match_data['player1_hash']}_{match_data['player2_hash']}_{match_data['match_date']}".encode()
        ).hexdigest()
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO matches 
                (match_id, player1_hash, player2_hash, surface, weather, temperature, 
                 humidity, winner_hash, score, match_date, tournament)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                match_id,
                match_data['player1_hash'],
                match_data['player2_hash'],
                match_data.get('surface', 'hard'),
                match_data.get('weather', 'sunny'),
                match_data.get('temperature', 20),
                match_data.get('humidity', 50),
                match_data['winner_hash'],
                match_data.get('score', '6-4 6-4'),
                match_data['match_date'],
                match_data.get('tournament', 'Unknown')
            ))
            conn.commit()
        return match_id

    # === ПРОГНОЗИРОВАНИЕ ===
    def predict_match(self, player1_hash, player2_hash, surface, weather, temperature=20):
        """Прогноз результата матча с учетом условий"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Получаем базовые рейтинги
            cursor.execute('SELECT ranking_points FROM players WHERE player_hash IN (?, ?)', 
                          (player1_hash, player2_hash))
            points = cursor.fetchall()
            
            if len(points) != 2:
                return None
            
            base_prob = points[0][0] / (points[0][0] + points[1][0])
            
            # Корректировка на покрытие
            surface_stats = self.compare_players_on_surface(player1_hash, player2_hash, surface)
            if surface_stats:
                base_prob += surface_stats['advantage'] * 0.2
            
            # Корректировка на погоду
            weather_stats = self.compare_players_in_weather(player1_hash, player2_hash, weather)
            if weather_stats:
                base_prob += weather_stats['advantage'] * 0.15
            
            # Корректировка на температуру
            if temperature > 30:  # Очень жарко
                base_prob += 0.05
            elif temperature < 10:  # Очень холодно
                base_prob -= 0.05
            
            # Ограничиваем вероятность
            final_prob = max(0.1, min(0.9, base_prob))
            
            return {
                'player1_probability': final_prob,
                'player2_probability': 1 - final_prob,
                'recommended_bet': 'player1' if final_prob > 0.5 else 'player2',
                'confidence': abs(final_prob - 0.5) * 2
            }

    # === СТАТИСТИКА ===
    def get_top_players_by_surface(self, surface, limit=10):
        """Лучшие игроки на конкретном покрытии"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.name, p.country, s.win_rate, s.matches_played
                FROM surface_stats s
                JOIN players p ON s.player_hash = p.player_hash
                WHERE s.surface_type = ? AND s.matches_played >= 10
                ORDER BY s.win_rate DESC
                LIMIT ?
            ''', (surface, limit))
            return cursor.fetchall()

    def get_top_players_by_weather(self, weather, limit=10):
        """Лучшие игроки в конкретных погодных условиях"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.name, p.country, w.win_rate, w.matches_played
                FROM weather_stats w
                JOIN players p ON w.player_hash = p.player_hash
                WHERE w.weather_type = ? AND w.matches_played >= 5
                ORDER BY w.win_rate DESC
                LIMIT ?
            ''', (weather, limit))
            return cursor.fetchall()

    # === БАЗОВЫЕ МЕТОДЫ ===
    def get_all_players(self, limit=None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if limit:
                cursor.execute('SELECT * FROM players ORDER BY ranking LIMIT ?', (limit,))
            else:
                cursor.execute('SELECT * FROM players ORDER BY ranking')
            return cursor.fetchall()

    def search_players_by_name(self, name):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM players 
                WHERE name LIKE ? 
                ORDER BY ranking
            ''', (f'%{name}%',))
            return cursor.fetchall()

    def get_players_count(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM players')
            return cursor.fetchone()[0]

# === ИНТЕРФЕЙС ===
class TennisAnalyticsSystem:
    def __init__(self):
        self.db = TennisDatabase()
        self.init_sample_data()
    
    def init_sample_data(self):
        """Инициализация демо-данных"""
        if self.db.get_players_count() == 0:
            print("Создание демо-данных...")
            self.create_demo_players()
    
    def create_demo_players(self):
        """Создание демонстрационных игроков"""
        demo_players = [
            {
                'name': 'Карлос Алькарас', 'country': 'Испания', 'age': 21,
                'ranking': 1, 'ranking_points': 12050,
                'height_cm': 183, 'weight_kg': 74,
                'play_style': 'aggressive_baseliner',
                'preferred_hand': 'right'
            },
            {
                'name': 'Новак Джокович', 'country': 'Сербия', 'age': 37,
                'ranking': 4, 'ranking_points': 4830,
                'height_cm': 188, 'weight_kg': 77,
                'play_style': 'all_court',
                'preferred_hand': 'right'
            },
            {
                'name': 'Рафаэль Надаль', 'country': 'Испания', 'age': 38,
                'ranking': 44, 'ranking_points': 1180,
                'height_cm': 185, 'weight_kg': 85,
                'play_style': 'clay_specialist',
                'preferred_hand': 'left'
            },
            {
                'name': 'Даниил Медведев', 'country': 'Россия', 'age': 28,
                'ranking': 13, 'ranking_points': 2760,
                'height_cm': 198, 'weight_kg': 83,
                'play_style': 'defensive_baseliner',
                'preferred_hand': 'right'
            },
            {
                'name': 'Янник Синнер', 'country': 'Италия', 'age': 23,
                'ranking': 2, 'ranking_points': 11500,
                'height_cm': 188, 'weight_kg': 76,
                'play_style': 'power_baseliner',
                'preferred_hand': 'right'
            }
        ]
        
        for player in demo_players:
            self.db.add_player_with_stats(player)
        
        print(f"Создано {len(demo_players)} демо-игроков")
    
    def display_player_analysis(self):
        """Анализ конкретного игрока"""
        name = input("Введите имя игрока: ")
        players = self.db.search_players_by_name(name)
        
        if not players:
            print("Игрок не найден")
            return
        
        player = players[0]
        player_hash = player[0]
        
        print(f"\n{'='*60}")
        print(f"АНАЛИЗ ИГРОКА: {player[1]}")
        print(f"{'='*60}")
        
        # Статистика по покрытиям
        print("\n📊 СТАТИСТИКА ПО ПОКРЫТИЯМ:")
        surface_stats = self.db.get_surface_stats(player_hash)
        for surface, win_rate, matches, points in surface_stats:
            print(f"  {surface.upper():<6} | Побед: {win_rate:.1%} | Матчи: {matches}")
        
        # Статистика по погоде
        print("\n🌤️ СТАТИСТИКА ПО ПОГОДЕ:")
        weather_stats = self.db.get_weather_stats(player_hash)
        for weather, win_rate, matches in weather_stats:
            print(f"  {weather.upper():<8} | Побед: {win_rate:.1%} | Матчи: {matches}")
    
    def predict_match_menu(self):
        """Прогноз матча"""
        print("\n🎾 ПРОГНОЗ МАТЧА")
        print("-" * 40)
        
        name1 = input("Игрок 1: ")
        name2 = input("Игрок 2: ")
        surface = input("Покрытие [hard/clay/grass]: ").lower() or 'hard'
        weather = input("Погода [sunny/rainy/windy]: ").lower() or 'sunny'
        temp = input("Температура [20]: ") or '20'
        
        players1 = self.db.search_players_by_name(name1)
        players2 = self.db.search_players_by_name(name2)
        
        if not players1 or not players2:
            print("Игроки не найдены")
            return
        
        prediction = self.db.predict_match(
            players1[0][0], players2[0][0], surface, weather, int(temp)
        )
        
        if prediction:
            print(f"\n{'='*50}")
            print("РЕЗУЛЬТАТ ПРОГНОЗА:")
            print(f"{'='*50}")
            print(f"{players1[0][1]}: {prediction['player1_probability']:.1%}")
            print(f"{players2[0][1]}: {prediction['player2_probability']:.1%}")
            print(f"\n🎯 РЕКОМЕНДАЦИЯ: {prediction['recommended_bet'].upper()}")
            print(f"📈 УВЕРЕННОСТЬ: {prediction['confidence']:.1%}")
    
    def show_surface_masters(self):
        """Показать мастеров покрытий"""
        surface = input("Покрытие [hard/clay/grass]: ").lower() or 'hard'
        masters = self.db.get_top_players_by_surface(surface)
        
        print(f"\n{'='*60}")
        print(f"МАСТЕРА {surface.upper()}")
        print(f"{'='*60}")
        for name, country, win_rate, matches in masters:
            print(f"{name:<20} {country:<15} {win_rate:.1%} ({matches} матчей)")
    
    def show_ranking(self):
        """Показать рейтинг"""
        players = self.db.get_all_players(limit=20)
        
        print(f"\n{'='*70}")
        print(f"АТП РЕЙТИНГ")
        print(f"{'='*70}")
        print(f"{'Поз.':<4} {'Игрок':<20} {'Страна':<15} {'Очки':<10}")
        print(f"{'-'*70}")
        
        for player in players:
            print(f"{player[4]:<4} {player[1]:<20} {player[3]:<15} {player[5]:<10}")
    
    def run(self):
        """Запуск системы"""
        menu_items = {
            '1': {'name': 'Показать рейтинг ATP', 'func': self.show_ranking},
            '2': {'name': 'Анализ игрока (покрытия + погода)', 'func': self.display_player_analysis},
            '3': {'name': 'Прогноз матча', 'func': self.predict_match_menu},
            '4': {'name': 'Мастера покрытий', 'func': self.show_surface_masters},
            '5': {'name': 'Выход', 'func': None}
        }
        
        while True:
            print(f"\n{'='*50}")
            print("🎾 ТЕННИСНАЯ АНАЛИТИЧЕСКАЯ СИСТЕМА")
            print("   с учетом погоды и покрытий")
            print(f"{'='*50}")
            
            for key, item in menu_items.items():
                print(f"{key}. {item['name']}")
            
            choice = input("\nВыберите опцию: ")
            
            if choice == '5':
                print("Выход из системы...")
                break
            elif choice in menu_items and menu_items[choice]['func']:
                menu_items[choice]['func']()
            else:
                print("Неверный выбор. Попробуйте снова.")

# === ЗАПУСК ===
if __name__ == "__main__":
    print("🎾 Теннисная аналитическая система")
    print("Загрузка...")
    system = TennisAnalyticsSystem()
    system.run()
