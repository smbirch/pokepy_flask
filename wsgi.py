from app import app

if __name__ == "__main__":
    app.run()


WorkingDirectory=/home/smbirch/pokepy_flask
Environment="PATH=/home/smbirch/pokepy_flask/pokepyenv/bin"
ExecStart=/home/smbirch/pokepy_flask/pokepy/bin/gunicorn --workers 3 --bind unix:myproject.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target