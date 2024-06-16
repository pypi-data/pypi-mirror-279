"""对MCC进行封装
xyt2txt
mindtct2txt
mcc_enroll
mcc_match
mcc_txt
mcc
"""

import numpy as np
from os import system
from pathlib import Path
from tqdm import tqdm
from fplab.tools.nbis import mindtct_n
from fplab.tools.array import IMA
from fplab.tools.image import get_data_dirs
from fplab.matching.tools import analyse_score
from time import strftime, localtime


def xyt2txt(xyt_d, txt_d, sp, dpi=500):
    """将xyt文件转化为mcc的txt形式
    xyt_d   xyt文件地址，字符串形式或Path形式
    txt_d   txt文件地址，字符串形式或Path形式
    sp      xyt文件对应的图像长宽，整数或2维整数元组
    dpi     xyt文件对应的图像分辨率，整数"""
    # 处理输入sp
    if isinstance(sp, int):
        h, w = sp, sp
    else:
        h, w = sp
    # 读取xyt文件
    with open(xyt_d, 'r') as xyt_f:
        mts = xyt_f.readlines()
    with open(txt_d, 'w') as txt_f:
        txt_f.write(f"{w}\n")
        txt_f.write(f"{h}\n")
        txt_f.write(f"{dpi}\n")
        txt_f.write(f"{len(mts)}\n")
        for i in range(len(mts)):
            mt = mts[i].strip().split()
            x = int(mt[0])
            y = h-int(mt[1])
            t = (int(mt[2])+180) % 360
            t = t/180.*np.pi
            txt_f.write(f"{x} {y} {t}\n")
    return txt_d


def mindtct2txt(ims_dir, mts_dir, src_dir=r'C:\SRC\NBIS\Main\bin\mindtct.exe', dpi=500, ext=".png"):
    """使用mindtct批量获取mcc能够处理的txt形式细节点
    ims_dir    图像地址，可以为单个图像地址或图像文件夹地址
    mts_dir    输出细节点文件夹地址
    src_dir    mindtct源程序地址
    dpi        xyt文件对应的图像分辨率，整数
    ext        图像后缀名"""
    info_d = str((Path(mts_dir)/"info").absolute())
    xyts_d = str((Path(mts_dir)/"xyts").absolute())
    txts_d = str((Path(mts_dir)/"txts").absolute())
    Path(info_d).mkdir(parents=True, exist_ok=True)
    Path(xyts_d).mkdir(parents=True, exist_ok=True)
    Path(txts_d).mkdir(parents=True, exist_ok=True)
    info_ds = mindtct_n(ims_dir, info_d, need_out=".xyt", src_dir=src_dir)
    xyt_ds = []
    txt_ds = []
    with tqdm(total=len(info_ds)) as pbar:
        pbar.set_description("将.xyt文件转化为.txt文件")
        for d in info_ds:
            img_d = str(Path(d).absolute()).replace(info_d, str(Path(ims_dir).absolute())).replace(".xyt", ext)
            xyt_d = str(Path(d).absolute()).replace(info_d, xyts_d)
            txt_d = str(Path(d).absolute()).replace(info_d, txts_d).replace(".xyt", ".txt")
            with open(d, "r") as f1:
                with open(xyt_d, "w") as f2:
                    f2.write(f1.read())
            xyt_ds.append(xyt_d)
            sp = IMA.read(img_d).rgb2l().shape
            txt_ds.append(xyt2txt(d, txt_d, sp, dpi=dpi))
            pbar.update(1)
    return xyt_ds, txt_ds


def mcc_enroll(txt_d, sv_d, script_d,
               enroller_d=r"C:\SRC\MCC\Executables\MccEnroller.exe",
               enroller_p_d=r"C:\SRC\MCC\Executables\MccSdk1.4OptimalEnrollParameters.xml"):
    """MCC注册器"""
    system(enroller_d+" "+txt_d+" "+sv_d+" "+enroller_p_d+" "+script_d)
    with open(script_d, "r") as f:
        if f.readlines()[-1].strip()[-2:] != 'OK':
            print("注册失败！")
    return sv_d


def mcc_match(p_d, g_d, script_d,
              matcher_d=r"C:\SRC\MCC\Executables\MccMatcher.exe",
              matcher_p_d=r"C:\SRC\MCC\Executables\MccSdk1.4OptimalMatchParameters.xml",
              enroller_p_d=r"C:\SRC\MCC\Executables\MccSdk1.4OptimalEnrollParameters.xml"):
    """MCC匹配器"""
    system(matcher_d+" "+p_d+" "+g_d+" "+matcher_p_d+" "+script_d+" "+enroller_p_d)
    with open(script_d, "r") as f:
        script = f.readlines()[-1].strip().split(" ")
        if script[-2] == 'OK':
            return float(script[-1])
        else:
            return 0


