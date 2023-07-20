import json
import os
import sys

import pymysql
from flask import *

SQL_PATH = 'sql'

app = Flask(__name__)
config = {}
try:
    with open('.config') as f:
        for line in f.read().split('\n'):
            c = line.split('=')
            if len(c) != 2:
                raise ValueError
            config[c[0]] = c[1]
except IndexError:
    print("Some error with config file!")
    sys.exit()
except ValueError:
    print("Some error with config file!")
    sys.exit()
except os.error:
    print("Some error with config file!")
    sys.exit()


def __connect__():
    return pymysql.connect(user=config['user'],
                           host=config['host'],
                           port=int(config['port']),
                           password=config['password'],
                           database=config['database'],
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)


def __get_all_addresses__():
    conn = __connect__()
    with conn:
        with conn.cursor() as cur:
            sql = "select * from address;"
            cur.execute(sql)
        conn.commit()
    return cur.fetchall()


def __get_all_tracks__():
    conn = __connect__()
    with conn:
        with conn.cursor() as cur:
            sql = "select track_icon, track_no, track_title, time_since_release(track_release_date) as track_release, concat(\"$\", track_price) as track_price, millis_to_duration(duration_ms) as duration, language_name, album_name, band_name from track natural join languages natural join album_track natural join album natural join album_band natural join band;"
            cur.execute(sql)
        conn.commit()
    return cur.fetchall()


def __get_featured_tracks__():
    conn = __connect__()
    with conn:
        with conn.cursor() as cur:
            sql = "select track_icon, track_title, time_since_release(track_release_date) as track_release, millis_to_duration(duration_ms) as duration, album_name, band_name from track natural join album_track natural join album natural join album_band natural join band limit 6;"
            cur.execute(sql)
        conn.commit()
    return cur.fetchall()


def __get_all_albums__():
    conn = __connect__()
    with conn:
        with conn.cursor() as cur:
            sql = "select album_name, time_since_release(album_release_date) as album_release, album_icon, band_name, count(track_id) as track_count from album natural join album_band natural join band natural join album_track;"
            cur.execute(sql)
        conn.commit()
    return cur.fetchall()


def __get_featured_albums__():
    conn = __connect__()
    with conn:
        with conn.cursor() as cur:
            sql = "select album_name, band_name, time_since_release(album_release_date) as album_release, count(*) as num_tracks, album_icon from album natural join album_band natural join band natural join album_track limit 6;"
            cur.execute(sql)
        conn.commit()
    return cur.fetchall()


def __get_all_artists__():
    conn = __connect__()
    with conn:
        with conn.cursor() as cur:
            sql = "select concat(first_name, \" \", last_name) as name, gender, trim(leading '0' from (date_format(from_days(datediff(curdate(), date_of_birth)), \"%Y\"))) as age, concat(city, \", \", state, \", \", country) as current_city, phone_no, email_address, ifnull(band_name, \"\") as band_name from artist natural join address left join band_artist using (artist_id) left join band using (band_id);"
            cur.execute(sql)
        conn.commit()
    return cur.fetchall()


def __get_featured_bands__():
    conn = __connect__()
    with conn:
        with conn.cursor() as cur:
            sql = "select band_name, group_concat(concat(first_name, \" \", last_name)) as band_members from band natural join band_artist natural join artist group by band_id limit 6;"
            cur.execute(sql)
        conn.commit()
    return cur.fetchall()


def __get_all_country_codes__():
    conn = __connect__()
    with conn:
        with conn.cursor() as cur:
            sql = "select country_name, numeric_code from country_code order by country_name;"
            cur.execute(sql)
        conn.commit()
    return cur.fetchall()


def __get_all_available_artists__(artist_id):
    conn = __connect__()
    with conn:
        with conn.cursor() as cur:
            sql = "select * from artist where artist_id not in (select artist_id from band_artist) and artist_id != %s;"
            cur.execute(sql, artist_id)
        conn.commit()
    return cur.fetchall()


def __get_all_proficiencies__():
    conn = __connect__()
    with conn:
        with conn.cursor() as cur:
            sql = "select * from proficiency;"
            cur.execute(sql)
        conn.commit()
    return cur.fetchall()


def is_logged_in():
    user = request.cookies.get('user')
    login_or_profile = '<a href="' + \
                       url_for('login') + \
                       '"><button type="button" class="btn btn-outline-light">Login</button></a>'
    sign_up_or_sign_out = '<ul class="dropdown-menu dropdown-menu-end"><li><a class="dropdown-item" href="' + \
                          url_for('signup') + \
                          '">Sign up</a></li></ul>'
    if user:
        login_or_profile = '<a href="' + \
                           url_for('profile') + \
                           '"><button type="button" class="btn btn-outline-light">Profile</button></a>'
        sign_up_or_sign_out = '<ul class="dropdown-menu dropdown-menu-end"><li><a class="dropdown-item" href="' + \
                              url_for('signout') + \
                              '">Sign out</a></li></ul>'
    return login_or_profile, sign_up_or_sign_out


