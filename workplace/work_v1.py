from pydantic import BaseModel, Field
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
import json
from typing import Union


#model=OpenAIModel('gpt-4o')
model= GroqModel('llama-3.1-8b-instant')


ticket = {
"ticket_id": "SUP-005",
"customer_tier": "enterprise",
"subject": "Urgent: Security vulnerability?",
"message": "Our security team flagged that your API responses include internal server paths in danger",
"previous_tickets": 20,
"monthly_revenue": 50000,
"account_age_days": 900
}

# Agent1:  Tickets Analyzer
class TicketAnalysis(BaseModel):
    summarized_issue: str= Field()
    sentiment: str= Field()
    urgency_level: str= Field()
    monthly_revenue: int
    account_age_days: int
    previous_tickets: int
    ticket_id: Union[str, int] 
    customer_tier: str


analyzer_agent= Agent(
    model=model,
    output_type=TicketAnalysis,
    system_prompt=(
        "You are a support ticket analyzer.\n"
        "Given a ticket with subject, message, revenue, and account age, perform the following:\n"
        "- Using subject and message, summarize the core issue in one short sentence explaining the issue to support.\n"
        "- Using subject and message, analyze the customer's tone to determine the sentiment (positive,or neutral, or negative).\n"
        "- Based on tone, content, and customer tier, monthly_revenue, account_age_days, assess urgency as Critical/P1, High/P2, Medium/P3, Low/P4. Determine urgency level. Even if sentiment is negative, consider customer tier and value. \n"
        "Return ONLY a JSON with: summarized_issue,sentiment,urgency_level"
    )
)

analyzer_result= analyzer_agent.run_sync(str(ticket))
intermediate_output= analyzer_result.output.model_dump()
# print("\n[Agent 1 op]")
# print(json.dumps(intermediate_output, indent=2))


# Agant 2: Issue Classifier
class IssueTypeOutput(BaseModel):
    issue_type: str= Field()
    confidence_score: float= Field()

issue_classifier_agent = Agent(
    model=model,
    output_type=IssueTypeOutput,
    system_prompt=(
        "You are an issue classification expert for customer support.\n"
        "Classify the issue based on the subject and message provided.\n"
        "Only use these categories: bug, feature_request,billing, security, login_issue, ui_feedback, documentation, general_query.\n"
        "Return a JSON with exactly two fields: issue_type (string), confidence_score (float between 0 and 1).\n"
        "Do not explain or add any other text. Output only a JSON object."
    )

)
classification_input= {
    "subject": ticket["subject"],
    "message": ticket["message"]
}

issue_classifier_result= issue_classifier_agent.run_sync(json.dumps(classification_input)) ## issue ho sakta hai

classified_issue = issue_classifier_result.output  
# print("\n[Agent 2 op]")
# print(json.dumps(classified_issue.model_dump(),indent=2))

def combine_ticket_results(ticket1, intermediate_output, classified_issue):
    ticket_summary = {
        "summarized_issue": intermediate_output["summarized_issue"],
        "sentiment": intermediate_output["sentiment"],
        "urgency_level": intermediate_output["urgency_level"]
    }
    final_output= {
        "ticket_id": ticket1["ticket_id"],
        "customer_details": {
            "customer_tier": ticket1["customer_tier"],
            "previous_tickets": ticket1["previous_tickets"],
            "monthly_revenue": ticket1["monthly_revenue"],
            "account_age_days": ticket1["account_age_days"]
        },
        "ticket_details": ticket_summary,
        "issue_routing": classified_issue.model_dump()
    }

    return final_output


print(json.dumps(combine_ticket_results(ticket, intermediate_output, classified_issue), indent=2))
