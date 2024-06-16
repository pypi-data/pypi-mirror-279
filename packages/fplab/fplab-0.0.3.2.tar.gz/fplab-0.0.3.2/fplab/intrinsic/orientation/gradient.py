"""
基于梯度的指纹方向场估计方法
这里预先假设指纹为灰度图或二值图，不能保证函数在RGB图像的适用性
"""
import torch
import gc
from fplab.tools.image import type_as
from fplab.tools.tensor import imt_pad_blk, imt_cal_grad, imt_sum_average, imt_gaussian, imt_pad_crop


def rao1990(im, blk_sz, wd_sz=(5, 5), device=None, need_quality=True):
    """使用1990年Rao使用的方法估计指纹方向场。
    im是需要处理的指纹图像。
    blk_sz是估计方向场时的图像块大小，可以为整数或2维向量。
    wd_sz是计算方向场可信度时的窗口大小，可以为整数或2维向量。
    device是数组转化为张量后使用的设备"""
    # 处理输入参数
    if isinstance(blk_sz, int):
        ksp = blk_sz, blk_sz
    else:
        ksp = blk_sz
    if isinstance(wd_sz, int):
        wsp = wd_sz, wd_sz
    else:
        wsp = wd_sz
    # 估计方向场
    imt = type_as(im, md="t", device=device)
    hg, wg = imt_cal_grad(imt)
    vy = imt_sum_average(2*hg*wg, ksp, kmd="s")
    vx = imt_sum_average(hg*hg-wg*wg, ksp, kmd="s")
    out = 0.5*torch.atan2(vy, vx)
    if not need_quality:
        out = type_as(out, im)
        return out
    else:
        # 计算方向场可信度
        # 原文中使用了绝对值，为了便于使用卷积实现，这里使用了平方
        cost, sint = torch.cos(out), torch.sin(out)
        g = hg**2+wg**2
        g_cos = imt_sum_average(g*cost*cost, wsp, kmd="s")
        g_sin = imt_sum_average(g*sint*sint, wsp, kmd="s")
        g_2cs = imt_sum_average(2*g*sint*cost, wsp, kmd="s")
        sum_g = imt_sum_average(g, wsp, kmd="s")
        cd = (cost*cost*g_cos+sint*sint*g_sin+cost*sint*g_2cs)/(sum_g+1e-8)
        out = type_as(out, im)
        cd = type_as(cd, im)
        return out, cd


