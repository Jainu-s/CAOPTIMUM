import spacy


def split_instructions_to_steps(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    actions = []
    current_action = ""
    for token in doc:
        if token.dep_ == "nsubj":
            actions.append(current_action.strip())
            current_action = token.text
        else:
            current_action += " " + token.text

    actions.append(current_action.strip())

    # Remove empty strings from the list
    actions = list(filter(None, actions))

    return actions


# Example usage:
# paragraph = "Launch the URL. Click on the 'Net Banking' button. Click on the 'LOGIN' button and add the text 'PERSONAL.'"
# paragraph += " Click on the 'CONTINUE TO LOGIN' button. Enter your username. Enter your password. Click the 'Login' button."
# paragraph += " Enter the one-time password or OTP received on your mobile. Click the 'submit' button. Click on the 'Payments / Transfers' button."
# paragraph += " Choose 'Quick Transfer (Without Adding Beneficiary)' from the options. Enter the Beneficiary Name. Enter the Beneficiary Account Number."
# paragraph += " Re-enter the Beneficiary Account Number. Select the 'Within SBI' option. Enter the amount. Choose 'Rent' as the purpose."
# paragraph += " Finally, accept the terms & conditions by clicking on the checkbox."

paragraph = '''
First launch the url and click on "Net Banking" button. Now click on "LOGIN" button add_text PERSONAL, Now click on "CONTINUE TO LOGIN" button. You will see a username field there now enter username, enter password and click "Login" button. Now enter one time password or OTP received to your mobile, click "submit" button. Now click on "Payments / Transfers" button, and click on "Quick Transfer (Without Adding Beneficiary)" option. Enter Beneficiary Name, enter Beneficiary Account Number, Re-enter Beneficiary Account Number, select "Within SBI" option, now enter the amount and also choose rent "Rent" option in purpose.Finally accept the terms & conditions by clicking on checkbox.
'''

steps = split_instructions_to_steps(paragraph)
for index, step in enumerate(steps, 1):
    print(f"{index}. {step}")
