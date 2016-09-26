from flask import Flask, send_from_directory
from parser import getCal

flask_app = Flask(__name__)

@flask_app.route('/cal/<regex>')
def render_get(regex):
  getCal(regex)
  return send_from_directory(filename='my.ics')

if __name__ == "__main__":
  flask_app.run(port=5999, host='0.0.0.0')
