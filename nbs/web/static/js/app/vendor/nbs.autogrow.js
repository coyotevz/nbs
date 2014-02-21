/*
 * Autogrow input resizer
 * Based on: https://github.com/rkivalin/jquery-autogrow
 */

define([
  'jquery',
  'backbone',
  'backbone.stickit',
], function($, Backbone) {
  "use strict";

  var testSubject,
      inherit = ['font', 'font-family', 'font-weight', 'font-size',
                 'letter-spacing', 'text-transform'];

  var getTestSubject = function() {
    if (!testSubject) {
      testSubject = $('<span id="autogrow-tester"/>').css({
        'position': 'absolute', 'top': -9999, 'left': -9999,
        'width': 'auto', 'visibility': 'hidden',
      }).appendTo('body');
    }
    return testSubject;
  };

  $.fn.autogrow = function(options) {
    return this.each(function() {
      var check, input, prop, styles = {};

      input = $(this);
      input._originalWidth = input.width();
      $.each(inherit, function(i, prop) {
        styles[prop] = input.css(prop);
      });

      check = function() {
        if (!input.val()) {
          return input.width(input._originalWidth);
        } else {
          var ts = getTestSubject();
          ts.css(styles);
          ts.html($('<span>').text(input.val()).html().replace(/ /g, '&nbsp;'));
          return input.width(ts.width() + 3);
        }
      };

      input.on('input.autogrow', check);
      input.on('change.stickit', check);
      check();
    });
  };

  /* Add handler for backbone stickit */
  if (Backbone.Stickit) {
    Backbone.Stickit.addHandler({
      selector: '*',
      afterUpdate: function($el) {
        $el.trigger('change.stickit');
      },
    });
  }
});
