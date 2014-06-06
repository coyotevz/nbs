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

  unsaved: {},
    _trackingChanges: false,
    _originalAttrs: {},
    _unsavedChanges: {},

    // Opt in to tracking attribute changes
    // between saves.
    startTracking: function() {
      this._trackingChanges = true;
      return this;
    },

    // Resets the default tracking values
    // and stops tracking attribute changes
    stopTracking: function() {
      this._trackingChanges = false;
      return this;
    },

    isTracked: function() {
      return this._trackingChanges;
    },

    isChanged: function() {
    },

    // Gets rid of accrued changes and resets state.
    restartTracking: function() {
      return this;
    },

    // Restores this model's attributes to their original values since tracking
    // started, the last save, or last restart.
    resetAttributes: function() {
      return this;
    },

    // Symmetric to Bakcbone's * `model.changedAttributes()`, except that this
    // returns a has of the model's attributes that have changed since the last
    // save, or `false` if there are none.
    // Like `changedAttributes`, an external attributes hash can be passed in,
    // returning the attributes in that hash which differ from the model.
    unsavedAttributes: function(attrs) {

    },
  });

  // Wrap `model.set()` and update the internal unsaved changes record keeping.
  Backbone.Model.prototype.set = _.wrap(Backbone.Model.prototype.set, function(oldSet, key, val, options) {
  })

  // Don't return anything
});
