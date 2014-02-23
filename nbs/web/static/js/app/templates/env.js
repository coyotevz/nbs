define([
  'nunjucks',
  'templates/templates',
], function(nunjucks) {
  "use strict";

  /* Check if have precompiled templates else use HttpLoader */
  if (!nunjucks.env) {
    var CustomLoader = nunjucks.WebLoader.extend({

      getSource: function(name) {
        var url = 'static/js/app/' + this.baseURL + '/' + name;
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

  return nunjucks.env;
});
