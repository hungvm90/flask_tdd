Using python 3
export FLASK_APP=price_adjust.py

- Test
-- flask test

Run:
    gunicorn -w 1 -b :6600 price_adjust:app --access-logfile out.log