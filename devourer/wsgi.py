# coding: utf-8

import os

from devourer.systemwide import app
from devourer.usagicompat import DevourerUsagiClient


usagi = DevourerUsagiClient(app.wsgi_app, os.getenv('TSUKINO_USAGI_URL', 'http://127.0.0.1:5900'), 'devourer')
app.wsgi_app = usagi.app
usagi()


if __name__ == '__main__':
    app.run(port=app.config.get('SERVER_PORT', 6606))
