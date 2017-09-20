from flask import Flask, send_from_directory, make_response
from banda_parser import getCal

flask_app = Flask(__name__)

@flask_app.route('/cal/<regex>')
def render_get(regex):
  getCal(regex)
  resp = make_response(send_from_directory(filename='my.ics',directory='.'))
  resp.cache_control.max_age = 300
  resp.cache_control.public = True
  return resp
if __name__ == "__main__":
  flask_app.run(port=5998, host='0.0.0.0', debug=True)
