var committee_url_list = [[1, 'Joe Moreno', 'https://illinoissunshine.org/committees/20809/'],
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
 [50, 'Debra Silverstein', 'https://illinoissunshine.org/committees/22982/']];

var icons = {
  i: 'data:image/svg+xml;utf-8, \
          <svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"\
	 viewBox="0 0 132 135" style="enable-background:new 0 0 132 135;" xml:space="preserve">\
<style type="text/css">\
	.st0{fill:rgb(108,1,13);}\
	.st1{fill:rgb(255,255,255);}\
</style>\
<title>i</title>\
<g id="Ellipse_2">\
	<ellipse class="st0" cx="66" cy="67.5" rx="66" ry="67.5"/>\
</g>\
<g>\
	<path class="st1" d="M66,66.7c8.4,0,15.3-8.3,15.3-18.6c0-10.2-2.2-18.6-15.3-18.6s-15.3,8.3-15.3,18.6\
		C50.7,58.4,57.6,66.7,66,66.7z"/>\
	<path class="st1" d="M37.1,95C37.1,94.4,37.1,94.8,37.1,95L37.1,95z"/>\
	<path class="st1" d="M94.9,95.5C94.9,95.3,94.9,94.3,94.9,95.5L94.9,95.5z"/>\
	<path class="st1" d="M94.8,94.3c-0.3-17.9-2.6-22.9-20.5-26.2c0,0-2.5,3.2-8.4,3.2c-5.9,0-8.4-3.2-8.4-3.2\
		C40,71.3,37.5,76.3,37.2,93.7c0,1.4,0,1.5,0,1.3c0,0.3,0,0.9,0,1.9c0,0,4.2,8.6,28.9,8.6c24.6,0,28.9-8.6,28.9-8.6\
		c0-0.6,0-1.1,0-1.4C94.8,95.6,94.8,95.4,94.8,94.3z"/>\
</g>\
</svg>',
  b: 'data:image/svg+xml;utf-8, \
  <svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"\
  	 viewBox="0 0 132 135" style="enable-background:new 0 0 132 135;" xml:space="preserve">\
  <style type="text/css">\
  	.st0{fill:rgb(108,1,13);}\
  	.st1{fill:rgb(255,255,255);}\
  </style>\
  <title>i</title>\
  <g id="Ellipse_2">\
  	<ellipse class="st0" cx="66" cy="67.5" rx="66" ry="67.5"/>\
  </g>\
  <g>\
  	<path class="st1" d="M66,66.7c8.4,0,15.3-8.3,15.3-18.6c0-10.2-2.2-18.6-15.3-18.6s-15.3,8.3-15.3,18.6\
  		C50.7,58.4,57.6,66.7,66,66.7z"/>\
  	<path class="st1" d="M37.1,95C37.1,94.4,37.1,94.8,37.1,95L37.1,95z"/>\
  	<path class="st1" d="M94.9,95.5C94.9,95.3,94.9,94.3,94.9,95.5L94.9,95.5z"/>\
  	<path class="st1" d="M94.8,94.3c-0.3-17.9-2.6-22.9-20.5-26.2c0,0-2.5,3.2-8.4,3.2c-5.9,0-8.4-3.2-8.4-3.2\
  		C40,71.3,37.5,76.3,37.2,93.7c0,1.4,0,1.5,0,1.3c0,0.3,0,0.9,0,1.9c0,0,4.2,8.6,28.9,8.6c24.6,0,28.9-8.6,28.9-8.6\
  		c0-0.6,0-1.1,0-1.4C94.8,95.6,94.8,95.4,94.8,94.3z"/>\
  </g>\
  </svg>',
  g: 'data:image/svg+xml;utf-8, \
  <svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"\
  	 viewBox="0 0 132 135" style="enable-background:new 0 0 132 135;" xml:space="preserve">\
  <style type="text/css">\
  	.st0{fill:#02865C;}\
  	.st1{fill:#FFFFFF;}\
  </style>\
  <title>g</title>\
  <g id="Ellipse_2">\
  	<ellipse class="st0" cx="66" cy="67.5" rx="66" ry="67.5"/>\
  </g>\
  <g>\
  	<g>\
  		<g>\
  			<path class="st1" d="M92.7,89.1c0.9-1.2,1.5-2.8,1.5-4.4c0-4.1-3.4-7.5-7.5-7.5s-7.5,3.4-7.5,7.5c0,1.7,0.5,3.2,1.5,4.5\
  				c-1.7,0.8-3.2,2-4.3,3.5c-1.1-1.5-2.6-2.8-4.4-3.5c0.9-1.2,1.5-2.8,1.5-4.4c0-4.1-3.4-7.5-7.5-7.5c-4.1,0-7.5,3.4-7.5,7.5\
  				c0,1.7,0.5,3.2,1.5,4.5c-1.7,0.8-3.2,2-4.3,3.5c-1.1-1.5-2.6-2.8-4.4-3.5c0.9-1.2,1.5-2.8,1.5-4.4c0-4.1-3.4-7.5-7.5-7.5\
  				s-7.5,3.4-7.5,7.5c0,1.7,0.5,3.2,1.5,4.5c-3.7,1.6-6.3,5.3-6.3,9.6v1.9h66v-1.9C99,94.4,96.4,90.7,92.7,89.1z"/>\
  		</g>\
  	</g>\
  	<g>\
  		<g>\
  			<polygon class="st1" points="79.3,56.8 71,54.2 66,47.1 60.9,54.2 52.7,56.8 57.8,63.7 57.8,72.4 66,69.7 74.2,72.4 74.1,63.7 \
  							"/>\
  		</g>\
  	</g>\
  	<g>\
  		<g>\
  			<rect x="64.1" y="34.4" class="st1" width="3.9" height="5.6"/>\
  		</g>\
  	</g>\
  	<g>\
  		<g>\
  			<rect x="87.5" y="57.8" class="st1" width="5.6" height="3.9"/>\
  		</g>\
  	</g>\
  	<g>\
  		<g>\
  			<rect x="38.9" y="57.8" class="st1" width="5.6" height="3.9"/>\
  		</g>\
  	</g>\
  	<g>\
  		<g>\
  			\
  				<rect x="81.1" y="41.6" transform="matrix(0.7071 -0.7071 0.7071 0.7071 -6.1043 72.4296)" class="st1" width="6.5" height="3.9"/>\
  		</g>\
  	</g>\
  	<g>\
  		<g>\
  			\
  				<rect x="45.7" y="40.3" transform="matrix(0.7071 -0.7071 0.7071 0.7071 -16.8555 46.4214)" class="st1" width="3.9" height="6.5"/>\
  		</g>\
  	</g>\
  </g>\
  </svg>'
}

