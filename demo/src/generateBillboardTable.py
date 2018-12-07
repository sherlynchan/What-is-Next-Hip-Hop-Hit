import os
import sys
# setup the environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                       'spotify.settings')
import django
django.setup()
args = sys.argv

from frontpage.models import BillboardData


def populate():
    with open('../data/billboard_2014_to_current.csv','r') as f:
        for line in f:
            print(line)
            




if __name__ == "__main__":
    populate()