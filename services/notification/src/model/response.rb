# frozen_string_literal: true

class Response
  def initialize(status_code, body)
    @status_code = status_code
    @body = body
  end

  def resolve
    { status_code: @status_code, body: @body }
  end
end
