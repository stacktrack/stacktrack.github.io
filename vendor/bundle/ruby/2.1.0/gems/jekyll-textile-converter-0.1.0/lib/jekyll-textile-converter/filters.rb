module Jekyll
  module Filters
    # Convert a Textile string into HTML output.
    #
    # input - The Textile String to convert.
    #
    # Returns the HTML formatted String.
    def textilize(input)
      site = @context.registers[:site]
      converter = if site.respond_to?(:find_converter_instance)
        site.find_converter_instance(Jekyll::Converters::Textile)
      else
        site.getConverterImpl(Jekyll::Converters::Textile)
      end
      converter.convert(input)
    end
  end
end
