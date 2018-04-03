# -*- coding:utf-8 -*-
from octopus import app
from octopus.common.logger import mainLogger
from werkzeug.contrib.fixers import ProxyFix

app.wsgi_app = ProxyFix(app.wsgi_app)


if __name__ == '__main__':
    mainLogger.debug(app.config)
    app.run(app.config.get('HOST'), app.config.get("PORT"))


