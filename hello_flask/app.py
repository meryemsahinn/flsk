from flask import Flask, request, make_response
from functools import wraps

app = Flask(__name__)


def auth_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
      auth = request.authorization
      if auth and auth.username == 'username' and auth.password == 'password':
          return f(*args, **kwargs)

      return make_response('could not verify your login', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

  return decorated


@app.route('/')
def index():
  if request.authorization and request.authorization.username == 'username' and request.authorization.password == 'password':
      return '<h1> logged in</h1>'


  return make_response('could not verify', 401,{'WWW-Authenticate':'Basic realm="Login Required"'})


@app.route('/mainpage')
@auth_required
def page():
  return '<h1> you are on the main page </h1>'


@app.route("/<string:url>")
@auth_required
def search(url):
  return  url


if __name__ == '__main__':
		    app.run(debug=True)