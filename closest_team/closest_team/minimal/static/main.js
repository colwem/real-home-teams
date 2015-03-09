(function(){
// vim: sw=2 

var mapid = "mapbox.light",
    access_token = "pk.eyJ1IjoiY29sd2VtIiwiYSI6InpSV2NIT3MifQ.yiyrrpmxhNt6DJZDynUdmA";

var player_tooltip = d3.select("body")
    .append("div")
    .attr("id", "player-tooltip");

var width = 960,
    height = 500;

var tile = d3.geo.tile()
    .size([width, height]);

var projection = d3.geo.mercator()
    .scale((1 << 12) / 2 / Math.PI)
    .translate([-width / 2, -height / 2]); // just temporary

var tileProjection = d3.geo.mercator();

var tilePath = d3.geo.path()
    .projection(tileProjection);

var zoom = d3.behavior.zoom()
    .scale(projection.scale() * 2 * Math.PI)
    .scaleExtent([1 << 10, 1 << 23])
    .translate(projection([-100, 40.7142]).map(function(x) { return -x; }))
    .on("zoom", zoomed);

var path = d3.geo.path().projection(projection);

var map = d3.select("#map");
var svg = map.append('svg')
  .attr("width", width)
  .attr("height", height);

var raster = svg.append("g");

var voronoi_paths = svg
  .append("g")
  .attr("id", "voronoi")
  .selectAll(".voronoi");

var player_circles = svg
  .append("g")
  .attr("id", "players")
  .selectAll(".player");

var stadium_logos = svg
  .append("g")
  .attr("id", "stadiums")
  .selectAll(".stadium");

zoomed();

// var player_tip = d3.tip()
  // .attr('class', 'd3-tip')
  // .html(function(d) {
    // return "<strong>Name</strong> <span ='color:red'>" + d.name + "</span>";
  // });
// svg.call(player_tip);

d3.json( "players.json", function(error, players) {
  d3.json("stadiums.json", function(error, stadiums) {
    ready(error, players, stadiums);
  });
});

// queue()
    // .defer(d3.json, "players.json")
    // .defer(d3.json, "stadiums.json")
    // .defer(d3.json, "static/world-110m.json")
    // .await(ready);


function ready(error, players, stadiums) {
  stadiums = stadiums.stadiums;
  players = players.players;

  var delaunay = d3.geo.delaunay(stadiums.map(function(d) { 
            return d.coordinates; 
        })),
      voronoi = d3.geo.voronoi(stadiums, delaunay).geometries;

  voronoi_paths
    .data(voronoi)
    .enter().insert("path")
    .attr("class", "voronoi ocean")
    .style("fill", function(d, i) { 
      return stadiums[i].pri_color;
    });

  voronoi_paths = d3.selectAll(".voronoi");
    // .on("click", stadium_tip.show);

  player_circles
    .data(players)
    .enter().insert("circle")
    .attr("class", "player")
    .on("mouseover", playerMouseover)
    .on("mouseout", playerMouseout);

  player_circles = d3.selectAll(".player");

  stadium_logos
    .data(stadiums)
    .enter().insert("image")
    .attr("class", "stadium")
    .attr("xlink:href", function(d) {
      return "static/logos/" + d.abbr + "_logo.svg";
    })
    .on("click", stadiumClick);

  stadium_logos = d3.selectAll(".stadium");

  svg.call(zoom);
  zoomed();

    // .on("mouseover", player_tip.show)
    // .on("mouseout", player_tip.hide)

  // var w = 20,
      // h = 20;
}

function zoomed() {

  // g.attr("transform", "translate(" + zoom.scale() + ")scale(" +
      // zoom.scale() + ")");


  // d3.selectAll(".stadium")
    // .attr("height", h)
    // .attr("width", w);

  var tiles = tile
    .scale(zoom.scale())
    .translate(zoom.translate())
    ();

  projection
    .scale(zoom.scale() / 2 / Math.PI)
    .translate(zoom.translate());
  
  voronoi_paths.attr('d', path);

  var base = (1 << 12),
      c =  2, 
      b =  2;

  player_circles
    .attr("r", function(d) { 
      var r = b + c*Math.log(d.weighted_av + 1); 
      return r;
    }) 
    .style("stroke-width", 0.5 / zoom.scale() + "px")
    .attr("transform", function(d) {
      var p = projection(d.coordinates);
      return "translate(" + [p[0], p[1]] + ")";
    });

  var h = 20,
      w = 20;
  stadium_logos
    .attr("height", h)
    .attr("width", w)
    .attr("transform", function(d) {
      var p = projection(d.coordinates);
      return "translate(" + [p[0] -  w/2, p[1] - h/2] + ")";
    });

  var image = raster
    .attr("transform", "scale(" + tiles.scale + ")translate(" + 
        tiles.translate + ")")
    .selectAll("image")
    .data(tiles, function(d) { return d; });

  image.exit()
    .remove();

  image.enter().append("image")
    .attr("xlink:href", function(d) { 
      return "http://" + 
        "api.tiles.mapbox.com/v4/" + 
        mapid + "/" + 
        d[2] + "/" + 
        d[0] + "/" +
        d[1] + ".png" +
        "?access_token=" + access_token; 
    })
    .attr("width", 1)
    .attr("height", 1)
    .attr("x", function(d) { return d[0]; })
    .attr("y", function(d) { return d[1]; });

}

function playerMouseover(d) {

  player_tooltip
    .style("display", "inline-block");
  player_tooltip
    .transition()
    .duration(100)
    .style("opacity", 0.9);
  player_tooltip.html(d.name)
    .style("left", d3.event.pageX - 100 + "px")
    .style("top", d3.event.pageY - 40 + "px");
}

var block;
function stadiumClick(d) {
  if( block ) {
    block.style('display', 'none');
  }
  block = d3.select('#' + d.abbr + '-tip');
  block
    .style('display', 'block')
    .style('top', '0px');

  block.select('.close')
    .on('click', stadiumClose);
  map.node().appendChild(block.node());
}

function stadiumClose(d) {
  block.style('display', 'none');
}

function playerMouseout(d) {
  player_tooltip
    .transition()
    .duration(100)
    .style("opacity", 0)
    .style("display", "none");
}

})();

