from diffusers import StableDiffusion3Pipeline
import torch
import os

pipe = None

def load_model():
    global pipe
    if pipe is None:
        os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
        model_id = "stabilityai/stable-diffusion-3-medium-diffusers"
        token = os.environ.get("HUGGINGFACE_TOKEN")
        if not token:
            raise RuntimeError("HUGGINGFACE_TOKEN is missing in environment")
        print(f"Loading model: {model_id}, token prefix: {token[:8]}...")

        pipe = StableDiffusion3Pipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16,
            use_safetensors=True,
            cache_dir="/model-cache",
            token=token
        ).to("cuda")
    return pipe

def generate_image(prompt: str, steps: int = 30, width: int = 1024, height: int = 1024):
    pipe = load_model()
    image = pipe(
        prompt,
        negative_prompt="",               # SD3 支持 negative_prompt，可留空
        num_inference_steps=steps,
        guidance_scale=7.0,                # 推荐参数
        width=width,
        height=height
    ).images[0]
    out_path = "/model-cache/output.png"
    image.save(out_path)
    return f"✅ Image saved: {out_path}"
