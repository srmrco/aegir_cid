from fabric.api import *
import time

env.user = 'aegir'
env.shell = '/bin/bash -c'

# Fetch a fully constructed platform from the workplace and place it in Aegir's plaforms folder
def fetch_platform(site, profile, webserver, dbserver, platform, build):
  print "===> Fetching the latest version of a platform from the Workspace..."
  run("cp -r %s /var/aegir/platforms/%s" % (platform, build))
  run("drush --root='/var/aegir/platforms/%s' provision-save '@platform_%s' --context_type='platform'" % (build, build))
  run("drush @hostmaster hosting-import '@platform_%s'" % build)
  run("drush @hostmaster hosting-dispatch")

# Download and import a platform using Drush Make
def build_platform(site, profile, webserver, dbserver, platform, build):
  print "===> Building the platform..."
  run("drush make %s /var/aegir/platforms/%s" % (platform, build))
  run("drush --root='/var/aegir/platforms/%s' provision-save '@platform_%s' --context_type='platform'" % (build, build))
  run("drush @hostmaster hosting-import '@platform_%s'" % build)
  run("drush @hostmaster hosting-dispatch")

# Install a site on a platform, and kick off an import of the site
def install_site(site, profile, webserver, dbserver, platform, build):
  print "===> Installing the site for the first time..."
  time.sleep(5)
  run("drush @%s provision-install" % site)
  run("drush @hostmaster hosting-task @platform_%s verify" % build)
  time.sleep(5)
  run("drush @hostmaster hosting-dispatch")
  time.sleep(5)
  run("drush @hostmaster hosting-task @%s verify" % site)

# Migrate a site to a new platform
def migrate_site(site, profile, webserver, dbserver, platform, build):
  print "===> Migrating the site to the new platform"
  run("drush @%s provision-migrate '@platform_%s'" % (site, build))

# Save the Drush alias to reflect the new platform
def save_alias(site, profile, webserver, dbserver, platform, build):
  print "===> Updating the Drush alias for this site"
  run("drush provision-save @%s --context_type=site --uri=%s --platform=@platform_%s --server=@server_%s --db_server=@server_%s --profile=%s --client_name=a$

# Import a site into the frontend, so that Aegir learns the site is now on the new platform
def import_site(site, profile, webserver, dbserver, platform, build):
  print "===> Refreshing the frontend to reflect the site under the new platform"
  run("drush @hostmaster hosting-import @%s" % site)
  run("drush @hostmaster hosting-task @platform_%s verify" % build)
  run("drush @hostmaster hosting-import @%s" % site)
  run("drush @hostmaster hosting-task @%s verify" % site)
