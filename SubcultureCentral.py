from unicodedata import name

from flask import Flask, render_template, request, redirect
import mariadb
import sys

SubcultureCentral = Flask(__name__)

def connection():
    conn = mariadb.connect(
        user="remoto",
        password="remoto",
        host="192.168.1.132",
        port=3306,
        database="SubcultureCentral"
    )
    return conn

@SubcultureCentral.route("/")
def main():
    artista = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM artista")
    for row in cursor.fetchall():
        artista.append({"id_artista": row[0], "nombre_artistico": row[1], "nombre_real": row[2], "genero_principal": row[3], "subgenero": row[4], "pais": row[5], "enlaces_sociales": row[6], "cache": row[7]})
    conn.close()
    return render_template("SubcultureCentral.html", artista = artista)

#artista

# LISTA DE ARTISTAS
@SubcultureCentral.route("/artistas")
def artistas():
    artista = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM artista")
    for row in cursor.fetchall():
        artista.append({
            "id_artista": row[0],
            "nombre_artistico": row[1],
            "nombre_real": row[2],
            "genero_principal": row[3],
            "subgenero": row[4],
            "pais": row[5],
            "enlaces_sociales": row[6],
            "cache": row[7]
        })
    conn.close()
    return render_template("artistas.html", artista=artista)


# AÑADIR ARTISTA
@SubcultureCentral.route("/addartist", methods=['GET','POST'])
def addartist():
    if request.method == 'GET':
        return render_template("addartist.html")

    conn = connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO artista (nombre_artistico, nombre_real, genero_principal, subgenero, pais, enlaces_sociales, cache)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        request.form["nombre_artistico"],
        request.form["nombre_real"],
        request.form["genero_principal"],
        request.form["subgenero"],
        request.form["pais"],
        request.form["enlaces_sociales"],
        request.form["cache"]
    ))
    conn.commit()
    conn.close()
    return redirect("/artistas")


# EDITAR ARTISTA
@SubcultureCentral.route("/updateartist/<int:id>", methods=['GET','POST'])
def updateartist(id):
    conn = connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM artista WHERE id_artista=?", (id,))
    row = cursor.fetchone()
    artist = {
        "id_artista": row[0],
        "nombre_artistico": row[1],
        "nombre_real": row[2],
        "genero_principal": row[3],
        "subgenero": row[4],
        "pais": row[5],
        "enlaces_sociales": row[6],
        "cache": row[7]
    }

    if request.method == 'GET':
        conn.close()
        return render_template("addartist.html", artist=artist)

    cursor.execute("""
        UPDATE artista SET nombre_artistico=?, nombre_real=?, genero_principal=?, subgenero=?, pais=?, enlaces_sociales=?, cache=?
        WHERE id_artista=?
    """, (
        request.form["nombre_artistico"],
        request.form["nombre_real"],
        request.form["genero_principal"],
        request.form["subgenero"],
        request.form["pais"],
        request.form["enlaces_sociales"],
        request.form["cache"],
        id
    ))
    conn.commit()
    conn.close()
    return redirect("/artistas")


# ELIMINAR ARTISTA
@SubcultureCentral.route("/deleteartist/<int:id>")
def deleteartist(id):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM artista WHERE id_artista=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/artistas")


#evento

@SubcultureCentral.route("/evento")
def evento():
    eventos = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM evento")
    for row in cursor.fetchall():
        eventos.append({
            "id_evento": row[0],
            "titulo": row[1],
            "descripcion": row[2],
            "fecha": row[3],
            "hora_inicio": row[4],
            "hora_fin": row[5],
            "id_ubicacion": row[6],
            "tipo_evento": row[7],
            "estado": row[8]
        })
    conn.close()
    return render_template("evento.html", evento=eventos)


