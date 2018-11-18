 d3.json("https://raw.githubusercontent.com/ryantimjohn/chicago_aldermen_campaign_finance/master/web_json/Ward1_totals.json", function(data){
        create_chart(data);
		d3.json("https://raw.githubusercontent.com/ryantimjohn/chicago_aldermen_campaign_finance/master/web_json/Ward1_sector.json", function(data){
        create_sector_chart(data);
		
      });
      });