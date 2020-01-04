export default {
  getYYYYMMDDStr: function (dateObj) {
    var YYYY = dateObj.getFullYear()
    // 「月」を取得する
    var MM = dateObj.getMonth() + 1
    // 「日」を取得する
    var DD = dateObj.getDate()
    var yStr = String(YYYY)
    var mStr = (MM >= 10 ? '' : '0') + String(MM)
    var dStr = (DD >= 10 ? '' : '0') + String(DD)
    return yStr + mStr + dStr
  },
  getLocalDateStr: function (yyyyMMddStr) {
    var yy = Number(yyyyMMddStr.substr(0, 4))
    var mm = Number(yyyyMMddStr.substr(4, 2))
    var dd = Number(yyyyMMddStr.substr(6, 2))
    // var dateObj = new Date(yy, mm, dd)
    return yy + ' / ' + mm + ' / ' + dd
  },
  getLocalDate: function (yyyyMMddStr) {
    var yy = Number(yyyyMMddStr.substr(0, 4))
    var mm = Number(yyyyMMddStr.substr(4, 2)) - 1
    var dd = Number(yyyyMMddStr.substr(6, 2))
    return new Date(yy, mm, dd)
  },
  getBaseAxiosHeader: function (key, token) {
    var wktoken = token
    if (token === undefined) {
      wktoken = 1
    }
    return {
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': key,
        'Authorization': wktoken
      },
      data: {}
    }
  }
}
