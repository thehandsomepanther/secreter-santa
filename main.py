from munkres import Munkres
import random
from print_matrix import *
from credentials import *
import json
import smtplib
from smtplib import SMTPException
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def main(debug=False):
    m = Munkres()

    A = []
    B = []
    santas = []

    with open('santa.json') as json_file:
        data = json.load(json_file)
        last_year = 0

        for person in data:
            years = []

            for key in data[person]['matches'].keys():
                years.append(int(key))

            last_year = max(last_year, max(years))

            santas.append(person)

            person_a = person + '_A'
            A.append(person_a)

            person_b = person + '_B'
            B.append(person_b)

        matrix = [[0 for x in range(len(A))] for x in range(len(A))]

        for i in range(len(A)):
            for j in range(len(B)):
                person_a = A[i][:-2]
                person_b = B[j][:-2]

                cost = 0
                scale = 100 / last_year

                if person_a != person_b:
                    if data[person_a]['matches'][str(last_year - 1)] != person_b:
                        repeats = 0
                        for key in data[person_a]['matches'].keys():
                            if data[person_a]['matches'][key] == person_b:
                                repeats += 1
                        cost = repeats * scale + random.random() * scale
                    else:
                        cost = 100
                else:
                    cost = 100

                matrix[i][j] = cost

        indices = m.compute(matrix)

        # Munkres matrix
        if debug:
            print_matrix(matrix, msg='Secret Santa costs: ')

        total = 0
        for row, column in indices:
            value = matrix[row][column]
            total += value

            if debug:
                # Santa -(cost)-> Assignee
                print '{} -({})-> {}'.format(santas[row], value, santas[column])
            else:
                sender = email
                receiver = data[santas[row]]['email']
                message = MIMEMultipart('alternative')

                message['Subject'] = 'Secret Santa Assignment'
                message['From'] = email
                message['To'] = receiver

                text = 'Ho, ho, ho. You have been assigned {}.'.format(santas[column])
                message.attach(MIMEText(text, 'plain'))

                try:
                    session = smtplib.SMTP('smtp.gmail.com', 587)
                    session.ehlo()
                    session.starttls()
                    session.login(email, password)
                    session.sendmail(sender, receiver, message.as_string())
                    session.close()
                except SMTPException:
                    print 'Error: unable to send email'

        print 'Secret Santa assignment done.'
        if debug:
            print 'total cost: %d' % total

if __name__ == '__main__':
    debug = False

    if len(sys.argv) > 1 and sys.argv[1] == '--debug':
        debug = True

    main(debug)
