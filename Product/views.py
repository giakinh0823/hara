import json
import math

import stripe
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from Order.models import Order, State
from Register.models import Profile, Notifications
from .models import *
from django.views import View
from django.conf import settings
from django.http import JsonResponse
from .getdata import data_scrap

import random

from django.contrib.auth.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.

def getData(request):
    data_scrap(request)
    return HttpResponse('done')


def products(request):
    group_category = CategoryGroup.objects.all()
    list_category = Category.objects.all()
    list_product = Product.objects.all()
    if request.method == 'GET':
        try:
            getProduct = request.GET['search']
        except:
            getProduct = None
        if getProduct:
            list_product = list_product.filter(Q(title__icontains=request.GET['search']))

    context = {
        'products': list_product,
        'group_category': group_category,
        'category_list': list_category
    }
    if request.user.is_authenticated:
        notify = Notifications.objects.filter(user=request.user)
        newNotify = Notifications.objects.filter(new=True, user=request.user)
        request.session['newNotify'] = len(newNotify)
        if notify or newNotify:
            request.session['newNotify'] = len(newNotify)
            notify = notify[:len(notify) - len(newNotify)]
            notify = reversed(notify)
            if not newNotify or len(newNotify) == 0:
                newNotify = None
            else:
                newNotify = reversed(newNotify)
        context = {
            'products': list_product,
            'group_category': group_category,
            'category_list': list_category,
            'newNotify': newNotify,
            'notify': notify,
        }
    return render(request, 'product/products.html', context)


def productDetail(request, slug):
    product_detail = Product.objects.get(slug=slug)
    profile_detail = Profile.objects.get(user=product_detail.user)
    profile_user = None
    if request.user.is_authenticated:
        profile_user = Profile.objects.get(user=request.user)
    list_products = Product.objects.filter(category=product_detail.category)
    ran = random.randint(0, len(list_products) - 3)
    videos = Video.objects.filter(product=product_detail)
    images = Image.objects.filter(product=product_detail)
    comments = Comment.objects.filter(product=product_detail)
    context = {
        'product_detail': product_detail,
        'profile_detail': profile_detail,
        'list_products': list_products[ran:ran + 3],
        'videos': videos,
        'images': images,
        'comments': comments,
        'profile_user': profile_user,
        'STRIPE_SECRET_KEY': settings.STRIPE_SECRET_KEY,
    }
    if request.user.is_authenticated:
        notify = Notifications.objects.filter(user=request.user)
        clickNotify = notify.filter(link=product_detail.get_absolute_url())
        for item in clickNotify:
            item.new = False
            item.save()
        newNotify = Notifications.objects.filter(new=True, user=request.user)
        notify = notify[:len(notify) - len(newNotify)]
        request.session['newNotify'] = len(newNotify)
        if notify or newNotify:
            request.session['newNotify'] = len(newNotify)
            notify = notify[:len(notify) - len(newNotify)]
            notify = reversed(notify)
            if not newNotify or len(newNotify) == 0:
                newNotify = None
            else:
                newNotify = reversed(newNotify)
        context = {
            'product_detail': product_detail,
            'profile_detail': profile_detail,
            'list_products': list_products[ran:ran + 3],
            'videos': videos,
            'images': images,
            'comments': comments,
            'profile_user': profile_user,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
            'newNotify': newNotify,
            'notify': notify,
        }
    return render(request, 'product/product_detail.html', context)


