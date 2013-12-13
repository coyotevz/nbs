define([
  'jquery',
  'views/base/view',
], function($, View) {
  "use strict";

  var BodyView = View.extend({
    template: 'admin/body.html',

    regions: {
      sidebar_header: '#sidebar_header',
      sidebar: '#sidebar',
      sidebar_footer: '#sidebar_footer',
      toolbar: '#toolbar',
      content_header: '#content_header',
      content: '#content',
      content_footer: '#content_footer',
    },

    initialize: function() {
      BodyView.__super__.initialize.apply(this, arguments);
      console.log('BodyView#initialize(%s)', this.cid);
    },

    attach: function() {
      BodyView.__super__.attach.apply(this, arguments);
      $(window).resize(this.resize).focus(this.resize);
      this.resize();
    },

    resize: function() {
      /* This requires:
       *    body { overflow: hidden; }
       * in CSS and that 'aside' view exists to work properly
       */
      var contentWrapper = this.$('#content_wrapper'),
          scrollWrapper = this.$('#scroll_wrapper'),
          contentAvlWidth = $(window).width() - this.$('aside').width(),
          contentAvlHeight = $(window).height() - contentWrapper.position().top;

      contentWrapper.width(contentAvlWidth);
      contentWrapper.height(contentAvlHeight);
      scrollWrapper.height(contentAvlHeight);
    },
  });

  return BodyView;
});
