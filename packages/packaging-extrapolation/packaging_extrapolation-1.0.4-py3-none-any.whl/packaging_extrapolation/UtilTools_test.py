import itertools

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from packaging_extrapolation.Extrapolation import *
from sklearn.model_selection import KFold
from scipy.optimize import least_squares

kcal = 627.51
kj = 2625.4996
eV = 27.211

def unit_KJ(temp):
    return temp * kj


def unit_Kcal(temp):
    return temp * kcal

def unit_eV(temp):
    return temp * eV

def KJ_to_Kcal(temp):
    return temp * 0.23900574

def eV_to_Hartree(temp):
    return temp / eV

# 拆分,两列数据拆成一列
def split_data(data):
    return data.iloc[:, 0], data.iloc[:, 1]


# 交叉验证，返回的是索引
def k_fold_index(data, k):
    kf = KFold(n_splits=k, shuffle=True, random_state=42)
    train_index_list = []
    test_index_list = []
    for train_index, test_index in kf.split(data):
        train_index_list.append(train_index)
        test_index_list.append(test_index)
    return train_index_list, test_index_list


# 根据索引返回数据集
def train_test_split(X, y, train_index, test_index):
    return X.iloc[train_index], X.iloc[test_index], y.iloc[train_index], y.iloc[test_index]


# 交叉验证最低水平函数，使用average alpha - alpha_std
def train_dt_k_fold(model, *, X, y, k, method, init_guess=0.001):
    """
        使用k-1的数据参数，拟合第k个数据集的参数
        返回平均精度
    """
    level = 'dt'
    # 评估指标
    train_mad_list = []
    train_rmsd_list = []
    train_max_list = []
    test_mad_list = []
    test_rmsd_list = []
    test_max_list = []
    # 平均参数
    avg_alpha_list = []
    # 获取索引
    train_index_list, test_index_list = k_fold_index(X, k)
    k_index = 0
    for i in range(len(train_index_list)):
        k_index += 1
        # 分割数据集
        X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                            train_index_list[i], test_index_list[i])
        # 分割x_energy,y_energy
        x_energy_list_train, y_energy_list_train = split_data(X_train)
        x_energy_list_test, y_energy_list_test = split_data(X_test)

        # 训练，获取avg_alpha

        _, alpha_list = train(model, x_energy_list=x_energy_list_train,
                              y_energy_list=y_energy_list_train,
                              limit_list=y_train, method=method, level=level, init_guess=init_guess)
        avg_alpha = calc_avg_alpha(alpha_list)
        avg_alpha = avg_alpha - calc_std(alpha_list)

        # 训练集使用avg_alpha
        energy_list = train_alpha(model, x_energy_list=x_energy_list_train,
                                  y_energy_list=y_energy_list_train,
                                  alpha=avg_alpha, method=method, level=level)

        # 训练集误差评估指标
        train_mad = calc_MAD(energy_list, y_train)
        train_max_mad = calc_max_MAD(energy_list, y_train)
        train_rmsd = calc_RMSE(energy_list, y_train)

        # 验证集使用avg_alpha计算能量
        energy_list = train_alpha(model, x_energy_list=x_energy_list_test, y_energy_list=y_energy_list_test,
                                  alpha=avg_alpha,
                                  method=method, level=level)

        # 验证集误差评估指标
        test_mad = calc_MAD(energy_list, y_test)
        test_max_mad = calc_max_MAD(energy_list, y_test)
        test_rmsd = calc_RMSE(energy_list, y_test)

        print('*****************************************')
        print(k_index, '折训练集误差，MAD={:.3f} ，RMSD={:.3f}'.format(train_mad, train_rmsd))
        print(k_index, '折训练集最大误差，MaxMAD={:.3f}'.format(train_max_mad))
        print(k_index, '折验证集误差，MAD={:.3f} ，RMSD={:.3f}'.format(test_mad, test_rmsd))
        print(k_index, '折验证集最大误差，MaxMAD={:.3f}'.format(test_max_mad))
        print(k_index, '折数据集，alpha={:.5f}'.format(avg_alpha))
        print('*****************************************')
        print()

        train_mad_list.append(train_mad)
        train_rmsd_list.append(train_rmsd)
        train_max_list.append(train_max_mad)
        test_mad_list.append(test_mad)
        test_rmsd_list.append(test_rmsd)
        test_max_list.append(test_max_mad)
        avg_alpha_list.append(avg_alpha)

    train_avg_mad = np.average(train_mad_list)
    train_avg_rmsd = np.average(train_rmsd_list)
    train_avg_max = np.average(train_max_list)
    test_avg_mad = np.average(test_mad_list)
    test_avg_rmsd = np.average(test_rmsd_list)
    test_avg_max = np.average(test_max_list)
    avg_alpha = np.average(avg_alpha_list)

    print('平均训练集误差，MAD={:.3f} ，RMSD={:.3f}'.format(train_avg_mad, train_avg_rmsd))
    print('平均训练集最大误差，MaxMAD={:.3f}'.format(train_avg_max))
    print('平均验证集误差，MAD={:.3f} ，RMSD={:.3f}'.format(test_avg_mad, test_avg_rmsd))
    print('平均验证集最大误差，MaxMAD={:.3f}'.format(test_avg_max))
    print('5折平均alpha，alpha={:.5f}'.format(avg_alpha))

    eva_list = [train_avg_mad, train_avg_rmsd,
                test_avg_mad, test_avg_rmsd, avg_alpha]

    # 返回k折平均mad,rmsd
    return eva_list


