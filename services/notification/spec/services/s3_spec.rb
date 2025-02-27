# frozen_string_literal: true

require_relative '../../src/services/s3'
require_relative '../../src/common/error'
require_relative '../spec_helper'

RSpec.describe S3 do
  before do
    @test_email_template = test_email_template
    @test_template_path = test_template_path
  end

  describe 'template' do
    let(:s3) { S3.new }
    let(:mock_response) { instance_double('Aws::S3::Types::GetObjectOutput') }
    let(:mock_client) { instance_double('Aws::S3::Client') }

    it 'returns an email template' do
      allow(Aws::S3::Client).to receive(:new).and_return(mock_client)
      allow(mock_response).to receive(:body).and_return(double('Body', read: @test_email_template))
      allow(mock_client).to receive(:get_object).and_return(mock_response)

      expect(s3.template).to eq(@test_email_template)
    end

    it 'raises ServiceError when aws returns an error' do
      allow(Aws::S3::Client).to receive(:new).and_return(mock_client)
      allow(mock_client).to receive(:get_object).and_raise(Aws::S3::Errors::ServiceError.new('error', {}))

      expect { s3.template }.to raise_error(ServiceError)
    end

    context 'in local environment' do
      it 'reads from local file' do
        s3.instance_variable_set(:@template, @test_template_path)
        allow(s3).to receive(:local).and_return(true)

        expect(s3.template).to eq(@test_email_template)
      end
    end
  end
end
