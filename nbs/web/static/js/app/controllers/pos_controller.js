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

    index: function(params) {
      var model = new Document();
      model.fetch();
      this.view = new DocumentView({
        model: model,
        region: 'body',
      });
    }
  });

  return PosController;
});
