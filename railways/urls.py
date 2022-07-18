from django.urls import path
from django.conf import settings


from . import views

urlpatterns = [
    path("",views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("book/<train>/<date>", views.book, name="book"),
    path("pay", views.payment, name="payment"),
    path("pay/<pnr>/<int:price>", views.pay, name="pay"),
    path("<train>/<date>/<fname>/<lname>/<int:age>/<gender>/<seat>/<int:pnr>/<int:cost>", views.booking_page, name="booking"),
    path("train", views.check_train, name="check_train"),
    path("cancel", views.cancel, name="cancel"),
    path("PNR", views.check_pnr, name="check_pnr"),
    path("seat", views.seat, name="seat")
]