# 以MAD，RMSD为目标函数拟合
def train_all(model, *, method, x_energy_list, y_energy_list, limit_list, init_guess=0.001, level='dt', temp='RMSD'):
    if is_series(x_energy_list):
        x_energy_list = to_list(x_energy_list)
    if is_series(y_energy_list):
        y_energy_list = to_list(y_energy_list)
    if is_series(limit_list):
        limit_list = to_list(limit_list)

    if level == 'dt':
        low_card = 2
        high_card = 3
    elif level == 'tq':
        low_card = 3
        high_card = 4
    elif level == 'q5':
        low_card = 4
        high_card = 5
    elif level == '56':
        low_card = 5
        high_card = 6
    else:
        raise ValueError('Invalid level name')

    model.update_method(method)
    model.update_card(low_card, high_card)
    # constraints = {'type': 'ineq', 'fun': lambda params: fun_model(init_guess, model, x_energy_list, y_energy_list, temp)}
    result = least_squares(loss_model, x0=init_guess,
                           args=(model, x_energy_list, y_energy_list,
                                 limit_list, temp))
    # result = minimize(loss_model, x0=init_guess,
    #                   args=(model, x_energy_list, y_energy_list,
    #                         limit_list, temp), bounds=[(1, 10)], constraints=constraints)
    return result.x[0]


def fun_model(alpha, model, x_energy_list, y_energy_list, temp):
    energy_list = []
    for i in range(len(x_energy_list)):
        x_energy = x_energy_list[i]
        y_energy = y_energy_list[i]
        model.update_energy(x_energy, y_energy)
        energy = model.get_function(alpha)
        energy_list.append(energy)
    return energy_list


def loss_model(alpha, model, x_energy_list, y_energy_list, limit_list, temp):
    energy_list = []
    for i in range(len(x_energy_list)):
        x_energy = x_energy_list[i]
        y_energy = y_energy_list[i]
        model.update_energy(x_energy, y_energy)
        energy = model.get_function(alpha)
        energy_list.append(energy)
    if temp == 'RMSD':
        result = calc_RMSE(limit_list, energy_list)
    elif temp == 'MAD':
        result = calc_MAD(limit_list, energy_list)
    else:
        return ValueError('Invalid assessment of indicators')
    # print(result)
    return result


# 交叉验证训练函数
def train_k_fold(model, *, X, y, k, method, level='dt', init_guess=0.001):
    """
    使用k-1的数据参数，拟合第k个数据集的参数
    返回平均精度
    """
    # 评估指标
    train_mad_list = []
    train_rmsd_list = []
    train_max_list = []
    test_mad_list = []
    test_rmsd_list = []
    test_max_list = []
    # 平均参数
    avg_alpha_list = []
    # 获取索引
    train_index_list, test_index_list = k_fold_index(X, k)
    k_index = 0
    for i in range(len(train_index_list)):
        k_index += 1
        # 分割数据集
        X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                            train_index_list[i], test_index_list[i])
        # 分割x_energy,y_energy
        x_energy_list_train, y_energy_list_train = split_data(X_train)
        x_energy_list_test, y_energy_list_test = split_data(X_test)

        # 训练，获取avg_alpha
        avg_alpha = get_k_fold_alpha(model, x_energy_list_train,
                                     y_energy_list_train, y_train, method, level, init_guess=init_guess)

        # 训练集使用avg_alpha
        energy_list = train_alpha(model, x_energy_list=x_energy_list_train,
                                  y_energy_list=y_energy_list_train,
                                  alpha=avg_alpha, method=method, level=level)

        # 训练集误差评估指标
        train_mad = calc_MAD(energy_list, y_train)
        train_max_mad = calc_max_MAD(energy_list, y_train)
        train_rmsd = calc_RMSE(energy_list, y_train)

        # 验证集使用avg_alpha计算能量
        energy_list = train_alpha(model, x_energy_list=x_energy_list_test, y_energy_list=y_energy_list_test,
                                  alpha=avg_alpha,
                                  method=method, level=level)

        # 验证集误差评估指标
        test_mad = calc_MAD(energy_list, y_test)
        test_max_mad = calc_max_MAD(energy_list, y_test)
        test_rmsd = calc_RMSE(energy_list, y_test)

        print('*****************************************')
        print(k_index, '折训练集误差，MAD={:.3f} ，RMSD={:.3f}'.format(train_mad, train_rmsd))
        print(k_index, '折训练集最大误差，MaxMAD={:.3f}'.format(train_max_mad))
        print(k_index, '折验证集误差，MAD={:.3f} ，RMSD={:.3f}'.format(test_mad, test_rmsd))
        print(k_index, '折验证集最大误差，MaxMAD={:.3f}'.format(test_max_mad))
        print(k_index, '折数据集，alpha={:.5f}'.format(avg_alpha))
        print('*****************************************')
        print()

        train_mad_list.append(train_mad)
        train_rmsd_list.append(train_rmsd)
        train_max_list.append(train_max_mad)
        test_mad_list.append(test_mad)
        test_rmsd_list.append(test_rmsd)
        test_max_list.append(test_max_mad)
        avg_alpha_list.append(avg_alpha)

    train_avg_mad = np.average(train_mad_list)
    train_avg_rmsd = np.average(train_rmsd_list)
    train_avg_max = np.average(train_max_list)
    test_avg_mad = np.average(test_mad_list)
    test_avg_rmsd = np.average(test_rmsd_list)
    test_avg_max = np.average(test_max_list)
    avg_alpha = np.average(avg_alpha_list)

    print('平均训练集误差，MAD={:.3f} ，RMSD={:.3f}'.format(train_avg_mad, train_avg_rmsd))
    print('平均训练集最大误差，MaxMAD={:.3f}'.format(train_avg_max))
    print('平均验证集误差，MAD={:.3f} ，RMSD={:.3f}'.format(test_avg_mad, test_avg_rmsd))
    print('平均验证集最大误差，MaxMAD={:.3f}'.format(test_avg_max))
    print('5折平均alpha，alpha={:.5f}'.format(avg_alpha))

    eva_list = [train_avg_mad, train_avg_rmsd,
                test_avg_mad, test_avg_rmsd, avg_alpha]

    # 返回k折平均mad,rmsd
    return eva_list


