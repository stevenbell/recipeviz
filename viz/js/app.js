var eggs = [1, 2, 3, 4]

var flour = [1, 2, 3, 4]

//Number of ingredient charts to display
var num_ing = 4;

//Total visualization area
var V_HEIGHT = 1200
var V_WIDTH = 600

var margin = {
  top: 20,
  bottom: 20,
  left: 50,
  right: 50
};

//Function to draw a single scatterplot - hopefully reusable
var histogram = function(data_in, chart_id, value, chart_title) {

  var height = V_HEIGHT / num_ing - margin.top - margin.bottom;
  var width = V_WIDTH - margin.left - margin.right;

  var svg = d3.select("#viz").append("svg")
      .attr("id", "chart" + chart_id)
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")"); // make sure translate graphs properly

  var domain = d3.extent(data_in, function(d){return d[value];});
  var xScale = d3.scaleLinear()
      .domain(domain)
      .range([0, 300]);

  var xAxis = d3.axisBottom(xScale)
    .ticks(6);

  svg.append('g')
     .attr("id", "plot" + chart_id)
     .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
     .call(xAxis);

  d3.select("#plot" + chart_id)
     .append('g')
     .selectAll('rect')
     .data(data_in)
     .enter()
       .append('rect')
       .attr('width', 3)
       .attr('height', 10)
       .attr('x', function(d) {
          return xScale(d[value]);
       })
       .attr('y', -5)
       .style('fill', 'blue')
       .style('fill-opacity', .5);

  svg.append('text')
    .attr("transform", "translate(" + 0 + "," + margin.top + ")")
    .text(chart_title);
}

// Load Data
d3.json("ingredients_matrix.json", function(error, data) {
  if(error){
    console.warn(error);
    return;
  }

  //extract top 4 (or however many) ingredient names, set up
  //dimensions for each?

  //console.log(data);

  // Set up Crossfilter
  var cf = crossfilter(data);
  var dim_name = cf.dimension(function(d){return d.name;});
  //I know the top ingredients. This should be edited to be adaptable.
  var dim_egg = cf.dimension(function(d){return d.egg;});
  var dim_flour = cf.dimension(function(d){return d['all-purpose flour'];});
  var dim_vanilla = cf.dimension(function(d){return d.vanilla;});
  var dim_sugar = cf.dimension(function(d){return d['white sugar'];});

  //console.log(dim_flour.top(Infinity));

  //set up groups - necessary?
  /*var group_egg = dim_egg.group();

  group_egg.top(Infinity).forEach(function(d, i) {
    console.log(JSON.stringify(d));
  });*/

  //Filter to only show values for which egg is not -1
  dim_egg.filter([0, Infinity]);
  dim_flour.filter([0, Infinity]);
  dim_vanilla.filter([0, Infinity]);
  dim_sugar.filter([0, Infinity]);

  /*dim_egg.top(Infinity).forEach(function(d, i) {
    console.log(JSON.stringify(d));
  });*/

  // Function that renders the plots
  var render_plots = function() {
    histogram(dim_egg.top(Infinity), 1, "egg", "Eggs");
    histogram(dim_flour.top(Infinity), 2, "all-purpose flour", "Flour");
    histogram(dim_vanilla.top(Infinity), 3, "vanilla", "Vanilla");
    histogram(dim_sugar.top(Infinity), 4, "white sugar", "Sugar");
  }

  // Render plots for first time
  render_plots();

});
