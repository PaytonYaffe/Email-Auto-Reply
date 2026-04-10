from . import models

def retrieve_all_inquiry_questions():
    all_inquiry_questions = models.InquiryQuestion.objects.all()
    print(f"### ### ### {all_inquiry_questions=}")
    return all_inquiry_questions

def save_inquiry_question(questions: list, email_content: str):
    # Create EmailInquiry object
    email_inquiry = models.EmailInquiry(email_content=email_content)
    email_inquiry.save()

    # Create InquiryQuestion objects for each question
    for question in questions:
        inquiry_question = models.InquiryQuestion(
            question=question,
            email_inquiry=email_inquiry
        )
        inquiry_question.save()

    return email_inquiry