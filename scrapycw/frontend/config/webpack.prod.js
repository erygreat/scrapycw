const { merge } = require('webpack-merge');
const path = require('path');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const common = require('./webpack.common.js');
const HtmlWebpackPlugin = require("html-webpack-plugin");

config = merge(common, {
    mode: "production",
    plugins: [
        new CleanWebpackPlugin({
            cleanOnceBeforeBuildPatterns: [
                path.resolve(__dirname, '../dist/*'),
            ]
        }),
        new HtmlWebpackPlugin({
            favicon: path.resolve(__dirname, '../src/favicon.ico'),
            template: 'src/index.html',
            filename: 'index.html',
        }),
    ]
});

module.exports = config;