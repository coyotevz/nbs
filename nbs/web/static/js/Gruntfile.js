module.exports = function(grunt) {

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    /* define tasks */
    jshint: {
      files: ['Gruntfile.js', 'app/**/*.js', '!app/vendor/**/*.js'],
      options: {
        globals: {
          jQuery: true,
          console: true,
          module: true
        }
      }
    },
    requirejs: {
      admin: {
        options: {
          baseUrl: "app",
          mainConfigFile: "app/config.js",
          name: "admin",
          out: "<%= pkg.name %>-admin.min.js",
          preserveLicenseComments: false,
          optimize: "none",
        }
      },
      pos: {
        options: {
          baseUrl: "app",
          mainConfigFile: "app/config.js",
          name: "pos",
          out: "<%= pkg.name %>-pos.min.js",
          preserveLicenseComments: false,
          optimize: "none",
        }
      }
    },
    nunjucks: {},
    clean: ['<%= pkg.name %>-admin.min.js', '<%= pkg.name %>-pos.min.js'],
  });

  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-requirejs');
  grunt.loadNpmTasks('grunt-nunjucks');

  grunt.registerTask('default', ['clean', 'jshint', 'requirejs']);
};
