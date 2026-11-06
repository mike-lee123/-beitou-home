# 全台首購：完整單檔，含22縣市368鄉鎮市區官方清單
# ===== beitou/regions.py =====
"""國土測繪中心戶政行政區清單，2026-11-06查核；離線內嵌，不依賴訪客即時呼叫。"""


def canonical_city(value):
    for name in REGIONS:
        if name.replace('臺', '台') == value.strip().replace('臺', '台'):
            return name
    raise ValueError('不支援的縣市')


def filename_for_city(city):
    return REGIONS[canonical_city(city)]['code'].lower() + '_lvr_land_a.csv'
REGION_SOURCE = "https://api.nlsc.gov.tw/other/ListCounty ; https://api.nlsc.gov.tw/other/ListTown1/{countycode}"
REGIONS = {
  "臺北市": {
    "code": "A",
    "districts": {
      "松山區": "63000010",
      "信義區": "63000020",
      "大安區": "63000030",
      "中山區": "63000040",
      "中正區": "63000050",
      "大同區": "63000060",
      "萬華區": "63000070",
      "文山區": "63000080",
      "南港區": "63000090",
      "內湖區": "63000100",
      "士林區": "63000110",
      "北投區": "63000120"
    }
  },
  "臺中市": {
    "code": "B",
    "districts": {
      "中區": "66000010",
      "東區": "66000020",
      "南區": "66000030",
      "西區": "66000040",
      "北區": "66000050",
      "西屯區": "66000060",
      "南屯區": "66000070",
      "北屯區": "66000080",
      "豐原區": "66000090",
      "東勢區": "66000100",
      "大甲區": "66000110",
      "清水區": "66000120",
      "沙鹿區": "66000130",
      "梧棲區": "66000140",
      "后里區": "66000150",
      "神岡區": "66000160",
      "潭子區": "66000170",
      "大雅區": "66000180",
      "新社區": "66000190",
      "石岡區": "66000200",
      "外埔區": "66000210",
      "大安區": "66000220",
      "烏日區": "66000230",
      "大肚區": "66000240",
      "龍井區": "66000250",
      "霧峰區": "66000260",
      "太平區": "66000270",
      "大里區": "66000280",
      "和平區": "66000290"
    }
  },
  "基隆市": {
    "code": "C",
    "districts": {
      "中正區": "10017010",
      "七堵區": "10017020",
      "暖暖區": "10017030",
      "仁愛區": "10017040",
      "中山區": "10017050",
      "安樂區": "10017060",
      "信義區": "10017070"
    }
  },
  "臺南市": {
    "code": "D",
    "districts": {
      "新營區": "67000010",
      "鹽水區": "67000020",
      "白河區": "67000030",
      "柳營區": "67000040",
      "後壁區": "67000050",
      "東山區": "67000060",
      "麻豆區": "67000070",
      "下營區": "67000080",
      "六甲區": "67000090",
      "官田區": "67000100",
      "大內區": "67000110",
      "佳里區": "67000120",
      "學甲區": "67000130",
      "西港區": "67000140",
      "七股區": "67000150",
      "將軍區": "67000160",
      "北門區": "67000170",
      "新化區": "67000180",
      "善化區": "67000190",
      "新市區": "67000200",
      "安定區": "67000210",
      "山上區": "67000220",
      "玉井區": "67000230",
      "楠西區": "67000240",
      "南化區": "67000250",
      "左鎮區": "67000260",
      "仁德區": "67000270",
      "歸仁區": "67000280",
      "關廟區": "67000290",
      "龍崎區": "67000300",
      "永康區": "67000310",
      "東區": "67000320",
      "南區": "67000330",
      "北區": "67000340",
      "安南區": "67000350",
      "安平區": "67000360",
      "中西區": "67000370"
    }
  },
  "高雄市": {
    "code": "E",
    "districts": {
      "鹽埕區": "64000010",
      "鼓山區": "64000020",
      "左營區": "64000030",
      "楠梓區": "64000040",
      "三民區": "64000050",
      "新興區": "64000060",
      "前金區": "64000070",
      "苓雅區": "64000080",
      "前鎮區": "64000090",
      "旗津區": "64000100",
      "小港區": "64000110",
      "鳳山區": "64000120",
      "林園區": "64000130",
      "大寮區": "64000140",
      "大樹區": "64000150",
      "大社區": "64000160",
      "仁武區": "64000170",
      "鳥松區": "64000180",
      "岡山區": "64000190",
      "橋頭區": "64000200",
      "燕巢區": "64000210",
      "田寮區": "64000220",
      "阿蓮區": "64000230",
      "路竹區": "64000240",
      "湖內區": "64000250",
      "茄萣區": "64000260",
      "永安區": "64000270",
      "彌陀區": "64000280",
      "梓官區": "64000290",
      "旗山區": "64000300",
      "美濃區": "64000310",
      "六龜區": "64000320",
      "甲仙區": "64000330",
      "杉林區": "64000340",
      "內門區": "64000350",
      "茂林區": "64000360",
      "桃源區": "64000370",
      "那瑪夏區": "64000380"
    }
  },
  "新北市": {
    "code": "F",
    "districts": {
      "板橋區": "65000010",
      "三重區": "65000020",
      "中和區": "65000030",
      "永和區": "65000040",
      "新莊區": "65000050",
      "新店區": "65000060",
      "樹林區": "65000070",
      "鶯歌區": "65000080",
      "三峽區": "65000090",
      "淡水區": "65000100",
      "汐止區": "65000110",
      "瑞芳區": "65000120",
      "土城區": "65000130",
      "蘆洲區": "65000140",
      "五股區": "65000150",
      "泰山區": "65000160",
      "林口區": "65000170",
      "深坑區": "65000180",
      "石碇區": "65000190",
      "坪林區": "65000200",
      "三芝區": "65000210",
      "石門區": "65000220",
      "八里區": "65000230",
      "平溪區": "65000240",
      "雙溪區": "65000250",
      "貢寮區": "65000260",
      "金山區": "65000270",
      "萬里區": "65000280",
      "烏來區": "65000290"
    }
  },
  "宜蘭縣": {
    "code": "G",
    "districts": {
      "宜蘭市": "10002010",
      "羅東鎮": "10002020",
      "蘇澳鎮": "10002030",
      "頭城鎮": "10002040",
      "礁溪鄉": "10002050",
      "壯圍鄉": "10002060",
      "員山鄉": "10002070",
      "冬山鄉": "10002080",
      "五結鄉": "10002090",
      "三星鄉": "10002100",
      "大同鄉": "10002110",
      "南澳鄉": "10002120"
    }
  },
  "桃園市": {
    "code": "H",
    "districts": {
      "桃園區": "68000010",
      "中壢區": "68000020",
      "大溪區": "68000030",
      "楊梅區": "68000040",
      "蘆竹區": "68000050",
      "大園區": "68000060",
      "龜山區": "68000070",
      "八德區": "68000080",
      "龍潭區": "68000090",
      "平鎮區": "68000100",
      "新屋區": "68000110",
      "觀音區": "68000120",
      "復興區": "68000130"
    }
  },
  "嘉義市": {
    "code": "I",
    "districts": {
      "東區": "10020010",
      "西區": "10020020"
    }
  },
  "新竹縣": {
    "code": "J",
    "districts": {
      "竹北市": "10004010",
      "竹東鎮": "10004020",
      "新埔鎮": "10004030",
      "關西鎮": "10004040",
      "湖口鄉": "10004050",
      "新豐鄉": "10004060",
      "芎林鄉": "10004070",
      "橫山鄉": "10004080",
      "北埔鄉": "10004090",
      "寶山鄉": "10004100",
      "峨眉鄉": "10004110",
      "尖石鄉": "10004120",
      "五峰鄉": "10004130"
    }
  },
  "苗栗縣": {
    "code": "K",
    "districts": {
      "苗栗市": "10005010",
      "苑裡鎮": "10005020",
      "通霄鎮": "10005030",
      "竹南鎮": "10005040",
      "頭份市": "10005050",
      "後龍鎮": "10005060",
      "卓蘭鎮": "10005070",
      "大湖鄉": "10005080",
      "公館鄉": "10005090",
      "銅鑼鄉": "10005100",
      "南庄鄉": "10005110",
      "頭屋鄉": "10005120",
      "三義鄉": "10005130",
      "西湖鄉": "10005140",
      "造橋鄉": "10005150",
      "三灣鄉": "10005160",
      "獅潭鄉": "10005170",
      "泰安鄉": "10005180"
    }
  },
  "南投縣": {
    "code": "M",
    "districts": {
      "南投市": "10008010",
      "埔里鎮": "10008020",
      "草屯鎮": "10008030",
      "竹山鎮": "10008040",
      "集集鎮": "10008050",
      "名間鄉": "10008060",
      "鹿谷鄉": "10008070",
      "中寮鄉": "10008080",
      "魚池鄉": "10008090",
      "國姓鄉": "10008100",
      "水里鄉": "10008110",
      "信義鄉": "10008120",
      "仁愛鄉": "10008130"
    }
  },
  "彰化縣": {
    "code": "N",
    "districts": {
      "彰化市": "10007010",
      "鹿港鎮": "10007020",
      "和美鎮": "10007030",
      "線西鄉": "10007040",
      "伸港鄉": "10007050",
      "福興鄉": "10007060",
      "秀水鄉": "10007070",
      "花壇鄉": "10007080",
      "芬園鄉": "10007090",
      "員林市": "10007100",
      "溪湖鎮": "10007110",
      "田中鎮": "10007120",
      "大村鄉": "10007130",
      "埔鹽鄉": "10007140",
      "埔心鄉": "10007150",
      "永靖鄉": "10007160",
      "社頭鄉": "10007170",
      "二水鄉": "10007180",
      "北斗鎮": "10007190",
      "二林鎮": "10007200",
      "田尾鄉": "10007210",
      "埤頭鄉": "10007220",
      "芳苑鄉": "10007230",
      "大城鄉": "10007240",
      "竹塘鄉": "10007250",
      "溪州鄉": "10007260"
    }
  },
  "新竹市": {
    "code": "O",
    "districts": {
      "東區": "10018010",
      "北區": "10018020",
      "香山區": "10018030"
    }
  },
  "雲林縣": {
    "code": "P",
    "districts": {
      "斗六市": "10009010",
      "斗南鎮": "10009020",
      "虎尾鎮": "10009030",
      "西螺鎮": "10009040",
      "土庫鎮": "10009050",
      "北港鎮": "10009060",
      "古坑鄉": "10009070",
      "大埤鄉": "10009080",
      "莿桐鄉": "10009090",
      "林內鄉": "10009100",
      "二崙鄉": "10009110",
      "崙背鄉": "10009120",
      "麥寮鄉": "10009130",
      "東勢鄉": "10009140",
      "褒忠鄉": "10009150",
      "臺西鄉": "10009160",
      "元長鄉": "10009170",
      "四湖鄉": "10009180",
      "口湖鄉": "10009190",
      "水林鄉": "10009200"
    }
  },
  "嘉義縣": {
    "code": "Q",
    "districts": {
      "太保市": "10010010",
      "朴子市": "10010020",
      "布袋鎮": "10010030",
      "大林鎮": "10010040",
      "民雄鄉": "10010050",
      "溪口鄉": "10010060",
      "新港鄉": "10010070",
      "六腳鄉": "10010080",
      "東石鄉": "10010090",
      "義竹鄉": "10010100",
      "鹿草鄉": "10010110",
      "水上鄉": "10010120",
      "中埔鄉": "10010130",
      "竹崎鄉": "10010140",
      "梅山鄉": "10010150",
      "番路鄉": "10010160",
      "大埔鄉": "10010170",
      "阿里山鄉": "10010180"
    }
  },
  "屏東縣": {
    "code": "T",
    "districts": {
      "屏東市": "10013010",
      "潮州鎮": "10013020",
      "東港鎮": "10013030",
      "恆春鎮": "10013040",
      "萬丹鄉": "10013050",
      "長治鄉": "10013060",
      "麟洛鄉": "10013070",
      "九如鄉": "10013080",
      "里港鄉": "10013090",
      "鹽埔鄉": "10013100",
      "高樹鄉": "10013110",
      "萬巒鄉": "10013120",
      "內埔鄉": "10013130",
      "竹田鄉": "10013140",
      "新埤鄉": "10013150",
      "枋寮鄉": "10013160",
      "新園鄉": "10013170",
      "崁頂鄉": "10013180",
      "林邊鄉": "10013190",
      "南州鄉": "10013200",
      "佳冬鄉": "10013210",
      "琉球鄉": "10013220",
      "車城鄉": "10013230",
      "滿州鄉": "10013240",
      "枋山鄉": "10013250",
      "三地門鄉": "10013260",
      "霧臺鄉": "10013270",
      "瑪家鄉": "10013280",
      "泰武鄉": "10013290",
      "來義鄉": "10013300",
      "春日鄉": "10013310",
      "獅子鄉": "10013320",
      "牡丹鄉": "10013330"
    }
  },
  "花蓮縣": {
    "code": "U",
    "districts": {
      "花蓮市": "10015010",
      "鳳林鎮": "10015020",
      "玉里鎮": "10015030",
      "新城鄉": "10015040",
      "吉安鄉": "10015050",
      "壽豐鄉": "10015060",
      "光復鄉": "10015070",
      "豐濱鄉": "10015080",
      "瑞穗鄉": "10015090",
      "富里鄉": "10015100",
      "秀林鄉": "10015110",
      "萬榮鄉": "10015120",
      "卓溪鄉": "10015130"
    }
  },
  "臺東縣": {
    "code": "V",
    "districts": {
      "臺東市": "10014010",
      "成功鎮": "10014020",
      "關山鎮": "10014030",
      "卑南鄉": "10014040",
      "鹿野鄉": "10014050",
      "池上鄉": "10014060",
      "東河鄉": "10014070",
      "長濱鄉": "10014080",
      "太麻里鄉": "10014090",
      "大武鄉": "10014100",
      "綠島鄉": "10014110",
      "海端鄉": "10014120",
      "延平鄉": "10014130",
      "金峰鄉": "10014140",
      "達仁鄉": "10014150",
      "蘭嶼鄉": "10014160"
    }
  },
  "金門縣": {
    "code": "W",
    "districts": {
      "金城鎮": "09020010",
      "金沙鎮": "09020020",
      "金湖鎮": "09020030",
      "金寧鄉": "09020040",
      "烈嶼鄉": "09020050",
      "烏坵鄉": "09020060"
    }
  },
  "澎湖縣": {
    "code": "X",
    "districts": {
      "馬公市": "10016010",
      "湖西鄉": "10016020",
      "白沙鄉": "10016030",
      "西嶼鄉": "10016040",
      "望安鄉": "10016050",
      "七美鄉": "10016060"
    }
  },
  "連江縣": {
    "code": "Z",
    "districts": {
      "南竿鄉": "09007010",
      "北竿鄉": "09007020",
      "莒光鄉": "09007030",
      "東引鄉": "09007040"
    }
  }
}


