from django.shortcuts import render

# Create your views here.
import os
import json
import re
from dotenv import load_dotenv
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")
# mongodb://localhost:27017/
# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["details"]
collection = db["details_connection"]
examples = """
Examples:
Q: What are the textbooks for 3rd semester CSE?
A: { "type": "textbook", "data.department": "csd", "data.semister":4}

Q: Show notes for Operating Systems.
A: { "type": "notebook", "data.subject": "Operating Systems" }

Q: List all CSD faculty.
A: { "type": "faculty", "data.department": "CSD" }

Q: How many students were placed in 2023?
A: { "type": "placement", "data.year": "2023" }

Q: what are the courses available?
A: {"type" : "courses_available"}

Q: Physics notebook
A: {"type":"notebook", "data.subject" : "Physics"}

Q: csd timetable of 3rd sem
A: {"type": "timetable", "data.semester": 6, "data.department":"CSD" }

Use these examples as guidance.
"""


def chat_view(request):
    return render(request, 'chatbot/chat.html')

@csrf_exempt
def get_response(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '').strip()

        if not user_message:
            return JsonResponse({'error': 'No message received'})

        try:
            # Step 1: Check if message is related to college
            if any(keyword in user_message.lower() for keyword in [
                'notebook',
                'college', 'ace college', 'engineering', 'acecollege', 'timetable','timetables',
                'notes', 'books', 'faculty', 'placements', 'infrastructure','events','event','textbook','ace engineering college','contact',
                'text book','course structure', 'courses', 'cousre','textbooks'
            ]):
                # Ask Gemini to generate MongoDB query
                prompt_for_query = f"""
You are a MongoDB expert helping generate queries for a college information chatbot.

Each document has a 'type' and a 'data' field.
Valid types are: textbook, notebook, faculty, placement, timetable, event, address.
"type": "notebook",  
      data.subject: "Java",
if any link provide give it to user
csd stands for DataScience not Computer Science and Design.

{examples}

Short forms with full form of Departments : CSD(cse datascience), CSM(cse machine learning), IOT(Internet of Things),CSE(computer science and Engineering), Al(Artificial Intellegent)
and dont mention this in response "Okay, here's a quick summary of the ACE Engineering College data you provided:"
Now generate a MongoDB query for this user question: '{user_message}'.
Return only the JSON query object.
"""

                query_response = model.generate_content(prompt_for_query)
                print(f"this is query:\n{query_response}")
                # Clean and extract JSON using regex
                raw_text = query_response.text.strip()
                json_match = re.search(r'{.*}', raw_text, re.DOTALL)

                if not json_match:
                    return JsonResponse({'response': "Sorry, I couldn't parse the generated query from Gemini."})

                try:
                    query_dict = json.loads(json_match.group())
                except Exception as e:
                    return JsonResponse({'response': f"Couldn't parse generated query. Error: {str(e)}"})

                # Step 2: Search MongoDB
                # Case-insensitive match for subject (if it exists in the query)

                result = list(collection.find(query_dict, {"_id": 0}))


                if result:
                    # Step 3: Summarize using Gemini
                    prompt_for_summary = (
                        f"The following is data from a MongoDB database about ACE Engineering College.\n"
                        f"Please summarize this information in a friendly, clear, and easy-to-understand way.\n"
                        f"Use natural language suitable for students or visitors.\n"
                        f"Department full forms:\n"
                        f" - CSD = CSE (Data Science)\n"
                        f" - CSM = CSE (Machine Learning)\n"
                        f" - CSE = Computer Science and Engineering\n\n"
                        f"If the data about timetable\n"
                        f"timetable semister: ...\n"
                        f"link....\nn"
                        f"If the data is about faculty, format the response like this:\n"
                        f"Name\n"
                        f" - Designation: ...\n"
                        f" - Department: ...\n"
                        f" - Professional Experience: ...\n"
                        f" - Research Interests: ...\n"
                        f"(List each faculty member in this format.)\n\n"
                        f"If the data is about textbooks, respond like this:\n"
                        f"'This book is available on the college website. You can find it here: [link]'\n\n"
                        f"If the data is about events, provide a short and neat summary mentioning:\n"
                        f" - Event type (e.g., Seminar, Hackathon, TechFest, Cultural Day)\n"
                        f" - Event dates (group similar events)\n"
                        f" - Use natural phrasing like: 'The college will host several seminars including on August 2nd, December 6th...'\n"
                        f" - End with: 'For more details, visit the official ACE Engineering College events page.'\n\n"
                        f"Data:\n{json.dumps(result, indent=2)}"
                    )

                    summary_response = model.generate_content(prompt_for_summary)
                    human_response = summary_response.text.strip()
                    return JsonResponse({'response': human_response})
                else:
                    # Step 4: No DB match, fallback to Gemini
                    fallback_response = model.generate_content(
                        f"The user asked: '{user_message}', but no matching data was found in the database. Respond appropriately."
                    )
                    return JsonResponse({'response': fallback_response.text.strip()})
            else:
                # Not college-related: answer using Gemini directly
                general_response = model.generate_content(user_message)
                return JsonResponse({'response': general_response.text.strip()})

        except Exception as e:
            return JsonResponse({'error': f'Processing error: {str(e)}'})

    return JsonResponse({'error': 'Invalid request method'})
