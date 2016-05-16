"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

from app import app, db, mail
from flask import Flask, Response, render_template, request, redirect, url_for, flash, jsonify, session, abort, g
from flask.ext.login import  LoginManager, login_user , logout_user , current_user , login_required
from flask.ext.sqlalchemy import SQLAlchemy
from flask_mail import Message
from app.models import User_info, Wishes
from datetime import *
from .forms import RegistrationForm, SigninForm, WishForm, ShareForm
import json
from werkzeug.utils import secure_filename
from sqlalchemy.sql.expression import func
import os
import time
from bs4 import BeautifulSoup
import urlparse
import requests
import urllib2


###
# Routing for your application.
###

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'

@login_manager.user_loader
def load_user(id):
    return User_info.query.get(int(id))

@app.route('/')
def home():
    """Render website's home page."""
    if g.user.is_authenticated:
      return redirect(url_for('profile', id=str(g.user.id)))
    return render_template('home.html')

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


def timeinfo():
    return datetime.now()
    
@app.route('/api/user/register', methods=['POST', 'GET'])
def register():
  """Render the register page"""
  form = RegistrationForm()
    
  if form.validate_on_submit():
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    password = request.form['password']
    age = int(request.form['age'])
    sex = request.form['sex']
    photo = request.files['image']
    imagename = fname + '_' + secure_filename(photo.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], imagename)
    photo.save(file_path)
    newUser = User_info(fname, lname, imagename, email, password, age, sex, timeinfo())
    db.session.add(newUser)
    db.session.commit()
    flash('You have successfully registered. Login below.')
    return redirect(url_for('signin'))
  if g.user.is_authenticated and g.user.email != "admin@wishlist.com":
    flash ("Cannot access registration page while logged in. Admin Only. You can log out and create a new account!")
    return redirect(url_for('profile', id=str(g.user.id)))
  return render_template('form.html', form=form)
  
  
  
@app.route('/api/user/login', methods=['GET', 'POST'])
def signin():
  form = SigninForm()
  if g.user.is_authenticated:
    flash ("You're already logged in!")
    return redirect(url_for('profile', id=str(g.user.id)))
   
  if request.method == 'POST':
    if form.validate() == False:
      msg = "Invalid Login!"
      return render_template('signin.html', form=form, messages=msg)
    else:
      email = form.email.data.lower()
      user = User_info.query.filter_by(email=email).first()
      if user is None and form.validate() == False:
        return redirect(url_for('signin'))
      login_user(user)
      return redirect(request.args.get('next') or url_for('profile', id=str(g.user.id)))
                 
  elif request.method == 'GET':
    return render_template('signin.html', form=form)
    
    
@app.route('/signout')
def signout():
    logout_user()
    return redirect(url_for('home')) 
  
  
@app.route('/profiles/', methods=["GET"])
@login_required
def profiles():
  users = db.session.query(User_info).all()
  if g.user.email == "admin@wishlist.com":
    return render_template('profiles.html', users=users)
  return redirect(url_for('profile', id=str(g.user.id)))
    

@app.route('/api/user/<id>/wishlist', methods=['POST', 'GET'])
def profile(id):
  usr = User_info.query.filter_by(id=id).first()
  if usr:
    if request.method == "GET":
      wishes = Wishes.query.filter_by(user=usr.email).order_by(Wishes.rating.desc()).all()
      form = WishForm()
      share = ShareForm()
      error = "User has no wishes"
      image = url_for('static', filename='img/'+usr.image)
      user = {'id':str(id), 'image':image, 'age':usr.age, 'fname':usr.fname, 'lname':usr.lname, 'email':usr.email, 'sex':usr.sex}
      if g.user.is_authenticated:
        if wishes:
          return render_template('user.html', user=user, wishes=wishes, datestr=date_to_str(g.user.datejoined), form=form, share=share)
        return render_template('user.html', user=user, datestr=date_to_str(g.user.datejoined), form=form, error=error)
      if wishes:
        return render_template('viewwishlist.html', wishes=wishes, user=user)
      return render_template('viewwishlist.html', user=user, error=error)
    bought = request.form['bought']
    title = request.form['title']
    desc = request.form['description']
    thumb = request.form['thumb']
    url = request.form['url']
    rating = request.form['priority']
    category = request.form["category"]
    user = usr.email
    if thumb is not None:
      wish = Wishes(title,desc,thumb,user,url,rating,bought,category)
      db.session.add(wish)
      db.session.commit()
      flash("your wish was successfully added!")
      return redirect(url_for('profile', id=str(g.user.id)))
  return render_template('404.html')
  
  
