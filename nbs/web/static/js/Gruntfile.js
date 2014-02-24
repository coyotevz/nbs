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
          out: '<%= pkg.name %>-admin.js',
          include: [
            'admin',
            'controllers/admin_controller',
            'controllers/dashboard_controller',
            'controllers/supplier_controller',
            'controllers/product_controller',
            '../<%= nunjucks.admin.dest %>',
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
          out: '<%= pkg.name %>-pos.js',
          include: [
            'pos',
            'controllers/pos_controller',
            '../<%= nunjucks.pos.dest %>',
          ],
          insertRequire: ['pos'],
          preserveLicenseComments: false,
          wrap: true,
          optimize: "uglify",
        }
      }
    },
    nunjucks: {
      admin: {
        baseDir: 'app/templates',
        src: ['app/templates/*.html', 'app/templates/admin/**/*.html'],
        dest: '<%= pkg.name %>-admin-templates.js',
        options: {
          name: function(filename) {
            return filename.replace('app/templates/', '');
          }
        }
      },
      pos: {
        baseDir: 'app/templates',
        src: ['app/templates/*.html', 'app/templates/pos/**/*.html'],
        dest: '<%= pkg.name %>-pos-templates.js',
        options: {
          name: function(filename) {
            return filename.replace('app/templates/', '');
          }
        }
      }
    },
    clean: {
      built: [
        '<%= requirejs.admin.options.out %>',
        '<%= requirejs.pos.options.out %>',
      ],
      generated: [
        '<%= nunjucks.admin.dest %>',
        '<%= nunjucks.pos.dest %>',
      ],
    }
  });

  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-requirejs');
  grunt.loadNpmTasks('grunt-nunjucks');

  grunt.registerTask('default',
    ['clean', 'jshint', 'nunjucks', 'requirejs', 'clean:generated']
  );
};
