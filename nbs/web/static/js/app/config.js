// Configure the AMD module loader
// This configuration can be shared along applications
// Use as:
// <script src="/static/js/config.js"></script>
// <script src="/static/js/vendor/require.js" data-main="script/<app>"></script>
var require = {

  // Path where JavaScript root modules are located
  baseUrl: "/static/js/app",

  paths: {
    // Specify the paths for vendor libraries
    'json':                   'vendor/json2-2013-05-25',
    'jquery':                 'vendor/jquery-1.10.2',
    'jquery.number':          'vendor/jquery.number-2.1.3',
    'underscore':             'vendor/lodash-2.4.1',
    'backbone':               'vendor/backbone-1.1.2',
    'backbone.stickit':       'vendor/backbone-stickit-0.8.0',
    'backbone.validation':    'vendor/backbone.validation/dist/backbone-validation-amd',
    'chaplin':                'vendor/chaplin-1.0.0',
    'nunjucks':               'vendor/nunjucks-1.0.1',
    'nunjucks-slim':          'vendor/nunjucks-slim-1.0.1',
    'pace':                   'vendor/pace-0.5.1',

    // Bootstap files
    'bootstrap.affix':        'vendor/bootstrap/affix',
    'bootstrap.alert':        'vendor/bootstrap/alert',
    'bootstrap.button':       'vendor/bootstrap/button',
    'bootstrap.carousel':     'vendor/bootstrap/carousel',
    'bootstrap.collapse':     'vendor/bootstrap/collapse',
    'bootstrap.dropdown':     'vendor/bootstrap/dropdown',
    'bootstrap.modal':        'vendor/bootstrap/modal',
    'bootstrap.popover':      'vendor/bootstrap/popover',
    'bootstrap.scrollspy':    'vendor/bootstrap/scrollspy',
    'bootstrap.tab':          'vendor/bootstrap/tab',
    'bootstrap.tooltip':      'vendor/bootstrap/tooltip',
    'bootstrap.transition':   'vendor/bootstrap/transition',

    // Custom plugins for this project
    'nbs.autogrow':           'lib/nbs.autogrow',
    'nbs.checkbox':           'lib/nbs.checkbox',
    'nbs.fixedheader':        'lib/nbs.fixedheader',
    'nbs.keycode':            'lib/nbs.keycode',
    'nbs.radio':              'lib/nbs.radio',
    'backbone.associations':  'lib/backbone-associations',
    'backbone.trackit':       'lib/backbone-trackit',

    // selectize
    'selectize':              'vendor/selectize',

    // List internal paths
    // 'ClientModel': 'models/client',
  },

  // For non AMD-capable per default, declare dependencies.
  shim: {
    'pace': {
      deps: ['jquery'],
    },
    'underscore': {
      exports: '_'
    },
    'backbone': {
      // inject json as a dependency
      deps: ['json', 'jquery', 'underscore'],
      exports: 'Backbone'
    },
    'nunjucks': {
      exports: 'nunjucks',
    },
    'jquery.number': {
      deps: ['jquery', 'underscore'],
      init: function($, _) {
        // Shortcut to format numbers to standard
        $.numeric = function(val) {
          return $.number(val, 2, ',', '.');
        };
      }
    },

    // bootstrap dependecy matrix
    'bootstrap.affix':      { deps: ['jquery'] },
    'bootstrap.alert':      { deps: ['jquery'] },
    'bootstrap.button':     { deps: ['jquery'] },
    'bootstrap.carousel':   { deps: ['jquery'] },
    'bootstrap.collapse':   { deps: ['jquery', 'bootstrap.transitions'] },
    'bootstrap.dropdown':   { deps: ['jquery'] },
    'bootstrap.modal':      { deps: ['jquery'] },
    'bootstrap.popover':    { deps: ['jquery', 'bootstrap.tooltip'] },
    'bootstrap.scrollspy':  { deps: ['jquery'] },
    'bootstrap.tab':        { deps: ['jquery'] },
    'bootstrap.tooltip':    { deps: ['jquery'] },
    'bootstrap.transition': { deps: ['jquery'] },

    'selectize': {
      exports: '$.selectize',
      deps: ['jquery'],
    },
  },

  // For easier development, disable browser caching
  // Of course, this should be remove in production environment
  urlArgs: 'ver=' + (new Date()).getTime()
};
