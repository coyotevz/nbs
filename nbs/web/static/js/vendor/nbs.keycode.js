/**
 * jQuery keycode inspection Plugin
 */

define([
  'jquery',
  'underscore',
], function($, _) {
  "use strict";

  var special_keys = {
    8: "backspace", 9: "tab", 10: "return", 13: "return", 16: "shift",
    17: "ctrl", 18: "alt", 19: "pause", 20: "capslock", 27: "esc",
    32: "space", 33: "pageup", 34: "pagedown", 35: "end", 36: "home",
    37: "left", 38: "up", 39: "right", 40: "down", 45: "insert", 46: "del",
    59: ";", 96: "0", 97: "1", 98: "2", 99: "3", 100: "4", 101: "5",
    102: "6", 103: "7", 104: "8", 105: "9", 106: "*", 107: "+", 109: "-",
    110: ".", 111 : "/", 112: "f1", 113: "f2", 114: "f3", 115: "f4",
    116: "f5", 117: "f6", 118: "f7", 119: "f8", 120: "f9", 121: "f10",
    122: "f11", 123: "f12", 144: "numlock", 145: "scroll", 186: ";",
    187: "=", 188: ",", 189: "-", 190: ".", 191: "/", 219: "[", 220: "\\",
    221: "]", 222: "'", 224: "meta"
  };

  $.keycode = function(event) {
    var special = special_keys[event.which],
        character = String.fromCharCode(event.which).toLowerCase(),
        modif = "";

    if (event.altKey && special !== "alt") {
      modif += "alt+";
    }
    if (event.ctrlKey && special !== "ctrl") {
      modif += "ctrl+";
    }
    if (event.metaKey && !event.ctrlKey && special !== "meta") {
      modif += "meta+";
    }
    if (event.shiftKey && special !== "shift") {
      modif += "shift+";
    }

    if (special) {
      return modif + special;
    } else {
      return modif + character;
    }
  };

  $.keycode_is = function(event, keys) {
    return _.contains(keys.split(' '), $.keycode(event));
  };
});
