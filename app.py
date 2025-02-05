from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///giri.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model for the Contact Manager
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)

# Create the database tables before handling any request
@app.before_request
def create_tables():
    db.create_all()

# Home Route - Show the index page
@app.route('/')
def index():
    return render_template('index.html')

# Get all contacts
@app.route('/contacts', methods=['GET'])
def get_contacts():
    search_query = request.args.get('search')
    if search_query:
        contacts = Contact.query.filter(Contact.name.like(f'%{search_query}%')).all()
    else:
        contacts = Contact.query.all()
    contacts_list = [{'id': contact.id, 'name': contact.name, 'phone': contact.phone, 'email': contact.email} for contact in contacts]
    return jsonify(contacts_list)

# Add a Contact
@app.route('/add', methods=['POST'])
def add_contact():
    data = request.json
    name = data.get('name')
    phone = data.get('phone')
    email = data.get('email')

    if name and phone and email:
        new_contact = Contact(name=name, phone=phone, email=email)
        db.session.add(new_contact)
        db.session.commit()
        return jsonify({'message': 'Contact added successfully!'}), 201
    return jsonify({'error': 'Invalid contact data'}), 400

# Delete a Contact
@app.route('/delete/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    contact = Contact.query.get(contact_id)
    if contact:
        db.session.delete(contact)
        db.session.commit()
        return jsonify({'message': 'Contact deleted successfully!'})
    return jsonify({'error': 'Contact not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
cd 