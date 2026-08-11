from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import streamlit as st
from io import BytesIO

def chat_session_exporter():
    buffer =  BytesIO()
    filename = 'chat_session.pdf'
    documenttitle = 'VectorDocs chat session'

    pdf = canvas.Canvas(buffer)
    pdf.setTitle(documenttitle)
    width,height = A4
    x,y = 40,height-40

    line_height = 15
    for chat,ses in st.session_state.chat_sessions.items():
        pdf.setFont("Helvetica-Bold",12)
        pdf.drawString(x,y,f"Chat session {chat}")
        y-=line_height
        for msg in ses['messages']:
            pdf.setFont("Helvetica",12)

            cont = f"{msg['role']}: {msg['content']}"
            cur = 0
            while cur<len(cont):
                pdf.drawString(x,y,cont[cur:cur+80])
                cur+=80 
                y-=line_height
            if y<40:
                pdf.showPage()
                pdf.setFont("Helvetica",12)
                x,y = 40,height-40
        y-=20
                
                 
    pdf.save()
    buffer.seek(0)
    st.download_button(
        label="Export session📤",
        data=buffer,
        file_name=filename,
        mime="application/pdf"
    )