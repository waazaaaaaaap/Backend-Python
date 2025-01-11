from ext import app, db, login_manager
from flask_login import login_user, logout_user, login_required, current_user
from flask import render_template, redirect, flash, request
from forms import RegisterForm, ServiceForm, LoginForm, UserEdit, PostForm, CourseForm, SoftwareForm
from models import Service, User, Course, Post, Like, Software
from functools import wraps
from os import path


@app.route("/404")
def notfoundpage():
    return render_template("404.html")

@app.errorhandler(404)
def page_not_found(e):
    return redirect("/404")


@app.route("/")
def home():
    services = Service.query.all() 
    courses = Course.query.all()
    softwares = Software.query.all()
    
    return render_template("index.html", services=services, courses=courses, softwares=softwares)





############ USER MANAGEMENT ############

@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    warning = None
    if form.validate_on_submit():
         
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            warning = "Username already exists. Please choose a different one."
            return render_template("register.html", form=form, warning=warning)
        
        new_user = User(username=form.username.data, email=form.email.data, name=form.name.data, surname=form.surname.data, password=form.password.data)  
        new_user.save()
        
        if form.password.data != form.repeat_password.data:
            warning = "Passwords do not match. Please try again."
            return render_template("register.html", form=form, warning=warning)
        
        return redirect("/")
    return render_template("register.html", form=form)





@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")
        else:
            flash("Invalid username or password", "danger")
    
    return render_template("login.html", form=form)





@app.route("/dashboard", methods=["POST", "GET"])
@login_required
def dashboard():
    form = PostForm()
    if form.validate_on_submit(): 
        new_post = Post(title=form.title.data, subtitle=form.subtitle.data, description=form.description.data, author=current_user.username, imgurl=form.imgurl.data)  
        new_post.save()
        
        return redirect("/dashboard")
    
    user_posts = Post.query.filter_by(author=current_user.username).all()
    post_count = len(user_posts)

    return render_template("dashboard.html", form=form, posts=user_posts, post_count=post_count) 


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

############ USER MANAGEMENT END ############








############ POSTS AND WRITEUPS #########

@app.route("/writeups")
def writeups():
    posts = Post.query.all()
    return render_template("writeups.html", posts=posts)



@app.route("/vulnerability-writeup/<int:post_id>")
def post(post_id):
    posts = Post.query.get(post_id)
    if not posts:
        return redirect("/404")
    return render_template("vulnerability_writeup.html", posts=posts, likes=posts.likes)



@app.route("/like_post/<int:post_id>", methods=["POST", "GET"])
@login_required
def like_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return redirect("/404")

    existing_like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if existing_like:
        return "You have already liked this post.", 400

    # Ensure post_id is passed correctly
    new_like = Like(user_id=current_user.id, post_id=post_id)
    post.likes += 1
    db.session.add(new_like)
    db.session.commit()
    
    return "Post liked successfully.", 200




@app.route("/delete_post/<int:post_id>", methods=["POST", "GET"])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return redirect("/404")

    if current_user.role == "Admin" or post.author == current_user.username:
        print(f"Deleting post: {post_id}")
        print(f"Likes associated with this post: {Like.query.filter_by(post_id=post_id).all()}")  # Debug info
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully.", "success")
        return redirect("/dashboard")
    
    return "Unauthorized: You cannot delete this post.", 401



@app.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = Post.query.get(post_id)
    form = PostForm(title=post.title, subtitle=post.subtitle, description=post.description, imgurl=post.imgurl)
    if form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.description = form.description.data
        post.imgurl = form.imgurl.data
        db.session.commit()
        return redirect("/dashboard")
    return render_template("editpost.html", form=form)






########## ADMIN DEFINE #########
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return render_template("401.html"), 401
        if getattr(current_user, "role", None) != "Admin":
            return render_template("403.html"), 403
        return f(*args, **kwargs)
    return decorated_function



############ ADMIN DASHBOARD ############

@app.route("/admin", methods=["GET", "POST"])
@admin_required
def admin():
    service_form = ServiceForm()
    software_form= SoftwareForm()
    course_form = CourseForm()
    
    
    if service_form.validate_on_submit() and request.form.get("form_name") == "service_form":
        new_service = Service(title = service_form.title.data, description = service_form.description.data, details = service_form.details.data, price = service_form.price.data, imgurl = service_form.imgurl.data)  
        new_service.save()
        
        return redirect("/admin")
    
    if software_form.validate_on_submit() and request.form.get("form_name") == "software_form":
        new_software = Software(title = software_form.title.data, description = software_form.description.data, details = software_form.details.data, price = software_form.price.data, imgurl = software_form.imgurl.data)  
        new_software.save()
        
        return redirect("/admin")
    
    if course_form.validate_on_submit() and request.form.get("form_name") == "course_form":
        new_course = Course(title = course_form.title.data, description = course_form.description.data, details = course_form.details.data, price = course_form.price.data, imgurl = course_form.imgurl.data)  
        new_course.save()
        
        return redirect("/admin")
    
    services = Service.query.all()
    courses = Course.query.all()
    softwares = Software.query.all() 
    users = User.query.all()
    posts = Post.query.all()
    
    return render_template("admindashboard.html", services=services, courses=courses, softwares=softwares, users=users, posts=posts, service_form=service_form, course_form=course_form, software_form=software_form)







