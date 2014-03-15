define(function(require, filters) {
  "use strict";
  var nunjucks;

  /* Check if have precompiled templates else use HttpLoader */
  if (window.nunjucksPrecompiled) {

    /* we have precompiled templates, use them */
    nunjucks = require('nunjucks-slim');
    if (!nunjucks.env) {
      nunjucks.env = new nunjucks.Environment();
    }
  } else {

    /* we are in development mode */
    nunjucks = require('nunjucks');
    if (!nunjucks.env) {
      var CustomLoader = nunjucks.WebLoader.extend({

        getSource: function(name) {
          var url = require.toUrl(this.baseURL + '/' + name);
          var src = this.fetch(url);
          var _this = this;

          if (!src) {
            return null;
          }

          return { src: src,
            path: name,
            upToDate: function() { return _this.neverUpdate; }
          };
        }

      });

      nunjucks.env = new nunjucks.Environment(
        new CustomLoader('templates')
      );
    }
  }

  var filters = require('./filters');

  for (var fname in filters) {
    nunjucks.env.addFilter(fname, filters[fname]);
  }

  return nunjucks.env;
});
