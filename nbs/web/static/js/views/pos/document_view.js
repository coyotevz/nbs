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
      console.log("TODO: DocumentView needs to be rewrited");
      this.model = new Document();

      var appenderview = new AppenderView({model: this.model.appender});
      this.listenTo(appenderview, 'append', this.onAppend);
      this.subview('appender', appenderview);

      this.subview('itemslist', new ItemsView({
        collection: this.model.items
      }));

      this.setupHtml();
    },

    setupHtml: function() {
      // First set height to #content base on header and footer elements
      this.$('#content').css({
        'top': this.$('header').outerHeight(),
        'bottom': this.$('footer').outerHeight(),
        'visibility': 'visible', // Avoid flickr unpositioned element
      }).scroll(function(evt) {
        var $t = $(evt.target);

        var hs = $t.scrollTop() > 0;
        $t.prev().toggleClass("shadowed", hs);

        var fs = ($t.children('table').outerHeight() - $t.scrollTop()) > $t.height()
        $t.next().toggleClass("shadowed", fs);
      });

      // Set focus on last item-row
      $('.item-list tr#appender input:first').focus();

      // Only for test
      $('#modal').modal({
        show: false,
        backdrop: "static",
      });
    },

    onAppend: function(model) {
      this.model.items.add(model);
    },
  });

  return DocumentView;
});
