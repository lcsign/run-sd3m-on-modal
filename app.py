import os
import modal
from modal import Volume
from sd3_runner import generate_image  # 引入你的推理函数

stub = modal.App("stable-diffusion-3-medium")
volume = Volume.from_name("sd3-model-cache", create_if_missing=True)

image = (
    modal.Image.debian_slim()
    .pip_install(
        "torch", "transformers", "diffusers", "accelerate",
        "safetensors", "huggingface_hub","sentencepiece"

    )
    .add_local_dir(".", remote_path="/root")
)

# 🔍 预检函数
@stub.function(
    image=image,
    secrets=[modal.Secret.from_name("huggingface-token")],
    volumes={"/model-cache": volume}
)
def preflight(model_id: str = "stabilityai/stable-diffusion-3-medium-diffusers"):
    from huggingface_hub import hf_hub_download, HfApi

    os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

    token = os.environ.get("HUGGINGFACE_TOKEN")
    if not token:
        raise RuntimeError("HUGGINGFACE_TOKEN is missing in environment")

    api = HfApi()
    who = api.whoami(token=token)
    print(f"HF account: {who.get('name') or who.get('email')}, token: {token[:8]}...")
    print(f"Testing access for: {model_id}")

    try:
        p = hf_hub_download(
            repo_id=model_id,
            filename="model_index.json",
            token=token,
            user_agent="hfclient",
            cache_dir="/model-cache"
        )
        print(f"✅ Access OK. model_index.json downloaded to: {p}")
    except Exception as e:
        print(f"❌ Access FAILED for {model_id}: {e}")
        print("Hints:")
        print("- 确保用的 Token 属于‘已在模型页面点过 Agree/Access 的同一账号’")
        print("- 如果你有多个 HF 账号，务必重新生成该账号的新 Token，并更新 Modal Secret")
        print("- 在模型页面右侧点 “Use in diffusers”，复制实际的 model_id（有时名称会变）")
        raise

# 🎯 推理主函数（CLI / modal run 调用）
@stub.function(
    image=image,
    secrets=[modal.Secret.from_name("huggingface-token")],
    volumes={"/model-cache": volume},
    gpu="A10G"
)
def run_sd3(prompt: str, negative_prompt: str = "", steps: int = 28, guidance_scale: float = 7.0,
            width: int = 1024, height: int = 1024):
    return generate_image(prompt, steps=steps, width=width, height=height)




