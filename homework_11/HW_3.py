# %% [markdown]
# # Задание 1 (6 баллов)

# %% [markdown]
# В данном задании мы будем работать со [списком 250 лучших фильмов IMDb](https://www.imdb.com/chart/top/?ref_=nv_mp_mv250)
# 
# 1. Выведите топ-4 *фильма* **по количеству оценок пользователей** и **количество этих оценок** (1 балл)
# 2. Выведите топ-4 лучших *года* (**по среднему рейтингу фильмов в этом году**) и **средний рейтинг** (1 балл)
# 3. Постройте отсортированный **barplot**, где показано **количество фильмов** из списка **для каждого режисёра** (только для режиссёров с более чем 2 фильмами в списке) (1 балл)
# 4. Выведите топ-4 самых популярных *режиссёра* (**по общему числу людей оценивших их фильмы**) (2 балла)
# 5. Сохраните данные по всем 250 фильмам в виде таблицы с колонками (name, rank, year, rating, n_reviews, director) в любом формате (2 балла)
# 
# Использовать можно что-угодно, но полученные данные должны быть +- актуальными на момент сдачи задания

# %%
# Ваше решение здесь
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %%
url = "https://www.imdb.com/chart/top/?ref_=nv_mp_mv250"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
content = soup.find('tbody', {'class': 'lister-list'}).find_all('tr')

# %%
movies = []
for movie_info in content:
    title_col = movie_info.find('td', {'class': 'titleColumn'})
    movie_name = title_col.a.get_text()
    director = title_col.a['title'].split(',')[0].replace(' (dir.)', '')
    movie_year = title_col.span.get_text().strip('()')
    movie_rating = movie_info.find('td', {'class': 'ratingColumn'}).strong.get_text()
    review_number = int(movie_info.find('span', {'name': 'nv'})['data-value'])
    movies.append({
        'name': movie_name,
        'year': movie_year,
        'rating': movie_rating,
        'n_reviews': review_number,
        'director': director
    })

# %%
movies_df = pd.DataFrame.from_dict(movies)
movies_df['rating'] = movies_df.rating.astype(float)

# %%
# task 1
movies_df\
    .sort_values(by="n_reviews", ascending=False)[["name", "n_reviews"]]\
    .head(4)

# %%
# task 2
movies_df\
    .groupby("year")\
    .agg({"rating": "mean"})\
    .reset_index()\
    .rename(columns={'rating': 'mean_rating'})\
    .sort_values(by="mean_rating", ascending=False)\
    .head(4)

# %%
# task 3 NOT DONE
best_directors = movies_df\
    .groupby("director")\
    .agg({"name": "count"})\
    .reset_index().\
    rename(columns={"name": "n_movies"})\
    .sort_values("n_movies", ascending=False)\
    .query("n_movies > 2")
sns.barplot(data=best_directors, x="n_movies", y="director");

# %%
# task 4
movies_df\
    .groupby("director")\
    .agg({"n_reviews": "sum"})\
    .reset_index()\
    .rename(columns={"n_reviews": "n_fans"})\
    .sort_values("n_fans", ascending=False)\
    .head(4)

# %%
# task 5
movies_df.to_csv("movies.tsv", sep="\t") 

# %% [markdown]
# # Задание 2 (10 баллов)

