define([
  'chaplin',
  'views/base/view',
], function(Chaplin, View) {
  "use strict";

  var ProductItemView = View.extend({
    template: 'admin/product/item.html',
    tagName: 'tr', // we can't insert <tr> element inside <div> with native code
    selected: false,

    initialize: function() {
      ProductItemView.__super__.initialize.apply(this, arguments);
      this.delegate('change', 'input[type=checkbox]', this.checked);
      this.delegate('click', 'td', this.open);
    },

    checked: function(evt) {
      this.selected = this.$(evt.target).is(':checked');
      this.$el.toggleClass('selected', this.selected);
      this.trigger('selected', this.selected);
    },

    open: function(evt) {
      if (this.$(evt.target).is('input[type=checkbox]')) return this.checked(evt);
      Chaplin.utils.redirectTo({name: 'product_show'}, {id: this.model.id})
    },

  });

  return ProductItemView;
});
