# frozen_string_literal: true

class ValidationError < StandardError
  def initialize(message)
    super(message)
    @status = 400
  end

  def status
    @status
  end
end

class ServiceError < StandardError
  def initialize(message)
    super(message)
    @status = 500
  end

  def status
    @status
  end
end
