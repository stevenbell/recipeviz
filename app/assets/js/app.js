//Total visualization area
var V_HEIGHT = 600
var V_WIDTH = 600

var margin = {
  top: 20,
  bottom: 20,
  left: 50,
  right: 50
};

var instructions = document.querySelector('.panel')
var closeInstructions = document.querySelector('#close')

closeInstructions.addEventListener('click', () => {
  instructions.style.display = "none"
})

var visualization = d3.select('#viz');
// Data structures for the charts - consolidate to one object?
var dim_ing = {};
var g_ing = {}
var charts = {};

//Name chart
var nameChart = dc.bubbleChart("#nameChart");

var form = document.querySelector('.search-recipes')
var search = form.querySelector('input[name="search"]')
form.addEventListener('submit', event => {
  event.preventDefault()

  // Load Data
  d3.json("/search/" + search.value, function(error, data) {
    if(error){
      console.warn(error);
      return;
    }

    //console.log(data);

    // Extract the ingredient names for however many there are
    var names = Object.keys(data[0]);
    names.splice(names.indexOf('name'), 1);
    names.splice(names.indexOf('link'), 1);

    console.log(names);

    var keys = names.map(function(d){
      key = d.replace(/ /g, '');
      if(key.indexOf('(') != -1)
      key = key.slice(0, key.indexOf('('));
      return key;
    });

    console.log(keys)

    // Set up Crossfilter
    var cf = crossfilter(data);
    var all = cf.groupAll();

    //Set up the chart of names
    var dim_name = cf.dimension(function(d){return d.name;});
    var g_name = dim_name.group().reduceCount();
    var colors = ['#8dd3c7','#ffffb3','#bebada','#fb8072','#80b1d3','#fdb462','#b3de69','#fccde5','#d9d9d9','#bc80bd','#ccebc5','#ffed6f']

    nameChart.x(d3.scale.ordinal().domain(dim_name))
      .xUnits(dc.units.ordinal)
      .dimension(dim_name)
      .group(g_name)
      .margins({ top: 0, right: 100, bottom: 0, left: 60})
      .width(window.innerWidth - 50)
      .height(150)
      .elasticY(true)
      .elasticX(true)
      .yAxisPadding(1)
      // .colorDomain([-500, 500])
      .ordinalColors(colors)
      .colorAccessor(function(d) {
        return colorGen(d.key[0].toLowerCase());
      })
      .keyAccessor(function(d) {
        return d.key;
      })
      .valueAccessor(function(d) {
        if(nameChart.filters().length != 0 && nameChart.filters().indexOf(d.key) != -1 && d.value != 0)
          return 2;
        return d.value;
      })
      .radiusValueAccessor(function(d) {
        if(d.value == 0 || nameChart.filters().length == 0 || nameChart.filters().indexOf(d.key) == -1)
          return .25;
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

    //To show filters and links
    nameChart.on('pretransition', function(chart) {
      var links = d3.select('.linkArea').selectAll('.links')
        .data(dim_name.bottom(chart.filters().length))
        .attr('href', function(d){        //hack to update old link, puts links in alphabetical order so yay?
          return "http://" + d.link;
        })
        .html(function(d) {
          return d.name + ", ";
        });
      links.enter().append('a')
        .attr('class', 'links')
        .attr('href', function(d){
          return "http://" + d.link;
        })
        .attr('target', "_blank")
        .html(function(d) {
          return d.name + ", ";
        });
      links.exit().remove();
    });

    // Create a chart for each of the ingredients
    for (i = 0; i < keys.length; i++) {
      dim_ing[keys[i]] = cf.dimension(function(d) {
        return [d[names[i]], 0];
      });
      g_ing[keys[i]] = dim_ing[keys[i]].group();

      var div = visualization.append('div')
        .attr('id', keys[i] + 'Chart') //remove namespaces here
        .attr('class', 'chart')
        .attr('style', 'padding-left:10px; padding-right:30px; float: right;');
      div.append('div')
        .attr('class', 'title')
        .attr('style', 'display: inline-block; margin-top: 7px; vertical-align:top;')
        .append('h4')
          .html(names[i]);
      div.append('div')
        .attr('class', "reset")
        .attr('style', 'margin-left: 10px; margin-top: 15px; display:inline-block; visibility: hidden; vertical-align:top;')
        .append('a')
          .attr('href', "javascript:charts['" + keys[i] + "'].filterAll();dc.redrawAll();")
          .html('<span class="label label-danger">reset</span>');

      charts[keys[i]] = dc.scatterPlot('#' + keys[i] + 'Chart'); //remove namespaces here

      charts[keys[i]].x(d3.scale.linear())
        .y(d3.scale.linear())
        .width(window.innerWidth - 330)
        .height(60)
        .elasticX(true)
        .elasticY(true)
        .yAxisPadding(.5)
        .dimension(dim_ing[keys[i]])
        .group(g_ing[keys[i]])
        .symbolSize(10)
        .clipPadding(40)
        .excludedOpacity(.3)
        .controlsUseVisibility(true);
    }

    function colorGen(letter) {
      if ('an'.includes(letter)) {
        return colors[0]
      } else if ('bo'.includes(letter)) {
        return colors[1]
      } else if ('cp'.includes(letter)) {
        return colors[2]
      } else if ('dq'.includes(letter)) {
        return colors[3]
      } else if ('er'.includes(letter)) {
        return colors[4]
      } else if ('fs'.includes(letter)) {
        return colors[5]
      } else if ('gt'.includes(letter)) {
        return colors[6]
      } else if ('hu'.includes(letter)) {
        return colors[7]
      } else if ('iv'.includes(letter)) {
        return colors[8]
      } else if ('jw'.includes(letter)) {
        return colors[9]
      } else if ('kx'.includes(letter)) {
        return colors[10]
      } else if ('ly'.includes(letter)) {
        return colors[11]
      } else if ('mz'.includes(letter)) {
        return colors[3]
      }
    }


    dc.renderAll();
    //Make things inline
    d3.selectAll('.chart svg').style('display', 'inline-block');
    //hide axes
    d3.selectAll('.chart svg g g.axis.y').style('display', 'none');
    d3.selectAll('#nameChart svg g g.axis.x').style('display', 'none');
    //make it so bubbles don't clip
    d3.selectAll('#nameChart svg g g.chart-body').attr('clip-path', null);
    //adjust symbol opacity
    d3.selectAll('.chart svg g g.chart-body path.symbol').style('opacity', '.7');

    window.onresize = function(event) {
      nameChart.width(window.innerWidth).transitionDuration(750);
      Object.values(charts).forEach(function(chart) {
        chart.width(window.innerWidth - 330).transitionDuration(750);
      });
      dc.redrawAll();
    }

  });
})
