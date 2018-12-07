import django_tables2 as tables
from models import BillboardData


class BillboardTable(tables.Table):
    class Meta():
        model = BillboardData
