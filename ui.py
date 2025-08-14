import gradio as gr
import subprocess
import tempfile
import os

BAT_PATH = r"D:\run_stable_diffusion_on_modal\start.bat"

def edit_and_run(prompt, width, height, steps):
    # 创建一个临时 bat 文件，把参数替换进模板
    with open(BAT_PATH, "r", encoding="utf-8") as f:
        bat_content = f.read()
    bat_content = bat_content.replace("A white cat sitting on a black sofa, cozy atmosphere", prompt)
    bat_content = bat_content.replace("set WIDTH=768", f"set WIDTH={width}")
    bat_content = bat_content.replace("set HEIGHT=768", f"set HEIGHT={height}")
    bat_content = bat_content.replace("set STEPS=28", f"set STEPS={steps}")

    tmp_bat = tempfile.NamedTemporaryFile(delete=False, suffix=".bat", mode="w", encoding="utf-8")
    tmp_bat.write(bat_content)
    tmp_bat.close()

    # 调用临时 bat
    subprocess.run([tmp_bat.name], shell=True)
    os.unlink(tmp_bat.name)

    if os.path.exists("output.png"):
        return "output.png"
    return None

with gr.Blocks() as demo:
    gr.Markdown("## SD3M 套娃 UI → 批处理 → 主程序")

    prompt = gr.Textbox(label="Prompt", value="A white cat sitting on a black sofa, cozy atmosphere")
    width = gr.Number(value=768, label="Width", precision=0)
    height = gr.Number(value=768, label="Height", precision=0)
    steps = gr.Number(value=28, label="Steps", precision=0)

    run_btn = gr.Button("运行")
    img = gr.Image(label="结果")

    run_btn.click(edit_and_run, [prompt, width, height, steps], img)

if __name__ == "__main__":
    demo.launch()
