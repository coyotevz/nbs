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
    requirejs: {},
    nunjucks: {},
  });

  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-requirejs');
  grunt.loadNpmTasks('grunt-nunjucks');

  grunt.registerTask('default', ['jshint']);
};