@SubcultureCentral.route("/addevento", methods=['GET','POST'])
def addevento():
    conn = connection()
    cursor = conn.cursor()

    # cargar ubicaciones para el select
    cursor.execute("SELECT id_ubicacion, nombre FROM ubicacion")
    ubicaciones = [{"id_ubicacion": u[0], "nombre": u[1]} for u in cursor.fetchall()]

    if request.method == 'GET':
        conn.close()
        return render_template("addevento.html", ubicaciones=ubicaciones)

    if request.method == 'POST':
        cursor.execute("""
            INSERT INTO evento (titulo, descripcion, fecha, hora_inicio, hora_fin, id_ubicacion, tipo_evento, estado)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            request.form["titulo"],
            request.form["descripcion"],
            request.form["fecha"],
            request.form["hora_inicio"],
            request.form["hora_fin"],
            request.form["id_ubicacion"] or None,
            request.form["tipo_evento"],
            request.form["estado"]
        ))
        conn.commit()
        conn.close()
        return redirect("/evento")


@SubcultureCentral.route("/updateevento/<int:id>", methods=['GET','POST'])
def updateevento(id):
    conn = connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM evento WHERE id_evento=?", (id,))
    row = cursor.fetchone()
    evento = {
        "id_evento": row[0],
        "titulo": row[1],
        "descripcion": row[2],
        "fecha": row[3],
        "hora_inicio": row[4],
        "hora_fin": row[5],
        "id_ubicacion": row[6],
        "tipo_evento": row[7],
        "estado": row[8]
    }

    cursor.execute("SELECT id_ubicacion, nombre FROM ubicacion")
    ubicaciones = [{"id_ubicacion": u[0], "nombre": u[1]} for u in cursor.fetchall()]

    if request.method == 'GET':
        conn.close()
        return render_template("addevento.html", evento=evento, ubicaciones=ubicaciones)

    if request.method == 'POST':
        cursor.execute("""
            UPDATE evento SET titulo=?, descripcion=?, fecha=?, hora_inicio=?, hora_fin=?, 
            id_ubicacion=?, tipo_evento=?, estado=? WHERE id_evento=?
        """, (
            request.form["titulo"],
            request.form["descripcion"],
            request.form["fecha"],
            request.form["hora_inicio"],
            request.form["hora_fin"],
            request.form["id_ubicacion"] or None,
            request.form["tipo_evento"],
            request.form["estado"],
            id
        ))
        conn.commit()
        conn.close()
        return redirect("/evento")


@SubcultureCentral.route("/deleteevento/<int:id>")
def deleteevento(id):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM evento WHERE id_evento=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/evento")

#merch

@SubcultureCentral.route("/merch")
def merch():
    merch_list = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM merch")
    for row in cursor.fetchall():
        merch_list.append({
            "id_merch": row[0],
            "id_artista": row[1],
            "nombre_item": row[2],
            "precio": row[3],
            "stock": row[4],
            "tipo": row[5]
        })
    conn.close()
    return render_template("merch.html", merch=merch_list)


@SubcultureCentral.route("/addmerch", methods=['GET','POST'])
def addmerch():
    conn = connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id_artista, nombre_artistico FROM artista")
    artistas = [{"id_artista": a[0], "nombre_artistico": a[1]} for a in cursor.fetchall()]

    if request.method == 'GET':
        conn.close()
        return render_template("addmerch.html", artistas=artistas)

    if request.method == 'POST':
        cursor.execute("""
            INSERT INTO merch (id_artista, nombre_item, precio, stock, tipo)
            VALUES (?, ?, ?, ?, ?)
        """, (
            request.form["id_artista"],
            request.form["nombre_item"],
            request.form["precio"],
            request.form["stock"],
            request.form["tipo"]
        ))
        conn.commit()
        conn.close()
        return redirect("/merch")


@SubcultureCentral.route("/updatemerch/<int:id>", methods=['GET','POST'])
def updatemerch(id):
    conn = connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM merch WHERE id_merch=?", (id,))
    row = cursor.fetchone()
    merch = {
        "id_merch": row[0],
        "id_artista": row[1],
        "nombre_item": row[2],
        "precio": row[3],
        "stock": row[4],
        "tipo": row[5]
    }

    cursor.execute("SELECT id_artista, nombre_artistico FROM artista")
    artistas = [{"id_artista": a[0], "nombre_artistico": a[1]} for a in cursor.fetchall()]

    if request.method == 'GET':
        conn.close()
        return render_template("addmerch.html", merch=merch, artistas=artistas)

    if request.method == 'POST':
        cursor.execute("""
            UPDATE merch SET id_artista=?, nombre_item=?, precio=?, stock=?, tipo=?
            WHERE id_merch=?
        """, (
            request.form["id_artista"],
            request.form["nombre_item"],
            request.form["precio"],
            request.form["stock"],
            request.form["tipo"],
            id
        ))
        conn.commit()
        conn.close()
        return redirect("/merch")


@SubcultureCentral.route("/deletemerch/<int:id>")
def deletemerch(id):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM merch WHERE id_merch=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/merch")


#patro

@SubcultureCentral.route("/patrocinador")
def patrocinador():
    lista = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patrocinador")
    for row in cursor.fetchall():
        lista.append({
            "id_patrocinador": row[0],
            "nombre": row[1],
            "tipo": row[2],
            "contacto": row[3],
            "enlace_web": row[4]
        })
    conn.close()
    return render_template("patrocinador.html", patrocinador=lista)


@SubcultureCentral.route("/addpatrocinador", methods=['GET','POST'])
def addpatrocinador():
    if request.method == 'GET':
        return render_template("addpatrocinador.html")

    conn = connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO patrocinador (nombre, tipo, contacto, enlace_web)
        VALUES (?, ?, ?, ?)
    """, (
        request.form["nombre"],
        request.form["tipo"],
        request.form["contacto"],
        request.form["enlace_web"]
    ))
    conn.commit()
    conn.close()
    return redirect("/patrocinador")


