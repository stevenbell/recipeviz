var eggs = [1, 2, 3, 4]

var flour = [1, 2, 3, 4]

var height = 600
var width = 1200

// Load Data Here!

var xScale = d3.scaleLinear()
    .domain(d3.extent(eggs, d => d))
    .range([0, 300])

var xAxis = d3.axisBottom(xScale)
  .ticks(eggs.length)

var svg = d3.select('svg')

svg.append('g')
   .attr('transform', `translate(0, 310)`)
   .call(xAxis)

svg.append('g')
   .selectAll('rect')
   .data(eggs)
   .enter()
     .append('rect')
     .attr('width', 3)
     .attr('height', 10)
     .attr('x', d => xScale(d) - 1)
     .attr('y', 300)
     .style('fill', 'blue')
     .style('fill-opacity', .7)

svg.append('text')
  .attr('transform', 'translate(0, 280)')
  .text('Eggs')
