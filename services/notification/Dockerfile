FROM public.ecr.aws/lambda/ruby:3.2 AS local

EXPOSE 8080 
WORKDIR /var/task
COPY Gemfile ./
RUN bundle install
COPY src ./

CMD ["app.handler"]
