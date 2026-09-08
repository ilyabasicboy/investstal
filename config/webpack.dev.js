//Default
let path = require('path');
const { merge } = require('webpack-merge');
const common = require('./webpack.common');
const projectDir = 'investstal';
let isDocker = process.env.IS_DOCKER;

//Require plugins
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const ReplaceHashInFileWebpackPlugin = require('replace-hash-in-file-webpack-plugin');

module.exports = merge(common, {
    mode: 'development',
    target: ['web'],
    devtool: 'inline-source-map',
    output: {
        path: path.join(__dirname, '../' + projectDir + '/static/bundle/'),
        filename: 'bundle_dev.js',
        publicPath: '/static/bundle/',
    },
    devServer: {
        static: {
            directory: path.resolve(__dirname, '../' + projectDir + '/static/bundle/'),
        },
        open: true,
        host: '0.0.0.0',
        compress: true,
        hot: true,
        port: 8000,
        proxy: {
                '!/static/bundle/**': {
                target: isDocker !== undefined ? 'http://host.docker.internal:8001' : 'http://localhost:8001',
                changeOrigin: true,
            },
        },
    },
    plugins: [
        new ReplaceHashInFileWebpackPlugin([{
            dir: './' + projectDir + '/templates/',
            files: ['base.html'],
            rules: [{
                search: /bundle\.*[a-zA-Z0-9]*\.js/,
                replace: 'bundle_dev.js'
            }],
        }]),
    ],
    module: {
        rules: [
            // Styles: Inject CSS into the head with source maps
            {
                test: /\.(sass|scss|css)$/,
                use: [
                    'style-loader',
                    {
                        loader: 'css-loader',
                        options: {
                            sourceMap: true,
                            importLoaders: 1,
                            modules: false
                        },
                    },
                    {
                        loader: 'postcss-loader',
                        options: {
                            sourceMap: true
                        }
                    },
                    {
                        loader: 'sass-loader',
                        options: {
                            sourceMap: true
                        }
                    },
                ],
            },
        ],
    },
});