#! /bin/bash

function create_jenkins_container(){
	echo "Creating the container..."
	
	docker container run \
        	--publish 8080:8080 \
        	--detach \
        	--name jenkins \
        	--volume /var/run/docker.sock:/var/run/docker.sock \
        	--volume jenkins_home:/var/jenkins_home \
        	jenkinsci/blueocean
	
	echo "Jenkins container created"
}


function extract_initial_admin_password(){
	echo "Getting the initial_admin_password..."
	
	touch .jenkins_initialAdminPassword

	docker container exec jenkins /bin/bash -c "cat /var/jenkins_home/secrets/initialAdminPassword" > .jenkins_initialAdminPassword

	echo "initial_admin_password can be found at .jenkins_initialAdminPassword"
}

function make_docker_gid_equal(){

	# If an error of the kind: some_gid_already_exists shows,
	# this means that the 'docker' group on your HOST has the
	# has the same GID as an already existing group in container.
	# exec -it /bin/bash to go into the container,
        # check for a GID that is NOT used by anything (e.g. 990 ),
        # change your HOST's 'docker' group to have the new GID,
        # remove the container and run the script again.
        # NOTE: if running with a non-root user, assign the NEW
        # 'docker' GID to the that user and re-login, so the change
        # takes effect.	
	
	
	# get the entire line for the host's
	# 'docker' group from the /etc/group file:
	FULL_INFO=$(getent group docker)

	# create a temporary 'internal field separator',
	# so FULL_INFO can be turned into an array (delimeter ':'):
	local IFS=':'
	
	# create the array from FULL_INFO:
	read -ra FULL_INFO_ARRAY <<< $FULL_INFO
	
	# get only the GID of the host's 'docker' group: 
	HOST_DOCKER_GID=${FULL_INFO_ARRAY[2]}

	# the name of Jenkins container:
	JENKINS_CONTAINER_NAME=$1

	echo "Changing the 'docker' GID in the container..."

	# delete the container's OLD 'docker' group and
	# create the container's NEW 'docker' group
	# with the same GID with the host's 'docker' group:
	docker container exec --user=root $JENKINS_CONTAINER_NAME /bin/bash -c "delgroup docker && addgroup --gid $HOST_DOCKER_GID docker"

	echo "Changed the 'docker' GID in the container"
}



create_jenkins_container

extract_initial_admin_password

make_docker_gid_equal jenkins