@SubcultureCentral.route("/updatepatrocinador/<int:id>", methods=['GET','POST'])
def updatepatrocinador(id):
    conn = connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patrocinador WHERE id_patrocinador=?", (id,))
    row = cursor.fetchone()
    patrocinador = {
        "id_patrocinador": row[0],
        "nombre": row[1],
        "tipo": row[2],
        "contacto": row[3],
        "enlace_web": row[4]
    }

    if request.method == 'GET':
        conn.close()
        return render_template("addpatrocinador.html", patrocinador=patrocinador)

    if request.method == 'POST':
        cursor.execute("""
            UPDATE patrocinador SET nombre=?, tipo=?, contacto=?, enlace_web=?
            WHERE id_patrocinador=?
        """, (
            request.form["nombre"],
            request.form["tipo"],
            request.form["contacto"],
            request.form["enlace_web"],
            id
        ))
        conn.commit()
        conn.close()
        return redirect("/patrocinador")


@SubcultureCentral.route("/deletepatrocinador/<int:id>")
def deletepatrocinador(id):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patrocinador WHERE id_patrocinador=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/patrocinador")

#ticket

@SubcultureCentral.route("/ticket")
def ticket():
    lista = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ticket")
    for row in cursor.fetchall():
        lista.append({
            "id_ticket": row[0],
            "id_evento": row[1],
            "tipo": row[2],
            "precio": row[3],
            "estado": row[4],
            "codigo_qr": row[5]
        })
    conn.close()
    return render_template("ticket.html", ticket=lista)


@SubcultureCentral.route("/addticket", methods=['GET','POST'])
def addticket():
    conn = connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id_evento, titulo FROM evento")
    eventos = [{"id_evento": e[0], "titulo": e[1]} for e in cursor.fetchall()]

    if request.method == 'GET':
        conn.close()
        return render_template("addticket.html", eventos=eventos)

    cursor.execute("""
        INSERT INTO ticket (id_evento, tipo, precio, estado, codigo_qr)
        VALUES (?, ?, ?, ?, ?)
    """, (
        request.form["id_evento"],
        request.form["tipo"],
        request.form["precio"],
        request.form["estado"],
        request.form["codigo_qr"]
    ))
    conn.commit()
    conn.close()
    return redirect("/ticket")