# %% [markdown]
# Напишите декоратор `telegram_logger`, который будет логировать запуски декорируемых функций и отправлять сообщения в телеграм.
# 
# 
# Вся информация про API телеграм ботов есть в официальной документации, начать изучение можно с [этой страницы](https://core.telegram.org/bots#how-do-bots-work) (разделы "How Do Bots Work?" и "How Do I Create a Bot?"), далее идите в [API reference](https://core.telegram.org/bots/api)
# 
# **Основной функционал:**
# 1. Декоратор должен принимать **один обязательный аргумент** &mdash; ваш **CHAT_ID** в телеграме. Как узнать свой **CHAT_ID** можно найти в интернете
# 2. В сообщении об успешно завершённой функции должны быть указаны её **имя** и **время выполнения**
# 3. В сообщении о функции, завершившейся с исключением, должно быть указано **имя функции**, **тип** и **текст ошибки**
# 4. Ключевые элементы сообщения должны быть выделены **как код** (см. скриншот), форматирование остальных элементов по вашему желанию
# 5. Время выполнения менее 1 дня отображается как `HH:MM:SS.μμμμμμ`, время выполнения более 1 дня как `DDD days, HH:MM:SS`. Писать форматирование самим не нужно, всё уже где-то сделано за вас
# 
# **Дополнительный функционал:**
# 1. К сообщению также должен быть прикреплён **файл**, содержащий всё, что декорируемая функция записывала в `stdout` и `stderr` во время выполнения. Имя файла это имя декорируемой функции с расширением `.log` (**+3 дополнительных балла**)
# 2. Реализовать предыдущий пункт, не создавая файлов на диске (**+2 дополнительных балла**)
# 3. Если функция ничего не печатает в `stdout` и `stderr` &mdash; отправлять файл не нужно
# 
# **Важные примечания:**
# 1. Ни в коем случае не храните свой API токен в коде и не загружайте его ни в каком виде свой в репозиторий. Сохраните его в **переменной окружения** `TG_API_TOKEN`, тогда его можно будет получить из кода при помощи `os.getenv("TG_API_TOKEN")`. Ручное создание переменных окружения может быть не очень удобным, поэтому можете воспользоваться функцией `load_dotenv` из модуля [dotenv](https://pypi.org/project/python-dotenv/). В доке всё написано, но если коротко, то нужно создать файл `.env` в текущей папке и записать туда `TG_API_TOKEN=<your_token>`, тогда вызов `load_dotenv()` создаст переменные окружения из всех переменных в файле. Это довольно часто используемый способ хранения ключей и прочих приватных данных
# 2. Функцию `long_lasting_function` из примера по понятным причинам запускать не нужно. Достаточно просто убедится, что большие временные интервалы правильно форматируются при отправке сообщения (как в примерах)
# 3. Допустима реализация логирования, когда логгер полностью перехватывает запись в `stdout` и `stderr` (то есть при выполнении функций печать происходит **только** в файл)
# 4. В реальной жизни вам не нужно использовать Telegram API при помощи ручных запросов, вместо этого стоит всегда использовать специальные библиотеки Python, реализующие Telegram API, они более высокоуровневые и удобные. В данном задании мы просто учимся работать с API при помощи написания велосипеда.
# 5. Обязательно прочтите часть конспекта лекции про API перед выполнением задания, так как мы довольно поверхностно затронули это на лекции
# 
# **Рекомендуемые к использованию модули:**
# 1. os
# 2. sys
# 3. io
# 4. datetime
# 5. requests
# 6. dotenv
# 
# **Запрещённые модули**:
# 1. Любые библиотеки, реализующие Telegram API в Python (*python-telegram-bot, Telethon, pyrogram, aiogram, telebot* и так далле...)
# 2. Библиотеки, занимающиеся "перехватыванием" данных из `stdout` и `stderr` (*pytest-capturelog, contextlib, logging*  и так далле...)
# 
# 
# 
# Результат запуска кода ниже должен быть примерно такой:
# 
# ![image.png](attachment:620850d6-6407-4e00-8e43-5f563803d7a5.png)
# 
# ![image.png](attachment:65271777-1100-44a5-bdd2-bcd19a6f50a5.png)
# 
# ![image.png](attachment:e423686d-5666-4d81-8890-41c3e7b53e43.png)

# %%
import sys
import time
import os
import io
import requests
from functools import wraps
from datetime import datetime as dt
from dotenv import load_dotenv


load_dotenv()
api_token = os.getenv("TG_API_TOKEN")
chat_id = os.getenv("TG_CHAT_ID")


def telegram_logger(chat_id):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            stdout_backup = sys.stdout
            stderr_backup = sys.stderr
            sys.stdout = io.StringIO()
            sys.stderr = io.StringIO()

            start_time = dt.now()

            try:
                result = func(*args, **kwargs)
                success = True
            except Exception:
                success = False
                exc_type, exc_value, _ = sys.exc_info()
            finally:
                stdout_val = sys.stdout.getvalue()
                stderr_val = sys.stderr.getvalue()
                sys.stdout = stdout_backup
                sys.stderr = stderr_backup
            
            end_time = dt.now()
            func_run_time = end_time - start_time

            base_url = f"https://api.telegram.org/bot{api_token}/sendMessage"

            if success:
                message = f"Function `{func.__name__}` completed in {func_run_time}"
            else:
                message = f"Function `{func.__name__}` failed with {exc_type.__name__}: {exc_value}"

            payload = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "Markdown",
            }

            response = requests.post(base_url, data=payload)

            # Send log file to Telegram if stdout or stderr have content
            if stdout_val or stderr_val:
                log_file_content = f"stdout:\n{stdout_val}\n\nstderr:\n{stderr_val}"
                log_file = io.BytesIO(log_file_content.encode())
                log_file.name = f"{func.__name__}.log"

                file_base_url = f"https://api.telegram.org/bot{api_token}/sendDocument"
                file_payload = {
                    "chat_id": chat_id,
                }
                file_data = {
                    "document": log_file
                }
                file_response = requests.post(file_base_url, data=file_payload, files=file_data)

            return result if success else None

        return wrapper

    return decorator

                


@telegram_logger(chat_id)
def good_function():
    print("This goes to stdout")
    print("And this goes to stderr", file=sys.stderr)
    time.sleep(2)
    print("Wake up, Neo")

