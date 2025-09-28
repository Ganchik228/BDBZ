from db import fetch_rules, fetch_audience_rules

def apply_simple_rules(game_dict):
    """Применяет простые правила для вывода дополнительных параметров"""
    # Простые правила механики по жанру
    if game_dict.get("Ж") == "RPG":
        game_dict["Мех"] = "прокачка"
    elif game_dict.get("Ж") == "FPS":
        game_dict["Мех"] = "стрелялки"
    elif game_dict.get("Ж") == "приключение":
        game_dict["Мех"] = "исследование"
    elif game_dict.get("Ж") == "стратегия":
        game_dict["Мех"] = "командное управление"
    elif game_dict.get("Ж") == "симулятор":
        game_dict["Мех"] = "управление ресурсами"
    elif game_dict.get("Ж") == "экшен":
        game_dict["Мех"] = "стелс"
    
    # Правила поддержки
    if game_dict.get("Гр") == "пиксель арт":
        game_dict["Под"] = "завершена"
    elif game_dict.get("DLC") == "Да":
        game_dict["Под"] = "активно"
    else:
        game_dict["Под"] = "завершена"
    
    # Правила онлайн-режима и мультиплеера
    if game_dict.get("Чис") in ["массовый мультиплеер", "многопользовательская игра", "кооператив"]:
        game_dict["Онл"] = "Да"
    else:
        game_dict["Онл"] = "Нет"
    
    # Правила сложности по популярности
    if game_dict.get("Поп") == "высокая":
        game_dict["Сл"] = "средняя"
    elif game_dict.get("Поп") == "низкая":
        game_dict["Сл"] = "низкая"
    
    # Правила сложности по тематике
    if game_dict.get("Тем") == "Выживание":
        game_dict["Сл"] = "высокая"
    
    return game_dict

def match_condition(game_dict, condition):
    """Проверяет соответствие игры условию"""
    for key, val in condition.items():
        if isinstance(val, dict):
            if "gt" in val and game_dict.get(key, 0) <= val["gt"]:
                return False
            if "lt" in val and game_dict.get(key, 0) >= val["lt"]:
                return False
            if "gte" in val and game_dict.get(key, 0) < val["gte"]:
                return False
            if "lte" in val and game_dict.get(key, 0) > val["lte"]:
                return False
        else:
            if game_dict.get(key) != val:
                return False
    return True

def determine_audience(game_dict):
    """Определяет аудиторию игры на основе правил"""
    # Применяем простые правила сначала
    game_dict = apply_simple_rules(game_dict)
    
    # Специальные правила для аудитории
    if game_dict.get("Сл") == "хардкор":
        return "хардкорные"
    
    if game_dict.get("Онл") == "Да" and game_dict.get("Мех") == "прокачка":
        return "казуальные"
    
    if game_dict.get("Сл") == "высокая" and game_dict.get("Поп") == "высокая":
        return "хардкорные"
    
    if game_dict.get("Р") == "E" and game_dict.get("Сл") == "низкая":
        return "дети"
        
    if game_dict.get("Онл") == "Нет" and game_dict.get("Р") == "T":
        return "дети"
    
    # Проверяем правила из базы данных
    audience_rules = fetch_audience_rules()
    for cond, aud in audience_rules:
        if match_condition(game_dict, cond):
            return aud
    
    # По умолчанию - казуальные
    return "казуальные"

def get_recommendation(game_dict):
    """Получает рекомендацию игры на основе параметров"""
    # Применяем простые правила
    game_dict = apply_simple_rules(game_dict)
    
    # Определяем аудиторию если не задана
    if "A" not in game_dict or not game_dict["A"]:
        game_dict["A"] = determine_audience(game_dict)
    
    # Специальные комплексные правила
    if (game_dict.get("Онл") == "Нет" and game_dict.get("A") == "дети"):
        return "Animal Crossing"
    
    if (game_dict.get("Онл") == "Да" and game_dict.get("Мех") == "стрелялки"):
        return "Call of Duty: Modern Warfare"
    
    if (game_dict.get("Мех") == "исследование" and game_dict.get("Под") == "активно"):
        return "Genshin Impact"
    
    if (game_dict.get("Мех") == "командное управление" and game_dict.get("Поп") == "высокая"):
        return "Civilization VI"
    
    # Проверяем правила из базы данных
    rules = fetch_rules()
    for cond, rec_game in rules:
        if match_condition(game_dict, cond):
            return rec_game
    
    return "Нет подходящих рекомендаций"