@app.route('/api/thumbnail/process', methods=['POST'])
@login_required
def addWish():
  form = WishForm()
  image = url_for('static', filename='img/'+g.user.image)
  user = {'id':g.user.id, 'image':image, 'age':g.user.age, 'fname':g.user.fname, 'lname':g.user.lname, 'email':g.user.email, 'sex':g.user.sex}
  if form.validate_on_submit():
    url = request.form['url']
    wishes = Wishes.query.filter_by(user=g.user.email).all()
    for wish in wishes:
      if url in wish.url:
        flash ('This item already exists in your wishlist.')
        return redirect(url_for('profile', id=str(g.user.id)))
    images = []
    if "dell.com" not in url:
      hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
      req = urllib2.Request(url, headers=hdr)
      page = urllib2.build_opener(urllib2.HTTPCookieProcessor).open(req).read()
    else:
      page = page = urllib2.build_opener(urllib2.HTTPCookieProcessor).open(url).read()
    soup = BeautifulSoup(page)
    title = (soup.find('meta', property='og:title') or 
                    soup.find('meta', attrs={'name': 'title'}))
    if title and title['content']:
      content = title['content']
    else:
      content = "Really want this"
      
    desc = (soup.find('meta', property='og:description') or 
                    soup.find('meta', attrs={'name': 'description'}))
    if desc and desc['content']:
      description = desc['content']
    else:
      description = "I want this item"
      
    og_image = (soup.find('meta', property='og:image') or 
                        soup.find('meta', attrs={'name': 'og:image'}))
    if og_image and og_image['content']:
      images.append(og_image['content'])

    for img in soup.findAll("img", src=True):
      if "sprite" not in img["src"] and "data:image" not in img["src"] and ".gif" not in img["src"]:
        images.append(img['src'])

    thumbnail_spec = soup.find('link', rel='image_src')
    if thumbnail_spec and thumbnail_spec['href']:
      images.append(thumbnail_spec['href'])
      
    if len(images) >= 1:
      return render_template('process.html', user=user, description=description, title=content, images=images, url=url)
    else:
      desc="Unable to scrape any images from given url"
      title="Error"
      return render_template('process.html', user=user, description=desc, title=title, images=images)
  return render_template('user.html', user=user, datestr=date_to_str(g.user.datejoined), form=form)
  
@app.route('/api/user/<id>/wishlist/share', methods=['POST'])
@login_required
def share(id):
  who = request.form['name']
  where = request.form['email']
  addresses = where.replace(" ","").split(",")
  user_name = g.user.fname
  user_email = g.user.email
  subject = g.user.fname + "'s Wishlist"
  msg = request.url
  url = msg.split("/share")[0]
  # message = """From: {} <{}>
  # To: {} <{}>
  # Subject: {}
  # {}
  # """
  
  msg = Message(subject,
                  sender=user_email,
                  recipients=addresses,
                  html="<h2>Hi "+who+":</h1> <p>This is "+user_name+". Please view my wishlistlist at the address below</p><br><a href="+url+" target=\"_blank\">Click on this link</a><br><p>If you can't see the link or if the link is disabled, copy and paste from below<br>"+url+"<br><br></p><br><p>I really hope you can purchase an item for me</p>")
  mail.send(msg)
  flash("Email sent!")
  return redirect(url_for('profile', id=id))
      
  
@app.route('/api/wish/<id>/delete', methods=['GET'])
@login_required
def delete(id):
  wish = Wishes.query.filter_by(id=id).first()
  if wish and wish.user == g.user.email:
    db.session.delete(wish)
    db.session.commit()
    flash ("Wish deleted!")
    return redirect(url_for('profile', id=str(g.user.id)))
  flash("unfortunately you are not authorized to delete this wish!!! Please do not use this website maliciously!!!")
  return redirect(url_for('profile', id=str(g.user.id)))
  
@app.route('/api/wish/<id>/priority', methods=['GET','POST'])
@login_required
def priority(id):
  if request.method == "POST":
    value = request.form['priority']
    wish = Wishes.query.get(id)
    wish.rating = value
    db.session.commit()
    flash("Wish rating/priority updated!")
    return redirect(url_for('home'))
  return render_template('update-priority.html', id=id)
  
@app.route('/api/wish/<id>/bought', methods=['GET'])
@login_required
def bought(id):
  wish = Wishes.query.get(id)
  if wish and wish.user == g.user.email:
    wish.bought = "1"
    db.session.commit()
    flash("Wish successfully marked as bought. Click 'View bought items' to view wishes already purchased.")
    return redirect(url_for('profile', id=str(g.user.id)))
  flash("unfortunately you are not authorized to update this wish!!! Please do not use this website maliciously!!!")
  return redirect(url_for('profile', id=str(g.user.id)))
  
