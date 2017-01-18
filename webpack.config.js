const path = require('path')
const webpack = require('webpack')
const grunt = require('grunt')
const _ = require('lodash')

const pkg = grunt.file.readJSON('package.json')
const rawBanner = grunt.file.read('res/templates/banner.txt')
const banner = grunt.template.process(rawBanner, {data: {package: pkg}})

const isDebug = (_.has(process.env, 'NODE_ENV') ? 'development' : 'production') === 'development'

module.exports = {
  context: path.join(__dirname, 'res/js'),
  devtool: isDebug ? '#source-map' : '#eval-source-map',
  entry: {
    app: './index.js',
    snake: './snake.js'
  },
  output: {
    publicPath: '/stadt/static/stadt/js/',
    path: path.join(__dirname, 'stadt/static/js/'),
    filename: '[name].js'
  },
  resolve: {
    alias: {
      app: path.resolve(__dirname, 'res/js'),
    }
  },
  module: {
    noParse: /node_modules\/json-schema\/lib\/validate\.js/,
    rules: [
      {
        test: /\.jsx?$/,
        include: [
          path.resolve(__dirname, 'res/js')
        ],
        loader: 'babel-loader',
        options: {
          presets: [
            ['es2015', {'modules': false}]
          ],
          plugins: ['transform-runtime', ['babel-root-slash-import', {
            'rootPathSuffix': 'res/js'
          }]]
        }
      }
    ]
  },
  plugins: [
    new webpack.BannerPlugin(banner),
    new webpack.ContextReplacementPlugin(/moment[/\\]locale$/, /de/),
    new webpack.optimize.UglifyJsPlugin({
      sourceMap: !isDebug,
      compress: {
        warnings: !isDebug
      }
    }),
    new webpack.LoaderOptionsPlugin({
      minimize: !isDebug,
      debug: isDebug
    })
  ]
}
