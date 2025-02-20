require 'aws-sdk-ses'
require_relative '../config'

class Ses
  def initialize
    @client = Aws::SES::Client.new(region: region())
  end

  def send_email(recipient:, html_data:)
    email_params = {
      source: sender(),
      destination: {
        to_addresses: [recipient]
      },
      message: {
        subject: {
          data: 'Application Outcome'
        },
        body: {
          html: {
            data: html_data
          }
        }
      }
    }

    begin
      response = @client.send_email(email_params)
      puts "Email sent successfully! Message ID: #{response}"
    rescue Aws::SES::Errors::ServiceError => error
      puts "Failed to send email: #{error.message}"
    end
  end
end
