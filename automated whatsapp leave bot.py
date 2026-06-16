#install this library before running the project

!pip install fastapi uvicorn nest-asyncio pyngrok twilio langchain langchain-openai python-dotenv gspread oauth2client python-multipart

#Run this cell to upload your clean JSON credentials file

from google.colab import files
print("Please upload your brand new JSON service account key file:")
uploaded = files.upload()

# Cell 2: Smart Auto-Repairing Credentials Engine

import json
import gspread
import re
from oauth2client.service_account import ServiceAccountCredentials
from google.colab import userdata

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

auth_success = False

try:
    # 1. Fetch raw environment text string
    raw_secret = userdata.get('GOOGLE_SHEETS_CREDS')
    if not raw_secret:
        raise ValueError("The secret 'GOOGLE_SHEETS_CREDS' is empty or missing.")

    # 2. AUTO-REPAIR: Clean text and extract only the first complete JSON object block
    # This prevents 'Extra Data' bugs if text was pasted twice or has leading/trailing garbage text
    clean_text = raw_secret.strip()

    # Use regular expressions to extract text inside the first matching set of curly braces {}
    json_match = re.search(r'(\{.*?\})', clean_text, re.DOTALL)

    if json_match:
        repaired_json_string = json_match.group(1)
    else:
        # If no internal match found, default back to full cleaned text string
        repaired_json_string = clean_text

    # 3. Parse text into Python Dictionary structure
    credentials_dict = json.loads(repaired_json_string)

    # Authenticate with Google
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
    client = gspread.authorize(creds)
    auth_success = True
    print("✅ Success: System successfully authenticated with Google Cloud APIs!")

except Exception as auth_err:
    print("\n🚨 [CRITICAL PARSE ERROR]: Authentication failed to process the secret text.")
    print(f"Details: {auth_err}")
    print("\n--- WHAT THE ENGINE SEES IN YOUR SECRET (FIRST 100 CHARACTERS) ---")
    try:
        print(userdata.get('GOOGLE_SHEETS_CREDS')[:100] + "...")
    except:
        print("Could not read secret.")
    print("------------------------------------------------------------------\n")

# Run sheet mapping only if authentication succeeds
if auth_success:
    try:
        sheet = client.open("LeaveRequests")
        all_worksheets = [ws.title for ws in sheet.worksheets()]
        print(f"[Sheet Inventory] Available tabs found in your file: {all_worksheets}")

        if "Balances" in all_worksheets:
            balance_sheet = sheet.worksheet("Balances")
            print("✅ Success: 'balance_sheet' mapped to 'Balances' tab.")
        elif "Sheet1" in all_worksheets:
            balance_sheet = sheet.worksheet("Sheet1")
            print("⚠️ Warning: 'Balances' tab not found. Using 'Sheet1'.")
        else:
            balance_sheet = sheet.get_worksheet(0)
            print(f"🚨 Critical: No matching tabs. Using first tab: '{balance_sheet.title}'")

        if "Log" in all_worksheets:
            log_sheet = sheet.worksheet("Log")
            print("✅ Success: 'log_sheet' mapped to 'Log' tab.")
        else:
            log_sheet = sheet.add_worksheet(title="Log", rows="1000", cols="5")
            log_sheet.insert_row(["Employee Name", "Leave Type", "Date", "Reason", "Status"], 1)
            print("✅ Success: Created a fresh 'Log' tab.")

        print(f"\n🚀 SYSTEM ONLINE -> Current Balance Columns: {balance_sheet.row_values(1)}")

    except Exception as sheet_err:
        print(f"🚨 Google Sheet Access Error: Could not open 'LeaveRequests'. Details: {sheet_err}")
else:
    print("❌ Sheet initialization halted because authentication failed.")

# Cell 3: Production-Grade Robust AI Agent Extractor

from datetime import date
from google.colab import userdata
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# Fetch API Key securely from Colab Secrets (🔑)
OPENROUTER_API_KEY = userdata.get('OPENROUTER_API_KEY')

