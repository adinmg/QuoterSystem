import os
import pandas as pd
from dotenv import load_dotenv
from utils.get_pdf import output_to_pdf
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import (
    PromptTemplate,
)

load_dotenv()

# EXCEL_FILE_PATH = os.getenv("EXCEL_FILE_PATH")
QUOTATION_TABLE_MODEL = os.getenv("QUOTATION_TABLE_MODEL")

# Initialize the ChatOpenAI model with the specified model and temperature
chat_model = ChatOpenAI(
    model=QUOTATION_TABLE_MODEL, # type: ignore
    temperature=0
)

# Define the response schemas for parsing the output
response_schemas = [
    ResponseSchema(name="client", description="Extract the company name or client's name or the person to whom the quotation will be sent, if not mentioned you should put ''.", type="string"),
    ResponseSchema(name="quantities", description="Extract the quantities of each product", type="List[integer]"),
    ResponseSchema(name="products", description="Extract the name of each product or promotional item", type="List[string]"),
    ResponseSchema(name="agent", description="Extract the name of the sales agent or seller", type="string"),
]

# Create a structured output parser from the response schemas
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

# Get the format instructions for the output parser
format_instructions = output_parser.get_format_instructions()

# Define the prompt template with the format instructions and input text
prompt = PromptTemplate(
    template="You are an expert in extraction algorithms. Make sure to include the company, quantities, and the name or description of each product.\n{format_instructions}\n{text}",
    input_variables=["text"],
    partial_variables={"format_instructions": format_instructions},
)

# Define the function to create a DataFrame with products and add additional columns
def output_to_dataframe(input, vector_store):
    client = input.get("client")
    quantities = input.get("quantities")
    products = input.get("products")
    agent = input.get("agent")
    
    data = {
        "Product": products,
        "Quantity": [int(quantity) for quantity in quantities],
        "Similar_Product": [],
        "Retail_Price": [],
        "Wholesale_Price": []
    }
    
    # Perform similarity search for each product and extract additional data
    for product in products:
        result = vector_store.similarity_search(query=product)[0]  
        metadata = result.metadata
        data['Similar_Product'].append(result.page_content)
        data['Retail_Price'].append( int( metadata.get("Unit Price (USD)") )) # type: ignore
        data['Wholesale_Price'].append( int( metadata.get("Wholesale Price (USD)") )) # type: ignore

    df = pd.DataFrame(data)
    return (client, agent, df)

# Define the function that takes a vector database to retrieve product names and prices
def get_parsing_chain(vector_store):
    # Create a RunnableLambda to transform the output to a DataFrame
    dataframe_lambda = RunnableLambda(lambda x: output_to_dataframe(x, vector_store))

    # Create a RunnableLambda to transform the dataframe products to a PDF file
    pdf_lambda = RunnableLambda(lambda x: output_to_pdf(x))

    # Create the parsing chain combining prompt, chat model, output parser, dataframe lambda, and pdf lambda
    parsing_chain = prompt | chat_model | output_parser | dataframe_lambda | pdf_lambda
    return parsing_chain
