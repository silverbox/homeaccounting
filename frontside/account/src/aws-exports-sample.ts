export default {
  Auth: {
    // (required) only for Federated Authentication - Amazon Cognito Identity Pool ID
    identityPoolId: 'XX-XXXX-X:XXXXXXXX-XXXX-1234-abcd-1234567890ab',

    // (required)- Amazon Cognito Region
    region: 'XX-XXXX-X',

    // (optional) - Amazon Cognito User Pool ID
    userPoolId: 'XX-XXXX-X_abcd1234',

    // (optional) - Amazon Cognito Web Client ID (26-char alphanumeric string, App client secret needs to be disabled)
    userPoolWebClientId: 'a1b2c3d4e5f6g7h8i9j0k1l2m3',
  }
}