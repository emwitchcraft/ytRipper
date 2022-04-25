from logging import exception
import os
try:
    os.system('pip3 install -r requirements.txt')
except Exception as e:
    input(e)