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
// Data structures for the charts - consolidate to one object?
var dim_ing = {};
var g_ing = {}
var charts = {};

//Name chart
var nameChart = dc.bubbleChart("#nameChart");

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

  // Set up Crossfilter
  var cf = crossfilter(data);
  var all = cf.groupAll();

  //Set up the chart of names
  var dim_name = cf.dimension(function(d){return d.name;});
  var g_name = dim_name.group().reduceCount();

  console.log(g_name.top(5));

  nameChart.x(d3.scale.ordinal().domain(dim_name))
    .xUnits(dc.units.ordinal)
    .dimension(dim_name)
    .group(g_name)
    .yAxisPadding(1)
    .xAxisPadding(1)
    .elasticY(true)
    .elasticX(true)
    .colorDomain([-500, 500])
    .keyAccessor(function(d) {
      return d.key;
    })
    .valueAccessor(function(d) {
      if(nameChart.filters().length != 0 && nameChart.filters().indexOf(d.key) != -1)
        return 2;
      return d.value;
    })
    .radiusValueAccessor(function(d) {
      if(d.value == 0 || nameChart.filters().length == 0 || nameChart.filters().indexOf(d.key) == -1)
        return .5;
      return 3;
    })
    .controlsUseVisibility(true)
    .renderTitle(true)
    .title(function(d) {
      return d.key;
    })
    .label(function(d) {
      if(d.value == 0 || nameChart.filters().length == 0 || nameChart.filters().indexOf(d.key) == -1)
        return "";
      return d.key;
    });

    //To See what filters are on the chart
    /*.renderlet(function(chart) {
            dc.events.trigger(function() {
                console.log(nameChart.filters())
            });
        });*/


  //hide axes: https://github.com/dc-js/dc.js/issues/548
  // Create a chart for each of the ingredients
  for (i = 0; i < keys.length; i++) {
    dim_ing[keys[i]] = cf.dimension(function(d) {
      return [0, d[names[i]]];
    });
    g_ing[keys[i]] = dim_ing[keys[i]].group();

    visualization.append('div')
      .attr('id', keys[i] + 'Chart') //remove namespaces here
      .attr('class', 'chart')
      .attr('style', 'width:200px; height:400px; padding:10px;')
      .append('h4')
        .html(names[i])
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
      .excludedOpacity(.5)
      .controlsUseVisibility(true);
  }

  dc.renderAll();

});