# Initialize the OpenRouter model gateway
llm = ChatOpenAI(
    openai_api_key=OPENROUTER_API_KEY,
    openai_api_base="https://openrouter.ai/api/v1",
    model_name="openrouter/free",
    temperature=0.1  # Low temperature makes the output deterministic and structural
)

# Initialize the structured JSON output parser
parser = JsonOutputParser()

# Dynamically fetch today's real-world date to help resolve terms like "tomorrow"
today_date = date.today().strftime("%Y-%m-%d")

# Advanced Instruction engineering to enforce case-normalization and complete metadata extraction
prompt = ChatPromptTemplate.from_template(
    "You are an expert HR automation extraction assistant. Your task is to accurately extract leave details from text messages.\n"
    f"CRITICAL context: Today's date is {today_date}.\n\n"

    "RULES FOR EXTRACTION AND NORMALIZATION:\n"
    "1. 'employee': Extract the full name of the employee. Trim any extra spaces.\n"
    "2. 'leave_type': MUST be normalized to lower-case string. Convert variations like 'Sick', 'SICK', 'Casual Leave' to either exactly 'sick' or 'casual'.\n"
    "3. 'date': Calculate and provide the absolute date(s) requested in YYYY-MM-DD format. If relative terms like 'tomorrow' are used, calculate it relative to today's date ({today_date}). If a range is provided, output it clearly (e.g., '2026-06-05 to 2026-06-07').\n"
    "4. 'reason': Extract the brief context or reason if given. If none is mentioned, default to 'Not specified'.\n\n"

    "CRITICAL: Return ONLY a raw JSON object matching the requested schema. Do not enclose it in markdown wrappers like ```json.\n\n"

    "EXAMPLES:\n"
    "Message: 'Hi, I am Raj. I need CASUAL LEAVE on June 5th due to personal work.'\n"
    "Output: {{\n  \"employee\": \"Raj\",\n  \"leave_type\": \"casual\",\n  \"date\": \"2026-06-05\",\n  \"reason\": \"personal work\"\n}}\n\n"

    "Message: 'Hey HR, please grant Amit Sharma a sick leave starting tomorrow.'\n"
    "Output: {{\n  \"employee\": \"Amit Sharma\",\n  \"leave_type\": \"sick\",\n  \"date\": \"Relative to today's date\",\n  \"reason\": \"Not specified\"\n}}\n\n"

    "Now process this incoming payload:\n"
    "Message: {message}\n\n"
    "{format_instructions}"
)

# Inject structural output rule variables
prompt = prompt.partial(format_instructions=parser.get_format_instructions())

# Chain implementation via LangChain Expression Language (LCEL)
extraction_chain = prompt | llm | parser
print(f"Upgraded AI Extractor Online! Time Anchor set to: {today_date}")

# Cell 4: Production-Grade Robust Business Logic (Text Coordinate Search)
import json

