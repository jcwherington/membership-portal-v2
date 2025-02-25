FROM public.ecr.aws/lambda/ruby:3.2 AS local

EXPOSE 8080 
WORKDIR /var/task

COPY Gemfile ./
RUN bundle config set --local path 'vendor/bundle' && \
    bundle install --without test
COPY src templates ./

CMD ["app.handler"]

FROM ruby:3.2.7-slim AS test

WORKDIR /app

COPY Gemfile ./
RUN bundle install
COPY src ./src
COPY spec ./spec
COPY templates ./templates
COPY events ./events

CMD [ "/bin/bash", "-c", "rspec" ]

FROM ruby:3.2.7-slim AS build

WORKDIR /app

COPY Gemfile ./
RUN apt-get update && apt-get install zip -y --no-install-recommends && apt-get clean
RUN bundle config set --local path 'vendor/bundle' && \
    bundle install --without test
COPY src ./

CMD ["/bin/sh", "-c", "zip -q -r build/notification.zip . -x 'Gemfile' 'Gemfile.lock' './build/*'"]
