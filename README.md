Please start the project file with commands below:
cd to the root file: for example, if you download the file with naming in C://FrameworkAssignment, please cd to the particular place first.

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

Then, ensure you are running the propertymanagement.settings


And this project do use the two-step verification, as just for testing, the verification code snet through 'email' will be shown in the terminal console. 
