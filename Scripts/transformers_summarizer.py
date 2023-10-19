import pandas as pd
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load the pre-trained model and tokenizer
model_name = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Function to summarize text
def summarize_text(text):
    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=20, min_length=10, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def llm_summarize(df):
    # Apply the summarize_text function to the 'text_column' and create a new 'summary' column
    df['summary'] = df['STEPS'].apply(summarize_text)

    df.to_csv("llm_summary.csv",index=False)
    # Print the DataFrame with the summaries
    return df
