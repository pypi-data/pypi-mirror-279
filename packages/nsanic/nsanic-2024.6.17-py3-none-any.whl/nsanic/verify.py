import datetime
import re

from nsanic.libs.tool_dt import to_datetime, dt_str


def password(pwd_str: str, len_min=6, len_max=18, qc=2):
    """
    统一密码校验
    :param pwd_str: 待校验的字符串
    :param len_min: 最小长度
    :param len_max: 最大长度
    :param qc: 密码复杂度 取值1-4
    """
    if not isinstance(pwd_str, str):
        pwd_str = str(pwd_str)
    if len_max >= len(pwd_str) >= len_min:
        sign = [0, 0, 0, 0]
        for i in pwd_str:
            ord_id = ord(i)
            if 33 <= ord_id <= 126:
                if (not sign[0]) and (48 <= ord_id <= 57):
                    sign[0] = 1
                elif (not sign[1]) and (65 <= ord_id <= 90):
                    sign[1] = 1
                elif (not sign[2]) and (97 <= ord_id <= 122):
                    sign[2] = 1
                elif not sign[3]:
                    sign[3] = 1
            else:
                return 0, f'Contains invalid characters:{i}'
        if sum(sign) < qc:
            return 0, '密码应包含数字、大小写字母、特殊符号中的至少两种'
        return 1, ''
    return 0, '密码长度应是6到18位'


def common_str(item_str: str, start_letter=True):
    """常规字符串校验 以字母开头 只包含数字字母下划线"""
    num_letter = re.compile("^[0-9a-zA-Z_]+$")
    if num_letter.search(item_str):
        if start_letter:
            first = re.compile('^[a-zA-Z]')
            if first.search(item_str):
                return True
        else:
            return True
    return False


def color(color_str: str):
    return True if re.match(r'^#[A-F0-9]', color_str) else False


def phone(phone_str: str):
    return True if re.match(r'^1[3-9]\d{9}', phone_str) else False


def extra_model(new_model: dict, default: dict, old_model: dict = None):
    """统一处理扩展字段检查"""
    if (not default) and (not old_model):
        return new_model
    if not old_model:
        old_model = {}
    if not default:
        default = {}
    new_extra = {}
    for k in new_model:
        v = default.get(k)
        old_v = old_model.get(k)
        new_extra[k] = v if old_v != v else old_v
    return new_extra


def vint(val, require=False, default=None, minval: int = None, maxval: int = None, inner=True, p_name=''):
    """
    整形参数校验

    :param val: 待校验值
    :param require: 是否必要参数 默认非必要
    :param default: 非必要状态下的默认值
    :param minval: 最小值范围 type--int 默认不校验
    :param maxval: 最大值范围 type--int 默认不校验
    :param inner: 是否范围内(针对于min_val或max_val有值校验)，默认范围内，False为范围外
    :param p_name: 参数名
    :return 状态, 值/失败原因
    """
    if val in ('', None, 'None', [], {}, 'null', 'NULL', 'Null'):
        if require:
            return False, f'缺少必要参数：{p_name}'
        return True, default
    if not isinstance(val, int):
        try:
            if isinstance(val, str):
                val = val.split('.')[0]
            val = int(val)
        except(ValueError, TypeError, SyntaxError):
            return False, f'{p_name}参数值无法解析成整形'
    if inner:
        if (minval is not None) and (val < minval):
            return False, f'{p_name}参数值小于限制的最小值:{minval}'
        if (maxval is not None) and (val > maxval):
            return False, f'{p_name}参数值大于限制的最大值:{maxval}'
    else:
        if (minval is not None) and (maxval is not None) and (minval < val < maxval):
            return False, f'{p_name}参数值不在指定的限制范围'
    return True, val


