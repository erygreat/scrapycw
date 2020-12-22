const { merge } = require('webpack-merge');
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
            '/i/**': {
                target: 'http://localhost:2312'
            },
        },
        historyApiFallback: {
            rewrites: [{
                    from: /^\/docs\/.*/g,
                    to: 'docs/'
                },
                {
                    from: /.*/g,
                    to: 'index.html'
                }
            ]
        }
    }
});