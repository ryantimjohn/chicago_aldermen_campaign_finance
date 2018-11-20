var committee_url_list = [
  [1, 'Joe Moreno', 'https://illinoissunshine.org/committees/20809/'],
  [2, 'Brian Hopkins', 'https://illinoissunshine.org/committees/25653/'],
  [3, 'Pat Dowell', 'https://illinoissunshine.org/committees/16892/'],
  [4, 'Sophia King', 'https://illinoissunshine.org/committees/32052/'],
  [5, 'Leslie Hairston', 'https://illinoissunshine.org/committees/14216/'],
  [6, 'Roderick Sawyer', 'https://illinoissunshine.org/committees/22875/'],
  [7, 'Gregory Mitchell', 'https://illinoissunshine.org/committees/22816/'],
  [8, 'Michelle Harris', 'https://illinoissunshine.org/committees/20016/'],
  [9, 'Anthony Beale', 'https://illinoissunshine.org/committees/14556/'],
  [10, 'Susan Sadlowski Garza', 'https://illinoissunshine.org/committees/26168/'],
  [11, 'Patrick Thompson', 'https://illinoissunshine.org/committees/26197/'],
  [12, 'George Cardenas', 'https://illinoissunshine.org/committees/17290/'],
  [13, 'Marty Quinn', 'https://illinoissunshine.org/committees/23282/'],
  [14, 'Ed Burke', 'https://illinoissunshine.org/committees/4410/'],
  [15, 'Raymond Lopez', 'https://illinoissunshine.org/committees/23079/'],
  [16, 'Toni Faulkes', 'https://illinoissunshine.org/committees/20107/'],
  [17, 'David Moore', 'https://illinoissunshine.org/committees/23127/'],
  [18, 'Derrick Curtis', 'https://illinoissunshine.org/committees/26217/'],
  [19, "Matthew O'Shea", 'https://illinoissunshine.org/committees/22919/'],
  [20, 'Willie Cochran', 'https://illinoissunshine.org/committees/19880/'],
  [21, 'Howard Brookins', 'https://illinoissunshine.org/committees/17003/'],
  [22, 'Ricardo Munoz', 'https://illinoissunshine.org/committees/9487/'],
  [23, 'Michael Zalewski', 'https://illinoissunshine.org/committees/14156/'],
  [24, 'Michael Scott', 'https://illinoissunshine.org/committees/26204/'],
  [25, 'Daniel Solis', 'https://illinoissunshine.org/committees/12260/'],
  [26, 'Roberto Maldonado', 'https://illinoissunshine.org/committees/9533/'],
  [27, 'Walter Burnett', 'https://illinoissunshine.org/committees/10591/'],
  [28, 'Jason Ervin', 'https://illinoissunshine.org/committees/23112/'],
  [29, 'Chris Taliaferro', 'https://illinoissunshine.org/committees/25937/'],
  [30, 'Ariel Reboyas', 'https://illinoissunshine.org/committees/17163/'],
  [31, 'Milly Santiago', 'https://illinoissunshine.org/committees/26162/'],
  [32, 'Scott Waguespack', 'https://illinoissunshine.org/committees/19898/'],
  [33, 'Deborah Mell', 'https://illinoissunshine.org/committees/20627/'],
  [34, 'Carrie Austin', 'https://illinoissunshine.org/committees/11884/'],
  [35, 'Carlos Ramirez-Rosa', 'https://illinoissunshine.org/committees/26021/'],
  [36, 'Gilbert Villegas', 'https://illinoissunshine.org/committees/26023/'],
  [37, 'Emma Mitts', 'https://illinoissunshine.org/committees/15622/'],
  [38, 'Nicholas Sposato', 'https://illinoissunshine.org/committees/19830/'],
  [39, 'Margaret Laurino', 'https://illinoissunshine.org/committees/9808/'],
  [40, "Patrick O'Connor", 'https://illinoissunshine.org/committees/4353/'],
  [41, 'Anthony Napolitano', 'https://illinoissunshine.org/committees/26028/'],
  [42, 'Brendan Reilly', 'https://illinoissunshine.org/committees/19263/'],
  [43, 'Michelle Smith', 'https://illinoissunshine.org/committees/19682/'],
  [44, 'Thomas Tunney', 'https://illinoissunshine.org/committees/17150/'],
  [45, 'John Arena', 'https://illinoissunshine.org/committees/22749/'],
  [46, 'James Cappleman', 'https://illinoissunshine.org/committees/20952/'],
  [47, 'Ameya Pawar', 'https://illinoissunshine.org/committees/23607/'],
  [48, 'Harry Osterman', 'https://illinoissunshine.org/committees/22976/'],
  [49, 'Joseph Moore', 'https://illinoissunshine.org/committees/6380/'],
  [50, 'Debra Silverstein', 'https://illinoissunshine.org/committees/22982/']
];