def imt_rao1990(imt, blk_sz, wd_sz=(5, 5), need_quality=True):
    """使用1990年Rao使用的方法估计指纹方向场，专为torch张量设计。
    :param imt:                 待处理指纹图像，n*1*h*w，不支持RGB等多通道图像
    :param blk_sz:              估计方向场的图像块大小，2维整数向量
    :param wd_sz:               计算方向场可信度的窗口大小，2维整数向量
    :param need_quality:        是否需要计算方向场可信度"""
    assert len(imt.shape) == 4 and imt.shape[-3] == 1
    assert len(blk_sz) == 2 and len(wd_sz) == 2
    conv_hk = torch.tensor([[[[-1., -2., -1., ], [0., 0., 0., ], [1., 2., 1., ]]]],
                           dtype=imt.dtype, device=imt.device)
    conv_wk = torch.tensor([[[[-1., 0., 1., ], [-2., 0., 2., ], [-1., 0., 1., ]]]],
                           dtype=imt.dtype, device=imt.device)
    imt_p = torch.nn.functional.pad(imt, (1, 1, 1, 1), mode='reflect')
    hg = torch.nn.functional.conv2d(imt_p, conv_hk)
    wg = torch.nn.functional.conv2d(imt_p, conv_wk)
    sum_k = torch.ones((1, 1, blk_sz[0], blk_sz[1]), dtype=imt.dtype, device=imt.device)
    pd_sp = blk_sz[1]-1-(blk_sz[1]-1)//2, (blk_sz[1]-1)//2, blk_sz[0]-1-(blk_sz[0]-1)//2, (blk_sz[0]-1)//2
    hg_p = torch.nn.functional.pad(hg, pd_sp, mode='reflect')
    wg_p = torch.nn.functional.pad(wg, pd_sp, mode='reflect')
    vy = torch.nn.functional.conv2d(2*hg_p*wg_p, sum_k)
    vx = torch.nn.functional.conv2d(hg_p**2-wg_p**2, sum_k)
    out = 0.5*torch.atan2(vy, vx)
    if not need_quality:
        return out
    else:
        # 计算方向场可信度
        # 原文中使用了绝对值，为了便于使用卷积实现，这里使用了平方
        cost, sint = torch.cos(out), torch.sin(out)
        g = hg**2+wg**2
        sum_k = torch.ones((1, 1, wd_sz[0], wd_sz[1]), dtype=imt.dtype, device=imt.device)
        pd_sp = wd_sz[1]-1-(wd_sz[1]-1)//2, (wd_sz[1]-1)//2, wd_sz[0]-1-(wd_sz[0]-1)//2, (wd_sz[0]-1)//2
        cost_p = torch.nn.functional.pad(cost, pd_sp, mode='reflect')
        sint_p = torch.nn.functional.pad(sint, pd_sp, mode='reflect')
        g_p = torch.nn.functional.pad(g, pd_sp, mode='reflect')
        g_cos = torch.nn.functional.conv2d(g_p*cost_p**2, sum_k)
        g_sin = torch.nn.functional.conv2d(g_p*sint_p**2, sum_k)
        g_2cs = torch.nn.functional.conv2d(2*g_p*sint_p*cost_p, sum_k)
        sum_g = torch.nn.functional.conv2d(g_p, sum_k)
        cd = ((cost**2)*g_cos+(sint**2)*g_sin+cost*sint*g_2cs)/(sum_g+1e-7)
        return out, cd


def hong1998(im, blk_sz=(16, 16), wd_sz=(3, 3), device=None):
    """使用1998年HongLin使用的方法估计指纹方向场。
    首先使用1990年Rao的方法估计指纹方向场，然后使用高斯滤波平滑方向场
    im是需要处理的指纹图像。
    blk_sz是估计方向场时的图像块大小，可以为整数或2维向量。
    wd_sz是平滑方向场的窗口大小，可以为整数或2维向量。
    device是数组转化为张量后使用的设备"""
    # 处理输入参数
    if isinstance(blk_sz, int):
        ksp = blk_sz, blk_sz
    else:
        ksp = blk_sz
    if isinstance(wd_sz, int):
        wsp = wd_sz, wd_sz
    else:
        wsp = wd_sz
    # 估计方向场
    imt = type_as(im, md="t", device=device)
    imt, im_sp = imt_pad_blk(imt, ksp)
    hg, wg = imt_cal_grad(imt)
    vy = imt_sum_average(2*hg*wg, ksp, kmd="s", s=ksp, keep_shape=False)
    vx = imt_sum_average(hg*hg-wg*wg, ksp, kmd="s", s=ksp, keep_shape=False)
    theta = 0.5*torch.atan2(vy, vx)
    # 平滑方向场
    phi_y, phi_x = torch.sin(2*theta), torch.cos(2*theta)
    phi_y = imt_gaussian(phi_y, wsp)
    phi_x = imt_gaussian(phi_x, wsp)
    out = 0.5*torch.atan2(phi_y, phi_x)
    out = out.repeat_interleave(ksp[-1], -1).repeat_interleave(ksp[-2], -2)
    out = imt_pad_crop(out, im_sp)
    out = type_as(out, im)
    del ksp, wsp, imt, im_sp, hg, wg, vy, vx, theta, phi_y, phi_x
    gc.collect()
    return out


