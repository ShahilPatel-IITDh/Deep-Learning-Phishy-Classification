import os
import numpy as np
from PIL import Image, ImageOps
from torchvision import transforms
import torch
import torch.nn.functional as F

def l2_norm(x):
    '''L2 Normalization'''
    if len(x.shape):
        x = x.reshape((x.shape[0], -1))
    return F.normalize(x, p=2, dim=1)

def pred_siamese(img_path, model, grayscale=False):
    img_size = 128
    mean = [0.5, 0.5, 0.5]
    std = [0.5, 0.5, 0.5]
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    img_transforms = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=mean, std=std),
    ])

    img = Image.open(img_path)
    img = img.convert("L").convert("RGB") if grayscale else img.convert("RGB")

    pad_color = 255 if grayscale else (255, 255, 255)
    img = ImageOps.expand(img, (
        (max(img.size) - img.size[0]) // 2, (max(img.size) - img.size[1]) // 2,
        (max(img.size) - img.size[0]) // 2, (max(img.size) - img.size[1]) // 2), fill=pad_color)

    img = img.resize((img_size, img_size))

    with torch.no_grad():
        img = img_transforms(img)
        img = img[None, ...].to(device)
        logo_feat = model.features(img)
        logo_feat = l2_norm(logo_feat).squeeze(0).cpu().numpy()

    return logo_feat

def siamese_inference(model, domain_map, logo_feat_list, file_name_list, shot_path, gt_bbox, t_s, grayscale=False):
    try:
        img = Image.open(shot_path)
        
    except OSError:
        print('Screenshot cannot be open')
        return None, None, None

    cropped = img.crop((gt_bbox[0], gt_bbox[1], gt_bbox[2], gt_bbox[3]))
    img_feat = pred_siamese(cropped, model, grayscale=grayscale)

    sim_list = logo_feat_list @ img_feat.T
    pred_brand_list = file_name_list

    assert len(sim_list) == len(pred_brand_list)

    idx = np.argsort(sim_list)[::-1][:3]
    pred_brand_list = np.array(pred_brand_list)[idx]
    sim_list = np.array(sim_list)[idx]

    top3_logolist = [Image.open(x) for x in pred_brand_list]
    top3_brandlist = [os.path.basename(os.path.dirname(x)) for x in pred_brand_list]
    top3_domainlist = [domain_map[x] for x in top3_brandlist]
    top3_simlist = sim_list

    for j in range(3):
        predicted_brand, predicted_domain = None, None

        if top3_brandlist[j] != top3_brandlist[0]:
            continue

        if top3_simlist[j] >= t_s:
            predicted_brand = top3_brandlist[j]
            predicted_domain = top3_domainlist[j]
            final_sim = top3_simlist[j]
        else:
            cropped, candidate_logo = resolution_alignment(cropped, top3_logolist[j])
            img_feat = pred_siamese(cropped, model, grayscale=grayscale)
            logo_feat = pred_siamese(candidate_logo, model, grayscale=grayscale)
            final_sim = logo_feat.dot(img_feat)
            if final_sim >= t_s:
                predicted_brand = top3_brandlist[j]
                predicted_domain = top3_domainlist[j]
            else:
                break

        if predicted_brand is not None:
            ratio_crop = cropped.size[0] / cropped.size[1]
            ratio_logo = top3_logolist[j].size[0] / top3_logolist[j].size[1]
            if max(ratio_crop, ratio_logo) / min(ratio_crop, ratio_logo) > 2.5:
                continue
            else:
                return predicted_brand, predicted_domain, final_sim

    return None, None, top3_simlist[0]

# Example usage:
# Define your Siamese model, domain_map, logo_feat_list, file_name_list, shot_path, gt_bbox, t_s, and grayscale.
# Then call siamese_inference to get the predicted brand and domain.