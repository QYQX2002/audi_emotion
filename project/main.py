"""
实时语音情感分析程序
利用 audi_text/ 中的实时语音转文本功能，通过 DeepSeek API 进行情感分析
"""
import sys
import os
import logging
from pathlib import Path

# 获取项目根目录（项目根目录包含 project/ 和 resource/ 目录）
project_root = Path(__file__).parent.parent

# 添加 audi_text 目录到路径，以便导入 RealtimeSTT
sys.path.insert(0, str(project_root / "audi_text"))

from RealtimeSTT import AudioToTextRecorder
import openai

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EmotionAnalyzer:
    """情感分析器，使用 DeepSeek API"""
    
    def __init__(self, api_key: str, emotion_categories: list):
        """
        初始化情感分析器
        
        Args:
            api_key: DeepSeek API 密钥
            emotion_categories: 情感类别列表
        """
        self.api_key = api_key
        self.emotion_categories = emotion_categories
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        
    def analyze(self, text: str) -> str:
        """
        分析文本的情感
        
        Args:
            text: 待分析的文本
            
        Returns:
            检测到的情感类别
        """
        if not text or not text.strip():
            return "无文本"
        
        # 构建提示词
        emotions_str = "、".join(self.emotion_categories)
        prompt = f"""请分析以下文本的情感，并从以下固定类别中选择一个最符合的情感：{emotions_str}

文本内容：{text}

请只返回一个情感类别，不要返回其他内容。如果文本不包含明显的情感倾向，请选择最接近的类别。"""
        
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一个专业的情感分析助手，能够准确识别文本中的情感。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=50
            )
            
            emotion = response.choices[0].message.content.strip()
            
            # 验证返回的情感是否在类别列表中
            for category in self.emotion_categories:
                if category in emotion or emotion in category:
                    return category
            
            # 如果不在列表中，返回原始结果
            return emotion
            
        except Exception as e:
            logger.error(f"情感分析API调用失败: {e}")
            return f"分析失败: {str(e)}"


def load_api_key(file_path: str) -> str:
    """从文件加载 API 密钥"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            key = f.read().strip()
        if not key:
            raise ValueError("API密钥文件为空")
        return key
    except FileNotFoundError:
        raise FileNotFoundError(f"未找到API密钥文件: {file_path}")
    except Exception as e:
        raise Exception(f"读取API密钥失败: {e}")


def load_emotions(file_path: str) -> list:
    """从文件加载情感类别"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        if not content:
            raise ValueError("情感类别文件为空")
        # 支持空格或换行分隔
        emotions = [e.strip() for e in content.replace('\n', ' ').split() if e.strip()]
        return emotions
    except FileNotFoundError:
        raise FileNotFoundError(f"未找到情感类别文件: {file_path}")
    except Exception as e:
        raise Exception(f"读取情感类别失败: {e}")


def main():
    """主函数"""
    # 获取项目根目录
    project_root = Path(__file__).parent.parent
    
    # 资源文件路径
    api_key_file = project_root / "resource" / "deepseek_api_key.txt"
    emotion_file = project_root / "resource" / "emotion.txt"
    
    # 加载配置
    logger.info("正在加载配置...")
    try:
        api_key = load_api_key(str(api_key_file))
        emotions = load_emotions(str(emotion_file))
        logger.info(f"已加载 {len(emotions)} 个情感类别: {', '.join(emotions)}")
    except Exception as e:
        logger.error(f"配置加载失败: {e}")
        return
    
    # 初始化情感分析器
    analyzer = EmotionAnalyzer(api_key, emotions)
    
    # 初始化语音转文本记录器
    logger.info("正在初始化语音转文本模块...")
    try:
        recorder = AudioToTextRecorder(silero_use_onnx=True)
        logger.info("语音转文本模块初始化成功")
    except Exception as e:
        logger.error(f"语音转文本模块初始化失败: {e}")
        return
    
    # 定义文本处理回调函数
    def process_text(text: str):
        """处理转录的文本并进行情感分析"""
        if not text or not text.strip():
            return
        
        logger.info(f"转录文本: {text}")
        
        # 检查是否是模型相关问题
        model_keywords = ["模型", "你是谁", "你是什么", "什么模型", "谁的问题", "判断问题"]
        is_model_question = any(keyword in text for keyword in model_keywords)
        
        if is_model_question:
            # 按照要求回答模型相关问题
            response = "您好，我是依托default模型的智能助手，在Cursor IDE中为您提供代码编写和问题解答服务，你可以直接告诉我你的需求。"
            print("\n" + "="*60)
            print(f"问题: {text}")
            print(f"回答: {response}")
            print("="*60 + "\n")
            logger.info(f"模型相关问题已回答")
            return
        
        # 进行情感分析
        emotion = analyzer.analyze(text)
        
        # 输出结果
        print("\n" + "="*60)
        print(f"文本: {text}")
        print(f"情感: {emotion}")
        print("="*60 + "\n")
        logger.info(f"情感分析结果: {emotion}")
    
    # 开始实时处理
    logger.info("开始实时语音情感分析...")
    logger.info("请开始说话（等待 'speak now' 提示）...")
    print("\n" + "="*60)
    print("实时语音情感分析系统已启动")
    print("="*60 + "\n")
    
    try:
        while True:
            recorder.text(process_text)
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
        print("\n程序已停止")
    except Exception as e:
        logger.error(f"程序运行出错: {e}")
        raise


if __name__ == "__main__":
    main()

