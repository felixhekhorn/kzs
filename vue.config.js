module.exports = {
  publicPath: process.env.NODE_ENV === 'production' ? '/kzs/' : '/',
  pluginOptions: {
    quasar: {
      importStrategy: 'kebab',
      rtlSupport: false
    }
  },
  transpileDependencies: [
    'quasar'
  ]
}
