var totalSvg = dimple.newSvg("#totalChartContainer", "100%", 450);
var sectorSvg = dimple.newSvg("#sectorChartContainer", "100%", 450);
var myChart;

//create small donor vs large donor chart
function create_chart(data) {
  var clicked = false;
  var maxAmount = d3.max(data, function(d) {
    return d.amount;
  })
  data_before = data.filter(function(d) {
    return d.before_after == "before";
  });
  var myChart = new dimple.chart(totalSvg, data_before);

  myChart.setBounds("22%", "0%", "40%", "80%");
  var x = myChart.addMeasureAxis("x", "amount");
  x.overrideMax = maxAmount;
  x.ticks=2; //only draw two tick lines to avoid stuff running into itself

  var y = myChart.addCategoryAxis("y", "type");
  y.fontSize = "12px";
    if (window.innerWidth <= 1400) { //minimum needed to avoid axis titles running off screen
	  myChart.addLegend("60%",1,"20%","20%"); //I am legend
	  y.fontSize="0px"; //make the labels invissible since they would be cut off anyway
  }
  y.title="";
  y.addOrderRule("amount", false);
  y.noFormats = true;
  
  x.fontSize = "12px";
  myChart.addSeries("type", dimple.plot.bar)
  
  
  myChart.draw();


  d3.select("#totalBtn").on("click", function() {
    if (clicked) {
      clicked = false;
      myChart.data = data.filter(function(d) {
        return d.before_after == "before";
      });
      myChart.draw(2000);
    } else {
      clicked = true;
      myChart.data = data.filter(function(d) {
        return d.before_after == "after";
      });
      myChart.draw(2000);
    }
  });
}

//create sector chart
function create_sector_chart(data) {
  var clicked = false;
  var maxAmount = d3.max(data, function(d) {
    return d.amount;
  })
  data_before = data.filter(function(d) {
    return d.before_after == "before";
  });
  var myChart = new dimple.chart(sectorSvg, data_before);

  myChart.setBounds("20%", "0%", "40%", "80%");
  var x = myChart.addMeasureAxis("x", "amount");
  x.overrideMax = maxAmount;
  var y = myChart.addCategoryAxis("y", "type");
  y.title = "";
  y.addOrderRule("amount", false);
  y.fontSize = "12px";
  x.fontSize = "12px";
  myChart.addSeries("type", dimple.plot.bar);
  myChart.draw();

  d3.select("#sectorBtn").on("click", function() {
    if (clicked) {
      clicked = false;
      myChart.data = data.filter(function(d) {
        return d.before_after == "before";
      });
      myChart.draw(2000);
    } else {
      clicked = true;
      myChart.data = data.filter(function(d) {
        return d.before_after == "after";
      });
      myChart.draw(2000);
    }
  });
}