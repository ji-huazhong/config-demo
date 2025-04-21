import sys
from contextlib import contextmanager

import hydra  
from omegaconf import DictConfig, OmegaConf
from jsonargparse import ArgumentParser


def dict_to_args(dictionary):
    result = []

    def traverse_dict(current_dict, prefix=""):
        for key, value in current_dict.items():
            new_prefix = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                traverse_dict(value, new_prefix)
            else:
                if isinstance(value, bool):
                    value = str(value).lower()
                arg = f"--{new_prefix}={value}"
                result.append(arg)

    traverse_dict(dictionary)
    return result


def add_arguments(parser, arg_list):
    for arg in arg_list:
        # 分割参数名和类型，这里简单假设参数值类型根据值自动推断，你也可以根据需求更精细处理
        param_name = arg.split('=')[0].lstrip('--')
        try:
            # 尝试将值转换为整数
            int(arg.split('=')[1])
            param_type = int
        except ValueError:
            try:
                # 尝试将值转换为布尔值
                if arg.split('=')[1].lower() in ['true', 'false']:
                    param_type = bool
                else:
                    param_type = str
            except IndexError:
                param_type = str
        parser.add_argument(f'--{param_name}', type=param_type)
    return parser


@contextmanager
def init_context(new_argv):
    """
    context manager to temporarily change sys.argv
    """
    original_argv = sys.argv.copy()
    try:
        # todo: 待确认是否需要把sys.argv[0]也替换掉
        sys.argv = new_argv
        print(f"当前超参数为: {sys.argv}")
        yield
    finally:
        sys.argv = original_argv
        print(f"恢复超参数为: {sys.argv}")


@hydra.main(version_base=None, config_path="../configs", config_name="m8")  
def my_app(cfg : DictConfig) -> None:
    # 禁止hybra创建输出目录
    # import hydra.core.hydra_config
    # from hydra.core.hydra_config import HydraConfig
    # HydraConfig.get().output_subdir = None
    print(OmegaConf.to_yaml(cfg)) # 打印配置
    print('-' * 20)
    cfg_dict = OmegaConf.to_container(cfg, resolve=True)
    args_list = dict_to_args(cfg_dict)
    print(args_list)

    parser = ArgumentParser()
    parser = add_arguments(parser, args_list)
    with init_context(args_list):
        config = parser.parse_args()
    print(config)


if __name__ == "__main__":  
    my_app()
