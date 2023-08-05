# User Registration - Flask Web App :brazil: :brazil::brazil::brazil::brazil::brazil::brazil:



This is a web application project developed with Flask, a Python web framework, that allows users to register and store their information in a SQLite database. The project includes a registration form with field validations, file upload, and interaction with an external API to fetch address information based on the provided ZIP code.


## Functionalities:

User registration with the following fields:

CPF/CNPJ (validated for 11 or 14 digits, numbers only);
Full Name;
Date of Birth;
Gender (options: male, female, and others);
Marital Status (options: single, married, and others);
Email (validated for a valid and non-duplicate email);
Phone number (validated for 11 digits, area code + phone number, together);
Password (with confirmation validation);
Address (ZIP code, Street, Number, Complement, Neighborhood, City, and State);
Identification (file upload).
Real-time data validations using JavaScript and jQuery:

CPF/CNPJ validation (11 or 14 digits);
Phone number validation (11 digits).
Secure password storage using the Werkzeug library.

Verification of registered emails and CPF/CNPJ to avoid duplicates.

## Prerequisites:

Python 3.x
Flask
Flask-WTF
Flask-SQLAlchemy
Werkzeug
Requests
Installation:

Clone this repository to your local machine:
```bash
git clone https://github.com/joseabrantesjr/SistemaJoseAbrantesJr.git
```

Access the project directory:
```bash
cd SistemaJoseAbrantesJr
```


Create and activate a virtual environment (optional, but recommended):

```bash
python -m venv venv
```

On Windows: venv\Scripts\activate

On Linux/Mac: source venv/bin/activate

Install project dependencies:
```bash
pip install -r requirements.txt
```
Start the Flask server:
```bash
python app.py
```
Access the application in the browser at http://localhost:5000/


## Contribution:

Contributions are welcome! If you have found any issues, have suggestions for improvements, or want to add new features, feel free to create a Pull Request.

## License:

This project does not have a license. Feel free to use and modify the code according to your needs.
