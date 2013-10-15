define([
  'jquery',
  'views/base/view',
  'views/pos/appender_view',
  'views/pos/items_view',
  'models/document',
], function($, View, AppenderView, ItemsView, Document) {
  "use strict";

  var DocumentView = View.extend({

    el: 'div#pos',
    autoRender: true,

    regions: {
      'header': 'header',
      'body': '#content',
      'footer': 'footer',
    },

    bindings: {
      '#total': {
        observe: 'total',
        onGet: $.numeric
      }
    },

    initialize: function() {
      DocumentView.__super__.initialize.apply(this, arguments);
      this.model = new Document();

      var appenderview = new AppenderView({model: this.model.appender});
      this.listenTo(appenderview, 'append', this.onAppend);
      this.subview('appender', appenderview);

      this.subview('itemslist', new ItemsView({
        collection: this.model.items
      }));

      this.setupHtml();

      //_.bindAll(this, "onAppend");
    },

    setupHtml: function() {
      // First set height to #content base on header and footer elements
      this.$('#content').css({
        'top': this.$('header').outerHeight(),
        'bottom': this.$('footer').outerHeight(),
        'visibility': 'visible', // Avoid flickr unpositioned element
      });

      // Set focus on last item-row
      $('.item-list tr#appender input:first').focus();
    },

    onAppend: function(model) {
      this.model.items.add(model);
    },
  });

  return DocumentView;
});
