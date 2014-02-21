define(function() {
  "use strict";

  var routes = function(match) {
    match('', 'pos#index', {name: 'pos_index'});
  };

  return routes;
});
