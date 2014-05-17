define([
  'jquery',
  'underscore',
  'views/base/view',
], function($, _, View) {
  "use strict";

  var BodyView = View.extend({
    template: 'admin/body.html',
    noWrap: true,

    regions: {
      sidebar: '#sidebar_container',
      content: '#page_container',
    },

    attach: function() {
      BodyView.__super__.attach.apply(this, arguments);
      $(window).on('resize', _.debounce(this.resize, 150));
      $(window).on('focus', this.resize);
      this.resize();
      this.$('.scroll-wrapper').on('scroll', this.scrolled);
    },

    resize: function() {
      var topbar_h = $('.top-bar').outerHeight() || 60;
      var window_h = $(window).height();
      $('.scroll-wrapper').css('max-height', window_h - topbar_h);
    },

    scrolled: function(evt) {
      var fixed = false;
      $('.scroll-wrapper').each(function(i, e) {
        fixed = fixed || $(e).scrollTop() > 0;
      });
      $('.top-bar').toggleClass('fixed', fixed);
    },
  });

  return BodyView;
});
