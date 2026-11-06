# 完整單檔：成交自動取得、可比估值、房貸與家庭現金流
# ===== beitou/etl.py =====
"""只接受臺北市買賣主檔；原始列與拒絕原因皆可追溯。"""
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


def road_key(address):
    match = re.search(r'(?:台北市)?北投區(.+?(?:路|街|大道)(?:[一二三四五六七八九十0-9]+段)?)', norm(address))
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


def read_source(payload, filename):
    if len(payload) > 200_000_000:
        raise ValueError('檔案超過 200 MB')
    if filename.lower().endswith('.zip'):
        with zipfile.ZipFile(io.BytesIO(payload)) as archive:
            members = [i for i in archive.infolist() if Path(i.filename).name.lower() == 'a_lvr_land_a.csv']
            if len(members) != 1:
                raise ValueError('ZIP 必須恰有一份臺北市買賣主檔 a_lvr_land_a.csv')
            if members[0].file_size > 100_000_000:
                raise ValueError('解壓後主檔超過 100 MB')
            payload = archive.read(members[0])
    elif Path(filename).name.lower() != 'a_lvr_land_a.csv':
        raise ValueError('CSV 請使用官方原名 a_lvr_land_a.csv，避免混入其他縣市/租賃/預售檔')
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


def clean(payload, filename, as_of=None):
    as_of = as_of or taipei_today()
    file_hash = hashlib.sha256(payload).hexdigest()
    output = []
    for line, raw in enumerate(read_source(payload, filename), start=2):
        if norm(raw.get('鄉鎮市區')).lower() == 'the villages and towns urban district':
            continue
        mapped = {k: norm(raw.get(v)) for k, v in FIELDS.items()}
        digest = hashlib.sha256(json.dumps(raw, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
        record = {'id': digest, 'serial': mapped['serial'], 'file_hash': file_hash,
                  'source_file': Path(filename).name, 'source_line': line,
                  'raw_json': json.dumps(raw, ensure_ascii=False), 'district': mapped['district'],
                  'address': mapped['address'], 'road': road_key(mapped['address']),
                  'building_type': mapped['building_type'], 'reasons': '', 'eligible': False}
        reasons = []
        if mapped['district'] != '北投區':
            reasons.append('非北投區')
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
transactions = Table('transactions', metadata,
    Column('id', String(64), primary_key=True), Column('serial', Text),
    Column('file_hash', String(64)), Column('source_file', Text), Column('source_line', Integer),
    Column('raw_json', Text), Column('district', Text), Column('address', Text), Column('road', Text),
    Column('building_type', Text), Column('reasons', Text), Column('eligible', Boolean),
    Column('trade_date', String(10)), Column('completion_date', String(10)), Column('age', Float),
    Column('floor', Float), Column('total_floors', Float), Column('area_ping', Float),
    Column('net_price', Float), Column('unit_wan', Float), Column('parking_price', Float), Column('parking_area', Float))
runs = Table('imports', metadata, Column('id', Integer, primary_key=True),
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


def load(engine):
    with engine.connect() as conn:
        return pd.DataFrame(conn.execute(select(transactions)).mappings().all(), columns=[c.name for c in transactions.columns])


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


def estimate(frame, target):
    if (not target.road.strip() or not target.building_type.strip()
            or not all(math.isfinite(v) for v in [target.area_ping, target.age, target.floor, target.total_floors])
            or target.area_ping <= 0 or target.age < 0 or not 1 <= target.floor <= target.total_floors):
        raise ValueError('待估條件不完整或超出範圍')
    rules = '同路段及型態、24個月內、坪數±25%、屋齡±10年、樓層±2；一樓/頂樓類別一致；至少5筆'
    result = {'status': '資料不足', 'rules': rules, 'count': 0, 'confidence': '不足',
              'unit_interval_wan': None, 'price_interval_wan': None,
              'method': '可比案例單價第25至75百分位×目標不含車位坪數；非統計信賴區間；無時間漲跌調整',
              'comparables': [], 'funnel': {}, 'as_of': target.as_of.isoformat()}
    if frame.empty:
        return result
    versions = frame.drop_duplicates('id')
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
    result['comparables'] = pool[['id', 'serial', 'address', 'trade_date', 'area_ping', 'age', 'floor',
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


def fetch_season(season, as_of):
    try:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'official.zip'
            meta = download(season, path)
            frame = clean(path.read_bytes(), path.name, as_of)
        if frame.empty or not (frame.district == '北投區').any():
            raise ValueError('無北投區紀錄')
        return {'ok': True, 'season': season, 'frame': frame, 'metadata': meta}
    except Exception:
        logging.exception('自動取得官方季別 %s 失敗', season)
        return {'ok': False, 'season': season, 'message': '官方資料暫不可取得、格式不符或無北投紀錄'}


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
def cached_official_season(season, as_of):
    # 只共用官方公開資料；訪客上傳與個別資料庫不進入共用快取。
    return fetch_season(season, as_of)

st.set_page_config(page_title='北投首購｜成交與房貸', page_icon='🏠', layout='wide')
st.title('北投區首購｜成交、房貸與現金流')
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


database_url = setting('DATABASE_URL')
shared_database = bool(database_url)
if '_engine' not in st.session_state:
    try:
        st.session_state['_engine'] = connect(database_url or 'sqlite://')
        snapshot = Path(__file__).resolve().parent / 'data' / 'a_lvr_land_a.csv'
        if not shared_database and snapshot.exists():
            save(st.session_state['_engine'], clean(snapshot.read_bytes(), snapshot.name), 'repository snapshot')
    except Exception:
        logging.exception('資料庫初始化失敗')
        st.error('資料庫連線或快照初始化失敗，請由管理者檢查 Cloud logs 與 Secrets。')
        st.stop()
engine = st.session_state['_engine']
page = st.sidebar.radio('功能', ['資料匯入與品質', '成交查詢', '可比估值', '房貸試算', '家庭現金流'])
st.sidebar.markdown('[官方下載與授權](https://plvr.land.moi.gov.tw/DownloadOpenData)')
st.sidebar.caption('只接受官方臺北市買賣主檔；空白畫面不會自動填入假行情。')
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
    if st.sidebar.button('重新取得官方資料'):
        cached_official_season.clear()
        st.session_state.pop('_auto_attempted', None)
        st.session_state['_auto_force'] = True
    if not st.session_state.get('_auto_attempted'):
        st.session_state['_auto_attempted'] = True
        force = st.session_state.pop('_auto_force', False)
        if force or load(engine).empty:
            results, successes = [], 0
            with st.spinner('正在自動取得內政部成交資料，首次載入可能需要一些時間…'):
                progress = st.empty()
                for auto_season in candidate_seasons(taipei_today()):
                    progress.info(f'正在取得 {auto_season} 官方資料…')
                    item = cached_official_season(auto_season, taipei_today())
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
            st.session_state['_auto_results'] = results
    if st.session_state.get('_auto_results'):
        auto_results = st.session_state['_auto_results']
        acquired = [x['season'] for x in auto_results if x['ok']]
        if acquired:
            st.success('已自動載入官方資料：' + '、'.join(acquired))
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
                    report = save(engine, clean(path.read_bytes(), path.name), meta['source_url'])
            st.success('匯入完成')
            st.json(report)
            st.json(meta)
            st.download_button('下載本次來源憑證', json.dumps(meta, ensure_ascii=False, indent=2), 'source.json')
        except Exception as exc:
            logging.exception('官方下載/匯入失敗')
            st.error('下載/匯入失敗，請檢查季別或改從官方網頁下載 ZIP 再上傳；詳細原因請管理者查看 Cloud logs。')
    uploaded = st.file_uploader('官方 ZIP 或 a_lvr_land_a.csv', type=['zip', 'csv'])
    if st.button('匯入上傳檔', disabled=uploaded is None or not can_import) and can_import:
        try:
            st.json(save(engine, clean(uploaded.getvalue(), uploaded.name), uploaded.name))
        except Exception as exc:
            logging.exception('上傳匯入失敗')
            st.error('匯入失敗，請確認來源、檔名與必要欄位；詳細原因請管理者查看 Cloud logs。')
    frame = load(engine)
    st.metric('資料庫原始交易版本數', len(frame))
    if len(frame):
        st.metric('清洗合格數（估值另檢查版本衝突）', int(frame.eligible.sum()))
        st.dataframe(frame.groupby(['eligible', 'reasons']).size().rename('筆數').reset_index(), hide_index=True)
        st.caption('備註非空一律需人工複核；因此一般文字備註也可能被保守排除。')
        st.dataframe(frame[['address', 'trade_date', 'eligible', 'reasons', 'file_hash', 'source_line']], hide_index=True)
elif page == '成交查詢':
    frame = load(engine)
    pool = frame[frame.eligible == True]
    if pool.empty:
        st.info('尚無合格成交資料，請先匯入官方買賣檔案。')
    else:
        road = st.selectbox('路段', ['全部'] + sorted(pool.road.unique().tolist()))
        if road != '全部':
            pool = pool[pool.road == road]
        st.caption('單價及總價已扣除可明確拆分的車位；成交查詢可能含隔離中的更正版本，估值會另行排除。')
        st.dataframe(pool[['road', 'building_type', 'trade_date', 'area_ping', 'unit_wan', 'net_price', 'age', 'floor']], hide_index=True)
        st.download_button('匯出查詢 CSV', pool.to_csv(index=False).encode('utf-8-sig'), 'transactions.csv', 'text/csv')
elif page == '可比估值':
    st.subheader('輸入待估房屋條件')
    with st.form('target'):
        road = st.text_input('完整路段（含段別，例如中央北路三段）', '中央北路三段')
        kind = st.text_input('建物型態（須與官方資料完全一致）', '公寓(5樓含以下無電梯)')
        area = st.number_input('不含車位建物移轉面積（坪，含公設）', 1.0, 300.0, 28.0)
        age = st.number_input('估值日屋齡（年）', 0.0, 150.0, 40.0)
        floor = st.number_input('所在樓層', 1, 100, 2)
        floors = st.number_input('總樓層', 1, 100, 5)
        as_of = st.date_input('估值基準日', taipei_today())
        submit = st.form_submit_button('尋找可比成交並估值')
    if submit:
        try:
            result = estimate(load(engine), Target(road, kind, area, age, floor, floors, as_of))
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
