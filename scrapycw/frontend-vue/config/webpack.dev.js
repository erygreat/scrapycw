const merge = require('webpack-merge/dist');
const common = require('./webpack.common.js');
const path = require('path');

// TODO 将代理抽出为依赖于当前环境
module.exports = merge(common, {
    mode: "development",
    devtool: 'inline-source-map',
    devServer: {
        contentBase: path.resolve(__dirname, '../dist'),
        hot: true,
        proxy: {
            '/api/**': {
                target: 'http://localhost:2312'
            },
        },
        historyApiFallback: {
            rewrites: [{
                from: /.*/g,
                to: 'index.html'
            }]
        }
    }
});