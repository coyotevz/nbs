/*
 * Table fixed headers
 */

define([
  'jquery',
], function($) {
  "use strict";

  $.fn.fixedHeader = function(options) {
    return this.each(function() {
      var offset, scrollTop, $cloned,
          $e = $(this),
          $h = $('thead tr', $e);
      offset = $e.offset();
      scrollTop = $(window).scrollTop();

      if ((scrollTop > offset.top) && scrollTop < offset.top + $e.height()) {
        $h.css({
          'visibility': 'visible',
          'top': Math.min(scrollTop - offset.top, $e.height() - $h.height()) + "px",
        });
      } else {
        $h.css({
          'visibility': 'hidden',
          'top': '0px',
        });
      }

    });
  }
});
