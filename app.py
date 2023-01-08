import os

from flask import Flask, render_template, request, url_for, redirect, jsonify

from bases import Arena
from classes import unit_classes
from equipment import Equipment
from setup_db import db
from unit import PlayerUnit, EnemyUnit

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

heroes = {
    "player": ...,
    "enemy": ...,
}

# Инициализируем класс арены
arena = Arena()


@app.route("/")
def menu_page():
    """
    Рендерим главное меню (шаблон index.html)
    """
    return render_template('index.html')


@app.route("/fight/")
def start_fight():
    """
    Выполняем функцию start_game экземпляра класса арена и передаем ему необходимые аргументы
    Рендерим экран боя (шаблон fight.html)
    """
    arena.start_game(player=heroes['player'], enemy=heroes['enemy'])
    return render_template('fight.html', heroes=heroes)


@app.route("/fight/hit")
def hit():
    """
    Кнопка нанесения удара
    Обновляем экран боя (нанесение удара) (шаблон fight.html)
    Если игра идет - вызываем метод player.hit() экземпляра класса арены
    Если игра не идет - пропускаем срабатывание метода (простот рендерим шаблон с текущими данными)
    """
    if arena.game_is_running:
        result = arena.player_hit()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/use-skill")
def use_skill():
    """
    Кнопка использования скилла
    Логика пркатикчески идентична предыдущему эндпоинту
    """
    if arena.game_is_running:
        result = arena.player_use_skill()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/pass-turn")
def pass_turn():
    """
    Кнопка пропус хода
    Логика пркатикчески идентична предыдущему эндпоинту
    Однако вызываем здесь функцию следующий ход (arena.next_turn())
    """
    if arena.game_is_running:
        result = arena.next_turn()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/end-fight")
def end_fight():
    """
    Кнопка завершить игру - переход в главное меню
    """
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    """
    Кнопка выбор героя. 2 метода GET и POST
    На GET отрисовываем форму.
    На POST отправляем форму и делаем редирект на эндпоинт choose enemy
    """
    if request.method == 'GET':
        header = "Выберите игрока"
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        result = {
            'header': header,
            'weapons': weapons,
            'armors': armors,
            'classes': unit_classes,
        }
        return render_template('hero_choosing.html', result=result)
    if request.method == 'POST':
        name = request.form['name']
        weapon_name = request.form['weapon']
        armor_name = request.form['armor']
        unit_class = request.form['unit_class']
        player = PlayerUnit(name=name, unit_class=unit_classes.get(unit_class))
        player.equip_armor(Equipment().get_armor(armor_name))
        player.equip_weapon(Equipment().get_weapon(weapon_name))
        heroes['player'] = player

        return redirect(url_for('choose_enemy'))


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    """
    Кнопка выбор соперников. 2 метода GET и POST
    На GET отрисовываем форму.
    На POST отправляем форму и делаем редирект на начало битвы
    """
    if request.method == 'GET':
        header = "Выберите противника"
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        result = {
            'header': header,
            'weapons': weapons,
            'armors': armors,
            'classes': unit_classes,
        }
        return render_template('hero_choosing.html', result=result)
    if request.method == 'POST':
        name = request.form['name']
        weapon_name = request.form['weapon']
        armor_name = request.form['armor']
        unit_class = request.form['unit_class']
        enemy = EnemyUnit(name=name, unit_class=unit_classes.get(unit_class))
        enemy.equip_armor(Equipment().get_armor(armor_name))
        enemy.equip_weapon(Equipment().get_weapon(weapon_name))
        heroes['enemy'] = enemy
        return redirect(url_for('start_fight'))


@app.route("/test_db/")
def test_db():
    result = db.session.execute(
        '''
        SELECT 1
        '''
    ).scalar()

    return jsonify(
        {
            'result': result,
        }
    )


db.init_app(app)

if __name__ == "__main__":
    app.run(port=25000)
