from flask import *
from app import *
from app.mixin import *
from app.models import *
from flask_user import *
from flask_sqlalchemy import *
import time, datetime

#setup user manager
user_manager = UserManager(app, db, User)

# add admin for testing if not added yet
if not User.query.filter(User.username == "Admin").all():
    user = User(
        username = "Admin",
        password = user_manager.hash_password("Password1"),
        first_name = "Chaostheorie",
        last_name = "Admin",
        level = "admin",
        level_specific = "Staff of VKS",
        description = "The admin of the Project."
    )
    user.roles.append(Role(name="Admin"))
    db_session.add(user)
    db_session.commit()

if not User.query.filter(User.username == "guest").all():
    user = User(
        username = "guest",
        password = user_manager.hash_password("Passwort"),
        first_name = "Gast",
        last_name = "Coder Dojo",
        level = "pupil",
        shool_class = "10B",
        description = "Anonymous guest user"
    )
    db_session.add(user)
    db_session.commit()


# this function is for form Processing
def make_dict(request):
    values = list(request.form.values())
    keys = list(request.form.keys())
    input = {}
    for i in range(len(keys)):
        value = values[i]
        key = keys[i]
        input.update({key:value})
    return input

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        try:
            text = "Welcome " + current_user.username + " to the webpage"
            return render_template("index.html", text=text)
        except:
            return render_template("index.html")

    if request.method == "POST":
        type = "specific"
        spdict = ""
        return_url = request.referrer or "/"
        return search_results(request, type, spdict, return_url)

@app.route("/admin/<method>/<username>", methods=["GET", "POST"])
@roles_required("Admin")
def admin(method, username):
    if request.method == "GET":
        return render_template("admin.html", method=method, username=username, \
        type="action")

@app.route("/admin")
@roles_required("Admin")
def admin_dashboard():
    login = logins.query.order_by("time_pr desc").limit(5).all()
    return render_template("admin.html", logins=login, type="view")

@app.route("/add-user", methods=["POST", "GET"])
@roles_required("Admin")
def add_user():
    if request.method == "GET":
        roles_all = Role.query.order_by(Role.name).all()
        return render_template("add_user.html", roles=roles_all)

    if request.method == "POST":
        multiselect = request.form.getlist("roles")
        user = User(
        username = request.form["username"],
        password = user_manager.hash_password(request.form["password"]),
        first_name = request.form["first_name"],
        last_name = request.form["last_name"],
        )
        user.roles = []
        for i in range(len(multiselect)):
            user.roles.append(Role(name=multiselect[i]))
            print(str(i) + ": " + multiselect[i])
        db.session.add(user)
        db.session.commit()
        flash("Add username: " + request.form["username"] + " sucessfully")
        return redirect("/add-user")

@app.route("/add-term", methods=["POST", "GET"])
@roles_required("Admin")
def add_term():
    if request.method == "GET":
        return render_template("add_term.html")

    if request.method == "POST":
        new_term = make_dict(request)
        return redirect("/add-term")

@app.route("/logins", methods=["GET", "POST"])
@roles_required("Admin")
def logins_view():
    if request.method == "GET":
        login = logins.query.order_by("time_pr desc").limit(100).all()
        return render_template("logins_overview.html", logins=login,
        current_page=1)

    if request.method == "POST":
        input = make_dict(request)
        login = logins.query.order_by("time_pr desc").limit(100).all()
        print(input)
        return logins_view_specific(input["page"])

@app.route("/logins/<page>")
@roles_required("Admin")
def logins_view_specific(page):
    number = int(page) * 100 + 100
    login = logins.query.order_by("time_pr desc").limit(number).all()
    login_list = login[:number]
    return render_template("logins_overview.html", logins=login_list,
    current_page=int(page))

