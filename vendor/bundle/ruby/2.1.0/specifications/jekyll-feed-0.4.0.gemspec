# -*- encoding: utf-8 -*-
# stub: jekyll-feed 0.4.0 ruby lib

Gem::Specification.new do |s|
  s.name = "jekyll-feed".freeze
  s.version = "0.4.0"

  s.required_rubygems_version = Gem::Requirement.new(">= 0".freeze) if s.respond_to? :required_rubygems_version=
  s.require_paths = ["lib".freeze]
  s.authors = ["Ben Balter".freeze]
  s.date = "2015-12-30"
  s.email = ["ben.balter@github.com".freeze]
  s.homepage = "https://github.com/jekyll/jekyll-feed".freeze
  s.licenses = ["MIT".freeze]
  s.rubygems_version = "2.6.2".freeze
  s.summary = "A Jekyll plugin to generate an Atom feed of your Jekyll posts".freeze

  s.installed_by_version = "2.6.2" if s.respond_to? :installed_by_version

  if s.respond_to? :specification_version then
    s.specification_version = 4

    if Gem::Version.new(Gem::VERSION) >= Gem::Version.new('1.2.0') then
      s.add_development_dependency(%q<jekyll>.freeze, ["< 3.1.0", ">= 2.4.0"])
      s.add_development_dependency(%q<bundler>.freeze, ["~> 1.6"])
      s.add_development_dependency(%q<rake>.freeze, ["~> 10.0"])
      s.add_development_dependency(%q<rspec>.freeze, ["~> 3.0"])
      s.add_development_dependency(%q<typhoeus>.freeze, ["~> 0.7"])
      s.add_development_dependency(%q<nokogiri>.freeze, ["~> 1.6"])
      s.add_development_dependency(%q<jekyll-last-modified-at>.freeze, ["= 0.3.4"])
    else
      s.add_dependency(%q<jekyll>.freeze, ["< 3.1.0", ">= 2.4.0"])
      s.add_dependency(%q<bundler>.freeze, ["~> 1.6"])
      s.add_dependency(%q<rake>.freeze, ["~> 10.0"])
      s.add_dependency(%q<rspec>.freeze, ["~> 3.0"])
      s.add_dependency(%q<typhoeus>.freeze, ["~> 0.7"])
      s.add_dependency(%q<nokogiri>.freeze, ["~> 1.6"])
      s.add_dependency(%q<jekyll-last-modified-at>.freeze, ["= 0.3.4"])
    end
  else
    s.add_dependency(%q<jekyll>.freeze, ["< 3.1.0", ">= 2.4.0"])
    s.add_dependency(%q<bundler>.freeze, ["~> 1.6"])
    s.add_dependency(%q<rake>.freeze, ["~> 10.0"])
    s.add_dependency(%q<rspec>.freeze, ["~> 3.0"])
    s.add_dependency(%q<typhoeus>.freeze, ["~> 0.7"])
    s.add_dependency(%q<nokogiri>.freeze, ["~> 1.6"])
    s.add_dependency(%q<jekyll-last-modified-at>.freeze, ["= 0.3.4"])
  end
end
