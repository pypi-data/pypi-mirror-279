import sys, os
## Code to disable creating pycache dir after running
sys.dont_write_bytecode = True
###################################################

sys.path.append(os.path.abspath(f"{os.getcwd()}/src/"))

import redhat_assisted_installer.assisted_installer as assisted_installer

installer = assisted_installer.assisted_installer()

try:
    cluster = installer.post_cluster("ocp-testing", "4.15")
    installer.delete_cluster(cluster['id'])

    clusters = installer.get_clusters()
    print(clusters)
except Exception as e:
    print(e)