def __get_band_details__(artist_id):
    conn = __connect__()
    with conn:
        with conn.cursor() as cur:
            sql = "select band_id, band_name, concat(first_name, \" \", last_name) as member, group_concat(ifnull(proficiency_name, \"\")) as proficiency from (select band_id, band_name from band_artist natural join band where artist_id = %s) as b natural join band_artist natural join artist left join artist_proficiency using (artist_id) left join proficiency using (proficiency_id) group by artist_id;"
            cur.execute(sql, artist_id)
        conn.commit()
    return cur.fetchall()


@app.route('/')
def index():
    login_or_profile, sign_up_or_sign_out = is_logged_in()
    return render_template('index.html',
                           login_or_profile=login_or_profile,
                           sign_up_or_sign_out=sign_up_or_sign_out,
                           featured_tracks=__get_featured_tracks__(),
                           featured_albums=__get_featured_albums__(),
                           featured_bands=__get_featured_bands__())


@app.route('/songs')
def songs():
    login_or_profile, sign_up_or_sign_out = is_logged_in()
    return render_template('tracks.html',
                           all_songs=__get_all_tracks__(),
                           login_or_profile=login_or_profile,
                           sign_up_or_sign_out=sign_up_or_sign_out)


@app.route('/albums')
def albums():
    login_or_profile, sign_up_or_sign_out = is_logged_in()
    return render_template('albums.html',
                           all_albums=__get_all_albums__(),
                           login_or_profile=login_or_profile,
                           sign_up_or_sign_out=sign_up_or_sign_out)


@app.route('/artists')
def artists():
    login_or_profile, sign_up_or_sign_out = is_logged_in()
    return render_template('artists.html',
                           all_artists=__get_all_artists__(),
                           login_or_profile=login_or_profile,
                           sign_up_or_sign_out=sign_up_or_sign_out)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_or_profile, sign_up_or_sign_out = is_logged_in()
    if request.cookies.get('user'):
        return redirect(url_for('index'))
    if request.method == 'POST':
        data = request.get_json(force=True)
        conn = __connect__()
        try:
            with conn:
                with conn.cursor() as cur:
                    role = data['role']
                    if role == 'customer':
                        sql = "select * from customer where email_address = %s and password = %s;"
                    elif role == 'artist':
                        sql = "select * from artist where email_address = %s and password = %s;"
                    cur.execute(sql, (data['email_address'], data['password']))
                    rows = cur.fetchall()
                conn.commit()
            if rows:
                res = make_response(json.dumps({"code": 200, "redirect_url": url_for('index')}))
                res.set_cookie('role', data['role'])
                res.set_cookie('user', data['email_address'])
                return res
            else:
                return json.dumps({"code": 401, "redirect_url": url_for('login')})
        except pymysql.Error:
            return json.dumps({"code": 401, "redirect_url": url_for('login')})
    else:
        return render_template('login.html',
                               login_or_profile=login_or_profile,
                               sign_up_or_sign_out=sign_up_or_sign_out)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    login_or_profile, sign_up_or_sign_out = is_logged_in()
    if request.cookies.get('user'):
        return redirect(url_for('index'))
    if request.method == 'POST':
        data = request.get_json(force=True)
        conn = __connect__()
        try:
            with conn:
                with conn.cursor() as cur:
                    role = data['role']
                    if role == 'customer':
                        sql = "insert into customer " \
                              "(first_name, last_name, gender, date_of_birth, " \
                              "address_id, phone_no, password, email_address) " \
                              "values (%s, %s, %s, %s, %s, %s, %s, %s)"
                    elif role == 'artist':
                        sql = "insert into artist " \
                              "(first_name, last_name, gender, date_of_birth, " \
                              "address_id, phone_no, password, email_address) " \
                              "values (%s, %s, %s, %s, %s, %s, %s, %s)"
                    rows = cur.execute(sql, (data['first_name'],
                                             data['last_name'],
                                             data['gender'],
                                             data['date_of_birth'],
                                             data['address_id'],
                                             data['phone_number'],
                                             data['password'],
                                             data['email_address']))
                conn.commit()
            if rows:
                res = make_response(json.dumps({"code": 200, "redirect_url": url_for('index')}))
                res.set_cookie('role', data['role'])
                res.set_cookie('user', data['email_address'])
                return res
            else:
                return json.dumps({"code": 401, "redirect_url": url_for('signup')})
        except pymysql.Error as e:
            print(e)
            return json.dumps({"code": 401, "redirect_url": url_for('signup')})
    else:
        return render_template('signup.html',
                               login_or_profile=login_or_profile,
                               sign_up_or_sign_out=sign_up_or_sign_out,
                               address_list=__get_all_addresses__(),
                               country_code_list=__get_all_country_codes__())


