# httpapihrmipnet
HTTP REST API PoC for HRM IPNet written in Python 3. 

# To use: 
1. Clone the repo. 

```git clone https://github.com/anzharip/httpapihrmipnet.git```

2. Enter the directory, create virtual environment. 

```cd httpapihrmipnet```

```python3 -m venv env```

3. Activate virtual environment. 

```
source env/bin/activate
```

4. Install dependencies. 

```python3 -m pip install -r requirements.txt```

5. Configure the DB connection. 

```vi config.py```

6. Run the app. 

```gunicorn --bind 0.0.0.0:5000 wsgi:app```

# config.py Example

```
# Database host
DBHOST = "localhost"

# Database user credential
DBUSER = "username"

# Database password credential
DBPASS = "password"

# Database name
DBNAME = "app"

# Database post
DBPORT = 3306

# Flask secret key for session signing
SECRET_KEY = "somesecret"

# Flask-JWT-Extended key for token signing
JWT_SECRET_KEY = "somejwtsecret"

# Flask-JWT-Extended token expiration in second
JWT_ACCESS_TOKEN_EXPIRES = 900

# User cryptographically strong random numbers suitable for managing data such as passwords, account authentication, security tokens, and related secrets (Lib/secrets.py) and convert it to base64 encoding
B64KEY = "ASWmyzvfxAYaxbIoCYrLV9O7l2TFVn1silaCfeEPRXw"
```