def mcc_txt(p_txt_dirs, g_txt_dirs, script_dir=None, verbose_flag=False,
            need_enroll_p=False, need_enroll_g=False, p_name=None, g_name=None,
            enroller_d=r"C:\SRC\MCC\Executables\MccEnroller.exe",
            matcher_d=r"C:\SRC\MCC\Executables\MccMatcher.exe",
            enroller_p_d=r"C:\SRC\MCC\Executables\MccSdk1.4OptimalEnrollParameters.xml",
            matcher_p_d=r"C:\SRC\MCC\Executables\MccSdk1.4OptimalMatchParameters.xml",):
    """封装MCC程序
    p_txt_dirs是待识别细节点，可以为细节点文件地址列表或细节点文件所在目录
    g_txt_dirs是模板细节点，可以为细节点文件地址列表或细节点文件所在目录
    script_dir为结果文本文件所在路径，默认为./scripts
    verbose_flag用来标识是否输出详细信息
    need_enroll_p和need_enroll_g用来标识是否需要重新注册，
    若为False,则p_txt_dirs和g_txt_dirs为已经注册好的细节点
    若为True,则注册p_txt_dirs和g_txt_dirs，并将结果存放到"txts"->"mccs"
    p_name, g_name用来标识数据
    enroller_dir是MCC注册器所在路径
    matcher_dir是MCC匹配器所在路径
    enroller_p_d是MCC注册器参数路径
    matcher_p_d是MCC匹配器参数路径
    """
    if isinstance(p_txt_dirs, list):
        probe_dirs = p_txt_dirs
    else:
        probe_dirs = []
        probe_dirs = get_data_dirs(Path(p_txt_dirs), probe_dirs, ext=".txt")
    if isinstance(g_txt_dirs, list):
        gallery_dirs = g_txt_dirs
    else:
        gallery_dirs = []
        gallery_dirs = get_data_dirs(Path(g_txt_dirs), gallery_dirs, ext=".txt")
    match_score = np.zeros((len(probe_dirs), len(gallery_dirs)), dtype=np.float32)
    if isinstance(script_dir, str):
        script_path = Path(script_dir)
    else:
        script_path = Path("scripts") / strftime("%Y%m%d%H%M%S", localtime())
    script_path.mkdir(parents=True, exist_ok=True)
    if need_enroll_p:
        temp = []
        script_d = str((script_path/"enroll_p.txt").absolute())
        with tqdm(total=len(probe_dirs)) as pbar:
            pbar.set_description("正在注册探测指纹")
            for d in probe_dirs:
                sv_d = d.replace("txts", "mccs")
                Path(sv_d).parent.mkdir(parents=True, exist_ok=True)
                out = mcc_enroll(d, sv_d, script_d, enroller_d=enroller_d, enroller_p_d=enroller_p_d)
                temp.append(out)
                pbar.update(1)
        probe_dirs = temp
    if need_enroll_g:
        temp = []
        script_d = str((script_path/"enroll_g.txt").absolute())
        with tqdm(total=len(gallery_dirs)) as pbar:
            pbar.set_description("正在注册库指纹")
            for d in gallery_dirs:
                sv_d = d.replace("txts", "mccs")
                Path(sv_d).parent.mkdir(parents=True, exist_ok=True)
                out = mcc_enroll(d, sv_d, script_d, enroller_d=enroller_d, enroller_p_d=enroller_p_d)
                temp.append(out)
                pbar.update(1)
        gallery_dirs = temp
    with tqdm(total=match_score.size) as pbar:
        pbar.set_description("正在匹配")
        script_d = str((script_path/"match.txt").absolute())
        for i in range(len(probe_dirs)):
            for j in range(len(gallery_dirs)):
                match_score[i, j] = mcc_match(probe_dirs[i],
                                              gallery_dirs[j],
                                              script_d,
                                              matcher_d=matcher_d,
                                              matcher_p_d=matcher_p_d,
                                              enroller_p_d=enroller_p_d)
                pbar.update(1)
    if verbose_flag:
        score_file = script_path / "match_score.txt"
        score_data = script_path / 'match_score.npy'
        probe_file = script_path / 'probe_dirs.txt'
        gallery_file = script_path / 'gallery_dirs.txt'
        np.save(score_data, match_score)
        with open(probe_file, "w") as pf:
            for pd in probe_dirs:
                pf.write(pd+"\n")
        with open(gallery_file, "w") as gf:
            for gd in gallery_dirs:
                gf.write(gd+"\n")
        with open(score_file, "w") as sf:
            sf.write(f"目标数据集:\t\t{p_name}\n")
            sf.write(f"库数据集:\t\t{g_name}\n")
            sf.write(f"文本路径:\t\t{str(script_path.absolute())}\n")
            sf.write(f"匹配结果路径:\t\t{str(score_data.absolute())}\n")
            sf.write(f"目标路径列表:\t\t{str(probe_file.absolute())}\n")
            sf.write(f"库路径列表:\t\t{str(gallery_file.absolute())}\n")
            sf.write(f"目标数据数目:\t\t{len(probe_dirs)}\n")
            sf.write(f"库数据数目:\t\t{len(gallery_dirs)}\n")
            sf.write(f"匹配分数最大值:\t\t{match_score.max()}\n")
            sf.write(f"匹配分数最小值:\t\t{match_score.min()}\n")
            sf.write(f"若匹配分数最小值小于0，则该结果没有参考性。\n")
            sf.write(f"匹配分数均值:\t\t{match_score.mean()}\n")
            sf.write(f"匹配分数中值:\t\t{np.median(match_score)}\n")
            sf.write("匹配分数\t\t目标指纹\t\t\t\t\t\t\t\t\t\t\t\t库指纹\n")
            for i in range(len(probe_dirs)):
                for j in range(len(gallery_dirs)):
                    sf.write(f"{match_score[i, j]}\t\t\t{probe_dirs[i]}\t\t\t{gallery_dirs[j]}\n")
    return match_score, probe_dirs, gallery_dirs, script_path


