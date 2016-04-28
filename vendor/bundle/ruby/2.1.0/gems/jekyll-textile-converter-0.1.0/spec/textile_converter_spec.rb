require File.dirname(__FILE__) + '/spec_helper'

RSpec.describe(Jekyll::Converters::Textile) do
  let(:configs)   { Hash.new }
  let(:converter) { described_class.new(configs) }

  context "configuration" do

    context "`redcloth`" do
      context "no explicit config" do
        it "preserves single line breaks in HTML output" do
          expect(converter.convert("p. line1\nline2").strip).to eq("<p>line1<br />\nline2</p>")
        end
      end

      context "empty redcloth config" do
        let(:configs)   { {'redcloth' => Hash.new} }

        it "preserves single line breaks in HTML output" do
          expect(converter.convert("p. line1\nline2").strip).to eq("<p>line1<br />\nline2</p>")
        end
      end

      context "explicity enabled hard_breaks" do
        let(:configs) { {'redcloth' => {'hard_breaks' => true}} }

        it "preserves single line breaks in HTML output" do
          expect(converter.convert("p. line1\nline2").strip).to eq("<p>line1<br />\nline2</p>")
        end
      end

      context "explicity disabled hard_breaks" do
        let(:configs) { {'redcloth' => {'hard_breaks' => false}} }

        it "does not generate break tags in HTML output" do
          expect(converter.convert("p. line1\nline2").strip).to eq("<p>line1\nline2</p>")
        end
      end

      context "explicity disabled no_span_caps" do
        let(:configs) { {'redcloth' => {'no_span_caps' => false}} }

        it "generates span tags around capitalized words" do
          expect(converter.convert("NSC").strip).to eq("<p><span class=\"caps\">NSC</span></p>")
        end
      end

      context "explicitly enabled no_span_caps" do
        let(:configs) { {'redcloth' => {'no_span_caps' => true}} }

        it "does generates span tags around capitalized words" do
          expect(converter.convert("NSC").strip).to eq("<p>NSC</p>")
        end
      end
    end

    context "`textile_ext`" do
      context "with a custom list including the default" do
        let(:configs) { {'textile_ext' => 'textile,text'} }

        it "matches the new ext" do
          expect(converter.matches('.text')).to be_truthy
        end

        it "matches the old ext" do
          expect(converter.matches('.textile')).to be_truthy
        end
      end

      context "with a replacement ext" do
        let(:configs) { {'textile_ext' => 'text'} }

        it "matches the new ext" do
          expect(converter.matches('.text')).to be_truthy
        end

        it "doesn't match the old ext" do
          expect(converter.matches('.textile')).to be_falsy
        end
      end
    end
  end

  context "in code blocks" do
    let(:content) do
      <<-CONTENT
_FIGHT!_

{% highlight ruby %}
puts "3..2..1.."
{% endhighlight %}

*FINISH HIM*
CONTENT
    end

    # Broken in RedCloth 4.1.9
    it "does not textilize highlight block" do
      expect(converter.convert(content)).not_to match(%r{3\.\.2\.\.1\.\.&quot;</span><br />})
    end
  end

end
