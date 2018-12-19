var totalSvg = dimple.newSvg("#totalChartContainer", "100%", 450);
var sectorSvg = dimple.newSvg("#sectorChartContainer", "100%", 450);
var totalChart="";
var sectorChart="";
var clicked=false;

function setPageText(isClicked) { // Show correct explanations of the graphhs isClicked should be true if we are displaying FEO projections.
	explanation=document.getElementById("graphExplanationText");
	toggleButton=document.getElementById("toggler");
	if (isClicked) {
	explanation.innerHTML="This is our projection of where the money would come from if this alderman fundraised under the <a href=\"https://reclaimfairelections.org/about\">Fair Elections Ordinance</a> since the last election";
	toggler.innerText="Show actual fundraising totals";
	}
	else {
		explanation.innerHTML="This is where the alderman got their money since the last aldermanic election in 2015.";
		toggler.innerText="Show with Fair Elections Ordinance";
	}
}

function toggleFEO() { //toggle  graphs to show with FEO or without
 document.getElementById("sectorToggle").click(); // Clicking the button is linked to toggling the total chart. However the sector chart has to be linked to a second hidden button so this clicks that.
}
//create small donor vs large donor chart
function create_chart(data,isClicked) {
  var maxAmount = d3.max(data, function(d) {
    return d.amount;
  })
  data_before = data.filter(function(d) {
    return d.before_after == "before";
  });
  totalChart = new dimple.chart(totalSvg, data_before);

  totalChart.setBounds("22%", "0%", "40%", "80%");
  var x = totalChart.addMeasureAxis("x", "amount");
  x.overrideMax = maxAmount;
  x.ticks=2; //only draw two tick lines to avoid stuff running into itself

  var y = totalChart.addCategoryAxis("y", "type");
  y.fontSize = "12px";
    if (window.innerWidth <= 1400) { //minimum needed to avoid axis titles running off screen
	  totalChart.addLegend("43%",1,"50px","100%"); //I am legend
	  y.fontSize="0px"; //make the labels invissible since they would be cut off anyway
	  totalChart.setBounds("10%", "0%", "40%", "80%"); //there are no axis labels anymore so we can scoot the chart farther to the left
  }
  y.title="";
  y.addOrderRule("amount", false);
  y.noFormats = true;
  
  x.fontSize = "12px";
  totalChart.addSeries("type", dimple.plot.bar)
  
  
  totalChart.draw();
  

  d3.select("#toggler").on("click", function() {
    if (clicked) {
      clicked = false;
      totalChart.data = data.filter(function(d) {
		  setPageText(false);
        return d.before_after == "before";
		
      });
	  
	  totalChart.draw(2000);
 
    } else {
      clicked = true;
      totalChart.data = data.filter(function(d) {
		  setPageText(true);
        return d.before_after == "after";
		 
      });
	  
      totalChart.draw(2000);
	  
	  
    }
  });
  
    //change the explanation text
 
  
  
}

//create sector chart
function create_sector_chart(data) {
	unfilteredSector=data;
  var clicked = false;
  var maxAmount = d3.max(data, function(d) {
    return d.amount;
  })
  data_before = data.filter(function(d) {
    return d.before_after == "before";
  });
  var sectorChart = new dimple.chart(sectorSvg, data_before);

  sectorChart.setBounds("20%", "0%", "40%", "80%");
  var x = sectorChart.addMeasureAxis("x", "amount");
  x.overrideMax = maxAmount;
  x.ticks=2; //limit to 2 ticks to avoid them running into each other
  var y = sectorChart.addCategoryAxis("y", "type");
  y.title = "";
  y.addOrderRule("amount", false);
  y.fontSize = "12px";
  if (window.innerWidth <= 1400) { //minimum needed to avoid axis titles running off screen
	  sectorChart.addLegend("43%",1,"50px","100%"); //I am legend
	  y.fontSize="0px"; //make the labels invissible since they would be cut off anyway
	  sectorlChart.setBounds("10%", "0%", "40%", "80%"); //there are no axis labels anymore so we can scoot the chart farther to the left
  }
  x.fontSize = "12px";
  sectorChart.addSeries("type", dimple.plot.bar);
  sectorChart.draw();

  d3.select("#sectorToggle").on("click", function() {
    if (clicked) {
      clicked = false;
      sectorChart.data = data.filter(function(d) {
        return d.before_after == "before";
      });
      sectorChart.draw(2000);
    } else {
      clicked = true;
      sectorChart.data = data.filter(function(d) {
        return d.before_after == "after";
      });
      sectorChart.draw(2000);
    }
  });
}