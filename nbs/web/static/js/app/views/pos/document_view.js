define([
  'jquery',
  'views/base/view',
  'views/base/collection_view',
  'views/pos/base_row_view',
  'models/document',
  'models/document_item',
], function($, View, CollectionView, BaseRowView, Document, DocumentItem) {
  "use strict";

  var AppenderView = BaseRowView.extend({
    id: 'appender',
    listen: {
      'row-done': 'onRowDone',
    },

    onRowDone: function(target) {
      this.trigger('append', this.model.clone());
      this.model.clear();
      this.$('.composed-field input').focus().val("");
    },
  });

  var ItemView = BaseRowView.extend({
    className: 'item-row',

    listen: {
      'row-done': 'onRowDone',
    },

    onRowDone: function(target) {
      this.$el.next().find('input:first').focus();
    },
  });

  var ItemsView = CollectionView.extend({
    template: 'pos/document_items.html',
    noWrap: true,
    listSelector: 'tbody',
    itemView: ItemView,
    animationDuration: 0,
  });

  var DocumentView = View.extend({
    noWrap: true,

    bindings: {
      '#total': {
        observe: 'total',
        onGet: $.numeric,
      }
    },

    render: function() {
      DocumentView.__super__.render.apply(this, arguments);
      this.initSubviews();
    },

    initSubviews: function() {
      var itemsView, appenderView, header, footer;

      // items list
      itemsView = new ItemsView({
        region: 'body',
        collection: this.model.get('items')
      });
      this.subview('itemslist', itemsView);

      // appender row
      appenderView = new AppenderView({
        model: new DocumentItem()
      });
      this.listenTo(appenderView, 'append', this.onAppend);
      this.subview('appender', appenderView);
      appenderView.$('input:first').focus();

      // header

      // footer
    },

    onAppend: function(item) {
      this.model.get('items').add(item);
    },

    resizeItemlist: function() {
      console.log('time for resize...');
    },
  });

  var DocumentView_old = View.extend({

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

        var fs = ($t.children('table').outerHeight() - $t.scrollTop()) > $t.height();
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
