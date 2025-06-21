"""
受信したバイナリデータを音声ファイルで保存
"""
def download_wav(data):
    get_logger().info('download_wav')
    response = {
        "status": True,
        "message": ''
    }
    try:
        # 受信する音声データを格納
        audio_data = bytearray()
        audio_data.extend(data)
        file_path = "data/uploads/received_audio.wav"
        audio = AudioSegment.from_file(io.BytesIO(audio_data), format="webm")
        audio.export(file_path, format="wav")
    except Exception as e:
        response['status'] = False
        response['message'] = e
        get_logger().error(e)
    finally:
        return response


"""
Google Speech Recognition で文字起こし
"""
async def convert_speech_2_text(websocket: WebSocket):
    response = {
        "status": True,
        "message": '',
        "language": ''
    }
    file_path = "data/uploads/received_audio.wav"
    try:
        get_logger().info('音声の解析を開始します')
        start = time.time()
        # 音声ファイルを読み込む
        with open(file_path, 'rb') as f:
            audio_data = f.read()
        # サーバーにPOSTリクエストを送信
        resp = requests.post(
            f"{ngrok_url}/transcribe",
            data=audio_data,
            headers={'Content-Type': 'application/octet-stream'}
        )        
        # レスポンスをJSONとして解析
        result = resp.json()
        end = time.time()
        get_logger().debug(f"音声ファイル分析処理時間: {end - start}秒")
        get_logger().info('解析を終了しました')
        get_logger().info(result)

        response['message'] = result['text']
        response['language'] = result['language']

        message = Message(
            message=response['message'],
            language=response['language'],
            type=0, # トーク
            status=0, # proceed
            user=User(
                type=1,
                name='Shinjo'
            )
        )
        message_json = message.dict()
        message_json['user'] = message.user.dict()
        get_logger().info(message_json)
        await websocket.send_json(message_json)
    except Exception as e:
        get_logger().error(e)
        response['status'] = False
    return response
