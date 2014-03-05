define([
  'jquery',
  'views/base/view',
  'views/base/collection_view',
  'views/pos/base_row_view',
  'models/document',
  'models/document_item',
], function($, View, CollectionView, BaseRowView, Document, DocumentItem) {
  "use strict";

  var HeaderView = View.extend({
    noWrap: true,
  });

  var AppenderView = BaseRowView.extend({
    id: 'appender',
    listen: {
      'row-done': 'onRowDone',
    },

    initialize: function() {
      AppenderView.__super__.initialize.apply(this, arguments);
      this.model.clear();
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

  var FooterView = View.extend({
    noWrap: true,
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

      // header
      header = new HeaderView({
        model: this.model,
        region: 'header',
      });
      this.subview('header', header);

      // footer
      footer = new FooterView({
        model: this.model,
        region: 'footer',
      });
      this.subview('footer', footer);

      this.$el.css({
        'top': header.$el.outerHeight(),
        'bottom': footer.$el.outerHeight(),
        'visibility': 'visible',
      });
      appenderView.$('input:first').focus();

      /*
       * Scroll event handler to signal list scroll
       *
      .scroll(function(evt) {
        var $t = $(evt.target);

        var hs = $t.scrollTop() > 0;
        $t.prev().toggleClass("shadowed", hs);

        var fs = ($t.children('table').outerHeight() - $t.scrollTop()) > $t.height();
        $t.next().toggleClass("shadowed", fs);
      })
       */
    },

    onAppend: function(item) {
      this.model.get('items').add(item);
    },

    resizeItemlist: function() {
      console.log('time for resize...');
    },
  });

  return DocumentView;
});
