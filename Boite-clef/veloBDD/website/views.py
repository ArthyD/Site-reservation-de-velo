from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
from .models import User, Reservation, Velo, Historique
import socket
from datetime import datetime
from sqlalchemy import func
from BotDiscord.bdd_bike_bot import runBot
import asyncio

views = Blueprint('views', __name__)
UDP_IP = "10.18.5.8"
UDP_PORT = 2390
MESSAGE = "ouvre"

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # On initialise les objets
    nom = current_user.nom
    user = User.query.filter_by(nom=nom).first()
    resa = Reservation.query.filter_by(id_user=user.id).first()
    bikes = Velo.query.all()
    if resa.id_velo == None:
        resa.id_velo = 0
        db.session.commit()
    if request.method == 'POST':
        if 'ouvrir' in request.form:
            today = datetime.now()
            if not resa:
                # Si il n'y a pas de réservation
                flash('Pas de réservation', category='error')

            elif resa.id_velo != 0:
                # Si l'utilisateur a déjà un vélo
                flash('Vous avez déjà le vélo ' + str(resa.id_velo))

            elif resa.date_debut.day - today.day < 0 or \
                    resa.date_debut.hour - today.hour > 0 or \
                    today.day - resa.date_fin.day > 0:
                # Si l'utilisateur veut récupérer un vélo en dehors de sa réservation
                flash('Récupérez votre vélo pendant votre réservation', category='error')

            else:
                # Si tout est ok on regarde quels sont les vélos actuellement disponible
                for velo in bikes:
                    if not velo.estPris:
                        flash('Ouverture prenez le vélo ' + str(velo.id), category='success')
                        # On envoie à la boîte une requête UDP pour lui dire de s'ouvrir
                        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
                        sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
                        # On met à jour la base de données
                        resa.id_velo = velo.id
                        velo.estPris = True
                        histo = Historique(id_user=user.id, id_velo=velo.id, date_debut=resa.date_debut,
                                           date_fin=resa.date_fin)
                        db.session.add(histo)
                        db.session.commit()
                        return render_template("home.html", user=current_user, resa=resa)

                flash("Tout les vélos sont pris désolé", category="error")

        elif 'rendre' in request.form:
            velo = Velo.query.filter_by(id=resa.id_velo).first()
            resa.id_velo = 0
            velo.estPris = False
            db.session.commit()
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
            sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
            flash('Vélo rendu merci et à bientôt', category='success')

            return render_template("home.html", user=current_user, resa=resa)
        elif 'pb' in request.form:
            velo = Velo.query.filter_by(id=resa.id_velo).first()
            resa.id_velo = 0
            velo.estPris = False
            db.session.commit()
        elif 'problemSubmit' in request.form:
            problem = user.nom + " " + request.form.get('problem')
            CHANNEL_ID = open('./channel.txt',"r").readline()
            asyncio.run(runBot(problem, int(CHANNEL_ID)))
        else:
            begin_date = request.form.get('start')
            end_date = request.form.get('end')
            begin_hour = request.form.get('begin_hour')
            end_hour = request.form.get('end_hour')

            if begin_date is None or \
                    end_date is None or \
                    begin_hour is None or \
                    end_hour is None:
                flash('Les dates ne sont pas correctes', category='error')

            elif begin_date == "" or \
                    end_date == "" or \
                    begin_hour == "" or \
                    end_hour == "":
                flash('Les dates ne sont pas correctes', category='error')

            else:
                date1 = datetime.strptime(begin_date + " " + begin_hour, "%Y-%m-%d %H:%M")
                date2 = datetime.strptime(end_date + " " + end_hour, "%Y-%m-%d %H:%M")
                timedelta = date2 - date1

                if timedelta.days > 3:
                    flash('Vous ne pouvez pas réserver plus de 3 jours', category='error')
                elif timedelta.days < 0:
                    flash('La date de fin doit être après la date de début ...', category='error')
                else:
                    if resa:
                        if resa.id_velo != 0 :
                            flash("Finissez votre réservation en cours avant d'en refaire une", category="error")
                            return render_template("home.html", user=current_user, resa=resa)

                        else:
                            db.session.delete(resa)
                            db.session.commit()

                    new_resa = Reservation(date_debut=date1, date_fin=date2, id_user=user.id)
                    db.session.add(new_resa)
                    db.session.commit()

                    return render_template("home.html", user=current_user, resa=new_resa)

    return render_template("home.html", user=current_user, resa=resa)


@views.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    nom = current_user.nom
    user = User.query.filter_by(nom=nom).first()
    bikes = Velo.query.all()
    histo = Historique.query.all()
    users = User.query.all()
    print()
    if user.est_admin:
        # if request.method == 'POST':
        if 'admin' in request.form:
            user_to_admin = User.query.filter_by(id=request.form.get('admin')).first()
            user_to_admin.est_admin = True
            db.session.commit()

        elif 'retirer' in request.form:
            if(User.query.filter(User.est_admin==True).count() != 1):
                user_not_admin = User.query.filter_by(id=request.form.get('retirer')).first()
                user_not_admin.est_admin = False
                db.session.commit()
            else :
                flash("Il ne faut pas supprimer le dernier admin", category="error")

        elif 'retirerResa' in request.form:
            print("ici")
            resa_to_delete = Historique.query.filter_by(id=request.form.get('retirerResa')).first()
            db.session.delete(resa_to_delete)
            db.session.commit()
            histo = Historique.query.all()

        elif 'delete' in request.form:
            user_to_delete = User.query.filter_by(id=request.form.get('delete')).first()
            db.session.delete(user_to_delete)
            db.session.commit()
            users = User.query.all()

        elif 'ouverture' in request.form:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
            sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))

        elif 'rendreDispo' in request.form:
            velo=Velo.query.filter_by(id=request.form.get('rendreDispo')).first()
            velo.estPris=False
            db.session.commit()
            bikes=Velo.query.all()

        elif 'repare' in request.form:
            velo=Velo.query.filter_by(id=request.form.get('repare')).first()
            velo.estPris=True
            db.session.commit()
            bikes=Velo.query.all()

        return render_template("admin.html", user=current_user, bikes=bikes, histo=histo, users=users)
    else:
        return render_template("permission_denied.html", user=user, url=request.url)

@views.route('/ipupdate/<ip>')
def ipupdate(ip):
    UDP_IP=ip
    print("hey listen")
    print(UDP_IP)
    return render_template("ipupdate.html")


