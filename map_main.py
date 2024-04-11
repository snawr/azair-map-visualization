import folium
import webbrowser

def createMap(coordinates):
    global main_map
    main_map = folium.Map(location=coordinates, zoom_start=3.5)
    
    

def createPin(coordinates, price, city, color='blue'):
    global main_map
    folium.Marker(location=coordinates, popup=city, icon=folium.Icon(color=color)).add_to(main_map)
    folium.Marker(location=coordinates, 
                  popup=city, 
                  icon=folium.DivIcon(
                    html=f"""<div style="font-family: 'Arial', sans-serif; color: black; font-size: 20px; font-weight: bold;">{price}</div>""")
                ).add_to(main_map)


def displayMap():
    global main_map
    main_map.save("map.html")
    webbrowser.open("map.html")
