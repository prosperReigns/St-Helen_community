from core.models import Response, User

def get_responses (user):
    responses = Response.objects.filter(user=user) #gets each response (from response model)
    return{response.question_id: response.option_id for response in responses} #returns all the user's responses to each question in a dictionary 

def calculate_match_score (student_a, student_b):
    responses_a = get_responses(student_a)
    responses_b = get_responses(student_b)

    score = 0 

    for question_id, option_id_a in responses_a.items(): #iterates through all the questions and responses for a student  
        option_id_b = responses_b.get(question_id) #gets the question_id of the question, to find the correct option

        if question_id == 1: #the 1st question (asks what year group they are in) ~greatest influence
            if option_id_a == option_id_b:
                score += 3
        
        elif question_id == 5: #the 5th question (asks what personality type they have) ~medium influence
            if option_id_a == option_id_b:
                score += 2
        else: #all other questions
            if option_id_a == option_id_b:
                score += 1
    
    return score