# 交叉验证训练函数，验证集使用原始参数评估
# 交叉验证训练函数
def train_k_fold_withOrg(model, *, X, y, k, method, level='dt', org_para):
    """
    使用k-1的数据参数，拟合第k个数据集的参数
    返回平均精度
    """
    # 评估指标
    test_mad_list = []
    test_rmsd_list = []
    test_max_list = []
    # 获取索引
    train_index_list, test_index_list = k_fold_index(X, k)
    k_index = 0
    for i in range(len(train_index_list)):
        k_index += 1
        # 分割数据集
        X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                            train_index_list[i], test_index_list[i])
        # 分割x_energy,y_energy
        x_energy_list_train, y_energy_list_train = split_data(X_train)
        x_energy_list_test, y_energy_list_test = split_data(X_test)

        # 验证集使用avg_alpha计算能量
        energy_list = train_alpha(model, x_energy_list=x_energy_list_test, y_energy_list=y_energy_list_test,
                                  alpha=org_para,
                                  method=method, level=level)

        # 验证集误差评估指标
        test_mad = calc_MAD(energy_list, y_test)
        test_max_mad = calc_max_MAD(energy_list, y_test)
        test_rmsd = calc_RMSE(energy_list, y_test)

        print('*****************************************')
        print(k_index, '折验证集误差，MAD={:.3f} ，RMSD={:.3f}'.format(test_mad, test_rmsd))
        print(k_index, '折验证集最大误差，MaxMAD={:.3f}'.format(test_max_mad))
        print(k_index, '折数据集，alpha={:.5f}'.format(org_para))
        print('*****************************************')
        print()

        test_mad_list.append(test_mad)
        test_rmsd_list.append(test_rmsd)
        test_max_list.append(test_max_mad)

    test_avg_mad = np.average(test_mad_list)
    test_avg_rmsd = np.average(test_rmsd_list)
    test_avg_max = np.average(test_max_list)

    print('平均验证集误差，MAD={:.3f} ，RMSD={:.3f}'.format(test_avg_mad, test_avg_rmsd))
    print('平均验证集最大误差，MaxMAD={:.3f}'.format(test_avg_max))

    eva_list = [test_avg_mad, test_avg_rmsd]

    # 返回k折平均mad,rmsd
    return eva_list


# 拟合k-1数据集，获取avg_alpha
def get_k_fold_alpha(model, x_energy_list, y_energy_list, limit, method, level, init_guess):
    alpha = train_all(model, x_energy_list=x_energy_list,
                      y_energy_list=y_energy_list,
                      limit_list=limit, method=method, level=level, init_guess=init_guess)
    return alpha


# 单点外推训练函数
def train_uspe(model, *, x_energy_list, tot_energy_list, alpha=None, limit_list=None, init_guess=0.001, level=2):
    if alpha is None and limit_list is None:
        raise ValueError('Alpha and limit_list must be assigned to one or the other')

    # 默认不拟合
    flag = False
    if limit_list is not None:
        flag = True
    energy_list = []
    alpha_list = []
    model.update_card(level)
    if is_series(x_energy_list):
        x_energy_list = to_list(x_energy_list)
    if is_series(tot_energy_list):
        tot_energy_list = to_list(tot_energy_list)
    if is_series(limit_list):
        limit_list = to_list(limit_list)
    for i in range(len(x_energy_list)):
        x_energy = x_energy_list[i]
        tot_energy = tot_energy_list[i]
        model.update_energy(x_energy, tot_energy)

        # 拟合
        if flag:
            limit = limit_list[i]
            result = least_squares(model.loss_function, init_guess, args=(limit,))
            alpha = result.x[0]
            alpha_list.append(alpha)

        energy = model.USPE(alpha)
        energy_list.append(energy)
    if flag:
        return energy_list, alpha_list
    return energy_list


# 指定alpha的训练函数
def train_alpha(model, *, method, x_energy_list, y_energy_list, alpha, level='dt'):
    energy_list = []
    if is_series(x_energy_list):
        x_energy_list = to_list(x_energy_list)
    if is_series(y_energy_list):
        y_energy_list = to_list(y_energy_list)

    if level == 'dt':
        low_card = 2
        high_card = 3
    elif level == 'tq':
        low_card = 3
        high_card = 4
    elif level == 'q5':
        low_card = 4
        high_card = 5
    elif level == '56':
        low_card = 5
        high_card = 6
    else:
        raise ValueError('Invalid level name')

    model.update_card(low_card, high_card)
    model.update_method(method)
    for i in range(len(x_energy_list)):
        x_energy = x_energy_list[i]
        y_energy = y_energy_list[i]

        model.update_energy(x_energy, y_energy)

        energy = model.get_function(alpha)
        energy_list.append(energy)
    return energy_list


