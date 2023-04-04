from django.shortcuts import render
from mainapp.models import Product, ProductCategory
from django.views.generic.list import ListView


def index(request):
    context = {'title': 'главная'}
    return render(request, 'mainapp/index.html', context)


class ProductListView(ListView):
    model = Product
    template_name = 'mainapp/products.html'
    paginate_by = 3

    def dispatch(self, request, *args, **kwargs):
        return super(ProductListView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if 'category_id' in kwargs.keys():
            self.object_list = Product.objects.filter(category_id=kwargs['category_id'])
        else:
            self.object_list = Product.objects.all()
        context = self.get_context_data()
        context['categories'] = ProductCategory.objects.all()
        return self.render_to_response(context)
