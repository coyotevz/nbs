define([
  'underscore',
  'backbone',
  'models/base/paginated_collection',
], function(_, Backbone, PaginatedCollection) {
  "use strict";

  var urlError = function() {
    throw new Error('A "url" property or function must be specified');
  };
  /*
   * Strongly based on https://github.com/tornado-utils/tornado-backbone
   * project
   */

  /*
   * Call this:
   * var result = new Search(Product, {sku: '20150'});
   * var single_object = result.one() // This trigger request to server
   * var multiple_objects = result.many() // This trigger request to server
   *
   * Other searches condition:
   * ~~~~~~~~~~~~~~~~~~~~~~~~~
   * 'eq': {sku: '20150'} // Exactly equal (sku=='20150')
   * 'like': {sku: '201%'}.
   * new Search(Product, {sku: {like: '201%'}})
   */

  var Search = PaginatedCollection.extend({

    urlRoot: null,

    initialize: function(model, condition, options) {
      this.model = model;
      this.condition = condition || {};
      this.options = options || {};
    },

    one: function(condition) {
      this.reset();
      this.fetch({condition: condition, async: false});
      return this.at(0);
    },

    many: function(condition) {
      this.reset();
      this.fetch({
        condition: condition
      });
      return this.models;
    },

    url: function() {
      var base = _.result(this.model.prototype, 'urlRoot') || _.result(this, 'urlRoot') || urlError();
      return base;
    },

    /**
     * Augment fetch() with all information
     */
    fetch: function(options) {
      var attrs = [];
      options = options ? _.clone(options) : {};
      attrs = options.condition ? options.condition : {};
      options.data = options.data ? options.data : {};
      options.data["q"] = JSON.stringify({"filters": this._makeFilters(attrs)});
      return Search.__super__.fetch.call(this, options);
    },

    /**
     * Build filters to restless interface based on condition
     */
    _makeFilters: function(condition) {

      var attrs = _.extend({}, this.condition, condition),
          filters = [];

      for (var i=0, keys=_.keys(attrs), tot=keys.length; i < tot; i++) {
        var key = keys[i],
            filter = {'name': key},
            attr = attrs[key];
        if (_.isObject(attr)) {
          var a = _.pairs(attr)[0];
          filter['op'] = a[0];
          filter['val'] = a[1];
        } else {
          filter['op'] = 'eq';
          filter['val'] = attr;
        }
        filters.push(filter);
      }

      return filters;
    },

  }, {
    operator: {
      equals: ["==", "eq", "equals", "equals_to"],
      unequals: ["!=", "ne", "neq", "does_not_equal", "not_equal_to"],
      gt: [">", "gt"],
      lt: ["<", "lt"],
      gte: [">=", "ge", "gte", "geq"],
      lte: ["<=", "le", "lte", "leq"],
      element_of: ["in", "element_of"],
      not_element_of: ["not_in", "not_element_of"],
      is_null: ["is_null"],
      is_not_null: ["is_not_null"],
      like: ["like"],
      has: ["has"],
      any: ["any"],
    },
  });

  window.Search = Search;
  return Search;

});
