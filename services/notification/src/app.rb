require_relative 'ses/ses'

def handler(event:, context:)
    ses = Ses.new
    puts ses.inspect
end