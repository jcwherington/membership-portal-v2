# frozen_string_literal: true

require_relative '../../src/app'
require_relative '../../src/common/error'
require_relative '../../src/services/s3'
require_relative '../../src/services/ses'
require_relative '../spec_helper'

RSpec.describe 'app' do
  before do
    @test_event = test_event()
    @test_email_template = test_email_template()
  end

  describe 'handler' do
    let(:s3) { instance_double('S3', get_template: @test_email_template) }
    let(:ses) { instance_double('Ses', send_email: nil) }

    context 'with a valid event' do
      it 'returns a 200 response' do
        allow(S3).to receive(:new).and_return(s3)
        allow(Ses).to receive(:new).and_return(ses)

        expected_result = { statusCode: 200, body: 'Email sent successfully' }

        expect(handler(event: @test_event, context: {})).to eq(expected_result)
      end
    end

    context 'with an invalid event' do
      it 'returns a 400 response' do      
        event = @test_event.dup
        event.delete('Records')

        expected_result = { statusCode: 400, body: 'invalid event object' }

        expect(handler(event:, context: {})).to eq(expected_result)
      end
    end

    context 'when a service error occurs' do
      it 'returns a 500 response' do
        allow(S3).to receive(:new).and_raise(ServiceError.new('service error'))

        expected_result = { statusCode: 500, body: 'service error' }

        expect(handler(event: @test_event, context: {})).to eq(expected_result)
      end
    end
  end
end
