import os
from huggingface_hub import snapshot_download, HfApi

def download_model(
    model_id: str = "stabilityai/stable-diffusion-3-medium-diffusers",
    cache_dir: str = "/model-cache",
    token_env: str = "HUGGINGFACE_TOKEN"
):
    """
    从 Hugging Face 下载 diffusers 模型（如已存在则跳过下载）
    """
    token = os.environ.get(token_env)
    if not token:
        raise EnvironmentError(f"环境变量 {token_env} 未设置，无法访问 Hugging Face 私有模型")

    # 禁用遥测，防编码问题
    os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

    # 打印账号信息 & token 前缀
    who = HfApi().whoami(token=token)
    print(f"HF account: {who.get('name') or who.get('email')}, token prefix: {token[:8]}...")
    print(f"📦 正在检查/下载模型缓存: {model_id}")

    snapshot_download(
        repo_id=model_id,
        cache_dir=cache_dir,
        token=token,
        resume_download=True,
        local_files_only=False,
        user_agent="hfclient"
    )

    print(f"✅ 模型已准备好并缓存到 {cache_dir}")
    return cache_dir
