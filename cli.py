import argparse
import modal

# 和 app.py 里的 App 名保持一致
stub = modal.App.from_name("stable-diffusion-3-medium")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run SD3 Medium on Modal from CLI")
    parser.add_argument("--prompt", required=True, help="正向提示词")
    parser.add_argument("--negative", default="", help="反向提示词，可选")
    parser.add_argument("--steps", type=int, default=28, help="采样步数")
    parser.add_argument("--guidance", type=float, default=7.0, help="CFG 引导系数")
    parser.add_argument("--width", type=int, default=1024, help="生成图像宽度")
    parser.add_argument("--height", type=int, default=1024, help="生成图像高度")
    args = parser.parse_args()

    with stub.run():
        result = stub.run_sd3.call(
            args.prompt,
            negative_prompt=args.negative,
            steps=args.steps,
            guidance_scale=args.guidance,
            width=args.width,
            height=args.height
        )
        print(result)

