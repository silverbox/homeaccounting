import {
  CognitoUserPool,
  CognitoUser,
  AuthenticationDetails,
  CognitoUserAttribute
} from 'amazon-cognito-identity-js'
import { Config, CognitoIdentityCredentials } from 'aws-sdk'

export default class Cognito {
  configure (config) {
    if (config.userPool) {
      this.userPool = config.userPool
    } else {
      this.userPool = new CognitoUserPool({
        UserPoolId: config.UserPoolId,
        ClientId: config.ClientId
      })
    }
    Config.region = config.region
    Config.credentials = new CognitoIdentityCredentials({
      IdentityPoolId: config.IdentityPoolId
    })
    this.options = config
  }

  static install = (Vue, options) => {
    Object.defineProperty(Vue.prototype, '$cognito', {
      get () { return this.$root._cognito }
    })

    Vue.mixin({
      beforeCreate () {
        if (this.$options.cognito) {
          this._cognito = this.$options.cognito
          this._cognito.configure(options)
        }
      }
    })
  }

  /**
   * username, passwordでサインアップ
   * username = emailとしてUserAttributeにも登録
   */
  signUp (username, password) {
    const dataEmail = { Name: 'email', Value: username }
    const attributeList = []
    attributeList.push(new CognitoUserAttribute(dataEmail))
    return new Promise((resolve, reject) => {
      this.userPool.signUp(username, password, attributeList, null, (err, result) => {
        if (err) {
          reject(err)
        } else {
          resolve(result)
        }
      })
    })
  }

  /**
   * 確認コードからユーザーを有効化する
   */
  confirmation (username, confirmationCode) {
    const userData = { Username: username, Pool: this.userPool }
    const cognitoUser = new CognitoUser(userData)
    return new Promise((resolve, reject) => {
      cognitoUser.confirmRegistration(confirmationCode, true, (err, result) => {
        if (err) {
          reject(err)
        } else {
          resolve(result)
        }
      })
    })
  }

  /**
   * username, passwordでログイン
   */
  login (username, password, onNewPasswordRequired) {
    const userData = { Username: username, Pool: this.userPool }
    const cognitoUser = new CognitoUser(userData)
    const authenticationData = { Username: username, Password: password }
    const authenticationDetails = new AuthenticationDetails(authenticationData)
    return new Promise((resolve, reject) => {
      var callbacks = {
        onSuccess: (result) => {
          resolve(result)
        },
        onFailure: (err) => {
          reject(err)
        },
        newPasswordRequired: (userAttributes, requiredAttributes) => {
          onNewPasswordRequired(userAttributes, requiredAttributes).then((newPass) => {
            // var newPass = window.prompt('Please input your new Password', 'Your input will not be masked. please make sure there is no other person.')
            cognitoUser.completeNewPasswordChallenge(newPass, {}, callbacks)
          }).catch((err) => {
            reject(err)
          })
        }
      }
      cognitoUser.authenticateUser(authenticationDetails, callbacks)
    })
  }

  /**
   * ログアウト
   */
  logout () {
    this.userPool.getCurrentUser().signOut()
  }

  /**
   * ログインしているかの判定
   */
  isAuthenticated () {
    const cognitoUser = this.userPool.getCurrentUser()
    return new Promise((resolve, reject) => {
      if (cognitoUser === null) { reject(cognitoUser) }
      cognitoUser.getSession((err, session) => {
        if (err) {
          reject(err)
        } else {
          if (!session.isValid()) {
            reject(session)
          } else {
            resolve(session)
          }
        }
      })
    })
  }

  /**
   * トークン再取得してAjax実行
   */
  callGetApi (axios, url) {
    const that = this
    return new Promise((resolve, reject) => {
      that.isAuthenticated().then(function (session) {
        const config = {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': session.getIdToken().getJwtToken()
          },
          data: {}
        }
        // console.log('isAuthenticatedGet:' + session.getIdToken().getJwtToken())
        return axios.get(url, config)
      }).then(function (response) {
        resolve(response)
      }).catch(err => {
        reject(err)
      })
    })
  }

  /**
   * トークン再取得してAjax実行
   */
  callPostApi (axios, url, data) {
    const that = this
    return new Promise((resolve, reject) => {
      that.isAuthenticated().then(function (session) {
        const config = {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': session.getIdToken().getJwtToken()
          },
          data: {}
        }
        // console.log('isAuthenticatedPost:' + session.getIdToken().getJwtToken())
        return axios.post(url, data, config)
      }).then(function (response) {
        resolve(response)
      }).catch(err => {
        reject(err)
      })
    })
  }
}
