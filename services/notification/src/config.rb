# frozen_string_literal: true

require 'logger'

def region
  'us-west-2'
end

def branch
  ENV['BRANCH']
end

def sender
  ENV['SENDER']
end

def template_bucket
  ENV['TEMPLATE_BUCKET']
end

def local
  ENV['BRANCH'] == 'local'
end

def template_path
  local ? './outcome_email.html' : "outcome_email_#{branch}.html"
end

def logger
  Logger.new($stdout)
end
