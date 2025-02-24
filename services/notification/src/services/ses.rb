# frozen_string_literal: true

require 'aws-sdk-ses'
require_relative '../config'
require_relative '../common/error'

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
    rescue Aws::SES::Errors::ServiceError => error
      raise ServiceError.new(error.message)
    end
  end
end
