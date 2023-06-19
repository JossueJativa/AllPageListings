from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    ## Modelos de vista creados
    path("categories", views.category, name="categories"),
    path("creates", views.creates, name="creates"),
    path("bids/<int:id>", views.bids, name="bids"),
    path("comments/<int:id>", views.comments, name="comments"),
    path("exception", views.exception, name="exception"),
    path("watchlist/<int:id>", views.watchlist, name="watchlist"),
    path("viewWatchlist", views.viewWatchlist, name="viewWatchlist"),
    path("deleteWatchlist/<int:id>", views.deleteWatchlist, name="deleteWatchlist"),
    path("mylistings", views.mylistings, name="mylistings"),
]
