# frozen_string_literal: true

require 'json'

def test_event
  JSON.parse(File.read('events/example.json'))
end
