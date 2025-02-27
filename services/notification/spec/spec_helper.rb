# frozen_string_literal: true

require 'json'

RSpec.configure do |config|
  config.before(:each) do
    Logger.new('/dev/null')

    allow_any_instance_of(Logger).to receive(:info)
    allow_any_instance_of(Logger).to receive(:debug)
    allow_any_instance_of(Logger).to receive(:warn)
    allow_any_instance_of(Logger).to receive(:error)
    allow_any_instance_of(Logger).to receive(:fatal)
  end
end

def test_event
  JSON.parse(File.read('events/example.json'))
end

def test_email_template
  File.read('templates/outcome_email.html')
end

def test_template_path
  'templates/outcome_email.html'
end