@app.route('/profile')
def profile():
    login_or_profile, sign_up_or_sign_out = is_logged_in()
    if not request.cookies.get('user'):
        return redirect(url_for('index'))
    conn = __connect__()
    try:
        with conn:
            with conn.cursor() as cur:
                rows = cur.callproc('fetch_user_profile', (request.cookies.get('role'), request.cookies.get('user'),))
                user_profile = cur.fetchone()
            if rows:
                with conn.cursor() as cur:
                    if request.cookies.get('role') == 'customer':
                        sql = "select * from order_track where customer_id = %s"
                        order_track_rows = cur.execute(sql, (user_profile['customer_id']))
                        if order_track_rows:
                            print(cur.fetchone())
            conn.commit()
        if rows:
            if request.cookies.get('role') == 'artist':
                return render_template('profile.html',
                                       user_profile=user_profile,
                                       role=request.cookies.get('role'),
                                       login_or_profile=login_or_profile,
                                       address_list=__get_all_addresses__(),
                                       sign_up_or_sign_out=sign_up_or_sign_out,
                                       proficiency_list=__get_all_proficiencies__(),
                                       band=__get_band_details__(user_profile['artist_id']),
                                       available_artists=__get_all_available_artists__(user_profile['artist_id']))
            elif request.cookies.get('role') == 'customer':
                return render_template('profile.html',
                                       user_profile=user_profile,
                                       role=request.cookies.get('role'),
                                       login_or_profile=login_or_profile,
                                       address_list=__get_all_addresses__(),
                                       sign_up_or_sign_out=sign_up_or_sign_out)
        else:
            return render_template('profile.html')
    except pymysql.Error:
        return render_template('profile.html')


@app.route('/create_band', methods=['POST'])
def create_band():
    if request.method == 'POST':
        data = request.get_json(force=True)
        conn = __connect__()
        try:
            with conn:
                with conn.cursor() as cur:
                    sql = "insert into band (band_name) values (%s);"
                    rows = cur.execute(sql, (data["band_name"]))
                    band_id = cur.lastrowid
                    for m in data["band_members"]:
                        sql = "insert into band_artist values (%s, %s);"
                        rows = cur.execute(sql, (band_id, m))
                conn.commit()
            if rows:
                return make_response(json.dumps({"code": 200, "redirect_url": url_for('profile')}))
            else:
                return json.dumps({"code": 401, "redirect_url": url_for('profile')})
        except pymysql.Error as e:
            return json.dumps({"code": 401, "redirect_url": url_for('profile')})


@app.route('/signout')
def signout():
    res = make_response(redirect(url_for('index')))
    res.delete_cookie('role')
    res.delete_cookie('user')
    return res


@app.route('/edit_profile', methods=['POST'])
def edit_profile():
    if request.method == 'POST':
        data = request.get_json(force=True)
        conn = __connect__()
        try:
            with conn:
                with conn.cursor() as cur:
                    rows = cur.callproc('update_user_profile', (
                        data['role'],
                        data['user'],
                        data['first_name'],
                        data['last_name'],
                        data['gender'],
                        data['date_of_birth'],
                        data['address_id'],
                        data['proficiency_id']
                    ))
                conn.commit()
            if rows:
                return json.dumps({"code": 200, "redirect_url": url_for('profile')})
            else:
                return json.dumps({"code": 401, "redirect_url": url_for('profile')})
        except pymysql.Error as e:
            print(e)
            return json.dumps({"code": 401, "redirect_url": url_for('profile')})


@app.route('/delete_account', methods=['POST'])
def delete_account():
    if request.method == 'POST':
        data = request.get_json(force=True)
        conn = __connect__()
        try:
            with conn:
                with conn.cursor() as cur:
                    if data['role'] == 'customer':
                        sql = "delete from customer where email_address = %s"
                    elif data['role'] == 'artist':
                        sql = "delete from artist where email_address = %s"
                    rows = cur.execute(sql, (data['user']))
                conn.commit()
            if rows:
                res = make_response(json.dumps({"code": 200, "redirect_url": url_for('index')}))
                res.delete_cookie('role')
                res.delete_cookie('user')
            else:
                res = make_response(json.dumps({"code": 401, "redirect_url": url_for('profile')}))
        except pymysql.Error as e:
            res = make_response(json.dumps({"code": 401, "redirect_url": url_for('profile')}))
        return res


if __name__ == '__main__':
    app.run()
