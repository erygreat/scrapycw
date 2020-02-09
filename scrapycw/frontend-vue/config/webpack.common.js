const path = require('path');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const webpack = require('webpack');
const merge = require('webpack-merge/dist');

module.exports = {
    entry: {
        app: "./src/main.js"
    },
    output: {
        filename: '[name].bundle.js',
        path: path.resolve(__dirname, '../dist/'),
        publicPath: '/static/',
    },
    module: {
        rules: [{
                test: /\.vue$/,
                use: [{
                        loader: 'vue-loader',
                        options: {}
                    },
                    {
                        loader: 'iview-loader',
                        options: {
                            prefix: false
                        }
                    }
                ]
            },
            {
                test: /\.js$/,
                loader: ['babel-loader'],
                exclude: /node_modules/
            },
            {
                test: /\.(png|jpg|gif|svg)$/,
                loader: 'file-loader',
                options: {
                    name: '[name].[ext]?[hash]'
                }
            },
            {
                test: /\.(woff|woff2|eot|ttf|otf)$/,
                use: [
                    'file-loader'
                ]
            },
            {
                test: /\.css$/,
                use: [
                    'vue-style-loader',
                    'css-loader'
                ]
            },
            {
                test: /\.scss$/,
                use: [
                    'vue-style-loader',
                    'css-loader',
                    'sass-loader'
                ]
            }
        ]
    },
    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.esm.js',
            '@': path.resolve(__dirname, '../src')
        },
        extensions: [".js", ".vue"]
    },
    plugins: [
        new VueLoaderPlugin(),
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery'
        }),

    ],
    optimization: {
        splitChunks: {
            chunks: "all",
            name: true,
            minSize: 0,
            cacheGroups: {
                vendors: {
                    minChunks: 2,
                    name: 'commons',
                    chunks: 'all'
                },
            }

        }
    }
};