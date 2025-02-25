# frozen_string_literal: true

require_relative '../../src/services/ses'
require_relative '../../src/common/error'
require_relative '../spec_helper'

RSpec.describe Ses do
  describe 'send_email' do
    let(:ses) { Ses.new() }
    let(:mock_client) { instance_double('Aws::SES::Client') }
    let(:recipient) { 'recipient' }
    let(:html_data) { '<p>data</p>' }

    it "sends the email" do
      allow(Aws::SES::Client).to receive(:new).and_return(mock_client)
      allow(mock_client).to receive(:send_email).and_return({})

      expect(ses.send_email(recipient:, html_data:)).to eq({})
    end

    it "raises ServiceError when aws returns an error" do
      allow(Aws::SES::Client).to receive(:new).and_return(mock_client)
      allow(mock_client).to receive(:send_email).and_raise(Aws::SES::Errors::ServiceError.new('error', {}))

      expect { ses.send_email(recipient:, html_data:) }.to raise_error(ServiceError)
    end
  end
end
