FROM python:3.10

WORKDIR /gde_project
COPY . /gde_project/

#install dependencies 
RUN sudo apt-get update && apt-get install -y \
  wget \
  unzip \
  curl \
  gnupg \
  --no-install-recommends

#install Firefox 
ARG FIREFOX_VERSION=55.0.3
RUN sudo apt-get update -qqy \
&& apt-get -qqy --no-install-recommends install firefox \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/* \
  && wget --no-verbose -O /tmp/firefox.tar.bz2 https://download-installer.cdn.mozilla.net/pub/firefox/releases/$FIREFOX_VERSION/linux-x86_64/en-US/firefox-$FIREFOX_VERSION.tar.bz2 \
  && apt-get -y purge firefox \
  && rm -rf /opt/firefox \
  && tar -C /opt -xjf /tmp/firefox.tar.bz2 \
  && rm /tmp/firefox.tar.bz2 \
  && mv /opt/firefox /opt/firefox-$FIREFOX_VERSION \
  && ln -fs /opt/firefox-$FIREFOX_VERSION/firefox /usr/local/bin/firefox

#install geckodriver (for firefox) web-driver
ARG GECKODRIVER_VERSION=0.18.0
RUN wget --no-verbose -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v$GECKODRIVER_VERSION/geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz \
  && rm -rf /opt/geckodriver \
  && tar -C /opt -zxf /tmp/geckodriver.tar.gz \
  && rm /tmp/geckodriver.tar.gz \
  && mv /opt/geckodriver /opt/geckodriver-$GECKODRIVER_VERSION \
  && chmod 755 /opt/geckodriver-$GECKODRIVER_VERSION \
  && ln -fs /opt/geckodriver-$GECKODRIVER_VERSION /usr/local/bin/geckodriver

#install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#set up environment variables for Firefox and Geckodriver
ENV FIREFOX_PATH=/usr/local/bin/firefox
ENV GECKODRIVER_PATH=/usr/local/bin/geckodriver

#Ensure geckodriver is in PATH
ENV PATH=$PATH:/usr/local/bin

CMD ["sh"]