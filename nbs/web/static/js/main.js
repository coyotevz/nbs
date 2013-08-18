// Configure the AMD module loader
require.config({

  // Path where JavaScript root modules are located
  baseUrl: "/static/js",

  paths: {
    // Specify the paths of vendor libraries
    'json':        'vendor/json2',
    'jquery':      'vendor/jquery-1.10.2',
    'underscore':  'vendor/lodash-1.3.1',
    'backbone':    'vendor/backbone-1.0.0',
    'chaplin':     'vendor/chaplin-0.10.0',
    'nunjucks':    'vendor/nunjucks-dev-0.1.10',
  },

  // For non AMD-capable per default, declare dependencies.
  shim: {
    'underscore': {
      exports: '_'
    },
    'backbone': {
      deps: ['json', 'jquery', 'underscore'],
      exports: 'Backbone'
    },
    'nunjucks': {
      exports: 'nunjucks',
    }
  }

  // For easier development, disable browser caching
  // Of course, this should be removed in prodocution environment
  ,urlArgs: 'ver=' + (new Date()).getTime()
});

// Bootstrap the application
require(['application','routes'], function(Application, routes) {
  var app = new Application({routes: routes});
});
