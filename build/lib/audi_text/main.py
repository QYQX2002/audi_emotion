from RealtimeSTT import AudioToTextRecorder
import logging

def process_text(text):
    print(text)

if __name__ == '__main__':
    # Enable INFO level logging to see initialization progress
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    print("Wait until it says 'speak now'")
    try:
        recorder = AudioToTextRecorder(silero_use_onnx=True)
    except RuntimeError as e:
        print(f"Error initializing recorder: {e}")
        raise

    while True:
        recorder.text(process_text)