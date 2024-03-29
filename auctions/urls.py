from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.new_item, name="new_item"),
    path("<int:list_id>", views.view_item, name="view_item"),
    path("<int:list_id>/comment", views.comment, name="comment"),
    path("watchlist", views.watch_list, name="watchlist"),
    path("<int:list_id>/add", views.add_watch_list, name="addwatchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<int:cats>", views.category_list, name="categoriesList"),
    path("<int:list_id>/bid", views.bid, name="placeBid"),
    path("<int:list_id>/closeBid", views.close_bid, name="CloseBid"),
]
