define([
  'jquery',
  'underscore',
  'jquery.number',
], function($, _) {
  "use strict";

  return {

    'numberfmt': function(n, digits, dsep, gsep) {
      return $.number(n, digits == null ? 2 : digits, dsep || ',', gsep || '.' );
    },

    'map': function(objs, attribute) {
      return _.pluck(objs, attribute);
    },

    'sum': function(array) {
      return _.reduce(array, function(memo, num) {
        return memo + Number(num);
      }, 0);
    },

    'attr': function(obj, attr) {
      return obj[attr];
    },

  };
});
