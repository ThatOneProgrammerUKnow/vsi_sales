const path = require('path');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CopyWebpackPlugin = require('copy-webpack-plugin');
const WatchExternalFilesPlugin = require('webpack-watch-external-files-plugin');

module.exports = {
  entry: {
    "site-js": './assets/site.js',
    "site-styles": './assets/site-styles.js'
  },
  output: {
    path: path.resolve(__dirname, './static'),
    filename: 'js/[name]-bundle.js',
    library: ["SiteJS", "[name]"],
  },
  module: {
    rules: [
      {
        test: /\.scss$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'sass-loader',
          'postcss-loader'
        ],
      },
      {
        test: /\.css$/i,
        use: [MiniCssExtractPlugin.loader, 'css-loader', 'postcss-loader'],
      },
      {
        test: /\.(png|svg|jpg|jpeg|gif)$/i,
        type: 'asset/resource',
      },
    ],
  },
  plugins: [
    new MiniCssExtractPlugin({
      'filename': 'css/[name].css',
    }),
    new WatchExternalFilesPlugin({
      files: [
        './templates/**/*.html',
      ]
    })
  ],
};