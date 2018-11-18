
        var totalSvg = dimple.newSvg("#totalChartContainer", 650, 400);
  var sectorSvg = dimple.newSvg("#sectorChartContainer", 650, 400);

      function create_chart(data){
        var clicked = false;
        var maxAmount = d3.max(data, function(d){return d.amount;})
        data_before = data.filter(function(d) { return d.before_after == "before";});
        var myChart = new dimple.chart(totalSvg, data_before);
      myChart.setBounds("10%","0%", "20%","80%");
        var x = myChart.addMeasureAxis("x", "amount");
        x.overrideMax = maxAmount;
        var y = myChart.addCategoryAxis("y", "type");
        y.addOrderRule("amount", false);
        myChart.addSeries("type", dimple.plot.bar);
        myChart.draw();

        d3.select("#totalBtn").on("click", function (){
                if (clicked){
                  clicked = false;
                  myChart.data = data.filter(function(d) { return d.before_after == "before";});
                  myChart.draw(2000);
                }
                else {
                  clicked = true;
                  myChart.data = data.filter(function(d) { return d.before_after == "after";});
                  myChart.draw(2000);
                }

              });
      }
	  
	  
	  
	    function create_sector_chart(data){
        var clicked = false;
        var maxAmount = d3.max(data, function(d){return d.amount;})
        data_before = data.filter(function(d) { return d.before_after == "before";});
        var myChart = new dimple.chart(sectorSvg, data_before);
       myChart.setBounds("10%","0%", "20%","80%");
        var x = myChart.addMeasureAxis("x", "amount");
        x.overrideMax = maxAmount;
        var y = myChart.addCategoryAxis("y", "type");
        y.addOrderRule("amount", false);
        myChart.addSeries("type", dimple.plot.bar);
        myChart.draw();

        d3.select("#sectorBtn").on("click", function (){
                if (clicked){
                  clicked = false;
                  myChart.data = data.filter(function(d) { return d.before_after == "before";});
                  myChart.draw(2000);
                }
                else {
                  clicked = true;
                  myChart.data = data.filter(function(d) { return d.before_after == "after";});
                  myChart.draw(2000);
                }

              });
      }
