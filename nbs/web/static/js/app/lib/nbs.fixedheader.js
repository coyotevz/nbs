/*
 * Fix table headers
 */

define([
  'jquery',
  'underscore',
], function($, _) {
  "use strict";

  $.fn.fixHeader = function(options) {
    return this.each(function() {
      var $table = $(this),
          $parent = $table.parent(),
          $cloned = $table.clone(),
          resize;

      $cloned.insertBefore($table).find('tbody').remove();
      $cloned.addClass('fixed');
      $table.find('thead').css('visibility', 'hidden');

      resize = _.partial(function($f, $p) {
        $f.css('width', $p.css('width'));
      }, $cloned, $table);

      resize();
      $(window).on('resize', _.debounce(resize, 150));
    });
  };
});
