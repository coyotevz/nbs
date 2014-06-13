define([
  'backbone',
  'underscore',
  'chaplin',
  'backbone.trackit',
  'backbone.validation',
  'backbone.associations',
], function(Backbone, _, Chaplin) {
  "use strict";
  var config = window.config || {};

  var Model = Chaplin.Model.extend({

    url: function() {
      var base;

      if (this.collection) {
        base = _.result(this.collection, 'url');
      } else if (this.urlRoot) {
        base = (config.urlRoot || '') + this.urlRoot;
      } else {
        throw new Error('A "urlRoot" property must be specified');
      }
      if (this.isNew()) return base;
      return base.replace(/([^\/])$/, '$1/') + encodeURIComponent(this.id);
    },

    isAttributeValid: function(attr) {
      var errors = _.extend({}, this.validationError),
          invalidAttrs = {},
          error,
          isValid;

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
