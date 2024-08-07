import pandas as pd
from fpdf import FPDF
from datetime import datetime

class PDF(FPDF):
    def header(self):
        # Set the font to Arial, bold, size 14
        self.set_font('Arial', 'B', 14)
        # Create a cell with the title 'Quotation', center aligned
        self.cell(0, 40, 'Quotation', 0, 1, 'C')
        self.ln(1)

    def client_details(self, client):
        # Set the font to Arial, regular, size 12
        self.set_font('Arial', '', 12)
        # Create a cell with 'Attention:' text
        self.cell(0, 1, 'Attention:', 0, 1)
        # Create a cell with the client name
        self.cell(0, 10, client, 0, 1)
        # Create a cell with the current date, right aligned
        self.cell(0, 10, datetime.now().strftime("%d-%m-%Y"), 0, 1, 'R')
        self.ln(2)

    def table(self, df):
        # Set the font to Arial, bold, size 10
        self.set_font('Arial', 'B', 10)
        # Create table headers
        self.cell(20, 10, 'Quantity', 1, 0, 'C')
        self.cell(70, 10, 'Product', 1, 0, 'C')
        self.cell(45, 10, 'Retail Price (USD)', 1, 0, 'C')
        self.cell(45, 10, 'Wholesale Price (USD)', 1, 0, 'C')
        self.ln()
        
        # Set the font to Arial, regular, size 10
        self.set_font('Arial', '', 10)
        subtotal_retail = 0
        subtotal_wholesale = 0
        
        # Iterate over DataFrame rows to create table rows
        for i in range(len(df)):
            self.cell(20, 8, str(df.iloc[i]['Quantity']), 1)
            self.cell(70, 8, df.iloc[i]['Similar_Product'], 1)
            self.cell(45, 8, str(df.iloc[i]['Retail_Price']), 1, 0, 'R')
            self.cell(45, 8, str(df.iloc[i]['Wholesale_Price']), 1, 0, 'R')
            self.ln()

            # Calculate subtotals
            subtotal_retail += df.iloc[i]['Quantity'] * df.iloc[i]['Retail_Price']
            subtotal_wholesale += df.iloc[i]['Quantity'] * df.iloc[i]['Wholesale_Price']
        
        # Add a subtotal row
        self.set_font('Arial', 'B', 10)
        self.cell(20, 10, '', 1)
        self.cell(70, 10, 'Subtotal', 1, 0, 'R')
        self.cell(45, 10, f'{subtotal_retail}', 1, 0, 'R')
        self.cell(45, 10, f'{subtotal_wholesale}', 1, 0, 'R')
        self.ln(20)

    def note(self):
        # Set the font to Arial, italic, size 12
        self.set_font('Arial', 'I', 12)
        # Add a note section
        self.cell(0, 10, 'NOTE:', 0, 1)
        bullet = "\x95"
        self.cell(0, 10, f'{bullet} These prices do not include VAT.', 0, 1)
        self.cell(0, 10, f'{bullet} For order processing, a 50% deposit is required, and 50% upon delivery.', 0, 1)
        self.ln(20)

    def signature(self, seller_name):
        # Set the font to Arial, bold, size 12
        self.set_font('Arial', 'B', 12)
        # Add signature text
        self.cell(0, 10, 'Sincerely at your service', 0, 1, 'C')
        self.cell(0, 10, 'S I N C E R E L Y', 0, 1, 'C')
        self.cell(0, 10, seller_name, 0, 1, 'C')

if __name__ == "__main__":
    # Data for the DataFrame
    data = {
        'Client': ['Client', 'Client', 'Client'],
        'Product': ['short sleeve shirts', 'long sleeve shirt', 'canvas bag'],
        'Quantity': [5, 10, 10],
        'Similar_Product': ['Basic short-sleeve shirt', 'Basic long-sleeve shirt', 'Canvas bag'],
        'Retail_Price': [8.82, 12.94, 14.71],  # Converted to USD
        'Wholesale_Price': [7.06, 10.59, 11.76]  # Converted to USD
    }

    df = pd.DataFrame(data)

    # Create the PDF
    CLIENT = df['Client'][0]
    pdf = PDF()
    pdf.add_page()
    pdf.client_details(CLIENT)
    pdf.table(df)
    pdf.note()
    pdf.signature('Sales Agent')

    # Save the PDF
    pdf.output(f"Quotation_for_{CLIENT}.pdf")
