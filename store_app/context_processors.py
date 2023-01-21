from .models import Category,CartProduct
from django.contrib.auth.decorators import login_required
def category(request):
    cate = Category.objects.filter(parent_category=None)

    context ={
        'cate':cate
    }
    return context

