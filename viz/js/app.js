var eggs = [1, 2, 3, 4]

var flour = [1, 2, 3, 4]

//Number of ingredient charts to display
var num_ing = 4;

//Total visualization area
var V_HEIGHT = 600
var V_WIDTH = 600

var margin = {
  top: 20,
  bottom: 20,
  left: 50,
  right: 50
};

var eggChart = dc.scatterPlot("#eggChart");
var flourChart = dc.scatterPlot("#flourChart");
var nameChart = dc.bubbleChart("#nameChart");

// Load Data
d3.json("ingredients_matrix.json", function(error, data) {
  if(error){
    console.warn(error);
    return;
  }

  //extract top 4 (or however many) ingredient names, set up
  //dimensions for each?

  // Set up Crossfilter
  var cf = crossfilter(data);
  var all = cf.groupAll();
  var dim_name = cf.dimension(function(d){return d.name;});
  //I know the top ingredients. This should be edited to be adaptable.
  var dim_egg = cf.dimension(function(d){return [d.egg, 0];});
  var dim_flour = cf.dimension(function(d){return [d['all-purpose flour'], 0];});
  var dim_vanilla = cf.dimension(function(d){return d.vanilla;});
  var dim_sugar = cf.dimension(function(d){return d['white sugar'];});


  //Group
  g_egg = dim_egg.group();
  g_flour = dim_flour.group();
  g_name = dim_name.group();

  //hide axes: https://github.com/dc-js/dc.js/issues/548
  eggChart.x(d3.scale.linear())
    .yAxisPadding(3)
    .xAxisPadding(1)
    .elasticX(true)
    .elasticY(true)
    .dimension(dim_egg)
    .group(g_egg)
    .symbolSize(10)
    .clipPadding(10)
    .excludedColor("red")
    .controlsUseVisibility(true);

  flourChart.x(d3.scale.linear())
    .yAxisPadding(3)
    .xAxisPadding(100)
    .elasticX(true)
    .elasticY(true)
    .dimension(dim_flour)
    .group(g_flour)
    .symbolSize(10)
    .clipPadding(10)
    .excludedColor("red")
    .controlsUseVisibility(true);

  nameChart.x(d3.scale.linear())
    .dimension(dim_name)
    .group(g_name); 

  dc.renderAll();

});
