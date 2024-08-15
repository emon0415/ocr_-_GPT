import streamlit as st
from PIL import Image
import pyocr
import platform

pyocr.tesseract.TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
set_language_list = {
    '日本語': 'jpn',
    '英語': 'eng',
}

st.title('文字認識 & 言葉変換アプリ')
set_language = st.selectbox('文字認識する言語を選んでください。',set_language_list.keys())
file_upload = st.file_uploader('ここに文字認識したファイルをアップロードしてください。', type=['png', 'jpg'])

txt = None

if (file_upload !=None):
    st.image(file_upload)
    engines = pyocr.get_available_tools()
    engine = engines[0]

    txt = engine.image_to_string(Image.open(file_upload), lang =set_language_list[set_language])
    st.write(txt)

st.write("以下にエラーが出ますが、画像をアップロードすれば消えます")

from openai import OpenAI

if txt:
    import os
    os.environ['OPENAI_API_KEY'] = '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'

    client = OpenAI()

    content_kind_of = [
        "中二病語に変換して欲しい",
        "赤ちゃん語に変換して欲しい",
        "ギャル語に変換して欲しい",
        "カタコト外人の言葉に変換して欲しい",
        "丁寧すぎて逆に失礼な敬語に変換して欲しい",
    ]

    content_kind_of_to_gpt = st.selectbox('変換したい言葉を選んでください', options=content_kind_of)
    content_maxStr_to_gpt = st.sidebar.slider('出力の最大文字数', 100, 1000, 3000)

    def run_gpt(content_text_to_gpt, content_kind_of_to_gpt, content_maxStr_to_gpt):
        request_to_gpt = (
            content_text_to_gpt 
            + '内容は' 
            + str(content_maxStr_to_gpt) 
            + '文字以内で出力してください。' 
            + content_kind_of_to_gpt 
        )

        response = client.chat.completions.create(
          model = 'gpt-4o-mini',
          messages=[
                {'role': 'user', 'content': request_to_gpt},
            ],
         )

        output_content = response.choices[0].message.content.strip()
        return output_content
    
output_content_text = run_gpt(txt, content_kind_of_to_gpt, content_maxStr_to_gpt)
st.write(output_content_text)
