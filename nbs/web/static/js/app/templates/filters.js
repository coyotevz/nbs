define([
  'jquery',
  'jquery.number',
], function($) {
  "use strict";

  return {
    'numberfmt': function(n, digits, dsep, gsep) {
      return $.number(n, digits || 2, dsep || ',', gsep || '.' );
    }
  };
});
