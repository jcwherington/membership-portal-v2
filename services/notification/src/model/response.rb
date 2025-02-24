# frozen_string_literal: true

class Response
  def initialize(statusCode, body)
    @statusCode = statusCode
    @body = body
  end

  def resolve
    { statusCode: @statusCode, body: @body }
  end
end
