import os
try:
    os.system('py pip3 install -r requirements.txt')
except Exception as e:
    input(e)