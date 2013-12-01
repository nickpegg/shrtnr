#!/usr/bin/env python

import datetime
import hashlib
from urlparse import urlparse

from flask import Flask, request, render_template, redirect

from models import Url


app = Flask(__name__)


# View functions
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        thing = request.form.get('url')
        if thing:
            if '://' not in thing:
                thing = 'http://' + thing

            # Verify the URL
            parsed = urlparse(thing)
            if parsed.scheme not in ('http', 'https'):
                return "I only take HTTP or HTTPS URLs, dummy"

            urlhash = hashlib.sha1(thing).hexdigest()
            try:
                url = Url.get(Url.url_hash == urlhash)
            except:
                url = Url()
                url.url = thing
                url.url_hash = urlhash
                url.created = datetime.datetime.now()
                url.save()

                # hokay. got us an ID, let's make a key.
                url.key = base36_encode(url.id)
                url.save()

            return render_template('added.html', short_url="http://{0}/{1}".format(request.headers['host'], url.key))
        else:
            return "You didn't give me shit"
    else:
        return render_template('index.html')


@app.route('/<key>')
def go(key):
    result = "There's no URL with that key, dummy!"

    try:
        url = Url.get(Url.key == key)
        if url.enabled:
            result = redirect(url.url)
    except:
        pass

    return result


# Utility functions
def base36_encode(num):
    """ stolen from the Wikipedia example, threw away shit I didn't need """
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'
    result = ''

    while num != 0:
        num, i = divmod(num, 36)
        result = alphabet[i] + result

    return result


def base36_decode(stuff):
    return int(stuff, 36)


if __name__ == "__main__":
    try:
        Url.create_table()
    except:
        pass    # Pfft, whatever.

    app.run(debug=True)
