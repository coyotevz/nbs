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

    initialize: function() {
      AppenderView.__super__.initialize.apply(this, arguments);
      this.listenTo(this, 'row-done', this.onRowDone);
    },

    onRowDone: function(target) {
      var model = this.model;
      console.log('try to detach:', this.model && this.model.get('sku'));
      this.setModel(new DocumentItem());
      this.trigger('append', model);
      this.$('.composed-field input').focus().val("");
    },

    setModel: function(model) {

      // clear model
      if (this.model) {
        //this.undelegate();          // chaplinjs specific
        this.stopListening();
        this.unstickit(this.model);

        //this.stopListening(this.model);
        //this.model.unbind();
        //this.model.stopListening();
        //this.unstickit(this.model);
      }

      // set new model and call initialize
      this.model = model;
      this.delegateEvents();        // calls undelegateEvents() internally
      this.delegateListeners();     // overriden in chaplinjs
      this.listenTo(this.model, 'dispose', this.dispose); // from chaplinjs
      this.listenTo(this, 'row-done', this.onRowDone);
      this.stickit(this.model);
    },

    onRemoveModel: function() {
      this.$('.cell-unit-price span, .cell-total-price span, .container-description').css({
        'visibility': 'hidden'
      });
    },
  });

  var ItemView = BaseRowView.extend({
    className: 'item-row',

    initialize: function() {
      ItemView.__super__.initialize.apply(this, arguments);
      this.listenTo(this, 'row-done', this.onRowDone);
      this.listenTo(this, 'remove', this.onRemove);
    },

    onRowDone: function(target) {
      this.$el.next().find('input:first').focus();
    },

    onRemove: function(target) {
      var m = target.model;
      target.$el.next().find('input:first').focus();
      m.collection.remove(m);
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
    template: 'pos/document_footer.html',

    bindings: {
      '#total': {
        observe: 'total',
        onGet: $.numeric,
      }
    }
  });

  var DocumentView = View.extend({
    noWrap: true,

    render: function() {
      DocumentView.__super__.render.apply(this, arguments);
      this.delegate('scroll', this.onScroll);
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
      window.items = this.model.get('items');

      // appender row
      appenderView = new AppenderView({
        model: new DocumentItem()
      });
      window.appender = appenderView;
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
        'bottom': footer.$el.outerHeight() + 3,
        'visibility': 'visible',
      });
      appenderView.$('input:first').focus();
    },

    onAppend: function(item) {
      this.model.get('items').add(item);
    },

    onRemove: function() {
      console.log('onRemove handler:', arguments);
    },

    onScroll: function(evt) {
      var hs, fs, $t = $(evt.target);
      hs = $t.scrollTop() > 0;
      $t.prev().toggleClass("shadowed", hs);
      fs = ($t.find('table').outerHeight() - $t.scrollTop() - 3) > $t.height();
      $t.next().toggleClass("shadowed", fs);
    },
  });

  return DocumentView;
});
