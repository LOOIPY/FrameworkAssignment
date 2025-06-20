Please start the project file with commands below:

python -m venv venv
venv\Scripts\activate
python.exe -m pip install --upgrade pip 
pip install django
pip install -r requirements.txt 
python -m pip install Pillow  
pip install social-auth-app-django 
pip install djangorestframework
pip install qrcode
python manage.py makemigrations
python manage.py migrate
python manage.py runserver


And this project do use the two-step verification, as just for testing, the verification code snet through 'email' will be shown in the terminal console. 
