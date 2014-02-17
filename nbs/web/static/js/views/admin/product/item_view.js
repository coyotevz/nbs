define([
  'underscore',
  'chaplin',
  'views/base/view',
], function(_, Chaplin, View) {
  "use strict";

  var ProductItemView = View.extend({
    template: 'admin/product/item.html',
    tagName: 'tr', // we can't insert <tr> element inside <div> with native code
    selected: false,
    optionNames: View.prototype.optionNames.concat(['parent']),

    initialize: function() {
      ProductItemView.__super__.initialize.apply(this, arguments);
      this.delegate('click', '.control-checkbox', this.onCheckboxClick);
      this.delegate('click', 'td', this.select);
    },

    render: function() {
      ProductItemView.__super__.render.apply(this, arguments);
      this.$checkbox = this.$('.control-checkbox');
    },

    select: function() {
      this.parent.unselectAll();
      this.toggleSelect(true);
    },

    onCheckboxClick: function(evt) {
      evt.preventDefault();
      this.toggleSelect();
      return false;
    },

    toggleSelect: function(opt) {
      opt = (opt !== undefined) ? Boolean(opt) : !this.selected;
      if (opt !== this.selected) {
        this.$checkbox.toggleClass('control-checkbox-checked', opt);
        this.$el.toggleClass('selected', opt);
        this.selected = opt;
        this.trigger({true: 'selected', false: 'unselected'}[opt], this);
      }
    },

  });

  return ProductItemView;
});
