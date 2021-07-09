const path = require('path');
const webpack = require('webpack');

module.exports = {
    entry: {
        app: "./src/index.tsx"
    },
    output: {
        filename: '[name].bundle.js',
        path: path.resolve(__dirname, '../dist/'),
        publicPath: '/static/',
    },
    module: {
        rules: [
            { test: /\.tsx?$/, loader: "ts-loader", exclude: /node_modules/ },
            { test: /\.(js|jsx)?$/, use: 'babel-loader', exclude: /node_modules/ },
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
                test: /\.module\.css$/i,
                use: [
                    'style-loader',
                    'css-loader?modules'
                ]
            },
            {
                test: /^((?!\.module).)*css$/,
                use: [
                    'style-loader',
                    'css-loader'
                ]
            },
            {
                test: /\.module\.s[ac]ss$/i,
                use: [
                    'style-loader',
                    'css-loader?modules',
                    "sass-loader",
                ]
            },
        ]

    },
    resolve: {
        alias: {
            '@': path.resolve(__dirname, '../src'),
            '@stylesheets': path.resolve(__dirname, '../src/stylesheets'),
            '@ui': path.resolve(__dirname, '../src/components/ui')
        },
        extensions: [".ts", ".tsx", ".js"]
    },
    plugins: [
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            axios: 'axios'
        }),
    ]
};