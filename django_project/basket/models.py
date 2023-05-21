from django.db import models
from authapp.models import User
from mainapp.models import Product


class BasketQuerySet(models.QuerySet):

    def delete(self):
        for object in self:
            object.refresh_quantity()
        super().delete()


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()


    def __str__(self):
        return f" Корзина для {self.user.username} Товар {self.product.name}"

    def total(self):
        return self.quantity * self.product.price

    @property
    def baskets(self):
        return Basket.objects.filter(user=self.user)

    def total_quantity(self):
        return sum(i.quantity for i in self.baskets)

    def total_sum(self):
        return sum((i.total()) for i in self.baskets)

    def delete(self, using=None, keep_parents=False):
        self.product.quantity += self.quantity
        self.product.save()
        super().delete()

    def refresh_quantity(self):
        if self.pk:
            self.product.quantity -= self.quantity - Basket.objects.get(pk=self.pk).quantity
        else:
            self.product.quantity -= self.quantity
        self.product.save()

    def save(self, *args):
        self.refresh_quantity()
        super().save(*args)
