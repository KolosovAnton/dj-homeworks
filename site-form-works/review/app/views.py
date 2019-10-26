from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView

from .models import Product, Review
from .forms import ReviewForm


class ProductsList(ListView):
    model = Product
    context_object_name = 'product_list'


class ProductView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(product=self.object)
        context['form'] = ReviewForm
        if self.object.id in self.request.session.get('has_commented', []):
            context['has_commented'] = self.request.session.get('has_commented')
            context['is_review_exist'] = True
        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        form = ReviewForm(self.request.POST)
        has_commented = self.request.session.get('has_commented', [])
        if form.is_valid() and pk not in has_commented:
            review = form.save(commit=False)
            review.product_id = pk
            review.save()
            has_commented.append(pk)
            self.request.session['has_commented'] = has_commented
        return redirect(reverse('product_detail', kwargs={'pk': pk}))