function makeRequest(ward) {
  var requestURL = 'https://raw.githubusercontent.com/ryantimjohn/chicago_aldermen_campaign_finance/master/json/Ward' + ward + '.json';
  var request = new XMLHttpRequest();

  request.addEventListener("load", function() {
    loadMap(ward, this);
  });

  request.open('GET', requestURL);
  request.responseType = 'json';
  request.send();
  return request;
}

function loadMap(ward, request) {
  var myStyles = [{
    featureType: "poi",
    elementType: "labels",
    stylers: [{
      visibility: "off"
    }]
  }]
  var mapOptions = {
    center: new google.maps.LatLng(41.8781, -87.6298),
    zoom: 7,
    styles: myStyles,
  }

  var obj = request.response;
  var map = new google.maps.Map(document.getElementById("map"), mapOptions);
  var infowindow = new google.maps.InfoWindow({
    maxWidth: 400
  });
  var kmlURL = 'https://raw.githubusercontent.com/ryantimjohn/chicago_aldermen_campaign_finance/master/kml/Ward' + ward + '.kml';
  var wardLayer = new google.maps.KmlLayer({
    url: kmlURL,
    map: map
  });
  var markers = [];
  for (var line in obj) {
    var url = "";
    switch (obj[line]["donor_type"]) {
      case "Business":
        url = "https://rawgit.com/ryantimjohn/chicago_aldermen_campaign_finance/master/icons/b.svg";
        break;
      case "Individual":
        url = "https://rawgit.com/ryantimjohn/chicago_aldermen_campaign_finance/master/icons/i.svg";
        break;
      case "Political Group":
        url = "https://rawgit.com/ryantimjohn/chicago_aldermen_campaign_finance/master/icons/g.svg";
        break;
    }
    size = (0.23034542456 * Math.sqrt(obj[line]["amount"] - 150)) + 10
    var image = {
      url: url,
      // size: new google.maps.Size(132, 135),
      scaledSize: new google.maps.Size(size, size),
    }
    var content = '<div id="content">' +
      '<div id="siteNotice">' +
      '</div>' +
      '<h3 id="firstHeading" class="firstHeading"> <a href="https://www.google.com/search?q=' + obj[line]["first_name"] + " " + obj[line]["last_name"] + '" target="_blank">' + obj[line]["first_name"] + " " + obj[line]["last_name"] + '</a></h3>' +
      '<h4>$' + obj[line]["amount"] + ' donated since 2015 election</h4>' +
      '<div id="bodyContent">' +
      '<p><b>Donor type: </b>' + obj[line]["donor_type"] + "</p>" +
      '<p><b>Address: </b>' + obj[line]["full_address"] + "</p>" +
      '<p>Information obtained from Illinois Sunshine: <a href="' + committee_url_list[ward - 1][2] + '">' +
      committee_url_list[ward - 1][1] + '</a> ' +
      '</p>' +
      '</div>' +
      '</div>';
    if (obj[line]["coord"]) {
      var marker = new google.maps.Marker({
        position: new google.maps.LatLng(obj[line]["coord"][0], obj[line]["coord"][1]),
        title: obj[line]["first_name"] + " " + obj[line]["last_name"],
        map: map,
        icon: image,
      });
      google.maps.event.addListener(marker, 'click', (function(marker, content, infowindow) {
        return function() {
          infowindow.setContent(content);
          infowindow.open(map, marker);
        };
      })(marker, content, infowindow));
    }
    markers.push([marker, size]);
  }
  //add an event listener for zoom state
  google.maps.event.addListener(map, 'zoom_changed', function() {

    var pixelSizeAtZoom0 = .00008; //the size of the icon at zoom level 0
    var maxPixelSize = 350; //restricts the maximum size of the icon, otherwise the browser will choke at higher zoom levels trying to scale an image to millions of pixels

    var zoom = map.getZoom();
    var relativePixelSize = Math.round(pixelSizeAtZoom0 * Math.pow(2, zoom)); // use 2 to the power of current zoom to calculate relative pixel size.  Base of exponent is 2 because relative size should double every time you zoom in

    if (relativePixelSize > maxPixelSize) //restrict the maximum size of the icon
      relativePixelSize = maxPixelSize;

    //change the size of the icon
    for (var i = 0, len = markers.length; i < len; i++) {
      try{
        markers[i][0].setIcon(
          new google.maps.MarkerImage(
            markers[i][0].getIcon().url, //marker's same icon graphic
            null, //size
            null, //origin
            null, //anchor
            new google.maps.Size(markers[i][1] * relativePixelSize < 8 ? 8 : markers[i][1] * relativePixelSize, markers[i][1] * relativePixelSize < 8 ? 8 : markers[i][1] * relativePixelSize) //changes the scale
        )
      )
    }
    catch(TypeError){}
    }
  });
}