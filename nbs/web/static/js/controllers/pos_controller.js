define([
  'chaplin',
  'views/pos/document_view',
], function(Chaplin, DocumentView) {
  "use strict";

  var PosController = Chaplin.Controller.extend({

    title: 'Point of Sale',

    index: function(params) {
      this.view = new DocumentView();
    }

  });

  return PosController;
});
