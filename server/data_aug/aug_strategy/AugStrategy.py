from data_aug.aug_strategy.BrightnessStrategy import brightness_aug
from data_aug.aug_strategy.FogStrategy import fog_aug
from data_aug.aug_strategy.HighTemperatureStrategy import high_temperature_aug
from data_aug.aug_strategy.MotionBlurStrategy import motion_blur_aug
from data_aug.aug_strategy.RainStrategy import rain_aug
from data_aug.aug_strategy.SaltPepperStrategy import noise_aug
from data_aug.aug_strategy.ShadowStrategy import shadow_aug
from data_aug.aug_strategy.SnowStrategy import snow_aug
from data_aug.aug_strategy.SpeckleNoiseStrategy import speckle_noise_aug
from data_aug.aug_strategy.VagueStrategy import vague_aug


def data_aug(aug_type, task_obj, config_obj, target_dir):
    if (aug_type == 'Shadow'):
        shadow_aug(task_obj, config_obj, target_dir)
    if (aug_type == 'MotionBlur'):
        motion_blur_aug(task_obj, config_obj, target_dir)
    if (aug_type == 'HighTemperature'):
        high_temperature_aug(task_obj, config_obj, target_dir)

    if (aug_type == 'Fog'):
        fog_aug(task_obj, config_obj, target_dir)
    if (aug_type == 'Rain'):
        rain_aug(task_obj, config_obj, target_dir)
    if (aug_type == 'Snow'):
        snow_aug(task_obj, config_obj, target_dir)



