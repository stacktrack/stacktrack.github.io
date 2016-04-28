require 'jekyll'

root = File.expand_path('jekyll-textile-converter', File.dirname(__FILE__))
require "#{root}/filters"
require "#{root}/version"

require File.expand_path('jekyll/converters/textile', File.dirname(__FILE__))

module Jekyll
  module TextileConverter
  end
end
