Для запуска через uv\n 
Тут документация
```
https://docs.astral.sh/uv/getting-started/installation/
```
это просто скрипт установки
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
Потом запускаете 
Для синхронизации пакетов
```
uv sync
```
для запуска скрипта
```
uv run main.py
```


через pip 
```
pip install -r requirements.txt
```
и потом
```
python main.py
```
