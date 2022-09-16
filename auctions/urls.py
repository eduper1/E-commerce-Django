from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("<int:list_id>", views.list_page, name="auctions_list"),
    path("<int:list_id>/comment", views.comment, name="comment"),
    path("watchlist", views.watch_list, name="watchlist" )
]