@telegram_logger(chat_id)
def bad_function():
    print("Some text to stdout")
    time.sleep(2)
    print("Some text to stderr", file=sys.stderr)
    raise RuntimeError("Ooops, exception here!")
    print("This text follows exception and should not appear in logs")
    
@telegram_logger(chat_id)
def long_lasting_function():
    time.sleep(30)


good_function()

try:
    bad_function()
except Exception:
    pass

long_lasting_function()

# %% [markdown]
# # Задание 3
# 
# В данном задании от вас потребуется сделать Python API для какого-либо сервиса
# 
# В задании предложено два варианта: простой и сложный, **выберите только один** из них.
# 
# Можно использовать только **модули стандартной библиотеки** и **requests**. Любые другие модули можно по согласованию с преподавателем.

# %% [markdown]
# ❗❗❗ В **данном задании** требуется оформить код в виде отдельного модуля (как будто вы пишете свою библиотеку). Код в ноутбуке проверяться не будет ❗❗❗

# %% [markdown]
# ## Вариант 1 (простой, 10 баллов)
# 
# В данном задании вам потребуется сделать Python API для сервиса http://hollywood.mit.edu/GENSCAN.html
# 
# Он способен находить и вырезать интроны в переданной нуклеотидной последовательности. Делает он это не очень хорошо, но это лучше, чем ничего. К тому же у него действительно нет публичного API.
# 
# Реализуйте следующую функцию:
# `run_genscan(sequence=None, sequence_file=None, organism="Vertebrate", exon_cutoff=1.00, sequence_name="")` &mdash; выполняет запрос аналогичный заполнению формы на сайте. Принимает на вход все параметры, которые можно указать на сайте (кроме Print options). `sequence` &mdash; последовательность в виде строки или любого удобного вам типа данных, `sequence_file` &mdash; путь к файлу с последовательностью, который может быть загружен и использован вместо `sequence`. Функция должна будет возвращать объект типа `GenscanOutput`. Про него дальше.
# 
# Реализуйте **датакласс** `GenscanOutput`, у него должны быть следующие поля:
# + `status` &mdash; статус запроса
# + `cds_list` &mdash; список предсказанных белковых последовательностей с учётом сплайсинга (в самом конце результатов с сайта)
# + `intron_list` &mdash; список найденных интронов. Один интрон можно представить любым типом данных, но он должен хранить информацию о его порядковом номере, его начале и конце. Информацию о интронах можно получить из первой таблицы в результатах на сайте.
# + `exon_list` &mdash; всё аналогично интронам, но только с экзонами.
# 
# По желанию можно добавить любые данные, которые вы найдёте в результатах

# %%
import genscan_module

genscan_module.run_genscan(sequence_file="OAS1.txt")

# %% [markdown]
# ## Вариант 2 (очень сложный, 20 дополнительных баллов)

# %% [markdown]
# В этом варианте от вас потребуется сделать Python API для BLAST, а именно для конкретной вариации **tblastn** https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=tblastn&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome
# 
# Хоть у BLAST и есть десктопное приложение, всё-таки есть одна область, где API может быть полезен. Если мы хотим искать последовательность в полногеномных сборках (WGS), а не в базах данных отдельных генов, у нас могут возникнуть проблемы. Так как если мы хотим пробластить нашу последовательность против большого количества геномов нам пришлось бы или вручную отправлять запросы на сайте, или скачивать все геномы и делать поиск локально. И тот и другой способы не очень удобны, поэтому круто было бы иметь способ сделать автоматический запрос, не заходя в браузер.
# 
# Необходимо написать функцию для запроса, которая будет принимать 3 обязательных аргумента: **белковая последовательность**, которую мы бластим, **базу данных** (в этом задании нас интересует только WGS, но по желанию можете добавить какую-нибудь ещё), **таксон**, у которого мы ищем последовательность, чаще всего &mdash; конкретный вид. По=желанию можете добавить также любые другие аргументы, соответствующие различным настройкам поиска на сайте. 
# 
# Функция дожна возвращать список объектов типа `Alignment`, у него должны быть следующие атрибуты (всё согласно результатам в браузере, удобно посмотреть на рисунке ниже), можно добавить что-нибудь своё:
# 
# ![Alignment.png](attachment:e45d0969-ff95-4d4b-8bbc-7f5e481dcda3.png)
# 
# 
# Самое сложное в задании - правильно сделать запрос. Для этого нужно очень глубоко погрузиться в то, что происходит при отправке запроса при помощи инструмента для разработчиков. Ещё одна проблема заключается в том, что BLAST не отдаёт результаты сразу, какое-то время ваш запрос обрабатывается, при этом изначальный запрос не перекидывает вас на страницу с результатами. Задание не такое простое как кажется из описания!

# %%
# Не пиши код здесь, сделай отдельный модуль


