from flask import Flask, render_template, request, jsonify, url_for, redirect, session, g
import sqlite3

app = Flask(__name__)

# gunakan config
# config bisa untuk debug atau untuk secret key yang fungsinya utk menghindari malware karena dapat dilihat di cookies

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'Thisshoukdberandomandsecret'


# pertama koneksikan ke database
def connect_db():
    sql = sqlite3.connect(
        'D:\\Programming\\Flask_udemy\\FLASK\\database\\test.db')
    # di bawah ini utk mengubah tupple menjadi dictionary
    sql.row_factory = sqlite3.Row
    return sql

# lalu ambil datarbase


def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

# lalu tutup database ?


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

# method digunakan utk bagaimana cara url tsb diterima oleh komputer
# GET = akan nampak diurl
# POST = tidak tampak diurl

# ini mereset nama


@app.route('/')
def index():
    session.pop('name', None)
    return "<h1>Hello world</h1>"

# ini untuk mengambil nama


@app.route('/home', methods=['GET', 'POST'], defaults={'name': 'Default'})
@app.route("/home/<string:name>", methods=["GET", "POST"])
def home(name):
    session['name'] = name
    db = get_db()
    cur = db.execute("select id, name, satker, bidang from users")
    result = cur.fetchall()
    return render_template('home.html', name=name, display=False, listoflist=[1, 2, 3, 4, 5], listofdicts=[{"name": "efje", "age": "23"}, {"name": "Aulia"}], result=result)

# ini untuk menampilkan nama


@app.route("/json")
def json():
    if 'name' in session:
        name = session['name']
    else:
        name = 'nonameinthesession'
    return jsonify({"Key": "Value", "Key2": [2, 5, 7, 9], 'name': name})

# ini untuk mengambil data langsung dari url, cara gunanya : serelah / gunakan ? lalu key dan valuenya ditambah & key dan value lainnya. contoh :
# /query?name=EFJE&location=Bengkulu


@app.route('/query')
def query():
    name = request.args.get('name')
    location = request.args.get('location')
    return f"hi {name} you are from {location}"

# mengambil data dari form


@app.route('/theform')
def theform():
    return render_template('index.html')

# @app.route("/process", methods=["POST"])
# def process():
#     name = request.form['name']
#     location = request.form['location']
#     return f"<h1> Hi {name} you are from {location}, your form has been submitted</h1>"

# mengambil data dari json


@app.route("/processjson", methods=["POST"])
def processjson():
    data = request.get_json()
    name = data['name']
    location = data['location']
    randomlist = data['randomlist']
    return jsonify({"result": "success", "name": name, "location": location, "randomkeyinlist": randomlist[0]})

# mengambil data dari form tapi hanya mengambil 1 url
# gunakan if statement


@app.route("/theform2", methods=["GET", "POST"])
def theform2():
    if request.method == "GET":
        # gunakan render_template untuk memanggil html
        return render_template('index.html')
    else:
        name = request.form['name']
        satker = request.form['satker']
        bidang = request.form['bidang']

        db = get_db()
        db.execute('insert into users(name,satker,bidang) values (?,?,?)', [
                   name, satker, bidang])
        db.commit()
        # return f"<h1>hello {name} you are from {location}</h1>"

        # bisa menggunakan redirect jika ingin mengubahnya menjadi url lain. dengan memanggil nama fungsi
        return redirect(url_for('home', name=name, satker=satker, bidang=bidang))


@app.route('/viewdb')
def viewdb():
    db = get_db()
    cur = db.execute('select id, name, satker, bidang from users')
    result = cur.fetchall()
    return f"<h1> selamat datang {result[3]['name']}. {result[3]['satker']} ada beberapa berkas yang gagal cetak SPM semuanya ada di bagian {result[3]['bidang']}</h1>"


if __name__ == "__main__":
    app.run()
