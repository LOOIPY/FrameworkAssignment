from django.shortcuts import render
from .models import Phone, Review

# Create your views here.
def index(request):
    """
    首页视图函数，显示所有手机和评论
    """
    phones = Phone.objects.all()
    reviews = Review.objects.all()
    
    context = {
        'phones': phones,
        'reviews': reviews,
    }
    
    return render(request, 'phoneReview/index.html', context)