# ===== beitou/etl.py =====
"""依官方縣市代碼讀取買賣主檔；原始列與拒絕原因皆可追溯。"""
import csv
import hashlib
import io
import json
import math
import re
import unicodedata
import zipfile
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import requests


PING = 3.305785


def taipei_today():
    return datetime.now(timezone(timedelta(hours=8))).date()
FIELDS = {
    'district': '鄉鎮市區', 'subject': '交易標的', 'address': '土地位置建物門牌',
    'date': '交易年月日', 'building_type': '建物型態', 'use': '主要用途',
    'completion': '建築完成年月', 'area': '建物移轉總面積平方公尺',
    'price': '總價元', 'floor': '移轉層次', 'total_floors': '總樓層數',
    'parking_type': '車位類別', 'parking_area': '車位移轉總面積平方公尺',
    'parking_price': '車位總價元', 'remarks': '備註', 'serial': '編號',
    'counts': '交易筆棟數',
}
REQUIRED = set(FIELDS.values())


def norm(value):
    return unicodedata.normalize('NFKC', str(value or '')).strip().replace('臺北市', '台北市')


def roc_date(value, month_only=False):
    value = norm(value)
    if not value.isdigit() or len(value) not in (5, 7):
        raise ValueError('民國日期格式錯誤')
    if len(value) == 5 and not month_only:
        raise ValueError('交易日不可缺日')
    return date(int(value[:3]) + 1911, int(value[3:5]), int(value[5:7]) if len(value) == 7 else 1)


