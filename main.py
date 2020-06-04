#!/usr/bin/python3
from __future__ import print_function, unicode_literals
from PyInquirer import prompt, style_from_dict, Token, Separator
from procedure import Scraping_Kit
import printing
import re

def choice():
    questions = [
    {
        'type': 'list',
        'name': 'first_choice',
        'message': 'What do you want to do?',
        'choices': [
            {
                'name':'View saved data from previous sessions'
            },
            {
                'name':'Start new session'
            }
        ]
        # 'validate': lambda answer: 'You must choose at least one option.' \
            # if len(answer) == 0 else True
    }
    ]
    answers = prompt(questions)
    print(answers)
        
def take_input():
    check = '^[a-z0-9]+[\._]?[a-z0-9]+@\w+\.\w{2,3}$'
    custom_style_2 = style_from_dict({
        Token.Separator: '#6C6C6C',
        Token.QuestionMark: '#FFFFFF bold',
        # Token.Selected: '',  # default
        Token.Selected: '#5F819D',
        Token.Pointer: '#FF9D00 bold',
        Token.Instruction: '',  # default
        Token.Answer: '#5F819D bold',
        Token.Question: '#FFA500',
    })
    questions = [
    {
        'type': 'input',
        'name': 'email',
        'message': "What is the target's email-id:",
    }
    ]
    ran_once_unsuccessfully=False
    target_email = ""
    while not re.search(check, target_email):
        if ran_once_unsuccessfully:
            print(printing.colors.fg.yellow,"Invalid email please try again")
        target_email = prompt(questions, style=custom_style_2)['email']
        ran_once_unsuccessfully=True

    return target_email

if __name__=="__main__":
    printing.intro()
    choice()
    # target = take_input()
    # do = Scraping_Kit(target)
    # do.headless_selenium()
    # do.sherly()
    # do.instagram()
    # do.twitter()
    # do.facebook()
    # do.findName()
    # do.decapitate()
