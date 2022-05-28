from django.shortcuts import render
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from my_app.forms import UserForm
from my_app.algorithm import recommend,gettitles,fetch_details,get_genreMovies

movies_titles=gettitles()

actionMovieids,adventureMovieids,thrillerMovieids,romanceMovieids,crimeMovieids,scfictionMovieids,fantasyMovieids,dramaMovieids,animationMovieids=get_genreMovies()
actionMovie_details=[]
crimeMovie_details=[]
romanceMovie_details=[]
animationMovie_details=[]
adventureMovie_details=[]
fantasyMovie_details=[]
dramaMovie_details=[]
scfictionMovie_details=[]

for i in range(10):
    actionMovie_details.append(fetch_details(actionMovieids[i]))
    crimeMovie_details.append(fetch_details(crimeMovieids[i]))
    romanceMovie_details.append(fetch_details(romanceMovieids[i]))
    animationMovie_details.append(fetch_details(animationMovieids[i]))
    fantasyMovie_details.append(fetch_details(fantasyMovieids[i]))
    dramaMovie_details.append(fetch_details(dramaMovieids[i]))
    scfictionMovie_details.append(fetch_details(scfictionMovieids[i]))

def actionmovies(request):
    return render(request,'my_app/newindex.html',{'pagename':'action','movies':actionMovie_details,'movies_titles':movies_titles})

def crimemovies(request):
    return render(request,'my_app/newindex.html',{'pagename':'crime','movies':crimeMovie_details,'movies_titles':movies_titles})

def romancemovies(request):
    return render(request,'my_app/newindex.html',{'pagename':'romance','movies':romanceMovie_details,'movies_titles':movies_titles})

def animationmovies(request):
    return render(request,'my_app/newindex.html',{'pagename':'animation','movies':animationMovie_details,'movies_titles':movies_titles})

def fantasymovies(request):
    return render(request,'my_app/newindex.html',{'pagename':'fantasy','movies':fantasyMovie_details,'movies_titles':movies_titles})

def dramamovies(request):
    return render(request,'my_app/newindex.html',{'pagename':'drama','movies':dramaMovie_details,'movies_titles':movies_titles})

def scfictionmovies(request):
    return render(request,'my_app/newindex.html',{'pagename':'scfiction','movies':scfictionMovie_details,'movies_titles':movies_titles})

def index(request):
    return render(request,'my_app/newindex.html',{'pagename':'newreleases','movies':fantasyMovie_details,'movies_titles':movies_titles})



def getMovie_details(request,id):
    movieDetails=fetch_details(id)
    movie_id,recommendedmoviesids = recommend(movieDetails['title'])
    recommendedmovies = []
    for id in recommendedmoviesids:
        movie_details = fetch_details(id)
        recommendedmovies.append(movie_details)
    return render(request,'my_app/movieDetails.html',{'movie':movieDetails1,'recommendedmovies':recommendedmovies1,'movies_titles':movies_titles})



def getMovie_details2(request):
    moviename=request.POST.get('selectedmovie')
    movie_id, recommendedmoviesids = recommend(moviename)
    movieDetails = fetch_details(movie_id)
    recommendedmovies = []
    for id in recommendedmoviesids:
        movie_details = fetch_details(id)
        recommendedmovies.append(movie_details)

    return render(request, 'my_app/movieDetails.html', {'movie': movieDetails, 'recommendedmovies': recommendedmovies,'movies_titles':movies_titles})



def register(request):
    registered = False
    if(request.method == "POST"):
        username=request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_form=UserForm(data={'username':username,'email':email,'password':password})
        if(user_form.is_valid()):
            user=user_form.save()
            user.set_password(user.password)
            user.save()
            registered=True
            return redirect('/login')
        else:
            print(user_form.errors)
    else:
        return render(request, 'my_app/registration.html')


def user_login(request):
    if (request.method == 'POST'):
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account not active")
        else:
            return HttpResponse("user not registered before")
    else:
        return render(request,'my_app/login.html')

@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

