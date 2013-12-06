define([
  'jquery',
  'underscore',
  'chaplin',
  'templates/env',
  'backbone.stickit',
], function($, _, Chaplin, env) {
  "use strict";

  var View = Chaplin.View.extend({

    getTemplateFunction: function() {
      /* Template compilation
       * ~~~~~~~~~~~~~~~~~~~~
       *
       * We use nunjucks templates to render views.
       * The templates is loaded with nunjucks.WebLoader. On rendering, it is
       * compiled on the client-side.
       * The compiled template function replaced the string on the view
       * prototype.
       *
       * In the end we want to precompile the templates to JavaScript functions
       * on the server-side and just load the JavaScript code.
       */
      var template = this.template,
          templateFunc = null;

      if (typeof template === 'string') {
        var tmpl = env.getTemplate(template);
        var templateFunc = function(ctx) {
          return tmpl.render(ctx);
        };
        this.constructor.prototype.template = templateFunc;
      } else {
        templateFunc = template;
      }

      return templateFunc;
    },

    render: function() {
      var html, $html, templateFunc;
      if (this.disposed) {
        return false;
      }
      templateFunc = this.getTemplateFunction();
      if (typeof templateFunc === 'function') {
        html = templateFunc(this.getTemplateData());
        // Respect noWrap option
        if (!this.noWrap) {
          this.$el.html(html);
        } else {
          $html = $(html);
          if ($html.length > 1) {
            throw new Error('There must be a single top-level element when ' +
                            'using `noWrap`');
          }
          this.setElement($html, true);
        }
      }
      if (this.bindings && this.model) {
        this.stickit();
      }
    },

  });

  return View;
});