def category(request, slug):
    categoryDetail = Category.objects.get(slug=slug)
    product = Product.objects.filter(category=categoryDetail)
    group_category = CategoryGroup.objects.all()
    list_category = Category.objects.all()
    if request.method == 'GET':
        try:
            getProduct = request.GET['search']
        except:
            getProduct = None
        if getProduct:
            product = product.filter(Q(title__icontains=request.GET['search']))
    context = {
        'category': categoryDetail,
        'products': product,
        'group_category': group_category,
        'category_list': list_category
    }
    if request.user.is_authenticated:
        notify = Notifications.objects.filter(user=request.user)
        newNotify = Notifications.objects.filter(new=True, user=request.user)
        request.session['newNotify'] = len(newNotify)
        notify = notify[:len(notify) - len(newNotify)]
        if notify or newNotify:
            request.session['newNotify'] = len(newNotify)
            notify = notify[:len(notify) - len(newNotify)]
            notify = reversed(notify)
            if not newNotify or len(newNotify) == 0:
                newNotify = None
            else:
                newNotify = reversed(newNotify)
        context = {
            'category': categoryDetail,
            'products': product,
            'group_category': group_category,
            'category_list': list_category,
            'newNotify': newNotify,
            'notify': notify,
        }
    return render(request, 'Product/category.html', context)


def groupCategory(request, slug):
    group_category = CategoryGroup.objects.all()
    list_category = Category.objects.all()
    category_group = group_category.get(slug=slug)
    product = Product.objects.all()
    if request.method == 'GET':
        try:
            getProduct = request.GET['search']
        except:
            getProduct = None
        if getProduct:
            product = product.filter(Q(title__icontains=request.GET['search']))
    context = {
        'products': product,
        'group_category': group_category,
        'category_list': list_category,
        'category_group': category_group,
    }
    if request.user.is_authenticated:
        notify = Notifications.objects.filter(user=request.user)
        newNotify = Notifications.objects.filter(new=True, user=request.user)
        request.session['newNotify'] = len(newNotify)
        notify = notify[:len(notify) - len(newNotify)]
        if notify or newNotify:
            request.session['newNotify'] = len(newNotify)
            notify = notify[:len(notify) - len(newNotify)]
            notify = reversed(notify)
            if not newNotify or len(newNotify) == 0:
                newNotify = None
            else:
                newNotify = reversed(newNotify)
        context = {
            'products': product,
            'group_category': group_category,
            'category_list': list_category,
            'category_group': category_group,
            'newNotify': newNotify,
            'notify': notify,
        }
    return render(request, 'Product/group_category.html', context)


@login_required
def create_product(request):
    if request.user.is_authenticated:
        notify = Notifications.objects.filter(user=request.user)
        newNotify = Notifications.objects.filter(new=True, user=request.user)
        request.session['newNotify'] = len(newNotify)
        notify = notify[:len(notify) - len(newNotify)]
        if notify or newNotify:
            request.session['newNotify'] = len(newNotify)
            notify = notify[:len(notify) - len(newNotify)]
            notify = reversed(notify)
            if not newNotify or len(newNotify) == 0:
                newNotify = None
            else:
                newNotify = reversed(newNotify)
        context = {
            'newNotify': newNotify,
            'notify': notify,
        }
    return render(request, 'product/create_product.html')


# 4242 4242 4242 4242
class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        product = Product.objects.get(slug=slug)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        # 'unit_amount': int(math.ceil(product.price)) * 100,
                        'unit_amount': 1000,
                        'product_data': {
                            'name': product.title,
                            # 'images': product.img.url,
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/' + slug + '/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


@login_required
def loading(request, slug):
    product = Product.objects.get(slug=slug)
    return render(request, "order/loading.html",
                  {'product': product, 'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY, })


@login_required
def success(request, slug):
    product = Product.objects.get(slug=slug)
    return render(request, "order/success.html", {'product': product})


@login_required
def done(request):
    notify = Notifications.objects.filter(user=request.user)
    newNotify = Notifications.objects.filter(new=True, user=request.user)
    request.session['newNotify'] = len(newNotify)
    notify = notify[:len(notify) - len(newNotify)]
    if notify or newNotify:
        request.session['newNotify'] = len(newNotify)
        notify = notify[:len(notify) - len(newNotify)]
        notify = reversed(notify)
        if not newNotify or len(newNotify) == 0:
            newNotify = None
        else:
            newNotify = reversed(newNotify)

    context = {
        'newNotify': newNotify,
        'notify': notify,
    }
    return render(request, "order/done.html", context)


@login_required
def error(request):
    return render(request, "order/error.html")


@login_required
def cancel(request):
    return render(request, "order/cancel.html")
