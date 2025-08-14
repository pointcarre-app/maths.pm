
Gandi default ?
The DNS record @ with the value 155.133.142.16 will be deleted.





from: https://gist.github.com/matt-bailey/bbbc181d5234c618e4dfe0642ad80297


How to set up DNS records on gandi.net to use a custom domain on Github Pages
You would think it would be easy to find this information, but none of the Github or Gandi documentation is clear so I have recorded the required steps here.

Create the following A records:

@ 1800 IN A 185.199.108.153
@ 1800 IN A 185.199.109.153
@ 1800 IN A 185.199.110.153
@ 1800 IN A 185.199.111.153
Remove the Gandi parking page A record:

@ 10800 IN A 217.70.184.38
Create the following CNAME record:

www 10800 IN CNAME [github-username].github.io.
Remove the Gandi parking page CNAME record:

www 1800 IN CNAME webredir.vip.gandi.net.
Finally, in your Github repo create a file called CNAME which contains your Gandi domain name, e.g. [my-domain].io.