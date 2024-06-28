import pandas as pd
from email.message import EmailMessage
import ssl
import smtplib

from facerecognition import *

app.secret_key = 'veriFace'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == "csv"

@app.route('/')
def index():
    instagram = ["@rizqiardi_15","@zekothok", "@ndypriitaaa_"]
    linkedin = ["linkedin.com/in/mochrizqiardi","linkedin.com/in/zekobaharudinfirdaus","linkedin.com/in/nadyaprita"]
    github = ["iq11k", "Tocacreamy", "nadyapriitaaa"]
    nama = ["Moch. Rizqi Ardi S. B.", "Zeko Baharudin Firdaus","Nadya Prita Ramadhani"]
    gambar = ["mochiProfile.jpg","zekoProfile.jpg","NapritProfile.jpg"]
    return render_template('index.html',instagram = instagram, linkedin = linkedin, github = github,nama=nama,gambar=gambar)

def isidata(data_path):
    data = pd.read_csv(data_path)
    header = data.columns.tolist()
    if len(header) < 2:
        data = pd.read_csv(data_path, delimiter=';')
        header = data.columns.tolist()
    return data, header

@app.route('/login', methods = ['GET','POST'])
def login():
    global uname, password
    if request.method == 'POST':
        conn = dbconnection()
        myconn=conn.cursor()
        uname = request.form['uname']
        password = request.form['pw']
        query = f"SELECT username FROM akun"
        myconn.execute(query)
        result = myconn.fetchall()
        for i in result:
            if uname == i[0]:
                session["akun"] = uname
                query = f"SELECT id_akun FROM akun WHERE username = '{uname}'"
                myconn.execute(query)
                id_akun = myconn.fetchone()[0]
                session["id"] = id_akun
                query = f"SELECT password FROM akun WHERE username = '{uname}'"
                myconn.execute(query)
                result = myconn.fetchone()
                password = request.form['pw']
                if password == result[0]:
                    return redirect('/mainpage')
        flash('Incorrect username or password. Please try again.', 'error')
    return render_template('loginPage.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        conn = dbconnection()
        myconn=conn.cursor()
        uname = request.form['uname']
        password = request.form['pw']
        query = "SELECT username FROM akun"
        myconn.execute(query)
        result = myconn.fetchall()
        for i in result:
            if uname == i[0]:
                flash('*username sudah ada', 'error')
                return render_template('registerPage.html')
        query = "INSERT INTO akun(username, password) VALUES (%s, %s)"
        value = (uname,password)
        myconn.execute(query,value)
        conn.commit()
        query = f"SELECT id_akun FROM akun WHERE username = '{uname}'"
        myconn.execute(query)
        id_akun = myconn.fetchone()[0]
        session["id"] = id_akun
        return redirect('/mainpage')
    return render_template('registerPage.html')

@app.route('/mainpage', methods = ['GET', 'POST'])
def mainpage():
    if "akun" in session:
        result = geteventData()
        return render_template('mainpage.html', event = result, akun = session['akun'])
    else:
        return redirect('/login')
    
def geteventData():
    conn = dbconnection()
    myconn=conn.cursor()
    query = f"SELECT * FROM event WHERE id_akun = '{session['id']}'"
    myconn.execute(query)
    result = myconn.fetchall()
    return result


@app.route('/make-event', methods = ['GET', 'POST'])
def makeEvent():
    if "akun" in session:
        if request.method == 'POST':
            conn = dbconnection()
            myconn=conn.cursor()
            id_akun = session["id"]
            namaEvent = request.form["nama_event"]
            keterangan = request.form["keterangan"]
            jadwalMulai = request.form["jadwal_mulai"]
            jadwalSelesai = request.form["jadwal_selesai"]
            waktumasuk = request.form["waktu_datang"]
            waktuPulang = request.form["waktu_pulang"]
            warna = request.form["color"]
            query = "INSERT INTO event(nama_event, keterangan, jadwal_mulai, jadwal_selesai, waktu_masuk, waktu_pulang, warna, id_akun) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            value = (namaEvent, keterangan, jadwalMulai, jadwalSelesai, waktumasuk, waktuPulang, warna, id_akun)
            myconn.execute(query,value)
            conn.commit()
            return redirect("/mainpage")
        return render_template('base.html', akun = session['akun'])
    else:
        return redirect('/login')

def getEvent():
    conn = dbconnection()
    myconn=conn.cursor()
    query = f"SELECT * FROM event WHERE id_event = '{session['event_id']}'"
    time = datetime.now()
    date = time.strftime("%d/%m/%Y")
    currentTime = time.strftime("%H:%M")
    myconn.execute(query)
    return myconn.fetchone(), currentTime, date

@app.route('/event/<event_id>', defaults={'section': 'presensi'}, methods = ["POST","GET"])
@app.route('/event/<event_id>/<section>', methods = ["POST","GET"])
def eventPageSection(event_id,section):
    if "akun" in session:
        session["event_id"] = event_id
        result, time, date = getEvent()
        con = dbconnection()
        myconn = con.cursor()
        query = f"SELECT p.id_peserta, p.nama, p.email, p.face_id_status, k.waktu, k.tanggal_kehadiran FROM peserta AS p LEFT JOIN kehadiran AS k ON p.id_peserta = k.id_peserta WHERE id_event = '{event_id}'"
        myconn.execute(query)
        data = myconn.fetchall()
        query = f"SELECT waktu_masuk FROM event WHERE id_event = '{event_id}'"
        myconn.execute(query)
        waktumasuk = myconn.fetchone()[0]
        query = f"SELECT DISTINCT k.tanggal_kehadiran FROM kehadiran AS k JOIN peserta AS p ON p.id_peserta = k.id_peserta  WHERE p.id_event = '{event_id}'"
        myconn.execute(query)
        tanggal_hadir = myconn.fetchall()
        if section == 'data':
            if request.method == 'POST':
                hadir = request.form.get('waktu_hadir')
                if hadir == 'none':
                    print("ga ngapa-ngapain")
                else:
                    hadir_waktu = datetime.strptime(hadir, '%d-%m-%Y').date()
                    query = f"SELECT p.id_peserta, p.nama, p.email, p.face_id_status, k.waktu, k.tanggal_kehadiran FROM peserta AS p LEFT JOIN kehadiran AS k ON p.id_peserta = k.id_peserta WHERE id_event = '{event_id}' AND k.tanggal_kehadiran = '{hadir_waktu}'"
                    myconn.execute(query)
                    data = myconn.fetchall()
                    print(":naprit ngabsen")
                    print(hadir_waktu)
        status = []
        for set in data:
            if set[4] == None:
                if section == 'data':
                    status.append("Tidak Hadir")
                if section == 'orang':
                    status.append("belum Hadir")
            elif set[4] == waktumasuk:
                status.append("Tepat waktu")
            elif set[4] > waktumasuk:
                status.append("telat")
            else:
                status.append("lebih awal")
        dataSetLength = len(data)
        query = f"SELECT nama, email FROM peserta WHERE id_event = '{event_id}'"
        myconn.execute(query)
        dataeditable = myconn.fetchall()
        path_status = 1
        if not os.path.isdir("static/faces/" + event_id):
            path_status = 0
        return render_template("eventpage.html", info = result, event = geteventData(), section = section, time = time, date = date, 
                            dataset = data, akun = session['akun'], status = status, dataSetLength = dataSetLength, editData = dataeditable, 
                            tanggal_hadir = tanggal_hadir, event_id = event_id, path_status = path_status)
    else:
        return redirect('/login')
    
@app.route('/importdata', methods = ['POST','GET'])
def importData():
    if "akun" in session:
        if request.method == 'POST':
            if 'dataset' not in request.files:
                flash('No file part')
                return redirect(f"/event/{session['event_id']}/orang")
            file = request.files['dataset']
            if file.filename == '':
                flash('No selected file')
                return redirect(f"/event/{session['event_id']}/orang")
            if file and allowed_file(file.filename):
                filename = f"uploads/{file.filename}"
                session['filename'] = filename
                file.save(filename)
                conn = dbconnection()
                myconn = conn.cursor()
                query = f"UPDATE event SET `filename` = '{filename}' WHERE id_event = {session['event_id']}"
                myconn.execute(query)

                dataset, header = isidata(filename)
                dataList = dataset.values.tolist()
                header = list(map(str.lower, header))
                index = [header.index('nama'),header.index('email')]
                query = "INSERT INTO peserta(nama,email,id_event) VALUES (%s,%s,%s)"
                listNama = [row[index[0]] for row in dataList]
                listEmail = [row[index[1]] for row in dataList]
                values = [(listNama[i], listEmail[i], session['event_id']) for i in range(len(listNama))]
                myconn.executemany(query,values)
                conn.commit()
            else:
                flash('Allowed file types are csv')
                return redirect(f"/event/{session['event_id']}/orang")
        return redirect(f"/event/{session['event_id']}/orang")
    else:
        return redirect("/login")
    
@app.route('/setting', methods = ["POST"])
def setting():
    if "akun" in session:
        if request.method == "POST":
            conn = dbconnection()
            myconn=conn.cursor()
            id_akun = session["id"]
            namaEvent = request.form["nama_event"]
            keterangan = request.form["keterangan"]
            jadwalMulai = request.form["jadwal_mulai"]
            jadwalSelesai = request.form["jadwal_selesai"]
            waktumasuk = request.form["waktu_datang"]
            waktuPulang = request.form["waktu_pulang"]
            warna = request.form["color"]
            query = f"UPDATE event SET nama_event = '{namaEvent}', keterangan = '{keterangan}', jadwal_mulai = '{jadwalMulai}', jadwal_selesai = '{jadwalSelesai}', waktu_masuk = '{waktumasuk}', waktu_pulang = '{waktuPulang}', warna = '{warna}' WHERE event.id_event = {session['event_id']}"
            myconn.execute(query)
            conn.commit()
            return redirect(f"/event/{session['event_id']}/pengaturan")
    else:
        return redirect("/login")

@app.route('/video_feed/<mode>')
def video_feed(mode):
    if mode == 'tambah':
        return Response(tambah(session['id_peserta'], getname(session['id_peserta']), session['event_id']), mimetype='multipart/x-mixed-replace; boundary=frame')
    if mode == 'cek': 
        return Response(cek(session['event_id']), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/presensi',defaults={'mode': 'cek','id': '0'})
@app.route('/presensi/<mode>/<user_id>')
def customEvent(mode,user_id):
    eventId = session["event_id"]
    list_hadir, list_nama = get_atendance(eventId)
    if mode == 'tambah':
        session['id_peserta'] = user_id
        conn = dbconnection()
        myconn = conn.cursor()
        query = f"SELECT nama FROM peserta WHERE `id_peserta` = {user_id}"
        myconn.execute(query)
        nama = myconn.fetchone()[0]
        return render_template('presensi.html', mode = mode, nama = nama, list_hadir = list_hadir, event_id = session['event_id'])  
    if mode == 'cek':
        return render_template('presensi.html', mode = mode, list_hadir = list_hadir, event_id = session['event_id']) 

@app.route('/video_feed_ready')
def video_feed_ready():
    camera = cv2.VideoCapture(0)
    if camera.isOpened():
        return jsonify(ready=True)
    else:
        return jsonify(ready=False)

@app.route("/log-out")
def logout():
    session.clear()
    return redirect("/")

@app.route("/export")
def expert():
    conn = dbconnection()
    myconn = conn.cursor()
    query = f"SELECT p.id_peserta, p.nama, p.email, p.face_id_status, k.waktu FROM peserta AS p LEFT JOIN kehadiran AS k ON p.id_peserta = k.id_peserta WHERE id_event = '{session['event_id']}'"
    myconn.execute(query)
    dataset = myconn.fetchall()    
    query = f"SELECT waktu_masuk FROM event WHERE id_event = '{session['event_id']}'"
    myconn.execute(query)
    waktumasuk = myconn.fetchone()[0]
    query = f"SELECT nama_event FROM event WHERE id_event = '{session['event_id']}'"
    myconn.execute(query)
    namaEvent = myconn.fetchone()[0]
    
    listNama = []
    listEmail = []
    listStatus = []
    listWaktu = []
    for set in dataset:
            if set[4] == None:
                listStatus.append("belum")
            elif set[4] == waktumasuk:
                listStatus.append("Tepat waktu")
            elif set[4] > waktumasuk:
                listStatus.append("telat")
            else:
                listStatus.append("Tidak Hadir")

    for data in dataset:
        listNama.append(data[1])
        listEmail.append(data[2])
        if data[4] is not None:
            total_seconds = int(data[4].total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            listWaktu.append(f'{hours:02}:{minutes:02}:{seconds:02}')
        else:
            listWaktu.append("-")

    data = {
        'Nama': listNama,
        'Email': listEmail,
        'Status': listStatus,
        'Waktu kehadiran': listWaktu
    }

    df = pd.DataFrame(data)
    filename = namaEvent + "data.xlsx"
    session['filename'] = filename
    df.to_excel(filename, index=False)
    flash('data berhasil di export', 'berhasil')
    return redirect(f"/download")

@app.route('/download')
def downloadFile ():
    path = f"{session['filename']}"
    return send_file(path, as_attachment=True)

@app.route("/hapus/<idPeserta>")
def hapusPeserta(idPeserta):
    conn = dbconnection()
    myconn = conn.cursor()
    query = f"DELETE FROM peserta WHERE `peserta`.`id_peserta` = {idPeserta}"
    myconn.execute(query)
    conn.commit()
    return redirect(f"/event/{session['event_id']}/orang")

@app.route("/editpeserta/<id_peserta>", methods=["POST"])
def editPeserta(id_peserta):
    if request.method == 'POST':
        nama = request.form["namaPeserta"]
        email = request.form["emailPeserta"]
        conn = dbconnection()
        myconn = conn.cursor()
        query = f"UPDATE `peserta` SET `nama` = '{nama}', `email` = '{email}' WHERE id_peserta = {id_peserta}"
        myconn.execute(query)
        conn.commit()
        return redirect(f"/event/{session['event_id']}/orang")

@app.route("/send-email")
def sendEmail():
    sender = 'naprittt@gmail.com'
    password_sender = 'dyuutrhztnilbypv'
    receiver = []
    conn = dbconnection()
    myconn = conn.cursor()
    query = f"SELECT `email` FROM peserta WHERE id_event = '{session['event_id']}'"
    myconn.execute(query)
    daftarEmail = myconn.fetchall()
    for email in daftarEmail:
        receiver.append(email)
    subject = 'subject testing veriface'
    body = 'bismilah jadi'

    em = EmailMessage()
    em['From'] = sender
    em['To'] = receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, password_sender)
        for email in receiver:
            smtp.sendmail(sender, email, em.as_string())

    return redirect(f"/event/{session['event_id']}/orang")

@app.route("/tambah-peserta", methods=["POST"])
def tambahPeserta():
    if request.method == 'POST':
        nama = request.form["namaPeserta"]
        email = request.form["emailPeserta"]
        print("Bisa tambah")
        conn = dbconnection()
        myconn = conn.cursor()
        query = f"INSERT INTO `peserta` (`nama`, `email`, `face_id_status`, `id_event`) VALUES ('{nama}', '{email}', '0', '{session['event_id']}')"
        myconn.execute(query)
        conn.commit()
        return redirect(f"/event/{session['event_id']}/orang")
    
if __name__ == '__main__':
    app.run(debug=True)
