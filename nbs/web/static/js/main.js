// Main application
require([
  'application',
  'routes',
], function(Application, routes) {
  var app = new Application({routes: routes});
});