def train_no_alpha(model, *, method, x_energy_list, y_energy_list, level='dt'):
    if x_energy_list is not list:
        x_energy_list = list(x_energy_list)
        y_energy_list = list(y_energy_list)
    if level == 'dt':
        low_card = 2
        high_card = 3
    elif level == 'tq':
        low_card = 3
        high_card = 4
    elif level == 'q5':
        low_card = 4
        high_card = 5
    elif level == '56':
        low_card = 5
        high_card = 6
    else:
        raise ValueError('Invalid level name')

    model.update_card(low_card, high_card)
    model.update_method(method)
    energy_list = []
    for i in range(len(x_energy_list)):
        x_energy = x_energy_list[i]
        y_energy = y_energy_list[i]

        model.update_energy(x_energy, y_energy)
        energy = model.get_function()
        energy_list.append(energy)
    return energy_list


# 训练函数，返回能量和alpha列表
def train(model, *, method, x_energy_list, y_energy_list, limit_list=None, init_guess=0.001, level='dt', tolerance=1e-6):
    # 默认需要拟合参数，默认需要拟合
    flag = True
    if limit_list is None:
        flag = False
    energy_list = []
    alpha_list = []
    if is_series(x_energy_list):
        x_energy_list = to_list(x_energy_list)
    if is_series(y_energy_list):
        y_energy_list = to_list(y_energy_list)
    if is_series(limit_list):
        limit_list = to_list(limit_list)

    # 判断基数
    if level == 'dt':
        low_card = 2
        high_card = 3
    elif level == 'tq':
        low_card = 3
        high_card = 4
    elif level == 'q5':
        low_card = 4
        high_card = 5
    else:
        raise ValueError('Invalid level name')
    model.update_method(method)
    model.update_card(low_card, high_card)

    for i in range(len(x_energy_list)):
        x_energy = x_energy_list[i]
        y_energy = y_energy_list[i]

        # 更新能量
        model.update_energy(x_energy, y_energy)

        # 为ture，则拟合
        if flag:
            limit = limit_list[i]
            alpha = opt_alpha(model.loss_function, limit, init_guess, tolerance)
            alpha_list.append(alpha)
            energy = calc_energy(model, alpha)

        else:
            energy = calc_energy(model)

        energy_list.append(energy)
    if flag:
        return energy_list, alpha_list
    return energy_list


# 拟合参数
def opt_alpha(loss_model, limit, init_guess, tolerance):
    result = least_squares(fun=loss_model, x0=init_guess,
                           args=(limit,))
    # result = minimize_scalar(fun=loss_model, args=(limit,))
    return result.x[0]


# 计算能量
def calc_energy(model, alpha=None):
    # 无alpha
    if alpha is None:
        energy = model.get_function()
    # 有alpha
    else:
        energy = model.get_function(alpha)
    return energy


# 计算函数参数个数
def count_parameter(fun):
    return fun.__code__.co_argcount


# 计算最大正偏差
def calc_MaxPosMAD(y_true, y_pred):
    return np.max(y_true - y_pred) * kcal


# 计算最大负偏差
def calc_MaxNegMAD(y_true, y_pred):
    return np.min(y_true - y_pred) * kcal


# 计算MSD
def calc_MSD(y_true, y_pred):
    return mean_squared_error(y_true, y_pred)


# 计算RMSD
def calc_RMSE(y_true, y_pred):
    return mean_squared_error(y_true, y_pred, squared=False) * 627.51


# 计算MAD
def calc_MAD(y_true, y_pred):
    return mean_absolute_error(y_true, y_pred) * kcal


# 计算max_MAD
def calc_max_MAD(y_true, y_pred):
    return np.max(abs(y_true - y_pred)) * kcal


# 计算min_MAD
def calc_min_MAD(y_true, y_pred):
    return np.min(abs(y_true - y_pred)) * kcal


# 计算R2
def calc_R2(y_true, y_pred):
    return r2_score(y_true, y_pred)


# 计算平均alpha
def calc_avg_alpha(alpha):
    return np.average(alpha)


# 计算最大alpha
def calc_max_alpha(alpha):
    return np.max(alpha)


# 计算最小alpha
def calc_min_alpha(alpha):
    return np.min(alpha)


# 计算中位数
def calc_median(alpha):
    return np.median(alpha)


# 计算标准差
def calc_std(alpha):
    return np.std(alpha)


# 计算方差
def calc_var(alpha):
    return np.var(alpha)


# 计算误差，带正负
def calc_me(energy_list, limit_list):
    return np.sum(limit_list - energy_list) / len(energy_list) * kcal


# 表函数
def create_table(method_list):
    df = pd.DataFrame(columns=['method', 'avg_alpha', 'min_alpha', 'max_alpha', 'RMSD', 'MAD', 'MaxAD'])
    df['method'] = method_list
    return df


# 存入评估指标
def input_result(result_df, *, index, energy_list, limit_list, alpha_list=None):
    result_df['RMSD'][index] = calc_RMSE(limit_list, energy_list)
    result_df['MAD'][index] = calc_MAD(limit_list, energy_list)
    result_df['MaxAD'][index] = calc_max_MAD(limit_list, energy_list)
    if alpha_list is not None:
        result_df['avg_alpha'][index] = calc_avg_alpha(alpha_list)
        result_df['min_alpha'][index] = calc_min_alpha(alpha_list)
        result_df['max_alpha'][index] = calc_max_alpha(alpha_list)
    return result_df


# 列表一维化
def flatting(ls):
    return list(itertools.chain.from_iterable(ls))


# 判断对象是否为Series
def is_series(obj):
    return isinstance(obj, pd.Series)