def process_leave_with_db(message: str) -> str:
    try:
        # 1. Extract structural data via the LangChain AI Layer
        try:
            extracted_data = extraction_chain.invoke({"message": message})
        except Exception as ai_err:
            print(f"[AI Error]: Extraction failed, trying fallbacks. Details: {ai_err}")
            extracted_data = {}

        employee = extracted_data.get("employee")
        leave_type = str(extracted_data.get("leave_type", "")).lower()
        date_str = extracted_data.get("date", "Not specified")
        reason = extracted_data.get("reason", "Not specified")

        # Fallbacks if AI outputs 'None' strings
        if not leave_type or leave_type == "none":
            if "sick" in message.lower(): leave_type = "sick"
            elif "casual" in message.lower(): leave_type = "casual"

        if not employee or employee == "none":
            words = message.split()
            for i, word in enumerate(words):
                if word.lower() in ["am", "is"] and i + 1 < len(words):
                    employee = words[i+1].strip(".,! ")
                    break

        print(f"\n[AI Extracted Log] -> Name: '{employee}' | Type: '{leave_type}'")

        if not employee or not leave_type:
            return "Could not extract your name or leave type. Please reply with: 'I am [Name], need [Sick/Casual] leave'."

        # 2. DYNAMIC LOOKUP: Fetch RAW Values instead of Dictionary Records
        # This completely avoids column header dictionary key bugs!
        all_rows = balance_sheet.get_all_values()

        if not all_rows:
            return "Error: The Google Sheet appears to be completely empty."

        header_row = [str(h).strip().lower() for h in all_rows[0]]
        print(f"[Sheet Debug] Found Headers: {header_row}")

        # Normalize the name we are searching for
        search_name = str(employee).strip().lower()

        emp_row_idx = None
        official_name = None

        # Scan Column A (Index 0) row by row for a match
        for idx, row in enumerate(all_rows):
            if idx == 0: continue # Skip header row
            if not row: continue

            current_row_name = str(row[0]).strip().lower()

            # Check if extracted name matches or is a part of the sheet name
            if search_name in current_row_name or current_row_name in search_name:
                emp_row_idx = idx + 1 # gspread is 1-indexed
                official_name = row[0]
                target_row_data = row
                break

        if not emp_row_idx:
            print(f"[Lookup Failed] Could not match '{search_name}' against any rows.")
            return f"Error: Employee '{employee}' was not found in our Google Sheet database."

        print(f"[Lookup Success] Matched '{employee}' to Row {emp_row_idx} as '{official_name}'")

        # 3. Dynamic Column Index Matching
        sick_col_idx = 2   # Column B
        casual_col_idx = 3 # Column C

        if "sick" in leave_type:
            col_to_update = sick_col_idx
            leave_name = "Sick"
            current_balance = int(target_row_data[1]) if len(target_row_data) > 1 and target_row_data[1].isdigit() else 0
        elif "casual" in leave_type:
            col_to_update = casual_col_idx
            leave_name = "Casual"
            current_balance = int(target_row_data[2]) if len(target_row_data) > 2 and target_row_data[2].isdigit() else 0
        else:
            return f"Invalid leave type '{leave_type}'. We only accept 'Sick' or 'Casual' leave."

        # 4. Policy Rules Validation & Deduction execution
        if current_balance > 0:
            new_balance = current_balance - 1

            # Direct coordinate update: cell(row, column)
            balance_sheet.update_cell(emp_row_idx, col_to_update, new_balance)

            log_sheet.append_row([official_name, leave_name, date_str, reason, "Approved"])
            return f"Approved! Your {leave_name} leave request for {date_str} is logged. Balance remaining: {new_balance}."
        else:
            log_sheet.append_row([official_name, leave_name, date_str, reason, "Rejected"])
            return f"Rejected: Insufficient {leave_name} balance (Current Balance: {current_balance})."

    except Exception as e:
        print(f"[Fatal Runtime Error]: {e}")
        return f"An internal data management error occurred: {str(e)}"
    
    # Cell 5: API Server & Communication Gateway
    
import nest_asyncio
import uvicorn
from fastapi import FastAPI, Request, Response
from twilio.twiml.messaging_response import MessagingResponse
from pyngrok import ngrok

app = FastAPI()

@app.get("/")
def home():
    return {"status": "operational"}

@app.post("/whatsapp")
async def whatsapp_reply(request: Request):
    form = await request.form()
    incoming_msg = form.get("Body", "")
    print(f"Received message stream: {incoming_msg}")

    # Send message to our engine
    reply_msg = process_leave_with_db(incoming_msg)

    # Generate XML payload structured for Twilio standard response rules
    twiml = MessagingResponse()
    twiml.message(reply_msg)
    return Response(content=str(twiml), media_type="application/xml")

# Step 5A: Open public exposure tunnel via Ngrok

NGROK_AUTH_TOKEN = userdata.get('NGROK_AUTH_TOKEN')
ngrok.set_auth_token(NGROK_AUTH_TOKEN)
public_url = ngrok.connect(8000)

print("\n" + "="*60)
print(f"👉 COPY THIS URL TO YOUR TWILIO WEBHOOK BOX:")
print(f"{public_url.public_url}/whatsapp")
print("="*60 + "\n")

# Step 5B: Boot async production-grade engine

nest_asyncio.apply()
config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
server = uvicorn.Server(config)
await server.serve()