############ USER ADMINISTRATION ############
@app.route("/delete_user/<int:user_id>")
@admin_required  
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash("User deleted successfully.", "success")
    else:
        flash("User not found.", "danger")
    return redirect("/admin") 


@app.route("/edit_user/<int:user_id>", methods=["GET", "POST"])
@admin_required  
def edit_user(user_id):
    user = User.query.get(user_id)
    form = UserEdit(username=user.username, email=user.email, name=user.name, surname=user.surname)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.name = form.name.data
        user.surname = form.surname.data
        db.session.commit()
        return redirect("/admin")
    return render_template("edituser.html", form=form)







############ SERVICE ADMINISTRATION ############

@app.route("/edit_service/<int:service_id>", methods=["GET", "POST"])
@admin_required
def edit_service(service_id):
    service = Service.query.get(service_id)
    service_form = ServiceForm(
        title=service.title,
        description=service.description,
        details=service.details,
        price=service.price,
        imgurl=service.imgurl
    )

    if service_form.validate_on_submit():
        service.title = service_form.title.data
        service.description = service_form.description.data
        service.details = service_form.details.data
        service.price = service_form.price.data
        service.imgurl = service_form.imgurl.data  

        db.session.commit()
        flash("service updated successfully.", "success")
        return redirect("/admin")
    
    return render_template("edit_service.html", service_form=service_form)


@app.route("/delete_service/<int:service_id>")
@admin_required  
def delete_service(service_id):
    service = Service.query.get(service_id)
    
    service.delete()
    return redirect("/admin")


############ SERVICE MANAGEMENT END ############



@app.route("/service/<int:service_id>")
def service(service_id):
    service = Service.query.get(service_id)
    if not service:
        return redirect("/404")
    return render_template("service.html", service=service)

@app.route("/course/<int:course_id>")
def course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return redirect("/404")
    return render_template("course.html", course=course)

@app.route("/software/<int:software_id>")
def software(software_id):
    software = Software.query.get(software_id)
    if not software:
        return redirect("/404")
    return render_template("software.html", software=software)



############ SOFTWARE MANAGEMENT ############


@app.route("/edit_software/<int:software_id>", methods=["GET", "POST"])
@admin_required
def edit_software(software_id):
    software = Software.query.get(software_id)
    software_form = SoftwareForm(
        title=software.title,
        description=software.description,
        details=software.details,
        price=software.price,
        imgurl=software.imgurl
    )

    if software_form.validate_on_submit():
        software.title = software_form.title.data
        software.description = software_form.description.data
        software.details = software_form.details.data
        software.price = software_form.price.data
        software.imgurl = software_form.imgurl.data  

        db.session.commit()
        flash("software updated successfully.", "success")
        return redirect("/admin")
    
    return render_template("edit_software.html", software_form=software_form)


@app.route("/delete_software/<int:software_id>")
@admin_required
def delete_software(software_id):
    software = Software.query.get(software_id)
    if software:
        db.session.delete(software)
        db.session.commit()
    return redirect("/admin")

############ SOFTWARE MANAGEMENT END ############


############ COURSE MANAGEMENT ############

@app.route("/delete_course/<int:course_id>")
@admin_required
def delete_course(course_id):
    course = Course.query.get(course_id)
    if course:
        db.session.delete(course)
        db.session.commit()
    return redirect("/admin")

@app.route("/edit_course/<int:course_id>", methods=["GET", "POST"])
@admin_required
def edit_course(course_id):
    course = Course.query.get(course_id)
    course_form = CourseForm(
        title=course.title,
        description=course.description,
        details=course.details,
        price=course.price,
        imgurl=course.imgurl
    )

    if course_form.validate_on_submit():
        course.title = course_form.title.data
        course.description = course_form.description.data
        course.details = course_form.details.data
        course.price = course_form.price.data
        course.imgurl = course_form.imgurl.data  

        db.session.commit()
        flash("Course updated successfully.", "success")
        return redirect("/admin")
    
    return render_template("edit_course.html", course_form=course_form)


@app.route("/about")
def about():
    return render_template("about.html")