# Series转list
def to_list(obj):
    return list(obj.values)


# 画图：一个外推水平的分子参数分布图
def plot_alpha_value(model, *, mol_list, x_energy_list, y_energy_list, fitting_list,
                     limit_energy, method, level='dt', init_guess=0.001):
    _, alpha_list = train(model, method=method, x_energy_list=x_energy_list,
                          y_energy_list=y_energy_list, limit_list=fitting_list,
                          level=level, init_guess=init_guess)

    avg_alpha = calc_avg_alpha(alpha_list)
    # avg_alpha = round(avg_alpha, 4)
    # alpha_std = calc_std(alpha_list)
    # mid_alpha = calc_median(alpha_list)
    # avg_alpha = avg_alpha - alpha_std
    energy_list = train_alpha(model, method=method, x_energy_list=x_energy_list,
                              y_energy_list=y_energy_list,
                              level=level, alpha=avg_alpha)

    print_information(mol_list=mol_list, energy_list=energy_list,
                      alpha_list=alpha_list,
                      limit_energy=limit_energy, level=level)

    plot_alpha(mol_list=mol_list, alpha_list=alpha_list, level=level)
    return energy_list, alpha_list


def plot_alpha(*, mol_list, alpha_list, level):
    plt.figure(figsize=(10, 6))
    plt.plot(mol_list, alpha_list, '.')
    plt.xticks(rotation=-80)
    plt.xticks(fontsize=6)
    plt.ylabel('alpha value')
    plt.xlabel('species')
    plt.title(level)
    plt.tight_layout()
    plt.grid(alpha=0.3)
    plt.show()


def print_information(*, mol_list, energy_list, alpha_list, limit_energy, level):
    energy_list = np.array(energy_list)
    limit_energy = np.array(limit_energy)

    print('***************************************')
    print('  ', level, ' average_alpha = {:.5f}         '.format(calc_avg_alpha(alpha_list)))
    # print('  ', level, ' compute_alpha = {:.5f}         '.format(calc_avg_alpha(alpha_list) - calc_std(alpha_list)))
    print('  ', level, ' MAD = {:.3f}                   '.format(calc_MAD(energy_list, limit_energy)))

    max_mad_index = np.argmax(abs(energy_list - limit_energy))

    print('The max MAD mol index is {} {}'.format(max_mad_index, mol_list[max_mad_index]))

    print('  ', level, ' max MAD = {:.3f}                   '.format(calc_max_MAD(energy_list, limit_energy)))
    print('  ', level, ' max Max_Pos_MAD = {:.3f}                   '.format(calc_MaxPosMAD(limit_energy, energy_list)))
    print('  ', level, ' max Max_Neg_MAD = {:.3f}                   '.format(calc_MaxNegMAD(limit_energy, energy_list)))

    print('  ', level, ' RMSD = {:.3f}                   '.format(calc_RMSE(energy_list, limit_energy)))
    print('  ', level, ' ME = {:.3f}                   '.format(calc_me(energy_list, limit_energy)))
    # print('  ', level, ' R2 = {:.3f}                   '.format(calc_R2(energy_list, limit_energy)))

    min_alpha = calc_min_alpha(alpha_list)
    max_alpha = calc_max_alpha(alpha_list)
    print('   Range of alpha : [{:.4f},{:.4f}]      '.format(min_alpha, max_alpha, '.2f'))
    print('   Median of alpha : {:.3f}            '.format(calc_median(alpha_list)))
    print('   alpha 标准差 : {:.3f}'.format(calc_std(alpha_list)))
    print('   alpha 方差 : {:.3f}'.format(calc_var(alpha_list)))
    print('***************************************')


