define([
  'chaplin',
  'models/base/model'
], function(Chaplin, Model) {
  "use strict";

  var Collection = Chaplin.Collection.extend({
    model: Model,

    // Mixin a synchronization state machine.
    initialize: function() {
      _.extend(this, Chaplin.SyncMachine);
      Collection.__super__.initialize.apply(this, arguments);
      this.on('request', this.beginSync);
      this.on('sync', this.finishSync);
      this.on('error', this.unsync);
    },
  });

  return Collection;
});
