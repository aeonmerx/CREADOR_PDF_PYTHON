import streamlit as st
from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        if hasattr(self, 'document_title'):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, self.document_title, 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title, font='Arial', size=12):
        self.set_font(font, 'B', size)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)

    def chapter_body(self, body, font='Arial', size=12):
        self.set_font(font, '', size)
        self.multi_cell(0, 10, body)
        self.ln()

    def create_pdf(self, filename, document_title, author, chapters, image_path=None):
        self.document_title = document_title
        self.add_page()
        if author:
            self.set_author(author)

        if image_path:
            self.image(image_path, x=10, y=25, w=self.w - 20)
            self.ln(120)

        for chapter in chapters:
            title, body, font, size = chapter
            self.chapter_title(title, font, size)
            self.chapter_body(body, font, size)

        self.output(filename)

def main():
    st.title('Generador de PDF con Python')
    st.write('Esta aplicación genera un PDF a partir de los datos proporcionados.')

    document_title = st.text_input('Título del documento')
    author = st.text_input('Autor')
    chapters = []

    for i in range(1, 4):
        chapter_title = st.text_input(f'Título del capítulo {i}')
        chapter_body = st.text_area(f'Cuerpo del capítulo {i}')
        chapters.append((chapter_title, chapter_body, 'Arial', 12))

    image_file = st.file_uploader("Sube una imagen", type=["jpg", "png", "jpeg"])
    image_path = None
    if image_file:
        image_path = os.path.join("temp", image_file.name)
        with open(image_path, "wb") as f:
            f.write(image_file.getbuffer())

    if st.button('Generar PDF'):
        pdf = PDF()
        pdf.create_pdf('output.pdf', document_title, author, chapters, image_path)
        st.success('PDF generado con éxito')
        with open('output.pdf', 'rb') as f:
            st.download_button('Descargar PDF', f, file_name='output.pdf')

if __name__ == "__main__":
    os.makedirs("temp", exist_ok=True)
    main()
