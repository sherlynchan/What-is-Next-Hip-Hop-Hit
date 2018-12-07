import os
import sys
import datetime
# setup the environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'spotify.settings')
import django
django.setup()
args = sys.argv

from frontpage.models import BillboardData

def populate():
    with open('data/billboard_2014_to_current.csv','r') as f:
        # skip first line for header
        next(f)
        for line in f:
            line = line.replace('\n','')
            data = line.split(',')
            print(data)
            BillboardData.objects.get_or_create(
                date = datetime.datetime.strptime(data[0],'%Y-%m-%d'),
                artist = data[1],
                isNew = data[2],
                lastPos = data[3],
                peakPos = data[4],
                rank = data[5],
                title = data[6],
                weeks = data[7]
                )
            

if __name__ == "__main__":
    populate()