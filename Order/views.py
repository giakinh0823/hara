from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail

# Create your views here.
from Order.models import Order, State
from Product.models import Product
from Register.models import Notifications, Profile


@login_required
def order(request):
    productFavorites = Product.objects.filter(user=request.user)
    profile = Profile.objects.get(user=request.user)
    # if productFavorites:
    #     productFavorites = productFavorites[len(productFavorites) - 7:]
    orders = Order.objects.filter(user=request.user)
    notifyOrder = Notifications.objects.filter(user=request.user)
    for item in notifyOrder:
        if not item.link.find('order') == -1:
            item.new = False
            item.save()
    newNotify = Notifications.objects.filter(new=True, user=request.user)
    notify = notifyOrder[:len(notifyOrder) - len(newNotify)]
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
        'newNotify': newNotify,
        'notify': notify,
        'orders': orders,
        'productFavorites': productFavorites,
        'profile': profile
    }
    return render(request, 'order/order.html', context)


def active_order(request):
    if request.is_ajax():
        id = request.GET["id"]
        my_order = Order.objects.get(id=id)
        if my_order.is_active:
            my_order.is_active = False
        else:
            my_order.is_active = True
        my_order.save()
        return JsonResponse({"data": "Is active"})


def success_order(request):
    if request.is_ajax():
        id = request.GET["id"]
        my_order = Order.objects.get(id=id)
        my_order.state = State.objects.get(slug="success")
        my_order.is_complete = True
        my_order.save()
        return JsonResponse({
            "user": str(my_order.user.username),
            "person": str(my_order.person.username),
            "product": my_order.product.title,
            "link": "/invest",
            "text": my_order.product.title,
        })


def cancel_order(request):
    if request.is_ajax():
        id = request.GET["id"]
        my_order = Order.objects.get(id=id)
        my_order.state = State.objects.get(slug="cancel")
        my_order.is_complete = False
        my_order.save()
        return JsonResponse({
            "user": str(my_order.user.username),
            "person": str(my_order.person.username),
            "product": my_order.product.title,
            "link": "/invest",
            "text": my_order.product.title,
        })


def accept_order(request):
    if request.is_ajax():
        id = request.GET["id"]
        my_order = Order.objects.get(id=id)
        my_order.state = State.objects.get(slug="waiting")
        my_order.save()
        return JsonResponse({
            "user": str(my_order.user.username),
            "person": str(my_order.person.username),
            "product": my_order.product.title,
            "link": "/invest",
            "text": my_order.product.title,
        })


def invest(request):
    orders = Order.objects.filter(person=request.user)
    notify = Notifications.objects.filter(user=request.user)
    notifyOrder = Notifications.objects.filter(user=request.user)
    for item in notifyOrder:
        if not item.link.find('invest') == -1:
            item.new = False
            item.save()
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
        "orders": orders,
    }
    return render(request, 'Order/invest.html', context)


@login_required
def complain(request, slug):
    product = Product.objects.get(slug=slug)
    if request.is_ajax():
        email = request.POST["email"]
        content = request.POST["content"]
        send_mail("Report product - " + str(product.title), "S???n ph???m c???a b???n ???? b??? khi???u n???i. "
                                                            "\nB???n c?? th??? b??? ????nh ch??? v??nh vi???n n???u nh?? ch??ng t??i x??c th???c ch??nh x??c ??i???u n??y"
                                                            "\n??i???u n??y d???n ?????n vi???c b???n vi ph???m ch??nh s??ch c???a ch??ng t??i v?? ch??ng t??i s??? m???i c??c c?? quan t??? ch???c v??o gi???i quy???t."
                                                            "\nXin li??n h??? v???i ch??ng t??i ????? bi???t th??m chi ti???t."
                                                            "\nCh??ng t??i s??? gi???i quy???t m???i v???n ????? qua ?????a ch??? email: giakinhfullstack@gmail.com"
                                                            "\nXin c???m ??n"
                                                            "\nDear, Hara",
                  'giakinhfullstack@gmail.com',
                  [product.user.email])
        send_mail("Report product - " + str(product.title), "Ch??ng t??i ???? nh???n ???????c ????n khi???u n???i c???a b???n v??? s???n ph???m " + product.title + ""
                                                            "\nB???n xin vui l??ng cung c???p c??c h??nh ???nh v?? th??ng tin r?? r??ng b???ng vi???c tr??? l???i mail n??y."
                                                            "\nTh??ng tin bao g???m h??a ????n, tin nh???n, v?? c??c th??ng tin v??? s???n ph???m, l???ch s??? giao d???ch, l???ch s??? order s???n ph???m"
                                                            "\nCh??ng t??i s??? xem x??t v??? th??ng tin c???a b???n k??? l?????ng v?? gi??p b???n ho??n l???i s??? ti???n c???a b???n."
                                                            "\nXin c???m ??n."
                                                            "\nDear, Hara",
                  'giakinhfullstack@gmail.com',
                  [email])
        send_mail("Report product - " + str(product.title), str(content + " \nFrom email: " + email),
                  'giakinhfullstack@gmail.com',
                  ['giakinhfullstack@gmail.com'])
        return JsonResponse({"success": "success"})
    return render(request, 'Order/complain.html', {"product": product})
