// Configure the AMD module loader
require.config({

  // Path where JavaScript root modules are located
  baseUrl: "/static/js",

  paths: {
    // Specify the paths for vendor libraries
    'json': 'vendor/json2',
    'jquery': 'vendor/jquery-1.10.2',
    'underscore': 'vendor/lodash-1.3.1',
    'backbone': 'vendor/backbone-1.0.0',
    'chaplin': 'vendor/chaplin-0.10.0',
    'nunjucks': 'vendor/nunjucks-dev-0.1.10',
    'bootstrap': 'vendor/bootstrap',
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
    },
    'bootstrap': {
      deps: ['jquery'],
      exports: 'bootstrap'
    }
  }

  // For easier development, disable browser caching
  // Of course, this should be remove in production environment
  ,urlArgs: 'ver=' + (new Date()).getTime()
});
