define([
  'underscore',
  'chaplin',
  'views/base/view',
  'views/toolbar',
], function(_, Chaplin, View, Toolbar) {
  "use strict";

  var EditToolbar = Toolbar.extend({
    template: 'admin/product/edit_toolbar.html',

    events: {
      'click [name=save]': 'saveChanges',
    },

    saveChanges: function() {
      var model = this.view.model;
      model.save(model.getPatch(), {patch: true, validate: false});
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
        onSet: function(val) {
          return val.replace('.','').replace(',','.');
        }
      },
    },

    render: function(params) {
      ProductEditView.__super__.render.apply(this, arguments);
      this.initSubviews();
      this.delegate('click', '[name=save]', this.saveChanges);
      this.delegate('click', '[name=cancel]', this.cancelChanges);
    },

    attach: function() {
      ProductEditView.__super__.attach.apply(this, arguments);
      this.$('.autogrow').autogrow();
      this.$('[name=sku]').focus().select();
    },

    initSubviews: function() {
      var toolbar;
      //toolbar = new EditToolbar({region: 'toolbar', view: this});
      //this.subview('toolbar', toolbar);
    },

    saveChanges: function(evt) {
      this.model.save(this.model.getPatch(), {patch: true, validate: false});
    },

    cancelChanges: function() {
      console.log('cancelling!');
      window.history.back();
    },

    onModelChange: function(model, options) {
      window.current_model = model;
      if (options.stickitChange) {
        var isValid = model.isValid(options.stickitChange.observe),
            enabled = isValid && model.hasStoredChange() && _.isEmpty(model.validationError || {});
        //this.subview('toolbar').$('[name=save]').attr('disabled', !enabled);
      }
    },

  });

  return ProductEditView;
});
