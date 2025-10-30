from fpdf import FPDF

def save_report_as_pdf(text,analysis,feedback,score , filename = 'report.pdf'):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200,10,txt="AI Interview Feedback report",ln = True,align='C')
    pdf.ln(10)

    pdf.multi_cell(0,10,txt=f"📝 Transcription:\n{text}\n", align="L")
    pdf.multi_cell(0,10,txt=f"🧠 Sentiment: {analysis['sentiment']['tone']} ({analysis['sentiment']['score']:.2f})", align="L")
    pdf.multi_cell(0,10,txt=f"💬 Filler Words: {analysis['filler_words']}", align="L")
    pdf.multi_cell(0,10,txt=f"✅ Keywords Found: {analysis['keywords_found']}", align="L")
    pdf.multi_cell(0,10,txt=f"\n💡 Feedback:\n{feedback}", align="L")
    pdf.multi_cell(0,10,txt=f"\n🎯 Score: {score}/100", align="L")
    
    pdf.output(filename)
    return filename