# -*- coding: utf-8 -*-
"""
Application Launch
------------------
"""

import os
from config import DevConfig
from picture import create_app

app = create_app('config.DevConfig')


@app.template_filter('autoversion')
def autoversion_filter(filename):
    fullpath = os.path.join('picture/', filename[1:])
    try:
        timestamp = str(os.path.getmtime(fullpath))
    except OSError:
        return filename
    newfilename = "{0}?v={1}".format(filename, timestamp)
    return newfilename


if __name__ == "__main__":
    app.run()
