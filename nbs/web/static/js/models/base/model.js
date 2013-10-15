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

  }).extend(Chaplin.EventBroker);

  // TODO: remove next line
  window.Model = Model;
  return Model;
});
