from math import pow


def calculate_profit(Ntl, Pb, T_alpha=200, Ipdw=100, Rdur=0.0002, D_alpha=15):
    """
    计算Alpha月度利润
    
    Args:
        Ntl: 日交易量档位
        Pb: 余额积分
        T_alpha: 门槛（默认200分）
        Ipdw: 每次领取预期收益（默认100）
        Rdur: 交易损耗率（默认0.0002）
        D_alpha: 积分过期天数（默认15）
    
    Returns:
        tuple: (月利润, 真实交易量, 余额档位, 余额USD)
    """
    # 输入验证
    if Ntl < 0 or Ntl > 50:
        raise ValueError("Ntl（日交易量档位）应在0-50范围内")
    if Pb < 0 or Pb > 15:
        raise ValueError("Pb（余额积分）应在0-15范围内")
    if T_alpha < 0 or T_alpha > 10000:
        raise ValueError("T_alpha（门槛）应在0-10000范围内")
    if Ipdw < 0 or Ipdw > 100000:
        raise ValueError("Ipdw（每次领取预期收益）应在0-100000范围内")
    if Rdur < 0 or Rdur > 1:
        raise ValueError("Rdur（交易损耗率）应在0-1范围内")
    
    try:
        Vactual = pow(2, Ntl) / 2
        Nbal = Pb
        balance = pow(10, Nbal + 1)
        first = 2 * max(0, ((Ntl + Pb) * 15 - T_alpha) / D_alpha) * Ipdw
        second = 30 * (Vactual * Rdur)
        third = pow(10, Nbal+1) * (0.04 / 12)
        return first - second - third, Vactual, Nbal, balance
    except OverflowError:
        raise ValueError(f"输入数值过大，无法计算。Ntl={Ntl}, Pb={Pb}")
    except Exception as e:
        raise ValueError(f"计算错误：{e}")


def calculate_auto_fields(Ntl, Pb):
    """
    计算自动填充字段
    
    Args:
        Ntl: 日交易量档位
        Pb: 余额积分
    
    Returns:
        tuple: (真实交易量, 余额档位, 余额USD)
    """
    # 输入验证
    if Ntl < 0 or Ntl > 50:
        raise ValueError("Ntl（日交易量档位）应在0-50范围内")
    if Pb < 0 or Pb > 15:
        raise ValueError("Pb（余额积分）应在0-15范围内")
    
    try:
        Vactual = pow(2, Ntl) / 2
        Nbal = Pb
        balance = pow(10, Nbal + 1)
        return Vactual, Nbal, balance
    except OverflowError:
        raise ValueError(f"输入数值过大，无法计算。Ntl={Ntl}, Pb={Pb}")
    except Exception as e:
        raise ValueError(f"计算错误：{e}")


def validate_inputs(Ntl, Pb, T_alpha=200, Ipdw=100, Rdur=0.0002):
    """
    验证输入参数
    
    Returns:
        tuple: (是否有效, 错误消息)
    """
    try:
        Ntl = float(Ntl)
        Pb = float(Pb)
        T_alpha = float(T_alpha)
        Ipdw = float(Ipdw)
        Rdur = float(Rdur)
        
        # 范围验证
        if Ntl < 0 or Ntl > 50:
            return False, "Ntl（日交易量档位）应在0-50范围内"
        if Pb < 0 or Pb > 15:
            return False, "Pb（余额积分）应在0-15范围内"
        if T_alpha < 0 or T_alpha > 10000:
            return False, "T_alpha（门槛）应在0-10000范围内"
        if Ipdw < 0 or Ipdw > 100000:
            return False, "Ipdw（每次领取预期收益）应在0-100000范围内"
        if Rdur < 0 or Rdur > 1:
            return False, "Rdur（交易损耗率）应在0-1范围内"
        
        return True, ""
    except ValueError as e:
        return False, f"输入参数格式错误：{e}" 