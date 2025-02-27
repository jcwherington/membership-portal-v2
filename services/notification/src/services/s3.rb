# frozen_string_literal: true

require 'aws-sdk-s3'
require_relative '../config'
require_relative '../common/error'

class S3
  def initialize
    @client = Aws::S3::Client.new(region: region)
    @template = template_path
  end

  def template
    return File.read(@template) if local

    response = @client.get_object(bucket: template_bucket, key: @template)

    response.body.read
  rescue Aws::S3::Errors::ServiceError => e
    raise ServiceError, e.message
  end
end
