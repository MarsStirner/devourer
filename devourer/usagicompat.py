# -*- coding: utf-8 -*-

from tsukino_usagi.client import TsukinoUsagiClient
from devourer.systemwide import app, db, cas
from devourer.api.app import module as api_module


class DevourerUsagiClient(TsukinoUsagiClient):
    def on_configuration(self, configuration):
        app.config.update(configuration)

        db.init_app(app)
        cas.init_app(app)

        app.register_blueprint(api_module, url_prefix='/api')
