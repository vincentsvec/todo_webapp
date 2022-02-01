from .models import Lists
from django.contrib.auth.models import User
import json


def tdlist_renderer(response):
    '''
    Renders all todolists
    '''

    if response.user.is_authenticated:
        return {'tdlist': response.user.lists.all().order_by('order')}

    return {'tdlist': None}


def order_lists(response):
    '''
    Gets order of lists passed by javascript into post request after sorting ends
    '''

    order = response.body.decode('utf-8')

    if 'order' in order:
        order = json.loads(order)
        if str(response.user) == order['user']:
            order = order['order']

            count = 0
            for i in order:
                tdlist = response.user.lists.get(name=i)
                tdlist.order = count
                tdlist.save()
                count += 1
