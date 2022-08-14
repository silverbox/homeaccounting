export default {
  getYYYYMMDDStr: (dateObj: Date): string => {
    const YYYY = dateObj.getFullYear()
    // 「月」を取得する
    const MM = dateObj.getMonth() + 1
    // 「日」を取得する
    const DD = dateObj.getDate()
    const yStr = String(YYYY)
    const mStr = (MM >= 10 ? '' : '0') + String(MM)
    const dStr = (DD >= 10 ? '' : '0') + String(DD)
    return yStr + mStr + dStr
  },
  getLocalDateStr: (yyyyMMddStr: string): string => {
    const yy = Number(yyyyMMddStr.substr(0, 4))
    const mm = Number(yyyyMMddStr.substr(4, 2))
    const dd = Number(yyyyMMddStr.substr(6, 2))
    // var dateObj = new Date(yy, mm, dd)
    return yy + ' / ' + mm + ' / ' + dd
  },
  getLocalDate: (yyyyMMddStr: string): Date => {
    const yy = Number(yyyyMMddStr.substr(0, 4))
    const mm = Number(yyyyMMddStr.substr(4, 2)) - 1
    const dd = Number(yyyyMMddStr.substr(6, 2))
    return new Date(yy, mm, dd)
  }
}
