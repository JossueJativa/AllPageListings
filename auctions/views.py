from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import NoReverseMatch, reverse

from .models import Comments, Listings, User, Categories, Bids, Watchlist


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listings.objects.filter(active=True).all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


##Parte de desarrollo de Jossue Jativa
def category(request):
    return render(request, "auctions/categories.html",{
        "categories": Categories.objects.all()
    })

def creates(request):
    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]
        image = request.POST["image"]
        category = Categories.objects.get(category=request.POST["category"])
        price = request.POST["price"]
        user = User.objects.get(username=request.user.username)
        active = True

        if name == "" or description == "" or image == "":
            return render(request, "auctions/create.html", {
                "message": "Error al crear el listado."
            })

        # Attempt to create new user
        try:
            listing = Listings(name=name, description=description, image=image, category=category, 
                               user=user, active=active, price_start=price)
            listing.save()
        except IntegrityError:
            return render(request, "auctions/create.html", {
                "message": "Error al crear el listado."
            })
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html", {
            "categories": Categories.objects.all()
        })
    
def bids(request, id):
    if request.method == "POST":
        price = request.POST["price"]
        listing = Listings.objects.get(id=id)
        price_bid = Listings.objects.get(id=id).price_start
        user = User.objects.get(username=request.user.username)

        if price == "":
            return render(request, "auctions/exception.html", {
                "message": "Error al poner la oferta, No debe ser menor a la oferta actual."
            })
        
        if float(price) <= float(price_bid):
            return render(request, "auctions/exception.html" , {
                "message": "Error al poner la oferta, No debe ser menor a la oferta actual."
            })
        else:
            Listings.objects.filter(id=id).update(price_start=price)

        try:
            bid = Bids(price_bids=price, listing=listing, user=user)
            bid.save()
        except IntegrityError:
            return render(request, "auctions/bids.html", {
                "message": "Error al crear la oferta."
            })   
        return HttpResponseRedirect(reverse("bids", args=(id,))) 
    else:
        listing = Listings.objects.get(id=id)
        return render(request, "auctions/bids.html", {
            "listings": listing,
            "bid": Bids.objects.filter(listing=listing).order_by('-price_bids').all(),
            "comments": Comments.objects.filter(listing=listing)
            })

def comments(request, id):
    if request.method == "POST":
        comment = request.POST["comment"]
        listing = Listings.objects.get(pk=id)
        if User.is_authenticated:
            user = User.objects.get(username=request.user.username)
        else:
            user = User.objects.get(id=1)

        if comment == "":
            return render(request, "auctions/bids.html", {
                "message": "Error al crear el comentario."
            })

        # Attempt to create new user
        try:
            comment = Comments(comment=comment, listing=listing, user=user)
            comment.save()
        except IntegrityError:
            return render(request, "auctions/bids.html", {
                "message": "Error al crear el comentario."
            })
        return HttpResponseRedirect(reverse("bids", args=(id,)))
    else:
        return render(reverse("bids", args=(id,)), {
            "comments": Comments.objects.filter(listing=id)
        })
    
def exception (request):
    return render(request, "auctions/exception.html", {
        "message": "Error al poner la oferta, No debe ser menor a la oferta actual."
    })

def watchlist(request, id):
    if request.method == "POST":
        listing = Listings.objects.get(id=id)
        if User.is_authenticated:
            user = User.objects.get(username=request.user.username)
        else:
            return render(request, "auctions/exception.html",{
                "message": "Error al agregar a la lista de observación."
            }) 
        
        try:
            watchlist = Watchlist(user=user, listing=listing)
            watchlist.save()
        except IntegrityError:
            return render(request, "auctions/exception.html",{
                "message": "Error al agregar a la lista de observación."
            })
        return HttpResponseRedirect(reverse("bids", args=(id,)))
    else:
        return render(reverse("bids", args=(id,)), {
            "comments": Comments.objects.filter(listing=id)
        })
    
def viewWatchlist (request):
    if User.is_authenticated:
        user = User.objects.get(username=request.user.username)
    else:
        return render(request, "auctions/exception.html",{
            "message": "Error al ver la lista de observación."
        }) 

    return render(request, "auctions/watchlist.html", {
        "watchlist": Watchlist.objects.filter(user=user)
    })

def deleteWatchlist (request, id):
    if request.method == "POST":

        delete = Watchlist.objects.filter(listing=id)
        delete.delete()
                
        return render(request, "auctions/watchlist.html", {
            "watchlist": Watchlist.objects.filter(user=User.objects.get(username=request.user.username))
        })
    
    else:
        return render(request, "auctions/watchlist.html",{
            "watchlist": Watchlist.objects.filter(user=User.objects.get(username=request.user.username))
        })