export default {
  getYYYYMMDDStr: (dateObj: Date): string => {
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
  getLocalDateStr: (yyyyMMddStr: string): string => {
    var yy = Number(yyyyMMddStr.substr(0, 4))
    var mm = Number(yyyyMMddStr.substr(4, 2))
    var dd = Number(yyyyMMddStr.substr(6, 2))
    // var dateObj = new Date(yy, mm, dd)
    return yy + ' / ' + mm + ' / ' + dd
  },
  getLocalDate: (yyyyMMddStr: string): Date => {
    var yy = Number(yyyyMMddStr.substr(0, 4))
    var mm = Number(yyyyMMddStr.substr(4, 2)) - 1
    var dd = Number(yyyyMMddStr.substr(6, 2))
    return new Date(yy, mm, dd)
  }
}
