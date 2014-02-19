define([
  'jquery',
  'underscore',
  'views/base/view',
], function($, _, View) {
  "use strict";

  var BodyView = View.extend({
    template: 'admin/body.html',

    regions: {
      sidebar_header: '#sidebar_header',
      sidebar: '#sidebar',
      sidebar_footer: '#sidebar_footer',
      toolbar: '.toolbar',
      content: '.content',
    },

    attach: function() {
      BodyView.__super__.attach.apply(this, arguments);
      $(window).on('resize', _.debounce(this.resize, 150));
      $(window).on('focus', this.resize);
      this.resize();
      this.$('.scroll-container').on('scroll', this.scrolled);
    },

    resize: function() {
      /* This requires:
       *    body { overflow: hidden; }
       * in CSS and that 'aside' view exists to work properly
       */
      var container = this.$('.view-container'),
          scrollContainer = this.$('.scroll-container'),
          contentAvlWidth = $(window).width() - this.$('aside').width(),
          contentAvlHeight = $(window).height() - container.position().top;

      container.width(contentAvlWidth);
      container.height(contentAvlHeight);
      scrollContainer.height(contentAvlHeight);
    },

    scrolled: function(evt) {
      if ($(this).scrollTop() > 0) {
        $('#viewpane').addClass('scrolled');
      } else {
        $('#viewpane').removeClass('scrolled');
      }
    },

  });

  return BodyView;
});
