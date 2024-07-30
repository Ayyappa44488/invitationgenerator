import requests
from llama_cpp import Llama
import json
import re
import qrcode
import os
from confidential import bashini_key
def translate_text(text,value,langcode):
    if value==0 or langcode=='en':
        return text
    url = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"
    headers = {
    "Authorization":bashini_key 
    }

    data = {
        "pipelineTasks": [
            {
                "taskType": "translation",
                "config": {
                    "language": {
                        "sourceLanguage": "en",
                        "targetLanguage": "te"
                    },
                    "serviceId": "ai4bharat/indictrans-v2-all-gpu--t4"
                }
            }
        ],
        "inputData": {
            "input": [
                {
                    "source": text
                }
            ]
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        response = response.json()
        return response['pipelineResponse'][0]['output'][0]['target']
    else:
        print("Request failed with status code:", response.status_code)


def qr_generator(url,filename):
# Data to be encoded
    data = url
    
    directory = os.path.dirname(filename)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    # Create a QR Code object
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Add data to the QR Code
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image
    img.save(filename)
    return


def story_generation(description, groom, bride, date):
    
    LLM = Llama(model_path="/home/ayyappa44488/code/carddesign/llama-2-7b-chat.ggmlv3.q4_0.bin", n_ctx=2048)
    prompt = f""" 
    Generate a fictional love story in JSON format for a couple named {groom} and {bride}, 
    leading up to their wedding on {date}. 
    based on given descrption(optional): '{description}'. 
    Format:
    {{
    "firstMeet": {{ "date": "yyyy-mm-dd", "description": "how they meet" }},
    "firstDate": {{ "date": "yyyy-mm-dd", "description": "where they gone" }},
    "proposal": {{ "date": "yyyy-mm-dd", "description": "how he/she proposed" }},
    "engagement": {{ "date": "yyyy-mm-dd", "description": "where they get engaged" }}
    }}
    Important:Do NOT generate short descriptions and don't generate half sentences,generate the fully formed sentences and give only json output.
    """

    output = LLM(prompt, temperature=0.9, max_tokens=0)
    text_output = output["choices"][0]["text"]
    # 1. Try to parse directly as JSON (ideal case)

    json_match = re.search(r'(\{.*\})', text_output, re.DOTALL | re.MULTILINE)
    json_data=json_match.group(1).strip()
    if json_match:
        try:
            if json_data.count("{")!=json_data.count("}"):
                if json_data.count("{")>json_data.count("}"):
                    story_data = json.loads(json_match.group(1).strip()+"}")
                else:
                    story_data = json.loads(json_match.group(1).strip()[:-1])
            else:
                story_data = json.loads(json_match.group(1).strip())
            print(story_data)
            return [story_data["firstMeet"]["description"], story_data["firstDate"]["description"], story_data["proposal"]["description"], story_data["engagement"]["description"],story_data["firstMeet"]["date"], story_data["firstDate"]["date"], story_data["proposal"]["date"], story_data["engagement"]["date"]]
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON after regex extraction: {e}")
            print(f"LLM Output: {text_output}")
            return None
    else:
        print("No valid JSON found in the output.")
        print(f"LLM Output: {text_output}")
        return None