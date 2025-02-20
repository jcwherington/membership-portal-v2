def region
    'us-west-2'
end

def stage
    ENV['STAGE']
end

def sender
    ENV['SENDER']
end

def template_bucket
    'mpv2-email-templates'
end

def local
    ENV['STAGE'] == 'local'
end

def template_path
    local() ? './outcome_email.html' : "outcome_email_#{stage()}"
end
