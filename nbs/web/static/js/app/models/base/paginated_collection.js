define([
  'underscore',
  'models/base/model',
  'models/base/collection'
], function(_, Model, Collection) {
  "use strict";

  var PaginatedCollection = Collection.extend({

    model: Model,

    // Objects on page
    page: 0,
    num_pages: 1,
    num_results: null,

    // is this collection fully loaded?
    hasMore: function() {
      return this.num_results < this.models.length;
    },

    fetch: function(options) {
      var collection = this,
          data = {};

      options = options ? _.clone(options) : {};
      options.increase = options.increase ? options.increase : false;
      // FIXME: For Pager debug only
      data.per_page = 8;

      if (options.increase) {
        data.page = !this.page ? undefined : this.page < this.num_pages ? this.page + 1 : undefined;
      } else {
        data.page = !this.page ? undefined: this.page;
      }

      options.data = _.defaults(options.data ? options.data : {}, data);

      return Collection.prototype.fetch.call(collection, options);
    },

    parse: function(data) {
      var objects = data.objects || data;

      this.num_results = data.num_results || data.length;
      this.num_pages = data.num_pages || 1;
      this.page = data.page || 1;
      if (this.num_results < this.models.length + objects.length) {
        this.trigger("pagination", "load");
      } else {
        this.trigger("pagination", "complete");
      }
      return objects;
    },

  });

  return PaginatedCollection;
});
