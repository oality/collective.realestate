/* Patterns bundle configuration.
 */
var baseLayers,
  bounds,
  geojson,
  geosearch,
  marker_cluster,
  marker_layer,
  map,
  main_marker;
var map_layers = [{
    'title': 'Map',
    'id': 'OpenStreetMap.Mapnik'
  },
  {
    'title': 'Satellite',
    'id': 'Esri.WorldImagery'
  },
  {
    'title': 'Topographic',
    'id': 'OpenTopoMap'
  },
  {
    'title': 'Toner',
    'id': 'Stamen.Toner'
  }
];

var image_path = 'src/bower_components/Leaflet.awesome-markers/dist/images';

$(document).ready(function() {

  jQuery(Faceted.Events).bind(
    Faceted.Events.INITIALIZE,
    init_map
  );

  jQuery(Faceted.Events).bind(
    Faceted.Events.AJAX_QUERY_SUCCESS,
    update_map
  );

  function init_map() {
    if ($('#map').length && $('#geojson').length) {
      map = L.map("map", {
        fullscreenControl: true,
        zoomControl: true,
        // Leaflet.Sleep options
        sleep: true,
        sleepNote: false,
        hoverToWake: false,
        sleepOpacity: 1
      });
      L.Icon.Default.imagePath = image_path;
      var locatecontrol = L.control.locate({
        icon: 'fa fa-crosshairs'
      }).addTo(map);

      baseLayers = {};
      for (var cnt = 0; cnt < map_layers.length; cnt++) {
        // build layers object with tileLayer instances
        baseLayers[map_layers[cnt].title] = L.tileLayer.provider(map_layers[cnt].id);
      }
      L.control.layers(baseLayers).addTo(map);

      L.tileLayer.provider('OpenStreetMap.Mapnik').addTo(map); // default map


      divgeojson = $('#map')[0];
      geojson = JSON.parse(divgeojson.dataset.geojson);
      marker_cluster = new L.MarkerClusterGroup();
      var red_marker = L.AwesomeMarkers.icon({
        markerColor: 'red',
        prefix: 'fa',
        icon: 'circle'
      });
      marker_layer = L.geoJson(geojson, {
        pointToLayer: function(feature, latlng) {
          var green_marker = L.AwesomeMarkers.icon({
            markerColor: 'green',
            prefix: 'fa',
            icon: 'circle'
          });
          var blue_marker = L.AwesomeMarkers.icon({
            markerColor: 'blue',
            prefix: 'fa',
            icon: 'circle'
          });
          var marker_color = green_marker;
          if (!main_marker || feature.properties.main) {
            marker_color = red_marker;
          }
          var marker = L.marker(latlng, {
            icon: marker_color,
            draggable: feature.properties.editable
          });
          if (!main_marker || feature.properties.main) {
            // Set main marker. This is the one, which is used
            // for setting the search result marker.
            marker.icon = blue_marker;
            main_marker = marker;
          }
          return marker;
        },
        onEachFeature: function(feature, marker) {
          var popup = feature.properties.popup;
          marker.bindPopup(popup);
        }
      });
      marker_cluster.addLayer(marker_layer);
      map.addLayer(marker_cluster);
      bounds = marker_cluster.getBounds();
      map.fitBounds(bounds);
      provider = new L.GeoSearch.Provider.OpenStreetMap();
      geosearch = new L.Control.GeoSearch({
          showMarker: typeof main_marker === 'undefined',
          draggable: true,
          provider: provider
      });
      geosearch.addTo(map);

      map.on('geosearch_showlocation', function(e) {
        if (main_marker) {
          var latlng = {lat: e.Location.Y, lng: e.Location.X};
          // update, otherwise screen is blank.
          marker_cluster.removeLayer(main_marker);
          main_marker.setLatLng(latlng).update();
          marker_cluster.addLayer(main_marker);
          // fit to window
          map.fitBounds([latlng]);
        }
      });
    }
  }

  function update_map() {
    // console.log('change');
    var divmap = $('#map')[0];
    if ($('#geojson').length == 0) {
        $('#map').hide();
        return
      } else {
        $('#map').show();
    }
    if ($('#geojson').length && $('#map').length) {
      if (typeof map == 'undefined') {
        init_map();
      }
      // var container = L.DomUtil.get('map');
      // if(container != null){
      //   container._leaflet_id = null;
      //   map.remove();
      //   // if (container._leaflet_id == null){
      //   // }
      // }
      var geojson_wrapper = $('#geojson')[0];
      if (geojson_wrapper.dataset.hasOwnProperty('geojson') &&
        divmap.dataset.hasOwnProperty('geojson')) {
        divmap.dataset.geojson = geojson_wrapper.dataset.geojson;

        geojson = JSON.parse(divmap.dataset.geojson);
        L.Icon.Default.imagePath = image_path;
        marker_cluster.removeLayer(marker_layer);
        marker_layer = L.geoJson(geojson, {
          pointToLayer: function(feature, latlng) {
            var red_marker = L.AwesomeMarkers.icon({
              markerColor: 'red',
              prefix: 'fa',
              icon: 'circle'
            });
            var green_marker = L.AwesomeMarkers.icon({
              markerColor: 'green',
              prefix: 'fa',
              icon: 'circle'
            });
            var blue_marker = L.AwesomeMarkers.icon({
              markerColor: 'blue',
              prefix: 'fa',
              icon: 'circle'
            });
            var marker_color = green_marker;
            if (!main_marker || feature.properties.main) {
              marker_color = red_marker;
            }
            var marker = L.marker(latlng, {
              icon: marker_color,
              draggable: feature.properties.editable
            });
            if (!main_marker || feature.properties.main) {
              // Set main marker. This is the one, which is used
              // for setting the search result marker.
              marker.icon = blue_marker;
              main_marker = marker;
            }
            return marker;
          },
          onEachFeature: function(feature, marker) {
            var popup = feature.properties.popup;
            marker.bindPopup(popup);
          }
        });
        marker_cluster.addLayer(marker_layer);
      }
    }
  }
});
