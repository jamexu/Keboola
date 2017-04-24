import requests
import json
# Code below should be transferable for other typeform responses, not only the test data

# API_KEY and UID as string so it is easily replaceable if making different  requests
API_key = 'ac83034cfa742c0f79c26e9a612b4ba7e2aa0d3d'
Uid = 'PfSNFM'

url = 'https://api.typeform.com/v1/form/{}?key={}'
response = requests.get(url.format(Uid, API_key))

# if response is 200
if response.ok:
    # List of question IDs to be used to gather responses
    Question_IDs = []

    # Generate json from response
    Data = json.loads(response.content)

    # Generate IDs for the questions and appends to Question_IDs list
    for entries in Data['questions']:
        Question_IDs.append(entries['id'])

    # Generate CSV file with no header (response data start from row 1)
    outfile = open('output.csv', 'w')

    # Gets responses based on the Questions IDs present in list
    for values in Data['responses']:
        for x in range(0, len(Question_IDs)):
            # If response field is not empty
            try:
                if x == len(Question_IDs) - 1:
                    # if last response, no need to add comma before new line
                    # strip address field of commas and newlines
                    answers = (values['answers'][Question_IDs[x]]).replace(',', ' ').replace('\n', '')
                    outfile.write(answers)
                else:
                    outfile.write(values['answers'][Question_IDs[x]])
                    outfile.write(', ')

            except KeyError:
                # If the response field is empty, than insert NaN into record
                if x == len(Question_IDs) - 1:
                    outfile.write('NaN')
                else:
                    outfile.write('NaN, ')
        outfile.write('\n')

    outfile.close()

# if request failed
else:
    print "Error making request"
    print response