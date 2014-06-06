/*
 * backbone.trackit - Smart change tracks
 *
 * Based on https://github.com/NYTimes/backbone.trackit
 * MIT License
 * Copyright (c) 2013 The New York Times, CMS Group, Matthew DeLambo <delambo@gmai.com>
 * Copyright (c) 2014 Augusto Roccasalva <augusto@rioplomo.com.ar>
 */

define([
  'underscore',
  'backbone',
], function(_, Backbone) {
  "use strict";

  // Backbone.Model API
  // ------------------

  _.extend(Backbone.Model.prototype, {

    _trackingChanges: false,
    _originalAttrs: {},
    _unsavedChanges: {},

    // Opt in to tracking attribute changes
    // between saves.
    startTracking: function() {
      this._trackingChanges = true;
      this._resetTracking();
      return this;
    },

    // Resets the default tracking values
    // and stops tracking attribute changes
    stopTracking: function() {
      this._trackingChanges = false;
      this._originalAttrs = {};
      this._unsavedChanges = {};
      return this;
    },

    isTracked: function() {
      return this._trackingChanges;
    },

    isChanged: function() {
      return !_.isEmpty(this._unsavedChanges);
    },

    // Gets rid of accrued changes and resets state.
    restartTracking: function() {
      this._resetTracking();
      return this;
    },

    // Restores this model's attributes to their original values since tracking
    // started, the last save, or last restart.
    resetAttributes: function() {
      if (!this._trackingChanges) return;
      this.attributes = this._originalAttrs;
      this._resetTracking();
      return this;
    },

    // Symmetric to Bakcbone's * `model.changedAttributes()`, except that this
    // returns a has of the model's attributes that have changed since the last
    // save, or `false` if there are none.
    // Like `changedAttributes`, an external attributes hash can be passed in,
    // returning the attributes in that hash which differ from the model.
    unsavedAttributes: function(attrs) {
      if (!attrs) return _.isEmpty(this._unsavedChanges) ? false : _.clone(this._unsavedChanges);
      var val, changed = false, old = this._unsavedChanges;
      for (var attr in attrs) {
        if (_.isEqual(old[attr], (val = attrs[attr]))) continue;
        (changed || (changed = {}))[attr] = val;
      }
      return changed;
    },

    _resetTracking: function() {
      this._originalAttrs = _.clone(this.attributes);
      this._unsavedChanges = {};
    },
  });

  // Wrap `model.set()` and update the internal unsaved changes record keeping.
  Backbone.Model.prototype.set = _.wrap(Backbone.Model.prototype.set, function(oldSet, key, val, options) {
    var attrs, ret;

    if (key == null) return this;
    // Handle both `"key", "value"` and `{key: value}` -style arguments.
    if (typeof key === 'object') {
      attrs = key;
      options = val;
    } else {
      (attrs = {})[key] = val;
    }
    options || (options = {});

    // Delegate to Backbone's set.
    ret = oldSet.call(this, attrs, options);

    if (this._trackingChanges && !options.silent) {
      _.each(attrs, _.bind(function(val, key) {
        if (_.isEqual(this._originalAttrs[key], val))
          delete this._unsavedChanges[key];
        else
          this._unsavedChanges[key] = val;
      }, this));
    }
    return ret;
  });

  // Intercept `model.save()` and reset tracking/unsaved changes if it was
  // successfull.
  Backbone.sync = _.wrap(Backbone.sync, function(oldSync, method, model, options) {
    options || (options = {});

    if (method == 'update') {
      options.success = _.wrap(options.success, _.bind(function(oldSuccess, data, textStatus, jqXHR) {
        var ret;
        if (oldSuccess) ret = oldSuccess.call(this, data, textStatus, jqXHR);
        if (model._trackingChanges) {
          model._resetTracking();
        }
        return ret;
      }, this));
    }
    return oldSync(method, model, options);
  });

  // Don't return anything
});
