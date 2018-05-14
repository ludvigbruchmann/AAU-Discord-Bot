import flask
import urllib.request

import config

# Create the application.
APP = flask.Flask(__name__)

@APP.route('/verify/')
def index():

    ticket = flask.request.args.get('ticket', None)

    url = config.verifyUrl + '?ticket=' + ticket + '&service=' + config.redirectUrl
    response = urllib.request.urlopen(url).read()
    print(str(response))
    if 'cas:authenticationSuccess' in str(response):
        response = "Ticket verified"
    else:
        response = "Invalid ticket"
    return flask.render_template('index.html', response=response)

if __name__ == '__main__':
    APP.debug=True
    APP.run()
