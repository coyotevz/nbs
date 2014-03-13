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
    xhr: null,

    initialize: function(model, condition, options) {
      this.model = model;
      this.condition = condition || {};
      this.options = options || {};
    },

    one: function(condition, options) {
      options = options ? _.clone(options) : {};
      options.condition = condition || {};
      options.async = options.async ? options.async : false;
      //this.reset();
      this.cancel();
      this.xhr = this.fetch(options);
      return this.at(0);
    },

    many: function(condition, options) {
      options = options ? _.clone(options) : {};
      options.condition = condition || {};
      //this.reset();
      this.cancel();
      this.xhr = this.fetch(options);
      return this.models;
    },

    cancel: function() {
      if (this.xhr) this.xhr.abort();
    },

    url: function() {
      var base = _.result(this.model.prototype, 'urlRoot') || _.result(this, 'urlRoot') || urlError();
      return base;
    },

    /**
     * Augment fetch() with all information
     */
    fetch: function(options) {
      var attrs = options ? options.condition || {} : {};
      options = _.omit(options, 'condition');
      options.data = _.extend(options.data || {}, this._makeFilters(attrs));

      // encode url-data traditionally see:
      // https://api.jquery.com/jQuery.param/#jQuery-param-obj-traditional
      options.traditional = true;

      return PaginatedCollection.prototype.fetch.call(this, options);
    },

    /**
     * Build filters to rest interface based on condition
     */
    _makeFilters: function(condition) {

      var attrs = _.extend({}, this.condition, condition),
          filters = {};

      for (var i=0, keys=_.keys(attrs), tot=keys.length; i < tot; i++) {
        var key = keys[i],
            name = key,
            attr = attrs[key],
            op = '', val, f;
        if (_.isObject(attr)) {
          var a = _.pairs(attr)[0];
          //op = a[0];
          if (Search.operator.contains(a[0])) op = ':'+a[0];
          val = a[1];
        } else {
          val = attr;
        }
        filters[name+op] = val;
      }

      return filters;
    },

  }, {
    operator: _(['eq', 'neq', 'gt', 'gte', 'lt', 'lte',
                 'contains', 'endswith', 'startswith', 'like', 'ilike',
                 'in', 'nin'])
  });

  window.Search = Search;
  return Search;

});
