require File.dirname(__FILE__) + '/spec_helper'

RSpec.describe(Jekyll::Filters) do
  class JekyllFilter
    include Jekyll::Filters
    attr_accessor :site, :context

    def initialize(opts = {})
      @site = Jekyll::Site.new(Jekyll::Configuration::DEFAULTS)
      @context = Liquid::Context.new({}, {}, { :site => @site })
    end
  end

  let(:filter) { JekyllFilter.new }

  it "should convert textile" do
    expect(filter.textilize("something *really* simple")).to eq("<p>something <strong>really</strong> simple</p>")
  end
end
