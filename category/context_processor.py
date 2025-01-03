from category.models import category

def menu_link(request):
    link=category.objects.all()
    return dict({'link':link})