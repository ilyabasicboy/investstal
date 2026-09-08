//Default
const { merge } = require('webpack-merge');
const common = require('./webpack.common');
const projectDir = 'investstal';

//Require plugins
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');
const TerserPlugin = require('terser-webpack-plugin');
const ReplaceHashInFileWebpackPlugin = require('replace-hash-in-file-webpack-plugin');

module.exports = merge(common, {
    mode: 'production',
    optimization: {
        minimizer: [
            new TerserPlugin({extractComments: false}),
            new CssMinimizerPlugin()
        ],
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: "[name].[fullhash].css",
        }),
        new ReplaceHashInFileWebpackPlugin([{
            dir: './' + projectDir + '/templates/',
            files: ['base.html'],
            rules: [{
                search: /bundle\.*[a-zA-Z0-9]*\.js/,
                replace: 'bundle.[hash].js'
            },
            {
                search: /bundle_dev\.js/,
                replace: 'bundle.[hash].js'
            },
            {
                search: /bundle\.*[a-zA-Z0-9]*\.css/,
                replace: 'bundle.[hash].css'
            }]
        }]),
    ],
    module: {
        rules: [
            //Styles
            {
                test: /\.(sass|scss|css)$/,
                use: [
                    MiniCssExtractPlugin.loader,
                        {
                            loader: 'css-loader',
                            options: {
                                importLoaders: 2,
                                sourceMap: false,
                                modules: false,
                            },
                        },
                        'postcss-loader',
                        'sass-loader',
                    ],
            },
        ],
    },
});