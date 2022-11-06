from django.shortcuts import render

# generic base view
from django.views.generic import TemplateView

# folium
import folium
from folium import plugins

# gee
import ee

ee.Initialize()


# frontend
# home
class home(TemplateView):
    template_name = 'index.html'

    # Define a method for displaying Earth Engine image tiles on a foilum map.
    def get_context_data(self, **kwargs):

        figure = folium.Figure()

        # create Foilum Object
        m = folium.Map(
            location=[28.5973518, 83.54495724],
            zoom_start=8,
        )

        # add map to figure
        m.add_to(figure)

        # select the Dataset Here's used the MODIS data
        dataset = (ee.ImageCollection('MODIS/006/MOD13Q1')
                   .filter(ee.Filter.date('2019-07-01', '2019-11-30'))
                   .first())
        modisndvi = dataset.select('NDVI')
        visParams = {'min': 0, 'max': 3000, 'palette': [
            '225ea8', '41b6c4', 'a1dab4', '034B48']}

        # Styling
        vis_paramsNDVI = {
            'min': 0,
            'max': 9000,
            'palette': ['FE8374', 'C0E5DE', '3A837C', '034B48', ]}

        # add the map to the folium map
        map_id_dict = ee.Image(modisndvi).getMapId(vis_paramsNDVI)

        # Gee raster data to TileLayer
        folium.raster_layers.TileLayer(
            tiles=map_id_dict['tile_fetcher'].url_format,
            attr='Google Earth Engine',
            name='NDVI',
            overlay=True,
            control=True
        ).add_to(m)

        # add Layer Control
        m.add_child(folium.LayerControl())

        # figure
        figure.render()

        # return map
        return {"map": figure}
