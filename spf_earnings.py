import requests
from requests.structures import CaseInsensitiveDict
import json

contract_rent = 4
spf_total = 400000000
spf_share = 0.15

def earnings(amount=10000, months=1, data_stored='no_data'):
  if data_stored == 'no_data':
    data_stored = data_stored_today()
  spf_share_dollars = contract_rent * data_stored * spf_share / spf_total
  return [round(amount, 0), round(months, 0), round(data_stored, 0), round(spf_share_dollars * amount * months, 4)]
  
def data_stored_today():
  url = 'https://grafana.scpri.me/api/ds/query'
  headers = CaseInsensitiveDict()
  headers["Accept"] = "application/json"
  headers["Content-Type"] = "application/json"
  data = json.dumps({"queries":[{"refId":"A","datasourceId":2,"rawSql":"select \r\n--providers_active_now as \"Today's Average\",\r\n--to_char(providers_active_now - providers_active_7dback,'SG 9999999') as active_diff7d,\r\n--to_char(providers_active_now - providers_active_30dback,'SG 9999999') as active_diff30d\r\n--capacity_now/1000000000000000.0 as \"Capacity Today\",\r\n--(capacity_now-capacity_7dback)/1000000000000000.0 as capacitydiff7d,\r\n--(capacity_now-capacity_30dback)/1000000000000000.0 as capacitydiff30d\r\nto_char(used_now/1000000000000.0,'9999999999990 \"TB\"') as \"Data Stored Today\",\r\nto_char((used_now-used_7dback)/1000000000000.0,'SG9999999999990.9 \"TB\"') as usagediff7d,\r\nto_char((used_now-used_30dback)/1000000000000.0,'SG9999999999990 \"TB\"') as usagediff30d\r\nfrom (select\r\n  time_bucket(3600*24, \"timestamp\") AS \"time\",\r\n  --first_value(avg(providers_active)::bigint) over (order by 1 desc) as providers_active_now,\r\n  --nth_value(avg(providers_active)::bigint,8) over (order by 1 desc) as providers_active_7dback, \r\n  --nth_value(avg(providers_active)::bigint,31) over (order by 1 desc) as providers_active_30dback\r\n  --first_value(avg(capacity_total)::bigint) over (order by 1 desc) as capacity_now,\r\n  --nth_value(avg(capacity_total)::bigint,8) over (order by 1 desc) as capacity_7dback,\r\n  --nth_value(avg(capacity_total)::bigint,31) over (order by 1 desc) as capacity_30dback\r\n  first_value(avg(capacity_used)::bigint) over (order by 1 desc) as used_now,\r\n  nth_value(avg(capacity_used)::bigint,8) over (order by 1 desc) as used_7dback,\r\n  nth_value(avg(capacity_used)::bigint,31) over (order by 1 desc) as used_30dback\r\nfrom \r\nnetwork.totals\r\nwhere \"timestamp\">=unix_now()-3600*24*31\r\ngroup by 1\r\norder by 1 desc\r\nlimit 1) daily_averages", "format":"table"}]})
  r = requests.post(url, data=data, headers=headers)
  r = r.json()
  r = r['results']['A']['frames'][0]['data']['values'][0][0]
  r = r.split()
  r = r[0]
  return float(r)
       

if __name__ == "__main__":
  print(earnings())
