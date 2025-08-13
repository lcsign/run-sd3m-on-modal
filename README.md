 



# 🖼 项目简介

**run-sd3m-on-modal** 是一个基于 **Stable Diffusion 3 Medium（SD3M）** 的云端推理项目，使用 **Modal** 云算力平台运行，无需本地 GPU 和复杂环境配置即可快速生成高质量图像。  
它适合：
- 🖥 无本地高性能显卡的开发者或爱好者  
- 🚀 想减少本地部署复杂度的人  
- 🧪 需要高频迭代文生图模型的创作者  

---

- **云端 GPU 推理**：按需运行，任务结束自动释放资源  
- **灵活可调**：分辨率、步数、提示词、负面提示等都能自定义  
- **安全的密钥管理**：采用 `.env` 文件存储 Token，避免硬编码泄露  
- **可扩展性强**：支持替换调度器、添加后处理等功能  
- **高可复用**：可将推理入口部署为 Modal 持久服务，随时调用  

---

## 📦 环境准备
1. **Python 3.10+**  
2. **Hugging Face 账号**（并接受 SD3M 模型协议）  
3. **Modal 账号** + 安装 CLI 工具  
4. **Hugging Face Token**（具备模型访问权限）  

---

## ⚙ 安装与配置

### 1️⃣ 克隆仓库
```bash
git clone git@github.com:lcsign/run-sd3m-on-modal.git
cd run-sd3m-on-modal
```

### 2️⃣ 创建虚拟环境
```bash
python -m venv .venv
# Windows PowerShell
. .\.venv\Scripts\Activate.ps1
# macOS / Linux
# source .venv/bin/activate
```

### 3️⃣ 安装依赖
```bash
pip install -U pip
pip install -r requirements.txt
```

### 4️⃣ 配置 `.env`
在根目录创建 `.env` 文件：
```env
HF_TOKEN=你的_huggingface_token
HF_HUB_ENABLE_HF_TRANSFER=1
SD3M_WIDTH=1024
SD3M_HEIGHT=1024
SD3M_STEPS=28
SD3M_GUIDANCE=4.5
```
> 注意：`.gitignore` 中应包含 `.env`

### 5️⃣ 登录 Modal
```bash
pip install modal
modal token set
```

---

## 🚀 使用方法

### 单张图片生成
```bash
modal run modal_app.py::infer \
  --prompt "黄昏下的赛博朋克城市，霓虹灯闪烁，雨后街道映出光影" \
  --negative "低质量，模糊，水印" \
  --steps 28 --guidance 4.5 --width 1024 --height 1024 --seed 123
```

### 批量生成
将提示词写入 `prompts.txt`（每行一个）：
```bash
modal run modal_app.py::batch_infer --file prompts.txt
```

### 下载结果（使用 Modal Volume 存储）
```bash
modal volume get sd3m-outputs /results ./output
```

---

## 🔍 常见问题

**1. 第一次运行很慢**  
- 因为需要下载模型权重，可使用 Modal Volume 缓存，加快后续运行  

**2. GitHub 推送被拦截**  
- 原因：硬编码了 Token  
- 解决：用 `.env` 管理，并清理提交历史中的敏感信息  

**3. 生成超时/显存不足**  
- 降低分辨率或步数，减少批量大小  

---

## 📂 项目结构建议
```
run-sd3m-on-modal/
├─ modal_app.py        # Modal 入口函数 infer/batch_infer
├─ sd3m_runner/        # 推理逻辑与工具函数
│  ├─ pipeline.py
│  └─ utils.py
├─ prompts.txt
├─ requirements.txt
├─ .env.example
├─ .gitignore
└─ output/             # 本地输出（gitignore）
```

---


