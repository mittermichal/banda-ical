from flask import Flask
from parser import getCal

flask_app = Flask(__name__)

@flask_app.route('/cal/<regex>')
def render_get(regex):
  return getCal(regex)

if __name__ == "__main__":
  flask_app.run(port=5999, host='0.0.0.0')
