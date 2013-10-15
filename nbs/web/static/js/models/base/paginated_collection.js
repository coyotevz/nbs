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

    // multiple call of fetch will increase in page count
    fetch: function(options) {
      var collection = this;

      options = options ? _.clone(options) : {};
      options.data = options.data ? options.data : {};
      if (!options.reset) {
        options.data["page"] = !this.page ? undefined : this.page < this.num_pages ? this.page + 1 : undefined;
      }

      return PaginatedCollection.__super__.fetch.call(collection, options);
    },

    parse: function(data) {
      var objects = data.objects || data;

      this.num_results = data.num_results || data.length;
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