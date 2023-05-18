from django.shortcuts import render
import pandas as pd
from sklearn.linear_model import LinearRegression
import openai
import seaborn as sns
from .models import House
from django.utils.safestring import mark_safe
import folium




def hello_world(request):




    queryset = House.objects.all()

    df = pd.DataFrame.from_records(queryset.values())



    df = df [['Price','Area','Room','Lon','Lat']]
    df['Price'] = df['Price'].astype(float)


    df['Area'] = df['Area'].astype(float)



    describe = df.describe()
    table1 = describe.to_html(float_format='{:,.2f}'.format, classes='table table-striped')
    table1 = mark_safe(table1)

    correlation_matrix = df.corr(method='pearson')
    table2 = correlation_matrix.to_html(float_format='{:,.2f}'.format, classes='table table-striped')
    table2 = mark_safe(table2)


    print_data = ""

    m = folium.Map(location=[52.370216, 4.895168], zoom_start=13)
    popup1 = folium.LatLngPopup()
    m.add_child(popup1)

    if request.method == 'POST':
        area = float(request.POST.get('area'))
        room = float(request.POST.get('room'))
        lat = m.location[0]
        lon = m.location[1]
        
        x = df[['Area', 'Room', 'Lon', 'Lat']]
        y = df[['Price']]
        
        model = LinearRegression()
        model.fit(x, y)

        data = []
        data.append([area, room, float(lon), float(lat)])
        value = model.predict(data)

        print_data = "--------------> Predicted Price is : " + str(value)

        print("Surface de la maison: " + str(area))
        print("Nombre de chanbre: " + str(room))
        print("Latitude of Popup: ", str(lat))
        print("Longitude of Popup: ", str(lon))
        print(print_data)


    context = {
        'describe' : table1,
        'correlation_matrix': table2,
        'm':  m._repr_html_(),
        'print_data': print_data,
        }  

    return render(request, 'hello_world.html', context)
