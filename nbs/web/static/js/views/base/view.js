define([
  'jquery',
  'underscore',
  'chaplin',
  'templates/env',
  'backbone.stickit',
], function($, _, Chaplin, env) {
  "use strict";

  var View = Chaplin.View.extend({
    autoRender: true,
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
      View.__super__.render.apply(this, arguments);
      if (this.bindings && this.model) {
        this.stickit();
      }
    },

    /* extra method, borrowed from controller */
    compose: function(name) {
      var method;
      method = arguments.length === 1 ? 'retrieve': 'compose';
      return Chaplin.mediator.execute.apply(Chaplin.mediator, ['composer:' + method].concat(([].slice.call(arguments))));
    },

  });

  return View;
});
