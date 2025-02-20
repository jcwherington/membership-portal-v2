require 'aws-sdk-s3'
require_relative '../config'

class S3
  def initialize
    @client = Aws::S3::Client.new(region: region())
    @template = template_path()
  end

  def get_template
    begin
      puts File.read(@template).inspect
      return File.read(@template) if local()

      response = @client.get_object(bucket: template_bucket(), key: @template)
      return response.body.read
    rescue Aws::S3::Errors::ServiceError => error
      puts "Failed to get template: #{error.message}"
    end
  end
end
