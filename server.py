import os
from flask import Flask, render_template, redirect, request
from data import db_session
from forms.user import RegisterForm, LoginForm
from forms.review import FeedbackForm
from data.users import User
from data.objects import Object
from data.reviews import Review
from data.events import Event
from data.disposal import Disposal
from data.categories import Category
from flask_login import LoginManager, login_user, login_required, logout_user, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route("/")
def index():
    db_sess = db_session.create_session()
    objects = db_sess.query(Object).all()
    images = [object.images.split(',')[0] for object in objects]
    print(images)
    obj_img = zip(objects, images)
    if current_user.is_authenticated:
        return render_template("index.html", name=current_user.name, obj_img=obj_img)
    else:
        return render_template("index.html", objects=objects, obj_img=obj_img)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.name == form.name.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            
        )
        user.set_password(form.hashed_password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == form.name.data).first()
        if user and user.check_password(form.hashed_password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/object/<int:id>', methods=['GET', 'POST'])
def object(id):
    db_sess = db_session.create_session()
    object = db_sess.query(Object).filter(Object.id == id).first()
    images = object.images.split(', ')
    feedbacks = db_sess.query(Review).filter(Review.object_id == id).all()
    if current_user.is_authenticated:     
        return render_template('object.html', object=object, images=images, name=current_user.name, reviews=feedbacks)
    else:
        return render_template('object.html', object=object, images=images, reviews=feedbacks)
    

@app.route('/feedback/<int:id>', methods=['GET', 'POST'])
def feedback(id):
    if request.method == 'POST':
        db_sess = db_session.create_session()
     
        rating = request.form['rating']
        comment = request.form['comment']
        photos = request.files.getlist('photos')

        photo_filenames = []
        for photo in photos:
            if photo.filename != '':
                filename = photo.filename
                photo.save(os.path.join('static/images/', filename))
                photo_filenames.append(filename)
        print(photo_filenames)
        feedback = Review(
            rating=rating,
            text=comment,
            object_id=id,
            user_id=current_user.id,
            images=', '.join(photo_filenames)
        )
        
        db_sess.add(feedback)
        object = db_sess.query(Object).filter(Object.id == id).first()
        ratings = [int(rew.rating) for rew in db_sess.query(Review).filter(Review.object_id == id).all()]
        rating = sum(ratings) / len(ratings)
        object.rating = rating
        db_sess.commit()
        return redirect('/')

    return render_template('feedback.html', id=id)


@app.route('/disposal')
def disposal():
    db_sess = db_session.create_session()
    disposals = db_sess.query(Disposal).all()
    images = [disposal.images.split(',')[0] for disposal in disposals]
    print(images)
    dis_img = zip(disposals, images)
    if current_user.is_authenticated:
        return render_template('disposal.html', dis_img=dis_img, name=current_user.name)
    else:
        return render_template('disposal.html', dis_img=dis_img)

@app.route('/dis/<int:id>', methods=['GET', 'POST'])
def dis(id):
    db_sess = db_session.create_session()
    disposal = db_sess.query(Disposal).filter(Disposal.id == id).first()
    images = disposal.images.split(', ')
    if current_user.is_authenticated:
        return render_template('dis.html', disposal=disposal, images=images, name=current_user.name)
    else:
        return render_template('dis.html', disposal=disposal, images=images)


@app.route('/events')
def events():
    db_sess = db_session.create_session()
    events = db_sess.query(Event).all()
    images = [event.images.split(',')[0] for event in events]
    evn_img = zip(events, images)
    if current_user.is_authenticated:
        return render_template('events.html', evn_img=evn_img, name=current_user.name)
    else:
        return render_template('events.html', evn_img=evn_img)


@app.route('/event/<int:id>', methods=['GET', 'POST'])
def event(id):
    db_sess = db_session.create_session()
    event = db_sess.query(Event).filter(Event.id == id).first()
    images = event.images.split(', ')
    if current_user.is_authenticated:
        return render_template('event.html', event=event, images=images, name=current_user.name)
    else:
        return render_template('event.html', event=event, images=images)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        db_sess = db_session.create_session()

        val = request.form.get('val')
        print(val)
        if int(val) == 1:
            return redirect('/add_object')        
        if int(val) == 2:
            return redirect('/add_event')
        if int(val) == 3:
            return redirect('/add_disposal')
        return redirect('/')

    return render_template('add.html', name=current_user.name)


@app.route('/add_object', methods=['GET', 'POST'])
def add_object():
    db_sess = db_session.create_session()
    categories = db_sess.query(Category).all()
    if request.method == 'POST':
        

        title = request.form['title']
        address = request.form['address']
        phone = request.form['phone']
        category_id = request.form.get('val')
        website = request.form['website']
        description = request.form['descpription']
        maps_url = request.form['maps-url']

        photos = request.files.getlist('photos')

        photo_filenames = []
        for photo in photos:
            if photo.filename != '':
                filename = photo.filename
                photo.save(os.path.join('static/images/', filename))
                photo_filenames.append(filename)

        print(photo_filenames)

        object = Object(
            title=title,
            address=address,
            phone=phone,
            category_id=category_id,
            website=website,
            description=description,
            maps_url=maps_url,
            images=', '.join(photo_filenames)
        )


        db_sess.add(object)
        db_sess.commit()
        return redirect('/')


    return render_template('add_object.html', categories=categories)


@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    db_sess = db_session.create_session()
    categories = db_sess.query(Category).all()
    if request.method == 'POST':
        

        title = request.form['title']
        address = request.form['address']
        phone = request.form['phone']
        website = request.form['website']
        description = request.form['descpription']
        maps_url = request.form['maps-url']

        photos = request.files.getlist('photos')

        photo_filenames = []
        for photo in photos:
            if photo.filename != '':
                filename = photo.filename
                photo.save(os.path.join('static/images/', filename))
                photo_filenames.append(filename)

        print(photo_filenames)

        event = Event(
            title=title,
            address=address,
            phone=phone,
            website=website,
            description=description,
            maps_url=maps_url,
            images=', '.join(photo_filenames)
        )


        db_sess.add(event)
        db_sess.commit()
        return redirect('/events')


    return render_template('add_event.html')

@app.route('/add_disposal', methods=['GET', 'POST'])
def add_disposal():
    db_sess = db_session.create_session()
    categories = db_sess.query(Category).all()
    if request.method == 'POST':


        title = request.form['title']
        address = request.form['address']
        phone = request.form['phone']
        website = request.form['website']
        description = request.form['descpription']
        maps_url = request.form['maps-url']

        photos = request.files.getlist('photos')

        photo_filenames = []
        for photo in photos:
            if photo.filename != '':
                filename = photo.filename
                photo.save(os.path.join('static/images/', filename))
                photo_filenames.append(filename)

        print(photo_filenames)

        disposal = Disposal(
            title=title,
            address=address,
            phone=phone,
            website=website,
            description=description,
            maps_url=maps_url,
            images=', '.join(photo_filenames)
        )


        db_sess.add(disposal)
        db_sess.commit()
        return redirect('/disposal')


    return render_template('add_disposal.html')



def main():
    db_session.global_init("db/database.db")
    app.run(port=8080, host="127.0.0.1", debug=True)

if __name__ == '__main__':
    main()