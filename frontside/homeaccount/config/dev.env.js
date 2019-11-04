'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  API_ENDPOINT_BASE: '"https://fugafuga.execute-api.ap-northeast-1.amazonaws.com/dev/api/"',
  API_KEY: '"hogehoge"'
})
