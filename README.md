Using python 3
export FLASK_APP=price_adjust.py

- Test
-- flask test

Run:
    gunicorn -w 4 -b :9090 price_adjust:app