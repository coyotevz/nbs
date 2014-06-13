define([
  'underscore',
  'chaplin',
  'models/base/model'
], function(_, Chaplin, Model) {
  "use strict";
  var config = window.config || {};

  var Collection = Chaplin.Collection.extend({
    model: Model,

    // Mixin a synchronization state machine.
    initialize: function() {
      _.extend(this, Chaplin.SyncMachine);
      Chaplin.Collection.prototype.initialize.apply(this, arguments);
      this.on('request', this.beginSync);
      this.on('sync', this.finishSync);
      this.on('error', this.unsync);
    },

    url: function() {
      var base;
      if (!this.urlRoot) {
        throw new Error('A "urlRoot" property must be specified on Collection');
      }

      if (this.parents && this.parents.length == 1) {
        base = _.result(this.parents[0], 'url');
      } else {
        base = config.urlRoot || '';
      }
      return base.replace(/([^\/])$/, '$1/') + encodeURIComponent(this.urlRoot);
    },
  });

  return Collection;
});
