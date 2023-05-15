from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/blog.db'
db = SQLAlchemy(app)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime)

    def __init__(self, title, content, created_at):
        self.title = title
        self.content = content
        self.created_at = created_at

@app.route('/')
def index():
    entries = Entry.query.order_by(Entry.created_at.desc()).all()
    return render_template('index.html', entries=entries)

@app.route('/entry/<int:id>')
def entry(id):
    entry = Entry.query.get(id)
    return render_template('entry.html', entry=entry)

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        created_at = datetime.datetime.now()
        entry = Entry(title=title, content=content, created_at=created_at)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('new.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