@app.route('/api/user/update-view', methods=['POST'])
@login_required
def updateView():
  cat = request.form['category']
  data = ""
  if cat == "All":
    wishes = Wishes.query.filter_by(user=g.user.email).order_by(Wishes.rating.desc()).all()
  else:
    wishes = Wishes.query.filter_by(category=cat).order_by(Wishes.rating.desc()).all()
  if wishes:
    for wish in wishes:
      if wish.bought == "0" or wish.bought is None:
        data += """<div class="needed">
          <div id=\""""
        data += str(wish.id)+"""\" class="ih-item square colored effect9 right_to_left"><a href=\""""
        data += wish.url+"""\" target="_blank">
          <div class="img"><img src=\""""
        data+= wish.thumbnail+"""\" alt="img" height="235" width="316"></div>
          <div class="info">
          <div class="info-back">
            <h3>"""
        data += wish.title+"""</h3>
            <p>"""
        data += wish.description+"""</p></a>
            <p class="raise">Mark item as bought: <input class="entry2" type="checkbox" name="wish" value=\""""
        data += str(wish.id)+"""\" onclick="javascript:bought(event)"></p>
            <table class="raise" style="margin:auto;color:white;margin-bottom:5px;">
              <thead>
                <tr>
                  <td>Rating</td><td>Delete?</td>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>
                    <a class="fancy fancybox.ajax" href=\""""
        data += url_for('priority', id=str(wish.id))+"""\">
                    <div class="rating">"""
        if wish.rating == "1" or wish.rating is None:
          data += """<img class="onestarrating" src=\""""
          data += url_for('static', filename='5-Star_rating_system.png')+"""\" height="100" width="100"/>""" 
        elif wish.rating == "2":
          data += """<img class="twostarrating" src=\""""
          data += url_for('static', filename='5-Star_rating_system.png')+"""\" height="100" width="100"/>"""
        elif wish.rating == "3":
          data += """<img class="threestarrating" src=\""""
          data += url_for('static', filename='5-Star_rating_system.png')+"""\" height="100" width="100"/>"""
        elif wish.rating == "4":
          data += """<img class="fourstarrating" src=\""""
          data += url_for('static', filename='5-Star_rating_system.png')+"""\" height="100" width="100"/>"""
        elif wish.rating == "5":
          data += """<img class="fivestarrating" src=\""""
          data += url_for('static', filename='5-Star_rating_system.png')+"""\" height="100" width="100"/>"""
        data +=    """</div></a>
                  </td><td><input class="entry" type="checkbox" name="wish" value=\""""
        data +=   str(wish.id)+"""\" onclick="javascript:delWish(event)"></td>
                </tr>
              </tbody>
            </table>
          </div>
          </div>
          </div>
          </div>"""
      elif wish.bought == "1":
        data += """<div class="bought" style="display:none;">
          <div id=\""""
        data += str(wish.id)+"""\" class="ih-item square colored effect9 right_to_left red"><a href=\""""
        data += wish.url+"""\" target="_blank">
          <div class="img"><img src=\""""
        data+= wish.thumbnail+"""\" alt="img" height="235" width="316"></div>
          <div class="info">
          <div class="info-back">
            <h3>"""
        data += wish.title+"""</h3>
            <p>"""
        data += wish.description+"""</p>
            <p><strong style="color:red;">This item was previously bought</strong></p></a>
            <table class="raise" style="margin:auto;color:white;margin-bottom:5px;">
              <thead>
                <tr>
                  <td>Rating</td><td>Delete?</td>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>
                    <a class="fancy fancybox.ajax" href=\""""
        data += url_for('priority', id=str(wish.id))+"""\">
                    <div class="rating">"""
        if wish.rating == "1" or wish.rating is None:
          data += """<img class="onestarrating" src=\""""
          data += url_for('static', filename='5-Star_rating_system.png')+"""\" height="100" width="100"/>""" 
        elif wish.rating == "2":
          data += """<img class="twostarrating" src=\""""
          data += url_for('static', filename='5-Star_rating_system.png')+"""\" height="100" width="100"/>"""
        elif wish.rating == "3":
          data += """<img class="threestarrating" src=\""""
          data += url_for('static', filename='5-Star_rating_system.png')+"""\" height="100" width="100"/>"""
        elif wish.rating == "4":
          data += """<img class="fourstarrating" src=\""""
          data += url_for('static', filename='5-Star_rating_system.png')+"""\" height="100" width="100"/>"""
        elif wish.rating == "5":
          data += """<img class="fivestarrating" src=\""""
          data += url_for('static', filename='5-Star_rating_system.png')+"""\" height="100" width="100"/>"""
        data +=    """</div></a>
                  </td><td><input class="entry" type="checkbox" name="wish" value=\""""
        data +=   str(wish.id)+"""\" onclick="javascript:delWish(event)"></td>
                </tr>
              </tbody>
            </table>
          </div>
          </div>
          </div>
          </div>"""
    return data
  data += '<h1 class="lash">Aww snap! Sorry there are no wishes in the selected category!</h1>'
  return data
    
@app.before_request
def before_request():
  g.user = current_user
    
def date_to_str(dt):
  return dt.strftime("%a, %d %b, %Y")


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)
    
@app.route('/<file_name>')
def preview(file_name):
    """Preview template."""
    return render_template(file_name, user=g.user, description="test", title="test", images=[])


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8888")
