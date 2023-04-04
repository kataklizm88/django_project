from basket.models import Basket
from mainapp.models import Product
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator


class BasketAddView(TemplateView):
    model = Basket
    template_name = 'authapp/profile.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(BasketAddView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(id=kwargs['product_id'])
        baskets = Basket.objects.filter(user=request.user, product=product)
        if not baskets.exists():
            basket = Basket(user=request.user, product=product)
            basket.quantity += 1
            basket.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            basket = baskets.first()
            basket.quantity += 1
            basket.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class BasketRemoveView(TemplateView):
    model = Basket
    template_name = 'authapp/profile.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(BasketRemoveView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        basket = Basket.objects.get(id=kwargs['pk'])
        basket.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, id, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        basket = Basket.objects.get(id=int(id))
        if quantity > 0:
            basket.quantity = quantity
            basket.save()
        else:
            basket.delete()
        baskets = Basket.objects.filter(user=request.user)
        context = {
            'baskets': baskets
        }
        result = render_to_string('basket/basket.html', context)
        return JsonResponse({'result': result})
