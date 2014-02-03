define([
  'backbone',
  'underscore',
  'chaplin',
  'backbone.relational',
  'backbone.validation',
], function(Backbone, _, Chaplin) {
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
        // save a copy of recently fetched attributes
        model._serverAttributes = _.clone(model.attributes);
        if (success) success(model, resp, options);
      }
      return Backbone.RelationalModel.prototype.fetch.call(this, options);
    },

    save: function(key, val, options) {
      console.debug("model save");
      return Backbone.RelationalModel.prototype.fetch.call(this, key, val, options);
    },

    hasStoredChange: function() {
      return _.isObject(this.getPatch()) ? true : false;
    },

    getPatch: function() {
      if (!this._serverAttributes) return false;
      var diff = {},
          keys = _.keys(this.attributes),
          self = this;
      _.each(keys, function(key) {
        var orig_val = self._serverAttributes[key],
            new_val = self.get(key);
        if (!_.isEqual(orig_val, new_val)) diff[key] = new_val;
      });
      if (!_.isEmpty(diff)) return diff;
      return false;
    },

  }).extend(Chaplin.EventBroker);

  return Model;
});
