# GameCraft Site MK III

Written in Django. Why? Lots of plugins and docs.

Why not flask? Less plugins and seems to have stalled somewhat.

## Hosting

The plan is to run as docker images on a super cheat (tm) Digital Ocean VM. With luck and smart caching we can run for $5 a month! Throw in another server and we can have redundancy for $10 a month :)

## Development

The other reason to use Docker is it makes it easier to get going with a Vagrant VM which more closely apes the real site.

In theory (tm) you can:

1. vagrant up
2. make (does a docker build)
3. make runserver (docker run gamecraft)

All you need is vagrant and a VM provider (virtualbox, vmware or hyperv on windows).
