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

  var getAttrPath = function(attrStrOrPath) {
    var path;

    if (_.isString(attrStrOrPath)) {
      path = (attrStrOrPath === '') ? [''] : attrStrOrPath.match(/[^\.\[\]]+/g);
      path = _.map(path, function(val) {
        // convert array accessors to numbers
        return val.match(/^\d+$/) ? parseInt(val, 10) : val;
      });
    } else {
      path = attrStrOrPath;
    }

    console.log('getAttrPath(' + attrStrOrPath + ') > ' + path);
    return path;
  };

  var createAttrStr = function(attrPath) {
    var attrStr = attrPath[0];
    _.each(_.rest(attrPath), function(attr) {
      attrStr += _.isNumber(attr) ? ('[' + attr + ']') : ('.' + attr);
    });

    return attrStr;
  };

  var walkPath = function(obj, attrPath, callback, scope) {
    var val = obj,
        childAttr;

    // walk through the child attributes
    for (var i = 0; i < attrPath.length; i++) {
      callback.call(scope || this, val, attrPath.slice(0, i + 1), attrPath[i+1]);

      childAttr = attrPath[i];
      val = val[childAttr];
      if (!val) break;
    }
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
        attrs = deepExtend({}, defaults, attrs);
      this.set(attrs, options);
      this.changed = {}
      this.initialize.apply(this, arguments);
    },

    toJSON: function(options) {
      return _.cloneDeep(this.attributes);
    },

    add: function(attr, value, options) {
      var current = this.get(attr);
      if (!_.isArray(current)) throw new Error('current value is not an array');
      return this.set(attr + '[' + current.length + ']', value, options);
    },

    _getAttr: function(attr) {
      var attrPath = getAttrPath(attr),
          result;
      walkPath(this.attributes, attrPath, function(val, path) {
        var attr = _.last(path);
        if (path.length === attrPath.length) {
          // attribute found
          result = val[attr];
        }
      });

      return result;
    },

    has: function(attr) {
      var result = this.get(attr);
      return !(result === null || _.isUndefined(result));
    },

    // Override set
    // Supports nested attributes via the syntax 'obj.attr' e.g. 'author.user.name'
    set: function(key, value, options) {
      var attributes, result;

      // Handle both `"key", value` and `{key: value}` -style arguments.
      if (_.isObject(key) || key == null) {
        attributes = key;
        options = value;
      } else {
        attributes = {};
        attributes[key] = value;
      }

      result = this._set(attributes, options);
      // Trigger events which have been blocked until the entire object graph is updated.
      this._processPendingEvents();
      return result;
    },

    _set: function(attributes, options) {
      if (!attributes) return this;
    },

    // Process all pending events after the entire object graph has been updated
    _processPendingEvents: function() {
      if (!this._processedEvents) {
        this._processedEvents = true;
        this._deferEvents = false;

        // Trigger all pending events
        _.each(this._pendingEvents, function(e) {
          e.c.trigger.apply(e.c, e.a);
        });

        this._pendingEvents = {};

        // Traverse down the object graph to call process pending events on sub-trees
        _.each(this.relations, function(relation) {
          var val = this.attributes[relation.key];
          val && val._processPendingEvents();
        }, this);

        delete this._processedEvents;
      }
    },

  });

  // Methods that use original implementation
  // ----------------------------------------

  // Override get to find nested attributes
  Model.prototype.get = _.wrap(Model.prototype.get, function(_get, attr) {
    var obj = _get.call(this, attr);
    return obj ? obj : this._getAttr.apply(this, _.rest(arguments));
  });
  
  // Override trigger to defer events in the object graph.
  Model.prototype.trigger = _.wrap(Model.prototype.trigger, function(_trigger) {
    // Defer event processing
    if (this._deferEvents) {
      this._pendingEvents = this._pendingEvents || [];
      // Maintain a queue of pending events to trigger.
      this._pendingEvents.push({c: this, a: _.rest(arguments)});
    } else {
      _trigger.apply(this, _.rest(arguments));
    }
  });

  // Don't return anything
});
