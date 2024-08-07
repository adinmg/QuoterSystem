from utils.quotation_format import PDF
import tempfile

def output_to_pdf(args):
    '''Creates a PDF and returns the path of the temporary file'''
    pdf = PDF()
    pdf.add_page()
    pdf.client_details(args[0])
    pdf.table(args[2])
    pdf.note()
    pdf.signature(args[1])

    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    pdf.output(temp_file.name)
    temp_file.close()

    return temp_file.name
