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
      this.delegate('click', 'td', this.select);
    },

    checked: function(target) {
      this.selected = this.$(target).is(':checked');
      this.$el.toggleClass('selected', this.selected);
      this.trigger('selected', this.selected);
    },

    select: function(evt) {
      console.log('select:', this.$el, evt);
      this.checked(this.$('input[type="checkbox"]'));
      //if (this.$(evt.target).is('input[type=checkbox]')) return this.checked(evt);
    },

  });

  return ProductItemView;
});
