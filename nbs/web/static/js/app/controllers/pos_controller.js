define([
  'chaplin',
  'views/standard_view',
  'views/dialog',
  'models/document',
  'views/pos/document_view',
], function(Chaplin,
            StandardView,
            DialogView,
            Document,
            DocumentView) {
  "use strict";

  var PosController = Chaplin.Controller.extend({
    title: 'Point of Sale',

    beforeAction: function(params, route) {
      this.reuse('main', StandardView, {region: 'main'});
      this.reuse('dialog', DialogView, {region: 'main'});
    },

    create: function(params) {
      var model = new Document();
      this.view = new DocumentView({
        model: model,
        region: 'body',
      });
      window.view = this.view;
    },

    edit: function(params) {
      var model = new Document({id: params.id});
      model.fetch();
      this.view = new DocumentView({
        model: model,
        region: 'body',
      });
    },
  });

  return PosController;
});