@app.route("/results")
@login_required
def search_results(request, type, spdict, return_url):
    if type == "specific":
        input = make_dict(request)

    elif type == "nonspecific":
        input = spdict

    else:
        flash("Error 02: Bad request")
        return redirect(return_url)
    len_s = ""

    if input["type"]=="broadcast":
        result_type = input["type"] or ""
        entrys.reindex()
        results = query, total = entrys.search(input["search"], 1, 100)
        if input["search"] == "":
                qry = db.session.query(entrys)
                results = qry.all()
                if len(entrys.query.all()) > 1:
                    text = " Es wurden " + str(len(entrys.query.all())) + \
                     " Ergebnisse gefunden:"
                else:
                    text = "Es wurde " + str(len(entrys.query.all())) + \
                     " Ergebniss gefunden: "
                if total == 0:
                    flash("Für diesen Suchbegriff wurde kein Ergebniss \
                     gefunden")
                    return redirect("/")
                return render_template("results.html", results=results,
                text=text, result_type=result_type)

    if input["type"]=="profile":
        User.reindex()
        result_type = input["type"]
        results = query, total = User.search(input["search"], 1 , 100)
        profile_results = []
        len_s = len(profile_results)
        for result in query:
            digest = hashlib.sha1(result.username.encode("utf-8")).hexdigest()
            avatar = "https://www.gravatar.com/avatar/{}?d=identicon&s=36".\
            format(digest)
            profile = {
            "username":result.username,
            "last_name":result.last_name,
            "first_name":result.first_name,
            "avatar_url":avatar
            }
            profile_results.append(profile)

        if input["search"] == "":
            results = db.session.query(User).order_by(User.username).all()
            len_s = len(results)
            profile_results = []
            if len(User.query.all()) > 1:
                    text = " Es wurden " + str(len(User.query.all())) + \
                     " Ergebnisse gefunden:"
            else:
                text = "Es wurde " + str(len(User.query.all())) + \
                 " Ergebniss gefunden: "
            for result in results:
                digest = hashlib.sha1(result.username.encode("utf-8")). \
                hexdigest()
                avatar = "https://www.gravatar.com/avatar/{}?d=identicon&s=36".\
                format(digest)
                profile = {
                "username":result.username,
                "last_name":result.last_name,
                "first_name":result.first_name,
                "avatar_url":avatar
                }
                profile_results.append(profile)
            #if total == 0:
            #    flash("Für diesen Suchbegriff wurde kein Ergebniss gefunden")
            #    return redirect("/")

            return render_template("results.html", results=profile_results,
             text=text, result_type=result_type, len=len_s)


    if input["type"]=="term":
        terms.reindex()
        results = query, total = terms.search(input["search"], 1, 100)
        result_type = input["type"]
        if input["search"] == "":
                results = db.session.query(terms).all()
                if len(terms.query.all()) > 1:
                    text = " Es wurden " + str(len(terms.query.all())) + \
                     " Ergebnisse gefunden:"
                else:
                    text = "Es wurde " + str(len(terms.query.all())) + \
                     " Ergebniss gefunden: "
                if total == 0:
                    flash("Für diesen Suchbegriff wurde kein Ergebniss \
                     gefunden")
                    return redirect("/")
                return render_template("results.html", results=results,
                text=text, result_type=result_type)
        if total == 0:
            flash("Für diesen Suchbegriff wurde kein Ergebniss gefunden")
            return redirect("/")

    if results[1] > 1:
        text = "Es wurden " + str(total) + " Ergebnisse für den Suchbegriff " +\
         input["search"] + " gefunden:"

    elif results[1] == 1:
        text = "Es wurde 1 Ergebniss für den Suchbegriff " + input["search"] + \
         " gefunden:"

    elif not results:
        flash("Database Failure 01 - no FTS index or search data")
        return redirect(return_url)

    if result_type == "profile":
        length = len(profile_results)
        text = "Es wurde " + str(length) + " Ergebniss gefunden."
        if length > 1:
            text = "Es wurde " + str(length) + " Ergebnisse gefunden."
        return render_template("results.html", text=text, results = \
        profile_results, result_type=result_type, len=length)
    if total == 0:
        flash("Für diesen Suchbegriff wurde kein Ergebniss gefunden")
        return redirect("/")
    return render_template("results.html", results=results, text=text, \
    result_type=result_type, len=len_s)

# for later implementation and allowing url_for(*) to work
@app.route("/about-us")
def about_us():
    flash("Noch nicht erstellt")
    return_url = request.referrer or "/"
    return redirect(return_url)

@app.route("/profile/<username>")
@login_required
def profile_specific(username):
    user_searched = User.query.filter_by(username=username).first_or_404()
    current_user_level = current_user.level
    print(current_user_level)
    return render_template("profile_specific.html", user=user_searched, \
    logged_level=current_user_level )

@app.route("/profile/")
def profile_redirect():
    return profile_main()

@app.route("/profile/<username>/popup")
@login_required
def user_popup(username):
    user_searched = User.query.filter_by(username=username).first_or_404()
    return render_template("user_popup.html", user=user_searched)

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile_main():
    if request.method == "GET":
        return render_template("profile_main.html")

    elif request.method == "POST":
        type = "specific"
        spdict = ""
        return_url = request.referrer or "/"
        return search_results(request, type, spdict, return_url)

@app.route("/all_terms")
@login_required
def all_terms():
    return_url = "/"
    spdict = {'search': '', 'type': 'term'}
    type = "nonspecific"
    return search_results("", type, spdict, return_url)

@app.route("/all_entrys")
@login_required
def all_entrys():
    return_url = "/"
    spdict = {'search': '', 'type': 'broadcast'}
    type = "nonspecific"
    return_url = request.referrer
    return search_results("", type, spdict, return_url)

@app.route("/report", methods=["GET", "POST"])
@login_required
def report():
    if request.method == "GET":
        return render_template("report.html")

    if request.method == "POST":
        make_dict(request)
        return ""

# Signals form flask user
@user_logged_in.connect_via(app)
def _after_login_hook(sender, user, **extra):
    flash(user.username + " logged in")
    return ""

# For recording of user logins
@user_logged_in.connect_via(app)
def _track_logins(sender, user, **extra):
    user.last_login_ip = request.remote_addr
    login = logins(
    ip = user.last_login_ip,
    name = user.username,
    time = time.asctime(),
    time_pr = datetime.datetime.now()
    )
    db.session.add(login)
    db.session.commit()
    return ""

# Errorhandler pages
# Use 500 errorhandler for security
@app.errorhandler(500)
def internal_server_error(e):
    er = "Serverfehler"
    return_url = request.referrer or "/"
    return render_template("error.html", return_url=return_url, error=er)

@app.errorhandler(404)
def page_not_found(e):
    return_url = request.referrer or "/"
    er = "404"
    return render_template("error.html", return_url=return_url, error=er), 404

@app.errorhandler(403)
def forbidden(e):
    return_url = request.referrer or "/"
    er = "403"
    return render_template("error.html", return_url=return_url, error=er), 403
