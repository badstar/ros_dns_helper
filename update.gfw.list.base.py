import base64
import re
import urllib.request

url = "https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt"

content = urllib.request.urlopen(url).read()

decoded_content = base64.b64decode(content).decode("utf-8")

manipulated_lines = []
lines = decoded_content.split("\n")
for line in lines:
    line = re.sub(r'^\|\|?', '', line)
    line = re.sub(r'https?:\/\/', '', line)
    line = re.sub(r'^\.', '', line)
    line = re.sub(r'\*.*', '', line)
    line = re.sub(r'\/.*', '', line)
    line = re.sub(r'%.*', '', line)
    if not re.match(r'^$|^!|^\@|^\[|\.$|^[^\.]*$|^[0-9\.]*$', line):
        manipulated_lines.append(line)

manipulated_lines = sorted(set(manipulated_lines))

# print(manipulated_lines)

def generate_rsc_file(dns_server, domain_list, file_path, nf_list, vip_domain):
    with open(file_path, "w", encoding="utf-8") as rsc_file:
        rsc_file.write(":global dnsserver \"%s\"\n" % dns_server)
        rsc_file.write("/ip dns static remove [/ip dns static find forward-to=$dnsserver]\n")
        rsc_file.write("/ip dns static\n")
        for domain in domain_list:
            if domain not in nf_list:
                rsc_file.write(
                    ":do { add forward-to=$dnsserver type=FWD address-list=gfw_list match-subdomain=yes name=%s } on-error={}\n" % (
                        domain))
        for domain in nf_list:
            rsc_file.write(
                ":do { add forward-to=$dnsserver type=FWD address-list=nf_list match-subdomain=yes name=%s } on-error={}\n" % (
                    domain))
        for domain in vip_domain:
            rsc_file.write(
                ":do { add forward-to=$dnsserver type=FWD address-list=gfw_list match-subdomain=yes name=%s } on-error={}\n" % (
                    domain))
        # rsc_file.write(
        #     '''/ip firewall address-list remove [/ip firewall address-list find list="nf_list"] \n'''
        # )
        rsc_file.write(
            '''/ip firewall address-list remove [/ip firewall address-list find list="gfw_list"] \n'''
        )
        print(file_path + " generated")

dns_server = "8.8.8.8"
domain_list = manipulated_lines
file_path = "gfw.domain.rsc"

nf_list = [
    'netflix.com',
    'netflix.net',
    'nflxext.com',
    'nflximg.com',
    'nflximg.net',
    'nflxsearch.net',
    'nflxso.net',
    'nflxvideo.net',
    'netflixdnstest0.com',
    'netflixdnstest1.com',
    'netflixdnstest2.com',
    'netflixdnstest3.com',
    'netflixdnstest4.com',
    'netflixdnstest5.com',
    'netflixdnstest6.com',
    'netflixdnstest7.com',
    'netflixdnstest8.com',
    'netflixdnstest9.com',
    'pandora.com',
    'tunein.com',
    'hbo.com',
    'hbonow.com',
    'hboasia.com',
    'hbogoasia.com',
    'hbogoasia.hk',
    'hbolb.onwardsmg.com',
    'hbounify-prod.evergent.com',
    'bcbolthboa-a.akamaihd.net',
    'amazonaws.com',
    'aws.amazon.com',
    'awsstatic.com',
    'fast.com',
    'hulu.com',
    'huluim.com',
    'hbogo.com',
    'openai.com',
    'challenges.cloudflare.com',
    'ai.com'
]

vip_domain = [
    '.me',
    '.hk',
    '.tw',
    '.jp',
    '.sg',
    '.ph',
    '.co'
]

generate_rsc_file(dns_server, domain_list, file_path, nf_list, vip_domain)

