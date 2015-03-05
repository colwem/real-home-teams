(function(){

var width = 960,
    height = 500;

var projection = d3.geo.mercator()
  .precision(0.1)
  .rotate([100,0,0])
  .center([0, 40])
  .scale((1 << 12) / 2 / Math.PI);
  // .clipAngle(90);
  
      
var path = d3.geo.path().projection(projection);

var zoom = d3.behavior.zoom()
  .scaleExtent([1, 10])
  .on("zoom", zoomed);

  // var drag = d3.behavior.drag()
    // .origin(function(d) { return d; })
    // .on("dragstart", dragstarted)
    // .on("drag", dragged)
    // .on("dragend", dragended);

var svg = d3.select('#map')
  .append('svg')
  .attr("width", width)
  .attr("height", height)
  .call(zoom);

var g = svg.append("g");

var player_tip = d3.tip()
  .attr('class', 'd3-tip')
  .html(function(d) {
    return "<strong>Name</strong> <span ='color:red'>" + d.name + "</span>";
  });
svg.call(player_tip);

d3.json( "players.json", function(error, players) {
  d3.json("stadiums.json", function(error, stadiums) {
    d3.json("static/world-110m.json", function(error, world) {
      ready(error, players, stadiums, world);
    });
  });
});

// queue()
    // .defer(d3.json, "players.json")
    // .defer(d3.json, "stadiums.json")
    // .defer(d3.json, "static/world-110m.json")
    // .await(ready);


function ready(error, players, stadiums, world) {
  stadiums = stadiums.stadiums;
  players = players.players;
  

  var stadium_tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([0, 0])
    .html(function(d, i) {
        return "<strong>Name</strong> <span style='color:red'>" + stadiums[i].name + "</span>";
    });
  svg.call(stadium_tip);

  var delaunay = d3.geo.delaunay(stadiums.map(function(d) { 
            return d.coordinates; 
        })),
      voronoi = d3.geo.voronoi(stadiums, delaunay).geometries;

  g.append("g")
    .attr("id", "world")
    .insert("path")
    .datum(topojson.feature(world, world.objects.land))
    .attr("d", path);

  g.append("g")
    .attr("id", "voronoi")
    .selectAll(".voronoi")
    .data(voronoi)
    .enter().insert("path")
    .attr("class", "voronoi ocean")
    .style("fill", function(d, i) { 
      return stadiums[i].pri_color;
    })
  .attr('d', path)
    .on("click", stadium_tip.show);


  g.append("g")
    .attr("id", "players")
    .selectAll(".player")
    .data(players)
    .enter().insert("circle")
    .attr("class", "player")
    .on("mouseover", player_tip.show)
    .on("mouseout", player_tip.hide)
    .attr("transform", function(d) {
      var p = projection(d.coordinates);
      return "translate(" + [p[0], p[1]] + ")";
    });

  var w = 20,
      h = 20;

  g.append("g")
    .attr("id", "stadiums")
    .selectAll(".stadium")
    .data(stadiums)
    .enter().insert("image")
    .attr("class", "stadium")
    .attr("xlink:href", function(d) {
      return "static/logos/" + d.abbr + "_logo.svg";
    })
    .attr("transform", function(d) {
      var p = projection(d.coordinates);
      return "translate(" + [p[0] -  w/2, p[1] - h/2] + ")";
    });
  
  zoomed();
  // TODO voronoi.mesh
  // svg.append("g")
    // .attr("id", "borders")
    // .selectAll(".voronoi-border")
      // .data(voronoi.map(function(cell) {
        // return {type: "LineString", coordinates: cell.coordinates[0]};
      // }))
    // .enter().insert("path", ".ocean")
      // .attr("class", "voronoi-border")
      // .style("stroke", function(d, i) { 
        // return stadiums[i].sec_color;
      // })
      // .attr("d", path);

  // $('table').on('click', function(d) {
    // trs.sort(function(a, b) { 
      // return d3.descending(a.av, b.av); 
    // });
  // });
  // svg.insert("path", ".ocean")
    // .datum(
      // topojson.mesh(
        // states,
        // states.objects.ne_10m_admin_1_states_provinces,
        // function(a, b) { return a !== b; }))
      // .attr("class", "countries")
      // .attr("d", path);
}

function zoomed() {
  g.attr("transform", "translate(" + d3.event.translate + ")scale(" +
      d3.event.scale + ")");

  var h = 20 / d3.event.scale,
      w = 20 / d3.event.scale;
  d3.selectAll(".stadium")
    .attr("height", h)
    .attr("width", w);

  var c = 2 / d3.event.scale, 
      b = 1 / d3.event.scale;
  d3.selectAll(".player")
    .attr("r", function(d) { return b + c*Math.log(d.weighted_av + 1); })
    .style("stroke-width", 0.5 / d3.event.scale + "px");

  player_tip.offset([ 10 / d3.event.scale, 0]);
}

})();

