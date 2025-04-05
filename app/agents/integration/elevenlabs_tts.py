import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

# .env 読み込み
loaded = load_dotenv()
print("Loaded .env:", loaded)

api_key = os.getenv("ELEVENLABS_API_KEY")
voice_id = os.getenv("ELEVENLABS_VOICE_ID")
output_file="data/outputs/output.mp3" # 実行ファイルのディレクトリ上の"output_file"のファイル名で作成される
client = ElevenLabs(api_key=api_key)


class ElevenLabs():
    def execute(self, user_prompts: str) -> None:
        audio_stream = client.text_to_speech.convert(
            text=user_prompts,
            voice_id=voice_id,
            model_id="eleven_multilingual_v2",
            voice_settings={
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        )

        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "wb") as f:
            for chunk in audio_stream:
                f.write(chunk)
        print(f"音声ファイルを生成しました: {output_file}")
