from helper import validate_image,encode_image_to_base64,clean_json_output
import openai
import os
from dotenv import load_dotenv
load_dotenv()

def extract_seal_stamp_data__from_image(image_path: str):
    print("Function Invoking")
    try:
        if not validate_image(image_path):
            return {
                "status": False,
                "statusCode": 400,
                "message": "I don't see a valid image. Please upload a supported image file (JPG, PNG, GIF, BMP, WEBP, or TIFF).",
                "data": [{}]
            }

        client = openai.OpenAI(
            base_url=os.getenv("GPT_URL"),
            api_key=os.getenv("AZURE_OPENAI_KEY"),
        )

        prompt = """
        You are a helpful assistant analyzing an image for Thirumurugan Subramaniyan. 

        Your task is to extract seal/stamp details from the document image.  
        Return the following fields exactly:

        - OWNER SIGNATURE
        - STRUCTURAL ENGINEER
        - REGISTERED ENGINEER

        ### Matching Rules:
        1. OWNER SIGNATURE → look for labels like:
           - OWNER SIGNATURE
           - SIGNATURE OF OWNER
           - OWNER's SIGNATURE
        2. STRUCTURAL ENGINEER → look for labels like:
           - STRUCTURAL ENGINEER
           - SIGNATURE OF STRUCTURAL ENGINEER
           - STRUCTURAL ENGINEER'S SIGNATURE
        3. REGISTERED ENGINEER → look for labels like:
           - REGISTERED ENGINEER
           - ARCHITECT SIGNATURE
           - SIGNATURE OF ARCHITECT
           - LICENSED SURVEYOR
           - ARCHITECT/LICENSED SURVEYOR SIGNATURE

        ### Output Rules:
        1. Return only the exact matched text as it appears in the document (no modifications).
        2. If a field is not found, return an empty string "" for that field.
        3. Output must be valid JSON only (no extra text, no explanation, no markdown).

        ### Example Output:
        {
          "OWNER SIGNATURE": "For HEADWAY PREMIER INDUSPARK PRIVATE LIMITED",
          "STRUCTURAL ENGINEER": "A.N. RAVICHANDRAN",
          "REGISTERED ENGINEER": "A.N. RAVICHANDRAN"
        }

        Now extract and return the results in the same JSON format.
        """

        base64_image = encode_image_to_base64(image_path)
        if base64_image:
            response = client.chat.completions.create(
                model=os.getenv("MODEL"),
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that analyzes images and responds in strict JSON format."
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                },
                            },
                        ],
                    },
                ],
                max_tokens=500,
            )
            raw_result = response.choices[0].message.content
            result = clean_json_output(raw_result)
            return {
                "status": True,
                "statusCode": 200,
                "message": "Successfully analyzed the image",
                "OWNER SIGNATURE": result["OWNER SIGNATURE"],
                "STRUCTURAL ENGINEER": result["STRUCTURAL ENGINEER"],
                "REGISTERED ENGINEER": result["REGISTERED ENGINEER"]
            }
        else:
            return {
                "status": False,
                "statusCode": 400,
                "message": "Failed to convert the image into base64 format",
                "data": [{}]
            }
    except Exception as e:
        print("Error in the analyze_image function : ", str(e))
        return {
            "status": False,
            "statusCode": 400,
            "message": str(e),
            "data": [{}]
        }
