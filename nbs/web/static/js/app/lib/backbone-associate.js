/*
 * backbone-associate - Relational for Backbone
 *
 * Based on http://github.com/dhruvaray/backbone-associations
 * MIT License
 * Copyright(c) 2013 Dhryva Ray, Jaynti Kanani, Persistent Systems Ltd.
 * Copyright(c) 2014 Augusto Roccasalva
 */

define([
  'underscore',
  'backbone',
], function(_, Backbone) {
  "use strict";

  var deepExtend = function() {
    var merged = {};
    for (var i = 0; i < arguments.length; i++) {
      _.merge(merged, arguments[i]);
    };
    return merged;
  };

  Backbone.One = "One";
  Backbone.Many = "Many";
  Backbone.Self = "Self";

  // Backbone.Model API
  // ------------------

  // Basic rule for implementation: (to avoid infinite recursion)
  //  if you need to call super method inside overwrited method implement that
  //  ModelProto.<method> = _.wrap(ModelProto.<method>, function(<method>, [args]) {};
  //  else implement that in _.extend() style

  var Model = Backbone.Model;

  _.extend(Model.prototype, {

    relations: undefined,

    // Override constructor
    // Suport having nested defaults by using _.deepExtend instead of _.extend
    constructor: function(attributes, options) {
      var defaults;
      var attrs = attributes || {};
      this.cid = _.uniqueId('c');
      this.attributes = {};
      if (options && options.collection) this.collection = options.collection;
      if (options && options.parse) attrs = this.parse(attrs, options) || {};
      if (defaults = _.result(this, 'defaults'))
        attrs = deepExtend(defaults, attrs);
      this.set(attrs, options);
      this.changed = {}
      this.initialize.apply(this, arguments);
    },

    activateRelations: function() {
      console.log('activating relations...');
    },

  });

  Model.prototype.initialize = _.wrap(Model.prototype.initialize, function(init) {
    init.apply(this, arguments);
    if (this.relations)
      this.activateRelations();
  });

  // Don't return anything
});
