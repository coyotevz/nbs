// Configure the AMD module loader
// This configuration can be shared along applications
// Use as:
// <script src="/static/js/config.js"></script>
// <script src="/static/js/vendor/require.js" data-main="script/<app>"></script>
var require = {

  // Path where JavaScript root modules are located
  baseUrl: "/static/js",

  paths: {
    // Specify the paths for vendor libraries
    'json':                 'vendor/json2',
    'jquery':               'vendor/jquery-1.10.2',
    'jquery.keycode':       'vendor/jquery.keycode',
    'jquery.number':        'vendor/jquery.number-2.1.3',
    'underscore':           'vendor/lodash-1.3.1',
    'backbone':             'vendor/backbone-1.0.0',
    'backbone.stickit':     'vendor/backbone.stickit-0.6.3',
    'backbone.relational':  'vendor/backbone-relational',
    'backbone.validation':  'vendor/backbone-validation-0.8.1-amd',
    'chaplin':              'vendor/chaplin-0.10.0',
    'nunjucks':             'vendor/nunjucks-dev-0.1.10',
    'bootstrap':            'vendor/bootstrap',

    // List internal paths
    // 'ClientModel': 'models/client',
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
    'backbone.stickit': {
      deps: ['jquery', 'backbone'],
    },
    'backbone.relational': {
      deps: ['backbone']
    },
    'nunjucks': {
      exports: 'nunjucks',
    },
    'bootstrap': {
      deps: ['jquery'],
      exports: 'bootstrap'
    },
    'jquery.keycode': {
      deps: ['jquery', 'underscore']
    },
    'jquery.number': {
      deps: ['jquery', 'underscore'],
      init: function($, _) {
        // Shortcut to format numbers to standard
        $.numeric = function(val) {
          return $.number(val, 2, ',', '.');
        };
      }
    }
  }

  // For easier development, disable browser caching
  // Of course, this should be remove in production environment
  ,urlArgs: 'ver=' + (new Date()).getTime()
};