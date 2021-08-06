const { merge } = require('webpack-merge');
const path = require('path');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const common = require('./webpack.common.js');

config = merge(common, {
    mode: "production",
    plugins: [
        new CleanWebpackPlugin({
            cleanOnceBeforeBuildPatterns: [
                path.resolve(__dirname, '../dist/*'),
            ]
        }),
    ]
});

module.exports = config;