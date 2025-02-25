# frozen_string_literal: true

require 'json'

def test_event
  JSON.parse(File.read('events/example.json'))
end

def test_email_template
  File.read('templates/outcome_email.html')
end
