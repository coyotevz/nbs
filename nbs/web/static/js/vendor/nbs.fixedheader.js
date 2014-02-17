/*
 * Table fixed headers
 */

define([
  'jquery',
], function($) {
  "use strict";

  $.fn.fixedHeader = function(options) {
    return this.each(function() {
      var $e = $(this);
      console.log('fixedHeader plugin:', $e);
    });
  }
});
