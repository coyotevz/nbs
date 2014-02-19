define([
  'views/base/view',
], function(View) {
  "use strict";

  var ProductItemView = View.extend({
    template: 'admin/product/item.html',
    tagName: 'tr', // we can't insert <tr> element inside <div> with native code
    selected: false,
    optionNames: View.prototype.optionNames.concat(['parent']),

    initialize: function() {
      ProductItemView.__super__.initialize.apply(this, arguments);
      this.delegate('click', '.cell-checkbox', this.onCheckboxClick);
      this.delegate('click', 'td:not(.cell-checkbox)', this.select);
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

    toggleSelect: function(opt, trigger) {
      opt = (opt !== undefined) ? Boolean(opt) : !this.selected;
      trigger = (trigger !== undefined) ? Boolean(trigger) : true;
      if (opt !== this.selected) {
        this.$checkbox.toggleClass('control-checkbox-checked', opt);
        this.$el.toggleClass('selected', opt);
        this.selected = opt;
        if (trigger) {
          this.trigger({true: 'selected', false: 'unselected'}[opt], this);
        }
      }
    },

  });

  return ProductItemView;
});
