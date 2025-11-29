"""
修复模型缓存问题的脚本
如果遇到 "Unable to open file 'model.bin'" 错误，运行此脚本可以删除损坏的模型缓存
"""
import os
import shutil
from pathlib import Path

def find_and_remove_model_cache():
    """查找并删除 faster-whisper-tiny 模型的缓存"""
    # 常见的 Hugging Face 缓存路径
    possible_paths = [
        Path.home() / ".cache" / "huggingface" / "hub" / "models--Systran--faster-whisper-tiny",
        Path.home() / ".cache" / "huggingface" / "hub" / "models--Systran--faster-whisper-tiny".replace("--", "-"),
    ]
    
    # Windows 用户目录
    username = os.environ.get('USERNAME', '')
    if username:
        windows_path = Path(f"C:/Users/{username}/.cache/huggingface/hub/models--Systran--faster-whisper-tiny")
        possible_paths.append(windows_path)
    
    found_paths = []
    for path in possible_paths:
        if path.exists():
            found_paths.append(path)
            print(f"找到模型缓存目录: {path}")
    
    if not found_paths:
        print("未找到模型缓存目录。可能模型尚未下载，或者缓存位置不同。")
        print("\n请手动检查以下位置：")
        print(f"  {Path.home() / '.cache' / 'huggingface' / 'hub'}")
        return
    
    print(f"\n找到 {len(found_paths)} 个模型缓存目录。")
    response = input("是否删除这些目录？这将强制程序重新下载模型。 (y/n): ")
    
    if response.lower() == 'y':
        for path in found_paths:
            try:
                print(f"正在删除: {path}")
                shutil.rmtree(path)
                print(f"  ✓ 已删除")
            except Exception as e:
                print(f"  ✗ 删除失败: {e}")
        
        print("\n✓ 模型缓存已清理完成！")
        print("请重新运行您的程序，模型将自动重新下载。")
    else:
        print("操作已取消。")

if __name__ == "__main__":
    print("=" * 60)
    print("Faster-Whisper 模型缓存清理工具")
    print("=" * 60)
    print()
    find_and_remove_model_cache()

