import uuid

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
        mobile_data.append(current_user.id)
        unique_code = uuid.uuid4().hex
        session["mobile"] = mobile
        flash(_("Mobile number updated successfully"))

    return redirect(url_for("main.profile"))

