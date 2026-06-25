import folium
from folium.plugins import GroupedLayerControl
from folium.plugins import Draw
from folium.plugins import MousePosition
from folium.plugins import MiniMap

m = folium.Map(location=(38.0032, 23.6755), zoom_start=17, control_scale=True)
Draw(export=False, position='bottomleft').add_to(m)
folium.plugins.Fullscreen(
    position="topright", title="Fullscreen Mode",
    title_cancel="Exit Fullscreen Mode", force_separate_button=True).add_to(m)
formatter = "function(num) {return L.Util.formatNum(num, 4) + '&deg;';};"
folium.plugins.Geocoder().add_to(m)
MousePosition( prefix="(Lat, Lon)", separator=", ",
    lat_formatter=formatter, lng_formatter=formatter).add_to(m)
MiniMap().add_to(m)
base01 = folium.FeatureGroup(name='ESRI World Imager')
folium.TileLayer('Esri.WorldImagery').add_to(base01)
base02 = folium.FeatureGroup(name='CartoDB Positron')
folium.TileLayer('CartoDB.Positron').add_to(base02)
m.add_child(base01)
m.add_child(base02)
GroupedLayerControl(groups={'Base Maps':[base01,base02]},collapsed=False).add_to(m)
my_sample_point = folium.FeatureGroup(name="My sample point", show=True).add_to(m)
folium.Marker(location=(37.98, 23.73)).add_to(my_sample_point)
GroupedLayerControl(groups={'Sample data':[my_sample_point]},collapsed=True).add_to(m)
m.save("DIGIHAZ_WebGIS_Topic_04_Example_Folium_export_VK.html")