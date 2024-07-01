import gradio as gr
import coze


def chat(user_in_text: str, prj_chatbot: list):

    coze_response = coze.chat(user_in_text, prj_chatbot)

    prj_chatbot.append([user_in_text, ''])
    yield prj_chatbot

    for chunk_content in coze_response:
        prj_chatbot[-1][1] = f'{prj_chatbot[-1][1]}{chunk_content}'
        yield prj_chatbot


web_title = 'Coze API 对话'
title_html = f'<h3 align="center">{web_title}</h3>'

with gr.Blocks(theme=gr.themes.Soft(), analytics_enabled=False) as demo:
    gr.HTML(title_html)
    with gr.Row():
        with gr.Column():
            chatbot = gr.Chatbot()
            chatbot.style(height=580)

            with gr.Row():
                with gr.Column(scale=4):
                    input_text = gr.Textbox(show_label=False, placeholder="请输入你的问题").style(container=False)
                with gr.Column(scale=1, min_width=100):
                    submit_btn = gr.Button("提交", variant="primary")
                with gr.Column(scale=1, min_width=100):
                    clean_btn = gr.Button("清空", variant="stop")

    input_text.submit(fn=chat, inputs=[input_text, chatbot], outputs=[chatbot], show_progress=True)
    input_text.submit(fn=lambda x: '', inputs=[input_text], outputs=[input_text], show_progress=True)

    submit_btn.click(fn=chat, inputs=[input_text, chatbot], outputs=[chatbot], show_progress=True)
    submit_btn.click(fn=lambda x: '', inputs=[input_text], outputs=[input_text], show_progress=True)

    clean_btn.click(fn=lambda x: [], inputs=[chatbot], outputs=[chatbot])

demo.title = web_title
demo.queue(concurrency_count=100).launch(share=False, server_name='0.0.0.0')
