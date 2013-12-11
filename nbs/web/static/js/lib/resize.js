/*
 * resize routine for admin view
 */

define(['jquery'], function($) {
  "use strict";

  var resize = function() {
    var contentWrapper = $('#content_wrapper'),
        scrollWrapper = $('#scroll_wrapper'),
        contentAvlWidth = $(window).width() - $('aside').width(),
        contentAvlHeight = $(window).height() - contentWrapper.position().top,

  contentWrapper.width(contentAvlWidth);
  contentWrapper.height(contentAvlHeight);
  scrollWrapper.height(contentAvlHeight);
  };

  $(window).resize(resize);
  $(window).focus(resize);
  resize();
});
