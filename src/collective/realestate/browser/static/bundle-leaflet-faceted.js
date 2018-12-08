/* Patterns bundle configuration.
 */
require([
  'jquery',
  'pat-registry',
  'pat-leaflet-faceted'
], function($, registry) {
  'use strict';

  // initialize only if we are in top frame
  if (window.parent === window) {
    $(document).ready(function() {
      $('body').addClass('bundle-leaflet-faceted');
      if (!registry.initialized) {
        registry.init();
      }
      jQuery(Faceted.Events).bind(
        Faceted.Events.AJAX_QUERY_SUCCESS,
        update_map
      );

      function update_map() {
        // console.log('change');
        if ($('.geolocation_wrapper').length && $('.map').length) {
          var geolocation_wrapper = $('.geolocation_wrapper')[0];
          var divmap = $('.map')[0];
          if (geolocation_wrapper.dataset.hasOwnProperty('json') &&
            divmap.dataset.hasOwnProperty('geojson')) {
            divmap.dataset.geojson = geolocation_wrapper.dataset.json;

            // registry.init();
            // map.update();

            geojson = JSON.parse(divmap.dataset.geojson);
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
  }
});
