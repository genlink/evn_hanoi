"""
A python module to the newest version number of Home Assistant.

This code is released under the terms of the MIT license. See the LICENSE
file for more details.
"""
import datetime
import logging
import requests, json, time
from bs4 import BeautifulSoup
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import locale

locale.setlocale(locale.LC_ALL, 'vi_VN.UTF-8')

class EVNHN:

    INTERVAL_6MIN = "6min"
    INTERVAL_DAY = "day"

    def next_month(self):
        today_date = datetime.datetime.now()
        d = today_date+relativedelta(day=31)
        next_month = d+ datetime.timedelta(days=1)
        next_month = next_month.strftime("%m")
        return next_month
    def get_hdon_tracuu(self,makhachhang,thang,nam):
        self.mainURL = 'http://42.112.213.225:8050/Service.asmx/'
        self.makhachhang = makhachhang
        self.thang = thang
        self.nam = nam
        next_month = self.next_month()
        url = self.mainURL+'get_hdon_tracuu?ma_kh='+self.makhachhang+'&nam='+str(self.nam)+'&thang='+str(self.thang)+'&thangsau='+next_month
        data = requests.get(url)
        data = BeautifulSoup(data.text, 'xml')
        check = data.find('NewDataSet')
        if not check : 
            tt_tiendien = 'Chưa cập nhật'
            tt_san_luong = 'Chưa cập nhật'
            kt_thanh_toan = 'Chưa cập nhật'
        else :
            tt_san_luong = data.find('SAN_LUONG')
            tt_san_luong = tt_san_luong.text+ 'kWh'
            tt_tiendien = data.find('TONG_TIEN')
            tt_tiendien = tt_tiendien.tex
            kt_thanh_toan = tt_tiendien
        return tt_tiendien,kt_thanh_toan,tt_san_luong
    def get_hdon_ttoan(self,makhachhang,thang,nam):
        self.mainURL = 'http://42.112.213.225:8050/Service.asmx/'
        self.makhachhang = makhachhang
        self.thang = thang
        self.nam = nam
        url_tt_hoadon = self.mainURL+'get_hdon_ttoan?ma_kh='+self.makhachhang+'&ky=1&thang='+str(self.thang)+'&nam='+str(self.nam)
        tt_hoadon = requests.get(url_tt_hoadon)
        tt_hoadon = BeautifulSoup(tt_hoadon.text, 'xml')
        check = tt_hoadon.find('NewDataSet')
        if not check :
            data = self.get_hdon_tracuu(self.makhachhang,self.thang,self.nam)
            tt_tiendien = data[0]
            kt_thanh_toan = data[1]
            tt_san_luong = data[2]
        else :
            tt_tiendien = tt_hoadon.find('TONG_TIEN')
            tt_tiendien = tt_tiendien.text
            kt_thanh_toan = tt_hoadon.find('TIEN_NO')
            kt_thanh_toan = kt_thanh_toan.text
            tt_san_luong = tt_hoadon.find('DIEN_TTHU')
            tt_san_luong = tt_san_luong.text+' kWh'
        return tt_tiendien,kt_thanh_toan,tt_san_luong
    def _get_details(self,makhachhang):
        self.makhachhang = makhachhang
        self.mainURL = 'http://42.112.213.225:8050/Service.asmx/'
        url_ma_ddo = self.mainURL + 'CHECK_DDO?ma_kh=' + self.makhachhang
        ma_ddo = requests.get(url_ma_ddo)
        ma_ddo = ma_ddo.text
        ma_ddo = ma_ddo.split('<MA_DDO>')
        ma_ddo = ma_ddo[1][:ma_ddo[1].find('</MA_DDO')]
        today_date = datetime.datetime.now()
        past_day = today_date - datetime.timedelta(days=3)
        url_sanluong_day = self.mainURL+'GET_THONGSO_VANHANH_SANLUONG_THEONGAY?ma_ddo='+ma_ddo+'&tu_ngay='+past_day.strftime("%d/%m/%Y")+'&den_ngay='+today_date.strftime("%d/%m/%Y")
        sanluong_day = requests.get(url_sanluong_day)
        sanluong_day = BeautifulSoup(sanluong_day.text, 'xml')
        sanluong_day = sanluong_day.find_all("CHI_SO")
        dem = len(sanluong_day)
        if dem == 3:
            sanluong_day.append(sanluong_day[2])
        sanluong_day1 = round(float(sanluong_day[3].text) - float(sanluong_day[2].text),2)
        sanluong_day2 = round(float(sanluong_day[2].text) - float(sanluong_day[1].text),2)
        sanluong_day3 = round(float(sanluong_day[1].text) - float(sanluong_day[0].text),2)
        '''Lay thong tin hoa don 3 thang gan nhat'''
        nam_hientai = today_date.year
        thang = [today_date.strftime("%m")]
        for _ in range(0, 2):
            today_date = today_date.replace(day=1) - datetime.timedelta(days=1)
            thang.append(today_date.strftime("%m"))
        tien_dien =[]
        thanh_toan = []
        san_luong = []
