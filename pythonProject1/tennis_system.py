# -*- coding: utf-8 -*- 
 
import sqlite3 
import hashlib 
from datetime import datetime 
import random 
 
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
                    country TEXT, 
                    ranking INTEGER, 
                    points INTEGER 
                ) 
            ''') 
            conn.commit() 
 
            # Таблица покрытий 
            cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS surfaces ( 
                    player_hash TEXT, 
                    surface TEXT, 
                    win_rate REAL, 
                    matches INTEGER, 
                    PRIMARY KEY (player_hash, surface) 
                ) 
            ''') 
 
            # Таблица погоды 
            cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS weather ( 
                    player_hash TEXT, 
                    weather TEXT, 
                    win_rate REAL, 
                    matches INTEGER, 
                    PRIMARY KEY (player_hash, weather) 
                ) 
            ''') 
 
            conn.commit() 
        print("База данных инициализирована") 
 
    def add_player(self, name, country, ranking, points, height=None, hand='right'): 
        """Добавить игрока в базу""" 
        player_hash = hashlib.md5(f"{name}_{country}".encode()).hexdigest() 
        with self.get_connection() as conn: 
            cursor = conn.cursor() 
            cursor.execute(''' 
                INSERT OR REPLACE INTO players 
                (player_hash, name, country, ranking, points, height, hand) 
                VALUES (?, ?, ?, ?, ?, ?, ?) 
            ''', (player_hash, name, country, ranking, points, height, hand)) 
            conn.commit() 
        print(f"Добавлен: {name}") 
        return player_hash 
 
 
    def add_surface_stats(self, player_hash, surface, win_rate, matches): 
        """Добавить статистику по покрытию""" 
        with self.get_connection() as conn: 
            cursor = conn.cursor() 
            cursor.execute(''' 
                INSERT OR REPLACE INTO surfaces 
                (player_hash, surface, win_rate, matches) 
                VALUES (?, ?, ?, ?) 
            ''', (player_hash, surface, win_rate, matches)) 
            conn.commit() 
 
    def add_weather_stats(self, player_hash, weather, win_rate, matches): 
        """Add weather statistics""" 
        with self.get_connection() as conn: 
            cursor = conn.cursor() 
            cursor.execute(''' 
                INSERT OR REPLACE INTO weather 
                (player_hash, weather, win_rate, matches) 
                VALUES (?, ?, ?, ?) 
            ''', (player_hash, weather, win_rate, matches)) 
            conn.commit() 
 
    def show_players(self, limit=10): 
        """Show players""" 
        with self.get_connection() as conn: 
            cursor = conn.cursor() 
            cursor.execute('SELECT * FROM players ORDER BY ranking LIMIT ?', (limit,)) 
            players = cursor.fetchall() 
            print(f"\\nTOP-{limit} ATP PLAYERS:") 
            print("=" * 50) 
            for player in players: 
                print(f"{player[3]:2d}. {player[1]:20} {player[2]:10} {player[4]:6d} points") 
 
