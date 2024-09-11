### Первоначальная настройка проекта и установка зависимостей
1) создаем папку для нашего проекта
2) создаем виртуальное окружение Env или virtualenv, активация workon NameApp
```python
mkvirtualenv NameApp 
```

3) устанавливаем пакеты  fastapi и uvicorn
```python
pip install fastapi uvicorn
```

4) переносим названия библиотек с версиями библиотек в файл или
```python
pip freeze > requirements.txt
```

5) или установим из готового списка с зависимостями в проект определенные версии
```python
pip install -r requirements.txt
```