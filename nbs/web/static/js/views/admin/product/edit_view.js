define([
  'chaplin',
  'views/base/view',
  'views/toolbar',
], function(Chaplin, View, Toolbar) {
  "use strict";

  var EditToolbar = Toolbar.extend({
    template: 'admin/product/edit_toolbar.html',

    events: {
      'click [name=save]': 'saveChanges',
    },

    saveChanges: function() {
      console.log('save changes');
    },

  });

  var ProductEditView = View.extend({
    template: 'admin/product/edit.html',
    noWrap: true,

    listen: {
      'change model': 'onModelChange',
    },

    bindings: {
      '[name=sku]': 'sku',
      '[name=description]': 'description',
      '[name=price]': {
        observe: 'price',
        onGet: $.numeric,
      },
    },

    render: function(params) {
      ProductEditView.__super__.render.apply(this, arguments);
      this.initSubviews();
    },

    attach: function() {
      ProductEditView.__super__.attach.apply(this, arguments);
      this.$('.autogrow').autogrow();
      this.$('[name=sku]').focus().select();
    },

    initSubviews: function() {
      var toolbar, sidebar;
      toolbar = new EditToolbar({region: 'toolbar', view: this});
      this.subview('toolbar', toolbar);
    },

    onModelChange: function(model, options) {
      if (options.stickitChange) {
        this.subview('toolbar').$('[name=save]').attr('disabled', false);
      }
    },

  });

  return ProductEditView;
});