function makeRequest(ward){
  var requestURL = 'https://raw.githubusercontent.com/ryantimjohn/chicago_aldermen_campaign_finance/master/json/Ward' + ward + '.json';
  var request = new XMLHttpRequest();
  request.open('GET', requestURL);
  request.responseType = 'json';
  request.send();
  return request;
}

function loadMap(ward, request) {

      var mapOptions = {
        center: new google.maps.LatLng(41.8781, -87.6298),
        zoom: 7
      }

      var obj = request.response;
      var map = new google.maps.Map(document.getElementById("map"), mapOptions);
      var infowindow = new google.maps.InfoWindow({maxWidth : 400});

      var kmlURL = 'https://raw.githubusercontent.com/ryantimjohn/chicago_aldermen_campaign_finance/master/kml/Ward' + ward + '.kml';
      var wardLayer = new google.maps.KmlLayer({
          url: kmlURL,
          map: map
        });

      for (var line in obj) {

        var url = "";

        switch (obj[line]["donor_type"]) {
          case "Business":
            url = icons.b;
            break;
          case "Individual":
            url = icons.i;
            break;
          case "Political Group":
            url = icons.g;
            break;
        }

        size = (0.23034542456 * Math.sqrt(obj[line]["amount"] - 150)) + 10

        var image = {
          url: url,
          origin: new google.maps.Point(0, 0),
          anchor: new google.maps.Point(0, 0),
          scaledSize: new google.maps.Size(size, size),
        }

        var content = '<div id="content">' +
          '<div id="siteNotice">' +
          '</div>' +
          '<h1 id="firstHeading" class="firstHeading">' + obj[line]["first_name"] + " " + obj[line]["last_name"] + '</h1>' +
          '<h2>$' + obj[line]["amount"] + ' donated since 2015 election</h2>' +
          '<div id="bodyContent">' +
          '<p><b>Donor type: </b>' + obj[line]["donor_type"] + "</p>" +
          '<p><b>Address: </b>' + obj[line]["full_address"] + "</p>" +
          '<p>Information obtained from Illinois Sunshine: <a href="' + committee_url_list[ward-1][2] + '">' +
          committee_url_list[ward-1][1] + '</a> ' +
          '(last visited August 30, 2018).</p>' +
          '</div>' +
          '</div>';

        if (obj[line]["coord"]) {
          var marker = new google.maps.Marker({
            position: new google.maps.LatLng(obj[line]["coord"][0], obj[line]["coord"][1]),
            icon: image,
            title: obj[line]["first_name"] + " " + obj[line]["last_name"],
            map: map,
          });
          google.maps.event.addListener(marker, 'click', (function(marker, content, infowindow) {
            return function() {
              infowindow.setContent(content);
              infowindow.open(map, marker);
            };
          })(marker, content, infowindow));
        }
      }
    }