@SubcultureCentral.route("/updateticket/<int:id>", methods=['GET','POST'])
def updateticket(id):
    conn = connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM ticket WHERE id_ticket=?", (id,))
    row = cursor.fetchone()
    ticket = {
        "id_ticket": row[0],
        "id_evento": row[1],
        "tipo": row[2],
        "precio": row[3],
        "estado": row[4],
        "codigo_qr": row[5]
    }

    cursor.execute("SELECT id_evento, titulo FROM evento")
    eventos = [{"id_evento": e[0], "titulo": e[1]} for e in cursor.fetchall()]

    if request.method == 'GET':
        conn.close()
        return render_template("addticket.html", ticket=ticket, eventos=eventos)

    cursor.execute("""
        UPDATE ticket SET id_evento=?, tipo=?, precio=?, estado=?, codigo_qr=?
        WHERE id_ticket=?
    """, (
        request.form["id_evento"],
        request.form["tipo"],
        request.form["precio"],
        request.form["estado"],
        request.form["codigo_qr"],
        id
    ))
    conn.commit()
    conn.close()
    return redirect("/ticket")


@SubcultureCentral.route("/deleteticket/<int:id>")
def deleteticket(id):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ticket WHERE id_ticket=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/ticket")

#ubicacion

@SubcultureCentral.route("/ubicacion")
def ubicacion():
    lista = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ubicacion")
    for row in cursor.fetchall():
        lista.append({
            "id_ubicacion": row[0],
            "nombre": row[1],
            "direccion": row[2],
            "ciudad": row[3],
            "capacidad": row[4],
            "coordenadas_gps": row[5]
        })
    conn.close()
    return render_template("ubicacion.html", ubicacion=lista)


