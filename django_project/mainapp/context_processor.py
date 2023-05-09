from basket.models import Basket

def show_basket_user(request):
    total = 0
    if request.user.is_authenticated and Basket.objects.filter(user=request.user):
        total = Basket.objects.filter(user=request.user)[0].total_sum()
    return {'total': total}
