# main.py
# A simple FastAPI service to convert Markdown text to Notion block JSON.
# This version uses the 'md2notion' library.

import uvicorn
from fastapi import FastAPI, Request, HTTPException
from md2notion.convert import convert

# Initialize the FastAPI application
app = FastAPI(
    title="Markdown to Notion Converter",
    description="A service that receives raw Markdown text and returns a JSON object compatible with the Notion API.",
    version="2.0.0",
)

@app.post("/convert")
async def convert_markdown_to_notion(request: Request):
    """
    This endpoint receives raw Markdown text in the request body.
    It converts the Markdown into a list of Notion block objects.
    The response is a JSON object containing a 'blocks' key.
    """
    # Check if the content type is text/markdown or text/plain
    content_type = request.headers.get("content-type")
    if not content_type or ("text/markdown" not in content_type and "text/plain" not in content_type):
        raise HTTPException(
            status_code=415,
            detail="Unsupported Media Type. Please use 'text/markdown' or 'text/plain' content type."
        )

    try:
        # Read the raw request body and decode it as UTF-8 text
        markdown_text = (await request.body()).decode('utf-8')

        if not markdown_text:
            raise HTTPException(status_code=400, detail="Request body is empty. Please provide Markdown text.")

        # Use the md2notion library to perform the conversion.
        # This function returns a list of dictionary objects, each representing a Notion block.
        notion_blocks = convert(markdown_text)

        # Return the blocks in a JSON object, ready for the n8n Notion node
        return {"blocks": notion_blocks}

    except Exception as e:
        # Catch any potential errors during conversion and return a meaningful error message
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during Markdown conversion: {str(e)}"
        )

# This part allows you to run the server directly for testing
if __name__ == "__main__":
    # To run: uvicorn main:app --host 0.0.0.0 --port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
