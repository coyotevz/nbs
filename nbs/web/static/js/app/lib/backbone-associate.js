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

  Backbone.One = "One";
  Backbone.Many = "Many";
  Backbone.Self = "Self";

  // Backbone.Model API
  // ------------------

  // Basic rule for implementation: (to avoid infinite recursion)
  //  if you need to call super method inside overwrited method implement that
  //  ModelProto.<method> = _.wrap(ModelProto.<method>, function(<method>, [args]) {};
  //  else implement that in _.extend() style

  var ModelProto = Backbone.Model.prototype;

  _.extend(ModelProto, {

    relations: undefined,

    activateRelations: function() {
      console.log('activating relations...');
    },

  });

  ModelProto.initialize = _.wrap(ModelProto.initialize, function(origInitialize) {
    origInitialize.apply(this, arguments);
    if (this.relations)
      this.activateRelations();
  });


  // Don't return anything
});
