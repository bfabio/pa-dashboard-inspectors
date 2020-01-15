#!/usr/bin/env ruby

require 'json'
require 'net/http'

TESTSSL="~/dev/testssl.sh/testssl.sh"

hosts_uri = URI(File.read('../../HOSTS_URL').strip)
reports_endpoint = URI.join(hosts_uri, '/reports')

loop do
    begin
      res = Net::HTTP.get(hosts_uri)
    rescue StandardError
      next
    end

    hosts = JSON.parse(res)

    hosts.each do |host|
        uri = URI(host)
        out_file = "/tmp/vulnerabilities.rb.#{uri.hostname}.json"

        File.delete(out_file) if File.exist?(out_file)

        status = system("#{TESTSSL} -s -B --jsonfile #{out_file} #{uri.hostname}")
        next unless status

        report = JSON.load(File.read(out_file))

        # Filter out testssl own checks
        report.reject!{|r| r['id'] =~ /^(engine_problem|service|scanTime)/ }

        puts report.to_json

        begin
            Net::HTTP.post reports_endpoint,
                           report.to_json,
                           'Content-Type' => 'application/json'
        rescue StandardError => e
            STDERR.puts "#{uri.hostname}\n#{e}"
            next
        end
    end

    sleep 60
end
