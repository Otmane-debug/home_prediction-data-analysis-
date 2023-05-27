from django.shortcuts import render, redirect
import pandas as pd
from sklearn.linear_model import LinearRegression
import seaborn as sns
from .models import House
from django.utils.safestring import mark_safe
import geopy
from geopy.geocoders import Nominatim
import plotly.express as px
import plotly.io as pio
import openai
from .forms import CreateUserFrom
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def register(request):
    form = CreateUserFrom()

    if request.method =="POST":
        form = CreateUserFrom(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    context = {'form': form}
    return render(request, "register.html", context)

def login_view(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username Or Password is incorrect')

    context = {}
    return render(request, 'login.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')


def index(request):
    return render(request, "index.html")

def contact(request):
    return render(request, "contact.html")

@login_required(login_url='login')
def analyse(request):

    queryset = House.objects.all()

    df = pd.DataFrame.from_records(queryset.values())
    
    df_price_area = df[['Price', 'Area']]
    fig_prix_area = px.scatter(df_price_area, x="Price", y="Area")
    graph_prix_area = pio.to_html(fig_prix_area)

    df_price_room = df[['Price', 'Room']]
    fig_prix_room = px.scatter(df_price_room, x="Price", y="Room")
    graph_prix_room = pio.to_html(fig_prix_room)

    df = df [['Price','Area','Room','Lon','Lat']]
    df['Price'] = df['Price'].astype(float)

    describe = df.describe()
    table1 = describe.to_html(float_format='{:,.2f}'.format, classes='table table-striped')
    table1 = mark_safe(table1)

    correlation_matrix = df.corr(method='pearson')
    table2 = correlation_matrix.to_html(float_format='{:,.2f}'.format, classes='table table-striped')
    table2 = mark_safe(table2)

    context = {
        'describe' : table1,
        'correlation_matrix': table2,
        'graph_prix_area': graph_prix_area,
        'graph_prix_room': graph_prix_room,
        } 
    
    return render(request, 'analyse.html', context)

@login_required(login_url='login')
def prices(request):
    queryset = House.objects.all()

    df = pd.DataFrame.from_records(queryset.values())

    context = {}

    if request.method == 'POST':
        area = float(request.POST.get('area'))
        room = float(request.POST.get('room'))
        address = request.POST.get('address')

        # Create a geocoder object
        geolocator = Nominatim(user_agent="code.txt")

        # Geocode the address
        location = geolocator.geocode(address)

        # Get the lat/lng coordinates of the location
        lat = round(float(location.latitude), 6)
        lon = round(float(location.longitude), 6)
        
        x = df[['Area', 'Room', 'Lon', 'Lat']]
        y = df[['Price']]
        
        model = LinearRegression()
        model.fit(x, y)

        data = []
        data.append([area, room, lon, lat])
        value = model.predict(data)

        value = round(value[0][0], 2)


        context = {
        'data': value,
        }  




    return render(request, 'prices.html', context)