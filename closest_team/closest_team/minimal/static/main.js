(function(){

var mapid = "mapbox.light",
    access_token = "pk.eyJ1IjoiY29sd2VtIiwiYSI6InpSV2NIT3MifQ.yiyrrpmxhNt6DJZDynUdmA";

var width = 960,
    height = 500,
    prefix = prefixMatch(["webkit", "ms", "Moz", "O"]);

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
    .scaleExtent([1 << 11, 1 << 17])
    .translate(projection([-100, 40.7142]).map(function(x) { return -x; }))
    .on("zoom", zoomed);

var path = d3.geo.path().projection(projection);

var svg = d3.select("#map").append('svg')
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
  .selectAll(".stadium")

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
  

  // var stadium_tip = d3.tip()
    // .attr('class', 'd3-tip')
    // .offset([0, 0])
    // .html(function(d, i) {
        // return "<strong>Name</strong> <span style='color:red'>" + stadiums[i].name + "</span>";
    // });
  // svg.call(stadium_tip);

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
    .attr("class", "player");
  
  player_circles = d3.selectAll(".player");

  stadium_logos
    .data(stadiums)
    .enter().insert("image")
    .attr("class", "stadium")
    .attr("xlink:href", function(d) {
      return "static/logos/" + d.abbr + "_logo.svg";
    });

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

function mousemoved() {
  info.text(formatLocation(projection.invert(d3.mouse(this)), zoom.scale()));
}

function matrix3d(scale, translate) {
  var k = scale / 256, r = scale % 1 ? Number : Math.round;
  return "matrix3d(" + [k, 0, 0, 0, 0, k, 0, 0, 0, 0, k, 0, r(translate[0] * scale), r(translate[1] * scale), 0, 1 ] + ")";
}

function prefixMatch(p) {
  var i = -1, n = p.length, s = document.body.style;
  while (++i < n) if (p[i] + "Transform" in s) return "-" + p[i].toLowerCase() + "-";
  return "";
}

function formatLocation(p, k) {
  var format = d3.format("." + Math.floor(Math.log(k) / 2 - 2) + "f");
  return (p[1] < 0 ? format(-p[1]) + "°S" : format(p[1]) + "°N") + " " +
    (p[0] < 0 ? format(-p[0]) + "°W" : format(p[0]) + "°E");
}
  // var scale = d3.event.scale;
  // player_tip.offset(function() {
    // return [this.getBBox().height / 2 / scale, 0];
  // });

})();

