import numpy as np


def loss_mse(imga, imgb):
    mse = 0.0
    for chan in (0,1,2):
        (a, b) = imga[:,:,chan], imgb[:,:,chan]
        diff = a.astype(np.longlong) - b.astype(np.longlong)
        scale = a.shape[0] * a.shape[1]
        mse_s = np.sum(diff**2)/scale
        mse = mse + mse_s
    return mse/3


def loss_mae(imga, imgb):
    mae = 0.0
    for chan in (0,1,2):
        (a, b) = imga[:,:,chan], imgb[:,:,chan]
        diff = a.astype(np.int16) - b.astype(np.int16)
        scale = a.shape[0] * a.shape[1]
        mae_s = np.sum(np.abs(diff))/scale
        mae = mae + mae_s
    return mae/3
    
    
def loss_psnr(a, b):
    psnr = 10 * np.log10((255 ** 2)/loss_mse(a, b))
    return psnr


def loss_ssim_rgb(imga, imgb):
    ssim = 0.0
    for chan in (0,1,2):
        (a, b) = imga[:,:,chan], imgb[:,:,chan]
        ua, ub = a.mean(), b.mean()
        sigmaa, sigmab = np.var(a), np.var(b)
        # covab = np.cov(np.stack((a.reshape(-1), b.reshape(-1)), axis=0))
        covab_ = 0
        ar, br = a.reshape(-1), b.reshape(-1)
        for i in range(len(ar)):
            covab_ += (ar[i] - ua) * (br[i] - ub)
        covab_ /= len(ar) - 1
        k_1, k_2 = 0.01, 0.03
        L = 255
        c_1 = (k_1 * L) ** 2
        c_2 = (k_2 * L) ** 2

        ssim = ssim + ((2*ua * ub + c_1) * (2 * covab_ + c_2))/((ua**2 + ub**2 + c_1) * (sigmaa + sigmab + c_2))

    return ssim/3



