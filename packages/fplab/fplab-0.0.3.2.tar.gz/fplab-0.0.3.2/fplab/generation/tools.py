import numpy as np
from fplab.tools.image import type_as
from scipy.ndimage import distance_transform_edt


def perlin2d(h, w, seed=0):
    """2维Perlin噪声

    :param:h       2维数组，对应每个像素的h坐标
    :param:w       2维数组，对应每个像素的w坐标
    :param:seed    随机数种子
    """
    assert len(h.shape) == len(w.shape) == 2
    assert h.shape[0] == w.shape[0]
    assert h.shape[1] == w.shape[1]
    n = max(h.shape[0], h.shape[1])
    # 排列表
    np.random.seed(seed)
    ptable = np.arange(n, dtype=int)
    np.random.shuffle(ptable)
    ptable = np.stack([ptable, ptable]).flatten()
    # 格点梯度
    hi, wi = h.astype(int), w.astype(int)
    id00 = ptable[ptable[hi % n] + wi % n] % 4
    id01 = ptable[ptable[hi % n] + wi % n + 1] % 4
    id10 = ptable[ptable[hi % n + 1] + wi % n] % 4
    id11 = ptable[ptable[hi % n + 1] + wi % n + 1] % 4
    vectors = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
    g00 = vectors[id00]
    g01 = vectors[id01]
    g10 = vectors[id10]
    g11 = vectors[id11]
    # 坐标转化
    hf0, wf0 = h - hi, w - wi
    hf1 = 6 * hf0 ** 5 - 15 * hf0 ** 4 + 10 * hf0 ** 3
    wf1 = 6 * wf0 ** 5 - 15 * wf0 ** 4 + 10 * wf0 ** 3
    # 格点影响力
    c00 = g00[:, :, 0] * hf0 + g00[:, :, 1] * wf0
    c01 = g01[:, :, 0] * hf0 + g01[:, :, 1] * (wf0 - 1)
    c10 = g10[:, :, 0] * (hf0 - 1) + g10[:, :, 1] * wf0
    c11 = g11[:, :, 0] * (hf0 - 1) + g11[:, :, 1] * (wf0 - 1)
    # 插值
    y1 = c00 + hf1 * (c10 - c00)
    y2 = c01 + hf1 * (c11 - c01)
    out = y1 + wf1 * (y2 - y1)
    return out


def perlin2d_octave(grid_h, grid_w, o=1, p=0.5, la=2, seed=0, need_norm=True):
    """2维Perlin噪声

    :param:grid_h       数组，对应每个像素的h坐标
    :param:grid_w       数组，对应每个像素的w坐标
    :param:o            octaves, 倍频程
    :param:p            persistence
    :param:la           lacunarity
    :param:seed         随机数种子
    :param:need_norm    是否将结果归一化
    """
    ind_h, ind_w = np.meshgrid(grid_h, grid_w, indexing='ij')
    noise = np.zeros(ind_h.shape)
    max_v = 0
    for i in range(o):
        noise += perlin2d(ind_h*la**i, ind_w*la**i, seed=seed) * p**i
        max_v += p**i
    if need_norm:
        return noise/max_v
    else:
        return noise


def cappelli2004(mk, tb=20, pl=0.1, k=3, o=3, p=0.5, la=2, freq=16):
    """cappelli2004年提出的噪声

    :param:mk           指纹mask
    :param:tb           有效距离范围
    :param:pl           基础噪声概率
    :param:k
    :param:o            octaves, 倍频程
    :param:p            persistence
    :param:la           lacunarity
    :param:freq         控制噪声精细程度，越小越精细
    """
    mka = type_as(mk, md="a")
    dta = distance_transform_edt(mka)
    dta[dta > tb] = 0
    dta = np.where(dta > 0, (tb-dta)/tb, dta)
    npa = pl*(1+dta**3)
    grid_h = np.arange(mka.shape[0])/(o*freq)
    grid_w = np.arange(mka.shape[1])/(o*freq)
    noise = perlin2d_octave(grid_h, grid_w, o, p, la, seed=np.random.randint(999))
    noise = (noise-noise.min())/(noise.max()-noise.min())
    npa = npa*(1+noise**k)
    return type_as(npa, mk)
