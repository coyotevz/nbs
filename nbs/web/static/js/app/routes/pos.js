define(function() {
  "use strict";

  var routes = function(match) {
    match('', 'pos#create', {name: 'pos_create'});
    match(':id', 'pos#edit', {name: 'pos_edit'});
  };

  return routes;
});
