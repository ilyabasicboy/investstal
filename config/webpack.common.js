//Default
let path = require('path');
const webpack = require('webpack');
const projectDir = 'investstal';

//Require plugins
const FileManagerPlugin = require('filemanager-webpack-plugin');

module.exports = {
    entry: {
        bundle: '/' + projectDir + '/static/index.js',
    },
    output: {
        path: path.join(__dirname, '../' + projectDir + '/static/bundle/'),
        filename: '[name].[fullhash].js',
        publicPath: '',
    },
    watchOptions: {
        ignored: /node_modules/,
    },
    stats: {
        errors: true,
        errorDetails: true,
        builtAt: true,
        assets: false,
        modules: false,
        children: false,
    },
    plugins: [
        //Add jquery to webpack
        new webpack.ProvidePlugin({
            $: "jquery",
            jQuery: "jquery",
            'window.jQuery': 'jquery'
        }),
        new FileManagerPlugin({
            events: {
                onStart: {
                    delete: ['./' + projectDir + '/static/bundle/'],
                },
            }
        })
    ],
    module: {
        rules: [
            //JavaScript: Use Babel to transpile JavaScript files
            {
                test: /\.js$/,
                exclude: '/node_modules/',
                use: 'babel-loader',
            },
            //Fonts and SVGs: Inline files
            {
                test: /\.(woff(2)?|eot|ttf|otf|svg|)$/,
                type: 'asset/inline'
            },
        ],
    },
    performance: {
        hints: false,
        maxEntrypointSize: 512000,
        maxAssetSize: 512000
    }
};