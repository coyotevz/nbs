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

    hasStoredChange: function() {
      return _.isObject(this.getPatch()) ? true : false;
    },

    getPatch: function() {
      if (!this._serverAttributes) return false;
      var attrs = this._serverAttributes,
          diff = {};

      _.each(this.attributes, function(val, key) {
        if (!_.isEqual(val, attrs[key])) diff[key] = val;
      });

      if (!_.isEmpty(diff)) return diff;
      return false;
    },

    isAttributeValid: function(attr) {
      var errors = _.extend({}, this.validationError),
          invalidAttrs = {},
          error,
          isValid;

      console.log('calling isAttributeValid() on %s', attr);

      if (attr === true) {
        this.validate();
        return this.validation ? this._isValid : true;
      }

      if (_.isString(attr)) {
        error = this.preValidate(attr, this.get(attr));
        if (error) {
          invalidAttrs[attr] = error;
        } else {
          delete errors[attr];
        }
      }

      if (_.isArray(attr)) {
        _.each(attr, function(key) {
          error = this.preValidate(key, this.get(key));
          if (error) {
            invalidAttrs[key] = error;
          } else {
            delete errors[key];
          }
        });
      }

      if (!_.isEmpty(invalidAttrs)) {
        // Restore validationError
        this.validationError = _.extend(errors, invalidAttrs);
        isValid = false;
      } else {
        this.validationError = _.isEmpty(errors) ? null : errors;
        isValid = true;
      }

      this._isValid = this.validationError === null ? true : false;

      return isValid;
    },

  }).extend(Chaplin.EventBroker);

  return Model;
});
