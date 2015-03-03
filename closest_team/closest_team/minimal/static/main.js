(function(){
// vim:sw=2:

  //Leaflet
var map = L.map('map').setView([39.77477, -97.03125], 4);

var tiles = L.tileLayer('http://oatile{s}.mqcdn.com/tiles/1.0.0/sat/{z}/{x}/{y}.jpg', {
        attribution: 'Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a> &mdash; Portions Courtesy NASA/JPL-Caltech and U.S. Depart. of Agriculture, Farm Service Agency',
        subdomains: '1234'
});

tiles.addTo(map);

L.control.mousePosition().addTo(map);

var svg = d3.select(map.getPanes().overlayPane).append("svg"),
    g = svg.append("g").attr("class", "leaflet-zoom-hide");

// var svg = d3.select('table').append("svg"),
    // g = svg.append("g").attr("class", "leaflet-zoom-hide");

function projectPoint(x, y) {
  var point = map.latLngToLayerPoint(new L.LatLng(y, x));
  this.stream.point(point.x, point.y);
}
  
var player_tip = d3.tip()
  .attr('class', 'd3-tip')
  .offset([-10, 0])
  .html(function(d) {
    return "<strong>Name</strong> <span ='color:red'>" + d.name + "</span>";
  });
svg.call(player_tip);

queue()
    .defer(d3.json, "players.json")
    .defer(d3.json, "stadiums.json")
    .await(ready);

function ready(error, players, stadiums) {
  stadiums = stadiums.stadiums;
  players = players.players;
  
  var stadium_tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-10, 0])
    .html(function(d, i) {
        return "<strong>Name</strong> <span style='color:red'>" + stadiums[i].name + "</span>";
    });
  svg.call(stadium_tip);

  // var delaunay = d3.geo.delaunay(stadiums.map(function(d) { 
            // return d.coordinates; 
        // })),
      // voronoi = d3.geo.voronoi(stadiums, delaunay).geometries;

  var coords = stadiums.map(function(d) {return d.coordinates;});
  var voronoi = d3.geom.voronoi();
  // voronoi.clipExtent([[-270, 85],[80,-80]]); 
  var polygons = voronoi(coords);

  var transform = d3.geo.transform({point: projectPoint}),
      path = d3.geo.path().projection(transform);

    
  var bounds = map.getBounds(),
      drawLimit = bounds.pad(0.1);

  function coordsToLatLng(c) {
      return new L.LatLng(c[1], c[0]);
  }

  function critical_path(a, b){
    return drawLimit.contains(a) || drawLimit.contains(b);
  }

  function find_transition(first, last, f) {
    var t = last,
        b = first,
        c = b + (t - b) / 2,
        iters = 10;

    for( var i = 0; i < iters; i++) {
      if(f(c)) {
        b = c;
        c = c + (t - c)/2; 
      } else {
        t = c;
        c = b + (c - b)/2;
      }
    }
    return b;
  }

  function clip_line(a, b) {
    var la = coordsToLatLng(a),
        lb = coordsToLatLng(b),
        ca = drawLimit.contains(la),
        cb = drawLimit.contains(lb),
        begin = a,
        end = b;
    if(ca || cb && ! (cb && ca)) {
      if(cb) {
        begin = b;
        end = a;
      }
      var interp = d3.geo.interpolate(a, b);
      var transition = find_transition(0, 1, function (v) {
        var p = coordsToLatLng(interp(v));
        return drawLimit.contains(p);
      });

      if(ca) {
        b = interp(transition);
      } else {
        a = interp(transition);
      }
    }
    return [a, b];
  }

  function indexOf(arr, f) {
    for (var i = 0; i < arr.length; i++) {
      if( f(arr[i]) ) return i;
    }
    return -1;
  }
  // var sf = {"type":"Polygon",
    // "coordinates": [ [
      // [-113.95461138901611,40.25369609821318],
      // [-115.72561442989571,37.60733996825128],
      // [-180 - (180 - 87.50496409829238), -47.783881637676274],
      // [-180 - (180 - 85.62306665182882), -44.684855690846135],
      // [-114.0188629659868,40.52230524471365],
      // [-113.95461138901611,40.25369609821318] ] ],
    // "neighbors":[9,0,24,16,21,9]
  // },
  // oak = {
    // "type": "Polygon",
    // "coordinates": [[
      // [-360 + 85.62306665182882,-44.684855690846135],
      // [-360 + 83.08646685000178,-39.99043555303789],
      // [-114.42179111790796,42.4616308490941],
      // [-114.0188629659868,40.52230524471366],
      // [-360 + 85.62306665182882,-44.684855690846135]]],
    // "neighbors":[26,16,25,9,26]
  // };

  // var sf = {"type":"Polygon",
    // "coordinates": [ [
      // [-113.95461138901611,40.25369609821318],
      // [-115.72561442989571,37.60733996825128],
      // [87.50496409829238, -47.783881637676274],
      // [85.62306665182882, -44.684855690846135],
      // [-114.0188629659868,40.52230524471365],
      // [-113.95461138901611,40.25369609821318] ] ],
    // "neighbors":[9,0,24,16,21,9]
  // },
  // oak = {
    // "type": "Polygon",
    // "coordinates": [[
      // [85.62306665182882,-44.684855690846135],
      // [83.08646685000178,-39.99043555303789],
      // [-114.42179111790796,42.4616308490941],
      // [-114.0188629659868,40.52230524471366],
      // [85.62306665182882,-44.684855690846135]]],
    // "neighbors":[26,16,25,9,26]
  // };
  // var nv = JSON.parse(JSON.stringify(voronoi));
  // nv = [sf, oak];
  // nv.forEach( function(v) {
    // var c = v.coordinates[0];
    // for(var i = 0; i < c.length - 1; i++) {
      // if (c[i][0] < -100 && c[i + 1][0] > 0){
        // c[i + 1][0] += -360;
      // }
      // if (c[i + 1][0] < -100 && c[i][0] > 0){
        // c[i][0] += -360;
      // }
    // }
  // });
  // nv.forEach( function(v) {
    // var c = v.coordinates[0];
    // for(var i = 0; i < c.length - 2; i++) {
      // var la = coordsToLatLng(c[i]),
          // lb = coordsToLatLng(c[i + 1]),
          // lc = coordsToLatLng(c[i + 2]);

      // if( ! critical_path(la, lb) && ! critical_path(lb, lc)) {
        // c.splice(i + 1, 1);
      // }
    // }

    // for(i = 0; i < c.length - 1; i++) {
      // var la = coordsToLatLng(c[i]);
      // var lb = coordsToLatLng(c[i + 1]);
      // if(drawLimit.contains(la) && drawLimit.contains(lb)) {
        // continue;
      // } 
      // var ls = clip_line(c[i], c[i + 1]);
      // v.coordinates[0][i] = ls[0];
      // v.coordinates[0][i + 1] = ls[1];
    // }
  // });
  polygons = polygons.map( function(v) {
    return { 
      "type": "Polygon",
      "coordinates": [v],
      "point": v.point
    };
  });
  var voronoi_features = g.append("g")
    .attr("id", "voronoi")
    .selectAll(".voronoi")
      .data(polygons)
    .enter().insert("path")
      .attr("class", "voronoi ocean")
      .style("fill", function(d, i) { 
        return stadiums[i].pri_color;
      })
      .on("click", stadium_tip.show);

  // var c = 2, 
      // b = 0.1,
      // player_features = g.append("g")
        // .attr("id", "players")
        // .selectAll(".player")
          // .data(players)
        // .enter().insert("circle")
          // .attr("class", "player")
          // .attr("r", function(d) { return b + c*Math.log(d.weighted_av + 1); })
          // .on("mouseover", player_tip.show)
          // .on("mouseout", player_tip.hide);

  // var w = 20,
      // h = 20,
      // stadium_features = g.append("g")
        // .attr("id", "stadiums")
        // .selectAll(".stadium")
          // .data(stadiums)
        // .enter().insert("image")
          // .attr("class", "stadium")
          // .attr("xlink:href", function(d) {
              // return "static/logos/" + d.abbr + "_logo.svg";
          // })
          // .attr("height", h)
          // .attr("width", w);

  // map.on("viewreset", reset);
  // reset();

  function reset() { 
    var bounds = map.getBounds(),
        topLeft = map.latLngToLayerPoint(bounds.getNorthWest()),
        bottomRight = map.latLngToLayerPoint(bounds.getSouthEast()),
        drawLimit = bounds.pad(0);

    svg .style("width", map.getSize().x + 'px')
        .style("height", map.getSize().y + 'px')
        .style("margin-left", topLeft.x + 'px')
        .style("margin-top", topLeft.y + 'px');
   
    g.attr("transform", "translate(" + -topLeft.x + "," + -topLeft.y + ")"); 
        
    voronoi_features.attr("d", path);


    // svg.attr("width", bottomRight[0] - topLeft[0])
      // .attr("height", bottomRight[1] - topLeft[1])
      // .style("left", topLeft[0] + "px")
      // .style("top", topLeft[1] + "px");
    


    // stadium_features.attr("transform", function(d) { 
      // var x = d.coordinates[1], 
          // y = d.coordinates[0],
          // point = map.latLngToLayerPoint(new L.LatLng(y, x));
      // return "translate(" + [point[0] - w/2, point[1] - h/2] + ")";
    // });

    // player_features.attr("transform", function(d) { 
      // var x = d.coordinates[1], 
          // y = d.coordinates[0],
          // point = map.latLngToLayerPoint(new L.LatLng(y, x));
      // return "translate(" + point + ")";
    // });
  }

  var CustomLayer = L.Class.extend({
    onAdd: function(map) {
      map.on("viewreset moveend", reset);
      reset();
      this._map = map;
    }
  });
  map.addLayer(new CustomLayer());

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

  // var table = d3.selectAll('#table').append('table');
  // var trs = table.selectAll('tr');
  // var enter = trs.data(stadiums).enter();
  // var tr = enter.insert("tr");
  // tr.append('td').text( function(d) { return d.team; });
  // tr.append('td').text( function(d) { return d.av; });

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


})();

