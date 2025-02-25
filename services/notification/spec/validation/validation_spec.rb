# frozen_string_literal: true

require_relative '../../src/common/validation'
require_relative '../../src/common/error'
require_relative '../spec_helper'

RSpec.describe 'validation' do
  before do
    @event = test_event()
    @message_attributes = @event['Records'][0]['Sns']['MessageAttributes']
  end

  describe 'validate_event' do
    context 'with a valid event object' do
      it 'does not raise a validation error' do
        expect { validate_event(event: @event) }.not_to raise_error
      end
    end

    context 'with an invalid event object' do
      let(:modified_event) { @event.dup }

      it 'raises a validation error when Records key is missing' do
        modified_event.delete('Records')

        expect { validate_event(event: modified_event) }.to raise_error(ValidationError)
      end

      it 'raises a validation error when EventSource is incorrect' do
        modified_event['Records'][0]['EventSource'] = 'wrong'

        expect { validate_event(event: modified_event) }.to raise_error(ValidationError)
      end

      it 'raises a validation error when MessageAttributes key is missing' do
        modified_event['Records'][0]['Sns'].delete('MessageAttributes')

        expect { validate_event(event: modified_event) }.to raise_error(ValidationError)
      end
    end
  end

  describe 'validate_message_attributes' do
    context 'with a valid MessageAttributes object' do
      it 'does not raise a validation error' do
        expect { validate_message_attributes(message_attributes: @message_attributes) }.not_to raise_error
      end
    end

    context 'with an invalid MessageAttributes object' do
      let(:modified_message_attributes) { @message_attributes.dup }

      it 'raises a validation error when Recipient key is missing' do
        modified_message_attributes.delete('Recipient')

        expect { validate_message_attributes(message_attributes: modified_message_attributes) }.to raise_error(ValidationError)
      end

      it 'raises a validation error when Name key is missing' do
        modified_message_attributes.delete('Name')

        expect { validate_message_attributes(message_attributes: modified_message_attributes) }.to raise_error(ValidationError)
      end

      it 'raises a validation error when Outcome key is missing' do
        modified_message_attributes.delete('Outcome')

        expect { validate_message_attributes(message_attributes: modified_message_attributes) }.to raise_error(ValidationError)
      end

      it 'raises a validation error when Recipient Value key is invalid' do
        modified_message_attributes['Recipient']['Value'] = 'invalid'

        expect { validate_message_attributes(message_attributes: modified_message_attributes) }.to raise_error(ValidationError)
      end

      it 'raises a validation error when Outcome Value key is invalid' do
        modified_message_attributes['Outcome']['Value'] = 'invalid'

        expect { validate_message_attributes(message_attributes: modified_message_attributes) }.to raise_error(ValidationError)
      end
    end
  end
end
