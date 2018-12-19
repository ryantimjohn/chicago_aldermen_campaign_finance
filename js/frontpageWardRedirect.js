function getWard(wards, point) {
  var ward = null;
  for (var i = 0; i < wards.features.length; i++) {
    var wardToCheck = wards.features[i];
    var collection = turf.featureCollection([point]);
    var points = turf.pointsWithinPolygon(turf.point(point), wardToCheck);
    
    if (points.features.length) {
      ward = wardToCheck.properties.ward;
      break;
    }
  }

  return ward;
}

$(document).ready(function() {

  var wards;
  $.ajax({
      url: 'https://data.cityofchicago.org/api/geospatial/sp34-6z76?method=export&format=GeoJSON'
    })
    .then(function(response) {
      wards = response;
      console.log(wards);
    });

  var form = $('#search-by-address');
  var cityscapeKey = "WwpHU6SLdp";

  if (form.length) { // I.e if we're on the front page
    // Set handler for submitting the form when someone hits the enter key
    form.keypress(function(event){
      if(event.key === 'Enter'){
        form.submit();
      }
    });

    form.submit(function(event) {
      event.preventDefault();

      var address = encodeURIComponent(form.find('#address-field').val());
      var url = 'https://www.chicagocityscape.com/api/index.php?address=' + address + '&city=Chicago&state=IL&key=' + cityscapeKey;
      
      $.ajax({
          url: url
        })
        .then(function(response) {
          if (response.properties.request.address === '[no address]') {
            $('#ward-search-no-results').removeClass('hidden');
          } else {
            var point = response.geometry.coordinates;
            var ward = getWard(wards, point);

            window.location.href = "https://reclaimfairelections.org/ward/" + ward;
          }
        });
    });
  }
});