def mcc(ps_dir=None, gs_dir=None, p_txt_dirs=None, g_txt_dirs=None,
        need_enroll_p=False, need_enroll_g=False, need_analyse=False,
        script_dir=None, verbose_flag=False, p_name=None, g_name=None,
        identify_ranks=None, verify_ranks=None,
        mindtct_dir=r'C:\SRC\NBIS\Main\bin\mindtct.exe',
        enroller_d=r"C:\SRC\MCC\Executables\MccEnroller.exe",
        matcher_d=r"C:\SRC\MCC\Executables\MccMatcher.exe",
        enroller_p_d=r"C:\SRC\MCC\Executables\MccSdk1.4OptimalEnrollParameters.xml",
        matcher_p_d=r"C:\SRC\MCC\Executables\MccSdk1.4OptimalMatchParameters.xml",
        j_func=None, need_eer=True, **kwargs):
    """将mindtct和mcc组合到一起
    ps_dir, gs_dir为目标图像文件夹地址和库图像文件夹地址
    p_txt_dirs, g_txt_dirs为细节点地址列表或者细节点所在目录
    need_enroll_p和need_enroll_g标识是否需要注册细节点，若需要标识则细节点地址中必须有txts
    p_dirs, g_dirs, p_txt_dirs, g_txt_dirs可以为单个图像地址或图像文件夹地址，且dirs和txt_dirs只需存在一个
    script_dir为结果文本文件所在路径，默认为./scripts
    verbose_flag用来标识是否输出详细信息
    p_name, g_name用来标识数据
    need_analyse控制是否分析数据
    identify_ranks是识别精度，比如rank-1, rank-5，可以为整数或整数列表
    verify_ranks控制匹配分数阈值，可以为整数或整数列表
    mindtct_dir, enroller_d, matcher_d, enroller_p_d和matcher_p_d是一些外部文件的地址
    need_eer是否需要输出eer
    j_func和**kwargs用来根据文件地址判断两个文件是否属于同一个指纹"""
    if ps_dir:
        temp = Path(ps_dir).stem
        p_txt_dirs = mindtct2txt(ps_dir, ps_dir.replace(temp, temp+"_mnt"), src_dir=mindtct_dir)[1]
        need_enroll_p = True
    if gs_dir:
        temp = Path(gs_dir).stem
        g_txt_dirs = mindtct2txt(gs_dir, gs_dir.replace(temp, temp+"_mnt"), src_dir=mindtct_dir)[1]
        need_enroll_g = True
    temp = mcc_txt(p_txt_dirs, g_txt_dirs, script_dir, verbose_flag, need_enroll_p, need_enroll_g, p_name, g_name,
                   enroller_d, matcher_d, enroller_p_d, matcher_p_d)
    match_score, probe_dirs, gallery_dirs, script_path = temp
    if need_analyse:
        script_stem = str(script_path.absolute())
        out = analyse_score(match_score, probe_dirs, gallery_dirs, script_stem,
                            rk_i=identify_ranks, rk_v=verify_ranks, j_func=j_func,
                            need_eer=need_eer, **kwargs)
        return out
    else:
        return match_score, probe_dirs, gallery_dirs, script_path
