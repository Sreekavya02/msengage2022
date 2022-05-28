from django.urls import re_path
from my_app import views

urlpatterns=[
    re_path(r'^$',views.index,name="index"),
    re_path(r'^register/$',views.register,name="register"),
    re_path(r'^login/$',views.user_login,name="login"),
    re_path(r'^logout/$',views.user_logout,name="logout"),
    re_path(r'^details/(?P<id>\d+)/$',views.getMovie_details,name="MovieDetails"),
    re_path(r'^details2',views.getMovie_details2,name="MovieDetails2"),
    re_path(r'^actionmovies/$',views.actionmovies,name="actionMovies"),
    re_path(r'^crimemovies/$',views.crimemovies,name="crimeMovies"),
    re_path(r'^romancemovies/$',views.romancemovies,name="romanceMovies"),
    re_path(r'^animationmovies/$',views.animationmovies,name="animationMovies"),
    re_path(r'^fantasymovies/$',views.fantasymovies,name="fantasyMovies"),
    re_path(r'^dramamovies/$',views.dramamovies,name="dramaMovies"),
    re_path(r'^science_fictionmovies/$',views.scfictionmovies,name="scfictionMovies"),

]