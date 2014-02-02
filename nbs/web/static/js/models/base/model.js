define([
  'backbone',
  'chaplin',
  'backbone.relational',
  'backbone.validation',
], function(Backbone, Chaplin) {
  "use strict";

  var Model = Backbone.RelationalModel.extend({

    dispose: function() {
      if (this.disposed) return;
      this.trigger('relational:unregister', this, this.collection);
      return Chaplin.Model.prototype.dispose.call(this);
    },

    // Methods & properties inherited from Chaplin.Model
    getAttributes: Chaplin.Model.prototype.getAttributes,
    serialize: Chaplin.Model.prototype.serialize,
    disposed: Chaplin.Model.prototype.disposed,

    fetch: function(options) {
      options = options ? _.clone(options) : {};
      var success = options.success;
      options.success = function(model, resp, options) {
        model._serverAttributes = resp;
        if (success) success(model, resp, options);
      }
      // FIXME: Remove next line!!
      window.current_model = this;
      return Backbone.RelationalModel.prototype.fetch.call(this, options);
    },

    save: function(key, val, options) {
      console.debug("model save");
      return Backbone.RelationalModel.prototype.fetch.call(this, key, val, options);
    },

    hasStoredChange: function() {
      if (!this._serverAttributes) return false;
    },

  }).extend(Chaplin.EventBroker);

  return Model;
});
