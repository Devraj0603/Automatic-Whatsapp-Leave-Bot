from fastapi import FastAPI, Request, Response
from twilio.twiml.messaging_response import MessagingResponse
from llm_extractor import extract_leave
from leave_logic import approve_leave
from sheets import save_leave

app = FastAPI()


@app.get("/")
def home():
    return {"status": "working"}


@app.post("/whatsapp")
async def whatsapp_reply(request: Request):

    form = await request.form()
    incoming_msg = form.get("Body")

    try:
        # Extract leave details using Gemini
        data = extract_leave(incoming_msg)

        employee = data["employee"]
        leave_type = data["leave_type"]
        days = int(data["days"])
        reason = data["reason"]

        # Check leave approval
        approved, remaining = approve_leave(
            employee,
            leave_type,
            days
        )

        status = "Approved" if approved else "Rejected"

        # Save to Google Sheets
        save_leave(
            employee,
            leave_type,
            days,
            reason,
            status
        )

        if approved:
            reply = (
                f"Leave Approved\n"
                f"Employee: {employee}\n"
                f"Type: {leave_type}\n"
                f"Days: {days}\n"
                f"Remaining Balance: {remaining}"
            )
        else:
            reply = (
                f"Leave Rejected\n"
                f"Insufficient {leave_type} leave balance."
            )

    except Exception as e:
        reply = f"Error processing leave request: {str(e)}"

    twiml = MessagingResponse()
    twiml.message(reply)

    return Response(
        content=str(twiml),
        media_type="application/xml"
    )
