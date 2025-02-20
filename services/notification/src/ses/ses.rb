require 'aws-sdk-ses'
require_relative '../config'

class Ses
  def initialize
    @client = Aws::SES::Client.new(region: region())
  end

#   def send_email(from:, to:, subject:, body:)
#     # Email parameters
#     email_params = {
#       source: from,
#       destination: {
#         to_addresses: [to]
#       },
#       message: {
#         subject: {
#           data: subject
#         },
#         body: {
#           text: {
#             data: body
#           }
#         }
#       }
#     }

#     begin
#       # Send the email using SES
#       response = @ses.send_email(email_params)
#       puts "Email sent successfully! Message ID: #{response.message_id}"
#     rescue Aws::SES::Errors::ServiceError => error
#       # Handle errors
#       puts "Failed to send email: #{error.message}"
#     end
#   end
end