#        thang[0] = '03'
#        thang[1] = '02'
#        thang[2] = '01'
        if int(thang[0]) == 1:
            for num in range(11,14):
                today_date = datetime.datetime.now()
                nam_hientai = today_date.year
                nam_hientai = nam_hientai-1
                if num ==13:
                    today_date = datetime.datetime.now()
                    nam_hientai = today_date.year
                    currentMonth = 1
                else: 
                    currentMonth = num
                data = self.get_hdon_ttoan(self.makhachhang,currentMonth,nam_hientai)
                tt_tiendien = data[0]
                kt_thanh_toan = data[1]
                tt_san_luong = data[2]
                tien_dien.append(tt_tiendien)
                thanh_toan.append(kt_thanh_toan)
                san_luong.append(tt_san_luong)
        if int(thang[0]) == 2:
            for num in range(12,15):
                today_date = datetime.datetime.now()
                nam_hientai = today_date.year
                nam_hientai = nam_hientai-1
                if num ==13:
                    today_date = datetime.datetime.now()
                    nam_hientai = today_date.year
                    currentMonth = 1
                elif num == 14:
                    today_date = datetime.datetime.now()
                    nam_hientai = today_date.year
                    currentMonth = 2
                else: 
                    currentMonth = num
                data = self.get_hdon_ttoan(self.makhachhang,currentMonth,nam_hientai)
                tt_tiendien = data[0]
                kt_thanh_toan = data[1]
                tt_san_luong = data[2]
                tien_dien.append(tt_tiendien)
                thanh_toan.append(kt_thanh_toan)
                san_luong.append(tt_san_luong)
        for num in range(int(thang[2]),int(thang[0])+1):
            data = self.get_hdon_ttoan(self.makhachhang,num,nam_hientai)
            tt_tiendien = data[0]
            kt_thanh_toan = data[1]
            tt_san_luong = data[2]
            tien_dien.append(tt_tiendien)
            thanh_toan.append(kt_thanh_toan)
            san_luong.append(tt_san_luong)
        thang.reverse()
        for i in range(len(thanh_toan)):
            if thanh_toan[i] == '0' :
                thanh_toan[i] = 'Đã thanh toán'
            elif thanh_toan[i] == 'Chưa cập nhật':
                thanh_toan[i] = 'Chưa cập nhật'
            else:
                thanh_toan[i] = 'Chưa thanh toán '+thanh_toan[i]

#        tien_thangtruocnua = locale.currency(float(tien_dien[0]), grouping=True)
#        tien_thangtruoc = locale.currency(float(tien_dien[1]), grouping=True)
#        tien_thangnay = locale.currency(float(tien_dien[2]), grouping=True)
        json_data = {
            'state': sanluong_day1,
            'ma_ddo': ma_ddo,
            'sanluong_day1': sanluong_day1,
            'sanluong_day2': sanluong_day2,
            'sanluong_day3': sanluong_day3,
            'thang_truoc_nua': thang[0],
            'thang_truoc': thang[1],
            'thang_nay': thang[2],
            'sanluong_thangtruocnua': san_luong[0],
            'sanluong_thangtruoc': san_luong[1],
            'sanluong_thangnay': san_luong[2],
            'tiendien_thangtruocnua': tien_dien[0],
            'tiendien_thangtruoc': tien_dien[1],
            'tiendien_thangnay': tien_dien[2],
            'thanhtoan_thangtruocnua': thanh_toan[0],
            'thanhtoan_thangtruoc': thanh_toan[1],
            'thanhtoan_thangnay': thanh_toan[2]
        }
        return json_data

    def get_evn_hanoi(self,makhachhang):
        return self._get_details(makhachhang)


