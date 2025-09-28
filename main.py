import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from db import init_db, save_game, fetch_all_games, populate_default_rules
from knowledge import get_recommendation, determine_audience

# Настройка темы
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GameRecommendationApp:
    def __init__(self):
        # Инициализация базы данных
        init_db()
        populate_default_rules()
        
        # Главное окно
        self.root = ctk.CTk()
        self.root.title("🎮 Рекомендатор игр")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        
        # Переменные для полей ввода
        self.init_variables()
        
        # Создание интерфейса
        self.create_widgets()
        
    def init_variables(self):
        """Инициализация переменных для полей ввода"""
        self.genre_var = ctk.StringVar(value="RPG")
        self.theme_var = ctk.StringVar(value="Фэнтези")
        self.rating_var = ctk.StringVar(value="E")
        self.players_var = ctk.StringVar(value="одиночная игра")
        self.year_var = ctk.StringVar(value="2022")
        self.graphics_var = ctk.StringVar(value="реализм")
        self.difficulty_var = ctk.StringVar(value="средняя")
        self.popularity_var = ctk.StringVar(value="высокая")
        self.dlc_var = ctk.StringVar(value="Да")
        self.platform_var = ctk.StringVar(value="PC")
        
    def create_widgets(self):
        """Создание виджетов интерфейса"""
        # Создание tabview
        self.tabview = ctk.CTkTabview(self.root, width=1150, height=750)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Вкладка рекомендаций
        self.tabview.add("🎯 Рекомендации")
        self.create_recommendation_tab()
        
        # Вкладка истории
        self.tabview.add("📚 История рекомендаций")
        self.create_history_tab()
        
        # Вкладка информации
        self.tabview.add("ℹ️ О системе")
        self.create_info_tab()
        
    def create_recommendation_tab(self):
        """Создание вкладки рекомендаций"""
        tab = self.tabview.tab("🎯 Рекомендации")
        
        # Главная рамка
        main_frame = ctk.CTkFrame(tab)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Заголовок
        title_label = ctk.CTkLabel(
            main_frame, 
            text="🎮 Система рекомендаций игр",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Рамка для параметров
        params_frame = ctk.CTkScrollableFrame(main_frame, height=400)
        params_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Создание полей ввода
        self.create_input_fields(params_frame)
        
        # Кнопка рекомендации
        recommend_btn = ctk.CTkButton(
            main_frame,
            text="✨ Получить рекомендацию",
            command=self.get_recommendation,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=40,
            corner_radius=10
        )
        recommend_btn.pack(pady=20)
        
        # Результат
        self.result_frame = ctk.CTkFrame(main_frame)
        self.result_frame.pack(fill="x", padx=20, pady=10)
        
        self.result_label = ctk.CTkLabel(
            self.result_frame,
            text="Выберите параметры и нажмите кнопку для получения рекомендации",
            font=ctk.CTkFont(size=16),
            wraplength=800
        )
        self.result_label.pack(pady=20)
        
    def create_input_fields(self, parent):
        """Создание полей ввода параметров"""
        fields_data = [
            ("🎮 Жанр", self.genre_var, ["RPG", "FPS", "приключение", "стратегия", "симулятор", "гонки", "экшен"]),
            ("🌍 Тематика", self.theme_var, ["Фэнтези", "Sci-fi", "Steampunk", "Post-Apocalyptic", "Выживание", "Аниме", "Открытый мир", "Хоррор", "Современность", "Исторический"]),
            ("🔞 Возрастной рейтинг", self.rating_var, ["E", "T", "M", "AO"]),
            ("👥 Тип игроков", self.players_var, ["кооператив", "массовый мультиплеер", "одиночная игра", "многопользовательская игра"]),
            ("📅 Год выпуска", self.year_var, None),
            ("🎨 Графика", self.graphics_var, ["реализм", "семи-реализм", "казуальная графика", "пиксель арт", "воксель арт"]),
            ("⚡ Сложность", self.difficulty_var, ["низкая", "средняя", "высокая", "хардкор"]),
            ("📈 Популярность", self.popularity_var, ["низкая", "средняя", "высокая"]),
            ("💾 DLC", self.dlc_var, ["Да", "Нет"]),
            ("🖥️ Платформа", self.platform_var, ["PC", "PlayStation", "Xbox", "Nintendo", "мобильные"])
        ]
        
        # Создание сетки полей (2 колонки)
        for i, (label, var, options) in enumerate(fields_data):
            row = i // 2
            col = i % 2
            
            # Рамка для поля
            field_frame = ctk.CTkFrame(parent)
            field_frame.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
            
            # Настройка колонок
            parent.grid_columnconfigure(0, weight=1)
            parent.grid_columnconfigure(1, weight=1)
            
            # Метка
            label_widget = ctk.CTkLabel(field_frame, text=label, font=ctk.CTkFont(size=14, weight="bold"))
            label_widget.pack(pady=(10, 5))
            
            # Поле ввода
            if options:
                input_widget = ctk.CTkOptionMenu(
                    field_frame,
                    variable=var,
                    values=options,
                    font=ctk.CTkFont(size=12),
                    dropdown_font=ctk.CTkFont(size=12)
                )
            else:
                input_widget = ctk.CTkEntry(
                    field_frame,
                    textvariable=var,
                    font=ctk.CTkFont(size=12),
                    justify="center"
                )
            
            input_widget.pack(pady=(0, 10), padx=10, fill="x")
    
    def create_history_tab(self):
        """Создание вкладки истории"""
        tab = self.tabview.tab("📚 История рекомендаций")
        
        # Заголовок
        title_label = ctk.CTkLabel(
            tab,
            text="📚 История рекомендаций",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Рамка для списка
        self.history_frame = ctk.CTkScrollableFrame(tab, height=600)
        self.history_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Кнопка обновления
        refresh_btn = ctk.CTkButton(
            tab,
            text="🔄 Обновить список",
            command=self.update_history,
            font=ctk.CTkFont(size=14)
        )
        refresh_btn.pack(pady=10)
        
        # Загрузка истории
        self.update_history()
    
    def create_info_tab(self):
        """Создание информационной вкладки"""
        tab = self.tabview.tab("ℹ️ О системе")
        
        info_frame = ctk.CTkScrollableFrame(tab)
        info_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Заголовок
        title_label = ctk.CTkLabel(
            info_frame,
            text="ℹ️ О системе рекомендаций игр",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Описание системы
        description = """
🎯 Эта система использует экспертные знания для рекомендации компьютерных игр.

📋 Как это работает:
• Система анализирует ваши предпочтения по множеству параметров
• Применяет простые правила для определения дополнительных характеристик
• Использует сложные правила для точного подбора игр
• Определяет целевую аудиторию на основе параметров игры

🧠 Типы правил:
• Простые правила: жанр → механика, популярность → сложность
• Сложные правила: комбинация условий → конкретная игра
• Правила аудитории: параметры → тип игроков (дети, казуальные, хардкорные)

🎮 Жанры игр:
• RPG - ролевые игры с прокачкой персонажа
• FPS - шутеры от первого лица
• Стратегия - игры на планирование и тактику
• Приключения - исследование мира и сюжет
• Симуляторы - имитация реальных процессов
• Гонки - автомобильные соревнования
• Экшен - динамичные боевые игры

🌟 Особенности:
• Учитывает возрастные ограничения
• Анализирует предпочтения по платформам
• Определяет подходящий уровень сложности
• Рекомендует игры с активной поддержкой или классику
        """
        
        info_label = ctk.CTkLabel(
            info_frame,
            text=description,
            font=ctk.CTkFont(size=14),
            justify="left",
            wraplength=800
        )
        info_label.pack(pady=20, padx=20)
        
    def get_recommendation(self):
        """Получение рекомендации"""
        try:
            # Собираем данные
            inputs = {
                "Ж": self.genre_var.get(),
                "Тем": self.theme_var.get(),
                "Р": self.rating_var.get(),
                "Чис": self.players_var.get(),
                "Г": int(self.year_var.get()),
                "Гр": self.graphics_var.get(),
                "Сл": self.difficulty_var.get(),
                "Поп": self.popularity_var.get(),
                "DLC": self.dlc_var.get(),
                "П": self.platform_var.get(),
            }
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректный год")
            return
        
        # Получаем рекомендацию
        recommendation = get_recommendation(inputs)
        audience = determine_audience(inputs)
        
        # Сохраняем в базу
        inputs["A"] = audience
        save_game(inputs, recommendation)
        
        # Обновляем результат
        self.show_result(recommendation, audience, inputs)
        
        # Обновляем историю
        self.update_history()
    
    def show_result(self, recommendation, audience, inputs):
        """Отображение результата рекомендации"""
        # Очищаем предыдущий результат
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        # Заголовок результата
        result_title = ctk.CTkLabel(
            self.result_frame,
            text="🎯 Результат рекомендации",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        result_title.pack(pady=(15, 10))
        
        # Рекомендованная игра
        game_label = ctk.CTkLabel(
            self.result_frame,
            text=f"🎮 Рекомендованная игра: {recommendation}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("green", "lightgreen")
        )
        game_label.pack(pady=5)
        
        # Аудитория
        audience_label = ctk.CTkLabel(
            self.result_frame,
            text=f"👥 Целевая аудитория: {audience}",
            font=ctk.CTkFont(size=16)
        )
        audience_label.pack(pady=5)
        
        # Дополнительная информация
        info_text = f"""
🔍 Анализ параметров:
• Жанр: {inputs['Ж']} | Тематика: {inputs['Тем']}
• Платформа: {inputs['П']} | Год: {inputs['Г']}
• Сложность: {inputs['Сл']} | Популярность: {inputs['Поп']}
• Графика: {inputs['Гр']} | DLC: {inputs['DLC']}
        """
        
        info_label = ctk.CTkLabel(
            self.result_frame,
            text=info_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        info_label.pack(pady=(10, 15))
    
    def update_history(self):
        """Обновление истории рекомендаций"""
        # Очищаем предыдущую историю
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        
        # Получаем данные из базы
        games = fetch_all_games()
        
        if not games:
            no_data_label = ctk.CTkLabel(
                self.history_frame,
                text="📝 История рекомендаций пуста",
                font=ctk.CTkFont(size=16)
            )
            no_data_label.pack(pady=50)
            return
        
        # Отображаем каждую игру
        for i, game in enumerate(reversed(games[-20:])):  # Последние 20 записей
            self.create_history_item(game, i)
    
    def create_history_item(self, game, index):
        """Создание элемента истории"""
        # Распаковка данных игры
        (id_, name, genre, theme, rating, players, year, graphics, 
         difficulty, popularity, dlc, mech, audience, support, online, platform) = game
        
        # Рамка для элемента
        item_frame = ctk.CTkFrame(self.history_frame)
        item_frame.pack(fill="x", padx=10, pady=5)
        
        # Заголовок с названием игры
        title_label = ctk.CTkLabel(
            item_frame,
            text=f"🎮 {name}",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        title_label.pack(fill="x", padx=15, pady=(10, 5))
        
        # Информация об игре
        info_text = f"""
🎯 Жанр: {genre} | 🌍 Тематика: {theme} | 🔞 Рейтинг: {rating}
👥 Игроки: {players} | 📅 Год: {year} | 🎨 Графика: {graphics}
⚡ Сложность: {difficulty} | 📈 Популярность: {popularity} | 💾 DLC: {dlc}
🖥️ Платформа: {platform} | 👤 Аудитория: {audience}
        """
        
        info_label = ctk.CTkLabel(
            item_frame,
            text=info_text.strip(),
            font=ctk.CTkFont(size=11),
            justify="left",
            anchor="w"
        )
        info_label.pack(fill="x", padx=15, pady=(0, 10))
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()

if __name__ == "__main__":
    app = GameRecommendationApp()
    app.run()