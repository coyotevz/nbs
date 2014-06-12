define([
  'backbone',
  'underscore',
  'chaplin',
  'backbone.trackit',
  'backbone.validation',
  'backbone.associations',
], function(Backbone, _, Chaplin) {
  "use strict";

  var Model = Chaplin.Model.extend({

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
