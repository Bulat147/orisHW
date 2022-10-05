# необходимые импорты
import json
from flask import Flask, render_template, request

# инициализируем приложение
# из документации:
#     The flask object implements a WSGI application and acts as the central
#     object.  It is passed the name of the module or package of the
#     application.  Once it is created it will act as a central registry for
#     the view functions, the URL rules, template configuration and much more.
app = Flask(__name__)

# дальше реализуем методы, которые мы можем выполнить из браузера,
# благодаря указанным относительным путям


# метод, который возвращает список фильмов по относительному адресу /films
@app.route("/")
def films_list():
    # читаем файл с фильмами
    with open("films.json", 'r', encoding="UTF-8") as f:
        films = json.load(f)

    # получаем GET-параметр country (Russia/USA/French
    country = request.args.get("country")
    try:
        rating = float(request.args.get("rating"))
    except Exception:
        rating = None

    # Обработаем случай, если вдруг мы попали сюда после добавления фильма
    film_name = request.args.get("film_name")
    film_rating = request.args.get("film_rating")
    film_country = request.args.get("film_country")

    if film_name is not None:
        is_exist = False
        # Суем фильм в список
        count_id = 0
        for film in films:
            count_id = film["id"]
            if film_name == film["name"]:
                is_exist = True
                break
        if not is_exist:
            with open("films.json", 'w', encoding="UTF-8") as f:
                films.append({
                    "id" : count_id+1,
                    "name" : film_name,
                    "rating" : float(film_rating),
                    "country" : film_country
                })
                json.dump(films, f)

    # формируем контекст, который мы будем передавать для генерации шаблона
    context = {
        'films': films,
        'title': "FILMS",
        'country': country,
        'rating' : rating
    }
    # TODO: украсить кнопку в этом файле
    # возвращаем сгенерированный шаблон с нужным нам контекстом
    return render_template("films.html", **context)


# метод, который возвращает конкретный фильм по id по относительному пути /film/<int:film_id>,
# где film_id - id необходимого фильма
@app.route("/film/<int:film_id>")
def get_film(film_id):
    # читаем файл
    with open("films.json", 'r') as f:
        films = json.load(f)

    # ищем нужный нам фильм и возвращаем шаблон с контекстом
    for film in films:
        if film['id'] == film_id:
            return render_template("film.html", title=film['name'], film=film)

    # если нужный фильм не найден, возвращаем шаблон с ошибкой
    return render_template("error.html", error="Такого фильма не существует в системе")

# метод, который возвращает список фильмов по относительному адресу /films
@app.route("/createFilm")
def create_film():

    # формируем контекст, который мы будем передавать для генерации шаблона
    context = {
        'title': "Create film"
    }

    # возвращаем сгенерированный шаблон с нужным нам контекстом
    return render_template("createFilm.html", **context)