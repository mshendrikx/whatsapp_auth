import random

from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_babel import gettext as _
from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    jsonify,
    session,
)

from models import User

from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route("/profile", methods=["POST"])
@login_required
def profile_post():

    password = request.form.get("password")
    repass = request.form.get("repass")
    name = request.form.get("name")
    email = request.form.get("email")
    mobile = request.form.get("mobile")
    language = request.form.get("lang_selection")
    theme = request.form.get("theme_selection")

    if password != repass:
        flash(_("Password do not match"))
        flash("alert-danger")
        return redirect(url_for("main.profile"))

    if "@" not in email:
        flash(_("Enter valid E-mail"))
        flash("alert-danger")
        return redirect(url_for("main.profile"))

    if password != "":
        current_user.password = generate_password_hash(password, method="pbkdf2:sha256")

    if name != "":
        current_user.name = name

    current_user.email = email
    current_user.mobile = mobile
    current_user.language = language
    current_user.theme = theme

    db.session.add(current_user)
    db.session.commit()
    
    mobile_data = []
    if mobile != current_user.mobile:
        mobile_data.append(mobile)
        mobile_data.append(str(random.randint(100000, 999999)))
        return render_template("mobilechange.html", mobile_data=mobile_data)

    return redirect(url_for("main.profile"))

@main.route('/mobilechange', methods=["POST"])
@login_required
def mobilechange_post():
    
    mobile = request.form.get("mobile")
    code = request.form.get("code")
    verify = request.form.get("verify")
    
    if code == verify:
        current_user.mobile = mobile
        db.session.add(current_user)
        db.session.commit()
        flash(_("Mobile number updated successfully"))
        flash("alert-success")
        return redirect(url_for("main.profile"))
    else:
        mobile_data = [mobile, code]
        flash(_("Verification code does not match"))
        flash("alert-danger")
        return render_template("mobilechange.html", mobile_data=mobile_data)

    
    return render_template('profile.html', name=current_user.name)