# 计算电子数
def count_ele(mol_list):
    mol_dict = {'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8, 'F': 9, 'Ne': 10,
                'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15, 'S': 16, 'Cl': 17, 'Ar': 18}

    count_list = []

    if is_series(mol_list):
        mol_list = to_list(mol_list)

    for i in range(len(mol_list)):
        mol_name = mol_list[i]
        count = 0
        j = 0
        # 遍历分子名
        while j < len(mol_name):
            k = 1
            mol_str = mol_name[j]
            j += 1
            # 判断是否带小写字符
            if j < len(mol_name) and 'z' > mol_name[j] > 'a':
                mol_str += mol_name[j]
                j += 1
            # 判断是否带数字
            if j < len(mol_name) and '9' > mol_name[j] > '0':
                # 记录原子个数
                k = int(mol_name[j])
                j += 1

            # 是否带电
            if j < len(mol_name) and mol_name[j] == '+':
                count -= 1
                j += 1
            if j < len(mol_name) and mol_name[j] == '-':
                count += 1
                j += 1

            # print(mol_str)
            count += mol_dict.get(mol_str) * k
        count_list.append(count)
    return count_list

# 提取单个体系的电子数
def count_ele_one(mol_name):
    mol_dict = {'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8, 'F': 9, 'Ne': 10,
                'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15, 'S': 16, 'Cl': 17, 'Ar': 18}
    count = 0
    j = 0
    # 遍历分子名
    while j < len(mol_name):
        k = 1
        mol_str = mol_name[j]
        j += 1
        # 判断是否带小写字符
        if j < len(mol_name) and mol_name[j].islower():
            mol_str += mol_name[j]
            j += 1
        # 判断是否带数字
        if j < len(mol_name) and '9' > mol_name[j] > '0':
            # 记录原子个数
            k = int(mol_name[j])
            j += 1

        # 是否带电
        if j < len(mol_name) and mol_name[j] == '+':
            count -= 1
            j += 1
        if j < len(mol_name) and mol_name[j] == '-':
            count += 1
            j += 1

        # print(mol_str)
        count += mol_dict.get(mol_str) * k
    return count

# 计算价电子数
def count_val_ele(mol_list):
    mol_dict = {'H': 1, 'He': 2, 'Li': 1, 'Be': 2, 'B': 3, 'C': 4, 'N': 5, 'O': 6, 'F': 7, 'Ne': 8,
                'Na': 1, 'Mg': 2, 'Al': 3, 'Si': 4, 'P': 5, 'S': 6, 'Cl': 7, 'Ar': 8}

    count_list = []

    if is_series(mol_list):
        mol_list = to_list(mol_list)

    for i in range(len(mol_list)):
        mol_name = mol_list[i]
        count = 0
        j = 0
        # 遍历分子名
        while j < len(mol_name):
            k = 1
            mol_str = mol_name[j]
            j += 1
            # 判断是否带小写字符
            if j < len(mol_name) and 'z' > mol_name[j] > 'a':
                mol_str += mol_name[j]
                j += 1
            # 判断是否带数字
            if j < len(mol_name) and '9' > mol_name[j] > '0':
                # 记录原子个数
                k = int(mol_name[j])
                j += 1

            # 是否带电
            if j < len(mol_name) and mol_name[j] == '+':
                # count -= 1
                j += 1
            if j < len(mol_name) and mol_name[j] == '-':
                # count += 1
                j += 1

            # print(mol_str)
            count += mol_dict.get(mol_str) * k
        count_list.append(count)
    return count_list


# 计算原子化能
def calc_atomize_energy(*, mol_data, atom_data, level='d'):
    if level == 'd':
        temp = 'aug-cc-pvdz'
    elif level == 't':
        temp = 'aug-cc-pvtz'
    elif level == 'q':
        temp = 'aug-cc-pvqz'
    elif level == '5':
        temp = 'aug-cc-pv5z'
    elif level == '6':
        temp = 'aug-cc-pv6z'
    else:
        return ValueError('Invalid level,please input d,t,q,5 or 6.')

    atom_dict = get_atom_dict(atom_data, temp)
    energy_list = []
    for i in mol_data.index:
        mol_name = mol_data['mol'][i]
        mol_energy = mol_data[temp][i]
        atomize_energy = get_atomize_energy(mol_name, mol_energy, atom_dict)
        energy_list.append(atomize_energy)
    return energy_list


# 计算单个分子的原子化能
def get_atomize_energy(mol_name, mol_energy, atom_dict):
    atom_energy_sum = 0
    i = 0
    while i < len(mol_name):
        atom = mol_name[i]
        count = 1
        i += 1
        # 判断是否有小写字符
        if i < len(mol_name) and 'z' > mol_name[i] > 'a':
            atom += mol_name[i]
            i += 1
        # 判断是否有数字
        if i < len(mol_name) and '9' > mol_name[i] > '0':
            # 记录个数
            count = int(mol_name[i])
            i += 1
        # print(atom)
        atom_energy_sum += atom_dict.get(atom) * count
    return atom_energy_sum - mol_energy


# 构造原子能量映射
def get_atom_dict(data, temp):
    atom_dict = {}
    for i in data.index:
        atom_name = data['mol'][i]
        atom_energy = data[temp][i]
        atom_dict.update({atom_name: float(atom_energy)})
    return atom_dict


# 计算原子化能--
def calc_TAE(*, mol_data, atom_data, temp):
    atom_dict = get_atom_dict(atom_data, temp)
    energy_list = []
    for i in mol_data.index:
        mol_name = mol_data['mol'][i]
        mol_energy = mol_data[temp][i]
        atomize_energy = get_atomize_energy(mol_name, mol_energy, atom_dict)
        energy_list.append(atomize_energy)
    return energy_list


# 穷举
def exhaustion_alpha(model, *, method, x_energy_list, y_energy_list, limit_list, init_alpha, init_step=1000,
                     level='dt'):
    error_df = pd.DataFrame(columns=['alpha', 'MAD', 'MaxMAD'])
    mad_list = []
    max_mad_list = []
    alpha_list = []
    alpha = init_alpha
    for i in range(init_step):
        alpha_list.append(alpha)
        energy_list = train_alpha(model, x_energy_list=x_energy_list, y_energy_list=y_energy_list,
                                  alpha=alpha, level=level, method=method)
        mad = calc_MAD(limit_list,
                       energy_list)
        max_mad = calc_max_MAD(limit_list,
                               energy_list)
        mad_list.append(mad)
        max_mad_list.append(max_mad)
        alpha += 0.001
    error_df['alpha'] = alpha_list
    error_df['MAD'] = mad_list
    error_df['MaxMAD'] = max_mad_list
    min_mad_alpha = error_df['alpha'][np.argmin(error_df['MAD'])]
    min_maxMad_alpha = error_df['alpha'][np.argmin(error_df['MaxMAD'])]
    print('使MAD最小的alpha值为 {}，最小MAD为 {}'.format(min_mad_alpha, np.min(error_df['MAD'])))
    print('使MaxMAD最小的alpha值为：{},最小MaxMAD为 {}'.format(min_maxMad_alpha, np.min(error_df['MaxMAD'])))
    return error_df


# 穷举-限制
def exhaustion_alpha_constraint(model, *, method, x_energy_list, y_energy_list, limit_list, init_alpha, init_step=1000,
                                level='dt'):
    error_df = pd.DataFrame(columns=['alpha', 'MAD', 'MaxMAD', 'MaxPosMAD', 'MaxNegMAD'])
    mad_list = []
    pos_mad_list = []
    neg_mad_list = []
    max_mad_list = []
    alpha_list = []
    # 初猜
    alpha = init_alpha
    for i in range(init_step):
        alpha_list.append(alpha)
        energy_list = train_alpha(model, x_energy_list=x_energy_list, y_energy_list=y_energy_list,
                                  alpha=alpha, level=level, method=method)
        mad = calc_MAD(limit_list,
                       energy_list)
        # 最大正偏差
        max_pos_mad = calc_MaxPosMAD(limit_list,
                                     energy_list)
        # 最大负偏差
        max_neg_mad = calc_MaxNegMAD(limit_list,
                                     energy_list)

        # 最大绝对偏差
        max_mad = calc_max_MAD(limit_list, energy_list)

        mad_list.append(mad)
        pos_mad_list.append(max_pos_mad)
        neg_mad_list.append(max_neg_mad)
        max_mad_list.append(max_mad)

        alpha += 0.001
    error_df['alpha'] = alpha_list
    error_df['MAD'] = mad_list
    error_df['MaxPosMAD'] = pos_mad_list
    error_df['MaxNegMAD'] = neg_mad_list
    error_df['MaxMAD'] = max_mad_list

    # 引起最小平均绝对偏差的alpha
    min_MAD_alpha = round(error_df['alpha'][np.argmin(error_df['MAD'])], 3)
    min_MAD_alpha_index = np.argmin(error_df['MAD'])

    # alpha使最大绝对偏差最小
    min_max_MAD_alpha = round(error_df['alpha'][np.argmin([error_df['MaxMAD']])], 3)
    min_max_MAD_alpha_index = np.argmin(error_df['MaxMAD'])

    # alpha使最大正偏差大于0且最小
    min_pos_MAD_alpha = round(error_df['alpha'][np.argmin(error_df['MaxPosMAD'] >= 0)], 3)
    min_pos_MAD_alpha_index = np.argmin(error_df['MaxPosMAD'] >= 0)

    # alpha使最大负偏差最大
    max_neg_MAD_alpha = round(error_df['alpha'][np.argmax(error_df['MaxNegMAD'] <= 0)], 3)
    max_neg_MAD_alpha_index = np.argmax(error_df['MaxNegMAD'] <= 0)

    print('使MAD最小的alpha值为 {}，MAD为 {}，MaxMAD为 {}，PosMAD为 {} ，NegMAD为 {}'.format(min_MAD_alpha, round(
        error_df['MAD'][min_MAD_alpha_index], 3),
                                                                               round(error_df['MaxMAD'][
                                                                                         min_MAD_alpha_index], 3),
                                                                               round(error_df['MaxPosMAD'][
                                                                                         min_MAD_alpha_index], 3),
                                                                               round(error_df['MaxNegMAD'][
                                                                                         min_MAD_alpha_index], 3)))

    print('使MaxMAD最小的alpha值为 {}，MAD {}，MaxMAD为 {},PosMAD为 {}，NegMAD为 {}'.format(min_max_MAD_alpha, round(
        error_df['MAD'][min_max_MAD_alpha_index], 3),
                                                                                round(error_df['MaxMAD'][
                                                                                          min_max_MAD_alpha_index], 3),
                                                                                round(error_df['MaxPosMAD'][
                                                                                          min_max_MAD_alpha_index], 3),
                                                                                round(error_df['MaxNegMAD'][
                                                                                          min_max_MAD_alpha_index], 3)))

    print('使PosMAD最小的alpha值为 {}，MAD {}，MaxMAD为 {},PosMAD为 {}，NegMAD为 {}'.format(min_pos_MAD_alpha, round(
        error_df['MAD'][min_pos_MAD_alpha_index], 3),
                                                                                round(error_df['MaxMAD'][
                                                                                          min_pos_MAD_alpha_index], 3),
                                                                                round(error_df['MaxPosMAD'][
                                                                                          min_pos_MAD_alpha_index], 3),
                                                                                round(error_df['MaxNegMAD'][
                                                                                          min_pos_MAD_alpha_index], 3)))
    print('使NegMAD最大的alpha值为 {}，MAD {}，MaxMAD为 {},PosMAD为 {}，NegMAD为 {}'.format(max_neg_MAD_alpha, round(
        error_df['MAD'][max_neg_MAD_alpha_index], 3),
                                                                                round(error_df['MaxMAD'][
                                                                                          max_neg_MAD_alpha_index], 3),
                                                                                round(error_df['MaxPosMAD'][
                                                                                          max_neg_MAD_alpha_index], 3),
                                                                                round(error_df['MaxNegMAD'][
                                                                                          max_neg_MAD_alpha_index]), 3))

    return error_df


# 计算反应物
def cal_reaction_heat(*, react_A_hf, react_B_hf, react_A_corr, react_B_corr,
                      method_hf, method_corr, alpha_hf, alpha_corr, level='dt'):
    if level == 'dt':
        low_card, high_card = 2, 3
    elif level == 'tq':
        low_card, high_card = 3, 4
    elif level == 'q5':
        low_card, high_card = 4, 5
    model = FitMethod(low_card=low_card, high_card=high_card)
    # 计算hf外推
    model.update_method(method_hf)
    model.update_energy(react_A_hf[0], react_A_hf[1])
    A_hf_energy = model.get_function(alpha_hf)
    model.update_energy(react_B_hf[0], react_B_hf[1])
    B_hf_energy = model.get_function(alpha_hf)

    # 计算相关能外推
    model.update_method(method_corr)
    model.update_energy(react_A_corr[0], react_A_corr[1])
    A_corr_energy = model.get_function(alpha_corr)
    model.update_energy(react_B_corr[0], react_B_corr[1])
    B_corr_energy = model.get_function(alpha_corr)

    # 产物能量
    return A_hf_energy + A_corr_energy + B_hf_energy + B_corr_energy


# 计算产物
def cal_reaction_product(*, react_hf, react_corr,
                         method_hf, method_corr, alpha_hf, alpha_corr, level='dt'):
    if level == 'dt':
        low_card, high_card = 2, 3
    elif level == 'tq':
        low_card, high_card = 3, 4
    elif level == 'q5':
        low_card, high_card = 4, 5
    model = FitMethod(low_card=low_card, high_card=high_card)
    # 计算hf外推
    model.update_method(method_hf)
    model.update_energy(react_hf[0], react_hf[1])
    hf_energy = model.get_function(alpha_hf)

    # 计算相关能外推
    model.update_method(method_corr)
    model.update_energy(react_corr[0], react_corr[1])
    corr_energy = model.get_function(alpha_corr)

    # 产物
    return hf_energy + corr_energy


# 判断原子序数
def atom_number(atom):
    atom_list = {'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8, 'F': 9, 'Ne': 10,
                 'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15, 'S': 16, 'Cl': 17, 'Ar': 18}
    # 返回原子序数
    return atom_list.values(atom)


# 任意函数拟合
def random_train(*, loss_fun, fun, X, Y, x_energy_list, y_energy_list, limit_list):
    para_list = []
    energy_list = []
    for i in x_energy_list.index:
        x_energy = x_energy_list[i]
        y_energy = y_energy_list[i]
        limit = limit_list[i]
        result = least_squares(loss_fun, x0=0.001, args=(X, Y, x_energy, y_energy, limit))
        para = result.x[0]
        para_list.append(para)
        energy = fun(para, X, Y, x_energy, y_energy)
        energy_list.append(energy)
    return para_list,energy_list

# 将任何存储转为(-1,1)的ndarray
def to_array(temp):
    return np.array(temp).reshape(-1,1)


# 计算自旋多重度，单电子数+1
def calculate_spin(mol_name):
    result = count_ele_one(mol_name)
    return result % 2 +1

# 计算自旋多重度，alpha-beta+1
def calculate_spin_1(mol_name):
    alpha_dict = {'H': 1, 'He': 1, 'Li': 2, 'Be': 2, 'B': 3, 'C': 4, 'N': 5, 'O': 5, 'F': 5, 'Ne': 5,
                 'Na': 6, 'Mg': 6, 'Al': 7, 'Si': 8, 'P': 9, 'S': 9, 'Cl': 9, 'Ar': 9}


    beta_dict = {'H': 0, 'He': 1, 'Li': 1, 'Be': 2, 'B': 2, 'C': 2, 'N': 2, 'O': 3, 'F': 4, 'Ne': 5,
                  'Na': 5, 'Mg': 6, 'Al': 6, 'Si': 6, 'P': 6, 'S': 7, 'Cl': 8, 'Ar': 9}

    alpha_ele = 0
    beta_ele = 0
    j = 0
    # 遍历分子名
    while j < len(mol_name):
        k = 1
        mol_str = mol_name[j]
        j += 1
        # 判断是否带小写字符
        if j < len(mol_name) and mol_name[j].islower():
            mol_str += mol_name[j]
            j += 1
        # 判断是否带数字
        if j < len(mol_name) and '9' > mol_name[j] > '0':
            # 记录原子个数
            k = int(mol_name[j])
            j += 1

        # 是否带电
        if j < len(mol_name) and mol_name[j] == '+':
            count -= 1
            j += 1
        if j < len(mol_name) and mol_name[j] == '-':
            count += 1
            j += 1

        # print(mol_str)
        alpha_ele += alpha_dict.get(mol_str) * k
        beta_ele += beta_dict.get(mol_str) * k
    return alpha_ele-beta_ele+1

# 结构排列
# length:长度，base:基数，count_type:种数
def chose_base(length, base):
    arr = []
    # 初始化
    for i in range(length):
        arr.append(1)
        random_arr = []
        random_arr.append(arr[:])
        i = length - 1
        j = 0

    while i > 0:
        j = 0
        k = j

        while arr[j] < base:
            arr[j] += 1

            random_arr.append(arr[:]) # 浅拷贝
        # 找到进位的位置，要保证没有越界
        while k < i and arr[k] == base:
            k += 1
        # 最后一位达到满了
        if arr[i] == base:
            i -= 1
        # 满base进1
        if arr[k - 1] == base and arr[i] != base:
            arr[k] += 1
            # 满base进1，其他位归为1
            while j < k:
                arr[j] = 1
                j += 1

            random_arr.append(arr[:])
    # print(len(random_arr))

    # 创建一个集合，用于存储已见过的元素
    seen = set()
    # 创建一个新的列表，用于存储去重后的元素
    unique_array = []

    for elem in random_arr:
        # 将每个元素排序并转化为元组
        sorted_elem = tuple(sorted(elem))
        # 如果该排序后的元组未在 seen 中出现过，则添加到 unique_array 中
        if sorted_elem not in seen:
            unique_array.append(elem)
            seen.add(sorted_elem)

    # 返回去重数组，原始数组
    return unique_array,random_arr