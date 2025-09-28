import sqlite3
import json

DB_NAME = "games.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Таблица игр
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        genre TEXT,
        theme TEXT,
        rating TEXT,
        players TEXT,
        year INTEGER,
        graphics TEXT,
        difficulty TEXT,
        popularity TEXT,
        dlc TEXT,
        mech TEXT,
        audience TEXT,
        support TEXT,
        online TEXT,
        platform TEXT
    )
    """)

    # Таблица правил рекомендаций
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        condition_json TEXT NOT NULL,
        recommended_game TEXT NOT NULL
    )
    """)

    # Таблица правил аудитории
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audience_rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        condition_json TEXT NOT NULL,
        audience TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def save_game(game_dict, rec_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO games (name, genre, theme, rating, players, year, graphics, difficulty, popularity, dlc, mech, audience, support, online, platform)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        rec_name,
        game_dict.get("Ж"), game_dict.get("Тем"), game_dict.get("Р"), game_dict.get("Чис"), game_dict.get("Г"),
        game_dict.get("Гр"), game_dict.get("Сл"), game_dict.get("Поп"), game_dict.get("DLC"), game_dict.get("Мех"),
        game_dict.get("A"), game_dict.get("Под"), game_dict.get("Онл"), game_dict.get("П")
    ))
    conn.commit()
    conn.close()


def fetch_all_games():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM games")
    rows = cursor.fetchall()
    conn.close()
    return rows


def add_rule(condition_dict, recommended_game):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO rules (condition_json, recommended_game) VALUES (?, ?)",
                   (json.dumps(condition_dict), recommended_game))
    conn.commit()
    conn.close()


def add_audience_rule(condition_dict, audience):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO audience_rules (condition_json, audience) VALUES (?, ?)",
                   (json.dumps(condition_dict), audience))
    conn.commit()
    conn.close()


def fetch_rules():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT condition_json, recommended_game FROM rules")
    rules = cursor.fetchall()
    conn.close()
    return [(json.loads(r[0]), r[1]) for r in rules]


def fetch_audience_rules():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT condition_json, audience FROM audience_rules")
    rules = cursor.fetchall()
    conn.close()
    return [(json.loads(r[0]), r[1]) for r in rules]


def populate_default_rules():
    # ----------------- Аудитория -----------------
    add_audience_rule({"Сл": "низкая", "Р": "E"}, "дети")
    add_audience_rule({"Сл": "высокая", "Поп": "высокая"}, "хардкорные")
    add_audience_rule({"Онл": "Да", "Мех": "прокачка"}, "казуальные")
    add_audience_rule({"Онл": "Нет", "Р": "T"}, "дети")
    
    # ----------------- RPG -----------------
    add_rule({"Ж": "RPG", "Мех": "прокачка", "Под": "активно", "Г": {"gt": 2021}}, "Diablo IV")
    add_rule({"Ж": "RPG", "Тем": "Фэнтези", "Чис": "одиночная игра", "Сл": "средняя"}, "The Witcher 3")
    add_rule({"Ж": "RPG", "Тем": "Фэнтези", "Чис": "одиночная игра", "Сл": "средняя", "Под": "активно"}, "Elder Scrolls V: Skyrim Special Edition")
    add_rule({"Ж": "RPG", "Тем": "Фэнтези", "Чис": "кооператив"}, "Divinity: Original Sin 2")
    
    # ----------------- FPS / TPS -----------------
    add_rule({"Ж": "FPS", "Онл": "Да", "Мех": "стрелялки"}, "Call of Duty: Modern Warfare")
    add_rule({"Ж": "FPS", "Тем": "Постапокалипсис", "Р": "M", "A": "хардкорные"}, "Escape from Tarkov")
    add_rule({"Ж": "FPS", "Тем": "Современность", "Онл": "Да"}, "Battlefield 2042")
    add_rule({"Ж": "TPS", "Тем": "Аниме", "Чис": "многопользовательская игра", "A": "казуальные"}, "Fortnite")
    
    # ----------------- Приключения -----------------
    add_rule({"Ж": "приключение", "Тем": "Хоррор", "Р": "M", "Чис": "одиночная игра"}, "Resident Evil 2 Remake")
    add_rule({"Ж": "приключение", "Тем": "Аниме"}, "Ni no Kuni II")
    add_rule({"Ж": "приключение", "П": "Nintendo"}, "The Legend of Zelda: BOTW")
    add_rule({"Ж": "приключение", "Тем": "Выживание", "Чис": "одиночная игра"}, "The Forest")
    
    # ----------------- Экшен -----------------
    add_rule({"Ж": "экшен", "Тем": "Киберпанк", "Гр": "реализм", "DLC": "Да", "Г": {"gt": 2019}}, "Cyberpunk 2077")
    add_rule({"Ж": "экшен", "Тем": "Современность", "Мех": "стелс"}, "Hitman 3")
    
    # ----------------- Стратегии -----------------
    add_rule({"Ж": "стратегия", "Тем": "Исторический", "Чис": "MMO", "DLC": "Да"}, "Civilization VI")
    add_rule({"Ж": "стратегия", "Тем": "Sci-fi", "Чис": "многопользовательская игра", "Под": "активно"}, "StarCraft II")
    add_rule({"Ж": "стратегия", "Тем": "Исторический", "Чис": "одиночная игра"}, "Total War: WARHAMMER II")
    
    # ----------------- Симуляторы -----------------
    add_rule({"Ж": "симулятор", "П": "мобильные"}, "Plague Inc.")
    add_rule({"Ж": "симулятор", "Ж": "гонки", "Тем": "Современность", "Сл": "средняя"}, "BeamNG.drive")
    add_rule({"Ж": "симулятор", "Ж": "гонки", "Тем": "Современность"}, "Assetto Corsa")
    
    # ----------------- Гонки -----------------
    add_rule({"Ж": "гонки", "A": "хардкорные"}, "Forza Horizon 5")
    add_rule({"Ж": "гонки", "Тем": "Современность", "Сл": "средняя", "A": "казуальные"}, "Need for Speed")
    add_rule({"Ж": "гонки", "Тем": "современность", "П": "мобильные"}, "Asphalt 9")
    
    # ----------------- Хоррор -----------------
    add_rule({"Ж": "хоррор", "Р": "M", "DLC": "Да", "Г": {"gt": 2018}}, "Resident Evil Village")
    add_rule({"Ж": "хоррор", "Р": "M", "Чис": "одиночная игра"}, "Amnesia: Rebirth")
    
    # ----------------- Казуальные -----------------
    add_rule({"Ж": "FPS", "Тем": "Аниме", "Чис": "многопользовательская игра", "A": "казуальные", "Гр": "казуальная графика"}, "Splatoon 3")
    add_rule({"Ж": "FPS", "Мех": "стрелялки", "Онл": "Да", "A": "казуальные"}, "Plants vs. Zombies: Battle for Neighborville")
    
    # ----------------- RPG-серии -----------------
    add_rule({"Ж": "RPG", "Мех": "прокачка", "Тем": "Фэнтези", "Чис": "кооператив"}, "Divinity: Original Sin 2")
    add_rule({"Ж": "RPG", "Тем": "Фэнтези", "Чис": "одиночная игра"}, "Elder Scrolls V: Skyrim")
