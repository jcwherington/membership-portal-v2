require_relative 'services/ses'
require_relative 'services/s3'
# require_relative 'common/validation'
require 'liquid'

def handler(event:, context:)
    recipient = event['Records'][0]['Sns']['MessageAttributes']['Recipient']['Value']

    template_variables = {
        'name' => event['Records'][0]['Sns']['MessageAttributes']['Name']['Value'],
        'outcome' => event['Records'][0]['Sns']['MessageAttributes']['Outcome']['Value']
    }

    s3 = S3.new
    template_data = s3.get_template()

    liquid_template = Liquid::Template.parse(template_data)
    html_data = liquid_template.render(template_variables)

    ses = Ses.new
    ses.send_email(recipient:, html_data:)

    { statusCode: 200, body: 'Email sent' }
end
