import argparse
import statistics
import time

import torch
from torch.utils.data import DataLoader

import opencood.hypes_yaml.yaml_utils as yaml_utils
from opencood.tools import train_utils, infrence_utils
from opencood.data_utils.datasets import build_dataset
from opencood.utils.seg_utils import cal_iou_training


def test_parser():
    parser = argparse.ArgumentParser(description="synthetic data generation")
    parser.add_argument('--model_dir', type=str, required=True,
                        help='Continued training path')
    parser.add_argument('--model_type', type=str, default='dynamic',
                        help='dynamic or static prediction')
    opt = parser.parse_args()
    return opt


class Testspace:
    def __init__(self, model_dir='opencood/logs/cobevt', model_type='dynamic'):
        self.model_dir = model_dir
        self.model_type = model_type

def inference_data(model_dir,validate_dir,result_path,model_type,visual_flag,ego_id):

    # parser = argparse.ArgumentParser(description="synthetic data generation")
    # parser.add_argument('--model_dir', type=str, default=model_dir,
    #                     help='Continued training path')
    # parser.add_argument('--model_type', type=str, default=model_type,
    #                     help='dynamic or static prediction')
    # opt = parser.parse_args()

    opt = Testspace(model_dir,model_type)
    print('opt------------------------------------------------------')
    print(opt)
    hypes = yaml_utils.load_yaml(None, opt)
    print('hypes------------------------------------------------------')
    print(hypes)
    hypes['validate_dir'] = validate_dir
    print('hypes------------------------------------------------------')
    print(hypes)

    print('Dataset Building')
    opencood_dataset = build_dataset(hypes, visualize=True, train=False,ego_id = ego_id)
    print('opencood_dataset--------------------------------')
    print(opencood_dataset)
    data_loader = DataLoader(opencood_dataset,
                             batch_size=1,
                             num_workers=10,
                             collate_fn=opencood_dataset.collate_batch,
                             shuffle=False,
                             pin_memory=False,
                             drop_last=False)

    print('Creating Model')
    model = train_utils.create_model(hypes)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # we assume gpu is necessary
    if torch.cuda.is_available():
        model.to(device)

    print('Loading Model from checkpoint')
    saved_path = opt.model_dir
    _, model = train_utils.load_saved_model(saved_path, model)
    model.eval()

    dynamic_ave_iou = []
    static_ave_iou = []
    lane_ave_iou = []

    for i, batch_data in enumerate(data_loader):
        print(i)
        with torch.no_grad():
            #torch.cuda.synchronize()

            batch_data = train_utils.to_device(batch_data, device)
            output_dict = model(batch_data['ego'])
            # visualization purpose
            output_dict = \
                opencood_dataset.post_process(batch_data['ego'],
                                              output_dict)

            if(visual_flag):
                # 结果可视化
                infrence_utils.camera_inference_visualization(output_dict,
                                                          batch_data,
                                                          result_path,
                                                          i,
                                                          opt.model_type,
                                                          ego_id)

            iou_dynamic, iou_static = cal_iou_training(batch_data,
                                                       output_dict)
            static_ave_iou.append(iou_static[1])
            dynamic_ave_iou.append(iou_dynamic[1])
            lane_ave_iou.append(iou_static[2])

    _static_ave_iou = statistics.mean(static_ave_iou)
    _dynamic_ave_iou = statistics.mean(dynamic_ave_iou)
    _lane_ave_iou = statistics.mean(lane_ave_iou)

    print('Road IoU: %f' % _static_ave_iou)
    print('Lane IoU: %f' % _lane_ave_iou)
    print('Dynamic IoU: %f' % _dynamic_ave_iou)

    return (static_ave_iou,lane_ave_iou,dynamic_ave_iou)


if __name__ == '__main__':
    inference_data()