def number(value):
    value = norm(value).replace(',', '')
    result = float(value) if value else 0.0
    if not math.isfinite(result):
        raise ValueError('非有限數值')
    return result


def floor_number(value):
    value = norm(value).removesuffix('層')
    if re.fullmatch(r'[1-9][0-9]*', value):
        return int(value)
    digits = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}
    if value in digits:
        return digits[value]
    if re.fullmatch('[一二三四五六七八九]?十[一二三四五六七八九]?', value):
        a, b = value.split('十')
        return digits.get(a, 1) * 10 + digits.get(b, 0)
    raise ValueError('不支援地下/多層/特殊樓層')


def road_key(address, city='臺北市', district='北投區'):
    address = norm(address).replace('臺', '台')
    city = norm(canonical_city(city)).replace('臺', '台')
    district = district.replace('臺', '台')
    if address.startswith(city):
        address = address[len(city):]
    if not address.startswith(district):
        return ''
    address = address[len(district):]
    match = re.match(r'(.+?(?:大道|路|街)(?:[一二三四五六七八九十0-9]+段)?)', address)
    return match.group(1) if match else ''


def download(season, destination):
    if not re.fullmatch(r'1[0-9]{2}S[1-4]', season):
        raise ValueError('季別格式例如 114S4')
    url = 'https://plvr.land.moi.gov.tw/DownloadSeason'
    with requests.get(url, params={'season': season, 'type': 'zip', 'fileName': 'lvr_landcsv.zip'},
                      timeout=(10, 120), stream=True) as response:
        response.raise_for_status()
        chunks, size = [], 0
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            size += len(chunk)
            if size > 200_000_000:
                raise ValueError('下載超過 200 MB')
            chunks.append(chunk)
        payload = b''.join(chunks)
        source_url = response.url
    if not zipfile.is_zipfile(io.BytesIO(payload)):
        raise ValueError('回應不是有效 ZIP 或超過 200 MB；請從官方網頁手動下載')
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(payload)
    metadata = {'source_url': source_url, 'downloaded_at': datetime.now(timezone.utc).isoformat(),
                'sha256': hashlib.sha256(payload).hexdigest(), 'season': season}
    destination.with_suffix(destination.suffix + '.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding='utf-8')
    return metadata


def read_source(payload, filename, city='臺北市'):
    expected = filename_for_city(city)
    if len(payload) > 200_000_000:
        raise ValueError('檔案超過 200 MB')
    if filename.lower().endswith('.zip'):
        with zipfile.ZipFile(io.BytesIO(payload)) as archive:
            members = [i for i in archive.infolist() if Path(i.filename).name.lower() == expected]
            if len(members) != 1:
                raise ValueError(f'ZIP 必須恰有一份 {city} 買賣主檔 {expected}')
            if members[0].file_size > 100_000_000:
                raise ValueError('解壓後主檔超過 100 MB')
            payload = archive.read(members[0])
    elif Path(filename).name.lower() != expected:
        raise ValueError(f'目前選擇 {city}，CSV 必須是 {expected}，請勿改名混入其他縣市/租賃/預售檔')
    for encoding in ('utf-8-sig', 'cp950'):
        try:
            content = payload.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise ValueError('不支援的 CSV 編碼')
    csv.field_size_limit(10_000_000)
    reader = csv.DictReader(io.StringIO(content))
    reader.fieldnames = [norm(v) for v in (reader.fieldnames or [])]
    missing = REQUIRED - set(reader.fieldnames)
    if missing:
        raise ValueError('缺少必要欄位：' + '、'.join(sorted(missing)))
    return list(reader)


def clean(payload, filename, as_of=None, city='臺北市'):
    city = canonical_city(city)
    as_of = as_of or taipei_today()
    file_hash = hashlib.sha256(payload).hexdigest()
    output = []
    for line, raw in enumerate(read_source(payload, filename, city), start=2):
        if norm(raw.get('鄉鎮市區')).lower() == 'the villages and towns urban district':
            continue
        mapped = {k: norm(raw.get(v)) for k, v in FIELDS.items()}
        for official_district in REGIONS[city]['districts']:
            if official_district.replace('臺', '台') == mapped['district'].replace('臺', '台'):
                mapped['district'] = official_district
                break
        digest = hashlib.sha256((city + '\n' + json.dumps(raw, ensure_ascii=False, sort_keys=True)).encode()).hexdigest()
        record = {'id': digest, 'city': city, 'serial': mapped['serial'], 'file_hash': file_hash,
                  'source_file': Path(filename).name, 'source_line': line,
                  'raw_json': json.dumps(raw, ensure_ascii=False), 'district': mapped['district'],
                  'address': mapped['address'], 'road': road_key(mapped['address'], city, mapped['district']),
                  'building_type': mapped['building_type'], 'reasons': '', 'eligible': False}
        reasons = []
        if mapped['district'] not in REGIONS[city]['districts']:
            reasons.append('行政區不在所選縣市清單')
        if mapped['subject'] not in ('房地(土地+建物)', '房地(土地+建物)+車位'):
            reasons.append('非完整房地買賣')
        if mapped['use'] != '住家用':
            reasons.append('非住家用/用途不明')
        # 非空備註保守排除，避免只靠關鍵字漏掉特殊交易；人工複核另行處理。
        if mapped['remarks']:
            reasons.append('備註非空需人工複核')
        if not re.search(r'建物1(?:\D|$)', mapped['counts']):
            reasons.append('非單一建物/交易筆棟數不明')
        try:
            traded = roc_date(mapped['date'])
            built = roc_date(mapped['completion'], month_only=True)
            if not built <= traded <= as_of:
                raise ValueError('日期先後錯誤/未來交易')
            record.update(trade_date=traded.isoformat(), age=(traded - built).days / 365.25,
                          completion_date=built.isoformat())
        except ValueError:
            reasons.append('日期/屋齡缺失或異常')
        try:
            floor = floor_number(mapped['floor'])
            total_floors = floor_number(mapped['total_floors'])
            if floor > total_floors:
                raise ValueError('樓層超出總樓層')
            record.update(floor=floor, total_floors=total_floors)
        except ValueError:
            reasons.append('樓層缺失或特殊')
        try:
            if not mapped['area'] or not mapped['price']:
                raise ValueError('必要價格或面積缺失')
            area, price = number(mapped['area']), number(mapped['price'])
            pa, pp = number(mapped['parking_area']), number(mapped['parking_price'])
            has_parking = ('車位' in mapped['subject'] or bool(mapped['parking_type']) or pa > 0 or pp > 0)
            if has_parking and not (0 < pa < area and 0 < pp < price):
                reasons.append('車位面積/價格無法同時拆分')
            net_area, net_price = area - pa, price - pp
            if not (net_area >= 1 and net_price > 0 and pa >= 0 and pp >= 0):
                raise ValueError('價格/面積異常')
            unit = net_price / (net_area / PING) / 10000
            if not 1 <= unit <= 500:
                reasons.append('單價超出研究門檻1至500萬/坪')
            record.update(area_ping=net_area / PING, net_price=net_price, unit_wan=unit,
                          parking_price=pp, parking_area=pa)
        except (ValueError, OverflowError):
            reasons.append('價格/面積缺失或異常')
        if not record['road']:
            reasons.append('路段無法辨識')
        if not mapped['building_type']:
            reasons.append('建物型態缺失')
        record['reasons'] = '；'.join(reasons)
        record['eligible'] = not reasons
        output.append(record)
    return pd.DataFrame(output)


# ===== beitou/store.py =====
import json
from datetime import datetime, timezone

import pandas as pd
from sqlalchemy import Boolean, Column, Float, Integer, MetaData, String, Table, Text, create_engine, select

metadata = MetaData()
transactions = Table('transactions_v2', metadata,
    Column('id', String(64), primary_key=True), Column('city', Text, index=True), Column('serial', Text),
    Column('file_hash', String(64)), Column('source_file', Text), Column('source_line', Integer),
    Column('raw_json', Text), Column('district', Text), Column('address', Text), Column('road', Text),
    Column('building_type', Text), Column('reasons', Text), Column('eligible', Boolean),
    Column('trade_date', String(10)), Column('completion_date', String(10)), Column('age', Float),
    Column('floor', Float), Column('total_floors', Float), Column('area_ping', Float),
    Column('net_price', Float), Column('unit_wan', Float), Column('parking_price', Float), Column('parking_area', Float))
runs = Table('imports_v2', metadata, Column('id', Integer, primary_key=True),
    Column('imported_at', Text), Column('source', Text), Column('report', Text))


def connect(url):
    from sqlalchemy.pool import StaticPool
    options = {'pool_pre_ping': True}
    if url in ('sqlite://', 'sqlite:///:memory:'):
        options.update(poolclass=StaticPool, connect_args={'check_same_thread': False})
    engine = create_engine(url, **options)
    metadata.create_all(engine)
    return engine


def save(engine, frame, source):
    from sqlalchemy.dialects.sqlite import insert as sqlite_insert
    from sqlalchemy.dialects.postgresql import insert as pg_insert
    dialect = engine.dialect.name
    if dialect not in ('sqlite', 'postgresql'):
        raise ValueError('只支援 SQLite / PostgreSQL')
    insert = sqlite_insert if dialect == 'sqlite' else pg_insert
    report = {'input': len(frame), 'inserted': 0, 'duplicate': 0,
              'eligible_input': int(frame.eligible.sum()) if len(frame) else 0,
              'exclusions': frame.reasons.value_counts().to_dict() if len(frame) else {}}
    with engine.begin() as conn:
        for record in frame.to_dict('records'):
            record = {k: (None if pd.isna(v) else v) for k, v in record.items()}
            result = conn.execute(insert(transactions).values(**record).on_conflict_do_nothing(index_elements=['id']))
            report['inserted'] += result.rowcount
        report['duplicate'] = len(frame) - report['inserted']
        conn.execute(runs.insert().values(imported_at=datetime.now(timezone.utc).isoformat(), source=source,
                                         report=json.dumps(report, ensure_ascii=False)))
    return report


def load(engine, city=None, district=None):
    query = select(transactions)
    if city is not None:
        query = query.where(transactions.c.city == city)
    if district is not None:
        query = query.where(transactions.c.district == district)
    with engine.connect() as conn:
        return pd.DataFrame(conn.execute(query).mappings().all(), columns=[c.name for c in transactions.columns])


# ===== beitou/value.py =====
from dataclasses import dataclass
from datetime import date
import math

import pandas as pd



@dataclass
class Target:
    road: str
    building_type: str
    area_ping: float
    age: float
    floor: int
    total_floors: int
    as_of: date
    city: str = '臺北市'
    district: str = '北投區'


def estimate(frame, target):
    city = canonical_city(target.city)
    if target.district not in REGIONS[city]['districts']:
        raise ValueError('行政區不屬於所選縣市')
    if (not target.road.strip() or not target.building_type.strip()
            or not all(math.isfinite(v) for v in [target.area_ping, target.age, target.floor, target.total_floors])
            or target.area_ping <= 0 or target.age < 0 or not 1 <= target.floor <= target.total_floors):
        raise ValueError('待估條件不完整或超出範圍')
    rules = '同路段及型態、24個月內、坪數±25%、屋齡±10年、樓層±2；一樓/頂樓類別一致；至少5筆'
    result = {'status': '資料不足', 'rules': rules, 'count': 0, 'confidence': '不足',
              'unit_interval_wan': None, 'price_interval_wan': None,
              'method': '可比案例單價第25至75百分位×目標不含車位坪數；非統計信賴區間；無時間漲跌調整',
              'comparables': [], 'funnel': {}, 'as_of': target.as_of.isoformat(),
              'city': city, 'district': target.district}
    if frame.empty:
        return result
    versions = frame[(frame.city == city) & (frame.district == target.district)].drop_duplicates('id')
    pool = versions[versions.eligible == True].copy()
    # 同一官方編號出現不同版本時全部隔離；不擅自猜測哪一版為更正。
    serial = versions.serial.fillna('')
    conflicts = serial[(serial != '') & serial.duplicated(keep=False)]
    pool = pool[~pool.serial.isin(conflicts)]
    result['conflicting_serial_count'] = int(conflicts.nunique())
    result['funnel']['合格且無版本衝突'] = len(pool)
    dates = pd.to_datetime(pool.trade_date)
    days = (pd.Timestamp(target.as_of) - dates).dt.days
    masks = [
        ('同路段與型態', (pool.road == target.road.strip()) & (pool.building_type == target.building_type)),
        ('24個月內', (days >= 0) & (days <= 730)),
        ('坪數與屋齡', (pool.area_ping.between(target.area_ping * .75, target.area_ping * 1.25)) &
         (((pd.Timestamp(target.as_of) - pd.to_datetime(pool.completion_date)).dt.days / 365.25 - target.age).abs() <= 10)),
        ('樓層條件', ((pool.floor - target.floor).abs() <= 2) &
         ((pool.floor == 1) == (target.floor == 1)) &
         ((pool.floor == pool.total_floors) == (target.floor == target.total_floors))),
    ]
    for name, mask in masks:
        pool = pool.loc[mask.reindex(pool.index)]
        result['funnel'][name] = len(pool)
    pool = pool.sort_values(['trade_date', 'id'], ascending=[False, True]).head(30)
    result['count'] = len(pool)
    result['comparables'] = pool[['id', 'serial', 'city', 'district', 'address', 'trade_date', 'area_ping', 'age', 'floor',
                                  'unit_wan', 'net_price', 'file_hash', 'source_line']].to_dict('records')
    if len(pool) < 5:
        return result
    low, high = pool.unit_wan.quantile([.25, .75]).tolist()
    median = float(pool.unit_wan.median())
    result.update(status='可供研究', confidence='中' if len(pool) >= 10 and high / low <= 1.3 else '低',
                  unit_interval_wan=[low, high], price_interval_wan=[low * target.area_ping, high * target.area_ping],
                  median_unit_wan=median)
    return result


# ===== beitou/auto.py =====
"""有界的官方季度資料取得；不把下載失敗視為零成交。"""
import logging
import tempfile
from pathlib import Path



def candidate_seasons(as_of, count=3):
    quarter_index = as_of.year * 4 + (as_of.month - 1) // 3 - 1
    seasons = []
    for offset in range(count):
        year, quarter = divmod(quarter_index - offset, 4)
        seasons.append(f'{year - 1911}S{quarter + 1}')
    return seasons


def fetch_season(season, as_of, city='臺北市'):
    try:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'official.zip'
            meta = download(season, path)
            frame = clean(path.read_bytes(), path.name, as_of, city)
        if frame.empty:
            raise ValueError('該縣市檔案無紀錄')
        meta['city'] = city
        return {'ok': True, 'season': season, 'frame': frame, 'metadata': meta}
    except Exception:
        logging.exception('自動取得官方季別 %s 失敗', season)
        return {'ok': False, 'season': season, 'message': '官方資料暫不可取得、格式不符或該縣市無紀錄'}


# ===== beitou/finance.py =====
"""固定利率、本息平均攤還的情境試算；不代表銀行核貸。金額單位為元。"""
from dataclasses import asdict, dataclass
import math


def payment(principal, annual_rate, months):
    if not all(math.isfinite(v) for v in (principal, annual_rate, months)):
        raise ValueError('數值必須有限')
    if principal < 0 or annual_rate < 0 or months <= 0:
        raise ValueError('本金/利率不得為負且期數須大於零')
    if annual_rate == 0:
        return principal / months
    rate = annual_rate / 100 / 12
    return principal * rate / (-math.expm1(-months * math.log1p(rate)))


def amortize(principal, annual_rate, years, grace_years=0):
    if not isinstance(years, int) or not isinstance(grace_years, int) or not 0 <= grace_years < years <= 50:
        raise ValueError('年限須為整數，且 0 ≤ 寬限期 < 貸款年限 ≤ 50')
    total_months, grace_months = years * 12, grace_years * 12
    regular = payment(principal, annual_rate, total_months - grace_months)
    if principal == 0:
        return {'grace_payment': 0.0, 'regular_payment': 0.0, 'total_interest': 0.0,
                'total_paid': 0.0, 'schedule': []}
    balance, rows = principal, []
    for month in range(1, total_months + 1):
        interest = balance * annual_rate / 100 / 12
        repaid = 0.0 if month <= grace_months else min(balance, max(0.0, regular - interest))
        if month == total_months:
            repaid = balance
        balance = max(0.0, balance - repaid)
        rows.append({'month': month, 'payment': interest + repaid,
                     'principal': repaid, 'interest': interest, 'balance': balance})
    return {'grace_payment': principal * annual_rate / 100 / 12 if grace_months else 0.0,
            'regular_payment': regular, 'total_interest': sum(r['interest'] for r in rows),
            'total_paid': sum(r['payment'] for r in rows), 'schedule': rows}


@dataclass
class Purchase:
    price: float = 15_000_000
    down_payment: float = 3_750_000
    available_cash: float = 5_000_000
    transaction_cost: float = 750_000
    renovation_cost: float = 0
    monthly_income: float = 120_000
    monthly_living: float = 40_000
    monthly_other_debt: float = 0
    monthly_holding: float = 5_000
    annual_rate: float = 2.5
    years: int = 30
    grace_years: int = 0
    reserve_months: int = 6


def analyze_purchase(inputs):
    values = asdict(inputs)
    if not all(isinstance(v, (int, float)) and math.isfinite(v) and v >= 0 for v in values.values()):
        raise ValueError('所有輸入須為非負有限數值')
    if inputs.price <= 0 or inputs.monthly_income <= 0 or inputs.down_payment > inputs.price:
        raise ValueError('房價及月收入須大於零，頭期款不得超過房價')
    if not isinstance(inputs.reserve_months, int) or inputs.reserve_months < 1:
        raise ValueError('緊急預備金月份須為正整數')
    principal = inputs.price - inputs.down_payment
    loan = amortize(principal, inputs.annual_rate, inputs.years, inputs.grace_years)
    fixed_expenses = inputs.monthly_living + inputs.monthly_other_debt + inputs.monthly_holding
    monthly_expenses = fixed_expenses + loan['regular_payment']
    cash_needed = inputs.down_payment + inputs.transaction_cost + inputs.renovation_cost
    remaining = inputs.available_cash - cash_needed
    reserve_target = monthly_expenses * inputs.reserve_months
    scenarios = []
    for delta in (0.0, 0.5, 1.0, 2.0):
        rate = inputs.annual_rate + delta
        case = amortize(principal, rate, inputs.years, inputs.grace_years)
        scenarios.append({'rate_percent': rate, 'grace_payment': case['grace_payment'],
                          'regular_payment': case['regular_payment'], 'total_interest': case['total_interest'],
                          'monthly_surplus': inputs.monthly_income - fixed_expenses - case['regular_payment']})
    issues = []
    if remaining < 0:
        issues.append('購屋當下資金不足')
    if inputs.monthly_income - monthly_expenses < 0:
        issues.append('攤還期每月現金流為負')
    if remaining < reserve_target:
        issues.append('購屋後現金未達自訂緊急預備金目標')
    if loan['regular_payment'] / inputs.monthly_income > 1 / 3:
        issues.append('房貸月付超過月收入三分之一的規劃參考線（非核貸規則）')
    return {'inputs': values, 'principal': principal, 'loan_to_price_percent': principal / inputs.price * 100,
            'cash_needed': cash_needed, 'cash_remaining': remaining, 'reserve_target': reserve_target,
            'reserve_gap': max(0.0, reserve_target - remaining),
            'monthly_surplus': inputs.monthly_income - monthly_expenses,
            'grace_monthly_surplus': inputs.monthly_income - fixed_expenses - loan['grace_payment'] if inputs.grace_years else None,
            'mortgage_income_percent': loan['regular_payment'] / inputs.monthly_income * 100,
            'debt_income_percent': (loan['regular_payment'] + inputs.monthly_other_debt) / inputs.monthly_income * 100,
            'issues': issues, 'scenarios': scenarios, 'loan': loan}


# ===== app.py =====
import json
import os
import hmac
import logging
import tempfile
from datetime import date
from pathlib import Path

import streamlit as st
import pandas as pd



@st.cache_data(ttl=21600, max_entries=8, show_spinner=False)
def cached_official_season(season, as_of, city):
    # 只共用官方公開資料；訪客上傳與個別資料庫不進入共用快取。
    return fetch_season(season, as_of, city)

st.set_page_config(page_title='全台首購｜成交、房貸與現金流', page_icon='🏠', layout='wide')
st.title('全台首購｜成交、房貸與現金流')
st.caption('資料來源：內政部實價登錄公開買賣資料｜成交價研究｜不混用房仲刊登開價')
st.warning('估值為歷史可比成交分布，非鑑價、銀行核貸或保證成交價格。車位另計；屋況、產權、捷運步行距離均未查核。')
def setting(name, default=''):
    value = os.getenv(name)
    if value is not None:
        return value
    try:
        return st.secrets.get(name, default)
    except FileNotFoundError:
        return default


city = st.sidebar.selectbox('縣市', list(REGIONS), index=list(REGIONS).index('臺北市'), key='selected_city')
districts = list(REGIONS[city]['districts'])
default_district = '北投區' if city == '臺北市' else ('鼓山區' if city == '高雄市' else districts[0])
district = st.sidebar.selectbox('行政區', districts, index=districts.index(default_district), key='district_' + city)
st.caption(f'目前研究地區：{city} {district}')
database_url = setting('DATABASE_URL')
shared_database = bool(database_url)
if st.session_state.get('_schema_version') != 'national-v2':
    previous_engine = st.session_state.pop('_engine', None)
    if previous_engine is not None:
        previous_engine.dispose()
if '_engine' not in st.session_state:
    try:
        st.session_state['_engine'] = connect(database_url or 'sqlite://')
        st.session_state['_schema_version'] = 'national-v2'
    except Exception:
        logging.exception('資料庫初始化失敗')
        st.error('資料庫連線或快照初始化失敗，請由管理者檢查 Cloud logs 與 Secrets。')
        st.stop()
engine = st.session_state['_engine']
snapshot_done = st.session_state.setdefault('_snapshots_done', {})
if not shared_database and not snapshot_done.get(city):
    snapshot = Path(__file__).resolve().parent / 'data' / filename_for_city(city)
    if snapshot.exists():
        try:
            save(engine, clean(snapshot.read_bytes(), snapshot.name, city=city), 'repository snapshot')
        except Exception:
            logging.exception('所選縣市快照匯入失敗')
            st.warning('所選縣市的儲存庫快照無法匯入，將嘗試官方自動下載。')
    snapshot_done[city] = True
page = st.sidebar.radio('功能', ['資料匯入與品質', '成交查詢', '可比估值', '房貸試算', '家庭現金流'])
st.sidebar.markdown('[官方下載與授權](https://plvr.land.moi.gov.tw/DownloadOpenData)')
st.sidebar.caption(f'目前接受 {city} 買賣主檔 {filename_for_city(city)} 或含該主檔的官方 ZIP；不填入假行情。')
can_import = not shared_database
if shared_database:
    st.sidebar.info('共用資料庫模式：瀏覽者可查詢；匯入需要管理密碼。')
    expected_password = setting('IMPORT_PASSWORD')
    if expected_password:
        entered_password = st.sidebar.text_input('管理者匯入密碼', type='password')
        can_import = hmac.compare_digest(entered_password.encode(), str(expected_password).encode())
    else:
        st.sidebar.caption('管理密碼未設定，網頁匯入功能已關閉。')
else:
    st.sidebar.info('個人暫存模式：資料只在本次連線使用，重新整理或重啟後可能清空。')

auto_enabled = str(setting('AUTO_LOAD', 'true')).lower() in ('true', '1', 'yes')
if not shared_database and auto_enabled and page not in ('房貸試算', '家庭現金流'):
    st.sidebar.caption('首次開啟自動載入最近可取得的最多2季；官方資料快取6小時。')
    attempted = st.session_state.setdefault('_auto_done_by_city', {})
    stored_results = st.session_state.setdefault('_auto_results_by_city', {})
    if st.sidebar.button('重新取得官方資料'):
        cached_official_season.clear()
        attempted.pop(city, None)
        st.session_state['_auto_force'] = True
    if not attempted.get(city):
        attempted[city] = True
        force = st.session_state.pop('_auto_force', False)
        if force or load(engine, city).empty:
            results, successes = [], 0
            with st.spinner('正在自動取得內政部成交資料，首次載入可能需要一些時間…'):
                progress = st.empty()
                for auto_season in candidate_seasons(taipei_today()):
                    progress.info(f'正在取得 {city} {auto_season} 官方資料…')
                    item = cached_official_season(auto_season, taipei_today(), city)
                    if item['ok']:
                        report = save(engine, item['frame'], item['metadata']['source_url'])
                        results.append({'season': auto_season, 'ok': True,
                                        'metadata': item['metadata'], 'report': report})
                        successes += 1
                    else:
                        results.append({k: v for k, v in item.items() if k != 'frame'})
                    if successes == 2:
                        break
                progress.empty()
            stored_results[city] = results
    if stored_results.get(city):
        auto_results = stored_results[city]
        acquired = [x['season'] for x in auto_results if x['ok']]
        if acquired:
            st.success(f'已自動載入 {city} 官方資料：' + '、'.join(acquired))
            st.caption('這是近期可取得的季度資料，不代表完整兩年或即時行情；案例不足時仍不估價。')
        else:
            st.warning('官方自動下載暫時失敗。可按左側「重新取得官方資料」，或使用下方手動上傳；不代表沒有成交。')
        if any(not x['ok'] for x in auto_results) and acquired:
            st.warning('部分季別暫不可取得，已使用較早的可用資料；請核對實際載入季別。')
        with st.expander('自動取得紀錄與來源'):
            st.json(auto_results)
            st.download_button('下載自動取得紀錄', json.dumps(auto_results, ensure_ascii=False, indent=2), 'auto-source.json')

if page == '資料匯入與品質':
    st.subheader('下載或匯入官方公開資料')
    season = st.text_input('民國季別', '114S4')
    if st.button('下載並匯入指定季別', disabled=not can_import) and can_import:
        try:
            with st.spinner('下載並清洗資料中'):
                with tempfile.TemporaryDirectory() as folder:
                    path = Path(folder) / 'official.zip'
                    meta = download(season, path)
                    report = save(engine, clean(path.read_bytes(), path.name, city=city), meta['source_url'])
            st.success('匯入完成')
            st.json(report)
            st.json(meta)
            st.download_button('下載本次來源憑證', json.dumps(meta, ensure_ascii=False, indent=2), 'source.json')
        except Exception as exc:
            logging.exception('官方下載/匯入失敗')
            st.error('下載/匯入失敗，請檢查季別或改從官方網頁下載 ZIP 再上傳；詳細原因請管理者查看 Cloud logs。')
    uploaded = st.file_uploader(f'官方 ZIP 或 {filename_for_city(city)}', type=['zip', 'csv'], key='upload_' + city)
    if st.button('匯入上傳檔', disabled=uploaded is None or not can_import) and can_import:
        try:
            st.json(save(engine, clean(uploaded.getvalue(), uploaded.name, city=city), uploaded.name))
        except Exception as exc:
            logging.exception('上傳匯入失敗')
            st.error('匯入失敗，請確認來源、檔名與必要欄位；詳細原因請管理者查看 Cloud logs。')
    frame = load(engine, city, district)
    st.metric('所選地區原始交易版本數', len(frame))
    if len(frame):
        st.metric('清洗合格數（估值另檢查版本衝突）', int(frame.eligible.sum()))
        st.dataframe(frame.groupby(['eligible', 'reasons']).size().rename('筆數').reset_index(), hide_index=True)
        st.caption('備註非空一律需人工複核；因此一般文字備註也可能被保守排除。')
        st.dataframe(frame[['city', 'district', 'address', 'trade_date', 'eligible', 'reasons', 'file_hash', 'source_line']], hide_index=True)
    else:
        st.info(f'{city}{district} 目前沒有已載入的交易。這不表示沒有成交；請檢查來源與季別。')
elif page == '成交查詢':
    frame = load(engine, city, district)
    pool = frame[frame.eligible == True]
    if pool.empty:
        st.info('尚無合格成交資料，請先匯入官方買賣檔案。')
    else:
        road = st.selectbox('路段', ['全部'] + sorted(pool.road.unique().tolist()))
        if road != '全部':
            pool = pool[pool.road == road]
        st.caption('單價及總價已扣除可明確拆分的車位；成交查詢可能含隔離中的更正版本，估值會另行排除。')
        st.dataframe(pool[['city', 'district', 'road', 'building_type', 'trade_date', 'area_ping', 'unit_wan', 'net_price', 'age', 'floor']], hide_index=True)
        st.download_button('匯出查詢 CSV', pool.to_csv(index=False).encode('utf-8-sig'), 'transactions.csv', 'text/csv')
elif page == '可比估值':
    st.subheader('輸入待估房屋條件')
    local = load(engine, city, district)
    good = local[local.eligible == True]
    roads = sorted(good.road.dropna().unique().tolist())
    types = sorted(good.building_type.dropna().unique().tolist()) or ['公寓(5樓含以下無電梯)', '住宅大樓(11層含以上有電梯)', '華廈(10層含以下有電梯)', '透天厝']
    preferred_road = '中央北路三段' if city == '臺北市' and district == '北投區' else (roads[0] if roads else '')
    if roads:
        st.caption('已載入的合格成交路段：' + '、'.join(roads[:20]))
    with st.form('target'):
        road = st.text_input('完整路段（含段別）', preferred_road, key=f'road_{city}_{district}')
        kind = st.selectbox('建物型態（官方分類）', types, key=f'type_{city}_{district}')
        area = st.number_input('不含車位建物移轉面積（坪，含公設）', 1.0, 300.0, 28.0)
        age = st.number_input('估值日屋齡（年）', 0.0, 150.0, 40.0)
        floor = st.number_input('所在樓層', 1, 100, 2)
        floors = st.number_input('總樓層', 1, 100, 5)
        as_of = st.date_input('估值基準日', taipei_today())
        submit = st.form_submit_button('尋找可比成交並估值')
    if submit:
        try:
            result = estimate(local, Target(road, kind, area, age, floor, floors, as_of, city, district))
            st.write(result['rules'])
            st.json(result['funnel'])
            if result['status'] == '資料不足':
                st.warning(f"只有 {result['count']} 筆可比案例，至少需要5筆；不產生估價。")
            else:
                low, high = result['price_interval_wan']
                st.metric('不含車位研究區間', f'{low:,.0f} ～ {high:,.0f} 萬元')
                st.write('每坪區間（萬元）', result['unit_interval_wan'])
                st.write('證據充足度：' + result['confidence'])
            st.caption(result['method'])
            st.dataframe(result['comparables'], hide_index=True)
            st.download_button('下載估值證據 JSON', json.dumps(result, ensure_ascii=False, indent=2), 'valuation.json')
        except ValueError as exc:
            st.error(str(exc))
else:
    st.subheader(page + '｜可調整購屋情境')
    st.info('此頁不需先匯入成交資料。下列利率、費用及貸款條件均為使用者情境，不是銀行報價或核貸結果。')
    st.caption('家庭收入及購屋試算僅留在本次連線，不寫入成交資料庫；需要保存時可下載試算 JSON。')
    with st.form('purchase_scenario'):
        left, right = st.columns(2)
        with left:
            price_wan = st.number_input('購屋總價（萬元）', 1.0, 100000.0, 1500.0, key='buy_price')
            down_wan = st.number_input('頭期款（萬元，可調整）', 0.0, 100000.0, 375.0, key='buy_down')
            cash_wan = st.number_input('可動用購屋現金（萬元）', 0.0, 100000.0, 500.0, key='buy_cash')
            cost_wan = st.number_input('交易費用預留（萬元，非固定稅率）', 0.0, 10000.0, 75.0, key='buy_cost')
            renovation_wan = st.number_input('裝修與搬家預留（萬元）', 0.0, 10000.0, 0.0, key='buy_renovation')
            annual_rate = st.number_input('情境年利率（%）', 0.0, 20.0, 2.5, 0.1, key='buy_rate')
            years = st.number_input('貸款總年限（含寬限期）', 1, 50, 30, key='buy_years')
            grace = st.number_input('本金寬限期（年，0表示沒有）', 0, 49, 0, key='buy_grace')
        with right:
            income = st.number_input('家庭每月實領收入（元）', 1.0, 10000000.0, 120000.0, key='buy_income')
            living = st.number_input('每月生活費（元，不含房貸）', 0.0, 10000000.0, 40000.0, key='buy_living')
            debt = st.number_input('其他貸款每月還款（元）', 0.0, 10000000.0, 0.0, key='buy_debt')
            holding = st.number_input('每月持有成本預留（元）', 0.0, 1000000.0, 5000.0, key='buy_holding')
            reserve = st.number_input('緊急預備金目標（月）', 1, 36, 6, key='buy_reserve')
            st.caption('持有成本可含管理費、修繕、保險及房屋持有稅費月均預留；請避免與其他欄位重複計入。')
        submitted = st.form_submit_button('計算房貸與購屋現金流')
    if submitted:
        try:
            purchase = Purchase(price_wan * 10000, down_wan * 10000, cash_wan * 10000,
                                cost_wan * 10000, renovation_wan * 10000, income, living, debt, holding,
                                annual_rate, int(years), int(grace), int(reserve))
            st.session_state['_purchase_report'] = analyze_purchase(purchase)
        except ValueError as exc:
            st.session_state.pop('_purchase_report', None)
            st.error(str(exc))
    if '_purchase_report' not in st.session_state and not submitted:
        st.session_state['_purchase_report'] = analyze_purchase(Purchase())
    if '_purchase_report' in st.session_state:
        result = st.session_state['_purchase_report']
        loan = result['loan']
        st.caption('下列結果依最近一次試算條件顯示；修改上方欄位後請按計算更新。預設：房價1500萬、頭期款375萬、可動用現金500萬、月收入12萬。')
        a, b, c = st.columns(3)
        a.metric('貸款本金', f"{result['principal'] / 10000:,.1f} 萬元")
        b.metric('攤還期每月房貸', f"{loan['regular_payment']:,.0f} 元")
        c.metric('攤還期每月結餘', f"{result['monthly_surplus']:,.0f} 元")
        a, b, c = st.columns(3)
        a.metric('購屋後剩餘現金', f"{result['cash_remaining'] / 10000:,.1f} 萬元")
        b.metric('全期利息', f"{loan['total_interest'] / 10000:,.1f} 萬元")
        c.metric('房貸占收入', f"{result['mortgage_income_percent']:.1f}%")
        if result['inputs']['grace_years']:
            st.write(f"寬限期月付 {loan['grace_payment']:,.0f} 元；寬限期後月付 {loan['regular_payment']:,.0f} 元。")
            st.write(f"寬限期每月結餘 {result['grace_monthly_surplus']:,.0f} 元；本金並未在寬限期下降。")
        for issue in result['issues']:
            st.warning(issue)
        st.write(f"自訂緊急預備金目標 {result['reserve_target'] / 10000:,.1f} 萬元；與購屋後現金的缺口 {result['reserve_gap'] / 10000:,.1f} 萬元。")
        st.caption('預備金以生活費＋其他貸款＋持有成本＋寬限期後房貸，乘上指定月份估算。')
        st.write('利率壓力比較：基準、增加0.5、1與2個百分點，均假設該情境利率維持全期。')
        scenarios = pd.DataFrame(result['scenarios']).rename(columns={
            'rate_percent': '情境年利率(%)', 'grace_payment': '寬限期月付(元)',
            'regular_payment': '攤還期月付(元)', 'total_interest': '全期利息(元)', 'monthly_surplus': '攤還期月結餘(元)'})
        if not result['inputs']['grace_years']:
            scenarios = scenarios.drop(columns=['寬限期月付(元)'])
        st.dataframe(scenarios, hide_index=True)
        st.bar_chart(scenarios.set_index('情境年利率(%)')[['攤還期月付(元)']])
        if page == '家庭現金流':
            i = result['inputs']
            cash_table = pd.DataFrame({'項目': ['每月收入', '生活費', '其他貸款', '持有成本', '攤還期房貸', '每月結餘'],
                '金額（元）': [i['monthly_income'], -i['monthly_living'], -i['monthly_other_debt'],
                              -i['monthly_holding'], -loan['regular_payment'], result['monthly_surplus']]})
            st.dataframe(cash_table, hide_index=True)
            st.write(f"一次性資金需求：頭期款＋交易費用＋裝修搬家 = {result['cash_needed'] / 10000:,.1f} 萬元。")
            st.write(f"貸款占購屋總價 {result['loan_to_price_percent']:.1f}%；房貸及其他貸款合計占收入 {result['debt_income_percent']:.1f}%。")
        with st.expander('逐月攤還明細'):
            schedule = pd.DataFrame(loan['schedule']).rename(columns={'month': '期數', 'payment': '月付(元)',
                'principal': '本金(元)', 'interest': '利息(元)', 'balance': '剩餘本金(元)'})
            st.dataframe(schedule, hide_index=True)
            st.download_button('下載攤還明細 CSV', schedule.to_csv(index=False).encode('utf-8-sig'), 'mortgage-schedule.csv')
        st.download_button('下載購屋試算 JSON', json.dumps(result, ensure_ascii=False, indent=2), 'purchase-scenario.json')
        st.caption('本息平均攤還、按月計息、全期固定利率；銀行逐日計息、四捨五入、浮動利率與額外費用可能不同。寬限期包含在總年限內；不模擬提前清償。')
        st.markdown('[金管會金融智慧網：房貸與寬限期說明](https://moneywise.fsc.gov.tw/uploaddowndoc?file=publicizeinfo%2F202109241416010.pdf&filedisplay=%E9%8A%80%E8%A1%8C%E7%AF%87.pdf&flag=doc)')
