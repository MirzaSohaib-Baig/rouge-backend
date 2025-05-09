from waitress import serve
from Rough_Secret_Web_App.wsgi import application

serve(application, host='0.0.0.0', port=8000)
