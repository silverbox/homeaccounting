# dynamodb tables design

## account_slip
every income/consume information
- tgt_date (Primary key : HASH, Type : String)<br>
  YYYYMMDD format date string. event date.
- kind_cd_seq (Primary key : RANGE, Type : String) <br>
  combine kind_cd and 0000 format string.
- val (Type : Number)<br>
  amount of consume(or income).
- memo (Type : String)<br>
  information of each consume.

## account_kind_mst
master data of income/consume
- kind_cd (Primary key : HASH, Type : String)<br>
  code for type of consume.
- kind_nm (Type : String)<br>
  name of the kind.
- memo (Type : String)<br>
  information of the type
- income_flg (Type : Number)<br>
  0: consume, 1:income

## account_balance
balance at the beginning of the settle date.
- tgt_date (Primary key : HASH, Type : String)<br>
  YYYYMMDD format date string. event date.

