import datetime
import logging
from . import api
import locale

locale.setlocale(locale.LC_ALL, 'vi_VN.UTF-8')
_LOGGER = logging.getLogger(__name__)

class AddSensor:
    def __init__(self, makhach='xxx'):
        self._state = 'n/a'
        self._makhach = makhach
        self._attribute = {}

    @property
    def state(self):
        return self._state

    @property
    def attribute(self):
        return self._attribute

class SensorAttribute(AddSensor):
    def get_evnhanoi(self):
        api = api.EVNHN()
        data_out = api.get_evn_hanoi(self._makhach)
        self._state = data_out['state']
        self._attribute["state_class"] = 'measurement'
        today_date = datetime.datetime.now()
        sanluong_thangtruocnua = 'Tháng ' + data_out['thang_truoc_nua'] + ': ' + data_out['sanluong_thangtruocnua'] + ' kWh'
        sanluong_thangtruoc = 'Tháng ' + data_out['thang_truoc'] + ': ' + data_out['sanluong_thangtruoc'] + ' kWh'
        sanluong_thangnay = 'Tháng ' + data_out['thang_nay'] + ': ' + data_out['sanluong_thangnay'] + ' kWh'
        tien_thangtruocnua = 'Tháng ' + data_out['thang_truoc_nua'] + ':' + data_out['tiendien_thangtruocnua']
        tien_thangtruoc = 'Tháng ' + data_out['thang_truoc'] + ':' + data_out['tiendien_thangtruoc']
        tien_thangnay = 'Tháng ' + data_out['thang_nay'] + ':' + data_out['tiendien_thangnay']
        self._attribute["last_reset"] = today_date.strftime("%d/%m/%Y - %H:%M:%S")
        self._attribute["ma_khach"] = self._makhach
        self._attribute["ma_ddo"] = data_out['ma_ddo']
        self._attribute["sanluong_day1"] = data_out['sanluong_day1']
        self._attribute["sanluong_day2"] = data_out['sanluong_day2']
        self._attribute["sanluong_day3"] = data_out['sanluong_day3']
        self._attribute["thang_truocnua"] = data_out['thang_truoc_nua']
        self._attribute["thang_truoc"] = data_out['thang_truoc']
        self._attribute["thang_nay"] = data_out['thang_nay']
#        self._attribute["sanluong_thangtruocnua"] = data_out['sanluong_thangtruocnua']
#        self._attribute["sanluong_thangtruoc"] = data_out['sanluong_thangtruoc']
#        self._attribute["sanluong_thangnay"] = data_out['sanluong_thangnay']
        self._attribute["sanluong_thangtruocnua"] = sanluong_thangtruocnua
        self._attribute["sanluong_thangtruoc"] = sanluong_thangtruoc
        self._attribute["sanluong_thangnay"] = sanluong_thangnay
        self._attribute["tien_thangtruocnua"] = tien_thangtruocnua
        self._attribute["tien_thangtruoc"] = tien_thangtruoc
        self._attribute["tien_thangnay"] = tien_thangnay
#        self._attribute["tien_thangtruocnua"] = data_out['tiendien_thangtruocnua']
#        self._attribute["tien_thangtruoc"] = data_out['tiendien_thangtruoc']
#        self._attribute["tien_thangnay"] = data_out['tiendien_thangnay']
        self._attribute["thanhtoan_thangnay"] = data_out['thanhtoan_thangnay']


