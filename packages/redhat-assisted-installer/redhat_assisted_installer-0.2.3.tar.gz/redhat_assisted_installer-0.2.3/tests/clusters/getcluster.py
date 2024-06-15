import sys, os
## Code to disable creating pycache dir after running
sys.dont_write_bytecode = True

sys.path.append(os.path.abspath(f"{os.getcwd()}/src/"))

from redhat_assisted_installer.assisted_installer import assisted_installer


installer = assisted_installer()

cluster = installer.get_clusters(cluster_id="72d3187a-8997-4c14-a78d-dfee19f5a295")

# clusters = installer.get_clusters()