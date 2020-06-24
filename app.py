from flask import Flask, Response, redirect, url_for, request, session, abort, render_template
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import sqlite3 as sql

app = Flask(__name__)

# Łukasz Szymański
# 18929, grupa 4
# Projekt PWJS

# config
app.config.update(
    DEBUG=True,
    SECRET_KEY='sekretny_klucz'
)

# ustawienie flask login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)


users = [User(id) for id in range(1, 10)]


@app.route('/')  # strona główna
def main():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute('SELECT * FROM posty WHERE usuniety=0')
    rekordy = cur.fetchall()
    return render_template('index.html', rekordy = rekordy)


@app.route('/about')  # o mnie
def omnie():
    tytul = 'O mnie'
    return render_template('omnie.html', tytul = tytul)


@app.route('/login', methods=['GET', 'POST'])  # logowanie
def login():
    tytul='Zaloguj się'
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if password == username + "_secret":
            id = username.split('user')[1]
            user = User(id)
            login_user(user)
            return redirect(url_for("main"))
        else:
            return abort(401)
    else:
        return render_template('formularz_logowania.html', tytul=tytul)


@app.errorhandler(401)  # handler błędu
def page_not_found(e):
    tytul = "Coś poszło nie tak..."
    blad = "401"
    return render_template('blad.html', tytul=tytul, blad=blad)


@app.route('/logout')  # wylogowanie
@login_required
def logout():
    logout_user()
    return render_template('logout.html')


@login_manager.user_loader  # ładowanie uzytkownika
def load_user(userid):
    return User(userid)


@app.route('/dodaj')  # dodawanie postu
@login_required
def new_pracownik():
    return render_template("add.html")


@app.route('/uzytkownik/<username>')  # widok profilu
def show_user_posts(username):
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute(f'SELECT * FROM posty WHERE autor="{username}" AND usuniety=0')
    rekordy = cur.fetchall()
    return render_template('user_posts.html', username = username, rekordy = rekordy)


@app.route('/addrec', methods=['POST', 'GET'])  # dodawanie posta
@login_required
def addrec():
    if request.method == 'POST':
        try:
            tytul = request.form['tytul']
            tresc = request.form['tresc']
            autor = current_user.name

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO posty(tytul, tresc, autor) VALUES (?, ?, ?)", (tytul, tresc, autor))
                con.commit()
                msg = "Rekord zapisany"

        except:
            con.rollback()
            msg = "Błąd przy dodawaniu rekordu"

        finally:
            return render_template("rezultat.html", msg = msg)
            con.close()


@app.route('/delrec', methods=['POST', 'GET'])  # usuwanie posta
@login_required
def delrec():
    if request.method == 'POST':
        try:
            post_id = request.form['post_id']

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(f'UPDATE posty SET usuniety=1 WHERE id={post_id}')
                con.commit()
                msg = "Usunięto post"

        except:
            con.rollback()
            msg = "Błąd podczas usuwania"

        finally:
            return render_template("rezultat.html", msg=msg)
            con.close()



@app.route('/moje')  # widok moich postow
@login_required
def my_posts():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute(f'SELECT * FROM posty WHERE autor="{current_user.name}" AND usuniety=0')
    rekordy = cur.fetchall()
    return render_template('moje.html', rekordy=rekordy)


if __name__ == '__main__':
    app.run()
