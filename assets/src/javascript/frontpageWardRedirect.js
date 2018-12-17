var wards;

function getWard(wards, point) {
  var ward = null;
  for (var i = 0; i < wards.features.length; i++) {
    var wardToCheck = wards.features[i];
    var collection = turf.featureCollection([point]);
    var points = turf.pointsWithinPolygon(turf.point(point), wardToCheck);
    console.log(points);
    if (points.features.length) {
      ward = wardToCheck.properties.ward;
      break;
    }
  }

  return ward;
}

if($("#search-button").length > 0){
    $(document).ready(function() {
        $.ajax({
            url: 'https://data.cityofchicago.org/api/geospatial/sp34-6z76?method=export&format=GeoJSON'
        })
            .then(function(response) {
                console.log(response);
                wards = response;
            });

    });

    $("#search-button").on('click', function(){
        var address = encodeURIComponent($("#streetAddress").val());
        var loading =  $("#search-loading");
        var alert = $(".callout.alert");
        $("#search-loading").css('visibility', 'visible');
        alert.css('display', 'none');

        var cityscapeKey = "WwpHU6SLdp";
        var url = 'https://www.chicagocityscape.com/api/index.php?address=' + address + '&city=Chicago&state=IL&key=' + cityscapeKey;

        $.ajax({
            url: url
        })
            .then(function(response) {
                if (response.properties.request.address === '[no address]') {
                    display_error();
                } else {
                    var point = response.geometry.coordinates;
                    var ward = getWard(wards, point);
                    if(ward === null){
                        display_error();
                    }else{
                        alert.css('display', 'block');
                        window.location.href = "../ward/" + ward;
                    }
                }
            }).fail(function(error){
            display_error();
        }).catch(function(error){
            display_error();
        });

    });

}



function display_error(){
    var loading =  $("#search-loading");
    var alert = $(".callout.alert");
    loading.css('visibility', 'hidden');
    alert.fadeIn();
}

