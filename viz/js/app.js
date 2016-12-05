//Total visualization area
var V_HEIGHT = 600
var V_WIDTH = 600

var margin = {
  top: 20,
  bottom: 20,
  left: 50,
  right: 50
};

var visualization = d3.select('#viz');
var dim_ing = {};
var g_ing = {}
var charts = {};
//var eggChart = dc.scatterPlot("#eggChart");
//var flourChart = dc.scatterPlot("#flourChart");
//var sugarChart = dc.scatterPlot("#sugarChart");

// Load Data
d3.json("ingredients_matrix.json", function(error, data) {
  if(error){
    console.warn(error);
    return;
  }

  //console.log(data);

  // Extract the ingredient names for however many there are
  var names = Object.keys(data[0]);
  names.splice(names.indexOf('name'), 1);

  var keys = names.map(function(d){
    return d.replace(' ', '');
  });

  console.log(keys);

  // Set up Crossfilter
  var cf = crossfilter(data);
  var all = cf.groupAll();

  //create dimensions for all the ingredients
  /*var chart_data = keys.map(function(d){
    return {
      name: d,
      dim: cf.dimension(function(c) {
        return [0, c[d];
      })
      group: this.dim.group();
      chart: dc.scatterPlot('#' + d + 'Chart')
    };
  });*/

  for (i = 0; i < keys.length; i++) {
    dim_ing[keys[i]] = cf.dimension(function(d) {
      return [0, d[names[i]]];
    });
    g_ing[keys[i]] = dim_ing[keys[i]].group();

    visualization.append('div')
      .attr('id', keys[i] + 'Chart') //remove namespaces here
      .attr('class', 'chart')
      .attr('style', 'width:200px; height:400px')
      .append('div')
        .attr('class', "reset")
        .attr('style', 'visibility: hidden;')
        .append('a')
          .attr('href', "javascript:charts['" + keys[i] + "'].filterAll();dc.redrawAll();")
          .html('reset');

    charts[keys[i]] = dc.scatterPlot('#' + keys[i] + 'Chart'); //remove namespaces here

    charts[keys[i]].x(d3.scale.linear())
      .y(d3.scale.linear())
      .yAxisPadding(1)
      .xAxisPadding(1)
      .elasticX(true)
      .elasticY(true)
      .dimension(dim_ing[keys[i]])
      .group(g_ing[keys[i]])
      .symbolSize(10)
      .clipPadding(20)
      .excludedColor("red")
      .controlsUseVisibility(true);
  }

  var nameChart = dc.bubbleChart("#nameChart");
  var dim_name = cf.dimension(function(d){return d.name;});
  var g_name = dim_name.group();

  //hide axes: https://github.com/dc-js/dc.js/issues/548

  nameChart.x(d3.scale.linear())
    .dimension(dim_name)
    .group(g_name); 

  dc.renderAll();

});
