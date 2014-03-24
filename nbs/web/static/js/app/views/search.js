define([
  'underscore',
  'views/base/view',
  'views/base/collection_view',
], function(_, View, CollectionView) {
  "use strict";

  var SearchDialogRowView = View.extend({
    template: 'pos/search_item_row.html',
    tagName: 'tr',
    className: 'search-result-row',
  });

  var SearchDialogView = CollectionView.extend({
    optionNames: CollectionView.prototype.optionNames.concat([
      'dialog', 'template', 'firstChar', 'currentFocus', 'delay',
    ]),
    term: null,
    timer: null,
    delay: 300,
    listSelector: 'tbody',
    itemView: SearchDialogRowView,
    animationDuration: 0,

    // Internal properties
    _selected_idx: null,

    listen: {
      'show': function() {
        this.$('[name=term]').focus().val(this.firstChar || '');
      },
      'beforeReposition': function() {
        this.resize();
      },
      'fetched': function(collection) {
        this.updateTerms(collection.models);
        this.select(0);
      },
    },

    render: function() {
      this.collection.reset();
      SearchDialogView.__super__.render.apply(this, arguments);
      this.delegate('keydown', '[name=term]', this.onTermKeydown);
      this.delegate('keyup', '[name=term]', this.onTermKeyup);
      this.$term = this.$('[name=term]');
      this.dialog.$d.addClass('search-dialog');
      this.$('table').fixHeader();
    },

    resize: function() {
      var availableHeight = this.$el.height() - this.$('.modal-header').outerHeight(true) - this.$('.modal-footer').outerHeight(true);
      this.$('.search-container').height(availableHeight);
    },

    onTermKeydown: function(evt) {
      var idx,
          k = $.keycode(evt);

      switch(k) {
        case 'esc':
          this.selected = null;
          this.dialog.close();
          return false;
        case 'down':
          this.moveSelect(+1);
          return false;
        case 'up':
          this.moveSelect(-1);
          return false;
        case 'return':
          if (this.selected) this.dialog.close();
          return false;
      }
    },

    onTermKeyup: function(evt) {
      var terms = this.$term.val().trim();
      if (this.term !== terms) {
        this.term = terms;
        this.collection.cancel();
        if (this.timer) clearTimeout(this.timer);
        if (terms !== '') {
          var search = _.bind(this.search, this, terms);
          this.timer = _.delay(search, this.delay);
        } else {
          this.collection.reset();
        }
      }
    },

    search: function() {
      throw new Error('You must implement SearchDialog.search() method');
    },

    updateTerms: function() {
      throw new Error('You must implement SearchDialog.updateTerms() method');
    },

    moveSelect: function(m) {
      var idx = (this._selected_idx || 0) + m;
      if (idx >= 0 && idx < this.collection.length) {
        this.select(idx);
      }
    },

    select: function(idx) {
      var itemView, selected;
      if (this._selected_idx !== null && this.selected) {
        itemView = this.subview('itemView:'+this.selected.cid);
        if (itemView) itemView.$el.removeClass('selected');
      }
      selected = this.collection.at(idx);
      if (selected) {
        itemView = this.subview('itemView:'+selected.cid);
        if (itemView) {
          itemView.$el.addClass('selected');
          this.checkScrollFor(itemView.$el);
        }
        this._selected_idx = idx;
      } else {
        this._selected_idx = null;
      }
      this.selected = selected;
    },

    checkScrollFor: function(el) {
      var container = this.$('.search-container'),
          gap = this.$('.search-results thead').height(),
          cellTop = el.offset().top - gap,
          cellBottom = cellTop + el.outerHeight() + gap,
          containerTop = container.offset().top,
          containerBottom = containerTop + container.outerHeight(),
          scrollTop = container.scrollTop();

      if (cellTop < containerTop) {
        container.scrollTop(scrollTop - (containerTop - cellTop));
      } else if (cellBottom > containerBottom) {
        container.scrollTop(scrollTop + (cellBottom - containerBottom));
      }

    },

  });

  SearchDialogView.SearchDialogRowView = SearchDialogRowView;
  return SearchDialogView;

});
