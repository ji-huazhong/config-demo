import sys

from jsonargparse import ArgumentParser

def main():
    sys_args = sys.argv
    breakpoint()
    parser = ArgumentParser()
    # 添加嵌套参数
    parser.add_argument('--model.network.tp', type=int, default=1, help='Set the value of model.network.tp')
    args = parser.parse_args()
    print(args.model)
    breakpoint()
    print(args)

if __name__ == "__main__":
    main()
    