from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tickets.db'
db = SQLAlchemy(app)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='open')

db.create_all()

@app.route('/')
def index():
    tickets = Ticket.query.all()
    return render_template('index.html', tickets=tickets)

@app.route('/ticket/create', methods=['POST'])
def create_ticket():
    title = request.form.get('title')
    description = request.form.get('description')
    ticket = Ticket(title=title, description=description)
    db.session.add(ticket)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/ticket/<int:ticket_id>')
def view_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    return render_template('ticket.html', ticket=ticket)

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/ticket/new')
def new_ticket():
    return render_template('submit_ticket.html')