def vstr(val, require=False, default: str = None, turn=0, minlen: int = None, maxlen: int = None, p_name=''):
    """
    字符串参数校验

    :param val: 待校验对象
    :param require: 是否必要参数 默认非必要
    :param default: 非必要状态下的默认值
    :param turn: 默认转换 1--全转化大写 2--全转换小写 3--首字母大写 其它值--不转化
    :param minlen: 最小长度 type--int 默认不校验
    :param maxlen: 最大长度 type--int 默认不校验
    :param p_name: 参数名
    """
    if isinstance(val, str):
        val = val.strip()
    if val in ('', None, 'None', [], {}, 'null', 'NULL', 'Null'):
        if require:
            return False, f'缺少必要参数：{p_name}'
        return True, default
    if not isinstance(val, str):
        val = str(val)
    len_val = len(val)
    if turn == 1:
        val = val.upper()
    elif turn == 2:
        val = val.lower()
    elif turn == 3:
        val = f'{val[0].upper()}{val[1:]}' if len_val > 1 else val.upper()
    if (not minlen) and (not maxlen):
        return True, val
    if minlen and (len_val < minlen):
        return False, f'{p_name}参数值长度小于的限制最小长度{minlen}'
    if maxlen and (len_val > maxlen):
        return False, f'{p_name}参数值长度大于的限制最大长度{maxlen}'
    return True, val


def vfloat(
        val,
        require=False,
        default: float = None,
        keep_val=3,
        minval: float or int = None,
        maxval: float or int = None,
        inner=True,
        p_name=''):
    """
    浮点数校验

    :param val: 待校验对象
    :param require: 是否必要参数 默认非必要
    :param default: 非必要状态下的默认值
    :param keep_val: 保留小数未 默认3位
    :param minval: 最小值范围 type--int 默认不校验
    :param maxval: 最大值范围 type--int 默认不校验
    :param inner: 是否范围内(针对于min_val或max_val有值校验)，默认范围内，False为范围外
    :param p_name: 参数名
    :return 校验状态--bool, 转换的值--float/错误信息
    """
    if val in ('', None, 'None', [], {}, 'null', 'NULL', 'Null'):
        if require:
            return False, f'缺少必要参数：{p_name}'
        return True, default
    try:
        val = float('%.{0}f'.format(keep_val) % float(val))
    except(SyntaxError, ValueError, TypeError):
        return False, f'{p_name}参数值无法解析成整形'
    if (minval is None) and (maxval is None):
        return True, val
    if inner:
        if (maxval is not None) and (val > maxval):
            return False, f'{p_name}参数值大于限制的最大值:{maxval}'
        if (minval is not None) and (val < minval):
            return False, f'{p_name}参数值小于限制的最小值:{minval}'
    else:
        if (minval is not None) and (maxval is not None) and (minval < val < maxval):
            return False, f'{p_name}参数值不在指定的限制范围'
    return True, val


def vdatetime(
        val,
        require=False,
        default: datetime.datetime = None,
        time_min: datetime.datetime = None,
        time_max: datetime.datetime = None,
        inner=True,
        p_name=''):
    """
    校验时间

    :param val: 待校验对象
    :param require: 是否必要参数 默认非必要
    :param default: 非必要状态下的默认值
    :param time_min: 最小值范围 type--Datetime 默认不校验
    :param time_max: 最大值范围 type--Datetime 默认不校验
    :param inner: 是否范围内(针对于min_val或max_val有值校验)，默认范围内，False为范围外
    :param p_name: 参数名
    :return 校验状态--bool, 转换的值--float/错误信息
    """
    if val in ('', None, 'None', [], {}, 'null', 'NULL', 'Null'):
        if require:
            return False, f'缺少必要参数：{p_name}'
        return True, default
    val_time = to_datetime(val)
    if not val_time:
        return False, f'{p_name}参数值无法解析成时间'
    if (not time_min) and (not time_max):
        return True, val_time
    if inner:
        if time_min and val_time < time_min:
            return False, f'{p_name}参数值小于限制的最小时间:{dt_str(time_min)}'
        if time_max and val_time > time_max:
            return False, f'{p_name}参数值大于于限制的最大时间:{dt_str(time_max)}'
    else:
        if time_min and time_max and (time_min < val_time < time_max):
            return False, '{p_name}参数值不在指定的时间限制范围'
    return True, val
