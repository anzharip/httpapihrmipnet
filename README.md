# httpapihrmipnet
HTTP REST API PoC for HRM IPNet written in Python 3. 

# To use: 
1. Clone the repo. 

```git clone https://github.com/anzharip/httpapihrmipnet.git```

2. Enter the directory, create virtual env. 

```cd httpapihrmipnet```

```python3 -m venv ./```

3. Install dependencies. 

```python3 -m pip install -r requirements.txt```

4. Configure the DB connection. 

```vi config.py```

5. Run the app. 

```gunicorn --bind 0.0.0.0:5000 wsgi:app```
