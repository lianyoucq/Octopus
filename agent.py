# -*- coding:utf-8 -*-
from octopus import app
from octopus.common.logger import mainLogger


if __name__ == '__main__':
    mainLogger.debug( app.config)
    app.run(app.config.get('HOST'), port=app.config.get("PORT"), debug = app.config.get("DEBUG"))