def bazen2002(im, blk_sz, device=None):
    """使用2002年Bazen使用的方法估计指纹方向场。
    与1998年Hong相同，基于1990年Rao的方法，但是该方法中只指出了一个更加明确的方向场可信度估计方法
    im是需要处理的指纹图像。
    blk_sz是估计方向场时的图像块大小，可以为整数或2维向量。
    device是数组转化为张量后使用的设备"""
    # 处理输入参数
    if isinstance(blk_sz, int):
        ksp = blk_sz, blk_sz
    else:
        ksp = blk_sz
    # 估计方向场
    imt = type_as(im, md="t", device=device)
    hg, wg = imt_cal_grad(imt)
    hwg, hhg, wwg = 2*hg*wg, hg*hg, wg*wg
    hwg = imt_gaussian(hwg, ksp)
    hhg = imt_gaussian(hhg, ksp)
    wwg = imt_gaussian(wwg, ksp)
    out = 0.5*torch.atan2(hwg, hhg-wwg)
    # 计算方向场可信度
    cd = torch.sqrt((hhg-wwg)**2+hwg**2)/(hhg+wwg+1e-8)
    out = type_as(out, im)
    cd = type_as(cd, im)
    del ksp, imt, hg, wg, hwg, hhg, wwg
    gc.collect()
    return out, cd


def scholar_x(im, blk_sz, sg_sz=(9, 9), sa_sz=(25, 25), device=None):
    """从网络上找到的方向场估计算法
    基于1990年Rao的方法，多次使用了高斯滤波平滑提取到的特征，使用了2002年Bazen的置信度计算方法
    im是需要处理的指纹图像。
    blk_sz是估计方向场时的图像块大小，可以为整数或2维向量。
    sg_sz是平滑梯度时使用的卷积核大小，可以为整数或2维向量。
    sa_sz是平滑角度时使用的卷积核大小，可以为整数或2维向量。
    device是数组转化为张量后使用的设备"""
    # 处理输入参数
    if isinstance(blk_sz, int):
        ksp = blk_sz, blk_sz
    else:
        ksp = blk_sz
    if isinstance(sg_sz, int):
        gsp = sg_sz, sg_sz
    else:
        gsp = sg_sz
    if isinstance(sa_sz, int):
        asp = sa_sz, sa_sz
    else:
        asp = sa_sz
    # 计算梯度及有关变量
    imt = type_as(im, md="t", device=device)
    hg, wg = imt_cal_grad(imt)
    hg = imt_gaussian(hg, gsp)
    wg = imt_gaussian(wg, gsp)
    hwg, hhg, wwg = 2*hg*wg, hg*hg, wg*wg
    hwg = imt_gaussian(hwg, ksp)
    hhg = imt_gaussian(hhg, ksp)
    wwg = imt_gaussian(wwg, ksp)
    # 计算方向场
    rho = torch.sqrt(hwg**2+(hhg-wwg)**2)+1e-8
    sin2theta = hwg/rho
    cos2theta = (hhg-wwg)/rho
    sin2theta, im_sp = imt_pad_blk(sin2theta, asp)
    cos2theta = imt_pad_blk(cos2theta, asp)[0]
    sin2theta = imt_gaussian(sin2theta, asp, s=asp, keep_shape=False)
    cos2theta = imt_gaussian(cos2theta, asp, s=asp, keep_shape=False)
    out = 0.5*torch.atan2(sin2theta, cos2theta)
    out = out.repeat_interleave(asp[-1], -1).repeat_interleave(asp[-2], -2)
    out = imt_pad_crop(out, im_sp)
    out = type_as(out, im)
    # 计算方向场可信度
    rho = (hhg+wwg)/rho
    rho = imt_pad_blk(rho, asp)[0]
    rho = imt_gaussian(rho, asp, s=asp, keep_shape=False) + 1e-8
    cd = torch.sqrt(cos2theta**2 + sin2theta**2) / rho
    cd = cd.repeat_interleave(asp[-1], -1).repeat_interleave(asp[-2], -2)
    cd = imt_pad_crop(cd, im_sp)
    cd = type_as(cd, im)
    del ksp, gsp, asp, imt, hg, wg, hwg, hhg, wwg, rho, sin2theta, cos2theta
    gc.collect()
    return out, cd
