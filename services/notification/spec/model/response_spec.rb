# frozen_string_literal: true

require_relative '../../src/model/response'

RSpec.describe Response do
  describe "resolve" do
    it "returns a response object" do
      response = Response.new(200, 'message')
      expected_result = { statusCode: 200, body: 'message' }

      expect(response.resolve).to eq(expected_result)
    end
  end
end
