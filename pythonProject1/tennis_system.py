# -*- coding: utf-8 -*-
import sqlite3
import hashlib
from datetime import datetime
import random

class TennisDatabase:
    def __init__(self, db_name='tennis_atp.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        """Создание всех таблиц базы данных"""
        # Таблица игроков
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ranking INTEGER,
                name TEXT,
                country TEXT,
                points INTEGER,
                age INTEGER,
                hand TEXT
            )
        ''')
        
        # Таблица покрытий
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS surface_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER,
                surface TEXT CHECK(surface IN ('hard', 'clay', 'grass')),
                win_rate REAL,
                matches INTEGER,
                points_won REAL,
                FOREIGN KEY (player_id) REFERENCES players(id)
            )
        ''')
        
        # Таблица погоды
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER,
                weather TEXT CHECK(weather IN ('sunny', 'rainy', 'windy', 'indoor', 'hot', 'cold')),
                win_rate REAL,
                matches INTEGER,
                FOREIGN KEY (player_id) REFERENCES players(id)
            )
        ''')
        
        # Таблица турниров
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tournaments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                surface TEXT,
                location TEXT,
                level TEXT CHECK(level IN ('GS', 'Masters 1000', 'ATP 500', 'ATP 250'))
            )
        ''')
        
        self.conn.commit()
    
    def add_player_with_stats(self, ranking, name, country, points, age=None, hand='right'):
        """Добавить игрока со статистикой"""
        try:
            # Добавляем игрока
            self.cursor.execute('''
                INSERT INTO players (ranking, name, country, points, age, hand)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (ranking, name, country, points, age, hand))
            
            player_id = self.cursor.lastrowid
            
            # Генерируем статистику по покрытиям
            surfaces = ['hard', 'clay', 'grass']
            for surface in surfaces:
                # Более реалистичная статистика в зависимости от типа игрока
                if 'clay' in country.lower() or 'испания' in country.lower() or 'аргентина' in country.lower():
                    clay_bonus = 0.1 if surface == 'clay' else 0
                else:
                    clay_bonus = 0
                
                win_rate = random.uniform(0.45, 0.75) + clay_bonus
                matches = random.randint(15, 100)
                points_won = random.uniform(0.48, 0.52)
                
                self.cursor.execute('''
                    INSERT INTO surface_stats (player_id, surface, win_rate, matches, points_won)
                    VALUES (?, ?, ?, ?, ?)
                ''', (player_id, surface, win_rate, matches, points_won))
            
            # Генерируем статистику по погоде
            weather_types = ['sunny', 'rainy', 'windy', 'indoor']
            for weather in weather_types:
                # Некоторые игроки лучше в определенных условиях
                if ranking <= 10:  # Топ-10 более стабильны
                    win_rate = random.uniform(0.55, 0.80)
                else:
                    win_rate = random.uniform(0.40, 0.70)
                
                matches = random.randint(10, 60)
                
                self.cursor.execute('''
                    INSERT INTO weather_stats (player_id, weather, win_rate, matches)
                    VALUES (?, ?, ?, ?)
                ''', (player_id, weather, win_rate, matches))
            
            self.conn.commit()
            return player_id
            
        except Exception as e:
            print(f"Ошибка добавления {name}: {e}")
            return None
    
    def load_all_200_players(self):
        """Загрузить ВСЕХ 200 игроков из вашего списка"""
        print("Загрузка 200 игроков ATP рейтинга 2025...")
        
        # ВСЕ 200 ИГРОКОВ ИЗ ВАШЕГО СПИСКА
        all_players = [
            (1, "Карлос Алькарас", "Испания", 12050, 21, "right"),
            (2, "Янник Синнер", "Италия", 11500, 23, "right"),
            (3, "Александр Зверев", "Германия", 5160, 27, "right"),
            (4, "Новак Джокович", "Сербия", 4830, 37, "right"),
            (5, "Феликс Оже-Альяссим", "Канада", 4245, 24, "right"),
            (6, "Тейлор Фриц", "США", 4135, 26, "right"),
            (7, "Алекс де Минор", "Австралия", 4135, 25, "right"),
            (8, "Лоренцо Музетти", "Италия", 4040, 23, "right"),
            (9, "Бен Шелтон", "США", 3970, 22, "left"),
            (10, "Джек Дрейпер", "Великобритания", 2990, 22, "left"),
            (11, "Александр Бублик", "Казахстан", 2870, 27, "right"),
            (12, "Каспер Рууд", "Норвегия", 2835, 25, "right"),
            (13, "Даниил Медведев", "Россия", 2760, 28, "right"),
            (14, "Алехандро Давидович-Фокина", "Испания", 2635, 25, "right"),
            (15, "Хольгер Руне", "Дания", 2590, 21, "right"),
            (16, "Андрей Рублёв", "Россия", 2520, 26, "right"),
            (17, "Иржи Легечка", "Чехия", 2325, 24, "right"),
            (18, "Карен Хачанов", "Россия", 2320, 28, "right"),
            (19, "Якуб Меншик", "Чехия", 2180, 19, "right"),
            (20, "Томми Пол", "США", 2100, 26, "right"),
            (21, "Франсиско Серундоло", "Аргентина", 2085, 25, "right"),
            (22, "Флавио Коболли", "Италия", 2025, 22, "right"),
            (23, "Денис Шаповалов", "Канада", 1675, 25, "left"),
            (24, "Жоао Фонсека", "Бразилия", 1635, 19, "right"),
            (25, "Таллон Грикспор", "Нидерланды", 1615, 23, "right"),
            (26, "Лучано Дардери", "Италия", 1609, 21, "right"),
            (27, "Кэмерон Норри", "Великобритания", 1573, 28, "left"),
            (28, "Лёнер Тьен", "США", 1550, 21, "right"),
            (29, "Артур Риндеркнеш", "Франция", 1540, 23, "right"),
            (30, "Фрэнсис Тиафо", "США", 1510, 26, "right"),
            (31, "Валантен Вашеро", "Монако", 1483, 22, "right"),
            (32, "Томаш Махач", "Чехия", 1445, 28, "right"),
            (33, "Брэндон Накашима", "США", 1430, 22, "right"),
            (34, "Стефанос Циципас", "Греция", 1425, 25, "right"),
            (35, "Корентен Муте", "Франция", 1408, 27, "right"),
            (36, "Хауме Мунар", "Испания", 1395, 27, "right"),
            (37, "Уго Умбер", "Франция", 1380, 25, "right"),
            (38, "Алекс Михельсен", "США", 1325, 20, "right"),
            (39, "Лоренцо Сонего", "Италия", 1265, 28, "right"),
            (40, "Артюр Фис", "Франция", 1250, 22, "right"),
            (41, "Габриэль Диалло", "Канада", 1253, 24, "right"),
            (42, "Александр Мюллер", "Франция", 1230, 27, "right"),
            (43, "Зизу Бергс", "Болгария", 1218, 24, "right"),
            (44, "Григор Димитров", "Болгария", 1180, 33, "right"),
            (45, "Себастьян Баэс", "Аргентина", 1155, 26, "right"),
            (46, "Даниэль Альтмайер", "Германия", 1148, 26, "right"),
            (47, "Нуну Боржеш", "Португалия", 1145, 28, "right"),
            (48, "Себастьян Корда", "США", 1100, 24, "right"),
            (49, "Камило Уго Карабельи", "Аргентина", 1053, 25, "right"),
            (50, "Райлли Опелка", "США", 1026, 26, "right"),
            (51, "Фабиан Марожан", "Венгрия", 1025, 25, "right"),
            (52, "Миомир Кецманович", "Сербия", 1025, 26, "right"),
            (53, "Дженсон Бруксби", "США", 1017, 23, "right"),
            (54, "Алексей Попырин", "Австралия", 1000, 23, "right"),
            (55, "Мартон Фучович", "Венгрия", 963, 31, "right"),
            (56, "Маттео Берреттини", "Италия", 945, 28, "right"),
            (57, "Валентен Руае", "Франция", 936, 26, "right"),
            (58, "Джованни Мпетчи Перрикар", "Франция", 925, 29, "right"),
            (59, "Томас Мартин Этчеверри", "Аргентина", 920, 24, "right"),
            (60, "Александр Ковачевич", "США", 890, 25, "right"),
            (61, "Маттео Арнальди", "Италия", 883, 22, "right"),
            (62, "Камиль Майхшак", "Польша", 861, 27, "right"),
            (63, "Теренс Атман", "Франция", 855, 26, "right"),
            (64, "Маркос Гирон", "США", 855, 30, "right"),
            (65, "Дамир Джумхур", "Босния и Герцеговина", 850, 31, "right"),
            (66, "Артур Казо", "Франция", 848, 28, "right"),
            (67, "Франсиско Комесанья", "Аргентина", 845, 27, "right"),
            (68, "Гаэль Монфис", "Франция", 825, 37, "right"),
            (69, "Адриан Маннарино", "Франция", 817, 35, "right"),
            (70, "Итан Куинн", "США", 802, 20, "right"),
            (71, "Джейкоб Фирнли", "Великобритания", 787, 20, "right"),
            (72, "Мариано Навоне", "Аргентина", 785, 23, "right"),
            (73, "Хуберт Хуркач", "Польша", 775, 27, "right"),
            (74, "Маттия Беллуччи", "Италия", 766, 22, "right"),
            (75, "Марин Чилич", "Хорватия", 765, 35, "right"),
            (76, "Йеспер де Йонг", "Нидерланды", 763, 23, "right"),
            (77, "Ботик ван де Зандсхулп", "Нидерланды", 756, 27, "right"),
            (78, "Адам Уолтон", "Австралия", 740, 25, "right"),
            (79, "Филип Мисолич", "Австрия", 726, 28, "right"),
            (80, "Кристьян Гарин", "Чили", 726, 28, "right"),
            (81, "Алехандро Табило", "Чили", 721, 29, "right"),
            (82, "Александар Вукич", "Австралия", 718, 30, "right"),
            (83, "Хамад Меджедович", "Сербия", 718, 20, "right"),
            (84, "Ян-Леннард Штруфф", "Германия", 711, 33, "right"),
            (85, "Хуан-Мануэль Серундоло", "Аргентина", 710, 26, "right"),
            (86, "Джеймс Дакворт", "Австралия", 704, 32, "right"),
            (87, "Рафаэль Коллиньон", "Бельгия", 704, 24, "right"),
            (88, "Эмилио Нава", "США", 684, 25, "right"),
            (89, "Пабло Карреньо-Буста", "Испания", 681, 33, "right"),
            (90, "Элиот Спиццирри", "США", 680, 21, "right"),
            (91, "Кентен Алис", "Франция", 679, 23, "right"),
            (92, "Роберто Баутиста-Агут", "Испания", 670, 35, "right"),
            (93, "Педро Мартинес-Портеро", "Испания", 668, 27, "right"),
            (94, "Бенжамен Бонзи", "Франция", 667, 28, "right"),
            (95, "Александр Шевченко", "Казахстан", 662, 23, "right"),
            (96, "Далибор Сврчина", "Чехия", 661, 20, "right"),
            (97, "Юго Гастон", "Франция", 653, 23, "right"),
            (98, "Ласло Джере", "Сербия", 652, 27, "right"),
            (99, "Тристан Скулкейт", "Австралия", 649, 23, "right"),
            (100, "Синтаро Мочизуки", "Япония", 647, 21, "right"),
            (101, "Вит Коприва", "Чехия", 636, 21, "right"),
            (102, "Карлос Табернер", "Испания", 636, 26, "right"),
            (103, "Янник Ханфман", "Германия", 631, 32, "right"),
            (104, "Игнасио Бусе", "Перу", 627, 25, "right"),
            (105, "Роман Андрес Бурручага", "Аргентина", 615, 21, "right"),
            (106, "Тьяго Агустин Тиранте", "Аргентина", 612, 22, "right"),
            (107, "Лука Нарди", "Италия", 599, 21, "right"),
            (108, "Джордан Томпсон", "Австралия", 586, 29, "right"),
            (109, "Николоз Басилашвили", "Грузия", 573, 31, "right"),
            (110, "Йосихито Нисиока", "Япония", 566, 28, "right"),
            (111, "Томас Барриос-Вера", "Чили", 564, 27, "right"),
            (112, "Маккензи Макдональд", "США", 559, 28, "right"),
            (113, "Брендон Холт", "США", 559, 25, "right"),
            (114, "Ринки Хидзиката", "Австралия", 556, 22, "right"),
            (115, "Кристофер О'Коннелл", "Австралия", 546, 29, "right"),
            (116, "Александр Блокс", "Бельгия", 542, 23, "right"),
            (117, "Борна Чорич", "Хорватия", 538, 27, "right"),
            (118, "Патрик Кипсон", "США", 533, 24, "right"),
            (119, "Давид Гоффен", "Бельгия", 525, 34, "right"),
            (120, "Душан Лайович", "Сербия", 519, 32, "right"),
            (121, "Эльмер Мёллер", "Дания", 517, 22, "right"),
            (122, "Бу Юньчаокэтэ", "Китай", 509, 25, "right"),
            (123, "Николас Харри", "Чили", 501, 24, "right"),
            (124, "Чун Син Цен", "Китайский Тайбэй", 498, 23, "right"),
            (125, "Ян Хоински", "Великобритания", 498, 28, "right"),
            (126, "Билли Харрис", "Великобритания", 490, 24, "right"),
            (127, "Отто Виртанен", "Финляндия", 488, 27, "right"),
            (128, "Дино Прижмич", "Хорватия", 487, 24, "right"),
            (129, "Лиам Драсль", "Канада", 476, 21, "right"),
            (130, "Марко Трунгеллити", "Аргентина", 474, 31, "right"),
            (131, "Роберто Карбальес-Баэна", "Испания", 469, 31, "right"),
            (132, "Вилюс Гаубас", "Литва", 469, 20, "right"),
            (133, "Николай Будков Кьер", "Норвегия", 464, 25, "right"),
            (134, "Себастьян Офнер", "Австрия", 463, 27, "right"),
            (135, "Мартин Ландалус-Лакамбра", "Испания", 455, 27, "right"),
            (136, "Эшарги Моэ", "Тунис", 452, 26, "right"),
            (137, "Франческо Пассаро", "Италия", 449, 23, "right"),
            (138, "Кириян Жаке", "Франция", 442, 23, "right"),
            (139, "Франческо Маэстрелли", "Италия", 442, 28, "right"),
            (140, "Уго Дельен", "Боливия", 438, 26, "right"),
            (141, "Андреа Пеллегрино", "Италия", 438, 29, "right"),
            (142, "Лукаш Клейн", "Словакия", 436, 25, "right"),
            (143, "Захари Свайда", "США", 431, 26, "right"),
            (144, "Адольфо Даниэль Вальехо", "Парагвай", 431, 22, "right"),
            (145, "Юго Бланше", "Франция", 427, 23, "right"),
            (146, "Колтон Смит", "США", 424, 23, "right"),
            (147, "Со Симабукуро", "Япония", 414, 26, "right"),
            (148, "Марк Лаял", "Эстония", 413, 26, "right"),
            (149, "Титуан Дрог", "Франция", 410, 21, "right"),
            (150, "Маттео Джиганте", "Италия", 407, 22, "right"),
            (151, "Коулман Вон", "Гонконг", 406, 21, "right"),
            (152, "Жайме Фария", "Португалия", 405, 18, "right"),
            (153, "Даниэль-Элаи Галан", "Колумбия", 405, 27, "right"),
            (154, "Джулио Цеппьери", "Италия", 405, 22, "right"),
            (155, "Пьер-Юг Эрбер", "Франция", 399, 32, "right"),
            (156, "Кей Нисикори", "Япония", 397, 34, "right"),
            (157, "Стэн Вавринка", "Швейцария", 397, 39, "right"),
            (158, "Энрике Роша", "Португалия", 394, 25, "right"),
            (159, "Йосуке Ватануки", "Япония", 380, 25, "right"),
            (160, "Гуй Ден Оуден", "Нидерланды", 372, 26, "right"),
            (161, "Хуан Пабло Фикович", "Аргентина", 369, 23, "right"),
            (162, "Лука Микрут", "Хорватия", 367, 25, "right"),
            (163, "Гарол Майо", "Франция", 361, 24, "right"),
            (164, "Жомбор Пирош", "Венгрия", 353, 25, "right"),
            (165, "Даниэль Мерида-Агилар", "Испания", 353, 21, "right"),
            (166, "Люка Ван Аш", "Франция", 352, 25, "right"),
            (167, "Нишеш Басаваредди", "США", 349, 23, "right"),
            (168, "Рафаэль Ходар", "Испания", 349, 28, "right"),
            (169, "Виталий Сачко", "Украина", 349, 27, "right"),
            (170, "Николас Мехия", "Колумбия", 348, 24, "right"),
            (171, "Алекс Болт", "Австралия", 339, 31, "right"),
            (172, "Роман Сафиуллин", "Россия", 338, 26, "right"),
            (173, "Элиас Имер", "Швеция", 337, 28, "right"),
            (174, "Джей Кларк", "Великобритания", 336, 29, "right"),
            (175, "Уго Гренье", "Франция", 334, 25, "right"),
            (176, "Зденек Коларж", "Чехия", 331, 29, "right"),
            (177, "Мартин Дамм-мл.", "США", 330, 20, "right"),
            (178, "Юрий Родионов", "Австрия", 329, 24, "right"),
            (179, "Алекс Баррена", "Аргентина", 327, 27, "right"),
            (180, "Леандро Риди", "Швейцария", 326, 23, "right"),
            (181, "Тристан Бойер", "США", 326, 22, "right"),
            (182, "Дэйн Суини", "Австралия", 323, 31, "right"),
            (183, "У Ибин", "Китай", 322, 24, "right"),
            (184, "Джэйсон Каблер", "Австралия", 321, 31, "right"),
            (185, "Федерико-Агустин Гомес", "Аргентина", 319, 26, "right"),
            (186, "Бернард Томич", "Австралия", 319, 31, "right"),
            (187, "Рэи Сакамото", "Япония", 318, 22, "right"),
            (188, "Даниэль Эванс", "Великобритания", 317, 34, "right"),
            (189, "Юстин Энгель", "Германия", 316, 25, "right"),
            (190, "Жером Ким", "Швейцария", 315, 25, "right"),
            (191, "Джеймс Маккейб", "Австралия", 315, 30, "right"),
            (192, "Майкл Чжэн", "США", 315, 19, "right"),
            (193, "Артур Фери", "Великобритания", 313, 29, "right"),
            (194, "Аугуст Хольмгрен", "Дания", 312, 25, "right"),
            (195, "Стефано Травалья", "Италия", 308, 28, "right"),
            (196, "Альваро Гильен-Меса", "Эквадор", 308, 26, "right"),
            (197, "Тьяго Монтейро", "Бразилия", 304, 29, "right"),
            (198, "Даниил Глинка", "Эстония", 300, 25, "right"),
            (199, "Оливер Кроуфорд", "США", 300, 25, "right"),
            (200, "Саша Геймар-Вайенбург", "Франция", 297, 25, "right"),
        ]
        
        added = 0
        for player in all_players:
            if self.add_player_with_stats(*player):
                added += 1
                if added % 20 == 0:
                    print(f"Загружено {added} игроков...")
        
        print(f"✅ Всего загружено: {added} игроков из 200")
        return added
    
    def show_ranking(self, limit=50):
        """Показать рейтинг"""
        self.cursor.execute('SELECT ranking, name, country, points FROM players ORDER BY ranking LIMIT ?', (limit,))
        players = self.cursor.fetchall()
        
        print(f"\n{'='*70}")
        print(f"АТП РЕЙТИНГ 2025 - Топ-{limit}")
        print(f"{'='*70}")
        for player in players:
            print(f"{player[0]:3d}. {player[1]:25} {player[2]:15} {player[3]:6d}")
    
    def get_player_surface_stats(self, player_id):
        """Статистика по покрытиям"""
        self.cursor.execute('SELECT surface, win_rate, matches FROM surface_stats WHERE player_id = ? ORDER BY win_rate DESC', (player_id,))
        return self.cursor.fetchall()
    
    def get_player_weather_stats(self, player_id):
        """Статистика по погоде"""
        self.cursor.execute('SELECT weather, win_rate, matches FROM weather_stats WHERE player_id = ? ORDER BY win_rate DESC', (player_id,))
        return self.cursor.fetchall()
    
    def analyze_player(self, player_name):
        """Анализ игрока"""
        self.cursor.execute('SELECT id, name, country, ranking, points FROM players WHERE name LIKE ?', (f'%{player_name}%',))
        player = self.cursor.fetchone()
        
        if not player:
            print(f"Игрок '{player_name}' не найден")
            return
        
        player_id, name, country, ranking, points = player
        
        print(f"\n{'='*60}")
        print(f"АНАЛИЗ: {name}")
        print(f"Рейтинг: {ranking} | Страна: {country} | Очки: {points}")
        print(f"{'='*60}")
        
        # Покрытия
        print("\n📊 ПОКРЫТИЯ:")
        surfaces = self.get_player_surface_stats(player_id)
        for surface, win_rate, matches in surfaces:
            print(f"  {surface.upper():<6} | Побед: {win_rate:.1%} | Матчи: {matches}")
        
        # Погода
        print("\n🌤️ ПОГОДА:")
        weathers = self.get_player_weather_stats(player_id)
        for weather, win_rate, matches in weathers:
            print(f"  {weather.upper():<8} | Побед: {win_rate:.1%} | Матчи: {matches}")
    
    def predict_match(self, player1_name, player2_name, surface='hard', weather='sunny'):
        """Прогноз матча"""
        # Находим игроков
        self.cursor.execute('SELECT id, name, points FROM players WHERE name LIKE ?', (f'%{player1_name}%',))
        p1 = self.cursor.fetchone()
        self.cursor.execute('SELECT id, name, points FROM players WHERE name LIKE ?', (f'%{player2_name}%',))
        p2 = self.cursor.fetchone()
        
        if not p1 or not p2:
            print("Игроки не найдены")
            return
        
        p1_id, p1_name, p1_points = p1
        p2_id, p2_name, p2_points = p2
        
        print(f"\n🎾 ПРОГНОЗ: {p1_name} vs {p2_name}")
        print(f"Условия: {surface.upper()} | {weather.upper()}")
        
        # Базовая вероятность
        base_prob = p1_points / (p1_points + p2_points)
        
        # Корректировка на покрытие
        self.cursor.execute('SELECT win_rate FROM surface_stats WHERE player_id = ? AND surface = ?', (p1_id, surface))
        p1_surface = self.cursor.fetchone()
        self.cursor.execute('SELECT win_rate FROM surface_stats WHERE player_id = ? AND surface = ?', (p2_id, surface))
        p2_surface = self.cursor.fetchone()
        
        if p1_surface and p2_surface:
            base_prob += (p1_surface[0] - p2_surface[0]) * 0.3
        
        # Корректировка на погоду
        self.cursor.execute('SELECT win_rate FROM weather_stats WHERE player_id = ? AND weather = ?', (p1_id, weather))
        p1_weather = self.cursor.fetchone()
        self.cursor.execute('SELECT win_rate FROM weather_stats WHERE player_id = ? AND weather = ?', (p2_id, weather))
        p2_weather = self.cursor.fetchone()
        
        if p1_weather and p2_weather:
            base_prob += (p1_weather[0] - p2_weather[0]) * 0.2
        
        # Финальная вероятность
        final_prob = max(0.1, min(0.9, base_prob))
        
        print(f"\n{p1_name}: {final_prob:.1%}")
        print(f"{p2_name}: {1-final_prob:.1%}")
        
        if final_prob > 0.5:
            print(f"\n🎯 Ожидаемый победитель: {p1_name}")
        else:
            print(f"\n🎯 Ожидаемый победитель: {p2_name}")

    def find_similar_players(self, player_name):
        """Найти похожих игроков по стилю и статистике"""
        self.cursor.execute('SELECT id, name, country, ranking, points FROM players WHERE name LIKE ?', (f'%{player_name}%',))
        player = self.cursor.fetchone()
        
        if not player:
            print(f"Игрок '{player_name}' не найден")
            return
        
        player_id, name, country, ranking, points = player
        
        print(f"\n🔍 ПОХОЖИЕ ИГРОКИ НА {name}:")
        print(f"{'='*60}")
        
        # Ищем игроков с похожей статистикой на грунте
        self.cursor.execute('''
            SELECT p.name, p.country, p.ranking, s.win_rate 
            FROM players p
            JOIN surface_stats s ON p.id = s.player_id
            WHERE s.surface = 'clay' 
            AND p.id != ? 
            AND p.country = ?
            ORDER BY ABS(s.win_rate - (SELECT win_rate FROM surface_stats WHERE player_id = ? AND surface = 'clay'))
            LIMIT 5
        ''', (player_id, country, player_id))
        
        clay_similar = self.cursor.fetchall()
        
        if clay_similar:
            print("\n🎾 Похожие игроки на грунте:")
            for sim_player in clay_similar:
                print(f"  {sim_player[0]:20} {sim_player[1]:15} Рейтинг: {sim_player[2]} | Побед: {sim_player[3]:.1%}")
        
        # Ищем игроков с похожим рейтингом
        self.cursor.execute('''
            SELECT name, country, ranking, points 
            FROM players 
            WHERE id != ? 
            AND ranking BETWEEN ? AND ?
            ORDER BY ABS(points - ?)
            LIMIT 5
        ''', (player_id, max(1, ranking-10), min(200, ranking+10), points))
        
        ranking_similar = self.cursor.fetchall()
        
        if ranking_similar:
            print("\n📊 Игроки с похожим рейтингом:")
            for sim_player in ranking_similar:
                print(f"  {sim_player[0]:20} {sim_player[1]:15} Рейтинг: {sim_player[2]} | Очки: {sim_player[3]}")

    def get_top_players_by_surface(self, surface='hard', limit=10):
        """Получить лучших игроков на определенном покрытии"""
        print(f"\n🏆 ТОП-{limit} ИГРОКОВ НА {surface.upper()}:")
        print(f"{'='*60}")
        
        self.cursor.execute('''
            SELECT p.name, p.country, p.ranking, s.win_rate, s.matches
            FROM players p
            JOIN surface_stats s ON p.id = s.player_id
            WHERE s.surface = ?
            ORDER BY s.win_rate DESC
            LIMIT ?
        ''', (surface, limit))
        
        top_players = self.cursor.fetchall()
        
        for i, player in enumerate(top_players, 1):
            print(f"{i:2d}. {player[0]:20} {player[1]:15} Рейтинг: {player[2]:3d} | Побед: {player[3]:.1%} | Матчи: {player[4]}")
    
    def get_country_stats(self):
        """Статистика по странам"""
        print("\n🌍 СТАТИСТИКА ПО СТРАНАМ:")
        print(f"{'='*60}")
        
        self.cursor.execute('''
            SELECT country, COUNT(*) as players, 
                   AVG(ranking) as avg_ranking,
                   SUM(points) as total_points
            FROM players
            GROUP BY country
            HAVING COUNT(*) >= 2
            ORDER BY total_points DESC
            LIMIT 15
        ''')
        
        countries = self.cursor.fetchall()
        
        for country in countries:
            print(f"{country[0]:20} Игроков: {country[1]:2d} | Средний рейтинг: {country[2]:5.1f} | Очки: {country[3]:6.0f}")
    
    def search_players(self, search_term):
        """Поиск игроков по имени или стране"""
        print(f"\n🔎 РЕЗУЛЬТАТЫ ПОИСКА: '{search_term}'")
        print(f"{'='*60}")
        
        self.cursor.execute('''
            SELECT ranking, name, country, points, age
            FROM players 
            WHERE name LIKE ? OR country LIKE ?
            ORDER BY ranking
            LIMIT 20
        ''', (f'%{search_term}%', f'%{search_term}%'))
        
        results = self.cursor.fetchall()
        
        if not results:
            print("Ничего не найдено")
            return
        
        for player in results:
            print(f"{player[0]:3d}. {player[1]:25} {player[2]:15} Очки: {player[3]:6d} | Возраст: {player[4]}")
    
    def get_player_head_to_head(self, player1_name, player2_name):
        """Виртуальное противостояние игроков"""
        self.cursor.execute('SELECT id, name, points FROM players WHERE name LIKE ?', (f'%{player1_name}%',))
        p1 = self.cursor.fetchone()
        self.cursor.execute('SELECT id, name, points FROM players WHERE name LIKE ?', (f'%{player2_name}%',))
        p2 = self.cursor.fetchone()
        
        if not p1 or not p2:
            print("Игроки не найдены")
            return
        
        p1_id, p1_name, p1_points = p1
        p2_id, p2_name, p2_points = p2
        
        print(f"\n⚔️  ПРОТИВОСТОЯНИЕ: {p1_name} vs {p2_name}")
        print(f"{'='*60}")
        
        # Сравнение рейтинга
        print(f"\n📊 РЕЙТИНГ:")
        print(f"  {p1_name}: {p1_points} очков")
        print(f"  {p2_name}: {p2_points} очков")
        print(f"  Разница: {abs(p1_points - p2_points)} очков")
        
        # Сравнение на разных покрытиях
        surfaces = ['hard', 'clay', 'grass']
        for surface in surfaces:
            self.cursor.execute('SELECT win_rate FROM surface_stats WHERE player_id = ? AND surface = ?', (p1_id, surface))
            p1_surface = self.cursor.fetchone()
            self.cursor.execute('SELECT win_rate FROM surface_stats WHERE player_id = ? AND surface = ?', (p2_id, surface))
            p2_surface = self.cursor.fetchone()
            
            if p1_surface and p2_surface:
                diff = p1_surface[0] - p2_surface[0]
                print(f"\n🎾 {surface.upper()}:")
                print(f"  {p1_name}: {p1_surface[0]:.1%}")
                print(f"  {p2_name}: {p2_surface[0]:.1%}")
                if diff > 0:
                    print(f"  Преимущество: {p1_name} ({diff:+.1%})")
                else:
                    print(f"  Преимущество: {p2_name} ({-diff:+.1%})")
        
        # Общий прогноз
        self.predict_match(player1_name, player2_name)

def main():
    print("="*60)
    print("ТЕННИСНАЯ СИСТЕМА ATP 2025")
    print("200 игроков | Погода | Покрытия")
    print("="*60)
    
    db = TennisDatabase()
    
    # Проверяем базу
    db.cursor.execute('SELECT COUNT(*) FROM players')
    count = db.cursor.fetchone()[0]
    
    if count == 0:
        print("Загрузка 200 игроков...")
        db.load_all_200_players()
    else:
        print(f"В базе: {count} игроков")
    
    # Меню
    while True:
        print(f"\n{'='*50}")
        print("1. Показать рейтинг ATP")
        print("2. Анализ игрока")
        print("3. Прогноз матча")
        print("4. Найти похожих игроков")
        print("5. Лучшие игроки на покрытии")
        print("6. Статистика по странам")
        print("7. Поиск игрока")
        print("8. Сравнение игроков")
        print("9. Выход")
        
        choice = input("\nВыберите действие (1-9): ")
        
        if choice == '1':
            limit = input("Сколько игроков показать? (по умолчанию 50): ")
            limit = int(limit) if limit else 50
            db.show_ranking(limit)
        
        elif choice == '2':
            player = input("Введите имя игрока: ")
            db.analyze_player(player)
        
        elif choice == '3':
            player1 = input("Первый игрок: ")
            player2 = input("Второй игрок: ")
            surface = input("Покрытие (hard/clay/grass) [hard]: ") or "hard"
            weather = input("Погода (sunny/rainy/windy/indoor) [sunny]: ") or "sunny"
            db.predict_match(player1, player2, surface, weather)
        
        elif choice == '4':
            player = input("Введите имя игрока для поиска похожих: ")
            db.find_similar_players(player)
        
        elif choice == '5':
            surface = input("Покрытие (hard/clay/grass) [hard]: ") or "hard"
            limit = input("Сколько игроков показать? [10]: ") or "10"
            db.get_top_players_by_surface(surface, int(limit))
        
        elif choice == '6':
            db.get_country_stats()
        
        elif choice == '7':
            search = input("Введите имя или страну для поиска: ")
            db.search_players(search)
        
        elif choice == '8':
            player1 = input("Первый игрок: ")
            player2 = input("Второй игрок: ")
            db.get_player_head_to_head(player1, player2)
        
        elif choice == '9':
            print("\nСпасибо за использование системы ATP!")
            break
        
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
