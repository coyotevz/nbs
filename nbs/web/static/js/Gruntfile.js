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
          baseUrl: 'app',
          mainConfigFile: 'app/config.js',
          name: "../node_modules/almond/almond",
          out: '<%= pkg.name %>-admin.min.js',
          include: [
            'admin',
            'controllers/admin_controller',
            'controllers/dashboard_controller',
            'controllers/supplier_controller',
            'controllers/product_controller',
          ],
          insertRequire: ['admin'],
          preserveLicenseComments: false,
          wrap: true,
          optimize: "uglify",
        }
      },
      pos: {
        options: {
          baseUrl: 'app',
          mainConfigFile: 'app/config.js',
          name: "../node_modules/almond/almond",
          out: '<%= pkg.name %>-pos.min.js',
          include: [
            'pos',
            'controllers/pos_controller'
          ],
          insertRequire: ['pos'],
          preserveLicenseComments: false,
          wrap: true,
          optimize: "uglify",
        }
      }
    },
    nunjucks: {},
    clean: {
      generated: ['<%= pkg.name %>-admin.min.js',
                  '<%= pkg.name %>-pos.min.js'],
    }
  });

  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-requirejs');
  grunt.loadNpmTasks('grunt-nunjucks');

  grunt.registerTask('default', ['clean', 'jshint', 'requirejs']);
};