@SubcultureCentral.route("/addubicacion", methods=['GET','POST'])
def addubicacion():
    if request.method == 'GET':
        return render_template("addubicacion.html")

    conn = connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ubicacion (nombre, direccion, ciudad, capacidad, coordenadas_gps)
        VALUES (?, ?, ?, ?, ?)
    """, (
        request.form["nombre"],
        request.form["direccion"],
        request.form["ciudad"],
        request.form["capacidad"],
        request.form["coordenadas_gps"]
    ))
    conn.commit()
    conn.close()
    return redirect("/ubicacion")


@SubcultureCentral.route("/updateubicacion/<int:id>", methods=['GET','POST'])
def updateubicacion(id):
    conn = connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM ubicacion WHERE id_ubicacion=?", (id,))
    row = cursor.fetchone()
    ubicacion = {
        "id_ubicacion": row[0],
        "nombre": row[1],
        "direccion": row[2],
        "ciudad": row[3],
        "capacidad": row[4],
        "coordenadas_gps": row[5]
    }

    if request.method == 'GET':
        conn.close()
        return render_template("addubicacion.html", ubicacion=ubicacion)

    cursor.execute("""
        UPDATE ubicacion SET nombre=?, direccion=?, ciudad=?, capacidad=?, coordenadas_gps=?
        WHERE id_ubicacion=?
    """, (
        request.form["nombre"],
        request.form["direccion"],
        request.form["ciudad"],
        request.form["capacidad"],
        request.form["coordenadas_gps"],
        id
    ))
    conn.commit()
    conn.close()
    return redirect("/ubicacion")


@SubcultureCentral.route("/deleteubicacion/<int:id>")
def deleteubicacion(id):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ubicacion WHERE id_ubicacion=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/ubicacion")

#equipo

@SubcultureCentral.route("/solicitud_equipo_musica")
def solicitud_equipo_musica():
    lista = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM solicitud_equipo_musica")
    for row in cursor.fetchall():
        lista.append({
            "id_solicitud": row[0],
            "id_evento": row[1],
            "nombre_item": row[2],
            "cantidad": row[3],
            "estado": row[4]
        })
    conn.close()
    return render_template("solicitud_equipo_musica.html", solicitud_equipo_musica=lista)


@SubcultureCentral.route("/addsolicitud_equipo_musica", methods=['GET','POST'])
def addsolicitud_equipo_musica():
    conn = connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id_evento, titulo FROM evento")
    eventos = [{"id_evento": e[0], "titulo": e[1]} for e in cursor.fetchall()]

    if request.method == 'GET':
        conn.close()
        return render_template("addsolicitud_equipo_musica.html", eventos=eventos)

    cursor.execute("""
        INSERT INTO solicitud_equipo_musica (id_evento, nombre_item, cantidad, estado)
        VALUES (?, ?, ?, ?)
    """, (
        request.form["id_evento"],
        request.form["nombre_item"],
        request.form["cantidad"],
        request.form["estado"]
    ))
    conn.commit()
    conn.close()
    return redirect("/solicitud_equipo_musica")


@SubcultureCentral.route("/updatesolicitud_equipo_musica/<int:id>", methods=['GET','POST'])
def updatesolicitud_equipo_musica(id):
    conn = connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM solicitud_equipo_musica WHERE id_solicitud=?", (id,))
    row = cursor.fetchone()
    solicitud = {
        "id_solicitud": row[0],
        "id_evento": row[1],
        "nombre_item": row[2],
        "cantidad": row[3],
        "estado": row[4]
    }

    cursor.execute("SELECT id_evento, titulo FROM evento")
    eventos = [{"id_evento": e[0], "titulo": e[1]} for e in cursor.fetchall()]

    if request.method == 'GET':
        conn.close()
        return render_template("addsolicitud_equipo_musica.html", solicitud=solicitud, eventos=eventos)

    cursor.execute("""
        UPDATE solicitud_equipo_musica SET id_evento=?, nombre_item=?, cantidad=?, estado=?
        WHERE id_solicitud=?
    """, (
        request.form["id_evento"],
        request.form["nombre_item"],
        request.form["cantidad"],
        request.form["estado"],
        id
    ))
    conn.commit()
    conn.close()
    return redirect ("/solicitud_equipo_musica")

@SubcultureCentral.route("/deletesolicitud_equipo_musica/<int:id>")
def deletesolicitud_equipo_musica(id):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM solicitud_equipo_musica WHERE id_solicitud=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/solicitud_equipo_musica")

#artista

@SubcultureCentral.route("/evento_artista")
def evento_artista():
    lista = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM evento_artista")
    for row in cursor.fetchall():
        lista.append({
            "id_evento_artista": row[0],
            "id_evento": row[1],
            "id_artista": row[2],
            "slot_inicio": row[3],
            "slot_fin": row[4],
            "orden": row[5]
        })
    conn.close()
    return render_template("evento_artista.html", evento_artista=lista)


@SubcultureCentral.route("/addevento_artista", methods=['GET','POST'])
def addevento_artista():
    conn = connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id_evento, titulo FROM evento")
    eventos = [{"id_evento": e[0], "titulo": e[1]} for e in cursor.fetchall()]

    cursor.execute("SELECT id_artista, nombre_artistico FROM artista")
    artistas = [{"id_artista": a[0], "nombre_artistico": a[1]} for a in cursor.fetchall()]

    if request.method == 'GET':
        conn.close()
        return render_template("addevento_artista.html", eventos=eventos, artistas=artistas)

    cursor.execute("""
        INSERT INTO evento_artista (id_evento, id_artista, slot_inicio, slot_fin, orden)
        VALUES (?, ?, ?, ?, ?)
    """, (
        request.form["id_evento"],
        request.form["id_artista"],
        request.form["slot_inicio"],
        request.form["slot_fin"],
        request.form["orden"]
    ))
    conn.commit()
    conn.close()
    return redirect("/evento_artista")


@SubcultureCentral.route("/updateevento_artista/<int:id>", methods=['GET','POST'])
def updateevento_artista(id):
    conn = connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM evento_artista WHERE id_evento_artista=?", (id,))
    row = cursor.fetchone()
    ea = {
        "id_evento_artista": row[0],
        "id_evento": row[1],
        "id_artista": row[2],
        "slot_inicio": row[3],
        "slot_fin": row[4],
        "orden": row[5]
    }

    cursor.execute("SELECT id_evento, titulo FROM evento")
    eventos = [{"id_evento": e[0], "titulo": e[1]} for e in cursor.fetchall()]

    cursor.execute("SELECT id_artista, nombre_artistico FROM artista")
    artistas = [{"id_artista": a[0], "nombre_artistico": a[1]} for a in cursor.fetchall()]

    if request.method == 'GET':
        conn.close()
        return render_template("addevento_artista.html", ea=ea, eventos=eventos, artistas=artistas)

    cursor.execute("""
        UPDATE evento_artista SET id_evento=?, id_artista=?, slot_inicio=?, slot_fin=?, orden=?
        WHERE id_evento_artista=?
    """, (
        request.form["id_evento"],
        request.form["id_artista"],
        request.form["slot_inicio"],
        request.form["slot_fin"],
        request.form["orden"],
        id
    ))
    conn.commit()
    conn.close()
    return redirect("/evento_artista")


@SubcultureCentral.route("/deleteevento_artista/<int:id>")
def deleteevento_artista(id):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM evento_artista WHERE id_evento_artista=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/evento_artista")

#patro

@SubcultureCentral.route("/evento_patrocinador")
def evento_patrocinador():
    lista = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM evento_patrocinador")
    for row in cursor.fetchall():
        lista.append({
            "id_evento_patro": row[0],
            "id_evento": row[1],
            "id_patrocinador": row[2],
            "aporte": row[3]
        })
    conn.close()
    return render_template("evento_patrocinador.html", evento_patrocinador=lista)


@SubcultureCentral.route("/addevento_patrocinador", methods=['GET','POST'])
def addevento_patrocinador():
    conn = connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id_evento, titulo FROM evento")
    eventos = [{"id_evento": e[0], "titulo": e[1]} for e in cursor.fetchall()]

    cursor.execute("SELECT id_patrocinador, nombre FROM patrocinador")
    patrocinadores = [{"id_patrocinador": p[0], "nombre": p[1]} for p in cursor.fetchall()]

    if request.method == 'GET':
        conn.close()
        return render_template("addevento_patrocinador.html", eventos=eventos, patrocinadores=patrocinadores)

    cursor.execute("""
        INSERT INTO evento_patrocinador (id_evento, id_patrocinador, aporte)
        VALUES (?, ?, ?)
    """, (
        request.form["id_evento"],
        request.form["id_patrocinador"],
        request.form["aporte"]
    ))
    conn.commit()
    conn.close()
    return redirect("/evento_patrocinador")


@SubcultureCentral.route("/updateevento_patrocinador/<int:id>", methods=['GET','POST'])
def updateevento_patrocinador(id):
    conn = connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM evento_patrocinador WHERE id_evento_patro=?", (id,))
    row = cursor.fetchone()
    ep = {
        "id_evento_patro": row[0],
        "id_evento": row[1],
        "id_patrocinador": row[2],
        "aporte": row[3]
    }

    cursor.execute("SELECT id_evento, titulo FROM evento")
    eventos = [{"id_evento": e[0], "titulo": e[1]} for e in cursor.fetchall()]

    cursor.execute("SELECT id_patrocinador, nombre FROM patrocinador")
    patrocinadores = [{"id_patrocinador": p[0], "nombre": p[1]} for p in cursor.fetchall()]

    if request.method == 'GET':
        conn.close()
        return render_template("addevento_patrocinador.html", ep=ep, eventos=eventos, patrocinadores=patrocinadores)

    cursor.execute("""
        UPDATE evento_patrocinador SET id_evento=?, id_patrocinador=?, aporte=?
        WHERE id_evento_patro=?
    """, (
        request.form["id_evento"],
        request.form["id_patrocinador"],
        request.form["aporte"],
        id
    ))
    conn.commit()
    conn.close()
    return redirect("/evento_patrocinador")


@SubcultureCentral.route("/deleteevento_patrocinador/<int:id>")
def deleteevento_patrocinador(id):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM evento_patrocinador WHERE id_evento_patro=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/evento_patrocinador")



if(__name__ == "__main__"):
    SubcultureCentral.run(debug=True)